#!/bin/bash
###API that insert a host into /acpc/adm/etc/dhcp/dhcpd.conf.hosts
##	The API uses POST method, and accept id parameter, type 
## The postdata form name: 
##mac  00:50:56:39:20:54;
##ip: 172.20.16.101;
## and optional gateway: 
#### Exit codes
##	0: Success
##	1: Insufficient parameter
##	2: ID is not an integer
##	3: dhcp hosts file does not exist
##	4: dhcp hosts file does not have read permission
##	5: dhcp hosts file does not have write permission
##	6: host ip is already reserved dhcpd.conf.hosts)
##	7: passed ip address is not a valid ip
##	8: Error in replace operation
##	9: Error on postdata json format
##	10: Error, not a post method
##	11: Error writting in dhcp hosts file
##	12: Can not open source file, or can not write to temp file
##	13: Can not open  temp file to the dhcp hosts file
##	14: Invalid host type
##	15: Invalid MAC Address format
##	16: Post data does not contain IP
##	17: Post data does not contain MAC
##	18: Invalid GATEWAY IP Address
##	19: Host mac address already exists
##	20: Host name already exists
#### The post data must be in json and quated in '
## Example: '{"ip": "192.168.1.2","mac":"00:00:00:00:00:00","gateway":"10.0.0.2"}'
### Thanks goes to https://riptutorial.com/bash/example/29665/request-method--post--w-json

source create-json.sh
source common.sh
source checkers.sh
source ipops.sh
source macops.sh
source hostops.sh
FILE="/acpc/adm/etc/dhcp/dhcpd.conf.hosts"
TEMPLFILE="/acpc/adm/templs/dhcp/dhcpd.conf.hosts"
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

IP=$(getPostField "${DATA}" "ip")
[ ${?} -ne 0 ] && genError 410 "Post data does not contain IP field" 16
checkIP "${IP}"
[ ${?} -ne 0 ] && genError 408 "Invalid IP Address format" 7


MAC=$(getPostField "${DATA}" "mac")
[ ${?} -ne 0 ] && genError 410 "Post data does not contain MAC field" 17
checkMAC "${MAC}"
[ ${?} -ne 0 ] && genError 409 "Invalid MAC Address format" 15

GATEWAY=$(getPostField "${DATA}" "gateway")
GATEWAYRET=${?}
if [ ${GATEWAYRET} -eq 0 ]
then
	checkIP "${GATEWAY}"
	[ ${?} -ne 0 ] && genError 409 "Invalid GATEWAY IP Address" 18
fi

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
##Check for host exists or no
LINES=$(getHost "${GETTYPE}${GETID}")
RET=${?}
[ ${RET} -eq 0 ] && genError 403 "Host name ${GETTYPE}${GETID} is already taken" 20

## Check for mac exists or no
findMAC "${MAC}"
RET=${?}
[ ${RET} -ne 0 ] && genError 403 "Host MAC already exists" 19

## Check for Ip exists or no
findIP "${IP}"
RET=${?}
[ ${RET} -ne 0 ] && genError 403 "Host IP already reserved" 6

### Now, replacing the old ip with new ip in the file
TMPFILE=$(mktemp)
cat ${TEMPLFILE} | sed -e "s/#HOSTNAME#/${GETTYPE}${GETID}/g" \
		       -e "s/#HOSTMAC#/${MAC}/g" \
		       -e "s/#HOSTIP#/${IP}/g" \
		       -e "s/#DOMAINNAME#/acpc.local/g" > ${TMPFILE}

if [ ${GATEWAYRET} -ne 0 ]
then
	HOSTDATA=$(sed "/routers/d" ${TMPFILE})
else
	HOSTDATA=$(sed "s/#GATEWAYIP#/${GATEWAY}/g" ${TMPFILE})
fi
echo "${HOSTDATA}" > ${TMPFILE}
[ ${?} -ne 0 ] && genError 406 "Can not read source file, or can not write to temp file" 12
cat ${TMPFILE} >> ${FILE}
[ ${?} -ne 0 ] && genError 407 "Can not copy temp file to dhcp host" 13
rm ${TMPFILE}
if [ ${?} -eq 0 ]
then
	initResponse
	startJSON
	insertJSON "status_code" I "200"
	insertJSON "status_message" S "ok" 
	insertJSON "response" S "Added ${GETTYPE}${GETID} with IP ${IP}" L
	closeJSON
	printJSON
else
	genError 404 "Error occured updating ${IP} with ${newIP} in  the dhcp file - ${FILE} -" 11
fi
exit 0
