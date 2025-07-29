import sys
import time
import requests
import urllib3

# Disable warnings for self-signed certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def provision_kc(url):
    print(f'Provisioning Keycloak at {url}...')
    wait_for_keycloak_to_start(url)


def wait_for_keycloak_to_start(url):
    retries = 10
    while retries > 0:
        try:
            response = requests.get(url, verify=False)
            if response.status_code == 200:
                print("Keycloak is up and running.", flush=True)
                break
            else:
                print(f"Keycloak is not ready yet. Status code: {response.status_code}")
        except requests.exceptions.RequestException:
            print(f"Keycloak is not ready yet ...", flush=True)
        time.sleep(5)
        retries -= 1
    else:
        print("Keycloak did not start in time.", flush=True)
        sys.exit(1)
