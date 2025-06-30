# Use an official PyTorch image with CUDA support
FROM pytorch/pytorch:2.7.1-cuda12.6-cudnn9-runtime

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# Using pip from the PyTorch environment
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=use_model_flask.py

# Run the command to start the flask server
CMD ["flask", "run", "--host=0.0.0.0"]

