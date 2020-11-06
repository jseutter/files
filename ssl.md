# Tips and tricks for working with SSL

## Get all certs in chain from a server:
openssl s_client -host google.com -port 443 -prexit -showcerts
