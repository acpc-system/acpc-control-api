#!/bin/bash
###API that set a ip address for certain team from /acpc/adm/etc/dhcp/dhcpd.conf.hosts
##	The API uses POST method, and accept id parameter, type 
## The postdata form name: hostip
#### Exit codes
##	0: Success
##	1: Insufficient parameter
##	2: Invalid host type
##	3: Not enough parameter to parsePostFile fn
##	4: Not a post method from function parsePostFile
##	5: Could not write to the destination file
#### The post data must be in json and quated in '
## Example: '{"hostip": "192.168.1.2"}'
### Thanks goes to https://riptutorial.com/bash/example/29665/request-method--post--w-json

source create-json.sh
source common.sh
source checkers.sh
source ipops.sh
echo "Content-type: application/json"
echo ""
### Parsing 1st, the post data
TMPFILE=$(mktemp)
DATA=$(parsePostFile "${TMPFILE}")
RETPOST=${?}
case ${RETPOST} in
        1)
                genError 404 "Not enough parameters" 3
                ;;
        2)
                genError 405 "Is not a post method" 4
                ;;
	3)
		genError 406 "Could not update the mac file" 5
esac
GETTYPE=$(parseQueryString ${QUERY_STRING} "type")
[ -z ${GETTYPE} ] && rm ${TMPFILE} && genError 100 "Insufficient parameter " 1
checkHosttype "${GETTYPE}"
[ ${?} -ne 0 ] && rm ${TMPFILE} && genError 101 "Invalid ACPC Host type" 2
FILE="/acpc/adm/etc/${GETTYPE}"
[ ! -f ${FILE} ] && touch ${FILE}
isWrite "${FILE}"
[ ${?} -ne 0 ] && rm ${TMPFILE} && genError 406 "MAC file for ${GETTYPE} has no write permission" 5
cp ${TMPFILE} ${FILE}
#rm ${TMPFILE}

	initResponse
	startJSON
	insertJSON "status_code" I "200"
	insertJSON "status_message" S "ok" 
	insertJSON "response" S "Done" L
	closeJSON
	printJSON
exit 0
