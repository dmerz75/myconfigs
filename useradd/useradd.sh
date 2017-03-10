#!/bin/bash

# biocat
/usr/sbin/useradd -m -g users -d /data4/wittedd -s /bin/bash wittedd
passwd $USER

#!/bin/bash

# /usr/sbin/usermod -G wheel user
# usermod -aG wheel USERNAME

# /usr/bin/userdel -rf user1

# lock user:
# /etc/shadow
# user:!$1$eFd7EIOg$EeCk6XgKktWSUgi2pGUpk.:13852:0:99999:7:::
# passwd <username> -l
# passwd <username> -u
