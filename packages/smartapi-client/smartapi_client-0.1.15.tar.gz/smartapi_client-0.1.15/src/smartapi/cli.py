import click
import os
from smartapi.api_client import ApiClient


@click.command()
@click.option('--input', '-i', required=True, help='Input file path')
@click.option('--type', '-t', 'input_type', required=True,
              type=click.Choice(['postman', 'openapi', 'config']),
              help='Input type (postman/openapi/config)')
@click.option('--output', '-o', required=True, help='Output file path (e.g. endpoints.json or endpoints.yaml)')
@click.option('--base-url', '-b', required=False, help='Base URL for the API')
@click.option('--api-name', '-n', default='UnnamedAPI', help='Optional name for the API')
@click.option('--format', '-f', default='json', type=click.Choice(['json', 'yaml']), help='Output format')
def generate(input, input_type, output, base_url, api_name, format):
    outdir = os.path.dirname(output) or '.'
    filename = os.path.basename(output)
    os.makedirs(outdir, exist_ok=True)

    if input_type == 'postman':
        ApiClient.from_postman_collection(
            collection_path=input,
            base_url=base_url or "base_url",
            api_name=api_name,
            save_endpoints=True,
            path=outdir,
            file_name=filename,
            output_format=format
        )
        click.secho(f"✅ Saved to {output}", fg="green")
    elif input_type == 'openapi':
        ApiClient.from_openapi_spec(
            spec_path=input,
            base_url=base_url or "base_url",
            api_name=api_name,
            save_endpoints=True,
            path=outdir,
            file_name=filename,
            output_format=format
        )
        click.secho(f"✅ Saved to {output}", fg="green")
    else:
        click.secho(f"❌ Type '{input_type}' not yet supported.", fg="red")


if __name__ == '__main__':
    generate()
