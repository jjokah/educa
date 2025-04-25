# Pull official base Python Docker image
FROM python:3.12.3

# Set environment variables
ENV PYTHONDONOTWRITEBYCODE=1
ENV PYTHONBUFFERED=1

# Set work directory
WORKDIR /code

# Install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN  pip install -r requirements.txt

# Copy the Django project
COPY . .