# Openshift-related tips

## oc command line client

### multiple servers logged in at the same time

export KUBECONFIG=~/.prodkubeconfig

### delete namespace with finalizers

kubectl get namespace annoying-namespace-to-delete -o json > tmp.json

Edit tmp.json and remove "kubernetes".  The PUT it to the API directly:

curl -k -H "Content-Type: application/json" -X PUT --data-binary @tmp.json https://kubernetes-cluster-ip/api/v1/namespaces/annoying-namespace-to-delete/finalize

## Example applications

### Hello world webserver

oc new-app --template=openshift/nginx-example --name=my-nginx-example --param=NAME=my-nginx-example

..then expose it with a new route, foo.xvdemo.net.  Use the UI for this.

Then create a DNS CNAME record for foo.xvdemo.net, pointing to my-nginx-example-foo.apps.test.xvdemo.net.
Be aware that the UI hint is misleading for this.

Wait 72 hours, or modify your machine to point to the DNS server that gets an early update.

Once this is working, recreate the route, this time with an SSL certificate.

## Code Ready Containers

### Code Ready Containers on remote machine

Problem: You want to run CRC on its own machine.  OpenShift uses fancy DNS so connecting to it from
another machine won't work out of the box.

Solution: Run Tinyproxy on the CRC machine.  port forward ssh from your dev machine to the CRC machine.
In your browser, set the proxy to be the forwarded port.

yum -y install tinyproxy; systemctl start tinyproxy
ssh -L 8888:127.0.0.1:8888 crc-machine.local

Finally in firefox, make 127.0.0.1 port 8888 be your proxy, and enable for https as well.  This leaves
Chrome untouched for regular browsing.

Decoding secrets:
kubectl get secret name-of-secret -o go-template='
{{range $k,$v := .data}}{{printf "%s: " $k}}{{if not $v}}{{$v}}{{else}}{{$v | base64decode}}{{end}}{{"\n"}}{{end}}'

