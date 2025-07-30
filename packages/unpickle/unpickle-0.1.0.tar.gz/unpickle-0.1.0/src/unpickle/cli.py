import click
import os
from pathlib import Path


@click.group()
def cli():
    """Tools for working with pickled files"""
    pass


@cli.group()
def lightning():
    """Commands for working with PyTorch Lightning checkpoints"""
    pass


@lightning.command()
@click.argument('checkpoint_path', type=click.Path(exists=True))
@click.argument('output_path', type=click.Path())
@click.option('--force', is_flag=True, help='Overwrite output file if it exists')
@click.option('--verbose', is_flag=True, help='Print verbose output')
def ckpt_to_pth(checkpoint_path: str, output_path: str, force: bool, verbose: bool):
    """
    Convert a Lightning checkpoint to a PyTorch state dict
    """
    from unpickle.lightning import extract_state_dict_from_lightning_ckpt
    import torch

    if Path(output_path).exists() and not force:
        raise click.ClickException(
            f"Output path {output_path} already exists. Use --force to overwrite."
        )

    if verbose:
        click.echo(f"Extracting state dict from {checkpoint_path}")

    state_dict = extract_state_dict_from_lightning_ckpt(checkpoint_path)
    if verbose:
        click.echo("State dict keys:")
        for k in state_dict.keys():
            click.echo(f"  - {k}")
        click.echo(f"Saving state dict to {output_path}")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    torch.save(state_dict, output_path)
    click.echo(f"Saved state dict to {output_path}")


if __name__ == '__main__':
    cli()
