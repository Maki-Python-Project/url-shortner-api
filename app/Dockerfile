FROM python:3.10.7

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get -y update \
    && apt-get -y install \
    gcc python3-dev musl-dev netcat lsof procps \
    build-essential \
    libssl-dev \
    libffi-dev \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libc-dev \
    bash \
    git \
    && pip3 install --upgrade pip

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip --no-cache-dir install -r requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

COPY . .

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]