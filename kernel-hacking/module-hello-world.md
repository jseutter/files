# Making a hello world kernel module

Backing off from Rust kernel development for a minute, I figured it's a good idea to
understand how kernel modules are normally made.  In looking for guidance, I found
"The Linux Kernel Module Programming Guide", which has a section on creating a simple
kernel module.

Link: https://sysprog21.github.io/lkmpg/


Some notable facts:
- kernel modules can be in-tree (in the linux kernel source) or out-of-tree (outside
  the linux kernel source).
- A single file can be a kernel module, as long as it makes the right calls.
- A simple Makefile can compile a module against your system kernel

Their example worked well enough on my Ubuntu 25.10 system.

Source file: https://github.com/jseutter/kernel-hacking/blob/main/hello-world-module/hello-2.c
Makefile: https://github.com/jseutter/kernel-hacking/blob/main/hello-world-module/Makefile-for-host-os-compile

Testing it, I was able to insmod and rmmod successfully on my system.  However, for
my serious development I want to test the module against a current kernel in qemu.
I had to do this:

- Change the Makefile with the path to my kernel tree.
- Fix module initialization.  The init_module() and cleanup_module() functions are no
  longer supported and have been replaced by functions called ```module_init(fun_name)``` and
  ```module_exit(fun_name)```
- Copy the .ko module into my initrd.img


Once I had this done, I booted up my kernel in qemu and was able to insmod/rmmod
the module.  Success!

# Understanding the build process

I don't understand how this Makefile for my out-of-tree driver works:

```
obj-m += hello-2.o

TARGET_KERNEL_DIR := ../linux

PWD := $(CURDIR)

all:
        $(MAKE) -C $(TARGET_KERNEL_DIR) M=$(PWD) modules
clean:
        $(MAKE) -C $(TARGET_KERNEL_DIR) M=$(PWD) clean
```

..and I invoke it with ```make```.  How does it know I'm building a kernel module?

The answer is, it sort of doesn't know.  All it is doing is executing the all: target.
```make -C ../linux``` tells make to change to that directory and act as
if I invoked it from that directory.  ```../linux``` is my source tree and has all
the fancy Makefile stuff for building the kernel.  Ah!

The next arg, ```M=hello-world-module```, tells make to compile the source files
in my current directory (where my module source files are).

But this highlights something I never figured out in 30 years of casual Make usage:
when make recursively calls itself, the variables found by the current make process
get passed into the child make process.  Apparently this has been the case since
approximately forever.  The recursively-called make in the ../linux directory knows
how to do proper compilation.  Elegant!

The ```M=``` and ```obj-m=``` variables are part of the linux Kbuild system.

Note that kbuild has documentation in the kernel source tree.  See
Documentation/kubild/makefiles.rst and search for "obj-m".  "obj-y"
apparently compiles it into the kernel.  These letters match the ones in ```make menuconfig```,
where 'y' means to compile it into the kernel, and 'm' means build it as a module.

