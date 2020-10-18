from python:3.7-alpine
WORKDIR /


EXPOSE 5000

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "-u", "gateway.py"]