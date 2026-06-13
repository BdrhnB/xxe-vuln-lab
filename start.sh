#!/bin/bash
# HealthSync — Container Startup Script
# Regenerates SSH keys and user flag on every boot

# Generate fresh SSH key for devops (new key each container start)
rm -f /home/devops/.ssh/id_rsa /home/devops/.ssh/id_rsa.pub /home/devops/.ssh/authorized_keys
ssh-keygen -t rsa -b 2048 -f /home/devops/.ssh/id_rsa -N '' -C 'devops@healthsync' -q
cp /home/devops/.ssh/id_rsa.pub /home/devops/.ssh/authorized_keys
chmod 755 /home/devops/.ssh
chmod 644 /home/devops/.ssh/id_rsa /home/devops/.ssh/authorized_keys
chown -R devops:devops /home/devops/.ssh

# Write user flag (HTB standard: root:devops 644)
printf 'dbe9b6a812c78983a9dac84e2129b97a\n' > /home/devops/user.txt
chown root:devops /home/devops/user.txt
chmod 644 /home/devops/user.txt

# Start services
service ssh start
service apache2 start

# Start Flask application
exec python3 /app/app.py
