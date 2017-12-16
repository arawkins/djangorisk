FROM python:latest
ARG secret
ENV SECRET_KEY secret
RUN mkdir /code
COPY . /code
WORKDIR /code
RUN pip install -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "djangorisk.wsgi"]
