#!/bin/bash
set -e

echo "Setting up SSH..."

# Создание необходимых директорий
mkdir -p /var/run/sshd

# Генерация SSH ключей хоста
cat /etc/ssh/ssh_host_rsa_key
if [ ! -f /etc/ssh/ssh_host_rsa_key ]; then
    echo "Generating SSH host keys..."
    ssh-keygen -A
fi

## Создание пользователя django если его нет
#if ! id django 2>/dev/null; then
#    echo "Creating django user..."
#    groupadd -g 1000 django
#    useradd -u 1000 -g django -m -s /bin/bash django
#fi
#
## Установка пароля для django
#echo "Setting password for django user..."
#echo "django:django123" | chpasswd

# Настройка SSH конфигурации
#echo "Configuring SSH..."
#sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
#sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
#echo "AllowUsers django" >> /etc/ssh/sshd_config

## Установка правильных прав
#chown -R django:django /app
#chmod 755 /home/django

echo "Starting SSH daemon..."
exec /usr/sbin/sshd -D -e
