import requests
import json
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
KEYCLOAK_URL = "https://localhost:8443"
REALM_NAME = "master"
ADMIN_USERNAME = "temp-admin"
ADMIN_PASSWORD = "admin"
CLIENT_ID = "admin-cli"

# 1: Get an access token
token_url = f"{KEYCLOAK_URL}/realms/{REALM_NAME}/protocol/openid-connect/token"

token_response = requests.post(token_url, data={
    "client_id": CLIENT_ID,
    "username": ADMIN_USERNAME,
    "password": ADMIN_PASSWORD,
    "grant_type": "password"
}, verify=False)

if token_response.status_code != 200:
    print("Failed to get access token:", token_response.text)
    exit(1)

access_token = token_response.json()["access_token"]

# 2: Import master realm users
users_url = f"{KEYCLOAK_URL}/admin/realms/{REALM_NAME}/users"
# The users.json file should contain an array of user objects
with open("master-users.json", "r", encoding="utf-8") as f:
    users = json.load(f)

for user in users:
    # Check if the user already exists
    response = requests.get(users_url, headers={
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }, params={"username": user["username"]}, verify=False)

    if response.status_code == 200 and len(response.json()) > 0:
        print(f"User {user['username']} already exists. Skipping.")
        continue

    # Create the user
    create_response = requests.post(users_url, headers={
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }, data=json.dumps(user), verify=False)

    if create_response.status_code == 201:
        print(f"User {user['username']} created successfully.")
    else:
        print(f"Failed to create user {user['username']}: {create_response.text}")

    # Send e-mail to the user via keycloak for setting up password
