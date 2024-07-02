import os
from cryptography import x509
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import padding


class ValidatorService:
    def __init__(self, root_cert_pem: bytes, crl_directory: str):
        self.crl_path = os.path.join(crl_directory, "crl.pem")
        self.root_cert = x509.load_pem_x509_certificate(root_cert_pem)

    def verify_certificate(self, cert_pem: bytes) -> tuple[bool, str]:
        cert = x509.load_pem_x509_certificate(cert_pem)

        if not self._certificate_chain_is_valid(cert):
            return False, "Invalid certificate chain"

        if self._certiticate_is_revocated(cert):
            return False, "Certificate is revocated"

        return True, "Certificate is valid"

    def _certificate_chain_is_valid(self, cert: x509.Certificate):
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

    def _certiticate_is_revocated(self, cert: x509.Certificate):
        if not os.path.exists(self.crl_path):
            return False

        with open(self.crl_path, "rb") as f:
            crl = x509.load_pem_x509_crl(f.read())

        for revoked_cert in crl:
            if revoked_cert.serial_number == cert.serial_number:
                return True

        return False
