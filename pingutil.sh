######################## Shell module contains all functions related to host checking

### Function, takes a host and return 0 if live, 1 not live, 2 missed hostname
function checkHost() {
	[ ${#} -ne 1 ] && return 2
	local HOST="${1}"
	ping ${HOST} -c 1 >/dev/null 2>&1
	[ ${?} -eq 0 ] && return 0 || return 1

}
