FROM python:3.10.6-slim AS compile-image

COPY requirements.txt .
RUN pip install --user -r requirements.txt


FROM python:3.10.6-slim AS build-image
COPY --from=compile-image /root/.local /root/.local

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH=/root/.local/bin:$PATH
ENV WORKDIR=/

WORKDIR $WORKDIR

COPY ./statistic_counter_service $WORKDIR