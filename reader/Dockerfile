FROM alpine:3.5
MAINTAINER DEV_NICOLOKO "dev@nicoloko.com"
RUN apk add --no-cache python2 git && \
    python2 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip2 install --upgrade pip setuptools && \
    rm -r /root/.cache
COPY . /app
WORKDIR /app
RUN pip2 install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
