#!/bin/bash 
###API that counts the number of hosts type dhcpd.hosts file
### Accept one parameter "type", the host type
#### Exit codes
##	0: Success
##	1: Insufficient parameters
##	2: Invalid Host type
##	3: dhcpd.hosts is not exists
##	4: dhcpd.hosts is not readable
##	5: Generic Error 
source create-json.sh
source common.sh
source checkers.sh
GETTYPE=$(parseQueryString ${QUERY_STRING} "type")
FILE="/acpc/adm/etc/dhcp/dhcpd.conf.hosts"
echo "Content-type: application/json"
echo ""
initResponse
startJSON
[ -z ${GETTYPE} ] && genError 100 "Insufficient parameter " 1
checkHosttype "${GETTYPE}"
[ ${?} -ne 0 ] && genError 101 "Invalid ACPC Host type" 2
RC=0
[ ! -f ${FILE} ] && genError 401 "dhcpd hosts file not exist" 3
[ ! -r ${FILE} ] && genError 402 "dhcpd hosts file has no read permission"  4
PATTERN="^host *${GETTYPE}[0-9]*"
N=$(grep -c "${PATTERN}" ${FILE})
if [ ${?} -eq 0 ] || [ ${?} -eq 1 ]
then
	insertJSON "status_code" I "200"
	insertJSON "status_message" S "ok" 
	insertJSON "response" S "${N}" L
else
	genError 403 "Generic error reading the file" 5
fi
closeJSON
printJSON
exit 0
