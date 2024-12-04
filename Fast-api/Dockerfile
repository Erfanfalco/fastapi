FROM python:3.12-alpine3.20

# Set the working directory in the container
WORKDIR /app

# Copy hole of the Dir into the Docker image
COPY . .

# Upgrade pip
RUN python -m pip install --upgrade pip

# Install packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make ports available to the world outside this container
EXPOSE 8000

# initialize Docker's env
ENV HOST=0.0.0.0
ENV PORT=8000

# Run both services
CMD ["uvicorn", "main:app","--host","0.0.0.0", "--port", "8000"]

