## Function generates an error and exit the script
##	1st par: status_code
##	2nd par: status_message
##	3rd par: Main script exit code
source checkers.sh
function genError {
	local CODE=${1}
	local MSG="${2}"
	local RET=${3}
	initResponse
	startJSON
	insertJSON "status_code" I "${CODE}"
	insertJSON "status_message" S "${MSG}" L
	closeJSON
	printJSON
	exit ${RET}
}

###Function takes a query string and key, return the value for this key from query string if found
## The function returns empty string
function parseQueryString {
	local STR="${1}"
	local KEYC="${2}"
	local VALC=""
	local KEY=""
	local VAL=""
	OIFS=${IFS}
	IFS='&'
	for p in ${STR}
	do
		KEY=$(echo ${p} | cut -d= -f1)
		VAL=$(echo ${p} | cut -d= -f2)
		if [ ${KEY} == ${KEYC} ]
		then
			VALC="${VAL}"
			break;
		fi
	done
	IFS=${OIFS}
	echo ${VALC}
}


#Function, pars the post response, and save it to a file 
##	parameters:
##		file name
##Return
#	0: Success
#	1: not enough parameters
#	2: not a post method
#	3: Could not update the file
function parsePostFile() {
	local TMPFILE="${1}"
	[ ${#} -ne 1 ] && return 1
	local DATA=""
	if [ "$REQUEST_METHOD" == "POST" ]; then

	while read DATA
	do
		echo "${DATA}" >> ${TMPFILE}
	done
	else
		return 2
	fi
	return 0;
}


### Function, parse the post response, and print the body. 
## Return:
##	0: Success
#	1: Not a valid JSON format
#	2: Not a post method
function parsePost(){
if [ "$REQUEST_METHOD" == "POST" ]; then

    # The environment variabe $CONTENT_TYPE describes the data-type received
        # The environment variabe $CONTENT_LENGTH describes the size of the data
        read -n "$CONTENT_LENGTH" QUERY_STRING_POST        # read datastream
        # The following lines will prevent XSS and check for valide JSON-Data.
        # But these Symbols need to be encoded somehow before sending to this script
        QUERY_STRING_POST=$(echo "$QUERY_STRING_POST" | sed "s/'//g" | sed 's/\$//g;s/`//g;s/\*//g;s/\\//g' )        # removes some symbols (like \ * ` $ ') to prevent XSS with Bash and SQL.
        QUERY_STRING_POST=$(echo "$QUERY_STRING_POST" | sed -e :a -e 's/<[^>]*>//g;/</N;//ba')    # removes most html declarations to prevent XSS within documents
        JSON=$(echo "$QUERY_STRING_POST" | jq .)        # json encode - This is a pretty save way to check for valide json code
        if [ -z "${JSON}" ]
        then
               return 1 
        fi

else
	return 2
fi
echo "${JSON}"
return 0
}

### Function takes a post data, and field name. Prints out the value for this field and return 0, return 1 if the field is not found
## The post data in JSON format
function getPostField() {
	local DATA="${1}"
	local KEY="${2}"
	local VAL=$(echo "${DATA}" | jq ."${KEY}")
	if [ ${VAL} == "null" ] 
	then
		return 1
	else
		VAL="$(echo ${VAL} | sed 's/"//g')"
		echo "${VAL}"
		return 0
	fi
}

### Function takes a post data, and field name. Prints out the value for this field  (The field is a JSON array) and return 0, return 1 if the field is not found
## The post data in JSON format
function getPostFieldArray() {
        local DATA="${1}"
        local KEY="${2}"
	local CO=1
	local -n DATAARR="${3}"
	#echo "${DATA} "|jq -r ".conf[]" | while read -r LINE
	#echo "${DATA}" | jq '.conf.[]'
	TMPFILE=$(mktemp)
	echo "${DATA}" | jq -r ".${KEY}[]" >> ${TMPFILE}
	while read LINE
	do
		DATAARR+=("${LINE}")
	done < ${TMPFILE}
	rm ${TMPFILE}
	#[ ${CO} -eq 1 ] && return 1
	return 0
}


##Function, accepts array of strings, and return them as comma separated list, with each elements rurrounded by "
##	returns
##	0: Success
##	1: not enough parameters
function arrayToCSV () {
	[ ${#} -ne 1 ] && return 1
	local DATA="${1}"
	local RES=""
	localCO=1
	for EL in ${DATA}
	do
		if [ ${CO} -eq 1 ]
		then
			CO=2
			RES="\"${EL}\""
		else
			RES="${RES},\"${EL}\""
		fi
	done
	echo "${RES}"
	return 0
}

###Function takes a host, 
#	return 
#	0 if listed as bad
#	1 is not listed, 
#	3 enough parameters)
#	4 file does not exists
#	5 file has no read permission
function isBad() {
	[ ${#} -ne 1 ] && return 3
	local HOST="${1}"
	local FILE="/acpc/adm/etc/badpcs"
	isExist "${FILE}"
	[ ${?} -ne 0 ] && return 4
	isRead "${FILE}"
	[ ${?} -ne 0 ] && return 5
	N=$(grep -c "^${HOST}$" ${FILE})
	if [ ${N} -eq 0 ] 
	then
		return 0
	else
		return 1
	fi
}


###Function converts from integer to netmask octets
##Parameters:
#	integer
##	return 
##		0: Success
##		1: Invalid netmask integer
##		2: not enough paramters
function getSubnet() {
	[ ${#} -ne 1 ] && return 2
	local MASKINT=${1}
	local MASK=""
	if [ ${MASKINT} -le 0 ] || [ ${MASKINT} -gt 32 ]
	then
		return 1
	fi
	local NO255=$[ ${MASKINT} / 8 ]
	for j in $(seq 1 ${NO255} )
	do
		if [ ${j} -eq 1 ]
		then
			MASK="255"
		else
			MASK="${MASK}.255"
		fi
	done
	local RES=$[ NO255 + 1]
	for j in $(seq ${RES} 4)
	do
		NO1=$[ MASKINT % 8 ]
		MASKINT=0
		[ ${NO1} -eq 0 ] && VAL="0" || VAL=$[256 - 2 ** NO1]
		MASK="${MASK}.${VAL}"
	done
	echo "${MASK}"
	return 0
}

