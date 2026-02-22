"""
EXIF Metadata Extractor
-----------------------
Extracts hidden metadata from image files including GPS coordinates,
device info, timestamps, and more. A digital forensics tool.
"""

import sys
import os
import json
import datetime
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

# Terminal colors
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"


def get_exif_data(image_path: str) -> dict:
    """Extract raw EXIF data from an image file."""
    try:
        img = Image.open(image_path)
    except FileNotFoundError:
        print(f"{RED}Error: File not found: {image_path}{RESET}")
        return {}
    except Exception as e:
        print(f"{RED}Error opening image: {e}{RESET}")
        return {}

    exif_data = {}
    raw = img._getexif()

    if not raw:
        return {}

    for tag_id, value in raw.items():
        tag = TAGS.get(tag_id, tag_id)
        exif_data[tag] = value

    return exif_data


def convert_gps_coordinate(value, ref) -> float:
    """Convert GPS DMS (degrees/minutes/seconds) to decimal degrees."""
    degrees = float(value[0])
    minutes = float(value[1])
    seconds = float(value[2])
    decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
    if ref in ["S", "W"]:
        decimal = -decimal
    return round(decimal, 6)


def extract_gps(exif_data: dict) -> dict | None:
    """Pull GPS info from EXIF data and convert to decimal coords."""
    gps_info = exif_data.get("GPSInfo")
    if not gps_info:
        return None

    gps = {}
    for key, val in gps_info.items():
        gps[GPSTAGS.get(key, key)] = val

    lat = gps.get("GPSLatitude")
    lat_ref = gps.get("GPSLatitudeRef")
    lon = gps.get("GPSLongitude")
    lon_ref = gps.get("GPSLongitudeRef")
    alt = gps.get("GPSAltitude")

    result = {}

    if lat and lat_ref and lon and lon_ref:
        result["latitude"]  = convert_gps_coordinate(lat, lat_ref)
        result["longitude"] = convert_gps_coordinate(lon, lon_ref)
        result["maps_url"]  = f"https://maps.google.com/?q={result['latitude']},{result['longitude']}"

    if alt:
        result["altitude_meters"] = round(float(alt), 2)

    return result if result else None


def extract_metadata(image_path: str) -> dict:
    """Extract all relevant metadata from an image."""
    exif = get_exif_data(image_path)
    result = {
        "file": {
            "path":      os.path.abspath(image_path),
            "filename":  os.path.basename(image_path),
            "size_kb":   round(os.path.getsize(image_path) / 1024, 2),
        },
        "gps":    None,
        "device": {},
        "datetime": {},
        "image":  {},
        "other":  {},
    }

    if not exif:
        return result

    # GPS
    result["gps"] = extract_gps(exif)

    # Device / camera info
    device_tags = ["Make", "Model", "Software", "LensMake", "LensModel"]
    for tag in device_tags:
        if tag in exif:
            result["device"][tag] = str(exif[tag]).strip()

    # Date & time
    datetime_tags = ["DateTime", "DateTimeOriginal", "DateTimeDigitized"]
    for tag in datetime_tags:
        if tag in exif:
            result["datetime"][tag] = str(exif[tag])

    # Image settings
    image_tags = ["ExifImageWidth", "ExifImageHeight", "Orientation",
                  "Flash", "FocalLength", "ExposureTime", "FNumber",
                  "ISOSpeedRatings", "WhiteBalance", "ExposureMode"]
    for tag in image_tags:
        if tag in exif:
            val = exif[tag]
            try:
                result["image"][tag] = float(val) if hasattr(val, '__float__') else str(val)
            except Exception:
                result["image"][tag] = str(val)

    # Everything else
    skip = set(device_tags + datetime_tags + image_tags + ["GPSInfo", "MakerNote", "UserComment"])
    for tag, val in exif.items():
        if tag not in skip:
            try:
                result["other"][tag] = str(val)
            except Exception:
                pass

    return result


def print_section(title: str, data: dict):
    if not data:
        return
    print(f"\n{BOLD}{CYAN}[ {title} ]{RESET}")
    for key, val in data.items():
        print(f"  {DIM}{key:<25}{RESET} {val}")


def print_report(meta: dict):
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{CYAN}  EXIF METADATA REPORT{RESET}")
    print(f"{BOLD}{'='*60}{RESET}")

    # File info
    f = meta["file"]
    print(f"\n{BOLD}{CYAN}[ File Info ]{RESET}")
    print(f"  {'Filename':<25} {f['filename']}")
    print(f"  {'Path':<25} {f['path']}")
    print(f"  {'Size':<25} {f['size_kb']} KB")

    # GPS
    if meta["gps"]:
        gps = meta["gps"]
        print(f"\n{BOLD}{CYAN}[ GPS Location ]{RESET}")
        if "latitude" in gps:
            print(f"  {'Latitude':<25} {gps['latitude']}")
            print(f"  {'Longitude':<25} {gps['longitude']}")
            print(f"  {GREEN}{'Google Maps':<25} {gps['maps_url']}{RESET}")
        if "altitude_meters" in gps:
            print(f"  {'Altitude (m)':<25} {gps['altitude_meters']}")
    else:
        print(f"\n{BOLD}{CYAN}[ GPS Location ]{RESET}")
        print(f"  {YELLOW}No GPS data found.{RESET}")

    print_section("Device / Camera", meta["device"])
    print_section("Date & Time", meta["datetime"])
    print_section("Image Settings", meta["image"])

    if meta["other"]:
        print_section("Other Metadata", meta["other"])

    print(f"\n{BOLD}{'='*60}{RESET}\n")


def save_report(meta: dict):
    """Save metadata to a JSON report file."""
    ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{meta['file']['filename']}_metadata_{ts}.json"
    with open(filename, "w") as f:
        json.dump(meta, f, indent=2, default=str)
    print(f"{GREEN}Report saved to: {filename}{RESET}\n")


def main():
    print(f"{BOLD}{CYAN}")
    print("  ███████╗██╗  ██╗██╗███████╗")
    print("  ██╔════╝╚██╗██╔╝██║██╔════╝")
    print("  █████╗   ╚███╔╝ ██║█████╗  ")
    print("  ██╔══╝   ██╔██╗ ██║██╔══╝  ")
    print("  ███████╗██╔╝ ██╗██║██║     ")
    print("  ╚══════╝╚═╝  ╚═╝╚═╝╚═╝     ")
    print(f"  Metadata Extractor v1.0{RESET}\n")

    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = input(f"{BOLD}Enter path to image file:{RESET} ").strip()

    if not image_path:
        print(f"{RED}No file provided. Exiting.{RESET}")
        return

    print(f"\n{CYAN}Analyzing: {image_path}{RESET}")
    meta = extract_metadata(image_path)
    print_report(meta)

    save = input("Save report as JSON? (y/n): ").strip().lower()
    if save == "y":
        save_report(meta)


if __name__ == "__main__":
    main()
