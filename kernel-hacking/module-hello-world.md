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

Note: link to source file and makefile here.

Testing it, I was able to insmod and rmmod successfully on my system.  However, for
my serious development I want to test the module against a current kernel in qemu.
I had to do this:

- Change the Makefile with the path to my kernel tree.
- Fix module initialization.  The init_module() and cleanup_module() functions are no
  longer supported and have been replaced by more flexible macros called ```__init``` and
  ```__exit```
- Copy the .ko module into my initrd.img


Once I had this done, I booted up my kernel in qemu and was able to insmod/rmmod
the module.  Success!


