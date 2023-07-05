### Script contains all mac/ip address operations needed

## Function takes an host and prints out its IP,
#       Returns:
#               0: Success
#               1: Invalid host
##      Accepts:
        #one parameters, the host name
function getIP() {
        FILE="/acpc/adm/etc/dhcp/dhcpd.conf.hosts"
        local HOSTID="${1}"
        ##1-Get the line number contains the pattern host team{id}
        local LINEN=$(grep -n "^host *${HOSTID} " ${FILE} | cut -d: -f1)
        [ -z ${LINEN} ] && return  1
        ## Now, we have the line number grep the line contains mac address after this line
        local IP=$(tail -n +${LINEN} ${FILE} |grep "fixed-address" | head -1 | awk ' { print $2 }'| sed 's/;//g')
        echo "${IP}"
        return 0
}

