#!/bin/bash
### TO DO: read API Call return code
###API that generats a sequence of hosts from etc/(hostmac file) to /acpc/adm/etc/dhcp/dhcpd.conf.hosts using host-insert api
##	The API uses GET method, and accept  type, shost which is the start host count & sip which is the start ip
#### Exit codes
##	0: Success
##	1: Insufficient parameter
##	2: Invalid host type
##	3: invalid ip address
##	4: HOst mac is not found
##	5: HOst mac has no read permission
##	7: Error coming from insert mac API
#### The post data must be in json and quated in '

source create-json.sh
source common.sh
source checkers.sh
source ipops.sh
echo "Content-type: application/json"
echo ""
### Parsing 1st, the post data
GETTYPE=$(parseQueryString ${QUERY_STRING} "type")
[ -z ${GETTYPE} ] && genError 100 "Insufficient parameter " 1
GETSHOST=$(parseQueryString ${QUERY_STRING} "shost")
[ -z ${GETSHOST} ] && genError 100 "Insufficient parameter " 1
GETSIP=$(parseQueryString ${QUERY_STRING} "sip")
[ -z ${GETSIP} ] && genError 100 "Insufficient parameter " 1
checkHosttype "${GETTYPE}"
[ ${?} -ne 0 ] && genError 101 "Invalid ACPC Host type" 2
checkIP "${GETSIP}"
[ ${?} -ne 0 ] && genError 101 "Invalid IP Address" 3
FILE="/acpc/adm/tmp/macs"
isExist "${FILE}"
[ ! -f ${FILE} ] && genError 102 "Host mac file not found" 4
isRead "${FILE}"
[ ${?} -ne 0 ] && rm ${TMPFILE} && genError 406 "MAC file for has no read permission" 5
IP="${GETSIP}"
TEAMN="${GETSHOST}"
while read LINE
do
	## Check for mac exists or no
	findMAC "${LINE}"
	RET=${?}
	if  [ ${RET} -eq 0 ] 
	then
		MSG=$(curl -s -X POST -H "Content-Type: application/json" -d "{\"mac\":\"${LINE}\",\"ip\":\"${IP}\"}" http://10.0.3.2/api/team/${TEAMN}/insert)
		CODE=$(echo "${MSG}" | jq .status_code)
		if [ ${CODE} -eq 200 ] 
		then
			TEAMN=$[TEAMN+1]
			OCT1=$(echo ${IP} | cut -d. -f 1)
			OCT2=$(echo ${IP} | cut -d. -f 2)
			OCT3=$(echo ${IP} | cut -d. -f 3)
			OCT4=$(echo ${IP} | cut -d. -f 4)
			OCT4=$[OCT4+1]
			if [ ${OCT4} -gt 255 ]
			then
				OCT4=0
				OCT3=$[OCT3+1]
				if [ ${OCT3} -gt 255 ]
				then
					OCT3=0
					OCT2=$[OCT2+1]
				fi
			fi
			IP="${OCT1}.${OCT2}.${OCT3}.${OCT4}"
		else
			genError 407 "$(echo "${MSG}" | jq .status_message) ${IP} ${LINE} ${GETTYPE}${TEAMN}" 7
		fi
	fi
done < "${FILE}"
	initResponse
	startJSON
	insertJSON "status_code" I "200"
	insertJSON "status_message" S "ok" 
	insertJSON "response" S "Done" L
	closeJSON
	printJSON
exit 0
