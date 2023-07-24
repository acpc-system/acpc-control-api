#!/bin/bash
###API that reset all host mac addresses file
##	The API uses get method, and does not accept any parameter
## The postdata form name: hostip
#### Exit codes
##	0: Success
##	1: Insufficient parameter
##	2: Invalid host type
##	3: Not enough parameter to parsePostFile fn
##	4: Not a post method from function parsePostFile
##	5: Could not write to the destination file
### Thanks goes to https://riptutorial.com/bash/example/29665/request-method--post--w-json

source create-json.sh
source common.sh
source checkers.sh
echo "Content-type: application/json"
echo ""
FILE="/acpc/adm/tmp/macs"
[ ! -f ${FILE} ] && touch ${FILE}
isWrite "${FILE}"
[ ${?} -ne 0 ] &&  genError 406 "MAC file for ${GETTYPE} has no write permission" 5
rm "${FILE}"
touch "${FILE}"
	initResponse
	startJSON
	insertJSON "status_code" I "200"
	insertJSON "status_message" S "ok" 
	insertJSON "response" S "Done" L
	closeJSON
	printJSON
exit 0
