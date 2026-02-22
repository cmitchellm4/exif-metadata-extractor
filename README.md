# 🔬 EXIF Metadata Extractor

A digital forensics tool that uncovers hidden metadata embedded in image files — including GPS coordinates, device info, timestamps, and camera settings. Available as both a Python CLI tool and a browser-based web interface.

---

## What is EXIF Data?

When you take a photo on a phone or camera, the device secretly embeds information into the image file — this is called **EXIF data**. It can contain:

- 📍 **GPS coordinates** — the exact location where the photo was taken
- 📷 **Device info** — make, model, and software of the camera/phone
- 🕐 **Timestamps** — when the photo was taken, edited, and digitized
- ⚙️ **Camera settings** — ISO, aperture, shutter speed, focal length

This is a key technique used in **OSINT investigations** and **digital forensics**.

---

## Features

- Extracts GPS, device, datetime, and camera settings from JPEG images
- Converts GPS coordinates to decimal format with a direct Google Maps link
- Python CLI tool for terminal use
- Clean web interface (no install needed, drag & drop, fully local)
- Exports results to JSON

---

## Web Interface

Just open `index.html` in any browser — no installation required. Everything runs locally; no data is uploaded anywhere.

---

## Python CLI

### Install dependencies
```bash
pip install Pillow
```

### Run
```bash
python metadata_extractor.py image.jpg
```

Or run it interactively:
```bash
python metadata_extractor.py
```

### Example Output
```
[ GPS Location ]
  Latitude                 37.774929
  Longitude                -122.419418
  Google Maps              https://maps.google.com/?q=37.774929,-122.419418

[ Device / Camera ]
  Make                     Apple
  Model                    iPhone 14 Pro
  Software                 16.5

[ Date & Time ]
  DateTimeOriginal         2024:08:12 14:32:07

[ Image Settings ]
  ExifImageWidth           4032
  ExifImageHeight          3024
  ISOSpeedRatings          64
  FNumber                  1.78
  FocalLength              6 mm
```

---

## ⚠️ Disclaimer

This tool is for **educational and authorized use only**. Do not use it to violate anyone's privacy. Always obtain proper authorization before analyzing images that don't belong to you.

---

## Part of My OSINT Toolkit

This project is part of a growing set of OSINT/forensics tools:
- [Username Tracker](../osint-username-tracker) — Search for usernames across 15+ platforms
- **EXIF Metadata Extractor** ← you are here

---

## What I Learned

- How EXIF metadata is structured inside JPEG files (binary parsing)
- How GPS DMS (degrees/minutes/seconds) converts to decimal coordinates
- Python's `Pillow` library for image processing
- How forensic investigators use metadata to geolocate images

---

## Roadmap

- [ ] Support for more formats (PNG, HEIC, TIFF)
- [ ] Batch process multiple images at once
- [ ] Map view showing multiple geotagged images
- [ ] Strip metadata from images (privacy tool)

---

## License

MIT License
