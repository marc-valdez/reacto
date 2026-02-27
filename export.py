"""
Export Module

Functions for exporting reaction time results.
"""

import json
from supabase import Client

def export_results(results, test_duration, client: Client=None):
    """Export results to JSON file."""
    # Write to JSON
    with open("results.json", "w") as json_file:
        json.dump({
            "test_duration": test_duration,
            "results": results
        }, json_file, indent=4)
        print("Results exported to 'results.json'")

    try:
        if client is None:
            print("Supabase client not provided. Skipping upload to Supabase.")
            return
        client.rpc(
            "submit_experiment",
            {"payload": results}
        ).execute()
        print("Results submitted to Supabase successfully.")
    except Exception as e:
        print(f"Error submitting results to Supabase: {e}")
