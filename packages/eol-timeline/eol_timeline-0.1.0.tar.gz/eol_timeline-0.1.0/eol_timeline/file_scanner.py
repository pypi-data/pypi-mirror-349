"""
Module for scanning directories to find JSON files containing EOL information.
"""
import os
import glob
from pathlib import Path
from typing import List, Iterator
import logging

logger = logging.getLogger(__name__)

def find_release_files(root_path: str) -> List[str]:
    """
    Find all JSON files in the releases directories under the root path.
    
    Args:
        root_path: The root directory to start the search from
        
    Returns:
        List of absolute paths to JSON files
    """
    logger.info(f"Scanning for release files in: {root_path}")
    
    # Convert to Path object for easier manipulation
    root = Path(root_path)
    
    # Find all directories matching */releases
    release_dirs = []
    for path in root.glob("**/releases"):
        if path.is_dir():
            release_dirs.append(path)
    
    logger.info(f"Found {len(release_dirs)} release directories")
    
    # Find all JSON files in these directories
    json_files = []
    for release_dir in release_dirs:
        for json_file in release_dir.glob("*.json"):
            json_files.append(str(json_file))
    
    logger.info(f"Found {len(json_files)} JSON files")
    return json_files


def scan_directory(directory: str) -> Iterator[str]:
    """
    Iterator version of find_release_files that yields files one by one.
    
    Args:
        directory: The directory to scan
        
    Yields:
        Absolute paths to JSON files one at a time
    """
    for path in Path(directory).glob("**/releases/*.json"):
        if path.is_file():
            yield str(path)
