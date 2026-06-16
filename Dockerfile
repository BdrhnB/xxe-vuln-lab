FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update -y && \
    apt install -y python3 python3-pip openssh-server apache2 libapache2-mod-php php php-cli \
                   curl netcat-openbsd iputils-ping dnsutils iproute2 && \
    apt clean

WORKDIR /app

COPY app.py requirements.txt ./
COPY templates/ templates/

RUN mkdir -p /app/uploads

RUN pip3 install -r requirements.txt

RUN mkdir -p /etc/healthsync && \
    printf '# HealthSync Application Configuration\n# WARNING: This file contains sensitive credentials.\n# Last modified: 2026-05-14 by magnus_vinter\n\n[database]\nhost=db-internal.healthsync.local\nport=5432\nuser=hsdb_user\npassword=DbS3cur3!\n\n[portal]\nupload_user=magnus\nupload_password=superman\nsecret_key=hs_9k2m_2026\n\n[app]\ndebug=false\nlog_level=info\nenvironment=production\n' \
    > /etc/healthsync/app.conf && \
    chmod 644 /etc/healthsync/app.conf

RUN useradd -m -s /bin/bash devops && \
    echo 'devops:devops2026!' | chpasswd && \
    mkdir -p /home/devops/.ssh && \
    chmod 755 /home/devops

RUN ln -sf /dev/null /home/devops/.bash_history && \
    chown root:root /home/devops/.bash_history && \
    ln -sf /dev/null /root/.bash_history

RUN mkdir -p /run/sshd && \
    echo 'PermitRootLogin no' >> /etc/ssh/sshd_config && \
    echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config && \
    echo 'PubkeyAuthentication yes' >> /etc/ssh/sshd_config

RUN a2enmod php8.1 2>/dev/null || a2enmod php8.2 2>/dev/null || a2enmod php8.3 2>/dev/null || true

RUN rm -rf /var/www/html/uploads 2>/dev/null; \
    ln -sf /app/uploads /var/www/html/uploads && \
    chown -R www-data:www-data /app/uploads /var/www/html

RUN sed -i 's/Listen 80/Listen 8080/' /etc/apache2/ports.conf && \
    sed -i 's/<VirtualHost \\*:80>/<VirtualHost *:8080>/' /etc/apache2/sites-available/000-default.conf && \
    printf '<Directory /var/www/html/uploads>\n    Options Indexes FollowSymLinks\n    AllowOverride All\n    Require all granted\n</Directory>\n' >> /etc/apache2/apache2.conf

COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 5000 8080 22

CMD ["/start.sh"]
