import os
from typing import List
import click
from tqdm import tqdm
from metamove.yaml_transformer import transform_yaml

def process_files(input_files: List[str], output_dir: str, in_place: bool = False) -> None:
    if not in_place:
        os.makedirs(output_dir, exist_ok=True)
    
    for input_file in tqdm(input_files, desc="Processing YAML files"):
        try:
            if in_place:
                output_file = input_file
            else:
                output_file = os.path.join(output_dir, os.path.basename(input_file))
            
            transform_yaml(input_file, output_file)
            tqdm.write(f"✓ Processed {input_file}")
        except Exception as e:
            tqdm.write(f"✗ Error processing {input_file}: {str(e)}")

@click.command()
@click.argument('input_files', nargs=-1, type=click.Path(exists=True))
@click.option('--output-dir', '-o', default='transformed', help='Output directory for transformed files')
@click.option('--in-place', '-i', is_flag=True, help='Transform files in place instead of creating copies')
def cli(input_files: List[str], output_dir: str, in_place: bool) -> None:
    """Transform YAML files by moving meta and tags into config sections."""
    if not input_files:
        click.echo("No input files provided")
        return

    yaml_files = [f for f in input_files if f.endswith(('.yml', '.yaml'))]
    if not yaml_files:
        click.echo("No YAML files found in input")
        return

    click.echo(f"Found {len(yaml_files)} YAML files to process")
    process_files(yaml_files, output_dir, in_place)
    click.echo("\nTransformation complete!")

if __name__ == '__main__':
    cli() 