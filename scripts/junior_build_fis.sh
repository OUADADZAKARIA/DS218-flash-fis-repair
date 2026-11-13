#!/bin/sh
# À coller dans le shell BusyBox du mode junior (ligne par ligne ou en bloc).
# Généré par build_fis.py --busybox. N'écrit rien dans la flash.
# Construit /tmp/fis_new.bin (4096 octets) dans la RAM du NAS. N'écrit rien dans la flash.
i=0; while [ $i -lt 4096 ]; do printf '\377'; i=$((i+1)); done > /tmp/ff4k
rm -f /tmp/fis_new.bin
{ printf '\122\145\144\102\157\157\164\000\000\000\000\000\000\000\000\000'; printf '\000\000\000\000\000\000\000\000\000\000\020\000\000\000\000\000\000\000\020\000'; dd if=/tmp/ff4k bs=1 count=212 2>/dev/null; printf '\000\000\000\000\000\000\000\000'; } >> /tmp/fis_new.bin
{ printf '\172\111\155\141\147\145\000\000\000\000\000\000\000\000\000\000'; printf '\000\000\020\000\000\000\000\000\000\000\057\000\000\000\000\000\000\000\057\000'; dd if=/tmp/ff4k bs=1 count=212 2>/dev/null; printf '\000\000\000\000\000\000\000\000'; } >> /tmp/fis_new.bin
{ printf '\162\144\056\147\172\000\000\000\000\000\000\000\000\000\000\000'; printf '\000\000\077\000\000\000\000\000\000\360\077\000\000\000\000\000\000\360\077\000'; dd if=/tmp/ff4k bs=1 count=212 2>/dev/null; printf '\000\000\000\000\000\000\000\000'; } >> /tmp/fis_new.bin
{ printf '\166\145\156\144\157\162\000\000\000\000\000\000\000\000\000\000'; printf '\000\360\176\000\000\000\000\000\000\000\001\000\000\000\000\000\000\000\001\000'; dd if=/tmp/ff4k bs=1 count=212 2>/dev/null; printf '\000\000\000\000\000\000\000\000'; } >> /tmp/fis_new.bin
{ printf '\106\111\123\040\144\151\162\145\143\164\157\162\171\000\000\000'; printf '\000\360\177\000\000\000\000\000\000\020\000\000\000\000\000\000\000\020\000\000'; dd if=/tmp/ff4k bs=1 count=212 2>/dev/null; printf '\000\000\000\000\000\000\000\000'; } >> /tmp/fis_new.bin
dd if=/tmp/ff4k bs=1 count=2816 2>/dev/null >> /tmp/fis_new.bin
ls -l /tmp/fis_new.bin   # doit afficher exactement 4096
