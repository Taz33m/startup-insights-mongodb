"""
Utility functions for data processing and analysis.
"""
import json
import pandas as pd
from typing import List, Dict, Any


def load_json_file(filepath: str) -> List[Dict[str, Any]]:
    """Load data from JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def save_json_file(data: List[Dict[str, Any]], filepath: str):
    """Save data to JSON file."""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)


def calculate_funding_stats(startups: List[Dict[str, Any]]) -> Dict[str, float]:
    """Calculate funding statistics."""
    fundings = [s.get('total_funding_usd', 0) for s in startups]
    return {
        'total': sum(fundings),
        'average': sum(fundings) / len(fundings) if fundings else 0,
        'max': max(fundings) if fundings else 0,
        'min': min(fundings) if fundings else 0
    }


def format_currency(amount: float) -> str:
    """Format number as currency."""
    if amount >= 1_000_000_000:
        return f"${amount/1_000_000_000:.2f}B"
    elif amount >= 1_000_000:
        return f"${amount/1_000_000:.2f}M"
    elif amount >= 1_000:
        return f"${amount/1_000:.2f}K"
    else:
        return f"${amount:.2f}"
