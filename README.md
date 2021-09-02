# Solution to the assignment problem

*******************************************************************************************

## **Phase 1: Creating basic infrastructure**

1. Created Amazon EKS cluster for deployment testing and automation

2. Create nodegroup with 3 nodes

3. Updated local kubectl with the cluster kubeconfig using the command

  aws eks --region us-east-2 update-kubeconfig --name 	devopsassigncluster 

4. Connected to the cluster and verified

```
 kubectl get nodes
NAME                                          STATUS   ROLES    AGE     VERSION
ip-172-31-13-159.us-east-2.compute.internal   Ready    <none>   2d17h   v1.21.2-eks-c1718fb
ip-172-31-25-62.us-east-2.compute.internal    Ready    <none>   2d17h   v1.21.2-eks-c1718fb
ip-172-31-42-152.us-east-2.compute.internal   Ready    <none>   2d17h   v1.21.2-eks-c1718fb

```

5. Installed all basic softwares on my centralized EC2 instance like git, docker, kubectl and also configured AWS CLI using credentials.

************************************************************************************************


## **Phase 2: Writing the REST API code in Python**

1. Created getjson.py (code submitted in repository)
```
import flask
import requests
import yaml
import jsonify
import json
app = flask.Flask(__name__)
app.config["DEBUG"] = True

a = {'Status':'I am healthy' }
python2json = json.dumps(a)
@app.route('/health', methods=['GET'])
def health():
    return "Healthy"

@app.route("/getStatus", methods=["GET"])
def starting_url():
    mystatus = "Healthy"
    return python2json

app.run(host="0.0.0.0", port=8080)

@app.route('/data', methods=['GET'])
def getData():
    response = requests.get(cfg["url"]["prefix"] + "://" + cfg["url"]["host"] + ":" + cfg["url"]["port"] + "/" + cfg["url"]["path"])
    print(response.content)
    return response.content

app.run(host='0.0.0.0')
```

2. Opened Port 8080 on security group to access the application directly

3. Launched the application and test the functionality

```
 python3 getjson.py
 * Serving Flask app 'getjson' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on all addresses.
   WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://172.31.24.4:8080/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 446-529-565
103.208.69.134 - - [02/Sep/2021 09:06:08] "GET /getStatus HTTP/1.1" 200 -

curl http://18.224.151.69:8080/getStatus
{"Status": "I am healthy"}
``` 

4. Created the another Python service which invokes this API with name calljson.py

```
import json
import requests
import urllib
from urllib.request import urlopen
json_url = urlopen('http://18.224.151.69:8080/getStatus')
data = json.loads(json_url.read())
print(data)

``` 

5. Validating the callPython service and testing out

```
python3 calljson.py
{'Status': 'I am healthy'}

```
************************************************************************************************

## **Phase 3: Creating the custom images for both the services**

1. Created the Dockerfile code for containerizing 

```
[root@ip-172-31-21-28 pythonwebserver]# cat Dockerfile
FROM python:3
RUN pip3 install flask requests jsonify pyjson pyyaml
COPY getjson.py .
EXPOSE 8080
CMD [ "python3", "getjson.py" ]
```

2. docker build -t pythonhttpserver .

```
 docker build -t getjsonimage .
Sending build context to Docker daemon  3.584kB
Step 1/5 : FROM python:3
 ---> 6f1289b1e6a1
Step 2/5 : RUN pip3 install flask requests jsonify pyjson pyyaml
 ---> Running in 5d3a8e5cea7b
Collecting flask
  Downloading Flask-2.0.1-py3-none-any.whl (94 kB)
Collecting requests
  Downloading requests-2.26.0-py2.py3-none-any.whl (62 kB)
Collecting jsonify
  Downloading jsonify-0.5.tar.gz (1.0 kB)
Collecting pyjson
  Downloading pyjson-1.3.0-py3-none-any.whl (4.8 kB)
Collecting pyyaml
  Downloading PyYAML-5.4.1-cp39-cp39-manylinux1_x86_64.whl (630 kB)
Collecting Jinja2>=3.0
  Downloading Jinja2-3.0.1-py3-none-any.whl (133 kB)
Collecting itsdangerous>=2.0
  Downloading itsdangerous-2.0.1-py3-none-any.whl (18 kB)
Collecting click>=7.1.2
  Downloading click-8.0.1-py3-none-any.whl (97 kB)
Collecting Werkzeug>=2.0
  Downloading Werkzeug-2.0.1-py3-none-any.whl (288 kB)
Collecting idna<4,>=2.5
  Downloading idna-3.2-py3-none-any.whl (59 kB)
Collecting urllib3<1.27,>=1.21.1
  Downloading urllib3-1.26.6-py2.py3-none-any.whl (138 kB)
Collecting charset-normalizer~=2.0.0
  Downloading charset_normalizer-2.0.4-py3-none-any.whl (36 kB)
Collecting certifi>=2017.4.17
  Downloading certifi-2021.5.30-py2.py3-none-any.whl (145 kB)
Collecting MarkupSafe>=2.0
  Downloading MarkupSafe-2.0.1-cp39-cp39-manylinux_2_5_x86_64.manylinux1_x86_64.manylinux_2_12_x86_64.manylinux2010_x86_64.whl (30 kB)
Building wheels for collected packages: jsonify
  Building wheel for jsonify (setup.py): started
  Building wheel for jsonify (setup.py): finished with status 'done'
  Created wheel for jsonify: filename=jsonify-0.5-py3-none-any.whl size=1562 sha256=129109d290e01527e5ad7c1bdaaef0164ccc37a05dcc9fa0d9b4301c8fca26d1
  Stored in directory: /root/.cache/pip/wheels/4b/3c/1d/2237365baac7c6e922b81a3d1775d070c09b48cdc31b1a7c0e
Successfully built jsonify
Installing collected packages: MarkupSafe, Werkzeug, urllib3, Jinja2, itsdangerous, idna, click, charset-normalizer, certifi, requests, pyyaml, pyjson, jsonify, flask
Successfully installed Jinja2-3.0.1 MarkupSafe-2.0.1 Werkzeug-2.0.1 certifi-2021.5.30 charset-normalizer-2.0.4 click-8.0.1 flask-2.0.1 idna-3.2 itsdangerous-2.0.1 jsonify-0.5 pyjson-1.3.0 pyyaml-5.4.1 requests-2.26.0 urllib3-1.26.6
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
Removing intermediate container 5d3a8e5cea7b
 ---> 7a7b49a788fc
Step 3/5 : COPY getjson.py .
 ---> ed03487d859e
Step 4/5 : EXPOSE 8080
 ---> Running in 9e09ab2e175f
Removing intermediate container 9e09ab2e175f
 ---> e91349451189
Step 5/5 : CMD [ "python3", "getjson.py" ]
 ---> Running in 707f32d8bddc
Removing intermediate container 707f32d8bddc
 ---> ea31da3789c2
Successfully built ea31da3789c2
Successfully tagged getjsonimage:latest
```
 

3. Verified if the images are created correctly 
```
 docker images
REPOSITORY      TAG       IMAGE ID       CREATED          SIZE
calljsonimage   latest    f63072395f7b   10 seconds ago   929MB
getjsonimage    latest    ea31da3789c2   4 minutes ago    929MB
<none>          <none>    da691dfec0dd   5 minutes ago    926MB
<none>          <none>    766cc2acf04b   8 minutes ago    911MB
python          3         6f1289b1e6a1   38 hours ago     911MB
```

4. Executed the image to verify its running correctly

```
docker run  -t -i -p 8080:8080 getjsonimage
 * Serving Flask app 'getjson' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on all addresses.
   WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://172.17.0.2:8080/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 881-100-644
103.208.69.134 - - [02/Sep/2021 08:42:09] "GET /getStatus HTTP/1.1" 200 -

```

5. Access the webserver from outside, used port forwarding to connect to container and verified logs

6. Followed similar steps for callpython.py and created the image and tested it out

***************************************************************************************************

## **Phase 4: Creating the repository and push images, create Deployments**

1. Created the AWS ECR repository using command below
```
aws ecr create-repository \
>   --repository-name devopsec-assignment-ecr \
>   --image-scanning-configuration scanOnPush=true \
>   --region us-east-2
{
    "repository": {
        "repositoryUri": "618873054107.dkr.ecr.us-east-2.amazonaws.com/devopsec-assignment-ecr",
        "imageScanningConfiguration": {
            "scanOnPush": true
        },
        "encryptionConfiguration": {
            "encryptionType": "AES256"
        },
        "registryId": "618873054107",
        "imageTagMutability": "MUTABLE",
        "repositoryArn": "arn:aws:ecr:us-east-2:618873054107:repository/devopsec-assignment-ecr",
        "repositoryName": "devopsec-assignment-ecr",
        "createdAt": 1630574761.0
    }
}

```

2. Tag the image and push it to the repo
```
docker tag getjsonimage:latest 618873054107.dkr.ecr.us-east-2.amazonaws.com/devopsec-assignment-ecr:getjsoncode ( Get service)
docker tag calljsonimage:latest 618873054107.dkr.ecr.us-east-2.amazonaws.com/devopsec-assignment-ecr:calljsoncode (Calling service)

```

3. Perform the docker login

```
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 618873054107.dkr.ecr.us-east-2.amazonaws.com
WARNING! Your password will be stored unencrypted in /root/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded
```

4. Pushing  the image to repo

```
docker push 618873054107.dkr.ecr.us-east-2.amazonaws.com/devopsec-assignment-ecr:getjsoncode
The push refers to repository [618873054107.dkr.ecr.us-east-2.amazonaws.com/devopsec-assignment-ecr]
4848456dcafb: Pushed
5aaeeaa7fadd: Pushed
6e5f62a75eb2: Pushed
ac1252887a01: Pushed
060807c85bbe: Pushed
e80eb58cd4e1: Pushed
21abb8089732: Pushed
9889ce9dc2b0: Pushed
21b17a30443e: Pushed
05103deb4558: Pushed
a881cfa23a78: Pushed
getjsoncode: digest: sha256:ada97bc86bc8025954c52a3a03140864286785a865a39ff71b883bfaa0173a33 size: 2636

Pushing the Second Service:

 docker push 618873054107.dkr.ecr.us-east-2.amazonaws.com/devopsec-assignment-ecr:calljsoncode
The push refers to repository [618873054107.dkr.ecr.us-east-2.amazonaws.com/devopsec-assignment-ecr]
ee55839228d1: Pushed
5aaeeaa7fadd: Layer already exists
6e5f62a75eb2: Layer already exists
ac1252887a01: Layer already exists
060807c85bbe: Layer already exists
e80eb58cd4e1: Layer already exists
21abb8089732: Layer already exists
9889ce9dc2b0: Layer already exists
21b17a30443e: Layer already exists
05103deb4558: Layer already exists
a881cfa23a78: Layer already exists
calljsoncode: digest: sha256:73313df5fbba4c5e1c20bb6352941b0696a242b9d145c0835ed1ec6dc977f0ba size: 2636
```

***************************************************************************************************
## **Phase 5: Creating the Kubernetes object for the deployment, using Deployments**

1. Created the deployment yaml for GET REST API Python service with follwing contents

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: getjsoncode-deployment
  labels:
    app: getjsoncode
spec:
  replicas: 2
  selector:
    matchLabels:
      app: getjsoncode
  template:
    metadata:
      labels:
        app: getjsoncode
    spec:
      containers:
      - name: getjsoncode
        image: 618873054107.dkr.ecr.us-east-2.amazonaws.com/devopsec-assignment-ecr:getjsoncode
        stdin: true
        tty: true
        ports:
        - containerPort: 8080
```

2. Expose the deployment to Load Balancer

```
apiVersion: v1
kind: Service
metadata:
  name: getjsoncode-service-loadbalancer
spec:
  type: LoadBalancer
  selector:
    app: getjsoncode
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080

```
3. Check if the application is accessible from outside world and PODs are running

```
 kubectl get pods -l 'app=getjsoncode' -o wide | awk {'print $1" " $3 " " $6'} | column -t
NAME                                    STATUS   IP
getjsoncode-deployment-bf4d4d899-km4jm  Running  172.31.26.254
getjsoncode-deployment-bf4d4d899-r7lrx  Running  172.31.0.127


[root@ip-172-31-24-4 devopssecassign]# kubectl get service/getjsoncode-service-loadbalancer |  awk {'print $1" " $2 " " $4 " " $5'} | column -t
NAME                              TYPE          EXTERNAL-IP                                                              PORT(S)
getjsoncode-service-loadbalancer  LoadBalancer  aed7b0d3094294f45ac8057e1bb75e87-1543800842.us-east-2.elb.amazonaws.com  8080:31332/TCP

curl http://aed7b0d3094294f45ac8057e1bb75e87-1543800842.us-east-2.elb.amazonaws.com:8080/getStatus
{"Status": "I am healthy"}

```

4. Created the deployment yaml for CALL REST API Python service with follwing contents

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: calljsoncode-deployment
  labels:
    app: calljsoncode
spec:
  replicas: 2
  selector:
    matchLabels:
      app: calljsoncode
  template:
    metadata:
      labels:
        app: calljsoncode
    spec:
      containers:
      - name: calljsoncode
        image: 618873054107.dkr.ecr.us-east-2.amazonaws.com/devopsec-assignment-ecr:calljsoncodekubernetes
        stdin: true
        tty: true
        ports:
        - containerPort: 8080

```
**************************************************************************************************************

## **Phase 6: Alternate approach (additional task) - Creating the Kubernetes object for the deployment, using helm chart templates**

1. Creating the Helm chart templates for python GET REST SERVICE API 

```
 helm create getjsoncodehelm 
WARNING: Kubernetes configuration file is group-readable. This is insecure. Location: /root/.kube/config
WARNING: Kubernetes configuration file is world-readable. This is insecure. Location: /root/.kube/config
Creating getjsoncodehelm 

```

5. Modify the values.yaml and Chart.yaml for the Imagepath, Pull Policy, Ingress details and tag
(Templates are uploaded under helmcart folder)

6. Installation of helm charts on EKS cluster

```
```
