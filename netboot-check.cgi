#!/bin/bash 
###API that check (initrd, and vmlinuz) are compatibile with an ubuntu distro
##Parameters:
##	iso: the ubuntu versoin relies in /var/www/html/iso
#### Exit codes
##	0: Success
##	1: Not enough parameters
##	2: initrd is not found
##	3: vmlinuz is not found
##	4: iso file is not found
##	5: initrd has no read permission
##	6: vmlinuz has no read permission
##	7: iso file has no read permission
##	8: can not mount iso file
##	9: initrd is not compatibile with iso file
##	10: vmlinuz is not compatibile with iso file

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
[ ${?} -ne 0 ] && genError 102 "INITRD file is not found" 2
isExist "${KERNELFILE}"
[ ${?} -ne 0 ] && genError 103 "KERNEL file is not found" 3
isRead "${ISOFILE}"
[ ${?} -ne 0 ] && genError 104 "ISO file has no read permission" 7
isRead "${INITRDFILE}"
[ ${?} -ne 0 ] && genError 105 "INITRD file has no read permission" 5
isRead "${KERNELFILE}"
[ ${?} -ne 0 ] && genError 106 "KERNEL file has no read permission" 6
TMPDIR=$(mktemp -d)
sudo mount -o ro "${ISOFILE}" "${TMPDIR}" 2> /dev/null
[ ${?} -ne 0 ] && genError 107 "Can not mount ISO file" 8
TFTPINITRDMD5=$(openssl dgst -md5 "${INITRDFILE}" | awk ' BEGIN { FS="= " } { print $2 } ')
ISOINITRDMD5=$(openssl dgst -md5 "${TMPDIR}/casper/initrd" | awk ' BEGIN { FS="= " } { print $2 } ')
TFTPKERNELMD5=$(openssl dgst -md5 "${KERNELFILE}" | awk ' BEGIN { FS="= " } { print $2 } ')
ISOKERNELMD5=$(openssl dgst -md5 "${TMPDIR}/casper/vmlinuz" | awk ' BEGIN { FS="= " } { print $2 } ')
sudo umount ${TMPDIR} 2> /dev/null
rm -Rf ${TMPDIR} 2> /dev/null
[ "${TFTPINITRDMD5}" != "${ISOINITRDMD5}" ] && genError 107 "INITRD file is not compatibile" 9
[ "${TFTPKERNELMD5}" != "${ISOKERNELMD5}" ] && genError 107 "KERNEL file is not compatibile" 10
initResponse
startJSON
insertJSON "status_code" I "200"
insertJSON "status_message" S "ok" 
insertJSON "response" S "compatible" L
closeJSON
printJSON
exit 0
