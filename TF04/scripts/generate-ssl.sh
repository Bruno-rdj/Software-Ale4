#!/bin/bash
# Gera certificado SSL self-signed para desenvolvimento
mkdir -p ../nginx/ssl

openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ../nginx/ssl/key.pem \
  -out ../nginx/ssl/cert.pem \
  -subj "/C=BR/ST=SP/L=Sao Paulo/O=TechStore/CN=localhost"

echo "Certificados gerados em nginx/ssl/"
