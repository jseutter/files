# Notes on configuring integration with Active Directory

This is done by configuring an LDAP identity provider in OpenShift, because AD is an LDAP implementation.

There are two parts to this - LDAP for authentication and LDAP for group synchronization.

OpenShift docs chapter 7.3 document this procedure https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/authentication_and_authorization/configuring-identity-providers

The web interface has a good way to configure LDAP.  Go to Administration -> Cluster Settings
-> Configuration tab, and search for OAuth.


## Syncing LDAP groups

See Chapter 19 of docs: https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/authentication_and_authorization/ldap-syncing

LDAP group sync supports AD schema and augmented AD schema.  Augmented is recommended
because it supports nested groups.

LDAPSyncConfig is the object that needs to be configured.  See the docs for details.

Run it with ```oc adm groups sync --sync-config=config.yaml --confirm```.

This process can be automated if desired with a cron job.  Directions in the docs.

