# Openshift-related tips

## oc command line client

### multiple servers logged in at the same time

export KUBECONFIG=~/.prodkubeconfig

### delete namespace with finalizers

kubectl get namespace annoying-namespace-to-delete -o json > tmp.json

Edit tmp.json and remove "kubernetes".  The PUT it to the API directly:

curl -k -H "Content-Type: application/json" -X PUT --data-binary @tmp.json https://kubernetes-cluster-ip/api/v1/namespaces/annoying-namespace-to-delete/finalize

