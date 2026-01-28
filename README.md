# ARP - Aspect Ratio Tool

A simple and powerful tool for calculating aspect ratios and pixel dimensions for design, print, and social media.

## Features
- **Ratio Detection**: Automatically identifies the ratio (e.g., 16:9, 4:3, 21:9) from any resolution.
- **Aspect Ratio Presets**: Large list of common formats:
  - **Print**: A4, Letter, etc.
  - **Photo**: 4x6, 5x7, etc.
  - **Film**: 16:9, Cinema, Anamorphic.
  - **Social Media**: Instagram, TikTok/Reels, Banners.
- **DPI-based Calculation**: Define a DPI to automatically calculate pixel counts based on physical dimensions.
- **Orientation Toggle**: Instantly swap width and height with a single click (⇄).
- **Dark Mode UI**: Beautiful "Forest Dark" theme with rounded UI elements and smooth interactions.

## Installation

### Prerequisites
- Python 3
- GTK+ 3
- PyGObject

### Dependencies (Linux/Ubuntu)
```bash
sudo apt update
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0
```

### Running the App
```bash
python3 aspect_tool.py
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
