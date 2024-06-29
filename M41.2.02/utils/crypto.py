from cryptography.x509 import (
    Certificate,
    CertificateSigningRequest,
    load_pem_x509_csr as _load_pem_x509_csr,
    load_pem_x509_certificate as _load_pem_x509_certificate,
)
from cryptography.hazmat.backends import default_backend


def load_pem_x509_csr(csr_pem: bytes) -> CertificateSigningRequest:
    return _load_pem_x509_csr(csr_pem, default_backend())


def load_pem_x509_certificate(cert_pem: bytes) -> Certificate:
    return _load_pem_x509_certificate(cert_pem, default_backend())
