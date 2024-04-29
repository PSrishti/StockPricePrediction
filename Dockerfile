FROM python:3.10.11

RUN apt-get update && \
    apt-get install -y cmake && \
    apt-get install -y libopenblas-dev && \
    apt-get clean

WORKDIR /app
COPY src /app/src
WORKDIR /app/src

COPY requirements.txt /app/src/
RUN pip install --no-deps --no-cache-dir -r requirements.txt
RUN pip install --upgrade tensorflow keras


COPY . .

EXPOSE  8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
