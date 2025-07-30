import os
import sys
import shutil
import click

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
DEFAULT_FILES = ['main.tf', 'variables.tf', 'locals.tf', 'outputs.tf']

@click.command()
@click.argument('backend', type=click.Choice(['aws', 'gcp', 'azure', 'local']))
@click.argument('dest', default='.')
def init(backend, dest):
    """Initialize a Terraform project with standard files and provider for BACKEND."""
    dest = os.path.abspath(dest)
    if not os.path.exists(dest):
        os.makedirs(dest)

    # Copy provider.tf
    src_provider = os.path.join(TEMPLATE_DIR, backend, 'provider.tf')
    dst_provider = os.path.join(dest, 'provider.tf')
    shutil.copyfile(src_provider, dst_provider)
    click.echo(f"Created provider.tf for {backend} in {dest}")

    # Copy variables.tf template
    src_vars = os.path.join(TEMPLATE_DIR, 'variables.tf')
    dst_vars = os.path.join(dest, 'variables.tf')
    shutil.copyfile(src_vars, dst_vars)
    click.echo(f"Created variables.tf in {dest}")

    # Create other standard files with sample content
    for fname in ['main.tf', 'locals.tf', 'outputs.tf']:
        path = os.path.join(dest, fname)
        if os.path.exists(path):
            click.echo(f"Skipped {fname}, already exists")
            continue
        with open(path, 'w') as f:
            if fname == 'main.tf':
                f.write(f"# Main Terraform configuration for {backend} backend\n")
            elif fname == 'locals.tf':
                f.write("# Local variables and common configurations\n")
            elif fname == 'outputs.tf':
                f.write("# Output values for the Terraform configuration\n")
        click.echo(f"Created {fname}")

    click.echo("\nTerraform initializer completed.")
    click.echo("\nNext steps:")
    click.echo("1. Review and update the provider configuration in provider.tf")
    click.echo("2. Update variables.tf with your specific values")
    click.echo("3. Add your infrastructure code to main.tf")
    click.echo("4. Run 'terraform init' to initialize the project")

if __name__ == '__main__':
    init()