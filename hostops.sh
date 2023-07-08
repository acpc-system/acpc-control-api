### Script contains all host operations needed
source checkers.sh

## Function takes an host and prints out start line number, and end line number and returns 0, otherwise returns 1 (not found) 
#	Returns:
#		0: Success
#		1: Invalid host
##	Accepts:
	#one parameters, the host name
function getHost() {
	FILE="/acpc/adm/etc/dhcp/dhcpd.conf.hosts"
	local HOSTID="${1}"
	##1-Get the line number contains the pattern host team{id}
	local LINES=$(grep -n "^host *${HOSTID} " ${FILE} | cut -d: -f1)
	[ -z ${LINES} ] && return  1
	## Now, we have the line number grep the line contains mac address after this line
	local LINEE=$(tail -n +${LINES} ${FILE} |grep -n "}" | head -1| cut -d: -f1)
	LINEE=$[LINEE-1+LINES]
	echo "${LINES}:${LINEE}"
	return 0
}


##Function prints out all host of host type type
##	0:success
##	1:Invalid host type
function listHosts() {
	local TYPE="${1}"
	FILE="/acpc/adm/etc/dhcp/dhcpd.conf.hosts"
	checkHosttype "${TYPE}"
	[ ${?} -ne 0 ] && return 1
	#LINES=$(egrep "^ *host ${TYPE}[0-9]*( *|\{)" ${FILE}| awk 'BEGIN {ORS=","} { print "\""$2"\"" } ')
	LINES=$(egrep "^ *host ${TYPE}[0-9]*( *|\{)" ${FILE}| awk '{ print $2 } ')
	echo "${LINES}"
	return 0
}
