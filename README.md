# MPV Starter

[English below]

## 🇪🇸 Lanzador gráfico para MPV (solo enlaces web)

**MPV Starter** es una aplicación gráfica que te permite lanzar el reproductor [MPV](https://mpv.io/) fácilmente **solo con enlaces web** (YouTube, Twitch, Vimeo, etc.), gestionar parámetros personalizados, historial y marcadores, todo desde una interfaz intuitiva y multilenguaje.

> ⚠️ **Nota:** Actualmente, este software está diseñado **exclusivamente para reproducir enlaces web**.  
> **No admite archivos locales por ahora**, pero en el futuro se añadirá soporte para archivos locales y muchas más funciones.

---

### Características principales

- **Selección de ejecutable MPV:** Elige la ruta del ejecutable de MPV fácilmente.
- **Reproducción de enlaces web:** Ingresa enlaces de medios de internet para reproducirlos con MPV.
- **Parámetros personalizados:** Añade, selecciona y guarda parámetros de MPV para cada ejecución.
- **Gestión de historial:** Guarda automáticamente los últimos 100 enlaces web reproducidos, accesibles desde el menú.
- **Marcadores personalizados:** Guarda y administra marcadores con título y enlace web.
- **Soporte multilenguaje:** Interfaz disponible en Español, Inglés, Japonés, Chino, Coreano, Portugués, Francés, Italiano, Ruso y Alemán.
- **Validación de enlaces:** Verifica la validez de los enlaces web antes de lanzar MPV.
- **Acceso rápido:** Acceso directo a marcadores, historial y enlaces oficiales de MPV.
- **Configuración portable:** Todos los archivos de configuración y datos se guardan junto al ejecutable/script.

---

### Requisitos

- Python 3.8 o superior (solo para uso como script)
- Windows 7/10/11 (soporte principal)
- [MPV player](https://mpv.io/)

---

### Instalación y uso

#### Como script Python

1. Clona este repositorio o descarga el archivo `mpv_starter_main.py`.
2. Instala las dependencias estándar de Python (`tkinter` viene incluido en la mayoría de instalaciones).
3. Ejecuta:
   ```bash
   python mpv_starter_main.py
   ```

#### Como ejecutable

- Descarga el archivo `.exe` compilado (si está disponible) y colócalo en cualquier carpeta.
- Todos los archivos de configuración se crearán junto al `.exe`.

---

### Compilación (opcional)

Para crear un ejecutable con PyInstaller:

```bash
pyinstaller --onefile --noconsole mpv_starter_main.py
```

---

### Créditos

Desarrollado por Kenneth Andrey Pinto Medina  
GitHub: [KAPINTOM](https://github.com/KAPINTOM)

---

# 🇬🇧 MPV Graphical Launcher (web links only)

**MPV Starter** is a graphical application that lets you launch the [MPV](https://mpv.io/) player easily **with web links only** (YouTube, Twitch, Vimeo, etc.), manage custom parameters, history, and bookmarks, all from an intuitive and multilingual interface.

> ⚠️ **Note:** This software is currently designed **exclusively for playing web links**.  
> **Local file support is not available yet**, but it will be added in the future along with many more features.

---

### Main Features

- **MPV executable selection:** Easily choose the path to your MPV executable.
- **Play web links:** Enter internet media links to play them with MPV.
- **Custom parameters:** Add, select, and save MPV parameters for each run.
- **History management:** Automatically saves the last 100 played web links, accessible from the menu.
- **Custom bookmarks:** Save and manage bookmarks with title and web link.
- **Multilanguage support:** Interface available in English, Spanish, Japanese, Chinese, Korean, Portuguese, French, Italian, Russian, and German.
- **Link validation:** Checks the validity of web links before launching MPV.
- **Quick access:** Direct access to bookmarks, history, and official MPV links.
- **Portable configuration:** All configuration and data files are stored next to the executable/script.

---

### Requirements

- Python 3.8 or higher (for script usage)
- Windows 7/10/11 (main support)
- [MPV player](https://mpv.io/)

---

### Installation and Usage

#### As Python script

1. Clone this repository or download `mpv_starter_main.py`.
2. Install standard Python dependencies (`tkinter` is included in most installations).
3. Run:
   ```bash
   python mpv_starter_main.py
   ```

#### As executable

- Download the compiled `.exe` file (if available) and place it in any folder.
- All configuration files will be created next to the `.exe`.

---

### Compilation (optional)

To create an executable with PyInstaller:

```bash
pyinstaller --onefile --windowed mpv_starter_main.py
```

---

### Credits

Developed by Kenneth Andrey Pinto Medina  
GitHub: [KAPINTOM](https://github.com/KAPINTOM)
