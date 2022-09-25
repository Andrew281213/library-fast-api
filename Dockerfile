FROM python:3.10

WORKDIR /library
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /library/requirements.txt
#RUN apk add --update python3-pip
RUN apt-get update && apt-get install python3-pip -y
RUN python3.10 -m pip install --upgrade -r /library/requirements.txt
COPY ./app /library
EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
