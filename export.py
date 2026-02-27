"""
Export Module

Functions for exporting reaction time results.
"""

import json

def export_results(results):
    """Export results to JSON file."""
    # Write to JSON
    with open("results.json", "w") as json_file:
        json.dump(results, json_file, indent=4)
        print("Results exported to 'results.json'")
