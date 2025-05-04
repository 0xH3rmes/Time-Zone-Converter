#!/usr/bin/env python3

import argparse
import json
import datetime
import urllib.request
import os
from datetime import datetime

# Common time zones
COMMON_TIMEZONES = {
    'PST': 'America/Los_Angeles',
    'MST': 'America/Denver',
    'CST': 'America/Chicago',
    'EST': 'America/New_York',
    'UTC': 'UTC',
    'GMT': 'Europe/London',
    'CET': 'Europe/Paris',
    'IST': 'Asia/Kolkata',
    'JST': 'Asia/Tokyo',
    'AEST': 'Australia/Sydney',
    'SGT': 'Asia/Singapore',
    'HKT': 'Asia/Hong_Kong',
    'KST': 'Asia/Seoul',
    'PKT': 'Asia/Karachi',
    'AST': 'Asia/Tehran'
}

# Cache file for time zone data
CACHE_FILE = os.path.expanduser("~/.timezone_cache.json")
CACHE_EXPIRY = 86400  # 24 hours

def get_worldtime_api_data(timezone):
    """Get current time for a timezone from WorldTime API"""
    try:
        url = f"http://worldtimeapi.org/api/timezone/{timezone}"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            return data
    except Exception as e:
        print(f"Error fetching timezone data: {e}")
        return None

def get_timezones_from_api():
    """Get list of available timezones from API"""
    try:
        url = "http://worldtimeapi.org/api/timezone"
        with urllib.request.urlopen(url) as response:
            timezones = json.loads(response.read().decode())
            return timezones
    except Exception as e:
        print(f"Error fetching timezone list: {e}")
        return []

def load_cache():
    """Load cached timezone data"""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as f:
                cache = json.load(f)
                # Check if cache is expired
                if datetime.now().timestamp() - cache.get('timestamp', 0) < CACHE_EXPIRY:
                    return cache
        except:
            pass
    return None

def save_cache(data):
    """Save timezone data to cache"""
    try:
        cache = {
            'timestamp': datetime.now().timestamp(),
            'data': data
        }
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache, f)
    except:
        pass

def get_offset_from_utc(timezone):
    """Get UTC offset for a timezone"""
    data = get_worldtime_api_data(timezone)
    if data:
        return data.get('utc_offset', '+00:00')
    return '+00:00'

def convert_time(time_str, from_tz, to_tz):
    """Convert time from one timezone to another"""
    # Parse input time
    try:
        if time_str == "now":
            # Get current time in from_tz
            from_data = get_worldtime_api_data(from_tz)
            if from_data:
                datetime_str = from_data['datetime']
                current_time = datetime.fromisoformat(datetime_str)
            else:
                current_time = datetime.now()
        else:
            current_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        try:
            current_time = datetime.strptime(time_str, "%H:%M:%S")
            current_time = current_time.replace(year=datetime.now().year, 
                                              month=datetime.now().month, 
                                              day=datetime.now().day)
        except ValueError:
            print(f"Invalid time format. Use 'HH:MM:SS' or 'YYYY-MM-DD HH:MM:SS' or 'now'")
            return None
    
    # Get offset differences
    from_offset = get_offset_from_utc(from_tz)
    to_offset = get_offset_from_utc(to_tz)
    
    # Parse offsets
    from_hours = int(from_offset[1:3])
    from_minutes = int(from_offset[4:6])
    from_sign = 1 if from_offset[0] == '+' else -1
    
    to_hours = int(to_offset[1:3])
    to_minutes = int(to_offset[4:6])
    to_sign = 1 if to_offset[0] == '+' else -1
    
    # Calculate total minutes difference
    from_total_minutes = from_sign * (from_hours * 60 + from_minutes)
    to_total_minutes = to_sign * (to_hours * 60 + to_minutes)
    diff_minutes = to_total_minutes - from_total_minutes
    
    # Convert time
    result_time = current_time + datetime.timedelta(minutes=diff_minutes)
    
    return {
        'from_time': current_time.strftime("%Y-%m-%d %H:%M:%S"),
        'from_tz': from_tz,
        'to_time': result_time.strftime("%Y-%m-%d %H:%M:%S"),
        'to_tz': to_tz,
        'diff': f"{diff_minutes:+d} minutes"
    }

def display_current_time_all_zones():
    """Display current time in all common time zones"""
    print("\nCurrent time in different time zones:")
    print("=" * 60)
    
    for abbr, zone in COMMON_TIMEZONES.items():
        data = get_worldtime_api_data(zone)
        if data:
            dt = datetime.fromisoformat(data['datetime'])
            formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{abbr:<5} ({zone:<30}) {formatted_time}")
    
    print("=" * 60)

def list_all_timezones():
    """List all available timezones"""
    cache = load_cache()
    if cache and 'timezones' in cache.get('data', {}):
        timezones = cache['data']['timezones']
    else:
        timezones = get_timezones_from_api()
        if timezones:
            save_cache({'timezones': timezones})
    
    if timezones:
        print(f"\nAvailable Time Zones ({len(timezones)} total):")
        print("=" * 50)
        
        # Group by continent
        by_continent = {}
        for tz in timezones:
            if '/' in tz:
                continent = tz.split('/')[0]
                if continent not in by_continent:
                    by_continent[continent] = []
                by_continent[continent].append(tz)
        
        for continent in sorted(by_continent.keys()):
            print(f"\n{continent}:")
            for tz in sorted(by_continent[continent]):
                print(f"  {tz}")
    else:
        print("Could not fetch timezone list")

def resolve_timezone(tz_input):
    """Resolve timezone abbreviation to full timezone"""
    if tz_input.upper() in COMMON_TIMEZONES:
        return COMMON_TIMEZONES[tz_input.upper()]
    
    # Check if it's already a valid timezone
    if tz_input in get_timezones_from_api():
        return tz_input
    
    # Try to find a match
    all_timezones = get_timezones_from_api()
    for tz in all_timezones:
        if tz_input.lower() in tz.lower():
            return tz
    
    return None

def main():
    parser = argparse.ArgumentParser(description="Time Zone Converter")
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Convert command
    convert_parser = subparsers.add_parser("convert", help="Convert time between timezones")
    convert_parser.add_argument("time", help="Time to convert (HH:MM:SS, YYYY-MM-DD HH:MM:SS, or 'now')")
    convert_parser.add_argument("from_tz", help="Source timezone (e.g., PST, UTC, Asia/Tokyo)")
    convert_parser.add_argument("to_tz", help="Target timezone (e.g., EST, GMT, Europe/London)")
    
    # Current time command
    current_parser = subparsers.add_parser("current", help="Show current time in different zones")
    
    # List timezones command
    list_parser = subparsers.add_parser("list", help="List all available timezones")
    
    # List common timezones command
    common_parser = subparsers.add_parser("common", help="List common timezone abbreviations")
    
    args = parser.parse_args()
    
    if args.command == "convert":
        from_tz = resolve_timezone(args.from_tz)
        to_tz = resolve_timezone(args.to_tz)
        
        if not from_tz:
            print(f"Invalid source timezone: {args.from_tz}")
            return
        
        if not to_tz:
            print(f"Invalid target timezone: {args.to_tz}")
            return
        
        result = convert_time(args.time, from_tz, to_tz)
        if result:
            print(f"\nTime Conversion:")
            print(f"From: {result['from_time']} ({result['from_tz']})")
            print(f"To:   {result['to_time']} ({result['to_tz']})")
            print(f"Difference: {result['diff']}")
    
    elif args.command == "current":
        display_current_time_all_zones()
    
    elif args.command == "list":
        list_all_timezones()
    
    elif args.command == "common":
        print("\nCommon Time Zone Abbreviations:")
        print("=" * 50)
        for abbr, zone in sorted(COMMON_TIMEZONES.items()):
            print(f"{abbr:<5} -> {zone}")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
