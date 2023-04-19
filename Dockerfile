FROM python:3.10-slim
ENV PYTHONUNBUFFERED 1

RUN python -m pip install --upgrade pip && \
  pip install --upgrade setuptools

WORKDIR /backend

COPY requirements.txt /backend/requirements.txt
RUN pip install -r /backend/requirements.txt
COPY ./ /backend

CMD /backend/run.sh
