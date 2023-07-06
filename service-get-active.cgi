#!/bin/bash
###API that returns is the a service started or no
##	The API uses GET method, and accept service parameters 
#### Exit codes
##	0: Success
##	1: Insufficient parameter
##	2: Invalid service name
##	3: Service does nott exists
##	4: Permission denied
source create-json.sh
source common.sh
source checkers.sh
GETSERVICE=$(parseQueryString ${QUERY_STRING} "service")
echo "Content-type: application/json"
echo ""
initResponse
startJSON
[ -z ${GETSERVICE} ] && genError 100 "Insufficient parameter " 1
checkService ${GETSERVICE}
[ ${?} -ne 0 ] && genError 101 "Invalid service name " 2
RES=$(sudo systemctl is-active ${GETSERVICE})
insertJSON "status_code" I "200"
insertJSON "status_message" S "ok" 
insertJSON "response" S "active, ${RES}" L
closeJSON
printJSON
exit 0
