import json
import sys
import time
import requests
import urllib3

# Disable warnings for self-signed certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ADMIN_USERNAME = "temp-admin"
DEFAULT_URL = "https://localhost:8443"


def provision_keycloak(
        realm_json_path: str,
        password: str,
        username: str = ADMIN_USERNAME,
        url: str = DEFAULT_URL
):
    print(f'Provisioning Keycloak at {url}')
    wait_for_keycloak_to_start(url)

    token = get_access_token(url, username, password)
    realm = json.load(open(realm_json_path, "r", encoding="utf-8"))
    import_realm_users_if_they_dont_exist(url, token, realm)


def wait_for_keycloak_to_start(url):
    max_retries = 60
    retries = max_retries
    while retries > 0:
        try:
            response = requests.get(url, verify=False)
            print()
            if response.status_code == 200:
                print("Keycloak is up and running.", flush=True)
                break
            else:
                print(f"Keycloak is not ready yet. Status code: {response.status_code}")
        except requests.exceptions.RequestException:
            if retries == max_retries:
                print(f"Keycloak is not ready yet .", end="", flush=True)
            else:
                print(".", end="", flush=True)
        time.sleep(1)
        retries -= 1
    else:
        print("Keycloak did not start in time.", flush=True)
        sys.exit(1)


def get_access_token(url, username, password):
    token_url = f"{url}/realms/master/protocol/openid-connect/token"
    data = {
        "client_id": "admin-cli",
        "username": username,
        "password": password,
        "grant_type": "password"
    }
    response = requests.post(token_url, data=data, verify=False)
    if response.status_code != 200:
        print("Failed to get access token:", response.text)
        sys.exit(1)
    return response.json()["access_token"]


def import_realm_users_if_they_dont_exist(url, token, realm):
    users_url = f"{url}/admin/realms/master/users"
    user_credentials_url = lambda user_id: f"{url}/admin/realms/master/users/{user_id}/credentials"
    users = realm["users"]

    for user in users:
        # Check if the user already exists
        response = requests.get(users_url, headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }, params={"username": user["username"]}, verify=False)

        payload = response.json()
        user_id = payload[0]["id"] if len(payload) > 0 else None

        credentials_response = requests.get(user_credentials_url(user_id), headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }, verify=False)

        has_user_password = len(credentials_response.json()) > 0

        if response.status_code != 200 and not len(response.json()) > 0:
            create_response = requests.post(users_url, headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }, data=json.dumps(user), verify=False)

            if create_response.status_code == 201:
                print(f"User {user['username']} created successfully.")
            else:
                print(f"Failed to create user {user['username']}: {create_response.text}")
                continue

        if not has_user_password:
            send_email_for_password_setup(url, "master", token, user_id, user["email"])

    admin_user_id = next(u for u in users if u["username"] == ADMIN_USERNAME)["id"]
    delete_user(url, "master", token, admin_user_id)


def delete_user(url, realm, token, user_id):
    delete_url = url = f"{url}/admin/realms/{realm}/users/{user_id}"
    response = requests.delete(
        delete_url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        verify=False  # Set to True if using a valid SSL cert
    )

    # Handle response
    if response.status_code == 204:
        print(f"User {user_id} deleted successfully.")
    else:
        print(f"Failed to delete user: {response.status_code} {response.text}")


def send_email_for_password_setup(url, realm, token, user_id, user_mail):
    send_email_url = f"{url}/admin/realms/{realm}/users/{user_id}/execute-actions-email"
    send_email_response = requests.put(send_email_url,
                                       headers={
                                           "Authorization": f"Bearer {token}",
                                           "Content-Type": "application/json"
                                       },
                                       params={
                                           "lifespan": 3600 * 24 * 7,
                                           "client_id": "account-console",
                                       },
                                       data=json.dumps(["UPDATE_PASSWORD"]),
                                       verify=False)

    if send_email_response.status_code == 204:
        print(f"Email sent to {user_mail} for password setup.")
    else:
        print(f"Failed to send email to {user_mail}: {send_email_response.text}")
