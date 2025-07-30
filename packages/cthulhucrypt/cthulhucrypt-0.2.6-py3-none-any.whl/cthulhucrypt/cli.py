# cthulhucrypt/cli.py
import click
from .core import (
    encrypt as core_encrypt,
    decrypt as core_decrypt,
    med_hash as core_med_hash,
    high_hash as core_high_hash,
    hash2 as core_hash2,
    hash2_high as core_hash2_high,
)

@click.group()
def cli():
    """CthulhuCrypt CLI - An unholy encryption toolkit."""
    pass

@cli.command()
@click.argument("text")
@click.argument("table_idx", required=False, type=int)
def decrypt(text, table_idx=None):
    """Decrypt hex text with table index. Accepts either 'encrypted;text_idx' or separate args."""
    # Try to extract table_idx if not provided
    if table_idx is None:
        if ";" in text:
            encrypted_part, possible_idx = text.rsplit(";", 1)
            if possible_idx.isdigit():
                table_idx = int(possible_idx)
                text = encrypted_part
    if table_idx is None:
        click.echo("Error: You must provide a table_idx, either as a second argument or as 'encrypted;text_idx'.")
        return
    try:
        result = core_decrypt(text, table_idx)
        click.echo(f"Decrypted: {result}")
    except Exception as e:
        click.echo(f"Error: {e}")

@cli.command()
@click.argument("text")
def encrypt(text):
    """Encrypt text (returns hex;text_idx for easy copy-paste)."""
    result, table_idx = core_encrypt(text)
    click.echo(f"{result};{table_idx}")

@cli.command()
@click.argument("text")
def medhash(text):
    """Run med_hash on text."""
    result = core_med_hash(text)
    click.echo(f"med_hash: {result}")

@cli.command()
@click.argument("text")
@click.option("--iterations", default=7, help="Number of iterations")
def highhash(text, iterations):
    """Run high_hash on text."""
    result = core_high_hash(text, iterations)
    click.echo(f"high_hash: {result}")

@cli.command()
@click.argument("text")
@click.option("--iterations", default=7, help="Number of iterations")
def hash2(text, iterations):
    """Run hash2 on text."""
    result = core_hash2(text, iterations)
    click.echo(f"hash2: {result}")

@cli.command()
@click.argument("text")
@click.option("--iterations", default=7, help="Number of iterations")
def hash2_high(text, iterations):
    """Run hash2_high on text."""
    result = core_hash2_high(text, iterations)
    click.echo(f"hash2_high: {result}")

if __name__ == "__main__":
    cli()