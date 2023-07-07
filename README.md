# acpc-control-api
API used in the control server. <br>
* The host type means the type of host , which team|judge|print|web|pc2|cds|print|scoreboard.<br>
* host-count.cgi: Count number of mac addresses for a host type in dhcpd hosts<br>
Usage:<br>
http://ServerAddress/api/<<host type>>/count<br>
Exit codes:<br>
0: Success<br>
1: Insufficient parameters, missed host type<br>
2: Invalid host type, sent a word other than supported type<br>
3: dhcpd.conf.hosts is not found<br>
4: dhcpd.conf.hosts can not be read<br>
5: Generic error<br>
Response:<br>
In case of success, the API returns a JSON response with status code 200, and response with the number of that host defined in dhcpd.conf.hosts
Examples:<br>
/api/team/count to count the number of teams<br>
/api/judge/count to count the number of judges<br>

* host-get-ip.cgi: Retrieve the IP address of a certain host from dhcpd hosts<br>
Examples: <br>
 /api/team/2/get/ip to retrieve the ip address for the host team2<br>
 /api/judge/3/get/ip to retrieve the ip address for the host judge3<br>


