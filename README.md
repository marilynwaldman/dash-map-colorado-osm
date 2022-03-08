
# set up a clean environment

```
python3 -m venv ~/.dash
source ~/.dash/bin/activate
pip install dash
pip install dash_bootstrap_components
pip freeze > requirements.txt
make all
```
This has been moved to app runner using github. 

See:  https://www.coursera.org/learn/cloud-machine-learning-engineering-mlops-duke/lecture/FOjTX/continuously-deploy-flask-ml-application

use the github method, not containers - ecr.

#  from here:

https://github.com/russellromney/docker-dash/blob/master/README.md


Reqs: Python 3, AWS CLI, Docker
Install Docker, Python 3, and AWS CLI if not already done.

If needed, configure AWS CLI with aws configure.

Build the Docker image locally and teset
Build:

docker build -t docker-dash .

Test:

docker run -p 8050:8050 docker-dash

Send image to AWS ECR (Elastic Container Registry)
Create a repository in AWS ECR:

aws ecr create-repository --repository-name <my-repo-name>
aws ecr create-repository --repository-name dashmap

Get login auth token:

Go to aws console - ecr and look at push commands - 

docker build -t dashmap .

Go to aws console - ecr and look at push commands -  below does not work

        aws ecr get-login --region us-west-2 --no-include-email


run the aws container locally:

docker run -p 8050:8050 -e AWS_ACCESS_KEY_ID="your key" -e  AWS_SECRET_ACCESS_KEY="your secret" -e AWS_REGION="us-west-2" dashmap:latest      

Deploy the Dash app with ECS (Elastic Container Service)
Follow the instructions in step 4 here: https://linuxacademy.com/blog/linux-academy/deploying-a-containerized-flask-application-with-aws-ecs-and-docker/

While doing this, I find it easier to change the names to match -service, -cluster, etc. to make it consistent to refer back to later.

Updating
If you need to make changes later, you need to build, test, login (if token expired), tag, and push to get the image to ECR. Then run the following command in the terminal:

aws ecs update-service --cluster <cluster name> --service <service name> --force-new-deployment

This will force the service to reload with the new code.


