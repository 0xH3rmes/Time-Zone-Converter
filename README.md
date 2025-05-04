# 🌍 Time Zone Converter

A simple command-line tool for converting time between different time zones.

## ✨ Features

- ⏰ Convert time between any two time zones
- 🌐 Show current time in all common time zones
- 📋 List all available time zones
- 🔄 Support for common timezone abbreviations
- 💾 Cache timezone data for faster access
- 🌎 Accurate UTC offset calculations

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/0xH3rmes/timezone-converter.git
cd timezone-converter
```

2. Make the script executable (Unix/Linux/macOS):
```bash
chmod +x main.py
```

## ⚙️ Commands

- `convert`: Convert time between timezones
- `current`: Show current time in different zones
- `list`: List all available timezones
- `common`: List common timezone abbreviations

## 📋 Command Options

### Convert time:
```bash
python main.py convert <time> <from_timezone> <to_timezone>
```

Time formats:

- `HH:MM:SS`: Time only (uses current date)
- `YYYY-MM-DD HH:MM:SS`: Full date and time
- `now`: Current time

### Show current time:
```bash
python main.py current
```

### List timezones:
```bash
python main.py list
```

### List common abbreviations:
```bash
python main.py common
```

