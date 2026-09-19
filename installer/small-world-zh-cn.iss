; Small World 2 Chinese language pack — one-click Inno Setup 6 installer
; Build: tools\build_installer.ps1
;
; End-user flow: run Setup → confirm/choose game folder → Finish → play from Steam.

#define MyAppName "小小世界 中文语言包"
#define MyAppVersion "1.2.0"
#define MyAppPublisher "small-world-zh-cn (fan / learning)"
#define MyAppURL "https://github.com/"
#define MyAppExeName "SmallWorld-cn-Launcher.exe"
#define GameAppId "235620"

[Setup]
AppId={{A7C3E2F1-9B4D-4E8A-9C21-SMALLWORLD2ZH}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
DefaultDirName={code:GetGameDir}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
DisableDirPage=no
DirExistsWarning=no
UsePreviousAppDir=no
AllowNoIcons=yes
PrivilegesRequired=admin
OutputDir=..\dist
OutputBaseFilename=SmallWorld2-zh-CN-Setup-{#MyAppVersion}
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
WizardSizePercent=120
WizardImageFile=wizard-side.bmp
WizardSmallImageFile=wizard-small.bmp
WizardImageStretch=yes
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayName={#MyAppName}
InfoBeforeFile=info-before.txt
LicenseFile=license.txt
VersionInfoVersion=1.2.0.0
VersionInfoProductName={#MyAppName}
ShowLanguageDialog=no
SetupLogging=yes

[Languages]
Name: "chinesesimplified"; MessagesFile: "ChineseSimplified.isl"

[Messages]
chinesesimplified.WelcomeLabel1=欢迎使用小小世界中文语言包安装向导
chinesesimplified.WelcomeLabel2=本程序将把中文资源安装到你的小小世界游戏目录，并自动启用中文。%n%n无需在 Steam 中改成荷兰语或其他语言：启动器会按你当前的 Steam 游戏语言自动挂接中文。%n%n请确认下方游戏路径正确（可点击浏览修改），然后点击“下一步”继续。
chinesesimplified.SelectDirLabel3=请指定小小世界的游戏根目录（需包含 SmallWorld.exe）：
chinesesimplified.FinishedHeadingLabel=安装完成
chinesesimplified.FinishedLabelNoIcons=中文语言包已安装并启用。%n%n请从 Steam 启动 Small World，或使用开始菜单中的“启动小小世界（中文）”。%n关闭中文请使用“中文开关”工具或卸载本补丁。

[Tasks]
Name: "desktopicon"; Description: "创建桌面快捷方式（启动游戏·中文）"; GroupDescription: "附加选项:"

[Files]
Source: "..\payload\Resources\zh.lproj\*"; DestDir: "{app}\Resources\zh.lproj"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\payload\Resources\compendium\zh\*"; DestDir: "{app}\Resources\compendium\zh"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\payload\Resources\compendium\zh-short\*"; DestDir: "{app}\Resources\compendium\zh-short"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\payload\Resources\compendium\image\mdpi\zh\*"; DestDir: "{app}\Resources\compendium\image\mdpi\zh"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\dist\launcher\{#MyAppExeName}"; DestDir: "{app}\SmallWorld2-zh-cn"; Flags: ignoreversion

[Icons]
Name: "{group}\启动小小世界（中文）"; Filename: "{app}\SmallWorld2-zh-cn\{#MyAppExeName}"; Parameters: "--launch"
Name: "{group}\中文开关"; Filename: "{app}\SmallWorld2-zh-cn\{#MyAppExeName}"
Name: "{group}\卸载中文语言包"; Filename: "{uninstallexe}"
Name: "{autodesktop}\小小世界（中文）"; Filename: "{app}\SmallWorld2-zh-cn\{#MyAppExeName}"; Parameters: "--launch"; Tasks: desktopicon

[Run]
; Silently enable Chinese after files are copied (no Python needed)
Filename: "{app}\SmallWorld2-zh-cn\{#MyAppExeName}"; Parameters: "--enable"; StatusMsg: "正在启用中文…"; Flags: runhidden waituntilterminated
Filename: "{app}\SmallWorld2-zh-cn\{#MyAppExeName}"; Parameters: "--launch"; Description: "立即启动游戏（中文）"; Flags: nowait postinstall skipifsilent unchecked

[UninstallRun]
; Restore Dutch slot / Steam language before deleting files
Filename: "{app}\SmallWorld2-zh-cn\{#MyAppExeName}"; Parameters: "--disable"; RunOnceId: "DisableChinese"; Flags: runhidden waituntilterminated

[UninstallDelete]
Type: filesandordirs; Name: "{app}\Resources\zh.lproj"
Type: filesandordirs; Name: "{app}\Resources\compendium\zh"
Type: filesandordirs; Name: "{app}\Resources\compendium\zh-short"
Type: filesandordirs; Name: "{app}\Resources\compendium\image\mdpi\zh"
Type: filesandordirs; Name: "{app}\SmallWorld2-zh-cn"

[Code]
function GetSteamPath(): String;
var
  P: String;
begin
  Result := '';
  if RegQueryStringValue(HKCU, 'Software\Valve\Steam', 'SteamPath', P) then
    Result := P;
end;

function GetGameDir(Param: String): String;
var
  Steam, Manifest, Line, InstallDir, LibFile, LibPath: String;
  Lines: TArrayOfString;
  I: Integer;
begin
  Result := ExpandConstant('{commonpf32}\Steam\steamapps\common\SmallWorld2');
  Steam := GetSteamPath();
  if Steam = '' then
    Exit;

  Manifest := Steam + '\steamapps\appmanifest_{#GameAppId}.acf';
  if FileExists(Manifest) then
  begin
    if LoadStringsFromFile(Manifest, Lines) then
    begin
      for I := 0 to GetArrayLength(Lines) - 1 do
      begin
        Line := Lines[I];
        if Pos('"installdir"', Line) > 0 then
        begin
          InstallDir := Line;
          StringChangeEx(InstallDir, '"installdir"', '', True);
          StringChangeEx(InstallDir, '"', '', True);
          InstallDir := Trim(InstallDir);
          Result := Steam + '\steamapps\common\' + InstallDir;
          Exit;
        end;
      end;
    end;
  end;

  LibFile := Steam + '\steamapps\libraryfolders.vdf';
  if FileExists(LibFile) and LoadStringsFromFile(LibFile, Lines) then
  begin
    for I := 0 to GetArrayLength(Lines) - 1 do
    begin
      Line := Lines[I];
      if Pos('"path"', Line) > 0 then
      begin
        LibPath := Line;
        StringChangeEx(LibPath, '"path"', '', True);
        StringChangeEx(LibPath, '"', '', True);
        LibPath := Trim(LibPath);
        StringChangeEx(LibPath, '\\', '\', True);
        Manifest := LibPath + '\steamapps\appmanifest_{#GameAppId}.acf';
        if FileExists(Manifest) then
        begin
          Result := LibPath + '\steamapps\common\SmallWorld2';
          if DirExists(Result) then
            Exit;
        end;
      end;
    end;
  end;
end;

function NextButtonClick(CurPageID: Integer): Boolean;
begin
  Result := True;
  if CurPageID = wpSelectDir then
  begin
    if not FileExists(ExpandConstant('{app}\SmallWorld.exe')) then
    begin
      MsgBox('请选择小小世界的游戏根目录（该文件夹内必须有 SmallWorld.exe）。', mbError, MB_OK);
      Result := False;
    end;
  end;
end;

function InitializeSetup(): Boolean;
begin
  Result := True;
end;
