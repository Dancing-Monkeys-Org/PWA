FROM python:3.6.10

COPY requirements.txt /usr/src/app
RUN pip install -r requirements.txt

COPY . /usr/src/app
WORKDIR /usr/src/app

ENTRYPOINT [ "flask" ]
CMD ["run", "--host=0.0.0.0", "--port=5000"]
