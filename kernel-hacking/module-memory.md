# Creating a module that uses memory

After successfully testing the minimal kernel module, it's time to add some functionality.
I'd like to have a character device that will store some string sent in from user space
and retain it for reading later.  This tests my ability to allocate memory as well as
transferring data between user space and kernel space.

The documentation for kernel memory management is here: https://docs.kernel.org/core-api/memory-allocation.html.
Calls are differentiated based on the amount of memory they need, location restrictions
for DMA use, and other factors.  In my case I will only be allocating a small amount
of RAM so the kmalloc() and kzalloc() functions are ideal.

```void *kzalloc(size_t size, gfp_t flags)```

```gfp_t flags``` is a set of flags that indicate special needs for memory, like if
it is relocatable.  ```GFP_KERNEL``` is the most common and implies ```GFP_RECLAIM```,
which means that under memory pressure, the calling context that makes the kmalloc() call (ie: us)
can sleep until memory comes available and the call succeeds.  This is fine for my use
case as we don't have anything with hard requirements like data coming in over a wire.

The companion call to ```kmalloc``` is ```kfree```.

```void kfree(const void *object)```

## Transferring data between user space and kernel space

For this initial version I'll have a single variable in my driver:

```static void *buf = NULL;```

But how do I know that the user has done something like ```echo foo | /dev/scull```.
Backing up for a minute, how do I register my driver as listening to /dev/scull?
This information seems to be explained in chapter 3 of the book hosted on lwn.net.

## Registering a device



## Serving Documentation/output folder with Python
python3 -m http.server 8000


## copy_to_user() / copy_from_user()
- for single values such as ints or chars use put_user() / get_user()
 A pointer into userspace should never be simply dereferenced: data should be
 copied using these strings.  Both return -EFAULT or 0.
- for copying arbitrary data use copy_to_user() and copy_from_user().  These
 return the amount of uncopied data.  0 still means success.  This is a known
 bad interface.
- these functions may sleep implicitly, should never be called outside user
 context, or with interrupts disabled, or with a spinlock held

static inline int copy_from_user(void *to, const void __user volatile *from,
                                 unsigned long n)
{
        volatile_memcpy(to, from, n);
        return 0;
}

- The documentation about these functions appears to be out of date, as it
 appears to me that they will always return 0.  There are assembly versions
 of the functions, so it's possible they act differently on different
 platforms.

Now that we have code written to copy to and from userspace to our buffer,
let's test it.

## The character device

In order to support writes and reads we need to listen to a character
device.  For now we're going to ask the kernel to allocate us one.  These
functions apply:

```result = alloc_chrdev_region(&dev_num, 0, 1, DEVICE_NAME);```

```unregister_chrdev_region(dev_num, 1);```

When we call alloc_chrdev_region the linux kernel will give us a free
Major number of its choosing.  We'll print this out to dmesg with something
like this:

```pr_info("Scull3: Loaded.  Major: %d.", MAJOR(dev_num));```

With this number we can call mknod to create the device on our filesystem.

When we boot linux, we need a character device for userspace to interact with.
Normally this would be something like /dev/scull3 but there is no hard
requirement.  For quick and dirty testing I create the device in whatever
current directory I'm in:

```dmesg | grep -i scull```
```mknod s c 250 0```

The dmesg output from our scull driver shows us the Major number the
kernel has assigned us, which seems to be always 250.  The Minor number
is just an increasing integer to discriminate between devices, so start
at 0.  The name of the device is "s", and it is of type (c)haracter.
So now we should be able to run this:

```echo "hello world!" > s```

```cat s```

..which repeats "hello world!" back to us.  Success!


# Creating the character device

(my-scull4.c)

In the last step we had to manually create the device using mknod.
With a few more lines of code we can have the driver do it for us.

First is a call to create the class:

```scull_class = class_create(DEVICE_NAME);```

Followed by a call to create the device:

```device_create(scull_class, NULL, dev_num, NULL, DEVICE_NAME)```

Now when we test our kernel we can look for the dmesg line
that prints out the Major for the device (usually 250) and
grep for that in ```ls -al /dev```.

```
/ # ls -la /dev | grep 249
crw-------    1 0        0         249,   0 Dec  7 05:07 scull4
```

..and reads and writes continue to work as before.



