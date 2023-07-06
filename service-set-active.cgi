#!/bin/bash
###API that start/stop/restart a service
##	The API uses GET method, and accept service and state (start/stop/restart) parameters service=$1&state=$2
##	$1 is the service name
##	$2: start/stop/restart
#### Exit codes
##	0: Success
##	1: Insufficient parameter
##	2: Invalid service name
##	3: Unknown error
##	4: Permission denied
##	5: Invalid enable state mustbe enable or disable
source create-json.sh
source common.sh
source checkers.sh
GETSERVICE=$(parseQueryString ${QUERY_STRING} "service")
GETSTATE=$(parseQueryString ${QUERY_STRING} "state")
echo "Content-type: application/json"
echo ""
initResponse
startJSON
[ -z ${GETSERVICE} ] && genError 100 "Insufficient parameter " 1
[ -z ${GETSTATE} ] && genError 100 "Insufficient parameter " 1
checkService ${GETSERVICE}
[ ${?} -ne 0 ] && genError 101 "Invalid service name " 2
checkState ${GETSTATE}
[ ${?} -ne 0 ] && genError 101 "Invalid enable state " 5
### systemctl returns an exit code of 1 for non existing service, or disabled service
RES=$(sudo systemctl ${GETSTATE} ${GETSERVICE})
if  [ ${?} -ne 0 ] 
then
	RES=$(sudo journalctl -xeu ${GETSERVICE}.service)
	genError 102 "Error: ${RES}" 3
fi
insertJSON "status_code" I "200"
insertJSON "status_message" S "ok" 
insertJSON "response" S "${GETSTATE}" L
closeJSON
printJSON
exit 0
