#!/bin/bash 
###API that list the (dhcp different config files ) 
##Parameters:
##	type: which config file (hosts, subnet, and options)
#### Exit codes
##	0: Success
##	1: Not enough parameters
##	2: Invalid dhcp config extension
##	3: DHCP configuraiton extension is not found
##	4: DHCP configuraiton extension has no read permission

source checkers.sh
source create-json.sh
source common.sh
FILE="/acpc/adm/etc/dhcp/dhcpd.conf"
echo "Content-type: application/json"
echo ""
GETTYPE=$(parseQueryString ${QUERY_STRING} "type")
[ -z ${GETTYPE} ] && genError 100 "Insufficient parameter " 1
initResponse
startJSON
checkDHCPconf ${GETTYPE}
[ ${?} -ne 0 ] && genError 101 "Invalid DHCP configuration extension " 2
FILE="${FILE}.${GETTYPE}"
isExist "${FILE}"
[ ${?} -ne 0 ] && genError 103 "DHCP Configuration extension is not found" 3
isRead "${FILE}"
[ ${?} -ne 0 ] && genError 104 "DHCP Configuration extension is has no read permission" 4
DATA=""
CO=1
while read LINE
do
	LINE=$(echo "${LINE}" | sed  's/"/\\\"/g')
        if [ ${CO} -eq 1 ]
        then
                DATA="\"${LINE}\""
                CO=2
        else
                DATA="${DATA},\"${LINE}\""
        fi
done < ${FILE}
insertJSON "status_code" I "200"
insertJSON "status_message" S "ok" 
insertJSON "response" A "${DATA}" L
closeJSON
printJSON
exit 0
