FROM python:3.10.11

#Install system dependencies
RUN apt-get update && \
    apt-get install -y cmake && \
    apt-get install -y libopenblas-dev && \
    apt-get clean

#Set working directory and install python dependencies
COPY requirements.txt /app/
WORKDIR /app
RUN pip install --no-deps --no-cache-dir -r requirements.txt
RUN pip install --upgrade tensorflow keras

#Copy application code
COPY src /app/src
WORKDIR /app/src


COPY . .

#Expose the required port
EXPOSE  8000

#Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

