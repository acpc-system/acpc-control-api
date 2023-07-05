#!/bin/bash
###API that returns a mac address for certain team from /acpc/adm/etc/dhcp/dhcpd.conf.hosts
##	The API uses GET method, and accept id parameters 
#### Exit codes
##	0: Success
##	1: Insufficient parameter
##	2: ID is not an integer
##	3: dhcp hosts file does not exist
##	4: dhcp hosts file does not have read permission
##	5: team is not valid (not exists in dhcpd.conf.hosts)
source create-json.sh
source common.sh
source checkers.sh
source macops.sh
GETID=$(parseQueryString ${QUERY_STRING} "id")
FILE="/acpc/adm/etc/dhcp/dhcpd.conf.hosts"
echo "Content-type: application/json"
echo ""
initResponse
startJSON
[ -z ${GETID} ] && genError 100 "Insufficient parameter " 1
checkInteger ${GETID}
[ ${?} -ne 0 ] && genError 101 "team ID is not an integer :${GETID}" 2
[ ! -f ${FILE} ] && genError 401 "dhcp hosts file not exist" 3
[ ! -r ${FILE} ] && genError 402 "dhcp hosts  file has no read permission"  4
MAC=$(getMAC "team${GETID}")
RET=${?}
[ ${RET} -eq 1 ] && genError 403 "Host not found" 5
insertJSON "status_code" I "200"
insertJSON "status_message" S "ok" 
insertJSON "response" S "hostmac, ${MAC}" L
closeJSON
printJSON
exit 0
