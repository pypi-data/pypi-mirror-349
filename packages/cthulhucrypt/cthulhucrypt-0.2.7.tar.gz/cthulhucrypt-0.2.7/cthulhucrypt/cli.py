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

def get_input_text(text, file):
    if file:
        with open(file, 'r', encoding='utf-8') as f:
            return f.read()
    return text

def handle_output(result, output):
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            f.write(str(result) + '\n')
    else:
        click.echo(result)

@cli.command()
@click.argument("text", required=False)
@click.option('--file', '-fi', 'file', type=click.Path(exists=True), help='Input file to encrypt')
@click.option('--output', '-out', 'output', type=click.Path(), help='Output file for encrypted result')
def encrypt(text, file, output):
    """Encrypt text or file (returns hex;text_idx for easy copy-paste)."""
    input_text = get_input_text(text, file)
    input_text = input_text.rstrip('\n\r')
    result, table_idx = core_encrypt(input_text)
    output_str = f"{result};{table_idx}"
    handle_output(output_str, output)

@cli.command()
@click.argument("text", required=False)
@click.option('--file', '-fi', 'file', type=click.Path(exists=True), help='Input file to decrypt')
@click.argument("table_idx", required=False, type=int)
@click.option('--output', '-out', 'output', type=click.Path(), help='Output file for decrypted result')
def decrypt(text, file, table_idx, output):
    """Decrypt hex text or file with table index. Accepts either 'encrypted;text_idx' or separate args."""
    input_text = get_input_text(text, file)
    # Try to extract table_idx if not provided
    if table_idx is None:
        if ";" in input_text:
            encrypted_part, possible_idx = input_text.rsplit(";", 1)
            possible_idx = possible_idx.strip()  # Strip whitespace
            if possible_idx.isdigit():
                table_idx = int(possible_idx)
                input_text = encrypted_part
    if table_idx is None:
        click.echo("Error: You must provide a table_idx, either as a second argument or as 'encrypted;text_idx'.")
        return
    try:
        result = core_decrypt(input_text, table_idx)
        handle_output(result, output)
    except Exception as e:
        click.echo(f"Error: {e}")

@cli.command()
@click.argument("text", required=False)
@click.option('--file', '-fi', 'file', type=click.Path(exists=True), help='Input file to hash')
@click.option('--output', '-out', 'output', type=click.Path(), help='Output file for hash result')
def medhash(text, file, output):
    """Run med_hash on text or file."""
    input_text = get_input_text(text, file)
    result = core_med_hash(input_text)
    handle_output(f"med_hash: {result}", output)

@cli.command()
@click.argument("text", required=False)
@click.option('--file', '-fi', 'file', type=click.Path(exists=True), help='Input file to hash')
@click.option("--iterations", default=7, help="Number of iterations")
@click.option('--output', '-out', 'output', type=click.Path(), help='Output file for hash result')
def highhash(text, file, iterations, output):
    """Run high_hash on text or file."""
    input_text = get_input_text(text, file)
    result = core_high_hash(input_text, iterations)
    handle_output(f"high_hash: {result}", output)

@cli.command()
@click.argument("text", required=False)
@click.option('--file', '-fi', 'file', type=click.Path(exists=True), help='Input file to hash')
@click.option("--iterations", default=7, help="Number of iterations")
@click.option('--output', '-out', 'output', type=click.Path(), help='Output file for hash result')
def hash2(text, file, iterations, output):
    """Run hash2 on text or file."""
    input_text = get_input_text(text, file)
    result = core_hash2(input_text, iterations)
    handle_output(f"hash2: {result}", output)

@cli.command()
@click.argument("text", required=False)
@click.option('--file', '-fi', 'file', type=click.Path(exists=True), help='Input file to hash')
@click.option("--iterations", default=7, help="Number of iterations")
@click.option('--output', '-out', 'output', type=click.Path(), help='Output file for hash result')
def hash2_high(text, file, iterations, output):
    """Run hash2_high on text or file."""
    input_text = get_input_text(text, file)
    result = core_hash2_high(input_text, iterations)
    handle_output(f"hash2_high: {result}", output)

if __name__ == "__main__":
    cli()