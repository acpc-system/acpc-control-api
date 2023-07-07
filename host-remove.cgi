#!/bin/bash 
###API removes a host from dhcpd.hosts file
### Accept two parameters "id,type", 
#### Exit codes
##	0: Success
##	1: Insufficient parameters
##	2: Invalid Host type
##	3: dhcpd.hosts is not exists
##	4: dhcpd.hosts is not readable
##	5: Generic Error 
##	6: ID is not an integer
##	7: Host not exists
source create-json.sh
source common.sh
source checkers.sh
source hostops.sh
GETTYPE=$(parseQueryString ${QUERY_STRING} "type")
GETID=$(parseQueryString ${QUERY_STRING} "id")
FILE="/acpc/adm/etc/dhcp/dhcpd.conf.hosts"
echo "Content-type: application/json"
echo ""
initResponse
startJSON
[ -z ${GETTYPE} ] && genError 100 "Insufficient parameter " 1
[ -z ${GETID} ] && genError 100 "Insufficient parameter " 1
checkHosttype "${GETTYPE}"
[ ${?} -ne 0 ] && genError 101 "Invalid ACPC Host type" 2
checkInteger "${GETID}"
[ ${?} -ne 0 ] && genError 101 "ID is not an integer" 6
RC=0
[ ! -f ${FILE} ] && genError 401 "dhcpd hosts file not exist" 3
[ ! -r ${FILE} ] && genError 402 "dhcpd hosts file has no read permission"  4
LINES=$(getHost "${GETTYPE}${GETID}")
[ ${?} -ne 0 ] && genError 403 "Host is not found" 7
### Now, removing the lines from the file
STLINE=$(echo "${LINES}" | cut -d: -f1)
ENLINE=$(echo "${LINES}" | cut -d: -f2)
TMPFILE=$(mktemp)
cat ${FILE} | sed  "${STLINE},${ENLINE}d" > ${TMPFILE}
[ ${?} -ne 0 ] && genError 406 "Can not read source file, or can not write to temp file" 12
cp ${TMPFILE} ${FILE}
[ ${?} -ne 0 ] && genError 407 "Can not copy temp file to dhcp host" 13
rm ${TMPFILE}
if [ ${?} -eq 0 ]
then
	initResponse
	startJSON
	insertJSON "status_code" I "200"
	insertJSON "status_message" S "ok" 
	insertJSON "response" S "Removed the host ${GETTYPE}${GETID}, line from ${STLINE} to ${ENLINE}" L
	closeJSON
	printJSON
else
	genError 404 "Error occured  the host ${GETTYPE}${GETID} the dhcp file - ${FILE} -" 11
fi
exit 0
