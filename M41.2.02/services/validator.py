from cryptography.hazmat.primitives import padding
from cryptography.exceptions import InvalidSignature
from cryptography.x509 import load_pem_x509_certificate


class ValidatorService:
    def __init__(self, root_cert_pem: bytes):
        self.root_cert = load_pem_x509_certificate(root_cert_pem)

    def verify_certificate(self, cert_pem: bytes) -> bool:
        cert = load_pem_x509_certificate(cert_pem)
        public_key = self.root_cert.public_key()

        try:
            public_key.verify(
                cert.signature,
                cert.tbs_certificate_bytes,
                padding.PKCS1v15(),
                cert.signature_hash_algorithm,
            )
            return True
        except InvalidSignature:
            return False
