FROM python

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/HoneyShop

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .