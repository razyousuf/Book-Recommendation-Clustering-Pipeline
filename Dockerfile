FROM python:3.12-slim-buster

# Set working directory
WORKDIR /app

# Copy codebase first (before installing DVC, to allow DVC pull)
COPY . /app

# Install required system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies (including DVC)
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install dvc

# Pull DVC-tracked data (model, etc.)
RUN dvc pull && dvc checkout

# Expose the Streamlit port
EXPOSE 8080

# Set the entrypoint
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
