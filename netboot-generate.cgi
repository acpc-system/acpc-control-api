#!/bin/bash 
###API that generate (initrd, and vmlinuz) from an ubuntu distro
##Parameters:
##	iso: the ubuntu versoin relies in /var/www/html/iso
#### Exit codes
##	0: Success
##	1: Not enough parameters
##	4: iso file is not found
##	5: initrd has no write permission
##	6: vmlinuz has no write permission
##	7: iso file has no read permission
##	8: can not mount iso file
##	9: Can not create files in tftpboot
source checkers.sh
source create-json.sh
source common.sh
DOCROOT="/var/www/html/iso"
TFTPDIR="/acpc/tftpboot"
INITRDFILE="${TFTPDIR}/initrd"
KERNELFILE="${TFTPDIR}/vmlinuz"
echo "Content-type: application/json"
echo ""
ISOFILE=$(parseQueryString ${QUERY_STRING} "iso")
[ -z ${ISOFILE} ] && genError 100 "Insufficient parameter " 1
ISOFILE="${DOCROOT}/${ISOFILE}"
isExist "${ISOFILE}"
[ ${?} -ne 0 ] && genError 101 "ISO file is not found ${ISOFILE}" 4
isExist "${INITRDFILE}"
if [ ${?} -eq 0 ] 
then
	isWrite "${INITRDFILE}"
	[ ${?} -ne 0 ]  && genError 102 "INITRD file has no write permission" 5
fi
isExist "${KERNELFILE}"
if [ ${?} -eq 0 ] 
then
	isWrite "${KERNELFILE}"
	[ ${?} -ne 0 ] && genError 103 "KERNEL file has no write permission" 6
fi

isRead "${ISOFILE}"
[ ${?} -ne 0 ] && genError 104 "ISO file has no read permission" 7
TMPDIR=$(mktemp -d)
sudo mount -o ro "${ISOFILE}" "${TMPDIR}" 2> /dev/null
[ ${?} -ne 0 ] && genError 107 "Can not mount ISO file" 8
cp ${TMPDIR}/casper/initrd ${TMPDIR}/casper/vmlinuz ${TFTPDIR} 2> /dev/null
RES=${?}
sudo umount ${TMPDIR} 2> /dev/null
[ ${RET} -ne 0 ] && genError 104 "Can not create files in tftpboot directory" 9
rm -Rf ${TMPDIR} 2> /dev/null
initResponse
startJSON
insertJSON "status_code" I "200"
insertJSON "status_message" S "ok" 
insertJSON "response" S "generated" L
closeJSON
printJSON
exit 0
