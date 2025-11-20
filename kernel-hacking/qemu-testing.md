# Testing the built kernel image with qemu

The Rust development tutorial I watched used a qemu image from Google for hacking.
To test the kernel, they instructed you to run a nested qemu instance, but it doesn't
specify a filesystem, or so I thought.

For reference, here is the qemu command:

```qemu-system-x86_64 -nographic -kernel vmlinux -initrd initrd.img -nic user,model=rtl8139,hostfwd=tcp::5555-:23```

The two things it specifies are vmlinux, the kernel I just built, and initrd.img,
which is always used when booting a kernel.  initrd.img looks like some kind of magic.

Turns out initrd.img is a filesystem.  It is compressed with gzip, and is a cpio archive.
To look at it:

Step 1: Make a junk directory, and copy initrd.img into it.
```
mkdir initrd-files
cd initrd-files
cp ../initrd.img .
```

Step 2: Uncompress.
```
mv initrd.img initrd.img.gz
gunzip initrd.img.gz
```

Step 3: Extract the cpio archive
```
cat initrd.img | cpio -idmv
```

..and the files are exposed in the current directory.  Looking into how this system
works, it has its own init script.  For background, init is the first process that
runs when a linux system starts up (in the case of systemd, this would be systemd
init).  The /etc/init.d/rcS script:

```
#!bin/sh
mount -t proc none /proc
mount -t sysfs none /sys
mount -t devtmpfs none /dev
mkdir /dev/pts
mount -t devpts none /dev/pts
ifconfig lo up
udhcpc -i eth0
telnetd -l /bin/sh
acpid
```

- Mounting the proc filesystem provides the ability to get infromation about tasks in /proc.
- Mounting the sysfs filesystem gives information about hardware devices in /sys, which
  is used by things like udev or ifconfig.
- Mounting the devtmpfs filesystem gives functionality about devices, so like /dev/tty,
  /dev/sda and so on.
- The /dev/pts are the pseudo-terminals, which are needed for virtual terminals.
- The lo and eth0 lines are for the loopback device and requesting a dhcp address from
  the qemu networking service.
- The telnetd line starts the telnet daemon, so that when something connects it starts
  up a shell session.
- The acpid line isn't strictly needed, but listens for power events from qemu.  Most
  of the time I just use ```poweroff``` from the terminal instead.

The result of this is you can test a kernel in a few seconds:

```
<snip>
udhcpc: broadcasting select for 10.0.2.15, server 10.0.2.2
udhcpc: lease of 10.0.2.15 obtained from 10.0.2.2, lease time 86400
Setting IP address 10.0.2.15 on eth0
Deleting routers
route: SIOCDELRT: No such process
Adding router 10.0.2.2
Recreating /etc/resolv.conf
 Adding DNS server 10.0.2.3
[    1.605723] tsc: Refined TSC clocksource calibration: 3499.649 MHz
[    1.606583] clocksource: tsc: mask: 0xffffffffffffffff max_cycles: 0x327205aef5e, max_idle_ns: 440795352906 ns
[    1.607368] clocksource: Switched to clocksource tsc
/ # uname -a
Linux (none) 6.3.0+ #19 SMP Wed Nov 12 03:16:19 UTC 2025 x86_64 GNU/Linux
/ # poweroff
```

Armed with this knowledge, I should be able to take this initrd file to any computer and quickly test
a built linux kernel.

## Testing

The kernel newbies image I used is a few years old and a few things have changed.  On an Ubuntu 25.10 development
machine, I had to use this:

```
qemu-system-x86_64 -nographic -kernel arch/x86/boot/bzImage -initrd initrd.img -append "console=ttyS0 rdinit=/sbin/init"
```

- A make defconfig kernel doesn't create a vmlinuz, just a vmlinux.  I had to switch to using bzImage instead.
- I dropped the port forwarding for now, I'll add it back later.
- console=ttyS0 - I'm not sure why this is here, perhaps test without it?
- rdinit=/sbin/init.  When I look at the source it looks like the kernel should try this path, but it doesn't.
  For reference, /sbin/init exists in initrd.img and is the first thing to run after the kernel boots.

At any rate, I can now test a mainline linux kernel quickly without trashing my development system.  Success!

