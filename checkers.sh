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
        RET=$(echo ${N} | grep -c -v -i "^[0-9A-F][0-9A-F]:[0-9A-F][0-9A-F]:[0-9A-F][0-9A-F]:[0-9A-F][0-9A-F]:[0-9A-F][0-9A-F]:[0-9A-F][0-9A-F]$")
        return ${RET}
}

#####Function takes a parameter, check if the parameter is valid IPv4 address. Returns 0 if yes, otherwise not vaid IPv4 address
function checkIP {
	local IP="${1}"
	local oIFS="${IFS}"
	IFS="."
	CO=0
	for octet in ${IP}
	do
		checkInteger ${octet}
		[ ${?} -ne 0 ] && return 1
	        if [ ${octet} -lt 0 ] || [ ${octet} -gt 255 ] 
		then
			return 1
		fi
		CO=$[CO+1]
	done
	if [ ${CO} -ne 4 ]
	then
		return 1
	fi
	IFS="${oIFS}"
	return 0
}

###Function, check for service name is a valid, or contains invalid characters
function checkService() {
	local SERVICE="${1}"
	local INVALIDCHAR='$*?\<>&[]()"'
	##Check if the service name contains space
	local RET=$(echo "${SERVICE}" | grep -c " ")
	[ ${RET} -ne 0 ] && return 1
	##Check if the service name contains any XSS
	local LEN=$[$(echo ${INVALIDCHAR} | wc -c)-2]
	local CHAR=""
	for i in $(seq 0 ${LEN})
	do
		CHAR=${INVALIDCHAR:${i}:1}
		#### Used fgrep to do not interpret any special character
		RET=$(echo "${SERVICE}" | fgrep -c "${CHAR}")
		[ ${RET} -ne 0 ] && return 1
	done
	return 0
}

## Function, accepts the state as a parameter, return 0 if the parameter is either true or falce. Otherwise returns 1
function checkState() {
	local STATE="${1}"
	if [ ${STATE} != "true" ] && [ ${STATE} != "false" ] && [ ${STATE} != "start" ] && [ ${STATE} != "stop" ] && [ ${STATE} != "restart" ]
	then
		return 1
	fi
	return 0
}

##Function, accepts a host type, and check is it valid so return 0, not valid return 1
function checkHosttype() {
	local TYPE="${1}"
	### Modify the VALIDTYPES to add/remove host type
	local VALIDTYPES="team judge print web pc2 cds print scoreboard"
	RES=$(echo "${VALIDTYPES}" | grep -c -w "${TYPE}")
	if [ ${RES} -ne 0 ]
	then
		return 0
	else
		return 1
	fi
}

##Function accepts file name
## returns 
#	0 if exists
#	1 if not exists
#	2 not enough parameters
function isExist() {
	[ ${#} -ne 1 ] && return 2
	local FILE="${1}"
	[ -f "${FILE}" ] && return 0
	return 1
}

##Function accepts file name
## returns
#       0 if can read
#       1 if can not read 
#       2 not enough parameters
function isRead() {
        [ ${#} -ne 1 ] && return 2
        local FILE="${1}"
        [ -r "${FILE}" ] && return 0
        return 1
}

##Function accepts file name
## returns
#       0 if can write
#       1 if can not write
#       2 not enough parameters
function isWrite() {
        [ ${#} -ne 1 ] && return 2
        local FILE="${1}"
        [ -w "${FILE}" ]  && return 0
        return 1
}

##Function accepts a string, and return if this string is a valid dhcp.config.<string> or no
##	Parameter:
##		dhcp config file
##	Return:
#		0: Success, Valid
#		1: failed, Not valud
#		2: Not enough parameter
function checkDHCPconf () {
	[ ${#} -ne 1 ] && return 2
	local EXT="${1}"
	local VALIDCONF="hosts subnet options"
	N=$(echo "${VALIDCONF}" | grep -w -c ${EXT})
	[ ${N} -ne 0 ] && return 0
	return 1
}

### Function accepts a subnet id, and subnet mask. Check is the subnet id is a valid network id or no
##Paramters:
##	1-subnet id in form of ip.ip.ip.ip
##	2-mask in form if integer from 0 to 32
##	Returns:
#		0: Success
##		1: invalid subnet
function checkSubnet() {
	local NET="${1}"
	local MASK="${2}"
	local NNET=""
	local TERM=0
	local GMASK=$(getSubnet ${MASK})
	[ ${?} -ne 0 ] && return 1
	for i in $(seq 1 4) 
	do
		NETOCT=$(echo "${NET}" | cut -d. -f ${i})
		MASKOCT=$(echo "${GMASK}" | cut -d. -f ${i})
		TERM=$[NETOCT & MASKOCT]
		if [ ${i} -eq 1 ]
		then
			NNET="${TERM}"
		else
			NNET="${NNET}.${TERM}"
		fi
	done
	[ ${NNET} == ${NET} ] && return 0  || return 1
}
