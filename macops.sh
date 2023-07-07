### Script contains all mac address operations needed

## Function takes an host and prints out its mac,
#	Returns:
#		0: Success
#		1: Invalid host
##	Accepts:
	#one parameters, the host name
function getMAC() {
	FILE="/acpc/adm/etc/dhcp/dhcpd.conf.hosts"
	local HOSTID="${1}"
	##1-Get the line number contains the pattern host team{id}
	local LINEN=$(grep -n "^host *${HOSTID} " ${FILE} | cut -d: -f1)
	[ -z ${LINEN} ] && return  1
	## Now, we have the line number grep the line contains mac address after this line
	local MAC=$(tail -n +${LINEN} ${FILE} |grep "hardware ethernet" | head -1 | awk ' { print $3 }'| sed 's/;//g')
	echo "${MAC}"
	return 0
}


##Function search for a MAC, return 0 if MAC not exists, 1 exits
function findMAC() {
        local MAC="${1}"
        FILE="/acpc/adm/etc/dhcp/dhcpd.conf.hosts"
        return $(egrep -c " ${MAC}( +|;)" ${FILE})
}

