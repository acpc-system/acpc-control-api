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
