"""
Module for parsing JSON files into product data models.
"""
import json
import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple

from .models import Product, Release, Version

logger = logging.getLogger(__name__)

def parse_date(date_value: Any) -> Optional[datetime.date]:
    """Parse a date value in YYYY-MM-DD format."""
    # Convert to string if not already
    if not isinstance(date_value, str):
        if date_value is None:
            return None
        try:
            date_value = str(date_value)
        except Exception:
            logger.debug(f"Cannot convert to string: {date_value}")
            return None
    
    try:
        return datetime.strptime(date_value.strip(), "%Y-%m-%d").date()
    except (ValueError, TypeError) as e:
        logger.debug(f"Invalid date format: {date_value} - {e}")
        return None

def parse_json_file(file_path: str) -> Optional[Product]:
    """
    Parse a JSON file into a Product object.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Product object or None if parsing failed
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Error parsing JSON file {file_path}: {e}")
        return None
    
    # Extract product name from file path
    product_name = os.path.basename(file_path).replace('.json', '')
    
    # Create product object
    product = Product(name=product_name, source_file=file_path)
    
    # Parse releases if present
    if 'releases' in data and isinstance(data['releases'], dict):
        for release_name, release_data in data['releases'].items():
            release = parse_release(release_name, release_data, file_path)
            if release:
                product.releases[release_name] = release
    
    # Parse versions if present
    if 'versions' in data and isinstance(data['versions'], dict):
        for version_name, version_data in data['versions'].items():
            version = parse_version(version_name, version_data, file_path)
            if version:
                product.versions[version_name] = version
    
    return product

def parse_release(release_name: str, data: Dict[str, Any], source_file: str) -> Optional[Release]:
    """
    Parse release data into a Release object.
    
    Args:
        release_name: Name of the release
        data: Dictionary containing release data
        source_file: Path to the source file
        
    Returns:
        Release object or None if required data is missing
    """
    if not isinstance(data, dict):
        logger.warning(f"Invalid release data format for {release_name} in {source_file}")
        return None
    
    # Check for required fields
    name = data.get('name', release_name)
    
    # Parse dates with fallbacks
    release_date = None
    release_date_str = data.get('releaseDate')
    if release_date_str:
        release_date = parse_date(release_date_str)
    
    # Try both releaseDate and date fields
    release_date_str = data.get('releaseDate') or data.get('date')
    if release_date_str:
        release_date = parse_date(release_date_str)
    
    # Release date is optional, can be None
    
    # Parse EOL date if present
    eol_date = None
    eol_date_str = data.get('eol')
    if eol_date_str:
        eol_date = parse_date(eol_date_str)
    
    # Create release object
    release = Release(
        name=name,
        release_date=release_date,
        eol_date=eol_date,
        source_file=source_file,
        policy_source="explicit" if eol_date else "unknown",
        metadata={k: v for k, v in data.items() if k not in ['name', 'releaseDate', 'date', 'eol']}
    )
    
    return release

def parse_version(version_name: str, data: Dict[str, Any], source_file: str) -> Optional[Version]:
    """
    Parse version data into a Version object.
    
    Args:
        version_name: Version identifier
        data: Dictionary containing version data
        source_file: Path to the source file
        
    Returns:
        Version object or None if required data is missing
    """
    if not isinstance(data, dict):
        logger.warning(f"Invalid version data format for {version_name} in {source_file}")
        return None
    
    # Check for required fields
    name = data.get('name', version_name)
    
    # Parse release date
    date_str = data.get('date')
    if not date_str:
        logger.warning(f"Missing date for version {name} in {source_file}")
        return None
    
    release_date = parse_date(date_str)
    if not release_date:
        return None
    
    # Create version object
    version = Version(
        name=name,
        release_date=release_date,
        source_file=source_file,
        metadata={k: v for k, v in data.items() if k not in ['name', 'date']}
    )
    
    return version
