######################## Shell module contains all functions related to host checking

### Function, takes a host and return 0 if live, 1 not live, 2 missed hostname
function checkHost() {
	[ ${#} -ne 1 ] && return 2
	local HOST="${1}"
	ping ${HOST} -c 1 -W 1 >/dev/null 2>&1
	[ ${?} -eq 0 ] && return 0 || return 1
}

### Function, takes a host and return is it resolvable or no
##	0: Success
##	1: not enough parameter
##	2: not resolvable
function checkHostname() {
	[ ${#} -ne 1 ] && return 1
	local HOST="${1}"
	host ${HOST} > /dev/null 2>&1
	[ ${?} -ne 0 ] && return 2
	return 0
}
