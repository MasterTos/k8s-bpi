FROM python:3-slim

ENV WATCHFILES_FORCE_POLLING=true

WORKDIR /code
ADD requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

ADD src/ code/

HEALTHCHECK --interval=21s --timeout=3s --start-period=10s CMD curl --fail http://localhost:8000/ping || exit 1

CMD ["uvicorn", "user:app", "--proxy-headers", "--host", "0.0.0.0", "--reload", "--reload-dir", "/code"]