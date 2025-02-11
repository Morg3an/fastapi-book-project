FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Install Nginx
RUN apt-get update && apt-get install -y nginx

# Copy the Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy your FastAPI application
COPY ./app /app

# Expose the FastAPI and Nginx ports
EXPOSE 80 8000

# Start Nginx and FastAPI
CMD service nginx start && uvicorn app.main:app --host 0.0.0.0 --port 8000