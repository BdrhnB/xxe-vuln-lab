FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update -y && \
    apt install -y python3 python3-pip iputils-ping && \
    apt clean

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY app.py .
COPY root.txt /root/root.txt

# Servis root olarak calisir — privilege escalation yolu bu
EXPOSE 8080

CMD ["python3", "app.py"]
