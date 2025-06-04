# Visa-grant-prediction-MLOps

- Vs code: https://code.visualstudio.com/download
- Git: https://git-scm.com/
- Flowchart: https://whimsical.com/
- MLOPs Tool: https://www.evidentlyai.com/
- MongoDB: https://account.mongodb.com/account/login
- Data link: https://www.kaggle.com/datasets/moro23/easyvisa-dataset

## Git commands

```bash
git add .

git commit -m "Updated"

git push origin main
```

## Environments configuration

```bash
conda create -n visa python=3.10 -y
```

```bash
conda activate visa
```

```bash
pip install -r requirements.txt
```

## Workflow

1. Constants
2. Entities
3. Components
4. Pipeline
5. Main file

### Export the environment variables

Option 1: Include the variables inside your **.env** file as:

```bash

MONGODB_CREDENTIAL="mongodb+srv://<username>:<password>...."

AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>

AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>
```

Option 2: Include the above credintials/URLs in your OS system environment as environment varaibles.

```bash

export MONGODB_URL="mongodb+srv://<username>:<password>...."

export AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>

export AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>


```

# AWS-CICD-Deployment-with-Github-Actions

## 1. Login to AWS console.

## 2. Create IAM user for deployment

    #with specific access

    1. EC2 access : It is virtual machine

    2. ECR: Elastic Container registry to save your docker image in aws


    #Description: About the deployment

    1. Build docker image of the source code

    2. Push your docker image to ECR

    3. Launch Your EC2

    4. Pull Your image from ECR in EC2

    5. Lauch your docker image in EC2

    #Policy:

    1. AmazonEC2ContainerRegistryFullAccess

    2. AmazonEC2FullAccess

## 3. Create ECR repo to store/save docker image

    - Save the URI: E.g: "480865595393.dkr.ecr.us-east-1.amazonaws.com/visa"

## 4. Create EC2 machine (Ubuntu)

## 5. Open EC2 and Install docker in EC2 Machine:

    #optinal

```bash
    sudo apt-get update -y

    sudo apt-get upgrade
```

    #required

```bash
    curl -fsSL https://get.docker.com -o get-docker.sh

    sudo sh get-docker.sh

    sudo usermod -aG docker ubuntu

    newgrp docker
```

# 6. Configure EC2 as self-hosted runner:

    Repo Setting > Actions > Runner > new self-hosted runner > choose os (Linux) > then copy and run the connection and config commands in the EC2 terminal.

# 7. Setup github secrets:

- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_DEFAULT_REGION
- ECR_REPO
- MONGODB_URL
