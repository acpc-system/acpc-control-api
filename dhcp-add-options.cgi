#!/bin/bash 
###API that adds an option to dhcp options file
###Uses a post method to pass the subnet configuration with variable confkey, confvalue, and quote
###	To add the value enclosed in ", set the quote: 1 otherwise 0
#### Exit codes
##	0: Success
##	3: Not an integer
##	4: quote mst be 0 or 1
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
CONFKEY=$(getPostField "${DATA}" "confkey")
[ ${?} -ne 0 ] && genError 410 "Post data does not contain confkey field" 12
CONFVALUE=$(getPostField "${DATA}" "confvalue")
[ ${?} -ne 0 ] && genError 410 "Post data does not contain confvalue field" 12
QUOTE=$(getPostField "${DATA}" "quote")
[ ${?} -ne 0 ] && genError 410 "Post data does not contain quote field" 12
checkInteger ${QUOTE}
[ ${?} -ne 0 ] && genError 401 "Quote must be integer" 3
if  [ ${QUOTE} -ne 0 ] && [ ${QUOTE} -ne 1 ]
then
	genError 402 "Quote must be 0 or 1" 4
fi

isExist "${FILE}"
[ ${?} -ne 0 ] && genError 412 "subnet file not exist" 7
isRead "${FILE}"
[ ${?} -ne 0 ] && genError 413 "subnet file has no read permission" 8
isWrite "${FILE}"
[ ${?} -ne 0 ] && genError 414 "subnet file has no write permission" 9
CONFLINES=$(grep -c "${CONFKEY}" ${FILE})
[ ${CONFLINES} -ne 0 ] && genError 416 "Options already exists" 14
TMPFILE=$(mktemp)
cp ${FILE} ${TMPFILE}
if [ ${QUOTE} -eq 1 ]
then
	CONFVALUE="\"${CONFVALUE}\""
fi
echo "${CONFKEY} ${CONFVALUE}" >> ${TMPFILE}
cp ${TMPFILE} ${FILE}
rm ${TMPFILE}
initResponse
startJSON
insertJSON "status_code" I "200"
insertJSON "status_message" S "ok" 
insertJSON "response" S "added" L
closeJSON
printJSON
exit 0
