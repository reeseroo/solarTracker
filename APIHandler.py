import http.client
import base64
import json
import time

ClientId = "d1de724b0f961cf0e9724e46b5ec1ebf"
ClientSecret = "4b2cdc848a81af46946dcba95fa46489"
API_KEY = "9f7588b091038f35d2073cba2eb56fdb"
unique_access_token = ""
refresh_token = ""
system_id = "3821083"

# Function to read tokens from file
def read_tokens_from_file():
    global unique_access_token, refresh_token
    try:
        with open("keys.txt", "r") as file:
            lines = file.readlines()
            unique_access_token = lines[0].strip().split("=")[1]
            refresh_token = lines[1].strip().split("=")[1]
            system_id = lines[2].strip().split("=")[1]
    except FileNotFoundError:
        print("File not found. Tokens not read.")

# Function to write tokens to file
def write_tokens_to_file():
    global unique_access_token, refresh_token
    with open("keys.txt", "w") as file:
        file.write(f"unique_access_token={unique_access_token}\n")
        file.write(f"refresh_token={refresh_token}\n")
        file.write(f"system_id={system_id}\n")

read_tokens_from_file()

def get_access_token_and_refresh_token():
    global unique_access_token, refresh_token
    auth_str = f"{ClientId}:{ClientSecret}"
    base64_auth_str = base64.b64encode(auth_str.encode()).decode()

    conn = http.client.HTTPSConnection("api.enphaseenergy.com")
    payload = ''
    headers = {
        'Authorization': f'Basic {base64_auth_str}'
    }
    request_url = f"/oauth/token?grant_type=authorization_code&redirect_uri=https://api.enphaseenergy.com/oauth/redirect_uri&code={unique_access_token}"
    print(request_url)
    conn.request("POST", request_url, payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    conn.close()

    response = json.loads(data.decode("utf-8"))
    if res.status != 200:
        print("Error: " + response["error"])
        return
    unique_access_token = response.get("access_token", "")
    refresh_token = response.get("refresh_token", "")
    write_tokens_to_file()

def new_tokens():
    global unique_access_token, refresh_token
    auth_str = f"{ClientId}:{ClientSecret}"
    base64_auth_str = base64.b64encode(auth_str.encode()).decode()

    conn = http.client.HTTPSConnection("api.enphaseenergy.com")
    payload = ''
    headers = {
        'Authorization': f'Basic {base64_auth_str}'
    }
    request_url = f"/oauth/token?grant_type=refresh_token&refresh_token={refresh_token}"
    print(request_url)
    conn.request("POST", request_url, payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    conn.close()
    response = json.loads(data.decode("utf-8"))
    if res.status != 200:
        print("Error: " + json.dumps(response))
        return
    unique_access_token = response.get("access_token", "")
    refresh_token = response.get("refresh_token", "")
    write_tokens_to_file()


def get_systems():
    global system_id
    conn = http.client.HTTPSConnection("api.enphaseenergy.com")
    payload = ''
    headers = {
        'Authorization': f'Bearer {unique_access_token}'
    }
    conn.request("GET", f"/api/v4/systems?key={API_KEY}", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    conn.close()
    response = json.loads(data.decode("utf-8"))
    if res.status != 200:
        print("Error: " + response["error"])
        return
    system_id = response["systems"][0]["system_id"]
    write_tokens_to_file()


def get_system_summary():
    conn = http.client.HTTPSConnection("api.enphaseenergy.com")
    payload = ''
    headers = {
        'Authorization': f'Bearer {unique_access_token}'
    }
    conn.request("GET", f"/api/v4/systems/{system_id}/summary?key={API_KEY}", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    conn.close()
    response = json.loads(data.decode("utf-8"))
    print(response)
    if res.status != 200:
        print("Error: " + response["error"])
        return
    return response.get("current_power")

def get_name():
    conn = http.client.HTTPSConnection("api.enphaseenergy.com")
    payload = ''
    print(f"/api/v4/systems?key={API_KEY}/{system_id}")
    print(API_KEY)
    print(system_id)
    headers = {
        'Authorization': f'Bearer {unique_access_token}'
    }
    conn.request("GET", f"/api/v4/systems/{system_id}?key={API_KEY}", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    conn.close()
    response = json.loads(data.decode("utf-8"))
    if res.status != 200:
        print("Error: " + response["error"])
        return
    return response.get("name")




def get_system_consumption():
    conn = http.client.HTTPSConnection("api.enphaseenergy.com")
    payload = ''
    headers = {
        'Authorization': f'Bearer {unique_access_token}'
    }
    conn.request("GET", f"/api/v4/systems/{system_id}/telemetry/consumption_meter?key={API_KEY}", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    conn.close()
    response = json.loads(data.decode("utf-8"))
    if res.status != 200:
        print("Error: " + response["error"])
        return
    print(response["intervals"][0]["enwh"])

def grid_export_data():
    granularity = "5mins"
    start_at = int(time.time())
    end_at = int(time.time())
    conn = http.client.HTTPSConnection("api.enphaseenergy.com")
    payload = ''
    headers = {
        'Authorization': f'Bearer {unique_access_token}'
    }
    conn.request("GET", f"/api/v4/systems/{system_id}/energy_export_telemetry?start_at{start_at}&key={API_KEY}", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    conn.close()
    response = json.loads(data.decode("utf-8"))
    if res.status != 200:
        print("Error: " + response["error"])
        return
    print(response)
    print(response["intervals"][0][0]["wh_exported"])

def latest_telemetry():
    conn = http.client.HTTPSConnection("api.enphaseenergy.com")
    payload = ''
    headers = {
        'Authorization': f'Bearer {unique_access_token}'
    }
    conn.request("GET", f"/api/v4/systems/{system_id}/latest_telemetry?key={API_KEY}", payload, headers)
    res = conn.getresponse()
    data = res.read()
    #print(data.decode("utf-8"))
    conn.close()
    response = json.loads(data.decode("utf-8"))
    if res.status != 200:
        print("Error: " + json.dumps(response))
        return
    #print(response)
    total_production = 0
    total_consumption = 0

    # Loop through the meters in the devices
    for meter in response['devices']['meters']:
        if meter['name'] == 'production' and meter['power'] != None:
            total_production += meter['power']
            #print(total_production)
        elif meter['name'] == 'consumption' and meter['power'] != None:
            total_consumption += meter['power']
           # print(total_consumption)

    # Calculate net production (production - consumption)
    net_production = total_production - total_consumption

    #print("Total Production:", total_production)
    #print("Total Consumption:", total_consumption)
    #print("Net Production:", net_production)
    return net_production
