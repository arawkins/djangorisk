FROM python:latest
EXPOSE 8000
RUN mkdir /code
WORKDIR /code
RUN git clone https://github.com/arawkins/djangorisk.git .
RUN pip install -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate
CMD ["gunicorn", "djangorisk.wsgi"]
