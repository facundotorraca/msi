import datetime
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption


class GeneratorService:
    def __init__(self, root_cert_pem: bytes, root_key_pem: bytes):
        self.root_cert = x509.load_pem_x509_certificate(root_cert_pem)
        self.root_private_key = x509.load_pem_private_key(root_key_pem, password=None)

    def generate_certificate(
        self, subject_name: str, is_ca: bool = False, path_length: int = None
    ) -> tuple:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        public_key = private_key.public_key()

        builder = x509.CertificateBuilder()
        builder = builder.subject_name(
            x509.Name([x509.NameAttribute(x509.NameOID.COMMON_NAME, subject_name)])
        )
        builder = builder.issuer_name(self.root_cert.subject)
        builder = builder.not_valid_before(datetime.now() - datetime.timedelta(days=1))
        builder = builder.not_valid_after(
            datetime.now() + datetime.timedelta(days=365 * (5 if is_ca else 1))
        )
        builder = builder.serial_number(x509.random_serial_number())
        builder = builder.public_key(public_key)
        builder = builder.add_extension(
            x509.BasicConstraints(ca=is_ca, path_length=path_length),
            critical=True,
        )

        certificate = builder.sign(private_key=self.root_private_key, algorithm=hashes.SHA256())

        private_key_pem = private_key.private_bytes(
            Encoding.PEM, PrivateFormat.TraditionalOpenSSL, NoEncryption()
        )
        certificate_pem = certificate.public_bytes(Encoding.PEM)

        return private_key_pem, certificate_pem
