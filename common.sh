## Function generates an error and exit the script
##	1st par: status_code
##	2nd par: status_message
##	3rd par: Main script exit code
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
		VAL=$(echo ${VAL} | sed 's/"//g')
		echo "${VAL}"
		return 0
	fi
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
