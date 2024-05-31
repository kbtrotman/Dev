import requests
import debug_logging_top_level


def post_add_client(pol_name, client_name, apikey, base_url, req_json, cont_type):
    url = f"{base_url}/config/policies/{pol_name}/clients/{client_name}"
    debug_logging_top_level.send_log(f"Posting to url {url}")

    headers = {'Content-Type': cont_type, 'Authorization': apikey}

    debug_logging_top_level.send_log("\nMaking POST Request to create policy with defaults \n")
    debug_logging_top_level.send_log(f"JSON PACKET = /n{str(req_json)}")
    resp = requests.put(url, headers=headers, json=req_json, verify=False)

    if resp.status_code != 201:
        debug_logging_top_level.send_log(f"\nPolicy post is created with status code : {resp.status_code} \n")
    return resp


def post_policy_add(apikey, base_url, req_json, cont_type):
    url = f"{base_url}/config/policies/"
    debug_logging_top_level.send_log(f"Posting to url {url}")

    headers = {'Content-Type': cont_type, 'Authorization': apikey}

    debug_logging_top_level.send_log("\nMaking POST Request to create policy with defaults \n")
    debug_logging_top_level.send_log(f"JSON PACKET = /n{str(req_json)}")
    resp = requests.post(url, headers=headers, json=req_json, verify=False)

    if resp.status_code != 204:
        debug_logging_top_level.send_log(f"Create Policy API with defaults failed with status code {resp.status_code} and json {resp.json() } \n")
        debug_logging_top_level.send_log(f"\nPolicy post is created with status code : {resp.status_code}\n")
    return resp


def delete_policy(pol_name, apikey, base_url, req_json, cont_type):
    url = f"{base_url}/config/policies/{pol_name}/backupselections"
    debug_logging_top_level.send_log(f"Posting to url {url}")

    headers = {'Content-Type': cont_type, 'Authorization': apikey, 'X-NetBackup-Policy-Use-Generic-Schema': 'True'}

    debug_logging_top_level.send_log("\nMaking POST Request to create policy with defaults \n")
    resp = requests.delete(url, headers=headers, json=req_json, verify=False)

    if resp.status_code != 204:
        debug_logging_top_level.send_log(f"Delete Policy API with defaults failed with status code {resp.status_code} and json {resp.json()}")
        debug_logging_top_level.send_log(f"\nPolicy delete is completed with status code : {resp.status_code}\n")
    return resp


def delete_client(pol_name, cl_name, apikey, base_url, cont_type):
    url = f"{base_url}/config/policies/{pol_name}/clients/{cl_name}"
    debug_logging_top_level.send_log(f"Posting to url {url}")

    headers = {'Content-Type': cont_type, 'Authorization': apikey}

    debug_logging_top_level.send_log("\nMaking POST Request to create policy with defaults \n")
    resp = requests.delete(url, headers=headers, verify=False)

    if resp.status_code != 204:
        debug_logging_top_level.send_log(f"Delete client API with defaults failed with status code {resp.status_code} and json {resp.json()}\n")
        debug_logging_top_level.send_log(f"\nClient delete is completed with status code : {resp.status_code}\n")
    return resp