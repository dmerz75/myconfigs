#!/bin/bash

secure_all () {
    for i in /home/*;
    do
        echo $i;
        chmod 700 $i;
        # # drwx------  2 root   root   16K Dec 26 19:03 lost+found/
        # # drwx------  3 user1  users 4.0K Feb 23 15:43 user1/
        # # drwx------ 37 dmerz3 users 4.0K Feb 23 15:45 dmerz3/

        # chmod 750 $i;
        # # drwxr-x---  2 root   root   16K Dec 26 19:03 lost+found/
        # # drwxr-x---  3 user1  users 4.0K Feb 23 15:43 user1/
        # # drwxr-x--- 37 dmerz3 users 4.0K Feb 23 15:43 dmerz3/

        # chmod 770 $i;
        # # drwxrwx---  2 root   root   16K Dec 26 19:03 lost+found/
        # # drwxrwx---  3 user1  users 4.0K Feb 23 15:43 user1/
        # # drwxrwx--- 37 dmerz3 users 4.0K Feb 23 15:45 dmerz3/

        # chmod 755 $i;
        # # drwxr-xr-x  2 root   root   16K Dec 26 19:03 lost+found/
        # # drwxr-xr-x  3 user1  users 4.0K Feb 23 15:43 user1/
        # # drwxr-xr-x 37 dmerz3 users 4.0K Feb 23 15:45 dmerz3/
    done
}
secure_biocat () {
    for i in /data4/*;
    do
        echo $i
        chmod 750 $i;
    done
}




# change /etc/profile
# from default: 0022 ->
# umask 027


# umask value   Security level  Effective permission (directory)
# 022   Permissive  755
# 026   Moderate    751
# 027   Moderate    750
# 077   Severe      700


# --------------- RUN HERE --------------------------------------
secure_all
