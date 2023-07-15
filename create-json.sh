jsonResponse=""

### Function, empty jsonResponse
function initResponse {
	jsonResponse=""
}

### Function start and open jsonResponse with {
function startJSON {
	jsonResponse="{"
}

### Function close and terminates the jsonResponse with }
function closeJSON {
	jsonResponse="${jsonResponse}}"
}

### Function inserts a line into jsonResponse, add , at the end of msg
## Accepts 4 parameters
##	1-Key
##	2-Type of value I: integer, S: String
##	3-Value
##	4-If set to L means last, so do not add , to the end of message
function insertJSON {
	local KEY="\"${1}\""
	local TYPE=${2}
	local DATA="${3}"
	case ${TYPE} in
		SJ)
			###Sub JSON
			local CO=1
			local VALUE="{"
			local RKEY=""
			local RVAL=""
			local LINE=""
			local TOTAL=$(echo "${DATA}"| wc -l)
			for L in $(seq 1 ${TOTAL})
			do	
				LINE=$(echo "${DATA}" | head -1 | sed 's/"/\\\"/g')
				DATA=$(echo "${DATA}" | tail -n +2)
				if [ ${CO} -eq 1 ]
                        	then
                                	#VALUE="${VALUE} \"${RKEY}\": \"${RVAL}\""
                                	VALUE="${VALUE} ${LINE}"
                        	else
                                	VALUE="${VALUE}, ${LINE}"
                        	fi
				CO=$[CO+1]
			done
			VALUE="${VALUE} }"

			VALUE=$(echo "${DATA}" | sed 's/"/\\\"/g')
			VALUE="[ \"${VALUE}\" ]"
			;;
		I)
			local VALUE="${DATA}"
			;;
		S)
			local VALUE="\"${DATA}\""
			;;
		A)
			local VALUE="[ "
			OIFS=${IFS}
			IFS=','
			CO=1
			for H in ${DATA}
			do
				if [ ${CO} -eq 1 ]
				then
					VALUE="${VALUE} ${H}"
					CO=2
				else
					VALUE="${VALUE}, ${H}"
				fi
			done
			IFS=${OIFS}
			VALUE="${VALUE} ]"
			;;
	esac
	jsonResponse="${jsonResponse}${KEY}: ${VALUE}"
	[ -z ${4} ] && jsonResponse="${jsonResponse},"
}


### Function inserts a line into jsonResponse, does not add any thing at the end of message

function printJSON {
	echo "${jsonResponse}"
}
