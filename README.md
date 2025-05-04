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

## 📝 Examples

### Convert specific time:
```bash
# Using abbreviations
python main.py convert "14:30:00" PST EST
```

```bash
# Using full timezone names
python main.py convert "2023-10-15 09:00:00" Asia/Tokyo Europe/London
```
```bash
# Convert current time
python main.py convert now UTC IST
```

### Show current time in all zones:
```bash
python main.py current
```

### List all timezones:
```bash
python main.py list
```

### List common abbreviations:
```bash
python main.py common
```

## 🌐 Available Time Zones

The tool supports all standard IANA time zones, including:

### Common abbreviations:
- **PST** (Pacific Standard Time) → America/Los_Angeles
- **MST** (Mountain Standard Time) → America/Denver
- **CST** (Central Standard Time) → America/Chicago
- **EST** (Eastern Standard Time) → America/New_York
- **UTC** (Coordinated Universal Time) → UTC
- **GMT** (Greenwich Mean Time) → Europe/London
- **CET** (Central European Time) → Europe/Paris
- **IST** (India Standard Time) → Asia/Kolkata
- **JST** (Japan Standard Time) → Asia/Tokyo
- **AEST** (Australian Eastern Standard Time) → Australia/Sydney

Use the `list` command to see all available time zones.

## 💡 Tips

- Use 'now' to convert current time instantly
- Timezone abbreviations are case-insensitive (PST = pst)
- The tool automatically handles daylight saving time changes
- Cache is updated every 24 hours for better performance
- Use full timezone names for more accurate conversions
- You can mix abbreviations and full names in conversions

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
