FROM python:3

WORKDIR /app/islands

ADD . .

# RUN pip install -r requirements.txt

RUN chmod 755 your_script.sh

ENTRYPOINT ["./your_script.sh"]
