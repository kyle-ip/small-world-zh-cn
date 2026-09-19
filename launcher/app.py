#!/usr/bin/env python3
"""
Small World 2 Chinese patch — all-in-one EXE.

Embeds Chinese resources; can install, toggle Chinese, and launch the game.
"""
from __future__ import annotations

import ctypes
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

if getattr(sys, "frozen", False):
    HERE = Path(sys.executable).resolve().parent
else:
    HERE = Path(__file__).resolve().parent
    sys.path.insert(0, str(HERE))

import payload_install  # noqa: E402
import steam_lang  # noqa: E402

APP_TITLE = "小小世界 · 中文补丁"
APP_VERSION = "2.1.2"
BG = "#ffffff"
SIDE = "#e8f2fc"
TEXT = "#1a1a1a"
MUTED = "#5c5c5c"
ACCENT = "#3278c8"
# Right panel content width (logical px before DPI scale)
MAIN_WIDTH = 420
MAIN_HEIGHT = 400


def _dpi_scale() -> float:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass
    try:
        return max(1.0, float(ctypes.windll.user32.GetDpiForSystem()) / 96.0)
    except Exception:
        return 1.0


def _font(scale: float, size: int, bold: bool = False):
    return ("Microsoft YaHei UI", max(9, int(round(size * scale))), "bold" if bold else "normal")


def _bundled_ico() -> Path | None:
    """SmallWorld.exe icon, packaged next to the frozen app resources."""
    candidates: list[Path] = []
    if getattr(sys, "frozen", False):
        meipass = Path(getattr(sys, "_MEIPASS", ""))
        candidates.append(meipass / "app.ico")
        candidates.append(HERE / "app.ico")
    candidates.append(Path(__file__).resolve().parent / "app.ico")
    for path in candidates:
        if path.is_file():
            return path
    return None


def _bundled_cover() -> Path | None:
    """Launcher left-panel art (cover.png)."""
    candidates: list[Path] = []
    if getattr(sys, "frozen", False):
        meipass = Path(getattr(sys, "_MEIPASS", ""))
        candidates.append(meipass / "cover.png")
        candidates.append(HERE / "cover.png")
    here = Path(__file__).resolve().parent
    candidates.append(here / "cover.png")
    # Dev convenience: game-root cover next to the repo
    candidates.append(here.parents[1] / "cover.png")
    for path in candidates:
        if path.is_file():
            return path
    return None


def _resolve_game_dir() -> Path:
    try:
        game = steam_lang.find_game_dir()
        if (game / "SmallWorld.exe").exists():
            return game
    except Exception:
        pass
    path = filedialog.askdirectory(title="请选择 Small World 2 游戏根目录（含 SmallWorld.exe）")
    if not path:
        raise FileNotFoundError("未选择游戏目录")
    game = Path(path)
    if not (game / "SmallWorld.exe").exists():
        raise FileNotFoundError("该目录下没有 SmallWorld.exe")
    return game


def ensure_installed(game: Path | None = None) -> Path:
    if game is None:
        try:
            game = steam_lang.find_game_dir()
            if not (game / "SmallWorld.exe").exists():
                raise FileNotFoundError("invalid")
        except Exception:
            game = _resolve_game_dir()
    if not (game / "SmallWorld.exe").exists():
        raise FileNotFoundError(f"Not a Small World 2 folder: {game}")
    if not payload_install.zh_files_present(game):
        payload_install.install_payload(game)
    else:
        # Re-sync CSS + CJK fonts (covers upgrades while zh.lproj already present)
        payload_install.install_payload(game)
    return game


def do_enable() -> str:
    ensure_installed()
    return steam_lang.apply_chinese_enabled(True)


def do_disable() -> str:
    msg = steam_lang.apply_chinese_enabled(False)
    try:
        payload_install.restore_fonts(steam_lang.find_game_dir())
    except Exception:
        pass
    return msg


def do_launch() -> None:
    """Launch the game without changing Chinese on/off state."""
    steam_lang.launch_game()


def do_uninstall_files() -> None:
    do_disable()
    game = steam_lang.find_game_dir()
    payload_install.uninstall_payload(game)


def _run_cli(argv: list[str]) -> int:
    if "--enable" in argv:
        print("enable", do_enable())
        return 0
    if "--disable" in argv:
        print("disable", do_disable())
        return 0
    if "--launch" in argv:
        do_launch()
        return 0
    if "--install" in argv:
        print("installed to", ensure_installed())
        return 0
    if "--uninstall" in argv:
        do_uninstall_files()
        print("uninstalled")
        return 0
    if "--status" in argv:
        try:
            g = steam_lang.find_game_dir()
            print(
                "game=",
                g,
                "files=",
                payload_install.zh_files_present(g),
                "enabled=",
                steam_lang.chinese_hook_active(g),
                "steam=",
                steam_lang.read_steam_language(),
            )
        except Exception as exc:
            print("status error", exc)
        return 0
    return -1


class App(tk.Tk):
    def __init__(self, scale: float) -> None:
        super().__init__()
        self.scale = scale
        self._busy = False
        self._photo_icons: list[tk.PhotoImage] = []  # keep refs alive
        self._cover_photo: tk.PhotoImage | None = None
        self.title(APP_TITLE)
        self.resizable(False, False)
        self.configure(bg=BG)
        try:
            self.tk.call("tk", "scaling", 1.0)
        except tk.TclError:
            pass
        self._apply_window_icon()
        self._build()
        self._refresh()

    def _apply_window_icon(self) -> None:
        """Replace Tk's default feather with SmallWorld.exe icon (title bar + dialogs)."""
        ico = _bundled_ico()
        if not ico:
            return
        try:
            # -default makes messagebox / future Toplevels use this icon too
            self.iconbitmap(default=str(ico))
            self.iconbitmap(str(ico))
        except tk.TclError:
            pass
        # iconphoto improves taskbar / alt-tab on some Windows setups
        try:
            from PIL import Image, ImageTk

            img = Image.open(ico)
            frames: list[Image.Image] = []
            try:
                while True:
                    frames.append(img.copy().convert("RGBA"))
                    img.seek(img.tell() + 1)
            except EOFError:
                pass
            if not frames:
                frames = [img.convert("RGBA")]
            # Prefer mid/large sizes for window chrome
            frames.sort(key=lambda im: im.size[0])
            photos = []
            for im in frames[-3:]:
                photos.append(ImageTk.PhotoImage(im))
            self._photo_icons = photos
            if photos:
                self.iconphoto(True, *photos)
        except Exception:
            pass

    def _load_cover(self, height_px: int) -> tuple[tk.PhotoImage | None, int, int]:
        """Scale cover.png to ``height_px`` tall, keeping aspect (no crop / stretch)."""
        path = _bundled_cover()
        if not path:
            return None, int(120 * self.scale), height_px
        try:
            from PIL import Image, ImageTk

            img = Image.open(path).convert("RGBA")
            ow, oh = img.size
            if oh <= 0:
                return None, int(120 * self.scale), height_px
            side_h = max(1, height_px)
            side_w = max(1, int(round(side_h * (ow / oh))))
            # Exact panel fit: panel is sized to image aspect, so resize is 1:1 aspect
            img = img.resize((side_w, side_h), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            return photo, side_w, side_h
        except Exception:
            return None, int(120 * self.scale), height_px

    def _build(self) -> None:
        s = self.scale
        main_w = int(MAIN_WIDTH * s)
        main_h = int(MAIN_HEIGHT * s)

        cover, side_w, side_h = self._load_cover(main_h)
        self._cover_photo = cover
        win_w = side_w + main_w
        win_h = max(side_h, main_h)
        self.geometry(f"{win_w}x{win_h}")
        self.minsize(win_w, win_h)

        root = tk.Frame(self, bg=BG)
        root.pack(fill="both", expand=True)

        side = tk.Frame(root, bg=SIDE, width=side_w, height=win_h)
        side.pack(side="left", fill="y")
        side.pack_propagate(False)
        if cover is not None:
            tk.Label(side, image=cover, bg=SIDE, borderwidth=0, highlightthickness=0).place(
                x=0, y=0, width=side_w, height=side_h
            )
        else:
            tk.Label(side, text="ZH", font=_font(s, 28, True), bg=SIDE, fg=ACCENT).place(
                relx=0.5, rely=0.42, anchor="center"
            )

        main = tk.Frame(root, bg=BG, width=main_w)
        main.pack(side="left", fill="both", expand=True, padx=int(28 * s), pady=int(22 * s))

        tk.Label(
            main,
            text="小小世界中文语言包",
            font=_font(s, 18, True),
            bg=BG,
            fg=TEXT,
            anchor="w",
        ).pack(fill="x")

        tk.Label(
            main,
            text="本程序已内置中文资源。启用时会自动安装到游戏目录，\n并按你当前的 Steam 语言切换为中文。",
            font=_font(s, 10),
            bg=BG,
            fg=MUTED,
            justify="left",
            anchor="w",
        ).pack(fill="x", pady=(int(8 * s), int(12 * s)))

        self.status = tk.Label(
            main, text="", font=_font(s, 11), bg=BG, fg=TEXT, justify="left", anchor="w"
        )
        self.status.pack(fill="x", pady=(0, int(8 * s)))

        self.progress_label = tk.Label(
            main, text="", font=_font(s, 9), bg=BG, fg=MUTED, anchor="w"
        )
        self.progress = ttk.Progressbar(main, mode="indeterminate", length=int(360 * s))

        btn = tk.Frame(main, bg=BG)
        btn.pack(fill="x", side="bottom")

        self.btn_launch = tk.Button(
            btn,
            text="启动游戏",
            command=self._on_launch,
            font=_font(s, 11),
            bg=ACCENT,
            fg="#ffffff",
            activebackground="#2860a0",
            activeforeground="#ffffff",
            relief="flat",
            padx=int(14 * s),
            pady=int(8 * s),
            cursor="hand2",
        )
        self.btn_launch.pack(side="left")

        self.btn_toggle = tk.Button(
            btn,
            text="启用中文",
            command=self._on_toggle,
            font=_font(s, 11),
            relief="groove",
            padx=int(12 * s),
            pady=int(8 * s),
            cursor="hand2",
        )
        self.btn_toggle.pack(side="left", padx=(int(8 * s), 0))

        tk.Button(
            btn,
            text="退出",
            command=self.destroy,
            font=_font(s, 11),
            relief="groove",
            padx=int(12 * s),
            pady=int(8 * s),
            cursor="hand2",
        ).pack(side="right")

        tk.Label(
            main,
            text=f"v{APP_VERSION} · 单文件整合版 · 非官方学习用",
            font=_font(s, 8),
            bg=BG,
            fg="#999999",
            anchor="w",
        ).pack(side="bottom", fill="x", pady=(int(10 * s), 0))

    def _chinese_enabled(self) -> bool:
        try:
            return steam_lang.chinese_hook_active()
        except Exception:
            return False

    def _refresh(self) -> None:
        try:
            game = steam_lang.find_game_dir()
            files = payload_install.zh_files_present(game)
            enabled = steam_lang.chinese_hook_active(game)
            lines = [
                f"游戏目录：{game}",
                f"中文资源：{'已安装' if files else '未安装（启用时会自动写入）'}",
                f"中文状态：{'已启用' if enabled else '未启用'}",
            ]
            self.status.configure(text="\n".join(lines))
            self.btn_toggle.configure(text="关闭中文" if enabled else "启用中文")
        except Exception as exc:  # noqa: BLE001
            self.status.configure(text=f"尚未定位到游戏（可在启用时手动选择目录）。\n{exc}")
            self.btn_toggle.configure(text="启用中文")

    def _set_busy(self, busy: bool, message: str = "") -> None:
        self._busy = busy
        state = "disabled" if busy else "normal"
        self.btn_launch.configure(state=state)
        self.btn_toggle.configure(state=state)
        if busy:
            self.progress_label.configure(text=message or "处理中，请稍候…")
            self.progress_label.pack(fill="x", pady=(0, 4))
            self.progress.pack(fill="x", pady=(0, 12))
            self.progress.start(12)
        else:
            self.progress.stop()
            self.progress.pack_forget()
            self.progress_label.pack_forget()
            self.progress_label.configure(text="")

    def _run_async(self, message: str, work, on_ok) -> None:
        if self._busy:
            return
        self._set_busy(True, message)
        self.update_idletasks()

        def worker() -> None:
            err: BaseException | None = None
            result = None
            try:
                result = work()
            except BaseException as exc:  # noqa: BLE001
                err = exc
            self.after(0, lambda: self._finish_async(err, result, on_ok))

        threading.Thread(target=worker, daemon=True).start()

    def _finish_async(self, err, result, on_ok) -> None:
        self._set_busy(False)
        self._refresh()
        if err is not None:
            messagebox.showerror(APP_TITLE, str(err), parent=self)
            return
        on_ok(result)

    def _on_toggle(self) -> None:
        if self._chinese_enabled():
            self._run_async(
                "正在关闭中文并还原语言包…",
                do_disable,
                lambda _r: messagebox.showinfo(
                    APP_TITLE,
                    "已关闭中文，原语言包已还原。\n请重新启动游戏使其生效。",
                    parent=self,
                ),
            )
        else:
            self._run_async(
                "正在安装/启用中文（首次可能需要一点时间）…",
                do_enable,
                lambda lang: messagebox.showinfo(
                    APP_TITLE,
                    f"中文已启用（Steam 语言：{lang}）。\n可从 Steam 启动，或点「启动游戏」。",
                    parent=self,
                ),
            )

    def _on_launch(self) -> None:
        enabled = self._chinese_enabled()
        msg = "正在启动游戏（中文已启用）…" if enabled else "正在启动游戏（保持当前语言）…"
        self._run_async(
            msg,
            lambda: (do_launch(), None)[1],
            lambda _r: self.after(400, self.destroy),
        )


def main() -> None:
    code = _run_cli(sys.argv[1:])
    if code >= 0:
        sys.exit(code)
    App(_dpi_scale()).mainloop()


if __name__ == "__main__":
    main()
