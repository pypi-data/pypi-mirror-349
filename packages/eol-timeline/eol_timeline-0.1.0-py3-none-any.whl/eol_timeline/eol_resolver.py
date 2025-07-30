"""
Module for resolving EOL dates using policies and rules.
"""
import os
import logging
import yaml
from datetime import date, timedelta
from typing import Dict, Any, List, Optional, Set
from pathlib import Path
from dateutil.relativedelta import relativedelta

from .models import Product, Release, Version

logger = logging.getLogger(__name__)

DEFAULT_YEARS_AFTER_RELEASE = 3

class PolicyLoader:
    """Loads EOL policies from YAML configuration files."""
    
    def __init__(self, policy_file: Optional[str] = None):
        self.policies: Dict[str, Any] = {
            "defaults": {
                "years_after_release": DEFAULT_YEARS_AFTER_RELEASE
            },
            "products": {}
        }
        
        # Load policy file if provided
        if policy_file:
            self.load_policy_file(policy_file)
        else:
            # Try to load from default locations
            home_config = os.path.expanduser("~/.config/eol/policies.yaml")
            if os.path.exists(home_config):
                self.load_policy_file(home_config)
    
    def load_policy_file(self, file_path: str) -> bool:
        """
        Load policies from a YAML file.
        
        Args:
            file_path: Path to the YAML policy file
            
        Returns:
            True if the file was loaded successfully, False otherwise
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                policies = yaml.safe_load(f)
                
            if not isinstance(policies, dict):
                logger.error(f"Invalid policy file format: {file_path}")
                return False
                
            # Update the defaults if specified
            if 'defaults' in policies and isinstance(policies['defaults'], dict):
                self.policies['defaults'].update(policies['defaults'])
                
            # Update the product-specific policies
            if 'products' in policies and isinstance(policies['products'], dict):
                self.policies['products'].update(policies['products'])
                
            logger.info(f"Loaded policy file: {file_path}")
            return True
            
        except (yaml.YAMLError, IOError) as e:
            logger.error(f"Error loading policy file {file_path}: {e}")
            return False
    
    def get_default_years_after_release(self) -> int:
        """Get the default years after release value from policies."""
        return self.policies['defaults'].get('years_after_release', DEFAULT_YEARS_AFTER_RELEASE)
    
    def get_product_policy(self, product_name: str) -> Dict[str, Any]:
        """
        Get policy for a specific product.
        
        Args:
            product_name: Name of the product (may need normalization)
            
        Returns:
            Dictionary containing the product policy, or empty dict if not found
        """
        # Try exact match
        if product_name in self.policies['products']:
            return self.policies['products'][product_name]
        
        # Try with display name conversion (kebab-case to Title Case)
        display_name = " ".join(word.capitalize() for word in product_name.split("-"))
        if display_name in self.policies['products']:
            return self.policies['products'][display_name]
        
        # No specific policy found
        return {}


class EOLResolver:
    """Resolves EOL dates for products and releases based on policies."""
    
    def __init__(self, policy_file: Optional[str] = None):
        self.policy_loader = PolicyLoader(policy_file)
    
    def calculate_eol_date(self, release_date: date, years: int) -> date:
        """
        Calculate EOL date based on release date and years of support.
        
        Args:
            release_date: The release date
            years: Number of years of support
            
        Returns:
            Calculated EOL date
        """
        # Use relativedelta for accurate year-based calculation
        return release_date + relativedelta(years=years)
    
    def resolve_eol_for_product(self, product: Product) -> List[Release]:
        """
        Resolve EOL dates for all releases and versions of a product.
        
        Args:
            product: The product to resolve EOL dates for
            
        Returns:
            List of Release objects with resolved EOL dates
        """
        result: List[Release] = []
        
        # Get product-specific policy
        product_policy = self.policy_loader.get_product_policy(product.name)
        
        # Process explicit releases first
        for release_name, release in product.releases.items():
            if release.eol_date:
                # EOL date is explicitly specified
                release.policy_source = "explicit"
            else:
                # Need to determine EOL date using policy
                self._resolve_eol_for_release(release, product_policy)
            
            result.append(release)
        
        # Process versions and convert them to releases
        used_version_names: Set[str] = set()
        for version_name, version in product.versions.items():
            # Skip if this version name already exists as a release
            if version_name in used_version_names:
                continue
                
            # Create a new release object from this version
            release = Release(
                name=version_name,
                release_date=version.release_date,
                source_file=version.source_file,
                metadata=version.metadata
            )
            
            # Resolve EOL date using policy
            self._resolve_eol_for_release(release, product_policy)
            
            result.append(release)
            used_version_names.add(version_name)
        
        return result
    
    def _resolve_eol_for_release(self, release: Release, product_policy: Dict[str, Any]) -> None:
        """
        Resolve EOL date for a specific release using appropriate policy.
        
        Args:
            release: The release to resolve EOL date for
            product_policy: Product-specific policy dictionary
        """
        # Skip releases without a release date
        if not release.release_date:
            logger.debug(f"Skipping EOL calculation for {release.name} due to missing release date")
            return

        # Check if product policy specifies years_after_release
        if 'years_after_release' in product_policy:
            years = product_policy['years_after_release']
            release.eol_date = self.calculate_eol_date(release.release_date, years)
            release.policy_source = "product_policy"
            return
            
        # Check if this is an LTS release for products with lts_years policy
        if 'lts_years' in product_policy:
            # Check if version name or metadata indicates LTS
            is_lts = False
            if 'LTS' in release.name:
                is_lts = True
            elif release.metadata.get('lts') is True:
                is_lts = True
            elif release.metadata.get('codename', '').lower().endswith('lts'):
                is_lts = True
                
            if is_lts:
                years = product_policy['lts_years']
                release.eol_date = self.calculate_eol_date(release.release_date, years)
                release.policy_source = "lts_policy"
                return
        
        # Fall back to default years_after_release
        years = self.policy_loader.get_default_years_after_release()
        release.eol_date = self.calculate_eol_date(release.release_date, years)
        release.policy_source = "default_policy"


def resolve_eol_dates(products: List[Product], policy_file: Optional[str] = None) -> List[Release]:
    """
    Resolve EOL dates for a list of products.
    
    Args:
        products: List of products to resolve EOL dates for
        policy_file: Optional path to policy file
        
    Returns:
        List of all releases with resolved EOL dates
    """
    resolver = EOLResolver(policy_file)
    all_releases = []
    
    for product in products:
        releases = resolver.resolve_eol_for_product(product)
        all_releases.extend(releases)
    
    return all_releases
