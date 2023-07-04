#!/bin/bash
###API that set a mac address for certain team from /acpc/adm/etc/dhcp/dhcpd.conf.hosts
##	The API uses POST method, and accept id parameter
#### Exit codes
##	0: Success
##	1: Insufficient parameter
##	2: ID is not an integer
##	3: dhcp hosts file does not exist
##	4: dhcp hosts file does not have read permission
##	5: dhcp hosts file does not have write permission
##	6: team is not valid (not exists in dhcpd.conf.hosts)
##	7: passed mac address is not a valid mac
##	8: Error in replace operation
source create-json.sh
source common.sh
source checkers.sh
GETID=$(parseQueryString ${QUERY_STRING} "id")
FILE="/acpc/adm/etc/dhcp/dhcpd.conf.hosts"
echo "Content-type: application/json"
echo ""
initResponse
startJSON
[ -z ${GETID} ] && genError 100 "Insufficient parameter " 1
checkInteger ${GETID}
[ ${?} -ne 0 ] && genError 101 "team ID is not an integer :${GETID}" 2

###
### Extract mac address from POST body
POSTMAC=$(parseQueryString ${QUERY_STRING} "mac")
### Check for mac address
checkMAC ${POSTMAC}
[ ${?} -ne 0 ] && genError 101 "team ID is not a valid MAC Address :${POSTMAC}" 7

[ ! -f ${FILE} ] && genError 401 "dhcp hosts file not exist" 3
[ ! -r ${FILE} ] && genError 402 "dhcp hosts file has no read permission"  4
[ ! -w ${FILE} ] && genError 402 "dhcp hosts file has no write permission"  5
##1-Get the line number contains the pattern host team{id}
LINEN=$(grep -n "^host *team${GETID} " ${FILE} | cut -d: -f1)
[ -z ${LINEN} ] && genError 403 "team ${GETID} is not valid"  6
## Now, we have the line number grep the line contains mac address after this line
MAC=$(tail -n +15 ${FILE} |grep "hardware ethernet" | head -1 | awk ' { print $3 }'| sed 's/;//g')
### Here replace the old mac with new mac in the dhcpd.conf.hosts file
touch /tmp/DATA
sed -i ${FILE} "s/${MAC}/${POSTMAC}/g" 
[ ${?} -ne 0 ] && genError 404 "Error!! replace ${MAC} with ${POSTMAC} in ${FILE}"  8

insertJSON "status_code" I "200"
insertJSON "status_message" S "ok" 
insertJSON "response" S "${MAC}" L
closeJSON
printJSON
exit 0
