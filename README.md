# MPV Starter

<img src="https://github.com/KAPINTOM/MPV-Starter/blob/main/Images/mpv%20starter.png" alt="GUI" width="500">

---
## 🇬🇧 MPV Graphical Launcher (web links & local files)

**MPV Starter** is a graphical application that lets you launch the [MPV](https://mpv.io/) player easily **with web links and local files** (YouTube, Twitch, Vimeo, MP4/MKV/AVI files, etc.), manage custom parameters, history, and bookmarks, all from an intuitive and multilingual interface.

> ✅ **New:** Now with **local file support**!  
> Play both web links and locally stored videos.

---

### Main Features
- **Flexible playback:** Supports web links (YouTube, Twitch, etc.) **and local files** (MP4, MKV, AVI).
- **MPV executable selection:** Easily specify the path to MPV.
- **Automatic MPV installer:** Download and run MPV directly from the app if you don't have it yet.
- **Modern UI installer:** Install the modern graphical interface (OSC Modern) for MPV with one click.
- **Custom parameters:** Add and save launch parameters for MPV.
- **Smart history:** Automatically saves last 100 played items (accessible via menu).
- **Bookmark management:** Store web links and local files with custom titles.
- **Multilingual:** Supports English, Spanish, Japanese, Chinese, Korean, Portuguese, French, Italian, Russian, and German.
- **Input validation:** Checks links and file paths before playback.
- **Quick access:** One-click access to bookmarks, history, and settings.
- **Portable setup:** All data stored alongside the executable.
---

### **MPV config file example: `mpv.conf`:**

```ini
vo=gpu-next

#gpu-api=vulkan  # Vulkan for better performance (optional)

hwdec=no

#profile=gpu-hq  # High-quality settings
profile=high-quality

scale=ewa_lanczos4sharpest
cscale=ewa_lanczos4sharpest
dscale=ewa_lanczos4sharpest
tscale=ewa_lanczos4sharpest

correct-downscaling=yes

save-position-on-quit
fs

deband=yes

saturation=50
gamma=30

no-border
```

### **Most used params template: `params.conf`:**
 When using the tool, ensure that you do not select options beginning with '#'. Additionally, note that selecting multiple options with overlapping functionality may cause unexpected behavior in MPV.
 
 **Note:** This behavior will be fixed in future updates

```ini
# Only select one of each category, if nothing is selected MPV will use the default one

# Video Output
vo=gpu
vo=gpu-next

# Hardware decoders
hwdec=no
hwdec=auto
hwdec=auto-safe
hwdec=auto-copy

# GPU API
gpu-api=vulkan

# Profiles
profile=gpu-hq
profile=fast
profile=high-quality

# Speed
speed=0.5
speed=2

# Simple interpolation, activate both
video-sync=display-resample
interpolation=yes

# Individual options
deband=yes
save-position-on-quit
no-border
fs
mute
cache=yes
cache=auto
loop=yes
```

### **Check multiple simple MPV config files on my GitHub repository**: 

 🛠️👉 [KAPINTOM/mpv-player-personal-configs](https://github.com/KAPINTOM/mpv-player-personal-configs)

### **For more detailed information on configuring the MPV configuration file, please refer to the official MPV documentation**

 📖👉 [Reference Manual Main Page](https://mpv.io/manual) → [Stable Version Manual](https://mpv.io/manual/stable/)

---

### **Credits**

Developed by Kenneth Andrey Pinto Medina using vibe coding technique


GitHub: [KAPINTOM](https://github.com/KAPINTOM)  

**MPV Automated Installers Based On:**  
Repository: [zhongfly/mpv-winbuild](https://github.com/zhongfly/mpv-winbuild/releases)  
Thanks to [zhongfly](https://github.com/zhongfly) for providing builds and update scripts for MPV on Windows.  