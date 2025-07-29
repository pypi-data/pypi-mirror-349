import click


@click.group()
def cli():
    """Keycloak Provisioning CLI"""
    pass


@cli.command()
@click.option('--url', prompt='Keycloak URL', help='Keycloak server URL')
def provision(url):
    provision_kc(url)


def provision_kc(url):
    print(f'Provisioning Keycloak at {url}...')
