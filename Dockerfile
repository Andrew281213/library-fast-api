FROM python:3.10

WORKDIR /library
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install python3-pip -y
COPY . /library
RUN python3.10 -m pip install --upgrade -r /library/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app:api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
