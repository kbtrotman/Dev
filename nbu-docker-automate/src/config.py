
##   API connections Constants
PROTOCOL = "https"
NB_MASTER = "phx-nbkup"
API_KEY = "A9kdXLmwkG1P4Mxg0P38aOMlNvAw3boGd8X8h-5LCp3_7cwCJbSWIDMXz0xg2RmY"
BASE_URL = PROTOCOL + "://" + NB_MASTER + "/netbackup"
CONTENT_TYPE = "application/vnd.netbackup+json; version=2.0"
# match the prod policy names
VMARE_POLICY_NAME = "VMware_test_policy"
ORACLE_POLICY_NAME = "Oracle_test_policy"
FS_POLICY_NAME = "Filesystem_test_policy"
NAS_POLICY_NAME = "NAS_test_policy"

#   SQL GLOBAL CONSTANTS
SERVER_NAME = 'tcp:PHX-SQLDB'
DATABASE = 'Storage_Automation'
USER_NAME = 'storage_user'
PASSWORD = 'NmUXTm74zR42iJ96'

LOG_PATH = "/var/log/dpass-automation/"
LOG_FILENAME = "netbackup-workflows.log"

#  Command-line Args
LONG_OPTIONS = ['-client', '-ip', '-serialnum', '-requestor', '-pol', '-schedule', '-sox']
LONG_DESC = ['Client to be added.',
                'IP of client to be added.',
                'Serial Number of client.',
                'Requestors login ID.',
                'Policy type to be added to NBU.',
                'Schedule to be added to NBU.',
                'Boolean, is this sox data, 0 or 1 (True or False).'
                ]
