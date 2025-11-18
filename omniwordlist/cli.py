"""
Command-Line Interface for OmniWordlist Pro

Main entry point for the omni command
"""

import click
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.progress import track

from . import __version__
from .config import Config, FilterConfig
from .generator import Generator
from .presets import PresetManager, BUILTIN_PRESETS
from .fields import FieldManager
from .storage import OutputWriter
from .transforms import list_transforms


console = Console()


@click.group()
@click.version_option(version=__version__)
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.pass_context
def cli(ctx, verbose):
    """OmniWordlist Pro - Enterprise-grade wordlist generation"""
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose


@cli.command()
@click.option('--min', 'min_length', type=int, help='Minimum length')
@click.option('--max', 'max_length', type=int, help='Maximum length')
@click.option('--charset', help='Character set')
@click.option('--pattern', help='Pattern (Crunch-style)')
@click.option('--output', '-o', type=click.Path(), help='Output file')
@click.option('--compress', type=click.Choice(['gzip', 'bzip2', 'lz4', 'zstd']), help='Compression format')
@click.option('--prefix', help='Prefix for each token')
@click.option('--suffix', help='Suffix for each token')
@click.option('--format', type=click.Choice(['txt', 'jsonl', 'csv']), default='txt', help='Output format')
@click.option('--preset', help='Use a preset')
@click.option('--sample-size', '-s', type=int, help='Limit output to N tokens')
@click.option('--dedupe', is_flag=True, help='Enable deduplication')
@click.option('--transforms', multiple=True, help='Apply transforms')
@click.pass_context
def run(ctx, min_length, max_length, charset, pattern, output, compress, 
        prefix, suffix, format, preset, sample_size, dedupe, transforms):
    """Generate a wordlist"""
    
    verbose = ctx.obj.get('verbose', False)
    
    # Load preset if specified
    if preset:
        preset_mgr = PresetManager()
        config = preset_mgr.get_preset_config(preset)
        if verbose:
            console.print(f"[green]Loaded preset: {preset}[/green]")
    else:
        config = Config()
    
    # Override with command-line options
    if min_length is not None:
        config.min_length = min_length
    if max_length is not None:
        config.max_length = max_length
    if charset:
        config.charset = charset
    if pattern:
        config.pattern = pattern
    if prefix:
        config.prefix = prefix
    if suffix:
        config.suffix = suffix
    if compress:
        config.compression = compress
    if format:
        config.format = format
    if sample_size:
        config.sample_size = sample_size
        config.max_lines = sample_size
    if dedupe:
        config.dedupe = dedupe
    if transforms:
        config.transforms = list(transforms)
    
    config.verbose = verbose
    
    # Validate configuration
    try:
        config.validate()
    except Exception as e:
        console.print(f"[red]Configuration error: {e}[/red]")
        sys.exit(1)
    
    # Create generator
    try:
        generator = Generator(config)
    except Exception as e:
        console.print(f"[red]Generator error: {e}[/red]")
        sys.exit(1)
    
    # Show stats
    if verbose:
        estimated = generator.estimate_count()
        console.print(f"[cyan]Estimated tokens: {estimated:,}[/cyan]")
    
    # Generate and write
    if output:
        output_path = Path(output)
        console.print(f"[green]Generating wordlist to {output_path}...[/green]")
        
        try:
            with OutputWriter(output_path, config.compression, config.format) as writer:
                for token in track(generator.generate(), 
                                 description="Generating...",
                                 total=config.max_lines):
                    writer.write(token)
            
            console.print(f"[green]✓ Generated {generator.tokens_generated:,} tokens[/green]")
            console.print(f"[cyan]Output: {output_path}[/cyan]")
        except Exception as e:
            console.print(f"[red]Error writing output: {e}[/red]")
            sys.exit(1)
    else:
        # Write to stdout
        for token in generator.generate():
            print(token)


@cli.command()
@click.option('--preset', help='Preview a preset')
@click.option('--sample-size', type=int, default=10, help='Number of samples')
@click.option('--min', 'min_length', type=int, help='Minimum length')
@click.option('--max', 'max_length', type=int, help='Maximum length')
@click.option('--charset', help='Character set')
@click.pass_context
def preview(ctx, preset, sample_size, min_length, max_length, charset):
    """Preview wordlist generation"""
    
    verbose = ctx.obj.get('verbose', False)
    
    # Load preset if specified
    if preset:
        preset_mgr = PresetManager()
        config = preset_mgr.get_preset_config(preset)
        console.print(f"[green]Previewing preset: {preset}[/green]\n")
    else:
        config = Config()
    
    # Override with command-line options
    if min_length is not None:
        config.min_length = min_length
    if max_length is not None:
        config.max_length = max_length
    if charset:
        config.charset = charset
    
    config.verbose = verbose
    config.sample_size = sample_size
    config.max_lines = sample_size
    
    try:
        generator = Generator(config)
        samples = generator.preview(sample_size)
        
        console.print(f"[cyan]Sample output ({len(samples)} tokens):[/cyan]\n")
        for i, token in enumerate(samples, 1):
            console.print(f"  {i:3d}. {token}")
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command('list-presets')
def list_presets():
    """List available presets"""
    preset_mgr = PresetManager()
    presets = preset_mgr.list_presets()
    
    console.print("[cyan]Available Presets:[/cyan]\n")
    
    for i, preset_name in enumerate(presets, 1):
        preset = preset_mgr.get_preset(preset_name)
        desc = preset.get('description', 'No description')
        console.print(f"  {i}. [green]{preset_name:25s}[/green] - {desc}")


@cli.command('show-preset')
@click.argument('preset_name')
def show_preset(preset_name):
    """Show preset details"""
    preset_mgr = PresetManager()
    
    try:
        info = preset_mgr.show_preset(preset_name)
        console.print(info)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.option('--categories', is_flag=True, help='List field categories')
@click.option('--category', help='List fields in a category')
@click.option('--search', help='Search for fields')
def fields(categories, category, search):
    """Browse available fields"""
    
    if categories:
        # List categories
        cats = FieldManager.list_categories()
        console.print("[cyan]Field Categories:[/cyan]\n")
        for cat in cats:
            console.print(f"  - {cat}")
    elif category:
        # List fields in category
        field_list = FieldManager.get_fields_by_category(category)
        console.print(f"[cyan]Fields in category '{category}':[/cyan]\n")
        for field in field_list:
            console.print(f"  - {field['id']:30s} ({field['group']})")
    elif search:
        # Search fields
        results = FieldManager.search_fields(search)
        console.print(f"[cyan]Search results for '{search}':[/cyan]\n")
        for field in results:
            console.print(f"  - {field['id']:30s} [{field['category']}/{field['group']}]")
    else:
        # List all fields
        field_list = FieldManager.list_fields()
        console.print(f"[cyan]All Fields ({len(field_list)} total):[/cyan]\n")
        for field_id in field_list[:20]:  # Show first 20
            console.print(f"  - {field_id}")
        if len(field_list) > 20:
            console.print(f"\n  ... and {len(field_list) - 20} more")


@cli.command()
def info():
    """Show version and system info"""
    console.print(f"[cyan]OmniWordlist Pro v{__version__}[/cyan]\n")
    console.print(f"[green]Python-based Enterprise Wordlist Generator[/green]\n")
    
    console.print("[cyan]Supported transforms:[/cyan]")
    transforms = list_transforms()
    for i in range(0, len(transforms), 3):
        row = transforms[i:i+3]
        console.print(f"  {', '.join(row)}")
    
    console.print("\n[cyan]Supported compression:[/cyan]")
    console.print("  gzip, bzip2, lz4, zstd")
    
    console.print("\n[cyan]Supported formats:[/cyan]")
    console.print("  txt, jsonl, csv")


@cli.command()
def tui():
    """Launch interactive TUI (Terminal User Interface)"""
    console.print("[yellow]TUI not yet implemented in Python version[/yellow]")
    console.print("Use the CLI commands for now.")


def main():
    """Main entry point"""
    try:
        cli(obj={})
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
        sys.exit(130)
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        sys.exit(1)


if __name__ == '__main__':
    main()
