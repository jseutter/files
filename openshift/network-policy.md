# Notes about using NetworkPolicy in OpenShift

Red Hat's OpenShift documentation discribes NetworkPolicy in Chapter 3 at https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/network_security/network-policy .  Salient points:

By default, all pods can access each other across namespaces.  This is the default behavior
provided by Kubernetes.

If a pod is matched by selectors in one or more NetworkPolicy objects, the pod access is bound
by the connections allowed in those objects.

NetworkPolicy only applies to TCP, UDP, ICMP, and SCTP.  Other protocols are unaffected.

Be aware that NetworkPolicy does not apply if pods are given host network access.

The recommended way to use NetworkPolicy:

1. Make the project deny-all.

```yaml
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  name: deny-by-default
spec:
  podSelector: {}
  ingress: []
```

2. Only allow incoming connections from the cluster ingress controller.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-from-openshift-ingress
spec:
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          policy-group.network.openshift.io/ingress: ""
  podSelector: {}
  policyTypes:
  - Ingress
```

3. Only accept connections from pods in the same project.

```yaml
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  name: allow-same-namespace
spec:
  podSelector: {}
  ingress:
  - from:
    - podSelector: {}
```

These three NetworkPolicy objects together form a secure base for networking in OpenShift.  Create
these in each new project.


