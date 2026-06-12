FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

<<<<<<< HEAD
RUN apt update -y && \
    apt install python3 python3-pip -y && \
=======
# Temel paketler + SSH + Apache + PHP
RUN apt update -y && \
    apt install -y python3 python3-pip openssh-server apache2 libapache2-mod-php php php-cli \
                   curl netcat-openbsd iputils-ping dnsutils iproute2 && \
>>>>>>> a00a62a (all lab completly updated)
    apt clean

WORKDIR /app

<<<<<<< HEAD
COPY . .
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python3", "app.py"]
=======
COPY app.py requirements.txt ./
COPY templates/ templates/

# Uploads dizinini build zamaninda olustur
RUN mkdir -p /app/uploads

RUN pip3 install -r requirements.txt

# --- Config dosyasi (XXE hedefi) ---
RUN mkdir -p /etc/healthsync && \
    printf '# HealthSync Application Configuration\n# WARNING: This file contains sensitive credentials.\n# Last modified: 2026-05-14 by magnus_vinter\n\n[database]\nhost=db-internal.healthsync.local\nport=5432\nuser=hsdb_user\npassword=DbS3cur3!\n\n[portal]\nupload_user=magnus\nupload_password=superman\nsecret_key=hs_9k2m_2026\n\n[app]\ndebug=false\nlog_level=info\nenvironment=production\n' \
    > /etc/healthsync/app.conf && \
    chmod 644 /etc/healthsync/app.conf

# --- devops kullanicisi, SSH key ve user flag olustur ---
RUN useradd -m -s /bin/bash devops && \
    echo 'devops:devops2026!' | chpasswd && \
    mkdir -p /home/devops/.ssh && \
    ssh-keygen -t rsa -b 2048 -f /home/devops/.ssh/id_rsa -N '' -C 'devops@healthsync' && \
    cp /home/devops/.ssh/id_rsa.pub /home/devops/.ssh/authorized_keys && \
    chmod 755 /home/devops/.ssh && \
    chmod 644 /home/devops/.ssh/id_rsa /home/devops/.ssh/authorized_keys && \
    printf 'HTB{xm1_3xt3rn4l_3nt1ty_m4gnus_f4ll}\n' > /home/devops/user.txt && \
    chown -R devops:devops /home/devops && \
    chmod 755 /home/devops

# SSH konfigurasyonu
RUN mkdir -p /run/sshd && \
    echo 'PermitRootLogin no' >> /etc/ssh/sshd_config && \
    echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config && \
    echo 'PubkeyAuthentication yes' >> /etc/ssh/sshd_config

# --- Apache + PHP konfigurasyonu (uploads dizinini serve et) ---
# PHP modulunu bul ve etkinlestir
RUN a2enmod php8.1 2>/dev/null || a2enmod php8.2 2>/dev/null || a2enmod php8.3 2>/dev/null || true

RUN rm -rf /var/www/html/uploads 2>/dev/null; \
    ln -sf /app/uploads /var/www/html/uploads && \
    chown -R www-data:www-data /app/uploads /var/www/html

# Apache'nin port 8080'de dinlemesi icin (Flask 5000'de)
RUN sed -i 's/Listen 80/Listen 8080/' /etc/apache2/ports.conf && \
    sed -i 's/<VirtualHost \\*:80>/<VirtualHost *:8080>/' /etc/apache2/sites-available/000-default.conf && \
    printf '<Directory /var/www/html/uploads>\n    Options Indexes FollowSymLinks\n    AllowOverride All\n    Require all granted\n</Directory>\n' >> /etc/apache2/apache2.conf

# Calistirma scripti
RUN printf '#!/bin/bash\nservice ssh start\nservice apache2 start\npython3 /app/app.py\n' > /start.sh && \
    chmod +x /start.sh

EXPOSE 5000 8080 22

CMD ["/start.sh"]
>>>>>>> a00a62a (all lab completly updated)
