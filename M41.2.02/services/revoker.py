from datetime import datetime
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization


class RevokerService:
    def __init__(self, root_cert_pem: bytes, root_key_pem: bytes):
        self.root_cert = x509.load_pem_x509_certificate(root_cert_pem)
        self.root_private_key = x509.load_pem_private_key(root_key_pem, password=None)

    def revoke_certificate(self, cert_pem: bytes) -> bytes:
        cert_to_revoke = x509.load_pem_x509_certificate(cert_pem)
        crl_builder = x509.CertificateRevocationListBuilder()
        crl_builder = crl_builder.last_update(datetime.now())
        crl_builder = crl_builder.next_update(datetime.now() + datetime.timedelta(days=30))
        crl_builder = crl_builder.issuer_name(self.root_cert.subject)

        revoked_cert = (
            x509.RevokedCertificateBuilder()
            .serial_number(cert_to_revoke.serial_number)
            .revocation_date(datetime.now())
            .build()
        )

        crl_builder = crl_builder.add_revoked_certificate(revoked_cert)
        crl = crl_builder.sign(
            private_key=self.root_private_key,
            algorithm=hashes.SHA256(),
        )

        return crl.public_bytes(serialization.Encoding.PEM)
