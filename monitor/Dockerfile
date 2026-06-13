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

# HTB: root flag permissions (root:root 640)
RUN chown root:root /root/root.txt && \
    chmod 640 /root/root.txt

# HTB: history redirection
RUN ln -sf /dev/null /root/.bash_history

# Service runs as root — privilege escalation path
EXPOSE 8080

CMD ["python3", "app.py"]
