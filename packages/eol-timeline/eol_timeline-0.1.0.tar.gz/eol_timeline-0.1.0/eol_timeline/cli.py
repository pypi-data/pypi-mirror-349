"""
Main CLI module for the EOL Timeline application.
"""
import os
import sys
import logging
import json
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from pathlib import Path
from typing import List, Optional, Tuple

import typer
from rich.console import Console
from rich.logging import RichHandler

from . import __version__
from .file_scanner import find_release_files
from .data_parser import parse_json_file
from .eol_resolver import resolve_eol_dates
from .presenter import Presenter
from .models import Product, Release

# Set up logger
FORMAT = "%(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger("eol")

# Create Typer app
app = typer.Typer(
    help="EOL Timeline - Track software end-of-life dates",
    add_completion=False
)
console = Console()


# Common options
class CommonOptions:
    def __init__(
        self,
        root: str = None,
        today: Optional[date] = None,
        policy: Optional[Path] = None,
        verbose: bool = False,
        log_json: bool = False,
        no_color: bool = False
    ):
        self.root = root or "."
        self.today = today or date.today()
        self.policy = policy
        self.verbose = verbose
        self.log_json = log_json
        self.no_color = no_color
        
        # Set log level based on verbosity
        if verbose:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
        
        # Configure JSON logging if requested
        if log_json:
            # Replace handlers
            for handler in logging.root.handlers[:]:
                logging.root.removeHandler(handler)
            
            class JSONFormatter(logging.Formatter):
                def format(self, record):
                    log_data = {
                        "timestamp": datetime.now().isoformat(),
                        "level": record.levelname,
                        "message": record.getMessage(),
                        "module": record.module
                    }
                    if record.exc_info:
                        log_data["exception"] = self.formatException(record.exc_info)
                    return json.dumps(log_data)
            
            json_handler = logging.StreamHandler(sys.stderr)
            json_handler.setFormatter(JSONFormatter())
            logging.root.addHandler(json_handler)


def load_and_process_data(
    options: CommonOptions, 
    from_date: Optional[date] = None, 
    to_date: Optional[date] = None,
    products: Optional[List[str]] = None,
    no_color: bool = False,
    group_style: str = "auto",
    sort: str = "eol"
) -> Tuple[List[Product], List[Release]]:
    """
    Load and process data based on command options.
    
    Args:
        options: Common command options
        from_date: Optional filter for EOL dates from this date
        to_date: Optional filter for EOL dates up to this date
        products: Optional list of product names to filter by
        
    Returns:
        Tuple of (products list, filtered releases list)
    """
    # Find JSON files
    logger.debug(f"Scanning for JSON files in {options.root}")
    json_files = find_release_files(options.root)
    logger.info(f"Found {len(json_files)} JSON files")
    
    # Parse JSON files
    raw_products = []
    for file_path in json_files:
        product = parse_json_file(file_path)
        if product:
            raw_products.append(product)
    
    logger.info(f"Parsed {len(raw_products)} products successfully")
    
    # Resolve EOL dates
    policy_file = options.policy.as_posix() if options.policy else None
    all_releases = resolve_eol_dates(raw_products, policy_file)
    logger.info(f"Resolved EOL dates for {len(all_releases)} releases")
    
    # Filter releases
    filtered_releases = []
    for release in all_releases:
        # Only show releases with explicit EOL dates
        if release.policy_source != "explicit":
            continue
            
        # Apply date filters
        if from_date and release.eol_date < from_date:
            continue
        if to_date is not None and release.eol_date > to_date:
            continue
            
        # Apply product filter
        if products:
            if not any(p.lower() in release.display_name.lower() for p in products):
                continue
                
        # Add remaining releases
        filtered_releases.append(release)
    
    # Display results
    presenter = Presenter(use_color=not no_color, style=group_style)
    presenter.display_table(filtered_releases, options.today, sort_by=sort)
    
    logger.info(f"Filtered to {len(filtered_releases)} releases")
    return raw_products, filtered_releases


@app.callback()
def callback(
    version: bool = typer.Option(False, "--version", help="Show app version."),
    root: str = typer.Option(None, "--root", help="Root directory containing release-data. [env: EOL_DATA_ROOT]", envvar="EOL_DATA_ROOT"),
    policy: Optional[Path] = typer.Option(None, "--policy", help="YAML file defining EOL rules.", exists=True, file_okay=True, dir_okay=False),
    verbose: bool = typer.Option(False, "--verbose/--quiet", help="Enable verbose output."),
    log_json: bool = typer.Option(False, "--log-json", help="Emit structured logs to STDERR.")
):
    """EOL Timeline - Track software end-of-life dates."""
    if version:
        console.print(f"EOL Timeline version: {__version__}")
        raise typer.Exit()


@app.command("list")
def list_command(
    root: str = typer.Option(None, "--root", help="Root directory containing release-data. [env: EOL_DATA_ROOT]", envvar="EOL_DATA_ROOT"),
    today: Optional[str] = typer.Option(None, "--today", help="Override today's date (YYYY-MM-DD)."),
    policy: Optional[Path] = typer.Option(None, "--policy", help="YAML file defining EOL rules.", exists=True, file_okay=True, dir_okay=False),
    verbose: bool = typer.Option(False, "--verbose/--quiet", help="Enable verbose output."),
    log_json: bool = typer.Option(False, "--log-json", help="Emit structured logs to STDERR."),
    product: Optional[List[str]] = typer.Option(None, "--product", help="Filter by product name (can be used multiple times)."),
    products_yaml: Optional[Path] = typer.Option(None, "--products-yaml", help="YAML file with a list of product names to filter by. Overrides --product if both are used."),
    from_date: Optional[str] = typer.Option(None, "--from", help="Show EOL dates from this date (default: today)."),
    to_date: Optional[str] = typer.Option(None, "--to", help="Show EOL dates up to this date."),
    sort: str = typer.Option("eol", "--sort", help="Sort by: eol, product, or version."),
    group_style: str = typer.Option("auto", "--group-style", help="Display style: auto, plain, or emoji."),
    no_color: bool = typer.Option(False, "--no-color", help="Disable colored output."),
    max_age: Optional[str] = typer.Option(None, "--max-age", help="Show EOL dates within this time period from today (e.g., 1m, 1y, 2w)."),
):
    """Display upcoming EOL dates."""
    common = CommonOptions(root, None, policy, verbose, log_json, no_color)
    # Parse today
    if today is not None:
        try:
            parsed_today = datetime.strptime(today, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format for --today. Use YYYY-MM-DD.", file=sys.stderr)
            raise typer.Exit(1)
    else:
        parsed_today = date.today()
    common.today = parsed_today
    
    # Initialize date variables
    parsed_from_date = parsed_today
    parsed_to_date = None
    # Parse from_date and to_date
    if from_date is not None:
        try:
            parsed_from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
        except ValueError:
            logger.error("Invalid date format for --from. Use YYYY-MM-DD.")
            raise typer.Exit(1)
    
    # Parse max_age if provided
    if max_age is not None:
        try:
            # Parse the time unit
            value = int(max_age[:-1])
            unit = max_age[-1]
            if unit == 'd':
                parsed_to_date = parsed_today + timedelta(days=value)
            elif unit == 'w':
                parsed_to_date = parsed_today + timedelta(weeks=value)
            elif unit == 'm':
                parsed_to_date = parsed_today + relativedelta(months=value)
            elif unit == 'y':
                parsed_to_date = parsed_today + relativedelta(years=value)
            else:
                raise ValueError(f"Invalid time unit: {unit}. Use d (days), w (weeks), m (months), or y (years)")
        except (ValueError, TypeError) as e:
            error_msg = f"Invalid max-age format: {max_age}. Use format like 1m, 1y, 2w."
            logger.error(error_msg)
            print(error_msg, file=sys.stderr)
            raise typer.Exit(1)
    
    # If no max_age but to_date is provided, use that
    if to_date is not None:
        try:
            parsed_to_date = datetime.strptime(to_date, "%Y-%m-%d").date()
        except ValueError:
            logger.error("Invalid date format for --to. Use YYYY-MM-DD.")
            raise typer.Exit(1)
    # If products_yaml is provided, load product list from YAML and override --product
    products_list = list(product) if product else None
    if products_yaml is not None:
        try:
            import yaml
            with open(products_yaml, 'r', encoding='utf-8') as f:
                yaml_data = yaml.safe_load(f)
            if isinstance(yaml_data, dict) and 'products' in yaml_data:
                yaml_products = yaml_data['products']
            else:
                yaml_products = yaml_data
            if not isinstance(yaml_products, list) or not all(isinstance(p, str) for p in yaml_products):
                print("YAML file must contain a list of product names or a 'products' key with a list.", file=sys.stderr)
                raise typer.Exit(1)
            products_list = yaml_products
        except Exception as e:
            print(f"Failed to read products from YAML: {e}", file=sys.stderr)
            raise typer.Exit(1)
    _, filtered_releases = load_and_process_data(common, parsed_from_date, parsed_to_date, products_list, no_color, group_style, sort)
    if not filtered_releases:
        logger.warning("No EOL dates found matching the criteria")
        return
    presenter = Presenter(use_color=not no_color, style=group_style)
    presenter.display_table(filtered_releases, parsed_today, sort_by=sort)


@app.command("products")
def products_command(
    root: str = typer.Option(None, "--root", help="Root directory containing release-data. [env: EOL_DATA_ROOT]", envvar="EOL_DATA_ROOT"),
    output: Optional[Path] = typer.Option(None, "--output", help="Output file in YAML format. The file will contain a list of all available products."),
    verbose: bool = typer.Option(False, "--verbose/--quiet", help="Enable verbose output."),
    log_json: bool = typer.Option(False, "--log-json", help="Emit structured logs to STDERR."),
    no_color: bool = typer.Option(False, "--no-color", help="Disable colored output."),
):
    """List all available products."""
    common = CommonOptions(root, None, None, verbose, log_json, no_color)
    
    # Find and parse JSON files to get product names
    logger.debug(f"Scanning for JSON files in {common.root}")
    json_files = find_release_files(common.root)
    logger.info(f"Found {len(json_files)} JSON files")
    
    # Extract product names from file paths
    product_names = set()
    for file_path in json_files:
        try:
            # Extract product name from file path (filename without .json extension)
            product_name = os.path.splitext(os.path.basename(file_path))[0]
            product_names.add(product_name)
        except Exception as e:
            logger.warning(f"Failed to process file {file_path}: {e}")
    
    # Sort product names alphabetically
    sorted_products = sorted(product_names, key=str.lower)
    
    # Print to terminal
    console.print("[bold]Available Products:[/bold]")
    for product in sorted_products:
        console.print(f"• {product}")
    
    # If output file is specified, write to YAML
    if output is not None:
        try:
            import yaml
            with open(output, 'w', encoding='utf-8') as f:
                yaml.dump({"products": sorted_products}, f, default_flow_style=False)
            console.print(f"[bold]Products written to {output}[/bold]")
        except Exception as e:
            print(f"Failed to write to YAML file: {e}", file=sys.stderr)
            raise typer.Exit(1)

@app.command("export")
def export_command(
    root: str = typer.Option(None, "--root", help="Root directory containing release-data. [env: EOL_DATA_ROOT]", envvar="EOL_DATA_ROOT"),
    today: Optional[str] = typer.Option(None, "--today", help="Override today's date (YYYY-MM-DD)."),
    policy: Optional[Path] = typer.Option(None, "--policy", help="YAML file defining EOL rules.", exists=True, file_okay=True, dir_okay=False),
    verbose: bool = typer.Option(False, "--verbose/--quiet", help="Enable verbose output."),
    log_json: bool = typer.Option(False, "--log-json", help="Emit structured logs to STDERR."),
    format: str = typer.Option("csv", "--format", help="Export format: csv or json."),
    out: Optional[Path] = typer.Option(None, "--out", help="Output file path."),
    product: Optional[List[str]] = typer.Option(None, "--product", help="Filter by product name (can be used multiple times)."),
    products_yaml: Optional[Path] = typer.Option(None, "--products-yaml", help="YAML file with a list of product names to filter by."),
    from_date: Optional[str] = typer.Option(None, "--from", help="Show EOL dates from this date (default: today)."),
    to_date: Optional[str] = typer.Option(None, "--to", help="Show EOL dates up to this date."),
):
    """Export results to CSV/JSON."""
    common = CommonOptions(root, None, policy, verbose, log_json)
    # Parse today
    if today is not None:
        try:
            parsed_today = datetime.strptime(today, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format for --today. Use YYYY-MM-DD.", file=sys.stderr)
        raise typer.Exit(1)
    else:
        parsed_today = date.today()
    common.today = parsed_today
    # Parse from_date and to_date
    parsed_from_date = parsed_today
    parsed_to_date = None
    if from_date is not None:
        try:
            parsed_from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
        except ValueError:
            logger.error("Invalid date format for --from. Use YYYY-MM-DD.")
            raise typer.Exit(1)
    if to_date is not None:
        try:
            parsed_to_date = datetime.strptime(to_date, "%Y-%m-%d").date()
        except ValueError:
            logger.error("Invalid date format for --to. Use YYYY-MM-DD.")
            raise typer.Exit(1)
    _, filtered_releases = load_and_process_data(common, parsed_from_date, parsed_to_date, product)
    if not filtered_releases:
        logger.warning("No EOL dates found matching the criteria")
        return
    if not out:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out = Path(f"eol_{timestamp}.{format}")
    presenter = Presenter()
    if format.lower() == "csv":
        success = presenter.export_csv(filtered_releases, out)
    elif format.lower() == "json":
        success = presenter.export_json(filtered_releases, out)
    else:
        logger.error(f"Unsupported export format: {format}")
        raise typer.Exit(1)
    if success:
        console.print(f"Exported {len(filtered_releases)} entries to [bold]{out}[/bold]")
    else:
        print(f"Failed to export data to {out}", file=sys.stderr)
        raise typer.Exit(1)


@app.command("validate")
def validate_command(
    root: str = typer.Option(None, "--root", help="Root directory containing release-data. [env: EOL_DATA_ROOT]", envvar="EOL_DATA_ROOT"),
    today: Optional[str] = typer.Option(None, "--today", help="Override today's date (YYYY-MM-DD)."),
    policy: Optional[Path] = typer.Option(None, "--policy", help="YAML file defining EOL rules.", exists=True, file_okay=True, dir_okay=False),
    verbose: bool = typer.Option(False, "--verbose/--quiet", help="Enable verbose output."),
    log_json: bool = typer.Option(False, "--log-json", help="Emit structured logs to STDERR."),
):
    """Validate JSON dataset and policy file."""
    if today is not None:
        try:
            parsed_today = datetime.strptime(today, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format for --today. Use YYYY-MM-DD.", file=sys.stderr)
            raise typer.Exit(1)
    else:
        parsed_today = date.today()
    common = CommonOptions(root, parsed_today, policy, verbose, log_json)
    json_files = find_release_files(common.root)
    logger.info(f"Found {len(json_files)} JSON files")
    error_count = 0
    schema_errors = 0
    policy_errors = 0
    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if not isinstance(data, dict):
                logger.error(f"Invalid JSON structure in {file_path}: not a dictionary")
                schema_errors += 1
                continue
            if "releases" not in data:
                logger.error(f"Missing 'releases' key in {file_path}")
                schema_errors += 1
            if "versions" not in data:
                logger.error(f"Missing 'versions' key in {file_path}")
                schema_errors += 1
            if isinstance(data.get("releases"), dict):
                for release_name, release_data in data["releases"].items():
                    if not isinstance(release_data, dict):
                        logger.error(f"Invalid release data for {release_name} in {file_path}")
                        schema_errors += 1
                        continue
                    if "releaseDate" not in release_data and "date" not in release_data:
                        logger.error(f"Missing release date for {release_name} in {file_path}")
                        schema_errors += 1
            if isinstance(data.get("versions"), dict):
                for version_name, version_data in data["versions"].items():
                    if not isinstance(version_data, dict):
                        logger.error(f"Invalid version data for {version_name} in {file_path}")
                        schema_errors += 1
                        continue
                    if "date" not in version_data:
                        logger.error(f"Missing date for version {version_name} in {file_path}")
                        schema_errors += 1
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {file_path}: {e}")
            error_count += 1
        except IOError as e:
            logger.error(f"Error reading {file_path}: {e}")
            error_count += 1
    if common.policy:
        try:
            import yaml
            with open(common.policy, 'r', encoding='utf-8') as f:
                policy_data = yaml.safe_load(f)
            if not isinstance(policy_data, dict):
                logger.error(f"Invalid policy format: {common.policy}")
                policy_errors += 1
            else:
                if "defaults" in policy_data and not isinstance(policy_data["defaults"], dict):
                    logger.error(f"Invalid 'defaults' section in policy")
                    policy_errors += 1
                if "products" in policy_data and not isinstance(policy_data["products"], dict):
                    logger.error(f"Invalid 'products' section in policy")
                    policy_errors += 1
        except yaml.YAMLError as e:
            logger.error(f"Invalid YAML in policy file: {e}")
            policy_errors += 1
        except IOError as e:
            logger.error(f"Error reading policy file: {e}")
            policy_errors += 1
    total_errors = error_count + schema_errors + policy_errors
    if total_errors > 0:
        logger.error(f"Validation failed with {total_errors} errors")
        logger.error(f"- {error_count} file errors")
        logger.error(f"- {schema_errors} schema violations")
        logger.error(f"- {policy_errors} policy errors")
        raise typer.Exit(1)
    else:
        console.print("[bold green]Validation successful![/bold green]")


def main():
    """Entry point for the CLI."""
    app()
