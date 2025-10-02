# Notes on users and groups in OpenShift

See Chapter 8 of the docs https://docs.redhat.com/en/documentation/openshift_container_platform/4.8/html/authentication_and_authorization/using-rbac


There are 5 common groups, but you should probably focus on roles more.

1. cluster admins
2. project admins
3. viewers
4. system:authenticated
5. system:unauthenticated

The basic roles:

If your users should only have access to one or two projects, give them edit or view on those
projects.  If the user should be able to create projects, give them the self-provisioner role.

If your user is the cluster administrator, give them cluster-admin.


1. admin - a manager of a project
2. basic-user - pretty useless, only a bit of info about users and projects but no details
3. cluster-admin - this is what kubeadmin is
4. cluster-reader - like kubeadmin but read-only
5. edit - can modify most things but not roles or bindings.
6. self-provisioner - like edit, but with the ability to create projects
7. view - like the edit role, but can't modify


