FROM python:3
WORKDIR /usr/src/app

RUN apt update
RUN apt install -y vim

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py ./
COPY libs ./libs

CMD [ "python", "app.py" ]
