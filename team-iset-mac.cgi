#!/bin/bash
###API that set a mac address for certain team from /acpc/adm/etc/dhcp/dhcpd.conf.hosts
##	The API uses POST method, and accept id parameter
#### Exit codes
##	0: Success
##	1: Insufficient parameter
##	2: ID is not an integer
##	3: dhcp hosts file does not exist
##	4: dhcp hosts file does not have read permission
##	5: dhcp hosts file does not have write permission
##	6: team is not valid (not exists in dhcpd.conf.hosts)
##	7: passed mac address is not a valid mac
##	8: Error in replace operation
#!/bin/bash

exec 2>/dev/null    # We dont want any error messages be printed to stdout
trap "response_with_html && exit 0" ERR    # response with an html message when an error occurred and close the script

function response_with_html(){
    echo "Content-type: text/html"
    echo ""
    echo "<!DOCTYPE html>"
    echo "<html><head>"
    echo "<title>456</title>"
    echo "</head><body>"
    echo "<h1>456</h1>"
    echo "<p>Attempt to communicate with the server went wrong.</p>"
    echo "<hr>"
    echo "$SERVER_SIGNATURE"
    echo "</body></html>"
}

function response_with_json(){
    echo "Content-type: application/json"
    echo ""
    echo "{\"message\": \"Hello World!\"}"
}

function response_with_json1(){
    local V=$(/acpc/adm/bin/wrapper "touch /tmp/x")
    echo "Content-type: application/json"
    echo ""
    echo "{\"message\": \"$(whoami) , ${V}\"}"
}



if [ "$REQUEST_METHOD" = "POST" ]; then

    # The environment variabe $CONTENT_TYPE describes the data-type received
    case "$CONTENT_TYPE" in
    application/json)
        # The environment variabe $CONTENT_LENGTH describes the size of the data
        read -n "$CONTENT_LENGTH" QUERY_STRING_POST        # read datastream

        # The following lines will prevent XSS and check for valide JSON-Data.
        # But these Symbols need to be encoded somehow before sending to this script
        QUERY_STRING_POST=$(echo "$QUERY_STRING_POST" | sed "s/'//g" | sed 's/\$//g;s/`//g;s/\*//g;s/\\//g' )        # removes some symbols (like \ * ` $ ') to prevent XSS with Bash and SQL.
        QUERY_STRING_POST=$(echo "$QUERY_STRING_POST" | sed -e :a -e 's/<[^>]*>//g;/</N;//ba')    # removes most html declarations to prevent XSS within documents
        JSON=$(echo "$QUERY_STRING_POST" | jq .)        # json encode - This is a pretty save way to check for valide json code
    ;;
    *)
        response_with_html
        exit 0
    ;;
    esac

else
    response_with_html
    exit 0
fi

# Some Commands ...
if [ ${?} -ne 0 ]
then
	response_with_json1
else

response_with_json1
fi

exit 0
