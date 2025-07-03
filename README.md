# Book-Recommendation-Clustering-Pipeline

An end-to-end modular pipeline for book recommendation using clustering techniques, built with best practices in MLOps, data engineering, and cloud deployment.

---

## Features

- Modular, maintainable pipeline components (data ingestion, validation, transformation, training, prediction)
- Data versioning and pipeline orchestration using **DVC** for reproducibility
- Secure management of credentials via **AWS Secrets Manager**
- Containerised with **Docker** for easy deployment on cloud platforms (e.g. AWS EC2)
- Interactive **Streamlit** app interface for exploring book recommendations
- Automated download of datasets from Kaggle and external sources
- Comprehensive logging and exception handling for robustness

- VS code: https://code.visualstudio.com/download
- Git: https://git-scm.com/
- Data link: https://www.kaggle.com/datasets/ra4u12/bookrecommendation

## Workflow

1. Config file (Constants)
2. Config Entity (Return values)
3. App Config (Read config file)
4. Components (Pipeline code files)
5. Pipeline (Run components)
6. Main file (run pipeline)
7. App file (User interface)

````

# To run this project:
### Follow these steps:

Clone the repository

```bash
https://github.com/razyousuf/Book-Recommendation-Clustering-Pipeline.git
```

## 01: Environments configuration

```bash
conda create -n book python=3.10 -y
```

```bash
conda activate book
```


### 02: install the requirements
```bash
pip install -r requirements.txt
```


Now run,
```bash
streamlit run app.py
```


# Streamlit app Docker Image Deployment

## 1. Login with your AWS console and launch an EC2 instance
## 2. Run the following commands

Note: Do the port mapping to this port:- 8080

```bash
sudo apt-get update -y

sudo apt-get upgrade

#Install Docker

curl -fsSL https://get.docker.com -o get-docker.sh

sudo sh get-docker.sh

sudo usermod -aG docker ubuntu

newgrp docker
```

```bash
git clone "your-project-repository-url"
```

```bash
docker build -t raz/app:latest .
```

```bash
docker images -a
```

```bash
docker run -d -p 8501:8501 raz/app
```

```bash
docker ps
```

```bash
docker stop container_id
```

```bash
docker rm $(docker ps -a -q)
```

```bash
docker login
```

```bash
docker push raz/app:latest
```

```bash
docker rmi raz/app:latest
```

```bash
docker pull raz/app
```
---

## Git commands (Informmational only)

```bash
git add .

git commit -m "Updated"

git push origin main
```
````
