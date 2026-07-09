# Docker 201 demo: the BEFORE image.
#
# A perfectly normal Dockerfile on a standard base. It works fine.
# The point of the demo: run "docker scout" against this and see
# how much surface a general-purpose base carries.

FROM python:3.14-slim

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

ENV APP_VARIANT=standard

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
