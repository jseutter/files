# This use the OpenShift command line interface operator as a template, and
# creates a pod that lives forever.  Useful for when you don't have a reasonable
# command line environment any other way.  Presumable the SHA won't be the same,
# so you'll have to get a current one from a pod running via the operator.
# This also mounts a PVC that you must create beforehand.

apiVersion: apps/v1
kind: Deployment
metadata:
  name: persistent-cli
  namespace: js-test
spec:
  replicas: 1
  selector:
    matchLabels:
      app: persistent-cli
  template:
    metadata:
      labels:
        app: persistent-cli
    spec:
      containers:
      - name: terminal
        image: registry.redhat.io/web-terminal/web-terminal-tooling-rhel9@sha256:7af65ee06f1e8038b54dfd669910d7b7964ec89b03a5167601b86902561339cb
        # Keeps the container running indefinitely
        command: ["/bin/sh", "-c", "tail -f /dev/null"]
        volumeMounts:
        - name: workspace-storage
          mountPath: /home/user/pvc
        resources:
          limits:
            cpu: "500m"
            memory: "1Gi"
          requests:
            cpu: "100m"
            memory: "256Mi"
      volumes:
      - name: workspace-storage
        persistentVolumeClaim:
          claimName: js-workingspace
