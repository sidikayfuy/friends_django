FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /vk

COPY ./requirements.txt /vk/requirements.txt
RUN pip install -r /vk/requirements.txt

COPY . /vk

EXPOSE 8000
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000 --insecure