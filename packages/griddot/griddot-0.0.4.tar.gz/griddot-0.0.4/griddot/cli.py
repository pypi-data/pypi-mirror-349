import click
from griddot.provision_keycloak import provision_kc


@click.group()
def cli():
    """CLI for GridDot platform tools"""
    pass


@cli.command("provision-keycloak")
@click.option('--url', help='Keycloak server URL', default='https://localhost:8443')
def provision(url="https://localhost:8443"):
    """Provision Keycloak with the given URL."""
    provision_kc(url)
