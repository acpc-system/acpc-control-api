#!/bin/bash 
###API that get the dhcp options config files  
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
FILE="/acpc/adm/etc/dhcp/dhcpd.conf.options"
echo "Content-type: application/json"
echo ""
isExist "${FILE}"
[ ${?} -ne 0 ] && genError 412 "subnet file not exist" 7
isRead "${FILE}"
[ ${?} -ne 0 ] && genError 413 "subnet file has no read permission" 8

OPTIONS=$(cat ${FILE})
initResponse
startJSON
DATA=""
CO=1
while read LINEt
do
	LINE=$(echo "${LINEt}" | sed  's/"/\\\"/g')
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
