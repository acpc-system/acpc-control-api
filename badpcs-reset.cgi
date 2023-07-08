#!/bin/bash 
###API that reset the badpcs file (remove all its content) 
#### Exit codes
##	0: Success
##	1: badpcs not exist
##	2: Can not write to badpcs
##	3: Error updating badpcs file
source create-json.sh
source common.sh
FILE="/acpc/adm/etc/badpcs"
echo "Content-type: application/json"
echo ""
initResponse
startJSON
[ ! -f ${FILE} ] && genError 101 "Can not find badpcs file" 1
[ ! -w ${FILE} ] && genError 102 "Can not write to badpcs file" 2
TMPFILE=$(mktemp)
sed  '1,$d' ${FILE} > ${TMPFILE}
cp ${TMPFILE} ${FILE}
CPRET=${?}
rm ${TMPFILE}
[ ${CPRET} -ne 0 ] && genError 103 "Error updating the badpcs file" 3
MSG="reset"
insertJSON "status_code" I "200"
insertJSON "status_message" S "ok" 
insertJSON "response" S "${MSG}" L
closeJSON
printJSON
exit 0
