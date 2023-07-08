#!/bin/bash 
###API that list the content of the badpcs file 
#### Exit codes
##	0: Success
##	1: badpcs not exist
##	2: Can not read from badpcs
source create-json.sh
source common.sh
FILE="/acpc/adm/etc/badpcs"
echo "Content-type: application/json"
echo ""
initResponse
startJSON
[ ! -f ${FILE} ] && genError 101 "Can not find badpcs file" 1
[ ! -r ${FILE} ] && genError 102 "Can not read from badpcs file" 2
TMPHOSTS=$(cat ${FILE})
HOSTS=$(arrayToCSV "${TMPHOSTS}")
insertJSON "status_code" I "200"
insertJSON "status_message" S "ok" 
insertJSON "response" A "${HOSTS}" L
closeJSON
printJSON
exit 0
