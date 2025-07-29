﻿import click
from griddot.provision_keycloak import provision_keycloak, DEFAULT_USERNAME, DEFAULT_URL


@click.group()
def cli():
    """CLI for GridDot platform tools"""
    pass


@cli.command("provision-keycloak")
@click.option('--realm-json-path', help='Path to realm JSON file')
@click.option('--password', help='Username password')
@click.option('--username', help='User name')
@click.option('--url', help='Keycloak server URL')
def provision(realm_json_path, password, username=DEFAULT_USERNAME, url=DEFAULT_URL):
    """Provision Keycloak with the given URL."""
    provision_keycloak(realm_json_path, password, username, url)
