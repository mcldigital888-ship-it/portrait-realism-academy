#!/usr/bin/env bash
# Bootstrap OVH VPS (Ubuntu) per servire il sito statico dietro Cloudflare.
# Uso (sul VPS, come root):  bash ovh-bootstrap.sh portraitrealismacademy.com
set -euo pipefail
DOMAIN="${1:-portraitrealismacademy.com}"
ROOT="/var/www/academy"

apt-get update -y
apt-get install -y nginx rsync
mkdir -p "$ROOT"
chown -R www-data:www-data "$ROOT"

cat >/etc/nginx/sites-available/academy <<CONF
server {
    listen 80;
    listen [::]:80;
    server_name ${DOMAIN} www.${DOMAIN};
    root ${ROOT};
    index index.html;
    location / { try_files \$uri \$uri/ /index.html; }
    location ~* \.(webp|jpg|jpeg|png|css|js|woff2|svg|xml|txt)\$ { expires 30d; add_header Cache-Control "public, max-age=2592000"; }
    gzip on; gzip_types text/html text/css application/javascript image/svg+xml application/ld+json;
    # Cloudflare-only: opzionale, restringi l'accesso ai soli IP di Cloudflare + usa Origin Cert.
}
CONF
ln -sf /etc/nginx/sites-available/academy /etc/nginx/sites-enabled/academy
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx
echo "OK: nginx serve ${ROOT} per ${DOMAIN}."
echo "Poi: (1) su Cloudflare aggiungi il dominio, A record @ -> IP di questo VPS (Proxied), SSL=Full(strict);"
echo "     (2) genera un Origin Certificate su Cloudflare e installalo qui in nginx per HTTPS end-to-end;"
echo "     (3) su GitHub imposta secrets OVH_HOST/OVH_USER/OVH_SSH_KEY/OVH_PATH=${ROOT} e variabile OVH_ENABLED=true."
