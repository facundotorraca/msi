import os
from cryptography import x509
from utils.date import n_days_from_now
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import hashes
from utils.file import save_bin_file, safe_delete_file
from cryptography.hazmat.primitives.serialization import load_pem_private_key, Encoding

_CRL_NAME = "crl.pem"


class RevokerService:
    def __init__(self, root_cert_pem: bytes, root_key_pem: bytes, crl_directory: str):
        os.makedirs(crl_directory, exist_ok=True)
        self.crl_path = os.path.join(crl_directory, _CRL_NAME)
        self.root_cert = x509.load_pem_x509_certificate(root_cert_pem)
        self.root_private_key = load_pem_private_key(root_key_pem, password=None)

    def revoke_certificate(self, cert_pem: bytes) -> bool:
        cert_to_revoke = x509.load_pem_x509_certificate(cert_pem)
        curr_crl = self._load_current_crl()

        # Add the new revoked certificate
        revoked_cert = (
            x509.RevokedCertificateBuilder()
            .serial_number(cert_to_revoke.serial_number)
            .revocation_date(datetime.now())
            .build()
        )

        if revoked_cert in curr_crl:
            raise False

        # Update CRL with the new revoked certificate
        new_crl = (
            x509.CertificateRevocationListBuilder()
            .issuer_name(curr_crl.issuer)
            .last_update(datetime.now())
            .next_update(n_days_from_now(30))
        )

        for old_revoked_cert in curr_crl:
            new_crl = new_crl.add_revoked_certificate(old_revoked_cert)

        new_crl = new_crl.add_revoked_certificate(revoked_cert)
        new_crl = new_crl.sign(self.root_private_key, algorithm=hashes.SHA256())

        # Save the updated CRL
        safe_delete_file(self.crl_path)
        save_bin_file(new_crl.public_bytes(Encoding.PEM), self.crl_path)

        return True

    def _load_current_crl(self) -> x509.CertificateRevocationList:
        """Load the current CRL from a file, or create a new one if it doesn't exist."""

        if os.path.exists(self.crl_path):
            with open(self.crl_path, "rb") as f:
                return x509.load_pem_x509_crl(f.read())
        else:
            # Start a new CRL
            return (
                x509.CertificateRevocationListBuilder()
                .issuer_name(self.root_cert.subject)
                .last_update(datetime.now())
                .next_update(datetime.now() + timedelta(days=30))
                .sign(private_key=self.root_private_key, algorithm=hashes.SHA256())
            )
