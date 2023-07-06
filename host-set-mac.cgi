#!/bin/bash
###API that set a mac address for certain team from /acpc/adm/etc/dhcp/dhcpd.conf.hosts
##	The API uses POST method, and accept id parameter, and type
## The postdata form name: hostmac
#### Exit codes
##	0: Success
##	1: Insufficient parameter
##	2: ID is not an integer
##	3: dhcp hosts file does not exist
##	4: dhcp hosts file does not have read permission
##	5: dhcp hosts file does not have write permission
##	6: team is not valid (not exists in dhcpd.conf.hosts)
##	7: passed mac address is not a valid mac
##	8: Error in replace operation
##	9: Error on postdata json format
##	10: Error, not a post method
##	11: Error writting in dhcp hosts file
##	12: Can not open source file, or can not write to temp file
##	13: Can not open  temp file to the dhcp hosts file
##	14:Invalid acpc host type
#### The post data must be in json and quated in '
## Example: '{"hostmac": "00:00:00:00:00:01"}'
### Thanks goes to https://riptutorial.com/bash/example/29665/request-method--post--w-json

source create-json.sh
source common.sh
source checkers.sh
source macops.sh
FILE="/acpc/adm/etc/dhcp/dhcpd.conf.hosts"
echo "Content-type: application/json"
echo ""
### Parsing 1st, the post data
DATA=$(parsePost)
RETPOST=${?}
case ${RETPOST} in
        1)
                genError 404 "Error in post data JSON format" 9
                ;;
        2)
                genError 405 "Error, not post method" 10
                ;;
esac
newMAC=$(echo "${DATA}" | jq .hostmac  | sed 's/"//g')
checkMAC "${newMAC}"
[ ${?} -ne 0 ] && genError 408 "Invalid MAC Address format" 7

GETID=$(parseQueryString ${QUERY_STRING} "id")
[ -z ${GETID} ] && genError 100 "Insufficient parameter " 1
GETTYPE=$(parseQueryString ${QUERY_STRING} "type")
[ -z ${GETTYPE} ] && genError 100 "Insufficient parameter " 1
checkInteger ${GETID}
[ ${?} -ne 0 ] && genError 101 "host ID is not an integer" 2
checkHosttype "${GETTYPE}"
[ ${?} -ne 0 ] && genError 101 "Invalid ACPC Host type" 14
[ ! -f ${FILE} ] && genError 401 "dhcp hosts file not exist" 3
[ ! -r ${FILE} ] && genError 402 "dhcp hosts  file has no read permission"  4
MAC=$(getMAC "${GETTYPE}${GETID}")
RET=${?}
[ ${RET} -eq 1 ] && genError 403 "Host not found" 6
### Now, replacing the old mac with new mac in the file
TMPFILE=$(mktemp)
cat ${FILE} | sed  "s/${MAC}/${newMAC}/g" > ${TMPFILE}
[ ${?} -ne 0 ] && genError 406 "Can not read source file, or can not write to temp file" 12
cp ${TMPFILE} ${FILE}
[ ${?} -ne 0 ] && genError 407 "Can not copy temp file to dhcp host" 13
rm ${TMPFILE}
if [ ${?} -eq 0 ]
then
	initResponse
	startJSON
	insertJSON "status_code" I "200"
	insertJSON "status_message" S "ok" 
	insertJSON "response" S "Replacing ${MAC} with ${newMAC}" L
	closeJSON
	printJSON
else
	genError 404 "Error occured updating ${MAC} with ${newMAC} in  the dhcp file - ${FILE} -" 11
fi
exit 0
