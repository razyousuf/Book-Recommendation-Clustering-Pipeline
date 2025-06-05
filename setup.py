from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

## edit below variables as per your requirements -
REPO_NAME = "Book Recommendation Clustering Pipeline"
AUTHOR_USER_NAME = "Raz Yousufi"
SRC_REPO = "books_recommender"
LIST_OF_REQUIREMENTS = []


setup(
    name=SRC_REPO,
    version="0.0.0",
    author="Raz Yousufi",
    author_email="razyousufi350@gmail.com",
    description="Small packages for ML based book recommendation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Razyousuf/Book-Recommendation-Clustering-Pipeline",
    packages=find_packages(),
    license="MIT",
    python_requires=">=3.10",
    install_requires=LIST_OF_REQUIREMENTS
)