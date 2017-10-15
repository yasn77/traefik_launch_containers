FROM python:3.5
EXPOSE 80

COPY ./app.py /app-status/app.py
COPY ./templates /app-status/templates
COPY ./requirements.txt /app-status/requirements.txt
COPY docker-entrypoint.sh /entrypoint.sh
WORKDIR /app-status
RUN pip install -r requirements.txt
CMD ["app-status"]
ENTRYPOINT ["/entrypoint.sh"]
