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
##	7: subnet config file isnot found
##	8: Subnet config file has no read permission
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
isExist "${FILE}"
[ ${?} -ne 0 ] && genError 412 "subnet file not exist" 7
isRead "${FILE}"
[ ${?} -ne 0 ] && genError 413 "subnet file has no read permission" 8
FULLMASK=$(getSubnet ${GETMASK})
FLAG=$(grep -c "^ *subnet *${GETNET} *netmask *${FULLMASK} *{" ${FILE})
[ ${FLAG} -eq 0 ] && genError 411 "No defined subnet: ${COMMAND}" 6

SUBNET=$(cat ${FILE})
initResponse
startJSON
FILE="${FILE}"
isExist "${FILE}"
[ ${?} -ne 0 ] && genError 103 "DHCP subnets configuration is not exit" 4
isRead "${FILE}"
[ ${?} -ne 0 ] && genError 102 "DHCP subnets configuraiton has no read permission" 3

STARTLINE=$(grep -n "^ *subnet ${GETNET} *netmask *${FULLMASK} *{" ${FILE}| cut -f1 -d:)
ENDLINE=$(tail -n +${STARTLINE} ${FILE} | grep -n "}" | tail -1 | cut -f1 -d:)
ENDLINE=$[STARTLINE+ENDLINE-1]
TMPFILE=$(mktemp)
sed -n ${STARTLINE},${ENDLINE}p ${FILE} > ${TMPFILE}
DATA=""
CO=1
while read LINE
do
	if [ ${CO} -eq 1 ]
	then
		DATA="\"${LINE}\""
		CO=2
	else
		DATA="${DATA},\"${LINE}\""
	fi
done < ${TMPFILE}
rm ${TMPFILE}
insertJSON "status_code" I "200"
insertJSON "status_message" S "ok" 
insertJSON "response" A "${DATA}" L
closeJSON
printJSON
exit 0
