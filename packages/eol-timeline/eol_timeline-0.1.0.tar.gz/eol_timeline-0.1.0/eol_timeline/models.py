from dataclasses import dataclass, field
from datetime import date
from typing import Dict, Optional, Any, List


@dataclass
class Version:
    """Represents a specific version of a software product."""
    name: str
    release_date: date
    source_file: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Release:
    """Represents a major release of a software product with EOL information."""
    name: str
    release_date: date
    source_file: str
    eol_date: Optional[date] = None
    policy_source: str = "unknown"
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def days_remaining(self) -> Optional[int]:
        """Calculate days remaining until EOL from today."""
        if not self.eol_date:
            return None
        from datetime import datetime
        today = datetime.now().date()
        return (self.eol_date - today).days
    
    @property
    def display_name(self) -> str:
        """Return the formatted display name for the product."""
        # Extract product name from the source file path
        import os
        file_name = os.path.basename(self.source_file)
        product_name = os.path.splitext(file_name)[0]
        # Convert kebab-case to Title Case
        return " ".join(word.capitalize() for word in product_name.split("-"))


@dataclass
class Product:
    """Represents a software product with its releases and versions."""
    name: str
    releases: Dict[str, Release] = field(default_factory=dict)
    versions: Dict[str, Version] = field(default_factory=dict)
    source_file: str = ""
    
    @property
    def display_name(self) -> str:
        """Return the formatted display name for the product."""
        # Convert kebab-case to Title Case
        return " ".join(word.capitalize() for word in self.name.split("-"))
