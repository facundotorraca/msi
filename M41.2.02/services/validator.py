from cryptography import x509
from cryptography.hazmat.primitives import padding


class ValidatorService:
    def verify_certificate(
        self,
        cert: x509.Certificate,
        ca_cert: x509.Certificate,
    ) -> tuple[bool, str]:
        try:
            ca_public_key = ca_cert.public_key()

            ca_public_key.verify(
                cert.signature,
                cert.tbs_certificate_bytes,
                padding.PKCS1v15(),
                cert.signature_hash_algorithm,
            )
            return True, ""
        except Exception as e:
            return False, str(e)
