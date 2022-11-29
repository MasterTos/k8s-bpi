FROM python:3-slim

RUN apt update && apt install -y netcat
ADD init.sh /init.sh

WORKDIR /code
ADD requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

ADD src/ /code


ENTRYPOINT ["/init.sh"]
CMD ["uvicorn", "wallet:app", "--proxy-headers", "--host", "0.0.0.0", "--reload", "--reload-dir", "/code"]