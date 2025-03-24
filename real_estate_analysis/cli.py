#!/usr/bin/env python3
"""
Command-line interface for the Real Estate Market Analysis System.
"""

import asyncio
import logging
import sys
from typing import Optional
import os

import click
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import Progress, SpinnerColumn, TextColumn
from dotenv import load_dotenv

from api_integrations.census import CensusAPI
from api_integrations.property import PropertyAPI
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)

console = Console()

# Load environment variables
load_dotenv()

@click.group()
def cli():
    """Real Estate Market Analysis System CLI."""
    pass

@cli.command()
@click.argument("address")
@click.option("--output", "-o", help="Output file for the analysis results")
def analyze_property(address: str, output: Optional[str] = None):
    """Analyze a single property."""
    async def run_analysis():
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                # Initialize APIs
                census_api = CensusAPI(api_key=os.getenv('CENSUS_API_KEY'))
                property_api = PropertyAPI(api_key=os.getenv('PROPERTY_API_KEY'))

                # Get demographic data
                progress.add_task(description="Fetching demographic data...", total=None)
                demographics = await census_api.get_demographic_data(address)

                # Get property data
                progress.add_task(description="Fetching property data...", total=None)
                property_data = await property_api.get_property_details(address)

                # Analyze market
                progress.add_task(description="Analyzing market conditions...", total=None)
                market_analysis = await property_api.analyze_market(address)

                # Display results
                console.print("\n[bold green]Analysis Results[/bold green]")
                console.print("\n[bold]Demographic Data:[/bold]")
                console.print(demographics)
                console.print("\n[bold]Property Data:[/bold]")
                console.print(property_data)
                console.print("\n[bold]Market Analysis:[/bold]")
                console.print(market_analysis)

                if output:
                    # Save results to file
                    import json
                    with open(output, "w") as f:
                        json.dump({
                            "demographics": demographics,
                            "property_data": property_data,
                            "market_analysis": market_analysis,
                        }, f, indent=2)
                    console.print(f"\n[green]Results saved to {output}[/green]")

        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")
            sys.exit(1)

    asyncio.run(run_analysis())

@cli.command()
@click.argument("location")
@click.option("--output", "-o", help="Output file for the market analysis")
def analyze_market(location: str, output: Optional[str] = None):
    """Analyze market conditions for a location."""
    async def run_market_analysis():
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                # Initialize API
                property_api = PropertyAPI(api_key=os.getenv('PROPERTY_API_KEY'))

                # Analyze market
                progress.add_task(description="Analyzing market conditions...", total=None)
                market_analysis = await property_api.analyze_market(location)

                # Display results
                console.print("\n[bold green]Market Analysis Results[/bold green]")
                console.print(market_analysis)

                if output:
                    # Save results to file
                    import json
                    with open(output, "w") as f:
                        json.dump(market_analysis, f, indent=2)
                    console.print(f"\n[green]Results saved to {output}[/green]")

        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")
            sys.exit(1)

    asyncio.run(run_market_analysis())

@cli.command()
def check_health():
    """Check the health of all API integrations."""
    async def run_health_check():
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                # Initialize APIs
                census_api = CensusAPI(api_key=os.getenv('CENSUS_API_KEY'))
                property_api = PropertyAPI(api_key=os.getenv('PROPERTY_API_KEY'))

                # Check Census API
                progress.add_task(description="Checking Census API...", total=None)
                census_health = await census_api.health_check()
                console.print("\n[bold]Census API Health:[/bold]")
                console.print(census_health)

                # Check Property API
                progress.add_task(description="Checking Property API...", total=None)
                property_health = await property_api.health_check()
                console.print("\n[bold]Property API Health:[/bold]")
                console.print(property_health)

        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")
            sys.exit(1)

    asyncio.run(run_health_check())

def main():
    """Entry point for the CLI."""
    cli()

if __name__ == "__main__":
    main() 