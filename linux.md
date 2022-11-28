# Linux tips

## Mounting files
Problem: I have an SSD drive formatted with exfat.  When I plug it into my pi, I want files
on it to be owned by datauser:datausers.  I do not want other drives to be confused
with this one.

Solution:
- Most distributions have lsblk, which lists block devices.
- blkid /dev/sda2 gives a drive UUID.  I think this only showed up after I labelled the drive below.
- cat /proc/mounts to see what drives have been automounted
- Give the drive a label with exfatlabel
 - sudo umount /dev/sda2
 - sudo exfatlabel /dev/sda2 NETAC256GB
 - Now when I replug the drive, it mounts in /media/pi/NETAC256GB
- To give access to a specific user, you have to use /etc/fstab mounting.
blkid /dev/sda2
/dev/sda2: LABEL="NETAC256GB" UUID="1A26-82F0" TYPE="exfat" PARTLABEL="Basic data partition" PARTUUID="0e69cb7b-14f9-421a-b0a0-b979c5375427"
Keep track of the UUID and TYPE.
/dev/sda2 /media/pi/NETAC256GB fuseblk rw,nosuid,nodev,relatime,user_id=0,group_id=0,default_permissions,allow_other,blksize=4096 0 0


## Photo organizing
digikam

## Raspberry pi terminal
lxterminal

## Fedora libvirt

dnf groupinfo virtualization

sudo dnf install @virtualization

from https://docs.fedoraproject.org/en-US/quick-docs/getting-started-with-virtualization/

