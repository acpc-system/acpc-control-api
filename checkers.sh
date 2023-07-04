### Function takes a parameter, check if the parameter is an integer. Returns 0 if int otherwise not integer
function checkInteger {
	local N=${1}
	local RET=0
	RET=$(echo ${N} | grep -c -v "^[0-9]*$")
	return ${RET}

}

### Function takes a parameter, check if the parameter is a valid mac address. Returns 0 if yes otherwise not valid mac address
function checkMAC {
        local N="${1}"
        local RET=0
        RET=$(echo ${N} | grep -c -v "^[0-9A-F][0-9A-F]:[0-9A-F][0-9A-F]:[0-9A-F][0-9A-F]:[0-9A-F][0-9A-F]:[0-9A-F][0-9A-F]:[0-9A-F][0-9A-F]$")
        return ${RET}
}
