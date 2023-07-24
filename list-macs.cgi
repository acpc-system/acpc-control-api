#!/bin/bash
###API that returns all host mac addresses file
##	The API uses get method, and does not accept any parameter
## The postdata form name: hostip
#### Exit codes
##	0: Success
##	1: Insufficient parameter
##	2: Invalid host type
##	3: Not enough parameter to parsePostFile fn
##	4: macs file is not found
##	5: macs file has not read permission
### Thanks goes to https://riptutorial.com/bash/example/29665/request-method--post--w-json

source create-json.sh
source common.sh
source checkers.sh
echo "Content-type: application/json"
echo ""
FILE="/acpc/adm/tmp/macs"
isExist "${FILE}"
[ ${?} -ne 0 ] && genError 406 "MAC file for is not found" 4
isRead "${FILE}"
[ ${?} -ne 0 ] && rm ${TMPFILE} && genError 406 "MAC file for ${GETTYPE} has no read permission" 5
MACS=""
CO=1
while read HOST
do
        if [ ${CO} -eq 1 ]
        then
                CO=2
                MACS="\"${HOST}\""
        else
                MACS="${MACS},\"${HOST}\""
        fi
done < /acpc/adm/tmp/macs
	initResponse
	startJSON
	insertJSON "status_code" I "200"
	insertJSON "status_message" S "ok" 
	insertJSON "response" A "${MACS}" L
	closeJSON
	printJSON
exit 0
