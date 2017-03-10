#!/bin/bash

function userinfo {
    /etc/group
    /etc/passwd
    /etc/shadow
    lastlog
}
function monitoring {
    # who is a simple tool that lists out who is logged
    user@server:~>  who
    bjones   pts/0        May 23 09:33
    wally    pts/3        May 20 11:35
    aweeks   pts/1        May 22 11:03
    aweeks   pts/2        May 23 15:04

    # we can see that user aweeks is logged onto both pts/1 and pts/2, but what if we want to see what they are doing? We could to a ps -u aweeks and get the following output
    user@server:~> ps -u aweeks
    20876 pts/1    00:00:00 bash
    20904 pts/2    00:00:00 bash
    20951 pts/2    00:00:00 ssh
    21012 pts/1    00:00:00 ps
    # we can see that the user is doing a ps ssh.

    # w will print out not only who is on the system, but also the commands they are running.
    user@server:~> w
    aweeks   :0        09:32   ?xdm?  30:09   0.02s -:0
    aweeks   pts/0     09:33    5:49m  0.00s  0.82s kdeinit: kded
    aweeks   pts/2     09:35    8.00s  0.55s  0.36s vi sag-0.9.sgml
    aweeks   pts/1     15:03   59.00s  0.03s  0.03s /bin/bash

    # chsh -s /usr/local/lib/no-login/security billg
    # su - tester
    This account has been closed due to a security breach.
    Please call 555-1234 and wait for the men in black to arrive.
}

function biocat {
    # [dmerz3~]$df -h
    # Filesystem            Size  Used Avail Use% Mounted on
    # /dev/sda3             228G   40G  176G  19% /
    # /dev/sda1             122M  7.3M  108M   7% /boot
    # none                 1004M     0 1004M   0% /dev/shm
    # dq1:/data2            5.5T  4.8T  699G  88% /data2
    # nas3:/data4           7.3T  6.8T  569G  93% /data4
    # nas1:/backup          5.5T  5.2T  331G  95% /data3
    # nas5:/data5            11T  8.7T  2.2T  80% /data5

}
function library {
    # root@master:/home[167]>df -h
    # Filesystem            Size  Used Avail Use% Mounted on
    # /dev/sda3             180G  159G   12G  94% /
    # /dev/sda1             122M   21M   96M  18% /boot
    # tmpfs                 4.0G     0  4.0G   0% /dev/shm
    # /dev/sdb              3.6T  3.1T  332G  91% /data0
    # data01:/data           11T  2.5T  7.8T  24% /data01

    # root@master:/home[168]>du -h --max-depth=1
    # 52K./bashtest
    # 67M./aspensys
    # 700K./hpctest
    # 2.4M./tcshtest
    # 4.0K./lost+found
    # 60K./blake
    # 253M./srijan
    # 8.3G./pico
    # 84M./songhk
    # 27M./variyass
    # 56K./nick
    # 3.1G./pooja
    # 60K./dimar
    # 1.8G./gns
    # 56K./harshad
    # 104K./joshi
    # 516K./tadelek
    # 1.9M./darwisam
    # 317M./mrmoon
    # 781M./bodmernk
    # 108K./lewalldm
    # 25G./sam
    # 5.3G./kravatan
    # 1.1M./kim2jg
    # 271M./manori
    # 1.9G./nathan
    # 797M./wh
    # 950M./duanli
    # 56K./hw
    # 473M./rajesh
    # 56K./admin
    # 37M./bucherrn
    # 3.3M./greenjv
    # 652K./jngkim
    # 125M./lishuo
    # 7.6M./chittakr
    # 59M./kodalipd
    # 216K./schwarct
    # 18G./kehaines
    # 64K./yunhe
    # 64K./siweili
    # 64K./pratt
    # 660M./allisont
    # 2.3G./stockbm
    # 91M./mahendra
    # 6.4G./ningxi
    # 329M./anilee
    # 120M./dinhtq
    # 84K./mackenzie
    # 55M./cierra
    # 1.7G./yhshih
    # 5.3G./rui
    # 64K./yacyshgn
    # 8.0K./mckinleyjc
    # 112K./augustpowers
    # 104K./travispollard
    # 44M./emack
    # 20G./dmerz3
    # 4.1G./javidi
    # 4.9G./wq
    # 57M./nan
    # 212M./zhenhao
    # 927M./jayanth
    # 114G.
}
function gpu105 {
    # Filesystem      Size  Used Avail Use% Mounted on
    # /dev/sda1       1.8T  949G  763G  56% /
    # udev             16G  4.0K   16G   1% /dev
    # tmpfs           6.3G  312K  6.3G   1% /run
    # none            5.0M     0  5.0M   0% /run/lock
    # none             16G     0   16G   0% /run/shm
    # none            100M     0  100M   0% /run/user

    # root@ubuntu:/home# du -h --max-depth=1
    # 15G./Indentation_Files_For_Ningxi
    # 4.5G./yizhou
    # 16K./jayanth
    # 158G./nan
    # 8.4G./james
    # 215G./kehaines
    # 363G./ningxi
    # 14G./dmerz3
    # 775G.
}
function gpu24 {
    # Filesystem            Size  Used Avail Use% Mounted on
    # /dev/sda2             1.8T  1.7T  8.7G 100% /
    # none                  5.9G  268K  5.9G   1% /dev
    # none                  5.9G     0  5.9G   0% /dev/shm
    # none                  5.9G   72K  5.9G   1% /var/run
    # none                  5.9G     0  5.9G   0% /var/lock
    # none                  5.9G     0  5.9G   0% /lib/init/rw

    # Password:
    # root@ubuntu:/home/dmerz3# cd ..
    # root@ubuntu:/home# du -h --max-depth=1
    # 18G./senanabs
    # 35G./david
    # 586G./ningxi
    # 182G./Proj_gSOP_1.04
    # 3.8G./duanli
    # 29G./james
    # 24K./rajeesh
    # 7.8G./desainj
    # 1.3G./volskiam
    # 63M./test
    # 251M./nguyen
    # 12K./srijan
    # 32G./cody
    # 5.6G./nan
    # 748G./kehaines
    # 20K./zhenhao
    # 20K./nick
    # 299M./dmerz3
    # 48G./anilee
    # 20K./stockbm
    # 1.7T.
}
function gpu81 {
    # Filesystem            Size  Used Avail Use% Mounted on
    # /dev/sda1             906G  843G   17G  99% /
    # none                  2.1G  212K  2.1G   1% /dev
    # none                  2.1G     0  2.1G   0% /dev/shm
    # none                  2.1G   36K  2.1G   1% /var/run
    # none                  2.1G     0  2.1G   0% /var/lock

}
function gpu82 {
    # Filesystem            Size  Used Avail Use% Mounted on
    # /dev/sda2             1.8T  978G  731G  58% /
    # none                  5.9G  256K  5.9G   1% /dev
    # none                  5.9G     0  5.9G   0% /dev/shm
    # none                  5.9G   76K  5.9G   1% /var/run
    # none                  5.9G     0  5.9G   0% /var/lock
    # none                  5.9G     0  5.9G   0% /lib/init/rw
    # none                  1.8T  978G  731G  58% /var/lib/ureadahead/debugfs

    # Password:
    # root@ubuntu:/home# du -h --max-depth=1
    # 36K./ningxi
    # 189G./nick
    # 20K./nguyen
    # 18G./duanli
    # 709G./kehaines
    # 23G./david
    # 3.7G./nan
    # 299M./dmerz3
    # 255M./laughlrd
    # 527M./stockbm
    # 18G./senanabs
    # 20K./srijan
    # 13G./liddy
    # 36K./anilee
    # 230M./yizhou
    # 420M./desainj
    # 973G.
}
function biogate { #a
    # df: ‘/run/user/112/gvfs’: Permission denied
    # Filesystem      Size  Used Avail Use% Mounted on
    # /dev/sda1       229G   24G  194G  11% /
    # none            4.0K     0  4.0K   0% /sys/fs/cgroup
    # udev            482M  4.0K  482M   1% /dev
    # tmpfs            99M  1.1M   98M   2% /run
    # none            5.0M     0  5.0M   0% /run/lock
    # none            492M  144K  492M   1% /run/shm
    # none            100M   36K  100M   1% /run/user

    # Password:
    # root@biogate:/home# du -h --max-depth=1
    # 20K./slaughap
    # 32K./dinhtq
    # 869M./sam
    # 4.0G./ningxi
    # 84K./watson
    # 24K./lishuo
    # 56K./allisont
    # 203M./bucherrn
    # 209M./zhenhao
    # 24K./sellinux
    # 455M./javidi
    # 24K./pratt
    # 4.0K./blake
    # 981M./wh
    # 24K./kodalipd
    # 16K./bauerkk
    # 82M./pooja
    # 32K./artem
    # 59M./stefanie8532
    # 599M./gns
    # 56M./dimar
    # 8.5G./nathan
    # 40K./yhshih
    # 76K./amit
    # 268K./duanli
    # 4.0K./lost+found
    # 32K./rajesh
    # 32K./herrmazm
    # 48K./stockbm
    # 8.0K./srijan
    # 24K./jiyoung
    # 24K./greenjv
    # 66M./manori
    # 52K./kehaines
    # 32K./senanabs
    # 355M./paul
    # 20K./wq
    # 298M./tehver
    # 36K./pico
    # 101M./kravatan
    # 20K./mjtaft
    # 24K./chittakr
    # 48K./zampelke
    # 2.0G./jayanth
    # 20K./yizhou
    # 20K./maycee
    # 24K./jngkim
    # 36K./nick
    # 7.5M./rui
    # 1.5G./dmerz3
    # 20G.
}
function nas6 {
    # Filesystem            Size  Used Avail Use% Mounted on
    # /dev/sda3             857G   22G  791G   3% /
    # /dev/sda1             236M   87M  138M  39% /boot
    # none                   16G     0   16G   0% /dev/shm
    # /dev/sdb1              11T   34M   11T   1% /data6

}
