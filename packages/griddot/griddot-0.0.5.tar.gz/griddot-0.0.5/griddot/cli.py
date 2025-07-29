import click
from griddot.provision_keycloak import provision_keycloak


@click.group()
def cli():
    """CLI for GridDot platform tools"""
    pass


@cli.command("provision-keycloak")
@click.option('--url', help='Keycloak server URL', default='https://localhost:8443')
def provision(url="https://localhost:8443"):
    """Provision Keycloak with the given URL."""
    provision_keycloak(url)


@cli.command("generate-password")
@click.option('--lenght', help='Password lenght', default='32')
@click.option('--use-special', help='Use special characters', is_flag=True, default=False)
def provision(length=32, use_special=False):
    """Random password generator"""
    import random
    import string

    characters = string.ascii_letters + string.digits
    if use_special:
        characters += string.punctuation

    password = ''.join(random.choice(characters) for i in range(length))
    print(password)
    return password
