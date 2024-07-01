from cryptography import x509
from cryptography.hazmat.primitives import hashes
from utils.date import n_days_ago, n_days_from_now
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption


_RSA_KEY_SIZE = 2048
_RSA_EXPONENT = 65537

_DEFAULT_VALIDITY_IN_DAYS = 365


class GeneratorService:
    def __init__(self, root_cert_pem: bytes, root_key_pem: bytes):
        self.root_cert = x509.load_pem_x509_certificate(root_cert_pem)
        self.root_private_key = load_pem_private_key(root_key_pem, password=None)

    def generate_certificate(
        self, subject_name: str, is_ca: bool = False, path_length: int = None
    ) -> tuple:

        priv_key, pub_key = self._gen_key_pair()

        private_key_pem = priv_key.private_bytes(
            Encoding.PEM,
            PrivateFormat.TraditionalOpenSSL,
            NoEncryption(),
        )

        certificate_pem = (
            x509.CertificateBuilder()
            .subject_name(x509.Name([x509.NameAttribute(x509.NameOID.COMMON_NAME, subject_name)]))
            .issuer_name(self.root_cert.subject)
            .not_valid_before(n_days_ago(1))
            .not_valid_after(n_days_from_now(_DEFAULT_VALIDITY_IN_DAYS))
            .serial_number(x509.random_serial_number())
            .public_key(pub_key)
            .add_extension(x509.BasicConstraints(ca=is_ca, path_length=path_length), critical=True)
            .sign(private_key=self.root_private_key, algorithm=hashes.SHA256())
            .public_bytes(Encoding.PEM)
        )

        return private_key_pem, certificate_pem

    def _gen_key_pair(self) -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
        private_key = rsa.generate_private_key(
            key_size=_RSA_KEY_SIZE,
            public_exponent=_RSA_EXPONENT,
        )
        public_key = private_key.public_key()

        return private_key, public_key
