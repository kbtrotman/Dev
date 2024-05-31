import sys
import getopt

import requests
import json
##########################
##   Connection Vars    ##
##########################
protocol = "https"
nbmaster = "phx-nbkup-lt001.internal.salesforce.com"
apikey = "A9kdXLmwkG1P4Mxg0P38aOMlNvAw3boGd8X8h-5LCp3_7cwCJbSWIDMXz0xg2RmY"
base_url = protocol + "://" + nbmaster + ":" + "/netbackup"

##########################
##       API Vars       ##
##########################
content_type = "application/vnd.netbackup+json; version=2.0"
ClientName = ""
PolicyName = ""
ScheduleName = ""
etag = ""

##########################
##   Command-line Vars  ##
##########################
# Options
options = "hc:p:s:"
# Long options
long_options = ["help", "client", "polName", "schedule"]
# Remove 1st argument from the
# list of command line arguments
argumentList = sys.argv[1:]


try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)

    # check each argument
    for currentArgument, currentValue in arguments:

        if currentArgument in ("-h", "--Help"):
            send_log("netbackup_AutomationAdd Usage:")
            send_log("     -h or --help:      Displays this message")
            send_log("     -c or --client:    Client name to add to policy.")
            send_log("     -p or --polName:   Requires a policy name. Reports on all backups mmade fom that policy.")
            send_log("     -s or --schedule:  Name of schedule: full or incr, Application Backup, or empty for VMWare")

        elif currentArgument in ("-c", "--client"):
            ClientName = currentValue
            send_log("Set client name to [" + ClientName + "] [" + currentValue + "]")

        elif currentArgument in ("-s", "--schedule"):
            ScheduleName = currentValue
            send_log("Set schedule name to [" + ScheduleName + "] [" + currentValue + "]")

        elif currentArgument in ("-p", "--polName"):
                PolicyName = currentValue

        else:
                send_log("Incorrectly defined policy type in input: [" + currentValue + "]. Please correct and try again")
                exit()
    send_log("Requesting report with Policy Name [" + PolicyName + "] with Client [" + ClientName + "] and Schedule [" + ScheduleName + "] to Netbackup.")
    resp = post_netbackup_VMwarePolicy_defaults(apikey, base_url)

except getopt.error as err:
    # output error, and return with an error code
    send_log(str(err))
