#!/bin/bash 
###API that get the dhcp subnet config files  
###Parameters:
##	net: Network ID
##	mask mask as an integer 
#### Exit codes
##	0: Success
##	1: Not enough parameters
##	2: Invalid IP 
##	3: Not an integer
##	4: mask must be <=32
##	5: invalid subnet range
##	6: Not defined subnet
source checkers.sh
source create-json.sh
source common.sh
FILE="/acpc/adm/etc/dhcp/dhcpd.conf.subnet"
echo "Content-type: application/json"
echo ""
GETNET=$(parseQueryString ${QUERY_STRING} "net")
[ -z ${GETNET} ] && genError 100 "Insufficient parameter net " 1
GETMASK=$(parseQueryString ${QUERY_STRING} "mask")
[ -z ${GETMASK} ] && genError 100 "Insufficient parameter mask" 1
checkIP "${GETNET}"
[ ${?} -ne 0 ] && genError 408 "Invalid IP Address format" 2
checkInteger "${GETMASK}"
[ ${?} -ne 0 ] && genError 409 "Invalid Integer" 3
[ ${GETMASK} -gt 32 ] && genError 410 "Invalid subnet mask, must be <= 32" 4
checkSubnet "${GETNET}" "${GETMASK}"
[ ${?} -ne 0 ] && genError 411 "Invalid subnet range" 5
FULLMASK=$(getSubnet ${GETMASK})
FLAG=$(grep -c "^ *subnet *${GETNET} *netmask *${FULLMASK} *{" ${FILE})
[ ${FLAG} -eq 0 ] && genError 411 "No defined subnet: ${COMMAND}" 6


initResponse
startJSON
FILE="${FILE}"
isExist "${FILE}"
[ ${?} -ne 0 ] && genError 103 "DHCP subnets configuration is not exit" 4
isRead "${FILE}"
[ ${?} -ne 0 ] && genError 102 "DHCP subnets configuraiton has no read permission" 3
DATA=$(cat "${FILE}")
insertJSON "status_code" I "200"
insertJSON "status_message" S "ok" 
insertJSON "response" S "${GETNET}/${GETMASK} ${FULLMASK}" L
closeJSON
printJSON
exit 0
