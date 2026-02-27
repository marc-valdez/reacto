"""
Export Module

Functions for exporting reaction time results.
"""

import json

def export_results(results):
    """Export results to JSON file."""
    # Group results by game and color
    grouped = {}
    for clip_name, data in results.items():
        parts = clip_name.split('_')
        if len(parts) >= 3:
            game = parts[2]
            color = parts[1]
            if game not in grouped:
                grouped[game] = {}
            if color not in grouped[game]:
                grouped[game][color] = {}
            grouped[game][color][clip_name] = data

    # Ensure all games and colors are present
    games = ['rivals', 'valorant']
    colors = ['default', 'deuteranopia', 'protanopia', 'tritanopia']
    for game in games:
        if game not in grouped:
            grouped[game] = {}
        for color in colors:
            if color not in grouped[game]:
                grouped[game][color] = {}

    # Sort within each color
    def get_sort_key(clip_name):
        parts = clip_name.split('_')
        if len(parts) >= 3:
            stimulus = int(parts[0])
            return stimulus
        return 0

    for game in grouped:
        for color in grouped[game]:
            sorted_clips = sorted(grouped[game][color].keys(), key=get_sort_key)
            grouped[game][color] = {clip: grouped[game][color][clip] for clip in sorted_clips}

    # Write to JSON
    json_path = 'results.json'
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []
    data.append(grouped)
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)
