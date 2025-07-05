import re
import pandas as pd


def load_csv(file_path: str) -> pd.DataFrame:
    """Load a CSV file into a pandas DataFrame."""
    return pd.read_csv(file_path)


def extract_section(text: str, title: str) -> str:
    """Extract a section by its title from the LLM response."""
    pattern = rf"{re.escape(title)}\s*:?\s*(.+?)(?=\n\w|$)"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else ""
