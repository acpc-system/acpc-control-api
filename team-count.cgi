#!/bin/bash 
###API that counts the number of contestants mac in the contestantmac file
#### Exit codes
##	0: Success
##	1: file does not exists
##	2: file has no read permission
##	3: generic error
source create-json.sh
source common.sh
echo "Content-type: application/json"
echo ""
set -x
/usr/sbin/wrapper
echo ${?}
set +x
initResponse
startJSON
RC=0
[ ! -f /acpc/adm/etc/contestantmac ] && genError 401 "contestant mac file not exist" 1
[ ! -r /acpc/adm/etc/contestantmac ] && genError 402 "contestant mac file has no read permission"  2
N=$(cat /acpc/adm/etc/contestantmac |grep -v "^$" | wc -l)
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
