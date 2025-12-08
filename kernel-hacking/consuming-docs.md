# Consuming kernel documentation

https://lwn.net/Kernel/LDD3/ - an old book about writing device drivers

## Building docs

Building the docs requires several packages, but if the prereqs aren't installed
 ```make``` prints out the prerequisites.

make htmldocs

Other formats are ```make pdfdocs``` and ```make mandocs```, although the content
isn't the same in all formats.

The docs take a long time to build on my machine. :(

