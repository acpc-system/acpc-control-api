#!/bin/bash
###API stop/start/restart a service
##	The API uses GET method, and accept service parameters 
##	PArameters:
##		service=$1&state=$2
##		$1; Service name
##		$2: start/stop/restart
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
### systemctl returns an exit code of 1 for non existing service, or disabled service
RES=$(sudo systemctl is-enabled ${GETSERVICE})
if  [ ${?} -ne 0 ] && [ "${RES}" != "disabled" ]
then
	genError 102 "Service does not exists" 3
fi
insertJSON "status_code" I "200"
insertJSON "status_message" S "ok" 
insertJSON "response" S "enabled, ${RES}" L
closeJSON
printJSON
exit 0
