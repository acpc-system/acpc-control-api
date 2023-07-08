#!/bin/bash 
###API that returns the state (live or dead) for a certain host
### Accept one parameter "type", the host type, and host id with parameter id
#### Exit codes
##	0: Success
##	1: Insufficient parameters
##	2: Invalid Host type
##	3: ID is not an integer
##	4: Can not resolve the hostname
source create-json.sh
source common.sh
source checkers.sh
source hostops.sh
source pingutil.sh
GETTYPE=$(parseQueryString ${QUERY_STRING} "type")
GETID=$(parseQueryString ${QUERY_STRING} "id")
FILE="/acpc/adm/etc/dhcp/dhcpd.conf.hosts"
echo "Content-type: application/json"
echo ""
initResponse
startJSON
[ -z ${GETTYPE} ] && genError 100 "Insufficient parameter " 1
checkHosttype "${GETTYPE}"
[ ${?} -ne 0 ] && genError 101 "Invalid ACPC Host type" 2

[ -z ${GETID} ] && genError 100 "Insufficient parameter " 1
checkInteger "${GETID}"
[ ${?} -ne 0 ] && genError 101 "ID is not an integer" 3
HOST="${GETTYPE}${GETID}"
## Check the host name can be resolved to ip or no
checkHostname "${HOST}"
[ ${?} -ne 0 ] && genError 102 "Hostname ${HOST} can not be resolved" 4

checkHost "${HOST}"
[ ${?} -eq 0 ] && MSG="live" || MSG="dead"
insertJSON "status_code" I "200"
insertJSON "status_message" S "ok" 
insertJSON "response" S "${MSG}" L
closeJSON
printJSON
exit 0
