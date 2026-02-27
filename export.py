"""
Export Module

Functions for exporting reaction time results to server and local JSON.
"""

import json
import requests
from config import config

SERVER_URL = config.get_string('server', 'url', 'http://localhost:5000')

def export_results(results, auth_code):
    """Submit results to server and save to local JSON."""
    # Group results by game and color_mode
    grouped = {}
    for clip_name, data in results.items():
        parts = clip_name.split('_')
        if len(parts) >= 3:
            game = parts[2]
            color_mode = parts[1]
            if game not in grouped:
                grouped[game] = {}
            if color_mode not in grouped[game]:
                grouped[game][color_mode] = {}
            grouped[game][color_mode][clip_name] = data

    # Ensure all games and color_modes are present
    games = ['rivals', 'valorant']
    color_modes = ['default', 'deuteranopia', 'protanopia', 'tritanopia']
    for game in games:
        if game not in grouped:
            grouped[game] = {}
        for color_mode in color_modes:
            if color_mode not in grouped[game]:
                grouped[game][color_mode] = {}

    # Sort within each color_mode
    def get_sort_key(clip_name):
        parts = clip_name.split('_')
        if len(parts) >= 3:
            stimulus = int(parts[0])
            return stimulus
        return 0

    for game in grouped:
        for color_mode in grouped[game]:
            sorted_clips = sorted(grouped[game][color_mode].keys(), key=get_sort_key)
            grouped[game][color_mode] = {clip: grouped[game][color_mode][clip] for clip in sorted_clips}

    # Save to local JSON
    json_path = f'results_{auth_code}.json'
    with open(json_path, 'w') as f:
        json.dump(grouped, f, indent=4)
    print(f"Results saved to {json_path}")

    # Try to submit to server
    try:
        response = requests.post(f"{SERVER_URL}/submit_results", json={'auth_code': auth_code, 'results': results}, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("Results submitted to server successfully.")
            else:
                print(f"Server submission failed: {data.get('message')}")
        else:
            print(f"Server error: {response.status_code}")
    except requests.RequestException as e:
        print(f"Server connection error: {e}. Results saved locally only.")
