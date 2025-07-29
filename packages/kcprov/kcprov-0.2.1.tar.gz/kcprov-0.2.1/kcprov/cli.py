import click
from main import provision_kc


@click.group()
def cli():
    """Keycloak Provisioning CLI"""
    pass


@cli.command()
@click.option('--url', prompt='Keycloak URL', help='Keycloak server URL')
def provision(url):
    provision_kc(url)


def main():
    """Main entry point for the CLI"""
    cli()
