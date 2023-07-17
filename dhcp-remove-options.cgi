#!/bin/bash 
###API that removes an option from dhcp options file
###Uses a post method to pass the subnet configuration with variable config
#### Exit codes
##	0: Success
##	1: Not enough parameters
##	2: Invalid IP 
##	3: Not an integer
##	4: mask must be <=32
##	5: invalid subnet range
##	6: subnet is already exist
##	7: subnet config file isnot found
##	8: Subnet config file has no read permission
##	9: subnet config file has no write permission
##	10: Post data does not contain JSON format
##	11: not a post method
##	12: post does not contain conf field
##	13: Configurations specified exist more than once.
source checkers.sh
source create-json.sh
source common.sh
FILE="/acpc/adm/etc/dhcp/dhcpd.conf.options"
echo "Content-type: application/json"
echo ""
### Parsing 1st, the post data
DATA=$(parsePost)
RETPOST=${?}
case ${RETPOST} in
        1)
                genError 404 "Error in post data JSON format" 10
                ;;
        2)
                genError 405 "Error, not post method" 11
                ;;
esac
CONF=$(getPostField "${DATA}" "conf")
[ ${?} -ne 0 ] && genError 410 "Post data does not contain conf field" 12

isExist "${FILE}"
[ ${?} -ne 0 ] && genError 412 "subnet file not exist" 7
isRead "${FILE}"
[ ${?} -ne 0 ] && genError 413 "subnet file has no read permission" 8
isWrite "${FILE}"
[ ${?} -ne 0 ] && genError 414 "subnet file has no write permission" 9
CONFLINES=$(grep -c "${CONF}" ${FILE})
[ ${CONFLINES} -gt 1 ] && genError 415 "Configuration found more than once" 13
[ ${CONFLINES} -eq 0 ] && genError 416 "Options not found" 14
TMPFILE=$(mktemp)
sed "/${CONF}/d" ${FILE} > ${TMPFILE}
cp ${TMPFILE} ${FILE}
rm ${TMPFILE}
initResponse
startJSON
insertJSON "status_code" I "200"
insertJSON "status_message" S "ok" 
insertJSON "response" S "Removed" L
closeJSON
printJSON
exit 0
