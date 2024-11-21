FROM python:3.10-slim

RUN mkdir /fastapi

COPY requirements.txt /fastapi

WORKDIR /fastapi

RUN pip3 install -r requirements.txt
RUN pip3 install markdownify

COPY . /fastapi

EXPOSE 8000

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH "${PYTHONPATH}:/fastapi"

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "-1"]