# Notes on audit logging in OpenShift

In all 4.x versions, audit logging is enabled, and the logs are stored on nodes in /var/log/kube-apiserver/.

Audit logging sections in the OpenShift docs.  Chapter 12 (viewing) https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/security_and_compliance/audit-log-view#audit-log-view and Chapter 13 (configuring) https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/security_and_compliance/audit-log-policy-config#audit-log-policy-config


## Default behavior

By default, OpenShift logs metadata for read and write requests.  For OAuth it also logs request bodies.


## Viewing the audit logs

View only via the oc command, not the web interface..

```
oc adm node-logs --role=master --path=kube-apiserver/
```

followed by

```
oc adm node-logs <node_name> --path=kube-apiserver/<log_name>
```

The OAuth logs are in a different path:

```
oc adm node-logs --role=master --path=oauth-apiserver/
```



