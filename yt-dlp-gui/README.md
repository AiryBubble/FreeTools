# yt-dlp-gui

[English](#English) | [日本語](#日本語) | [Deutsch](#Deutsch) | [简体中文](#简体中文) | [Русский](#Русский)

## English

A lightweight desktop GUI built with Python and Tkinter. It uses `yt-dlp` and FFmpeg. The interface supports English, Japanese, German, Simplified Chinese, and Russian.

### Install and run

Requires Python 3.10+ with Tkinter, yt-dlp, and FFmpeg. On Windows, install the tools with `winget install --id yt-dlp.yt-dlp` and `winget install Gyan.FFmpeg`, then run `python .\main.py`. You can also select the yt-dlp executable in the app.

Paste a URL and click **Check available quality** beside the quality selector. Only available options among 4320p, 2160p, 1440p, 1080p, 720p, 360p, 240p, and 144p are shown. **List formats** is beside the file format selector and prints format IDs in Activity. Audio offers Best available or 320/256/192/128 kbps output targets. Re-encoding cannot improve the source audio. Choose a user-agent profile: yt-dlp default, desktop browser, mobile browser, or Smart TV. Downloads are saved to the selected folder.

Keyboard: Tab/Enter to navigate, Enter in the URL field to check quality, Ctrl+Enter to download. Use only for content you are authorized to download and follow applicable terms and copyright laws.

Optional Windows build: `python -m pip install pyinstaller` then `pyinstaller --onefile --windowed --name YouTubeDownloader .\main.py`. yt-dlp and FFmpeg remain external requirements.

## 日本語

PythonとTkinterで作成した軽量デスクトップGUIです。`yt-dlp`とFFmpegを使用します。英語・日本語・ドイツ語・中国語（簡体字）・ロシア語に対応しています。

### インストールと起動

Python 3.10以降（Tkinter付き）、yt-dlp、FFmpegが必要です。Windowsでは`winget install --id yt-dlp.yt-dlp`と`winget install Gyan.FFmpeg`で導入し、`python .\main.py`で起動します。yt-dlp実行ファイルはアプリ内から指定することもできます。

URLを貼り付け、画質欄の横にある「画質を確認」を押すと、利用可能な4320p、2160p、1440p、1080p、720p、360p、240p、144pだけを表示します。「形式一覧」はファイル形式欄の横にあり、形式IDを処理状況欄に表示します。音声は最良の品質、または320/256/192/128 kbpsの出力目標を選択できます。再エンコードで元音声より高音質にはなりません。ユーザーエージェントはyt-dlp標準、デスクトップ、モバイル、スマートTVから選べます。保存先は画面で指定します。

キーボード操作：Tab/Enterで移動、URL欄でEnterを押すと画質確認、Ctrl+Enterでダウンロードします。ダウンロードが許可されたコンテンツにのみ使用し、利用規約と著作権法を遵守してください。

Windows実行ファイルの作成（任意）：`python -m pip install pyinstaller`の後、`pyinstaller --onefile --windowed --name YouTubeDownloader .\main.py`を実行します。yt-dlpとFFmpegは別途必要です。

## Deutsch

Leichte Desktop-GUI mit Python und Tkinter, die `yt-dlp` und FFmpeg verwendet. Die Oberfläche unterstützt Englisch, Japanisch, Deutsch, vereinfachtes Chinesisch und Russisch.

### Installation und Start

Erforderlich sind Python 3.10+ mit Tkinter, yt-dlp und FFmpeg. Unter Windows installieren Sie die Werkzeuge mit `winget install --id yt-dlp.yt-dlp` und `winget install Gyan.FFmpeg` und starten anschließend mit `python .\main.py`. Die yt-dlp-Datei kann auch in der App ausgewählt werden.

URL einfügen und neben der Qualitätsauswahl auf **Qualität prüfen** klicken. Angezeigt werden nur verfügbare Optionen aus 4320p, 2160p, 1440p, 1080p, 720p, 360p, 240p und 144p. **Formate anzeigen** steht neben der Dateiformatauswahl und zeigt Format-IDs im Aktivitätsbereich. Für Audio gibt es Beste verfügbare oder 320/256/192/128 kbps als Ausgabeziel. Neukodierung verbessert die Quellqualität nicht. User-Agent: yt-dlp-Standard, Desktopbrowser, mobiler Browser oder Smart-TV. Der Speicherordner ist auswählbar.

Tastatur: Tab/Enter zur Navigation, Enter im URL-Feld prüft die Qualität, Strg+Enter startet den Download. Nur berechtigte Inhalte herunterladen und geltende Nutzungsbedingungen sowie Urheberrecht beachten.

Optionaler Windows-Build: `python -m pip install pyinstaller`, danach `pyinstaller --onefile --windowed --name YouTubeDownloader .\main.py`. yt-dlp und FFmpeg bleiben externe Voraussetzungen.

## 简体中文

使用 Python 和 Tkinter 构建的轻量桌面 GUI，调用 `yt-dlp` 和 FFmpeg。界面支持英语、日语、德语、简体中文和俄语。

### 安装与运行

需要安装带 Tkinter 的 Python 3.10+、yt-dlp 和 FFmpeg。Windows 可运行 `winget install --id yt-dlp.yt-dlp` 和 `winget install Gyan.FFmpeg` 安装，然后运行 `python .\main.py`。也可以在应用中选择 yt-dlp 可执行文件。

粘贴网址并点击画质选择旁的“检查可用画质”。只显示实际可用的 4320p、2160p、1440p、1080p、720p、360p、240p、144p。“查看格式”按钮位于文件格式选择旁，会在活动区域列出格式 ID。音频可选择最佳质量或 320/256/192/128 kbps 输出目标；重新编码无法提升源音频质量。用户代理可选 yt-dlp 默认、桌面浏览器、移动浏览器或智能电视。可选择保存目录。

键盘操作：Tab/Enter 导航；在网址框按 Enter 检查画质；Ctrl+Enter 开始下载。请仅下载获准内容，并遵守服务条款和版权法律。

可选 Windows 打包：运行 `python -m pip install pyinstaller`，再运行 `pyinstaller --onefile --windowed --name YouTubeDownloader .\main.py`。yt-dlp 和 FFmpeg 仍需单独安装。

## Русский

Лёгкое настольное приложение на Python и Tkinter, использующее `yt-dlp` и FFmpeg. Интерфейс доступен на английском, японском, немецком, упрощённом китайском и русском языках.

### Установка и запуск

Нужны Python 3.10+ с Tkinter, yt-dlp и FFmpeg. В Windows установите их командами `winget install --id yt-dlp.yt-dlp` и `winget install Gyan.FFmpeg`, затем запустите `python .\main.py`. Исполняемый файл yt-dlp также можно выбрать в приложении.

Вставьте ссылку и нажмите «Проверить качество» рядом с выбором качества. Отображаются только доступные варианты из 4320p, 2160p, 1440p, 1080p, 720p, 360p, 240p и 144p. Кнопка «Показать форматы» находится рядом с выбором формата файла и выводит ID форматов в журнал. Для аудио доступны наилучшее качество и целевой битрейт 320/256/192/128 кбит/с. Перекодирование не улучшает исходный звук. User-Agent: по умолчанию yt-dlp, браузер ПК, мобильный браузер или Smart TV. Папку сохранения можно выбрать.

Клавиатура: Tab/Enter для навигации, Enter в поле ссылки проверяет качество, Ctrl+Enter начинает загрузку. Загружайте только разрешённый контент, соблюдая условия сервиса и авторские права.

Необязательная сборка для Windows: `python -m pip install pyinstaller`, затем `pyinstaller --onefile --windowed --name YouTubeDownloader .\main.py`. yt-dlp и FFmpeg устанавливаются отдельно.
