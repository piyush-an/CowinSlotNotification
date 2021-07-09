FROM python:alpine3.12

WORKDIR /usr/src/CoWin

COPY script/app.py .
COPY script/config.ini .

RUN pip install requests
RUN chmod 755 .

CMD ["python", "/usr/src/CoWin/app.py" ]
