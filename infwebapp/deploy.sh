cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: streamlit-webapp
  namespace: dkube-kafka
spec:
  replicas: 1
  selector:
    matchLabels:
      app: streamlit-webapp
  template:
    metadata:
       labels:
         app: streamlit-webapp
    spec:
      containers:
      - name: app
        image: ocdr/streamlit-webapp:deltalake
        imagePullPolicy: Always

EOF

cat <<EOF | kubectl apply -f -
kind: Service
apiVersion: v1
metadata:
  name: streamlit-webapp
  namespace: dkube-kafka
spec:
  selector:
    app: streamlit-webapp
  ports:
  - protocol: TCP
    port: 8501
    nodePort: 31333
  type: NodePort

EOF
sleep 30s
echo "streamlit webapp is available @ <dkube-ip>:31333"
