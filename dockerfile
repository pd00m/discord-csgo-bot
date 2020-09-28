FROM python:3.8-alpine
ADD . /code
WORKDIR /code
RUN apk update && apk add --no-cache gcc git python3-dev musl-dev linux-headers libc-dev rsync findutils wget util-linux grep libxml2-dev libxslt-dev && pip3 install --upgrade pip && pip install -r requirements.txt 
CMD ["python", "main.py"]
