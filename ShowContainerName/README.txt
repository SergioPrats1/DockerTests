The test on this folder creates a very simple kubernetes cluster with one NodePort service and a deployment with three containers with a web application that returns some data from the host, including the host name which is the name of the pod attending the call.

There is also a power shell script that runs 200 requests against the web app in concurrent backgroun jobs and stores the host name that has attended each request in a file called RespondingHostName.txt that is created during the process. The results show a great rotation on the pod that attends the calls.

PREREQUISITES

This test has been tested on Minikube for Windows 10.

INSTRUCTIONS

- Start Minikube, move to the folder with the config files, .\ConfigFiles,
  execute the following command to start the container:
  
  kubectl apply -f .

- Verify the Service, deployment and pods have been initialized running these commands:

  kubectl get services
  kubectl get deployments
  kubectl get pods

- Run the power shell script CallTheWebApp.ps1 and wait until the process is completed

- Check the results written at the RespondingHostName.txt file.