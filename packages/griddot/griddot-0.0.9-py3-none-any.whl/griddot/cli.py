import click
from griddot.provision_keycloak import provision_keycloak, ADMIN_USERNAME, DEFAULT_URL


@click.group()
def cli():
    """CLI for GridDot platform tools"""
    pass


@cli.command("provision-keycloak")
@click.option('--realm-json-path', help='Path to realm JSON file')
@click.option('--password', help='Username password')
@click.option('--username', help='User name')
@click.option('--url', help='Keycloak server URL')
def provision(realm_json_path, password, username=ADMIN_USERNAME, url=DEFAULT_URL):
    """Keycloak provisioning tool"""
    provision_keycloak(realm_json_path, password, username, url)
