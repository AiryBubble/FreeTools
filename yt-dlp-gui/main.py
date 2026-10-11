from __future__ import annotations

import json
import queue
import shutil
import subprocess
import sys
import threading
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


TEXT = {
    "en": {
        "title": "yt-dlp-gui", "url": "Video URL", "folder": "Save to",
        "browse": "Browse…", "language": "Language", "kind": "Download as",
        "video": "Video", "audio": "Audio", "quality": "Video quality",
        "audio_quality": "Audio quality", "format": "File format", "best": "Best available",
        "audio_best": "Best available", "formats": "Available formats", "list": "List formats",
        "download": "Download", "cancel": "Cancel", "ready": "Ready",
        "checking": "Checking tools…", "yt_found": "yt-dlp: found", "yt_missing": "yt-dlp: not found",
        "ff_found": "FFmpeg: found", "ff_missing": "FFmpeg: not found (needed for conversion/merging)",
        "choose_folder": "Choose download folder", "need_url": "Enter a YouTube URL.",
        "need_ytdlp": "yt-dlp was not found. Install it with ‘python -m pip install -U yt-dlp’, or select its executable.",
        "need_ffmpeg": "FFmpeg is required for audio extraction and format conversion. Install FFmpeg and restart the app.",
        "working": "Working…", "done": "Download complete.", "failed": "Operation failed.",
        "cancelled": "Cancelled.", "log": "Activity", "select_ytdlp": "Select yt-dlp executable",
        "select_exe": "Executable", "formats_ready": "Formats loaded. Choose a format ID in the quality field, or leave it as Best available.",
        "format_id": "Format ID", "audio_desc": "Audio-only downloads are extracted and converted with FFmpeg.",
        "check_quality": "Check available quality", "quality_hint": "Select a listed resolution or audio bitrate. Availability is checked for this URL.",
        "quality_unchecked": "Check available quality to load options for this URL.", "no_qualities": "No listed resolutions matched the supported options; Best available remains selectable.",
        "bitrate_hint": "Bitrate is an output target; re-encoding cannot improve the source audio quality.",
        "usage": "Use only for content you are authorized to download. Follow YouTube's terms and applicable copyright laws.",
        "user_agent": "User agent", "ua_default": "yt-dlp default", "ua_desktop": "Desktop browser", "ua_mobile": "Mobile browser", "ua_tv": "Smart TV",
    },
    "ja": {
        "title": "yt-dlp-gui", "url": "動画URL", "folder": "保存先",
        "browse": "参照…", "language": "言語", "kind": "ダウンロード形式",
        "video": "動画", "audio": "音声", "quality": "動画画質",
        "audio_quality": "音声品質", "format": "ファイル形式", "best": "最良の品質",
        "audio_best": "最良の品質", "formats": "利用可能な形式", "list": "形式一覧",
        "download": "ダウンロード", "cancel": "キャンセル", "ready": "準備完了",
        "checking": "ツールを確認中…", "yt_found": "yt-dlp: 検出済み", "yt_missing": "yt-dlp: 未検出",
        "ff_found": "FFmpeg: 検出済み", "ff_missing": "FFmpeg: 未検出（変換・結合に必要）",
        "choose_folder": "保存先フォルダーを選択", "need_url": "YouTubeのURLを入力してください。",
        "need_ytdlp": "yt-dlpが見つかりません。「python -m pip install -U yt-dlp」でインストールするか、実行ファイルを指定してください。",
        "need_ffmpeg": "音声抽出と形式変換にはFFmpegが必要です。FFmpegをインストールしてアプリを再起動してください。",
        "working": "処理中…", "done": "ダウンロードが完了しました。", "failed": "処理に失敗しました。",
        "cancelled": "キャンセルしました。", "log": "処理状況", "select_ytdlp": "yt-dlp実行ファイルを選択",
        "select_exe": "実行ファイル", "formats_ready": "形式を読み込みました。画質欄に形式IDを指定するか、「最良の品質」のままにしてください。",
        "format_id": "形式ID", "audio_desc": "音声のみの場合、FFmpegで抽出・変換します。",
        "usage": "ダウンロードが許可されたコンテンツにのみ使用してください。YouTubeの利用規約と著作権法を遵守してください。",
        "check_quality": "画質を確認", "quality_hint": "このURLで利用できる解像度・音声ビットレートのみを選べます。",
        "quality_unchecked": "このURLの選択肢を読み込むには「画質を確認」を押してください。", "no_qualities": "該当する解像度がありません。「最良の品質」は選択できます。",
        "bitrate_hint": "ビットレートは出力時の目標値です。再エンコードで元音声より高音質にはなりません。",
        "user_agent": "ユーザーエージェント", "ua_default": "yt-dlp標準", "ua_desktop": "デスクトップブラウザー", "ua_mobile": "モバイルブラウザー", "ua_tv": "スマートTV",
    },
    "de": {
        "title": "yt-dlp-gui", "url": "Video-URL", "folder": "Speichern unter",
        "browse": "Durchsuchen…", "language": "Sprache", "kind": "Downloadtyp",
        "video": "Video", "audio": "Audio", "quality": "Videoqualität",
        "audio_quality": "Audioqualität", "format": "Dateiformat", "best": "Beste verfügbare",
        "audio_best": "Beste verfügbare", "formats": "Verfügbare Formate", "list": "Formate anzeigen",
        "download": "Herunterladen", "cancel": "Abbrechen", "ready": "Bereit",
        "checking": "Werkzeuge werden geprüft…", "yt_found": "yt-dlp: gefunden", "yt_missing": "yt-dlp: nicht gefunden",
        "ff_found": "FFmpeg: gefunden", "ff_missing": "FFmpeg: nicht gefunden (für Konvertierung/Zusammenführung nötig)",
        "choose_folder": "Downloadordner auswählen", "need_url": "Bitte eine YouTube-URL eingeben.",
        "need_ytdlp": "yt-dlp wurde nicht gefunden. Installiere es mit ‘python -m pip install -U yt-dlp’ oder wähle die ausführbare Datei aus.",
        "need_ffmpeg": "Für Audioextraktion und Formatkonvertierung wird FFmpeg benötigt. Installiere FFmpeg und starte die App neu.",
        "working": "Wird ausgeführt…", "done": "Download abgeschlossen.", "failed": "Vorgang fehlgeschlagen.",
        "cancelled": "Abgebrochen.", "log": "Aktivität", "select_ytdlp": "yt-dlp-Datei auswählen",
        "select_exe": "Ausführbare Datei", "formats_ready": "Formate geladen. Format-ID bei Qualität eingeben oder Beste verfügbare beibehalten.",
        "format_id": "Format-ID", "audio_desc": "Audio wird mit FFmpeg extrahiert und konvertiert.",
        "usage": "Nur Inhalte herunterladen, zu deren Download Sie berechtigt sind. Beachten Sie YouTubes Nutzungsbedingungen und geltendes Urheberrecht.",
        "check_quality": "Qualität prüfen", "quality_hint": "Nur für diese URL verfügbare Auflösungen und Bitraten werden angeboten.",
        "quality_unchecked": "Prüfe die Qualität, um Optionen für diese URL zu laden.", "no_qualities": "Keine passende Auflösung gefunden; Beste verfügbare bleibt auswählbar.",
        "bitrate_hint": "Die Bitrate ist ein Ausgabeziel; eine Neukodierung verbessert die Quellqualität nicht.",
        "user_agent": "User-Agent", "ua_default": "yt-dlp-Standard", "ua_desktop": "Desktopbrowser", "ua_mobile": "Mobiler Browser", "ua_tv": "Smart-TV",
    },
    "zh": {
        "title": "yt-dlp-gui", "url": "视频网址", "folder": "保存位置",
        "browse": "浏览…", "language": "语言", "kind": "下载类型",
        "video": "视频", "audio": "音频", "quality": "视频画质",
        "audio_quality": "音频质量", "format": "文件格式", "best": "最佳可用质量",
        "audio_best": "最佳可用质量", "formats": "可用格式", "list": "查看格式",
        "download": "下载", "cancel": "取消", "ready": "就绪",
        "checking": "正在检查工具…", "yt_found": "yt-dlp：已找到", "yt_missing": "yt-dlp：未找到",
        "ff_found": "FFmpeg：已找到", "ff_missing": "FFmpeg：未找到（转换/合并需要）",
        "choose_folder": "选择下载文件夹", "need_url": "请输入 YouTube 网址。",
        "need_ytdlp": "未找到 yt-dlp。请运行 ‘python -m pip install -U yt-dlp’ 安装，或选择其可执行文件。",
        "need_ffmpeg": "提取音频和转换格式需要 FFmpeg。请安装 FFmpeg 后重启应用。",
        "working": "处理中…", "done": "下载完成。", "failed": "操作失败。",
        "cancelled": "已取消。", "log": "活动", "select_ytdlp": "选择 yt-dlp 可执行文件",
        "select_exe": "可执行文件", "formats_ready": "格式已加载。请在画质栏输入格式 ID，或保留“最佳可用质量”。",
        "format_id": "格式 ID", "audio_desc": "纯音频下载将使用 FFmpeg 提取并转换。",
        "usage": "仅下载您获准下载的内容。请遵守 YouTube 服务条款及适用的版权法律。",
        "check_quality": "检查可用画质", "quality_hint": "仅显示此网址实际提供的分辨率和音频码率。",
        "quality_unchecked": "请检查可用画质以加载此网址的选项。", "no_qualities": "没有匹配的分辨率；仍可选择“最佳可用质量”。",
        "bitrate_hint": "码率是输出目标；重新编码无法提高源音频质量。",
        "user_agent": "用户代理", "ua_default": "yt-dlp 默认", "ua_desktop": "桌面浏览器", "ua_mobile": "移动浏览器", "ua_tv": "智能电视",
    },
    "ru": {
        "title": "yt-dlp-gui", "url": "Ссылка на видео", "folder": "Сохранить в",
        "browse": "Обзор…", "language": "Язык", "kind": "Тип загрузки",
        "video": "Видео", "audio": "Аудио", "quality": "Качество видео",
        "audio_quality": "Качество аудио", "format": "Формат файла", "best": "Наилучшее доступное",
        "audio_best": "Наилучшее доступное", "formats": "Доступные форматы", "list": "Показать форматы",
        "download": "Скачать", "cancel": "Отмена", "ready": "Готово",
        "checking": "Проверка инструментов…", "yt_found": "yt-dlp: найден", "yt_missing": "yt-dlp: не найден",
        "ff_found": "FFmpeg: найден", "ff_missing": "FFmpeg: не найден (нужен для конвертации/объединения)",
        "choose_folder": "Выберите папку загрузки", "need_url": "Введите ссылку YouTube.",
        "need_ytdlp": "yt-dlp не найден. Установите его командой «python -m pip install -U yt-dlp» или выберите исполняемый файл.",
        "need_ffmpeg": "Для извлечения аудио и конвертации нужен FFmpeg. Установите FFmpeg и перезапустите приложение.",
        "working": "Выполняется…", "done": "Загрузка завершена.", "failed": "Не удалось выполнить операцию.",
        "cancelled": "Отменено.", "log": "Ход выполнения", "select_ytdlp": "Выбрать yt-dlp",
        "select_exe": "Исполняемый файл", "formats_ready": "Форматы загружены. Введите ID формата в поле качества или оставьте «Наилучшее доступное».",
        "format_id": "ID формата", "audio_desc": "Аудио извлекается и конвертируется с помощью FFmpeg.",
        "usage": "Загружайте только контент, который разрешено загружать. Соблюдайте условия YouTube и применимое авторское право.",
        "check_quality": "Проверить качество", "quality_hint": "Показываются только разрешения и битрейты, доступные по этой ссылке.",
        "quality_unchecked": "Проверьте качество, чтобы загрузить варианты для этой ссылки.", "no_qualities": "Подходящие разрешения не найдены; доступен вариант «Наилучшее доступное».",
        "bitrate_hint": "Битрейт задаёт целевое качество файла; перекодирование не улучшает исходный звук.",
        "user_agent": "User-Agent", "ua_default": "По умолчанию yt-dlp", "ua_desktop": "Браузер на ПК", "ua_mobile": "Мобильный браузер", "ua_tv": "Smart TV",
    },
}

LANG_NAMES = {"en": "English", "ja": "日本語", "de": "Deutsch", "zh": "中文", "ru": "Русский"}
VIDEO_FORMATS = {"MP4": "mp4", "MKV": "mkv", "WebM": "webm"}
AUDIO_FORMATS = {"MP3": "mp3", "M4A": "m4a", "WAV": "wav", "FLAC": "flac", "OPUS": "opus"}
VIDEO_HEIGHTS = (4320, 2160, 1440, 1080, 720, 360, 240, 144)
AUDIO_BITRATES = (320, 256, 192, 128)
USER_AGENTS = {
    "ua_default": None,
    "ua_desktop": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "ua_mobile": "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
    "ua_tv": "Mozilla/5.0 (SMART-TV; Linux; Tizen 8.0) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/5.0 TV Safari/537.36",
}


class DownloaderApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.language = tk.StringVar(value="ja")
        self.kind = tk.StringVar(value="video")
        self.quality = tk.StringVar(value="")
        self.file_format = tk.StringVar(value="MP4")
        self.url = tk.StringVar()
        self.output_dir = tk.StringVar(value=str(Path.home() / "Downloads"))
        self.ytdlp_path = tk.StringVar(value=self._find_ytdlp() or "")
        self.ffmpeg_path = shutil.which("ffmpeg") or ""
        self.messages: queue.Queue[tuple[str, str]] = queue.Queue()
        self.result_queue: queue.Queue[tuple[str, object]] = queue.Queue()
        self.process: subprocess.Popen[str] | None = None
        self.busy = False
        self.available_heights: list[int] = []
        self._build_ui()
        self._translate()
        self._update_status()
        self.root.after(100, self._poll_messages)

    @staticmethod
    def _find_ytdlp() -> str:
        found = shutil.which("yt-dlp") or shutil.which("yt-dlp.exe")
        if found:
            return found
        try:
            import yt_dlp
            return str(Path(yt_dlp.__file__).parent / "__main__.py")
        except ImportError:
            return ""

    def tr(self, key: str) -> str:
        return TEXT[self.language.get()][key]

    def _build_ui(self) -> None:
        self.root.geometry("820x790")
        self.root.minsize(700, 680)
        self.root.columnconfigure(0, weight=1)
        outer = ttk.Frame(self.root, padding=18)
        outer.grid(sticky="nsew")
        outer.columnconfigure(1, weight=1)
        self.outer = outer
        self.style = ttk.Style()
        self.style.configure("App.TLabel", font=("Segoe UI", 10))
        self.style.configure("Title.TLabel", font=("Segoe UI Semibold", 18))
        self.style.configure("Hint.TLabel", font=("Segoe UI", 9))
        self.style.configure("TButton", padding=(12, 7), font=("Segoe UI", 10))
        self.style.configure("TCombobox", padding=5)
        self.style.configure("TEntry", padding=7)
        self.style.configure("Accent.TButton", padding=(16, 8), font=("Segoe UI Semibold", 10))

        self.heading = ttk.Label(outer, style="Title.TLabel")
        self.heading.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 12))

        self.lang_label = ttk.Label(outer)
        self.lang_label.grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(0, 12))
        self.lang_combo = ttk.Combobox(outer, state="readonly", width=18, values=list(LANG_NAMES.values()), takefocus=True)
        self.lang_combo.grid(row=1, column=1, sticky="w", pady=(0, 12))
        self.lang_combo.current(1)
        self.lang_combo.bind("<<ComboboxSelected>>", self._language_changed)

        self.url_label = ttk.Label(outer)
        self.url_label.grid(row=2, column=0, sticky="w", padx=(0, 10), pady=6)
        self.url_entry = ttk.Entry(outer, textvariable=self.url, takefocus=True)
        self.url_entry.grid(row=2, column=1, columnspan=2, sticky="ew", pady=6)

        self.folder_label = ttk.Label(outer)
        self.folder_label.grid(row=3, column=0, sticky="w", padx=(0, 10), pady=6)
        self.folder_entry = ttk.Entry(outer, textvariable=self.output_dir, takefocus=True)
        self.folder_entry.grid(row=3, column=1, sticky="ew", pady=6)
        self.browse_button = ttk.Button(outer, command=self._browse)
        self.browse_button.grid(row=3, column=2, padx=(8, 0), pady=6)

        self.user_agent_label = ttk.Label(outer)
        self.user_agent_label.grid(row=4, column=0, sticky="w", padx=(0, 10), pady=6)
        self.user_agent_combo = ttk.Combobox(outer, state="readonly", width=28, takefocus=True)
        self.user_agent_combo.grid(row=4, column=1, sticky="w", pady=6)

        ttk.Separator(outer).grid(row=5, column=0, columnspan=3, sticky="ew", pady=12)
        self.kind_label = ttk.Label(outer)
        self.kind_label.grid(row=6, column=0, sticky="w", padx=(0, 10), pady=5)
        self.kind_combo = ttk.Combobox(outer, state="readonly", width=20, takefocus=True)
        self.kind_combo.grid(row=6, column=1, sticky="w", pady=5)
        self.kind_combo.bind("<<ComboboxSelected>>", self._kind_changed)

        self.quality_label = ttk.Label(outer)
        self.quality_label.grid(row=7, column=0, sticky="w", padx=(0, 10), pady=5)
        self.quality_combo = ttk.Combobox(outer, state="readonly", width=24, takefocus=True)
        self.quality_combo.grid(row=7, column=1, sticky="ew", pady=5)
        self.check_quality_button = ttk.Button(outer, command=self._check_quality)
        self.check_quality_button.grid(row=7, column=2, padx=(8, 4), pady=5)

        self.format_label = ttk.Label(outer)
        self.format_label.grid(row=8, column=0, sticky="w", padx=(0, 10), pady=5)
        self.format_combo = ttk.Combobox(outer, state="readonly", width=24, takefocus=True)
        self.format_combo.grid(row=8, column=1, sticky="ew", pady=5)
        self.list_button = ttk.Button(outer, command=self._list_formats)
        self.list_button.grid(row=8, column=2, padx=(8, 4), pady=5)
        self.quality_hint = ttk.Label(outer, wraplength=650)
        self.quality_hint.grid(row=9, column=0, columnspan=3, sticky="w", pady=(5, 2))

        self.audio_hint = ttk.Label(outer, wraplength=620)
        self.audio_hint.grid(row=10, column=0, columnspan=3, sticky="w", pady=(3, 4))
        self.tool_status = ttk.Label(outer, wraplength=680)
        self.tool_status.grid(row=11, column=0, columnspan=3, sticky="w", pady=(3, 8))
        self.path_button = ttk.Button(outer, command=self._select_ytdlp)
        self.path_button.grid(row=12, column=0, columnspan=3, sticky="w", pady=(0, 8))

        self.progress = ttk.Progressbar(outer, mode="indeterminate")
        self.progress.grid(row=13, column=0, columnspan=3, sticky="ew", pady=6)
        buttons = ttk.Frame(outer)
        buttons.grid(row=14, column=0, columnspan=3, sticky="ew", pady=(4, 8))
        buttons.columnconfigure(0, weight=1)
        self.status_label = ttk.Label(buttons)
        self.status_label.grid(row=0, column=0, sticky="w")
        self.download_button = ttk.Button(buttons, command=self._download, style="Accent.TButton")
        self.download_button.grid(row=0, column=1, padx=(8, 0))
        self.cancel_button = ttk.Button(buttons, command=self._cancel)
        self.cancel_button.grid(row=0, column=2, padx=(8, 0))

        self.log_label = ttk.Label(outer)
        self.log_label.grid(row=15, column=0, columnspan=3, sticky="w", pady=(8, 4))
        self.log = tk.Text(outer, height=10, wrap="word", state="disabled")
        self.log.grid(row=16, column=0, columnspan=3, sticky="nsew")
        outer.rowconfigure(16, weight=1)
        self.usage_label = ttk.Label(outer, wraplength=680)
        self.usage_label.grid(row=17, column=0, columnspan=3, sticky="w", pady=(10, 0))
        self.url_entry.bind("<Return>", lambda _event: self._check_quality())
        self.root.bind("<Control-Return>", lambda _event: self._download())

    def _language_changed(self, _event: object = None) -> None:
        selected = self.lang_combo.get()
        self.language.set(next((code for code, name in LANG_NAMES.items() if name == selected), "en"))
        self._translate()

    def _translate(self) -> None:
        self.root.title(self.tr("title"))
        self.heading.configure(text=self.tr("title"))
        labels = ((self.lang_label, "language"), (self.url_label, "url"),
                  (self.folder_label, "folder"), (self.kind_label, "kind"),
                  (self.quality_label, "quality" if self.kind.get() == "video" else "audio_quality"),
                  (self.format_label, "format"), (self.log_label, "log"))
        for widget, key in labels:
            widget.configure(text=self.tr(key))
        self.browse_button.configure(text=self.tr("browse"))
        self.list_button.configure(text=self.tr("list"))
        self.check_quality_button.configure(text=self.tr("check_quality"))
        self.download_button.configure(text=self.tr("download"))
        self.cancel_button.configure(text=self.tr("cancel"))
        self.path_button.configure(text=f"{self.tr('select_ytdlp')}…")
        self.user_agent_label.configure(text=self.tr("user_agent"))
        ua_values = [self.tr(key) for key in USER_AGENTS]
        self.user_agent_combo.configure(values=ua_values)
        ua_index = list(USER_AGENTS).index(getattr(self, "selected_user_agent", "ua_default"))
        self.user_agent_combo.current(ua_index)
        self.user_agent_combo.bind("<<ComboboxSelected>>", lambda _event: setattr(self, "selected_user_agent", list(USER_AGENTS)[self.user_agent_combo.current()]))
        self.kind_combo.configure(values=[self.tr("video"), self.tr("audio")])
        self.kind_combo.set(self.tr(self.kind.get()))
        self.kind_combo.bind("<<ComboboxSelected>>", self._kind_changed)
        current_quality = getattr(self, "selected_quality", "")
        formats = VIDEO_FORMATS if self.kind.get() == "video" else AUDIO_FORMATS
        self.format_combo.configure(values=list(formats.keys()))
        if self.file_format.get() not in formats:
            self.file_format.set(next(iter(formats)))
        self.format_combo.set(self.file_format.get())
        self.quality_combo.configure(values=self._quality_options())
        self.quality_combo.set(current_quality if current_quality in self._quality_options() else self._quality_options()[0])
        self.audio_hint.configure(text=self.tr("audio_desc"))
        self.usage_label.configure(text=self.tr("usage"))
        self._update_kind()
        self.quality_combo.bind("<<ComboboxSelected>>", self._quality_changed)
        self._update_status()

    def _update_kind(self) -> None:
        label = self.kind_combo.get()
        self.kind.set("audio" if label == self.tr("audio") else "video")
        values = self._quality_options()
        self.quality_combo.configure(values=values)
        selected = getattr(self, "selected_quality", "")
        if selected not in values:
            selected = values[0]
        self.selected_quality = selected
        self.quality_combo.set(selected)
        self.quality_label.configure(text=self.tr("quality" if self.kind.get() == "video" else "audio_quality"))
        formats = AUDIO_FORMATS if self.kind.get() == "audio" else VIDEO_FORMATS
        self.format_combo.configure(values=list(formats.keys()))
        if self.file_format.get() not in formats:
            self.file_format.set(next(iter(formats)))
        self.format_combo.set(self.file_format.get())
        if self.kind.get() == "audio":
            self.quality_hint.configure(text=self.tr("bitrate_hint"))
        else:
            self.quality_hint.configure(text=self.tr("quality_hint") if self.available_heights else self.tr("quality_unchecked"))

    def _kind_changed(self, _event: object = None) -> None:
        selected = self.kind_combo.get()
        self.kind.set("audio" if selected == self.tr("audio") else "video")
        self.selected_quality = ""
        self._update_kind()

    def _quality_changed(self, _event: object = None) -> None:
        self.selected_quality = self.quality_combo.get()

    def _quality_options(self) -> list[str]:
        if self.kind.get() == "audio":
            return [self.tr("audio_best")] + [f"{rate} kbps" for rate in AUDIO_BITRATES]
        return [self.tr("best")] + [f"{height}p" for height in VIDEO_HEIGHTS if height in self.available_heights]

    def _update_status(self) -> None:
        y_ok = bool(self.ytdlp_path.get())
        f_ok = bool(self.ffmpeg_path and Path(self.ffmpeg_path).exists())
        y_text = self.tr("yt_found") if y_ok else self.tr("yt_missing")
        f_text = self.tr("ff_found") if f_ok else self.tr("ff_missing")
        self.tool_status.configure(text=f"{y_text}  •  {f_text}")

    def _browse(self) -> None:
        folder = filedialog.askdirectory(title=self.tr("choose_folder"), initialdir=self.output_dir.get())
        if folder:
            self.output_dir.set(folder)

    def _select_ytdlp(self) -> None:
        path = filedialog.askopenfilename(title=self.tr("select_ytdlp"), filetypes=[(self.tr("select_exe"), "*.exe"), ("All files", "*.*")])
        if path:
            self.ytdlp_path.set(path)
            self._update_status()

    def _command(self) -> list[str]:
        executable = self.ytdlp_path.get()
        if executable.lower().endswith("__main__.py"):
            return [sys.executable, executable]
        return [executable]

    def _list_formats(self) -> None:
        if not self._validate():
            return
        self._start_task("formats")

    def _check_quality(self) -> None:
        if not self._validate():
            return
        self._start_task("quality")

    def _download(self) -> None:
        if not self._validate():
            return
        kind = self.kind.get()
        if kind == "audio" and not self.ffmpeg_path:
            messagebox.showerror(self.tr("title"), self.tr("need_ffmpeg"))
            return
        if self.kind.get() == "video" and not self.available_heights:
            self._check_quality()
            self._append_log(self.tr("quality_unchecked"))
            return
        self._start_task("download")

    def _validate(self) -> bool:
        if not self.url.get().strip():
            messagebox.showerror(self.tr("title"), self.tr("need_url"))
            return False
        if not self.ytdlp_path.get():
            messagebox.showerror(self.tr("title"), self.tr("need_ytdlp"))
            return False
        return True

    def _start_task(self, task: str) -> None:
        if self.busy:
            return
        self.busy = True
        self.task_settings = {
            "user_agent": USER_AGENTS[list(USER_AGENTS)[self.user_agent_combo.current()]],
            "quality": self.quality_combo.get().strip(),
            "kind": self.kind.get(),
            "file_format": self.file_format.get(),
            "url": self.url.get().strip(),
            "output_dir": self.output_dir.get(),
        }
        self.progress.start(10)
        self.status_label.configure(text=self.tr("working"))
        self.download_button.configure(state="disabled")
        self.list_button.configure(state="disabled")
        threading.Thread(target=self._worker, args=(task,), daemon=True).start()

    def _worker(self, task: str) -> None:
        command = self._command() + ["--no-warnings", "--no-playlist"]
        settings = self.task_settings
        user_agent = settings["user_agent"]
        if user_agent:
            command += ["--user-agent", user_agent]
        if self.ffmpeg_path:
            command += ["--ffmpeg-location", self.ffmpeg_path]
        command += ["--newline", "--progress"]
        if task in ("formats", "quality"):
            command += ["--dump-single-json", "--skip-download", settings["url"]]
        else:
            kind = settings["kind"]
            extension = (AUDIO_FORMATS if kind == "audio" else VIDEO_FORMATS)[settings["file_format"]]
            quality = settings["quality"]
            if quality.isdigit():
                fmt = quality
            elif quality.endswith("p") and quality[:-1].isdigit():
                height = int(quality[:-1])
                fmt = f"bestvideo[height<={height}]+bestaudio/best[height<={height}]/best"
            elif kind == "video":
                fmt = "bestvideo*+bestaudio/best"
            else:
                fmt = "bestaudio/best"
            command += ["--format", fmt, "--output", str(Path(settings["output_dir"]) / "%(title)s.%(ext)s")]
            if kind == "audio":
                command += ["--extract-audio", "--audio-format", extension]
                if quality.endswith(" kbps") and quality[:-5].isdigit():
                    command += ["--audio-quality", quality[:-5]]
            elif extension != "mp4":
                command += ["--merge-output-format", extension]
            command += [settings["url"]]
        try:
            self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                            text=True, encoding="utf-8", errors="replace", bufsize=1,
                                            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            assert self.process.stdout
            json_output = ""
            for line in self.process.stdout:
                if task in ("formats", "quality"):
                    json_output += line
                    continue
                self.messages.put(("log", line.rstrip()))
            code = self.process.wait()
            if code == 0:
                if task in ("formats", "quality"):
                    try:
                        metadata = json.loads(json_output)
                    except json.JSONDecodeError as exc:
                        self.messages.put(("log", f"Could not parse yt-dlp metadata: {exc}"))
                        self.messages.put(("result", "failed"))
                        return
                    heights = sorted({int(item["height"]) for item in metadata.get("formats", [])
                                      if item.get("height") and item.get("vcodec") != "none"}, reverse=True)
                    self.result_queue.put((task, {"heights": heights, "metadata": metadata}))
                self.messages.put(("result", task if task in ("formats", "quality") else "done"))
            else:
                self.messages.put(("result", "failed"))
        except Exception as exc:
            self.messages.put(("log", str(exc)))
            self.messages.put(("result", "failed"))
        finally:
            self.process = None

    def _cancel(self) -> None:
        process = self.process
        if process and process.poll() is None:
            process.terminate()
        self.messages.put(("result", "cancelled"))

    def _poll_messages(self) -> None:
        try:
            while True:
                kind, value = self.messages.get_nowait()
                if kind == "log":
                    self.log.configure(state="normal")
                    self.log.insert("end", value + "\n")
                    self.log.see("end")
                    self.log.configure(state="disabled")
                else:
                    payload = None
                    if value in ("formats", "quality"):
                        try:
                            _task, payload = self.result_queue.get_nowait()
                        except queue.Empty:
                            payload = None
                    self.busy = False
                    self.progress.stop()
                    self.download_button.configure(state="normal")
                    self.list_button.configure(state="normal")
                    if value == "formats":
                        if payload:
                            self._log_formats(payload["metadata"])
                        self.status_label.configure(text=self.tr("ready"))
                        self._append_log(self.tr("formats_ready"))
                    elif value == "quality":
                        self.available_heights = payload["heights"] if payload else []
                        options = self._quality_options()
                        self.quality_combo.configure(values=options)
                        self.selected_quality = options[0]
                        self.quality_combo.set(options[0])
                        self.quality_hint.configure(text=self.tr("quality_hint") if self.available_heights else self.tr("no_qualities"))
                        self.status_label.configure(text=self.tr("ready"))
                    elif value == "done":
                        self.status_label.configure(text=self.tr("done"))
                    elif value == "cancelled":
                        self.status_label.configure(text=self.tr("cancelled"))
                    else:
                        self.status_label.configure(text=self.tr("failed"))
        except queue.Empty:
            pass
        self.root.after(100, self._poll_messages)

    def _append_log(self, value: str) -> None:
        self.log.configure(state="normal")
        self.log.insert("end", value + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def _log_formats(self, metadata: dict) -> None:
        formats = metadata.get("formats", [])
        self._append_log(f"{metadata.get('title', 'Media')} — {len(formats)} formats")
        for item in formats:
            height = item.get("height")
            ext = item.get("ext", "?")
            fid = item.get("format_id", "?")
            note = item.get("format_note", "")
            self._append_log(f"{fid}: {height or 'audio'}p {ext} {note}".strip())


def main() -> None:
    root = tk.Tk()
    try:
        ttk.Style().theme_use("vista" if sys.platform == "win32" else "clam")
    except tk.TclError:
        pass
    DownloaderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
