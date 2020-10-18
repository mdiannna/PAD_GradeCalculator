from python:3.8
WORKDIR /


EXPOSE 8000

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "-u", "service_type2.py"]