import sys
import os

# Carpeta de configuración: misma carpeta que el ejecutable/script
if getattr(sys, 'frozen', False):
    CONFIG_DIR = os.path.dirname(sys.executable)
else:
    CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(CONFIG_DIR, exist_ok=True)

import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess
import json
from pathlib import Path
from typing import Optional, Dict, List, Union
import traceback
import threading
import urllib.parse
import webbrowser

# Configuración de archivos (siempre relativos a CONFIG_DIR)
CONFIG_FILE = Path(CONFIG_DIR) / "config.conf"
PARAMS_FILE = Path(CONFIG_DIR) / "params.conf"
HISTORY_FILE = Path(CONFIG_DIR) / "history.json"
BOOKMARKS_FILE = Path(CONFIG_DIR) / "bookmarks.json"
LANGUAGE_FILE = Path(CONFIG_DIR) / "language.conf"

LANGUAGES = {
    "en": "English",
    "es": "Español",
    "ja": "日本語",
    "zh": "简体中文",
    "ko": "한국어",
    "pt": "Português",
    "fr": "Français",
    "it": "Italiano",
    "ru": "Русский",
    "de": "Deutsch"
}

TRANSLATIONS = {
    "title": {
        "en": "MPV Launcher",
        "es": "Lanzador de MPV",
        "ja": "MPVランチャー",
        "zh": "MPV启动器",
        "ko": "MPV 실행기",
        "pt": "Iniciador MPV",
        "fr": "Lanceur MPV",
        "it": "Avviatore MPV",
        "ru": "Запускатель MPV",
        "de": "MPV Starter"
    },
    "select_mpv": {
        "en": "Select MPV",
        "es": "Seleccionar MPV",
        "ja": "MPVを選択",
        "zh": "选择MPV",
        "ko": "MPV 선택",
        "pt": "Selecionar MPV",
        "fr": "Sélectionner MPV",
        "it": "Seleziona MPV",
        "ru": "Выбрать MPV",
        "de": "MPV auswählen"
    },
    "mpv": {
        "en": "MPV:",
        "es": "MPV:",
        "ja": "MPV:",
        "zh": "MPV：",
        "ko": "MPV:",
        "pt": "MPV:",
        "fr": "MPV:",
        "it": "MPV:",
        "ru": "MPV:",
        "de": "MPV:"
    },
    "mpv_not_selected": {
        "en": "MPV: Not selected",
        "es": "MPV: No seleccionado",
        "ja": "MPV: 未選択",
        "zh": "MPV：未选择",
        "ko": "MPV: 선택되지 않음",
        "pt": "MPV: Não selecionado",
        "fr": "MPV : Non sélectionné",
        "it": "MPV: Non selezionato",
        "ru": "MPV: Не выбрано",
        "de": "MPV: Nicht ausgewählt"
    },
    "media_link": {
        "en": "Media link:",
        "es": "Enlace multimedia:",
        "ja": "メディアリンク：",
        "zh": "媒体链接：",
        "ko": "미디어 링크:",
        "pt": "Link de mídia:",
        "fr": "Lien média :",
        "it": "Link multimediale:",
        "ru": "Медиа-ссылка:",
        "de": "Medienlink:"
    },
    "params": {
        "en": "Parameters:",
        "es": "Parámetros:",
        "ja": "パラメータ：",
        "zh": "参数：",
        "ko": "매개변수:",
        "pt": "Parâmetros:",
        "fr": "Paramètres :",
        "it": "Parametri:",
        "ru": "Параметры:",
        "de": "Parameter:"
    },
    "bookmark_title": {
        "en": "Bookmark title:",
        "es": "Título del marcador:",
        "ja": "ブックマークタイトル：",
        "zh": "书签标题：",
        "ko": "북마크 제목:",
        "pt": "Título do marcador:",
        "fr": "Titre du signet :",
        "it": "Titolo segnalibro:",
        "ru": "Название закладки:",
        "de": "Lesezeichentitel:"
    },
    "save_bookmark": {
        "en": "Save bookmark",
        "es": "Guardar marcador",
        "ja": "ブックマークを保存",
        "zh": "保存书签",
        "ko": "북마크 저장",
        "pt": "Salvar marcador",
        "fr": "Enregistrer le signet",
        "it": "Salva segnalibro",
        "ru": "Сохранить закладку",
        "de": "Lesezeichen speichern"
    },
    "launch_mpv": {
        "en": "Launch MPV",
        "es": "Iniciar MPV",
        "ja": "MPVを起動",
        "zh": "启动MPV",
        "ko": "MPV 실행",
        "pt": "Iniciar MPV",
        "fr": "Lancer MPV",
        "it": "Avvia MPV",
        "ru": "Запустить MPV",
        "de": "MPV starten"
    },
    "saved_params": {
        "en": "Saved parameters:",
        "es": "Parámetros guardados:",
        "ja": "保存されたパラメータ：",
        "zh": "已保存参数：",
        "ko": "저장된 매개변수:",
        "pt": "Parâmetros salvos:",
        "fr": "Paramètres enregistrés :",
        "it": "Parametri salvati:",
        "ru": "Сохранённые параметры:",
        "de": "Gespeicherte Parameter:"
    },
    "history": {
        "en": "History",
        "es": "Historial",
        "ja": "履歴",
        "zh": "历史记录",
        "ko": "기록",
        "pt": "Histórico",
        "fr": "Historique",
        "it": "Cronologia",
        "ru": "История",
        "de": "Verlauf"
    },
    "bookmarks": {
        "en": "Bookmarks",
        "es": "Marcadores",
        "ja": "ブックマーク",
        "zh": "书签",
        "ko": "북마크",
        "pt": "Marcadores",
        "fr": "Signets",
        "it": "Segnalibri",
        "ru": "Закладки",
        "de": "Lesezeichen"
    },
    "about": {
        "en": "About",
        "es": "Acerca de",
        "ja": "情報",
        "zh": "关于",
        "ko": "정보",
        "pt": "Sobre",
        "fr": "À propos",
        "it": "Informazioni",
        "ru": "О программе",
        "de": "Über"
    },
    "language": {
        "en": "Language",
        "es": "Idioma",
        "ja": "言語",
        "zh": "语言",
        "ko": "언어",
        "pt": "Idioma",
        "fr": "Langue",
        "it": "Lingua",
        "ru": "Язык",
        "de": "Sprache"
    },
    "close": {
        "en": "Close",
        "es": "Cerrar",
        "ja": "閉じる",
        "zh": "关闭",
        "ko": "닫기",
        "pt": "Fechar",
        "fr": "Fermer",
        "it": "Chiudi",
        "ru": "Закрыть",
        "de": "Schließen"
    },
    "about_text": {
        "en": (
            "This application allows you to launch the MPV player with online media links (YouTube, Twitch, Vimeo, etc.), "
            "focused on quick and effective use based on dynamic and personalized launch parameter selection for each execution.\n\n"
            "Main features:\n"
            "✔️ Select the MPV executable path.\n"
            "✔️ Enter local or internet media links to play them.\n"
            "✔️ Add and select MPV parameters via checkboxes.\n"
            "✔️ Save and manage custom parameters for future sessions.\n"
            "✔️ Automatic history of the last 100 played links, accessible from the menu.\n"
            "✔️ Save and manage custom bookmarks with title and link.\n"
            "✔️ Quick access to bookmarks and history from the top bar.\n"
            "✔️ Link and path validation before launching MPV.\n"
            "✔️ Intuitive and easy-to-use graphical interface.\n"
            "✔️ Direct access to official MPV repositories and downloads.\n"
            "✔️ All configuration and data are safely stored in local files."
        ),
        "es": (
            "Esta aplicación permite lanzar el reproductor MPV con enlaces de contenido multimedia online (YouTube, Twitch, Vimeo, etc.), "
            "con el enfoque de un uso rápido y efectivo basado en la selección de parámetros de lanzamiento de manera dinámica y personalizada para cada ejecución del reproductor.\n\n"
            "Características principales:\n"
            "✔️ Selecciona la ruta del ejecutable de MPV.\n"
            "✔️ Introduce enlaces multimedia locales o de internet para reproducirlos.\n"
            "✔️ Añade y selecciona parámetros de MPV mediante casillas de verificación.\n"
            "✔️ Guarda y administra parámetros personalizados para futuras sesiones.\n"
            "✔️ Historial automático de los últimos 100 enlaces reproducidos, accesibles desde el menú.\n"
            "✔️ Guarda y administra marcadores personalizados con título y enlace.\n"
            "✔️ Acceso rápido a los marcadores y al historial desde la barra superior.\n"
            "✔️ Validación de enlaces y rutas antes de lanzar MPV.\n"
            "✔️ Interfaz gráfica intuitiva y fácil de usar.\n"
            "✔️ Acceso directo a los repositorios y descargas oficiales de MPV.\n"
            "✔️ Toda la configuración y datos se guardan de forma segura en archivos locales."
        ),
        "ja": (
            "このアプリケーションは、MPVプレーヤーをオンラインメディアリンク（YouTube、Twitch、Vimeoなど）で起動でき、"
            "各実行ごとに動的かつ個別に起動パラメータを選択することで、迅速かつ効果的な利用を実現します。\n\n"
            "主な機能:\n"
            "✔️ MPV実行ファイルのパスを選択\n"
            "✔️ ローカルまたはインターネットのメディアリンクを入力して再生\n"
            "✔️ チェックボックスでMPVパラメータを追加・選択\n"
            "✔️ カスタムパラメータを保存・管理\n"
            "✔️ メニューからアクセスできる最新100件の履歴\n"
            "✔️ タイトルとリンク付きのブックマークを保存・管理\n"
            "✔️ 上部バーからブックマークと履歴に素早くアクセス\n"
            "✔️ MPV起動前のリンクとパスの検証\n"
            "✔️ 直感的で使いやすいGUI\n"
            "✔️ 公式MPVリポジトリとダウンロードへの直接アクセス\n"
            "✔️ すべての設定とデータはローカルファイルに安全に保存"
        ),
        "zh": (
            "本应用允许通过在线视频链接（YouTube、Twitch、Vimeo等）启动MPV播放器，"
            "专注于每次启动时动态、个性化选择启动参数，实现快速高效的使用体验。\n\n"
            "主要功能：\n"
            "✔️ 选择MPV可执行文件路径。\n"
            "✔️ 输入本地或互联网媒体链接进行播放。\n"
            "✔️ 通过复选框添加和选择MPV参数。\n"
            "✔️ 保存和管理自定义参数以便下次使用。\n"
            "✔️ 自动保存最近100个播放链接的历史，菜单可访问。\n"
            "✔️ 保存和管理带标题和链接的自定义书签。\n"
            "✔️ 顶部栏快速访问书签和历史。\n"
            "✔️ 启动MPV前验证链接和路径。\n"
            "✔️ 直观易用的图形界面。\n"
            "✔️ 直接访问MPV官方仓库和下载。\n"
            "✔️ 所有配置和数据均安全保存在本地文件中。"
        ),
        "ko": (
            "이 애플리케이션은 온라인 미디어 링크(YouTube, Twitch, Vimeo 등)로 MPV 플레이어를 실행할 수 있으며, "
            "각 실행마다 동적이고 맞춤형 실행 매개변수 선택을 통해 빠르고 효과적인 사용을 제공합니다.\n\n"
            "주요 기능:\n"
            "✔️ MPV 실행 파일 경로 선택\n"
            "✔️ 로컬 또는 인터넷 미디어 링크 입력 및 재생\n"
            "✔️ 체크박스로 MPV 매개변수 추가 및 선택\n"
            "✔️ 맞춤 매개변수 저장 및 관리\n"
            "✔️ 메뉴에서 접근 가능한 최근 100개 재생 기록\n"
            "✔️ 제목과 링크가 있는 맞춤 북마크 저장 및 관리\n"
            "✔️ 상단 바에서 북마크 및 기록에 빠르게 접근\n"
            "✔️ MPV 실행 전 링크 및 경로 검증\n"
            "✔️ 직관적이고 사용하기 쉬운 GUI\n"
            "✔️ 공식 MPV 저장소 및 다운로드 바로가기\n"
            "✔️ 모든 설정과 데이터는 로컬 파일에 안전하게 저장"
        ),
        "pt": (
            "Este aplicativo permite iniciar o reprodutor MPV com links de mídia online (YouTube, Twitch, Vimeo, etc.), "
            "focado em uso rápido e eficaz baseado na seleção dinâmica e personalizada de parâmetros de inicialização para cada execução.\n\n"
            "Principais características:\n"
            "✔️ Selecione o caminho do executável do MPV.\n"
            "✔️ Insira links de mídia locais ou da internet para reproduzi-los.\n"
            "✔️ Adicione e selecione parâmetros do MPV por caixas de seleção.\n"
            "✔️ Salve e gerencie parâmetros personalizados para sessões futuras.\n"
            "✔️ Histórico automático dos últimos 100 links reproduzidos, acessível pelo menu.\n"
            "✔️ Salve e gerencie favoritos personalizados com título e link.\n"
            "✔️ Acesso rápido aos favoritos e histórico pela barra superior.\n"
            "✔️ Validação de links e caminhos antes de iniciar o MPV.\n"
            "✔️ Interface gráfica intuitiva e fácil de usar.\n"
            "✔️ Acesso direto aos repositórios e downloads oficiais do MPV.\n"
            "✔️ Todas as configurações e dados são salvos com segurança em arquivos locais."
        ),
        "fr": (
            "Cette application permet de lancer le lecteur MPV avec des liens multimédias en ligne (YouTube, Twitch, Vimeo, etc.), "
            "axée sur une utilisation rapide et efficace grâce à la sélection dynamique et personnalisée des paramètres de lancement à chaque exécution.\n\n"
            "Fonctionnalités principales :\n"
            "✔️ Sélectionnez le chemin de l'exécutable MPV.\n"
            "✔️ Entrez des liens multimédias locaux ou Internet à lire.\n"
            "✔️ Ajoutez et sélectionnez des paramètres MPV via des cases à cocher.\n"
            "✔️ Enregistrez et gérez des paramètres personnalisés pour de futures sessions.\n"
            "✔️ Historique automatique des 100 derniers liens lus, accessible depuis le menu.\n"
            "✔️ Enregistrez et gérez des favoris personnalisés avec titre et lien.\n"
            "✔️ Accès rapide aux favoris et à l'historique depuis la barre supérieure.\n"
            "✔️ Validation des liens et chemins avant de lancer MPV.\n"
            "✔️ Interface graphique intuitive et facile à utiliser.\n"
            "✔️ Accès direct aux dépôts et téléchargements officiels de MPV.\n"
            "✔️ Toutes les configurations et données sont enregistrées en toute sécurité dans des fichiers locaux."
        ),
        "it": (
            "Questa applicazione consente di avviare il lettore MPV con link multimediali online (YouTube, Twitch, Vimeo, ecc.), "
            "concentrandosi su un uso rapido ed efficace basato sulla selezione dinamica e personalizzata dei parametri di avvio per ogni esecuzione.\n\n"
            "Caratteristiche principali:\n"
            "✔️ Seleziona il percorso dell'eseguibile MPV.\n"
            "✔️ Inserisci link multimediali locali o Internet da riprodurre.\n"
            "✔️ Aggiungi e seleziona parametri MPV tramite caselle di controllo.\n"
            "✔️ Salva e gestisci parametri personalizzati per sessioni future.\n"
            "✔️ Cronologia automatica degli ultimi 100 link riprodotti, accessibile dal menu.\n"
            "✔️ Salva e gestisci segnalibri personalizzati con titolo e link.\n"
            "✔️ Accesso rapido a segnalibri e cronologia dalla barra superiore.\n"
            "✔️ Validazione di link e percorsi prima di avviare MPV.\n"
            "✔️ Interfaccia grafica intuitiva e facile da usare.\n"
            "✔️ Accesso diretto ai repository e ai download ufficiali di MPV.\n"
            "✔️ Tutte le configurazioni e i dati vengono salvati in modo sicuro in file locali."
        ),
        "ru": (
            "Это приложение позволяет запускать проигрыватель MPV с онлайн-медиа-ссылками (YouTube, Twitch, Vimeo и др.), "
            "с акцентом на быстрое и эффективное использование благодаря динамическому и индивидуальному выбору параметров запуска для каждого запуска.\n\n"
            "Основные возможности:\n"
            "✔️ Выбор пути к исполняемому файлу MPV.\n"
            "✔️ Ввод локальных или интернет-ссылок для воспроизведения.\n"
            "✔️ Добавление и выбор параметров MPV с помощью флажков.\n"
            "✔️ Сохранение и управление пользовательскими параметрами для будущих сессий.\n"
            "✔️ Автоматическая история последних 100 воспроизведённых ссылок, доступная из меню.\n"
            "✔️ Сохранение и управление закладками с названием и ссылкой.\n"
            "✔️ Быстрый доступ к закладкам и истории с верхней панели.\n"
            "✔️ Проверка ссылок и путей перед запуском MPV.\n"
            "✔️ Интуитивно понятный и простой графический интерфейс.\n"
            "✔️ Прямой доступ к официальным репозиториям и загрузкам MPV.\n"
            "✔️ Все настройки и данные надёжно сохраняются в локальных файлах."
        ),
        "de": (
            "Diese Anwendung ermöglicht das Starten des MPV-Players mit Online-Medienlinks (YouTube, Twitch, Vimeo usw.), "
            "fokussiert auf eine schnelle und effektive Nutzung durch dynamische und personalisierte Auswahl von Startparametern für jede Ausführung.\n\n"
            "Hauptfunktionen:\n"
            "✔️ Wählen Sie den Pfad zur MPV-Programmdatei.\n"
            "✔️ Geben Sie lokale oder Internet-Medienlinks zur Wiedergabe ein.\n"
            "✔️ Fügen Sie MPV-Parameter per Checkbox hinzu und wählen Sie sie aus.\n"
            "✔️ Speichern und verwalten Sie benutzerdefinierte Parameter für zukünftige Sitzungen.\n"
            "✔️ Automatische Historie der letzten 100 wiedergegebenen Links, über das Menü zugänglich.\n"
            "✔️ Speichern und verwalten Sie benutzerdefinierte Lesezeichen mit Titel und Link.\n"
            "✔️ Schneller Zugriff auf Lesezeichen und Verlauf über die obere Leiste.\n"
            "✔️ Validierung von Links und Pfaden vor dem Start von MPV.\n"
            "✔️ Intuitive und einfach zu bedienende grafische Oberfläche.\n"
            "✔️ Direkter Zugriff auf offizielle MPV-Repositories und Downloads.\n"
            "✔️ Alle Einstellungen und Daten werden sicher in lokalen Dateien gespeichert."
        ),
    },
    "about_author": {
        "en": "Kenneth Andrey Pinto Medina - Developer",
        "es": "Kenneth Andrey Pinto Medina - Desarrollador",
        "ja": "Kenneth Andrey Pinto Medina - 開発者",
        "zh": "Kenneth Andrey Pinto Medina - 开发者",
        "ko": "Kenneth Andrey Pinto Medina - 개발자",
        "pt": "Kenneth Andrey Pinto Medina - Desenvolvedor",
        "fr": "Kenneth Andrey Pinto Medina - Développeur",
        "it": "Kenneth Andrey Pinto Medina - Sviluppatore",
        "ru": "Kenneth Andrey Pinto Medina - Разработчик",
        "de": "Kenneth Andrey Pinto Medina - Entwickler"
    },
    "about_github": {
        "en": "Personal GitHub:",
        "es": "GitHub personal:",
        "ja": "個人GitHub：",
        "zh": "个人GitHub：",
        "ko": "개인 GitHub:",
        "pt": "GitHub pessoal:",
        "fr": "GitHub personnel :",
        "it": "GitHub personale:",
        "ru": "Личный GitHub:",
        "de": "Persönliches GitHub:"
    },
    "about_repo": {
        "en": "MPV repository:",
        "es": "Repositorio de MPV:",
        "ja": "MPVリポジトリ：",
        "zh": "MPV仓库：",
        "ko": "MPV 저장소:",
        "pt": "Repositório MPV:",
        "fr": "Dépôt MPV :",
        "it": "Repository MPV:",
        "ru": "Репозиторий MPV:",
        "de": "MPV-Repository:"
    },
    "about_download": {
        "en": "MPV downloads for Windows:",
        "es": "Descargas MPV para Windows:",
        "ja": "Windows用MPVダウンロード：",
        "zh": "Windows版MPV下载：",
        "ko": "Windows용 MPV 다운로드:",
        "pt": "Downloads do MPV para Windows:",
        "fr": "Téléchargements MPV pour Windows :",
        "it": "Download MPV per Windows:",
        "ru": "Загрузки MPV для Windows:",
        "de": "MPV-Downloads für Windows:"
    },
    "about_year": {
        "en": "2025",
        "es": "2025",
        "ja": "2025年",
        "zh": "2025年",
        "ko": "2025년",
        "pt": "2025",
        "fr": "2025",
        "it": "2025",
        "ru": "2025",
        "de": "2025"
    }
    # Agrega más claves según sea necesario...
}

def get_translation(key, lang):
    """Devuelve la traducción para una clave y un idioma, o inglés si falta."""
    return TRANSLATIONS.get(key, {}).get(lang) or TRANSLATIONS.get(key, {}).get("en") or key

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lanzador de MPV")
        self.geometry("680x550")
        
        # Configuración inicial
        self.setup_files()
        self.load_all_data()
        self.param_vars: Dict[str, tk.BooleanVar] = {}
        self.language = self.load_language()
        
        # Interfaz gráfica
        self.create_widgets()
        self.setup_menu()
        self.refresh_param_checkboxes()
        self.update_params_entry()
        
        # Evento de cierre seguro
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    # region Inicialización y configuración
    def setup_files(self):
        """Asegura la existencia de todos los archivos necesarios"""
        try:
            for path, default in [
                (CONFIG_FILE, {"mpv_path": ""}),
                (PARAMS_FILE, []),
                (HISTORY_FILE, []),
                (BOOKMARKS_FILE, {}),
                (LANGUAGE_FILE, "en")
            ]:
                if not path.exists():
                    try:
                        self.save_json(path, default)
                    except FileNotFoundError:
                        path.parent.mkdir(parents=True, exist_ok=True)
                        self.save_json(path, default)
        except Exception as e:
            self.show_error(f"Error inicializando archivos: {e}")

    def load_all_data(self):
        """Carga todos los datos de configuración"""
        try:
            self.config_data = self.load_dict_config(CONFIG_FILE)
            self.params = self.load_list_config(PARAMS_FILE)
            self.history = self.load_json(HISTORY_FILE, [])
            self.bookmarks = self.load_json(BOOKMARKS_FILE, {})
            self.mpv_path = self.config_data.get("mpv_path", "")
        except Exception as e:
            self.show_error(f"Error cargando configuración: {e}")

    def load_language(self):
        """Carga el idioma desde language.conf o usa inglés por defecto."""
        try:
            if LANGUAGE_FILE.exists():
                with LANGUAGE_FILE.open("r", encoding="utf-8") as f:
                    lang = f.read().strip()
                    if lang in LANGUAGES:
                        return lang
            return "en"
        except Exception:
            return "en"

    def save_language(self, lang):
        """Guarda el idioma en language.conf, reseteando el archivo."""
        try:
            with LANGUAGE_FILE.open("w", encoding="utf-8") as f:
                f.write(lang)
        except Exception:
            pass

    # endregion

    # region Métodos de carga/guardado
    @staticmethod
    def load_dict_config(file_path: Path) -> Dict[str, str]:
        """Carga un archivo de configuración como diccionario"""
        config = {}
        try:
            if file_path.exists():
                with file_path.open("r", encoding="utf-8") as file:
                    for line in file:
                        line = line.strip()
                        if line and "=" in line:
                            key, value = line.split("=", 1)
                            config[key.strip()] = value.strip()
        except Exception as e:
            messagebox.showerror("Error", f"Error loading {file_path}: {e}")
        return config

    @staticmethod
    def load_list_config(file_path: Path) -> List[str]:
        """Carga un archivo de configuración como lista"""
        params = []
        try:
            if file_path.exists():
                with file_path.open("r", encoding="utf-8") as file:
                    params = [line.strip() for line in file if line.strip()]
        except Exception as e:
            messagebox.showerror("Error", f"Error loading {file_path}: {e}")
        return params

    def load_json(self, file_path: Path, default: Union[list, dict]) -> Union[list, dict]:
        """Carga datos desde un archivo JSON con verificación de integridad"""
        try:
            if not file_path.exists():
                return default

            with file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            # Verificación de tipo y estructura
            if not isinstance(data, type(default)):
                raise ValueError(f"Tipo incorrecto en {file_path.name}")

            # Validación específica para bookmarks
            if file_path == BOOKMARKS_FILE:
                if not all(isinstance(k, str) and isinstance(v, str) for k, v in data.items()):
                    # Intentar reparar automáticamente
                    repaired_data = {}
                    for k, v in data.items():
                        repaired_data[str(k)] = str(v)
                    self.save_json(file_path, repaired_data)
                    return repaired_data

            return data

        except (json.JSONDecodeError, ValueError) as e:
            self.show_error(f"Archivo {file_path.name} corrupto. Reseteando a valores por defecto.")
            self.save_json(file_path, default)
            return default
        except Exception as e:
            self.show_error(f"Error cargando {file_path.name}: {e}")
            return default

    def save_json(self, file_path: Path, data: Union[list, dict]):
        """Guarda datos en JSON con formato consistente y manejo seguro"""
        try:
            # Crear directorio si no existe
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Guardado temporal
            temp_path = file_path.with_suffix(".tmp")
            with temp_path.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False, sort_keys=True)
            
            # Reemplazar archivo original
            if file_path.exists():
                backup = file_path.with_suffix(".bak")
                file_path.replace(backup)
            temp_path.replace(file_path)
            
        except Exception as e:
            self.show_error(f"Error guardando {file_path.name}: {e}")
            if temp_path.exists():
                temp_path.unlink()
    
    def save_config(self, file_path: Path, data: Union[dict, list]):
        """Guarda la configuración en un archivo, ya sea como diccionario o lista"""
        try:
            # Crear directorio si no existe
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Guardado temporal
            temp_path = file_path.with_suffix(".tmp")
            
            if isinstance(data, dict):
                with temp_path.open("w", encoding="utf-8") as f:
                    for key, value in data.items():
                        f.write(f"{key}={value}\n")
            elif isinstance(data, list):
                with temp_path.open("w", encoding="utf-8") as f:
                    for item in data:
                        f.write(f"{item}\n")
            else:
                raise ValueError("Data must be a dictionary or a list")
            
            # Reemplazar archivo original
            if file_path.exists():
                backup = file_path.with_suffix(".bak")
                file_path.replace(backup)
            temp_path.replace(file_path)
            
        except Exception as e:
            self.show_error(f"Error guardando {file_path.name}: {e}")
            if temp_path.exists():
                temp_path.unlink()

    # endregion

    # region Interfaz gráfica
    def create_widgets(self):
        """Crea los elementos de la interfaz gráfica usando traducciones."""
        self.grid_columnconfigure(1, weight=1)

        tk.Button(self, text=get_translation("select_mpv", self.language), command=self.select_mpv_exe).grid(
            row=0, column=0, columnspan=2, pady=5, sticky="ew"
        )
        self.mpv_label = tk.Label(
            self,
            text=f"{get_translation('mpv', self.language)} {self.mpv_path}" if self.mpv_path else get_translation("mpv_not_selected", self.language),
            fg="blue", wraplength=500
        )
        self.mpv_label.grid(row=1, column=0, columnspan=2, pady=5, sticky="w")

        tk.Label(self, text=get_translation("media_link", self.language)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.link_entry = tk.Entry(self, width=60)
        self.link_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        tk.Label(self, text=get_translation("params", self.language)).grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.params_entry = tk.Entry(self, width=60)
        self.params_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        tk.Label(self, text=get_translation("bookmark_title", self.language)).grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.bookmark_title_entry = tk.Entry(self, width=30)
        self.bookmark_title_entry.grid(row=4, column=1, padx=(10,0), pady=5, sticky="w")
        tk.Button(self, text=get_translation("save_bookmark", self.language), command=self.save_bookmark).grid(
            row=4, column=1, padx=(200, 80), pady=5, sticky="w"
        )

        tk.Button(self, text=get_translation("launch_mpv", self.language), command=self.launch_mpv, bg="#4CAF50", fg="white").grid(
            row=5, column=0, columnspan=2, pady=10, sticky="ew"
        )

        tk.Label(self, text=get_translation("saved_params", self.language)).grid(row=7, column=0, padx=10, pady=5, sticky="ne")
        self.param_frame = tk.Frame(self)
        self.param_frame.grid(row=7, column=1, padx=10, pady=5, sticky="nsew")

    def setup_menu(self):
        """Configura los menús desplegables, incluyendo el de idioma."""
        menu_bar = tk.Menu(self)

        # Menú Historial
        self.history_menu = tk.Menu(menu_bar, tearoff=0)
        self.refresh_history_menu()

        # Menú Bookmarks
        self.bookmarks_menu = tk.Menu(menu_bar, tearoff=0)
        self.refresh_bookmarks_menu()

        menu_bar.add_cascade(label=get_translation("history", self.language), menu=self.history_menu)
        menu_bar.add_cascade(label=get_translation("bookmarks", self.language), menu=self.bookmarks_menu)

        # Menú Acerca de
        about_menu = tk.Menu(menu_bar, tearoff=0)
        about_menu.add_command(label=get_translation("about", self.language), command=self.show_about_window)
        menu_bar.add_cascade(label=get_translation("about", self.language), menu=about_menu)

        # Menú Idioma
        language_menu = tk.Menu(menu_bar, tearoff=0)
        for code, name in LANGUAGES.items():
            language_menu.add_command(
                label=name,
                command=lambda c=code: self.change_language(c)
            )
        menu_bar.add_cascade(label=get_translation("language", self.language), menu=language_menu)

        self.config(menu=menu_bar)

    def change_language(self, lang):
        """Cambia el idioma de la interfaz, lo guarda y reinicia la aplicación."""
        if lang not in LANGUAGES:
            lang = "en"
        self.language = lang
        self.save_language(lang)
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def update_all_texts(self):
        """Actualiza todos los textos de la interfaz según el idioma."""
        try:
            self.title(get_translation("title", self.language))
            self.mpv_label.config(
                text=f"{get_translation('mpv', self.language)} {self.mpv_path}" if self.mpv_path else get_translation("mpv_not_selected", self.language)
            )
            # Actualiza los labels y botones principales
            for widget in self.grid_slaves():
                if isinstance(widget, tk.Label):
                    text = widget.cget("text")
                    # Busca la clave de traducción correspondiente
                    for key in TRANSLATIONS:
                        if text == TRANSLATIONS[key].get("en") or text == TRANSLATIONS[key].get(self.language):
                            widget.config(text=get_translation(key, self.language))
                if isinstance(widget, tk.Button):
                    text = widget.cget("text")
                    for key in TRANSLATIONS:
                        if text == TRANSLATIONS[key].get("en") or text == TRANSLATIONS[key].get(self.language):
                            widget.config(text=get_translation(key, self.language))
            # Actualiza los labels y botones en about window si está abierta
            # (Opcional: puedes guardar la referencia y actualizarla)
        except Exception:
            pass

    def refresh_history_menu(self):
        """Actualiza el menú de historial"""
        self.refresh_menu(self.history_menu, self.history, self.select_history_link)

    def refresh_bookmarks_menu(self):
        """Actualiza el menú de marcadores"""
        try:
            self.bookmarks = self.load_json(BOOKMARKS_FILE, {})
            self.refresh_menu(self.bookmarks_menu, self.bookmarks, self.select_bookmark)
        except Exception as e:
            self.show_error(f"Error actualizando marcadores: {e}")

    def refresh_menu(self, menu: tk.Menu, items: Union[list, dict], command):
        """Actualiza un menú desplegable"""
        menu.delete(0, tk.END)
        try:
            if isinstance(items, dict):
                for title, link in items.items():
                    menu.add_command(
                        label=f"{title[:40]}...{title[-10:]}" if len(title) > 50 else title,
                        command=lambda t=title: command(t)
                    )
            else:
                for item in items:
                    menu.add_command(
                        label=item[:60] + "..." if len(item) > 60 else item,
                        command=lambda l=item: command(l)
                    )
        except Exception as e:
            self.show_error(f"Error actualizando menú: {e}")

    # endregion

    # region Funcionalidad principal
    def select_mpv_exe(self):
        """Selecciona el ejecutable de MPV"""
        try:
            new_path = filedialog.askopenfilename(
                title="Seleccionar MPV",
                filetypes=[("Ejecutables", "*.exe"), ("Todos los archivos", "*.*")]
            )
            if new_path:
                self.mpv_path = new_path
                self.config_data["mpv_path"] = self.mpv_path
                self.save_config(CONFIG_FILE, self.config_data)
                self.mpv_label.config(text=f"MPV: {self.mpv_path}")
        except Exception as e:
            self.show_error(f"Error seleccionando MPV: {e}")

    def save_dict_config(self):
        """Guarda la configuración actual"""
        try:
            with CONFIG_FILE.open("w", encoding="utf-8") as f:
                for key, value in self.config_data.items():
                    f.write(f"{key}={value}\n")
        except Exception as e:
            self.show_error(f"Error guardando configuración: {e}")

    def save_bookmark(self):
        """Guarda un marcador con validación mejorada"""
        try:
            link = self.link_entry.get().strip()
            title = self.bookmark_title_entry.get().strip()

            # Validaciones
            error = None
            if not link:
                error = "El enlace no puede estar vacío"
            elif not title:
                error = "El título no puede estar vacío"
            elif len(title) > 100:
                error = "Título demasiado largo (máx. 100 caracteres)"
            elif any(c in title for c in '/\\:*?"<>|'):
                error = "Caracteres inválidos en el título"
                
            if error:
                messagebox.showerror("Error", error)
                return

            # Confirmar sobrescritura
            if title in self.bookmarks:
                if not messagebox.askyesno(
                    "Confirmar",
                    f"'{title}' ya existe. ¿Sobrescribir?",
                    icon="warning"
                ):
                    return

            # Actualizar y guardar
            self.bookmarks[title] = link
            self.save_json(BOOKMARKS_FILE, self.bookmarks)
            self.refresh_bookmarks_menu()
            self.bookmark_title_entry.delete(0, tk.END)
            messagebox.showinfo("Éxito", "Marcador guardado correctamente")
            
        except Exception as e:
            self.show_error(f"Error guardando marcador: {e}")

    def select_history_link(self, link: str):
        """Selecciona un enlace del historial"""
        try:
            self.link_entry.delete(0, tk.END)
            self.link_entry.insert(0, link)
        except Exception as e:
            self.show_error(f"Error seleccionando historial: {e}")

    def select_bookmark(self, title: str):
        """Selecciona un marcador"""
        try:
            current_bookmarks = self.load_json(BOOKMARKS_FILE, {})
            if title not in current_bookmarks:
                self.bookmarks = current_bookmarks
                self.refresh_bookmarks_menu()
                raise ValueError(f"El marcador '{title}' no existe")
                
            self.link_entry.delete(0, tk.END)
            self.link_entry.insert(0, current_bookmarks[title])
            
        except Exception as e:
            self.show_error(str(e))

    def refresh_param_checkboxes(self):
        """Actualiza las casillas de parámetros en columnas"""
        try:
            for widget in self.param_frame.winfo_children():
                widget.destroy()

            num_params = len(self.params)
            num_columns = 3
            num_rows = (num_params + num_columns - 1) // num_columns

            for i, param in enumerate(self.params):
                var = tk.BooleanVar()
                self.param_vars[param] = var
                row = i % num_rows
                column = i // num_rows
                tk.Checkbutton(
                    self.param_frame,
                    text=param,
                    variable=var,
                    command=self.update_params_entry
                ).grid(row=row, column=column, sticky="w")

        except Exception as e:
            self.show_error(f"Error actualizando parámetros: {e}")

    def update_params_entry(self):
        """Actualiza la entrada de parámetros"""
        try:
            seleccionados = [f"--{param}" for param, var in self.param_vars.items() if var.get()]
            self.params_entry.delete(0, tk.END)
            self.params_entry.insert(0, " ".join(seleccionados))
        except Exception as e:
            self.show_error(f"Error actualizando parámetros: {e}")
    
    def is_valid_url(self, url):
        """Valida si una URL es válida"""
        try:
            result = urllib.parse.urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False

    def launch_mpv(self):
        """Inicia MPV con validación reforzada"""
        try:
            # Validaciones
            if not Path(self.mpv_path).exists():
                raise FileNotFoundError("Ruta de MPV inválida")
                
            link = self.link_entry.get().strip()
            if not link:
                raise ValueError("Ingrese un enlace multimedia")
            
            if not self.is_valid_url(link) and not Path(link).exists():
                raise ValueError("Enlace multimedia inválido")
                
            # Agregar al historial
            if link not in self.history:
                self.history.insert(0, link)
                self.history = self.history[:100]
                self.save_json(HISTORY_FILE, self.history)
                self.refresh_history_menu()

            # Construir comando
            command = [self.mpv_path, link]
            if params := self.params_entry.get().strip():
                command.extend(params.split())
                
            # Ejecutar en segundo plano
            def run_mpv():
                try:
                    subprocess.Popen(
                        command,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        stdin=subprocess.DEVNULL,
                        start_new_session=True
                    )
                except Exception as e:
                    self.show_error(f"Error al ejecutar MPV: {e}")

            threading.Thread(target=run_mpv).start()
            
        except Exception as e:
            self.show_error(f"Error iniciando MPV: {e}")

    def show_about_window(self):
        """Muestra la ventana Acerca de con traducción."""
        about = tk.Toplevel(self)
        about.title(get_translation("about", self.language))
        about.geometry("1000x800")
        about.resizable(False, False)

        tk.Label(
            about,
            text=get_translation("title", self.language),
            font=("Arial", 15, "bold")
        ).pack(pady=(15, 5))

        tk.Label(
            about,
            text=get_translation("about_text", self.language),
            font=("Arial", 10),
            justify="left",
            wraplength=570
        ).pack(pady=(5, 10))

        tk.Label(
            about,
            text=get_translation("about_author", self.language),
            font=("Arial", 12, "bold")
        ).pack(pady=(5, 5))

        tk.Label(about, text=get_translation("about_github", self.language), font=("Arial", 10)).pack(pady=(10, 0))
        tk.Button(
            about, text="github.com/KAPINTOM",
            command=lambda: webbrowser.open("https://github.com/KAPINTOM"),
            fg="blue", cursor="hand2"
        ).pack(pady=2)

        tk.Label(about, text=get_translation("about_repo", self.language), font=("Arial", 10)).pack(pady=(15, 0))
        tk.Button(
            about, text="github.com/mpv-player/mpv",
            command=lambda: webbrowser.open("https://github.com/mpv-player/mpv"),
            fg="blue", cursor="hand2"
        ).pack(pady=2)

        tk.Label(about, text=get_translation("about_download", self.language), font=("Arial", 10)).pack(pady=(15, 0))
        tk.Button(
            about, text="mpv-winbuild releases",
            command=lambda: webbrowser.open("https://github.com/zhongfly/mpv-winbuild/releases"),
            fg="blue", cursor="hand2"
        ).pack(pady=2)

        tk.Label(about, text=get_translation("about_year", self.language), font=("Arial", 10, "italic")).pack(pady=(20, 0))

        tk.Button(about, text=get_translation("close", self.language), command=about.destroy).pack(pady=(15, 10))

    # endregion

    # region Utilidades
    def show_error(self, message: str):
        """Muestra un mensaje de error detallado"""
        error_msg = f"{message}\n\nTraceback:\n{traceback.format_exc()}"
        messagebox.showerror("Error", error_msg)

    def on_close(self):
        """Maneja el cierre seguro de la aplicación"""
        try:
            self.save_json(HISTORY_FILE, self.history)
            self.save_json(BOOKMARKS_FILE, self.bookmarks)
            self.destroy()
        except Exception as e:
            self.show_error(f"Error al cerrar: {e}")
    # endregion

if __name__ == "__main__":
    try:
        import sys, os
        if getattr(sys, 'frozen', False):
            BASE_DIR = sys._MEIPASS
        else:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            
        app = Application()
        app.mainloop()
    except Exception as e:
        messagebox.showerror("Error crítico", f"Error inicial: {str(e)}\n{traceback.format_exc()}")