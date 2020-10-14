from python:3.7-alpine
WORKDIR /
ENV LANG=en_US.UTF-8

EXPOSE 5000

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "gateway.py"]