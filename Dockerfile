# Use the official Python 3.10 image as the base image
FROM python:3.10-slim-buster

RUN pip install --upgrade pip
# Set the working directory
WORKDIR /usr/src/app

# Copy the entire repo into the container
COPY . .

# Install the required Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Streamlit port
EXPOSE 8501

# Command to run the Streamlit app
ENTRYPOINT ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0", "--theme.primaryColor=Black"]
