# Some notes about installing Airflow into openshift

## Fetching

Airflow publish Helm charts for k8s, they need some
tending to before they can deploy into openshift.

helm chart docs: https://airflow.apache.org/docs/helm-chart/stable/index.html

The docs are incomplete, so pull the chart down locally:

helm repo add apache-airflow https://airflow.apache.org
helm pull apache-airflow/airflow

That repo has a fully specced values.yaml which helps understand
the options available.

## Installing

The helm chart created several service accounts but they are for
running setuid containers.  Add anyuid to the service accounts:

oc adm policy add-scc-to-user anyuid -z airflow-webserver

Several parts of the install can make user of persistent volumes,
so check for pvc and pv issues if nothing seems to be working.

One part of the install relies on migrations being run via a Job.
If the Job fails due to setuid issues, delete the Job or uninstall
and try again.  There is no Job restart functionality in k8s.

## Accessing

Once the pods are running, the webserver will still be inaccessible.
Expose the service to create a route.

oc expose svc airflow-webserver

Once you can reach the login page, admin/admin is the default user.

## Using

Airflow relies on pulling DAGs (the scripts to run) from Git.  I
created a repo with a dags folder, added a hello world dag to it
and pushed.  The repo was hosted in Azure Devops, and by generating
a username/password in Azure, the Airflow scheduler was able
to pull down the git repo and run my DAG.

Pertinent section from my values.yaml file:

dags:
  persistence:
    enabled: true
    size: 1Gi
  gitSync:
    uid: null
    enabled: true
    credentialsSecret: airflow-git-creds-secret
    repo: https://xxxxx@dev.azure.com/yyyyyy/foo/_git/foo
    branch: main
    subPath: dag

extraSecrets:
  airflow-git-creds-secret:
    type: Opaque
    data: |
      # To base64 encode, echo -n "asdfusername" | base64
      # To verify, view secret in OpenShift web UI
      GIT_SYNC_USERNAME: xxxxxxxxxxxxx
      # To base64 encode, echo -n "asdfpassword" | base64
      # To verify, view secret in OpenShift web UI
      GIT_SYNC_PASSWORD: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

Note: I put my value.yaml file in my personalfiles repo
Note: This was tested using codereadycontainers on my x86 box.

