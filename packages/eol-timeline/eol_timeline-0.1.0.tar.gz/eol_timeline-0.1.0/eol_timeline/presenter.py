"""
Module for formatting and displaying EOL timeline data.
"""
import csv
import json
import logging
from datetime import date, datetime
from typing import List, Optional, Dict, Any, TextIO
from rich.console import Console
from rich.table import Table
from rich.theme import Theme
from rich.style import Style

from .models import Release

logger = logging.getLogger(__name__)

# Define symbols and styles for urgency levels
URGENCY_LEVELS = {
    "critical": {"symbol": "‼", "days": 30, "style": "bold red"},
    "warning": {"symbol": "!", "days": 90, "style": "bold yellow"},
    "notice": {"symbol": "•", "days": 365, "style": "blue"},
    "info": {"symbol": "·", "style": "dim"}
}

# Define theme for rich
THEME = Theme({
    "critical": "bold red",
    "warning": "bold yellow",
    "notice": "blue",
    "info": "dim",
    "header": "bold",
})


class Presenter:
    """Class for displaying EOL timeline data in various formats."""
    
    def __init__(self, use_color: bool = True, style: str = "auto"):
        """
        Initialize presenter with display options.
        
        Args:
            use_color: Whether to use ANSI colors
            style: Display style ("auto", "plain", or "emoji")
        """
        self.console = Console(theme=THEME, highlight=False, color_system="auto" if use_color else None)
        self.style = style
    
    def determine_urgency(self, days_remaining: int) -> str:
        """
        Determine urgency level based on days remaining.
        
        Args:
            days_remaining: Number of days until EOL
            
        Returns:
            Urgency level string ("critical", "warning", "notice", or "info")
        """
        if days_remaining < URGENCY_LEVELS["critical"]["days"]:
            return "critical"
        elif days_remaining < URGENCY_LEVELS["warning"]["days"]:
            return "warning"
        elif days_remaining < URGENCY_LEVELS["notice"]["days"]:
            return "notice"
        else:
            return "info"
    
    def get_symbol(self, urgency: str) -> str:
        """Get the symbol for an urgency level."""
        if self.style == "plain":
            return ""
        elif self.style == "emoji":
            # Use emoji instead of text symbols
            if urgency == "critical":
                return "🚨"
            elif urgency == "warning":
                return "⚠️"
            elif urgency == "notice":
                return "ℹ️"
            else:
                return "✓"
        else:
            # Default to text symbols
            return URGENCY_LEVELS[urgency]["symbol"]
    
    def display_table(self, releases: List[Release], today: date, sort_by: str = "eol") -> None:
        """
        Display EOL timeline as a rich table.
        
        Args:
            releases: List of releases to display
            today: Reference date for calculating days remaining
            sort_by: Field to sort by ("eol", "product", or "version")
        """
        # Filter out releases without EOL dates
        valid_releases = [r for r in releases if r.eol_date and r.days_remaining is not None]
        
        # Sort the releases
        if sort_by == "eol":
            valid_releases.sort(key=lambda r: (r.eol_date or date.max, r.display_name))
        elif sort_by == "product":
            valid_releases.sort(key=lambda r: (r.display_name, r.eol_date or date.max))
        elif sort_by == "version":
            valid_releases.sort(key=lambda r: (r.display_name, r.name, r.eol_date or date.max))
        
        # Create the table
        table = Table(show_header=True, header_style="header")
        table.add_column(" ", justify="center", no_wrap=True, width=2)
        table.add_column("EOL Date", justify="left")
        table.add_column("Days", justify="right")
        table.add_column("Product", justify="left")
        table.add_column("Version", justify="left")
        table.add_column("Notes", justify="left")
        
        # Add rows to the table
        for release in valid_releases:
            days = release.days_remaining
            if days is None:
                continue
                
            urgency = self.determine_urgency(days)
            symbol = self.get_symbol(urgency)
            
            # Extract any relevant notes
            notes = release.metadata.get('codename', '-')
            
            table.add_row(
                symbol,
                release.eol_date.isoformat() if release.eol_date else "",
                f"{days} d",
                release.display_name,
                release.name,
                notes,
                style=urgency
            )
        
        # Print the table
        self.console.print(table)
        
        # Print summary
        self.console.print(f"\n{len(valid_releases)} releases displayed")
    
    def export_csv(self, releases: List[Release], output_file: str) -> None:
        """
        Export EOL timeline data to CSV.
        
        Args:
            releases: List of releases to export
            output_file: Path to output CSV file
        """
        # Filter out releases without EOL dates
        valid_releases = [r for r in releases if r.eol_date]
        
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # Write header
                writer.writerow(['product', 'version', 'eol_date', 'days_remaining', 'source_file'])
                
                # Write data
                for release in valid_releases:
                    writer.writerow([
                        release.display_name,
                        release.name,
                        release.eol_date.isoformat() if release.eol_date else "",
                        release.days_remaining if release.days_remaining is not None else "",
                        release.source_file
                    ])
                    
            logger.info(f"Exported {len(valid_releases)} releases to {output_file}")
            return True
        except IOError as e:
            logger.error(f"Error exporting to CSV: {e}")
            return False
    
    def export_json(self, releases: List[Release], output_file: str) -> None:
        """
        Export EOL timeline data to JSON.
        
        Args:
            releases: List of releases to export
            output_file: Path to output JSON file
        """
        # Filter out releases without EOL dates
        valid_releases = [r for r in releases if r.eol_date]
        
        # Convert to serializable format
        data = []
        for release in valid_releases:
            data.append({
                'product': release.display_name,
                'version': release.name,
                'eol_date': release.eol_date.isoformat() if release.eol_date else None,
                'days_remaining': release.days_remaining,
                'source_file': release.source_file,
                'policy_source': release.policy_source
            })
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
                
            logger.info(f"Exported {len(valid_releases)} releases to {output_file}")
            return True
        except IOError as e:
            logger.error(f"Error exporting to JSON: {e}")
            return False
