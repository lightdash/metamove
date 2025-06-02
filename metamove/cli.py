import os
from typing import List
import click
from tqdm import tqdm
from metamove.yaml_transformer import transform_yaml

def process_files(input_files: List[str], output_dir: str, in_place: bool = False) -> None:
    if not in_place:
        click.echo(f"Creating output directory: {output_dir}")
        os.makedirs(output_dir, exist_ok=True)
    
    click.echo("\nStarting transformation...")
    successful = 0
    failed = 0
    
    for input_file in tqdm(input_files, desc="Processing YAML files"):
        try:
            if in_place:
                output_file = input_file
                click.echo(f"\nTransforming in place: {input_file}")
            else:
                output_file = os.path.join(output_dir, os.path.basename(input_file))
                click.echo(f"\nTransforming: {input_file}")
                click.echo(f"Output: {output_file}")
            
            transform_yaml(input_file, output_file)
            click.echo(f"✓ Successfully transformed {input_file}")
            successful += 1
        except Exception as e:
            click.echo(f"✗ Error processing {input_file}: {str(e)}", err=True)
            failed += 1
    
    click.echo("\nTransformation Summary:")
    click.echo(f"✓ Successfully transformed: {successful} files")
    if failed > 0:
        click.echo(f"✗ Failed to transform: {failed} files", err=True)

@click.command()
@click.argument('input_files', nargs=-1, type=click.Path(exists=True))
@click.option('--output-dir', '-o', default='transformed', help='Output directory for transformed files')
@click.option('--in-place', '-i', is_flag=True, help='Transform files in place instead of creating copies')
def cli(input_files: List[str], output_dir: str, in_place: bool) -> None:
    """Transform YAML files by moving meta and tags into config sections.
    
    This tool helps migrate your dbt YAML files to be compatible with dbt 1.10
    by moving meta and tags properties under config sections.
    
    Examples:
        # Transform a single file
        metamove models/my_model.yml
        
        # Transform multiple files to a specific directory
        metamove models/*.yml -o transformed_models
        
        # Transform files in place
        metamove models/*.yml -i
        
        # Transform all YAML files in a dbt project
        metamove models/*.yml seeds/*.yml snapshots/*.yml
    """
    if not input_files:
        click.echo(click.get_current_context().get_help())
        return

    yaml_files = [f for f in input_files if f.endswith(('.yml', '.yaml'))]
    if not yaml_files:
        click.echo("No YAML files found in input. Please provide .yml or .yaml files.")
        return

    click.echo(f"Found {len(yaml_files)} YAML files to process")
    if in_place:
        click.echo("⚠️  Warning: Files will be modified in place. Make sure you have backups!")
        if not click.confirm("Do you want to continue?"):
            return
    
    process_files(yaml_files, output_dir, in_place)

if __name__ == '__main__':
    cli() 