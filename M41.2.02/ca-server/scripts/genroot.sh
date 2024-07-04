#RT!/bin/bash

COMMON_NAME="msi-kerberos.com"
DAYS=3650
KEY_SIZE=2048
CONFIG_FILE="/etc/ssl/openssl.cnf"
CERTS_DIR="$PWD/certs"

# Ensuring the certificates directory exists
mkdir -p "$CERTS_DIR"

while getopts c:d:k: flag
do
    case "${flag}" in
        c) COMMON_NAME=${OPTARG};;
        d) DAYS=${OPTARG};;
        k) KEY_SIZE=${OPTARG};;
    esac
done

ROOT_PEM_FILE="$CERTS_DIR/root.pem"
ROOT_KEY_FILE="$CERTS_DIR/root.key"

echo "*** Generating RSA private key for root CA..."
openssl genrsa -out "$ROOT_KEY_FILE" $KEY_SIZE

echo "*** Generating root certificate..."
openssl req -x509 -new -nodes \
    -key "$ROOT_KEY_FILE" \
    -sha256 \
    -days $DAYS \
    -out "$ROOT_PEM_FILE" \
    -subj "/CN=$COMMON_NAME" \
    -config "$CONFIG_FILE"


echo "*** Root certificate generated"
echo "*** Key: $ROOT_PEM_FILE"
echo "*** Pem: $ROOT_KEY_FILE"
