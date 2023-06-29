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
	[ ${TYPE} == 'I' ] && local VALUE="${3}" || local VALUE="\"${3}\""
	jsonResponse="${jsonResponse}${KEY}: ${VALUE}"
	[ -z ${4} ] && jsonResponse="${jsonResponse},"
}


### Function inserts a line into jsonResponse, does not add any thing at the end of message

function printJSON {
	echo "${jsonResponse}"
}
