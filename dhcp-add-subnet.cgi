#!/bin/bash 
###API that add a subnet to the dhcp subnet config files
###Parameters:
##	net: Network ID
##	mask mask as an integer 
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
source checkers.sh
source create-json.sh
source common.sh
FILE="/acpc/adm/etc/dhcp/dhcpd.conf.subnet"
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
getPostFieldArray "${DATA}" "conf" CONFARR
[ ${?} -ne 0 ] && genError 410 "Post data does not contain conf field" 12


GETNET=$(parseQueryString ${QUERY_STRING} "net")
[ -z ${GETNET} ] && genError 100 "Insufficient parameter net " 1
GETMASK=$(parseQueryString ${QUERY_STRING} "mask")
[ -z ${GETMASK} ] && genError 100 "Insufficient parameter mask" 1
checkIP "${GETNET}"
[ ${?} -ne 0 ] && genError 408 "Invalid IP Address format" 2
checkInteger "${GETMASK}"
[ ${?} -ne 0 ] && genError 409 "Invalid Integer" 3
[ ${GETMASK} -gt 32 ] && genError 410 "Invalid subnet mask, must be <= 32" 4
checkSubnet "${GETNET}" "${GETMASK}"
[ ${?} -ne 0 ] && genError 411 "Invalid subnet range" 5
isExist "${FILE}"
[ ${?} -ne 0 ] && genError 412 "subnet file not exist" 7
isRead "${FILE}"
[ ${?} -ne 0 ] && genError 413 "subnet file has no read permission" 8
isWrite "${FILE}"
[ ${?} -ne 0 ] && genError 414 "subnet file has no write permission" 9
FULLMASK=$(getSubnet ${GETMASK})
FLAG=$(grep -c "^ *subnet *${GETNET} *netmask *${FULLMASK} *{" ${FILE})
[ ${FLAG} -ne 0 ] && genError 411 "subnet is already exists" 6

SUBNET=$(cat ${FILE})
initResponse
startJSON
FILE="${FILE}"
isExist "${FILE}"
[ ${?} -ne 0 ] && genError 103 "DHCP subnets configuration is not exit" 4
isRead "${FILE}"
[ ${?} -ne 0 ] && genError 102 "DHCP subnets configuraiton has no read permission" 3
CONFLEN=${#CONFARR[@]}
CONFLEN=$[CONFLEN-1]
TMPFILE=$(mktemp)
echo "subnet ${GETNET} netmask ${FULLMASK} {" > ${TMPFILE}
for i in $(seq 0 ${CONFLEN})
do
	echo -e "\t${CONFARR[${i}]}" >> ${TMPFILE}
done
echo "}" >> ${TMPFILE}
cat ${TMPFILE} >> ${FILE}
rm ${TMPFILE}
insertJSON "status_code" I "200"
insertJSON "status_message" S "ok" 
insertJSON "response" S "Added" L
closeJSON
printJSON
exit 0
