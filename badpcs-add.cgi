#!/bin/bash
###API that adds  host into /acpc/adm/etc/badpcs
##	The API uses get method, and accept id parameter, type 
#### Exit codes
##	0: Success
##	1: Insufficient parameter
##	2: ID is not an integer
##	3: Invalid ACPC host type
##	4: badpcs is not exists
##	5: badpcs is not writable
##	6: badpcs is not readable
##	7: host is already listed as bad
##	8: Can not update badpcs file

source create-json.sh
source common.sh
source checkers.sh
FILE="/acpc/adm/etc/badpcs"
echo "Content-type: application/json"
echo ""
GETID=$(parseQueryString ${QUERY_STRING} "id")
[ -z ${GETID} ] && genError 100 "Insufficient parameter " 1
GETTYPE=$(parseQueryString ${QUERY_STRING} "type")
[ -z ${GETTYPE} ] && genError 100 "Insufficient parameter " 1
checkInteger ${GETID}
[ ${?} -ne 0 ] && genError 101 "host ID is not an integer" 2
checkHosttype "${GETTYPE}"
[ ${?} -ne 0 ] && genError 101 "Invalid ACPC Host type" 3
isExist "${FILE}" 
[ ${?} -ne 0  ] && genError 401 "The badpcs file not exist" 4
isRead "${FILE}" 
[ ${?} -ne 0 ] && genError 403 "The badpcs file has no read permission"  6
isWrite "${FILE}"
[ ${?} -ne 0 ] && genError 403 "The badpcs file has no write permission"  5
HOST="${GETTYPE}${GETID}"
isBad "${HOST}" 
[ ${?} -eq 1 ] && genError 404 "The host ${HOST} is already listed as bad" 7

### Now, replacing the old ip with new ip in the file
TMPFILE=$(mktemp)
cp ${FILE} ${TMPFILE}
echo "${HOST}" >> ${TMPFILE}
cp ${TMPFILE} ${FILE}
rm ${TMPFILE}
	initResponse
	startJSON
	insertJSON "status_code" I "200"
	insertJSON "status_message" S "ok" 
	insertJSON "response" S "Added ${HOST}" L
	closeJSON
	printJSON
exit 0
