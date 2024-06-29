import datetime
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa


class GeneratorService:
    def generate_certificate(
        self,
        csr: x509.CertificateSigningRequest,
        ca_cert: x509.Certificate,
        ca_key: rsa.RSAPrivateKey,
    ) -> x509.Certificate:
        cert = (
            x509.CertificateBuilder()
            .subject_name(csr.subject)
            .issuer_name(ca_cert.subject)
            .public_key(csr.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(datetime.datetime.now(datetime.timezone.utc))
            .not_valid_after(
                datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365)
            )
            .sign(private_key=ca_key, algorithm=hashes.SHA256(), backend=default_backend())
        )
        return cert
