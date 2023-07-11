#!/bin/bash 
###API that reset the (dhcp different config files ) remove all its content) 
##Parameters:
##	type: which config file (hosts, subnet, and options)
#### Exit codes
##	0: Success
##	1: Not enough parameters
##	2: Invalid dhcp config extension
##	3: DHCP configuraiton extension has no write permission
##	4: Can not create DHCP configuration file

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
if [ ${?} -eq 0 ]
then
	isWrite "${FILE}"
	[ ${?} -ne 0 ] && genError 102 "DHCP configuraiton extension has no write permission" 3
	rm ${FILE}
fi
touch ${FILE}
[ ${?} -ne 0 ] && genError 103 "Can not create DHCP configuration file" 4

insertJSON "status_code" I "200"
insertJSON "status_message" S "ok" 
insertJSON "response" S "RESET" L
closeJSON
printJSON
exit 0
