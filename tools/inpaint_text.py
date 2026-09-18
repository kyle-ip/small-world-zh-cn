# -*- coding: utf-8 -*-
"""Text replacement via EN/JA diff-mask + OpenCV inpainting.

The English and Japanese image packs share identical background artwork;
only the baked-in text differs. Their pixel-difference yields a precise
text mask, which lets us erase the original text (inpainting the art
behind it) and draw Chinese text in the same spot and similar color.

Where EN and JA letterforms overlap (same position, same near-white
color on a metal plaque) the diff is blind, so the mask is augmented
with a local-contrast ("saliency") text detector inside each text band.
"""
import numpy as np
import cv2
from PIL import Image, ImageDraw

import cnfont


def _load_rgba(path):
    return np.array(Image.open(path).convert("RGBA"))


def _segments(idx):
    if len(idx) == 0:
        return []
    return [s for s in np.split(idx, np.where(np.diff(idx) != 1)[0] + 1) if len(s)]


def _raw_diff(en, ja, jpg=False):
    h, w = en.shape[:2]
    if ja is None or ja.shape[:2] != (h, w):
        return None
    if jpg:
        diff = np.abs(en[..., :3].astype(np.int16) - ja[..., :3].astype(np.int16))
        valid = np.ones((h, w), dtype=bool)
        thresh = 45
    else:
        # RGBA diff: EN/JA letterforms on transparent titles barely
        # overlap, so alpha differences are essential markers.
        diff = np.abs(en.astype(np.int16) - ja.astype(np.int16))
        valid = (en[..., 3] > 200) | (ja[..., 3] > 200)
        thresh = 32
    dist = diff.max(axis=2)
    raw = ((dist > thresh) & valid).astype(np.uint8) * 255
    k_open = 5 if jpg else 3
    raw = cv2.morphologyEx(raw, cv2.MORPH_OPEN, np.ones((k_open, k_open), np.uint8))
    if jpg:
        raw = cv2.morphologyEx(raw, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    return raw


def _saliency(rgba):
    """Pixels that strongly differ from their 15px neighborhood median:
    text strokes on any background, bright or dark."""
    gray = cv2.cvtColor(rgba[..., :3], cv2.COLOR_RGB2GRAY)
    bg = cv2.medianBlur(gray, 15)
    out = (np.abs(gray.astype(np.int16) - bg.astype(np.int16)) > 45)
    return (out & (rgba[..., 3] > 200)).astype(np.uint8) * 255


def _row_band(profile, h):
    """Contiguous row segment containing the strongest interior peak.
    Segments hugging the image edge that are also thin are cross-pack
    border drift (e.g. map edges), never text."""
    prof = profile.astype(np.float32)
    if prof.max() <= 0:
        return None
    keep = (prof > 0.3 * prof.max()).astype(np.uint8)
    keep = cv2.morphologyEx(keep.reshape(1, -1), cv2.MORPH_CLOSE,
                            np.ones((1, 3), np.uint8))[0]
    segs = _segments(np.where(keep > 0)[0])
    valid = [s for s in segs
             if not (s[-1] >= h - 2 or s[0] <= 2) or len(s) >= 0.25 * h]
    pool = valid or segs
    best = max(pool, key=lambda s: float(prof[s].sum()))
    return int(best[0]), int(best[-1])


def _col_span(profile, w):
    """Union of all meaningful dense column segments."""
    prof = profile.astype(np.float32)
    if prof.max() <= 0:
        return None
    keep = (prof > 0.12 * prof.max()).astype(np.uint8)
    keep = cv2.morphologyEx(keep.reshape(1, -1), cv2.MORPH_CLOSE,
                            np.ones((1, max(5, w // 8)), np.uint8))[0]
    segs = _segments(np.where(keep > 0)[0])
    segs = [s for s in segs if len(s) >= max(3, 0.04 * w)]
    if not segs:
        return None
    return int(segs[0][0]), int(segs[-1][-1])


def _band_mask(raw, h, w, sal=None, y_range=None):
    """Find one dense text band within y_range (full image by default),
    keep all glyph components around it, augment with local-contrast text
    pixels, and return the dilated mask."""
    y_lo, y_hi = y_range or (0, h - 1)
    region = raw[y_lo:y_hi + 1, :]
    if region.sum() == 0:
        return None
    rel_b = _row_band(region.sum(axis=1), y_hi - y_lo + 1)
    if rel_b is None:
        return None
    y0 = y_lo + rel_b[0]
    y1 = y_lo + rel_b[1]
    xb = _col_span(raw[y0:y1 + 1, :].sum(axis=0), w)
    if xb is None:
        return None
    x0, x1 = xb

    # Components intersecting the core rectangle preserve glyph
    # ascenders/descenders whose rows are too sparse for the band.
    n, labels, stats, _ = cv2.connectedComponentsWithStats(raw, 8)
    core_h = y1 - y0 + 1
    pad = max(4, core_h // 2)
    rx0, rx1, ry0, ry1 = x0 - 6, x1 + 6, y0 - pad, y1 + pad
    clean = np.zeros_like(raw)
    for i in range(1, n):
        x, y, cw, ch, area = stats[i]
        if area < 12:
            continue
        if not (x + cw < rx0 or x > rx1 or y + ch < ry0 or y > ry1):
            clean[labels == i] = 255

    # Augment with EN/JA local-contrast pixels inside the band rect;
    # catches letters that coincide position+color across language packs.
    if sal is not None:
        ex = 2
        rect = np.zeros_like(raw)
        rect[max(0, y0 - ex):min(h, y1 + ex + 1),
             max(0, x0 - ex):min(w, x1 + ex + 1)] = 255
        clean = np.maximum(clean, sal & rect)

    if clean.sum() == 0:
        return None

    k_iter = 2 if (raw.shape[0] > 300) else 3
    ksize = 5 if raw.shape[0] > 300 else 3
    return cv2.dilate(clean, np.ones((ksize, ksize), np.uint8),
                      iterations=k_iter)


def _plaque_mask(raw, en, ja, h, w, decline=False):
    """Race/power banner name on a standardized metal plaque. The plaque
    spans fixed fractions of the token; mask the engraved letter pixels
    (diff union + BRIGHT high-contrast pixels) inside it. Brightness gate
    is essential: the scratched metal itself is high-contrast texture and
    would otherwise eat the whole plaque during inpainting. In-decline
    race tokens mirror the layout with the plaque on the right."""
    def bright(rgba):
        gray = cv2.cvtColor(rgba[..., :3], cv2.COLOR_RGB2GRAY)
        return ((gray > 185) & (rgba[..., 3] > 200)).astype(np.uint8) * 255

    letters = bright(en)
    if ja is not None and ja.shape[:2] == (h, w):
        letters = np.maximum(letters, bright(ja))
    if decline:
        x0, x1 = int(w * 0.46), int(w * 0.99)
    else:
        wide = w / h > 1.5        # race token (215x114) vs power (115x114)
        x0, x1 = int(w * 0.02), int(w * (0.58 if wide else 0.92))

    if decline:
        # Decline name strips live at the same fractions in SD and HD
        # (letters y~0.08h-0.22h); use a fixed tight strip. Dim letters on
        # faded metal come from the raw diff, while the bright channel is
        # gated adaptively because HD plaque metal itself can be pale
        # (gray ~190) and a fixed 185 gate would erase the whole strip.
        y0, y1 = int(h * 0.01), int(h * 0.27)
        gray = cv2.cvtColor(en[..., :3], cv2.COLOR_RGB2GRAY)
        core = gray[int(h * 0.04):int(h * 0.24), int(w * 0.52):int(w * 0.95)]
        core = core[core > 60]
        gate = max(185, int(np.median(core)) + 30) if len(core) else 185
        dletters = ((gray > gate) & (en[..., 3] > 200)).astype(np.uint8) * 255
        if ja is not None and ja.shape[:2] == (h, w):
            jg = cv2.cvtColor(ja[..., :3], cv2.COLOR_RGB2GRAY)
            dletters = np.maximum(
                dletters, ((jg > gate) & (ja[..., 3] > 200)).astype(np.uint8) * 255)
        rect = np.zeros((h, w), np.uint8)
        rect[y0:y1, x0:x1] = 255
        px = np.maximum(raw if raw is not None else 0, dletters) & rect
        px = cv2.morphologyEx(px, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        if px.sum() == 0:
            return None
        ksize, iters = (5, 2) if h > 150 else (3, 3)
        return cv2.dilate(px, np.ones((ksize, ksize), np.uint8), iterations=iters)

    # Walk down through dense letter rows to bound the plaque vertically.
    # Normal plaques may wrap to two lines (DRAGON MASTER, PEACE LOVING).
    y0 = int(h * 0.01)
    y1 = int(h * 0.27)
    rowcnt = (letters[y0:min(h, int(h * 0.40)), x0:x1].sum(axis=1) // 255)
    first = np.where(rowcnt > max(4, w // 25))[0]
    if len(first):
        start = int(first[0])
        line_density = max(20.0, float(np.median(rowcnt[start:start + 12])))
        ink = rowcnt > 0.22 * line_density
        i = start
        last_ink = start
        gap = 0
        while i < len(ink) and i - start < 0.38 * h:
            if ink[i]:
                if gap <= 4:
                    last_ink = i
                gap = 0
            else:
                gap += 1
                if gap > 4 and i > start + 6:
                    break
            i += 1
        y1 = min(h - 1, y0 + last_ink + 3)
    rect = np.zeros((h, w), np.uint8)
    rect[y0:y1, x0:x1] = 255
    px = np.maximum(raw if raw is not None else 0, letters) & rect
    px = cv2.morphologyEx(px, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    if px.sum() == 0:
        return None
    ksize, iters = (5, 2) if h > 150 else (3, 3)
    return cv2.dilate(px, np.ones((ksize, ksize), np.uint8), iterations=iters)


def build_text_masks(en, ja, jpg=False, subtext=False, plaque=False):
    """Return [primary_mask] or [primary_mask, bottom_mask].
    For plaque images without an EN counterpart, ja=None and the bright
    engraved-letter detector alone provides the mask."""
    h, w = en.shape[:2]
    raw = _raw_diff(en, ja, jpg=jpg)
    sal = None
    if not jpg:
        sal = _saliency(en)
        if ja is not None and ja.shape[:2] == (h, w):
            sal = np.maximum(sal, _saliency(ja))

    if plaque:
        if raw is None:
            raw = np.zeros((h, w), np.uint8)
        primary = _plaque_mask(raw, en, ja, h, w, decline=(plaque == "decline"))
    else:
        if raw is None or raw.sum() == 0:
            return []
        primary = _band_mask(raw, h, w, sal)
    if primary is None:
        return []
    masks = [primary]

    if subtext:
        ys, _ = np.where(primary > 0)
        start = max(int(h * 0.55), int(ys.max()) + 6)
        if start < h - 6:
            # ignore already-consumed primary pixels
            extra_raw = raw.copy()
            extra_raw[primary > 0] = 0
            bottom = _band_mask(extra_raw, h, w, sal, y_range=(start, h - 1))
            if bottom is not None and int((bottom > 0).sum()) >= 30:
                masks.append(bottom)
    return masks


def _draw_text(result, en, mask, text, w, h, style=None):
    """Draw `text` centered in the mask bbox. style=None derives a fill
    color from the EN letter pixels; 'plaque' uses engraved white letters,
    'sub' is the small handwritten bottom annotation."""
    ys, xs = np.where(mask > 0)
    bx0, bx1, by0, by1 = xs.min(), xs.max(), ys.min(), ys.max()

    if style == "plaque":
        fill, stroke = (232, 230, 222), (72, 52, 32)
    elif style == "sub":
        fill, stroke = (236, 226, 205), (96, 62, 30)
    else:
        m = mask > 0
        opaque_text = m & (en[..., 3] > 200)
        body_rgb = en[..., :3][opaque_text]
        if len(body_rgb) < 8:
            body_rgb = en[..., :3][m]
        fill = tuple(int(v) for v in np.median(body_rgb, axis=0))
        fill_bright = sum(fill) / 3
        stroke = (238, 224, 196) if fill_bright < 110 else (86, 56, 26)

    box_w, box_h = bx1 - bx0 + 1, by1 - by0 + 1
    height_factor = 0.68 if style == "sub" else 0.9
    size = max(9, int(box_h * height_factor))
    if style == "plaque":
        # Two-line plaques have a tall bbox; keep glyphs at cap height.
        size = min(size, int(h * 0.185))
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    while size > 8:
        stroke_w = max(1, size // 16)
        font = cnfont.load_font(size)
        bb = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_w)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        if tw <= box_w and th <= box_h:
            break
        size -= 1
    font = cnfont.load_font(size)
    stroke_w = max(1, size // 16)
    bb = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_w)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    cx, cy = (bx0 + bx1) // 2, (by0 + by1) // 2
    x = cx - tw // 2 - bb[0]
    y = cy - th // 2 - bb[1]
    draw.text((x, y), text, font=font,
              fill=fill + (255,), stroke_width=stroke_w, stroke_fill=stroke + (255,))

    base = Image.fromarray(result, "RGBA")
    base.alpha_composite(layer)
    return np.array(base)


def _align_canvas(en, ja):
    """Fit a reference image whose canvas differs by 1-2 px onto the EN
    canvas by translation + edge padding (no resampling). Offset is scored
    on the artwork band below the plaque, where the two renders agree."""
    h, w = en.shape[:2]
    jh, jw = ja.shape[:2]
    if abs(jh - h) > 2 or abs(jw - w) > 2:
        return cv2.resize(ja, (w, h), interpolation=cv2.INTER_LINEAR)

    def shifted(dy, dx):
        canvas = np.zeros_like(en)
        ys0, ys1 = max(0, dy), min(h, jh + dy)
        xs0, xs1 = max(0, dx), min(w, jw + dx)
        if ys1 <= ys0 or xs1 <= xs0:
            return None
        tile = ja[ys0 - dy:ys1 - dy, xs0 - dx:xs1 - dx]
        canvas[ys0:ys1, xs0:xs1] = tile
        if ys0 > 0:
            canvas[:ys0] = canvas[ys0:ys0 + 1]
        if ys1 < h:
            canvas[ys1:] = canvas[ys1 - 1:ys1]
        if xs0 > 0:
            canvas[:, :xs0] = canvas[:, xs0:xs0 + 1]
        if xs1 < w:
            canvas[:, xs1:] = canvas[:, xs1 - 1:xs1]
        return canvas

    best, best_cost = None, None
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            cand = shifted(dy, dx)
            if cand is None:
                continue
            band = slice(int(h * 0.55), int(h * 0.95))
            d = np.abs(en[band, ..., :3].astype(int) - cand[band, ..., :3].astype(int)).max(axis=2)
            valid = (en[band, ..., 3] > 200) & (cand[band, ..., 3] > 200)
            cost = int((d[valid] > 32).sum())
            if best_cost is None or cost < best_cost:
                best, best_cost = cand, cost
    return best


def inpaint_localize(en_path, ja_ref_path, chinese_text, jpg=False,
                    subtext=None, plaque=False):
    """Return localized RGBA image, or None if EN/JA share no text diff.

    subtext: optional Chinese string for a second baked text line near
    the image bottom (small flavor/rule annotations).
    plaque: name sits on a standardized race/power metal plaque.
    """
    en = _load_rgba(en_path)
    ja = _load_rgba(ja_ref_path) if ja_ref_path else None
    if ja is not None and ja.shape[:2] != en.shape[:2]:
        ja = _align_canvas(en, ja)
    h, w = en.shape[:2]

    masks = build_text_masks(en, ja, jpg=jpg, subtext=bool(subtext),
                             plaque=plaque)
    if not masks or int((masks[0] > 0).sum()) < 40:
        return None
    texts = [chinese_text]
    if subtext and len(masks) == 2:
        texts.append(subtext)

    union = np.zeros((h, w), np.uint8)
    for msk in masks[:len(texts)]:
        union = np.maximum(union, msk)

    bgr = en[..., :3][:, :, ::-1].copy()
    inp_rgb = cv2.inpaint(bgr, union, 3, cv2.INPAINT_TELEA)[:, :, ::-1]
    alpha = en[..., 3].copy()
    alpha_inp = cv2.inpaint(alpha, union, 3, cv2.INPAINT_TELEA)

    m = union > 0
    result = en.copy()
    result[..., :3] = np.where(m[..., None], inp_rgb, en[..., :3])
    if jpg:
        result[..., 3] = np.where(m, alpha_inp, alpha)
    else:
        new_alpha = np.where(alpha_inp >= 200, np.maximum(alpha_inp, 200), 0).astype(np.uint8)
        result[..., 3] = np.where(m, new_alpha, alpha)

    for i, (msk, txt) in enumerate(zip(masks[:len(texts)], texts)):
        if i == 0 and plaque:
            style = "plaque"
        elif i == 1:
            style = "sub"
        else:
            style = None
        result = _draw_text(result, en, msk, txt, w, h, style=style)
    return Image.fromarray(result, "RGBA")
