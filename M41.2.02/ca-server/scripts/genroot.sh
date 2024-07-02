#!/bin/bash

COMMON_NAME="Example Root CA"
DAYS=3650
KEY_SIZE=2048
CONFIG_FILE="/etc/ssl/openssl.cnf"
CERTS_DIR="$PWD/certs"

# Ensuring the certificates directory exists
mkdir -p "$CERTS_DIR"

while getopts c:d:k:f: flag
do
    case "${flag}" in
        c) COMMON_NAME=${OPTARG};;
        d) DAYS=${OPTARG};;
        k) KEY_SIZE=${OPTARG};;
        f) CONFIG_FILE=${OPTARG};;
    esac
done

echo "Generating RSA private key for root CA..."
openssl genrsa -out "$CERTS_DIR/root-ca.key" $KEY_SIZE

echo "Generating root certificate..."
openssl req -x509 -new -nodes -key "$CERTS_DIR/rootcert.key" -sha256 -days $DAYS -out "$CERTS_DIR/rootcert.pem" \
    -subj "/CN=$COMMON_NAME" -config "$CONFIG_FILE"

echo "Root certificate generated:"
echo " - Key: $CERTS_DIR/root-ca.key"
echo " - Certificate: $CERTS_DIR/root-ca.pem"
