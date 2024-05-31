import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../dbconn/'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../debug/'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../lib/'))
import argparse

# Automation source imports
import config
import mssql_top_level_calls
import debug_logging_top_level
import nbu_api_top_level

##    Globals
client_name = ""
policy_name = ""
schedule_name = ""
ip = ""
serial = ""
req_id = ""
etag = ""
req_body=""
req_type = ""
sox = False
errcode = 0


##         Main         ##

try:
    # Parsing command-line arguments
    parser = argparse.ArgumentParser()
    for i in range(6):
        parser.add_argument(config.LONG_OPTIONS[i], type=str, help="'" + config.LONG_DESC[i] + "'")
        debug_logging_top_level.send_log(f"Added arg {config.LONG_OPTIONS[i]} at index {str(i)} to arguments list.")
    parser.add_argument(config.LONG_OPTIONS[6], type=bool, help="'" + config.LONG_DESC[6] + "'")
    debug_logging_top_level.send_log(f"Added arg {config.LONG_OPTIONS[6]} at index [6] to arguments list.")
    args = parser.parse_args()

    # check each argument
    if args.client:
        client_name = args.client
    if args.ip:
        ip = args.ip
    if args.serialnum:
        serial = args.serialnum
    if args.requestor:
        req_id = args.requestor
    if args.schedule:
        schedule_name = args.schedule
    if args.sox:
        sox = args.sox
        print("sox = " + str(sox))
    if args.pol:
        if args.pol == "Filesystem":
            policy_name = config.FS_POLICY_NAME
            req_type = "Standard"
        elif args.pol == "VMware":
            policy_name = config.VMARE_POLICY_NAME
            req_type = "VMware"
        elif args.pol == "Oracle":
            policy_name = config.ORACLE_POLICY_NAME
            req_type = "Oracle"
        else:
            debug_logging_top_level.send_log(f"Incorrectly defined policy type in input: {args.pol}. Please correct and try again")
            exit()

    if req_type == "Standard":
        # Then we only add a client to an existing policy. This will do Windows or UNIX backups as Standard, but at some point
        # we should also add support for a windows-only style filesystem backup here too.
        req_body = {
            "data": {
                "type": "client",
                "attributes": {
                    "hardware": "VMware",  #  Once Anthony has a front-end, this needs to be a drop-down.
                    "hostName": client_name,
                    "OS": "VMware"         #  Once Anthony has a front-end, this needs to be a drop-down.
                }
            }
        }

        debug_logging_top_level.send_log(f"Adding Standard client to policy {policy_name} with Client {client_name} and Schedule {schedule_name} to Netbackup.")
        nbu_api_top_level.post_add_client(policy_name, client_name, config.API_KEY, config.BASE_URL, req_body, config.CONTENT_TYPE)

    else:
        # The policies left now are NDMP and Oracle, and these need a full policy setup with standard default parameters.
        req_body = {
            "data": {
                "type": "policy",
                "id": policy_name,
                "attributes": {
                    "policy": {
                        "policyName": policy_name,
                        "policyType": req_type,
                        "policyAttributes": {},
                        "clients": [],
                        "schedules": [],
                        "backupSelections": {
                            "selections": []
                        }
                    }
                }
            }
        }
        debug_logging_top_level.send_log(f"Adding Policy {policy_name} with Client {client_name} and Schedule {schedule_name} to Netbackup.")
        nbu_api_top_level.post_policy_add(config.API_KEY, config.BASE_URL, req_body, config.CONTENT_TYPE)


    debug_logging_top_level.send_log(f"COMMITTING THESE VALUES: {client_name}, {ip}, {serial}, {req_id}, {str(sox)} ")
    mssql_top_level_calls.call_sql_commit_dp_Contacts(client_name, serial, req_id)

except argparse.ArgumentError as err:
    # output error, and return with an error code
    debug_logging_top_level.send_log(str(err))
