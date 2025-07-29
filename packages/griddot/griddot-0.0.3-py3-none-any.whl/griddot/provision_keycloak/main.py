import sys
import time
import requests
import urllib3


def provision_kc(url):
    print(f'Provisioning Keycloak at {url}...')

    # Disable warnings for self-signed certs
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Wait for keycloak to be up and running
    url = "https://localhost:8443"
    retries = 10
    while retries > 0:
        try:
            response = requests.get(url, verify=False)  # <-- skip SSL verification here
            if response.status_code == 200:
                print("Keycloak is up and running.")
                break  # exit loop if ready
            else:
                print(f"Keycloak is not ready yet. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Keycloak is not ready yet. Error: {e}")
        time.sleep(5)
        retries -= 1
    else:
        print("Keycloak did not start in time.")
        sys.exit(1)
