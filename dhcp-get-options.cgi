#!/bin/bash 
###API that get the dhcp options config files  
#### Exit codes
##	0: Success
##	1: Not enough parameters
##	2: Invalid dhcp config extension
##	3: DHCP configuraiton extension has no read permission
##	4: DHCP configuration extension is not exist

source checkers.sh
source create-json.sh
source common.sh
FILE="/acpc/adm/etc/dhcp/dhcpd.conf.options"
echo "Content-type: application/json"
echo ""
initResponse
startJSON
FILE="${FILE}"
isExist "${FILE}"
[ ${?} -ne 0 ] && genError 103 "DHCP options configuration is not exit" 4
isRead "${FILE}"
[ ${?} -ne 0 ] && genError 102 "DHCP options configuration has no read permission" 3
DATA=$(cat "${FILE}")
insertJSON "status_code" I "200"
insertJSON "status_message" S "ok" 
insertJSON "response" SJ "${DATA}" L
closeJSON
printJSON
exit 0
