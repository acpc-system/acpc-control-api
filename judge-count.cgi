#!/bin/bash
###API that counts the number of judge mac in the judgemac file
#### Exit codes
##	0: Success
##	1: file does not exists
##	2: file has no read permission
##	3: generic error
source create-json.sh
source common.sh
echo "Content-type: application/json"
echo ""
initResponse
startJSON
RC=0
[ ! -f /acpc/adm/etc/judgesmac ] && genError 401 "judge mac file not exist" 1
[ ! -r /acpc/adm/etc/judgesmac ] && genError 402 "judge mac file has no read permission"  2
N=$(cat /acpc/adm/etc/judgesmac |grep -v "^$" | wc -l)
if [ ${?} -eq 0 ]
then
	insertJSON "status_code" I "200"
	insertJSON "status_message" S "ok" 
	insertJSON "response" S "${N}" L
	RC=0
else
	genError 403 "Generic error reading the file"
	RC=3
fi
closeJSON
printJSON
exit RC
