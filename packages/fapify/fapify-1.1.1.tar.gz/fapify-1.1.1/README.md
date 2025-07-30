````markdown
# Coomify

An async CLI to bulk-download photos & videos from [coomer.su](https://coomer.su). Cass × GPT made this.

---

## 🚀 Features

- **Async & concurrent** downloads (configurable batch size)  
- **Auto-pagination** through user galleries  
- **HTML scraping** for full-res images & video sources  
- **Real-time terminal status** (via `tabulate` + `colorama`)  
- **ffmpeg**-powered media saving  

---

## 📦 Install

```bash
pip install fapify
````

Make sure you have Python 3.8+ and `ffmpeg` on your PATH.

---

## 💡 Quickstart

```bash
fapify -u <USERNAME> [--photos] [--videos] [--batch N]
```

* `-u, --user`  **(required)** target username
* `-p, --photos` only photos
* `-v, --videos` only videos
* `-b, --batch` concurrent downloads (default: 5)

**Example:** download everything from `jane_doe` with batch 10

```bash
fapify -u jane_doe -b 10
```

---

## 📂 Output

```
./jane_doe/
├─ photos/
└─ videos/
```

Enjoy! 🚀