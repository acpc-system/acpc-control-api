#!/bin/bash
source create-json.sh
echo "Content-type: application/json"
echo ""
initResponse
startJSON
RC=0
N=$(wc -l /acpc/adm/etc/contestantmac)
if [ ${?} -eq 0 ]
then
	insertJSON "status_code" I "200"
	insertJSON "status_message" S "ok" 
	insertJSON "response" S "${N}" L
	RC=0
else

	insertJSON "status_code" I "401"
	insertJSON "status_message" S "Can not read the contestant counter file" L
	RC=1
fi

closeJSON
printJSON
exit RC
