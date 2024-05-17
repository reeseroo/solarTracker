import http.client
import base64

ClientId = "d1de724b0f961cf0e9724e46b5ec1ebf"
API_KEY = "5d80c9af4f68a48296f257fc12f76066"
access_token = "HUNsCR"
unique_access_token = "change"
refresh_token = "change"
system_id = "change"

def get_access_token_and_refresh_token():
  auth_str = f"{ClientId}:{API_KEY}"
  base64_auth_str = base64.b64encode(auth_str.encode()).decode()

  conn = http.client.HTTPSConnection("api.enphaseenergy.com")
  payload = ''
  headers = {
    'Authorization': f'Basic {base64_auth_str}'
  }
  request_url = f"/oauth/token?grant_type=authorization_code&redirect_uri=https://api.enphaseenergy.com/oauth/redirect_uri&code={access_token}"
  print(request_url)
  conn.request("POST", request_url, payload, headers)
  res = conn.getresponse()
  data = res.read()
  print(data.decode("utf-8"))
  conn.close()

def new_tokens():
    auth_str = f"{ClientId}:{API_KEY}"
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

def get_systems():
    conn = http.client.HTTPSConnection("api.enphaseenergy.com")
    payload = ''
    headers = {
        'Authorization': f'Bearer {unique_access_token}'
    }
    conn.request("GET", "/api/v4/systems", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    conn.close()

def get_system_summary():
    conn = http.client.HTTPSConnection("api.enphaseenergy.com")
    payload = ''
    headers = {
        'Authorization': f'Bearer {unique_access_token}'
    }
    conn.request("GET", f"/api/v4/systems/{system_id}/summary", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    conn.close()

def get_system_consumption():
    conn = http.client.HTTPSConnection("api.enphaseenergy.com")
    payload = ''
    headers = {
        'Authorization': f'Bearer {unique_access_token}'
    }
    conn.request("GET", f"/api/v4/systems/{system_id}/consumption_lifetime", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    conn.close()