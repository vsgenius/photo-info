FROM python:3.10-alpine
ADD . /severstal
WORKDIR /severstal
COPY * /severstal/
RUN pip install -r requirements.txt
CMD ["python", "app.py"]