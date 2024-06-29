from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from services.generator import GeneratorService
from services.validator import ValidatorService
from cryptography.hazmat.primitives import serialization
from utils.crypto import load_pem_x509_csr, load_pem_x509_certificate

##################### APP #######################
app = FastAPI()
#################################################

#################### SERVICES ###################
generator = GeneratorService()
validator = ValidatorService()
#################################################


# Example storage for issued certificates
# (replace with proper storage solution in production)
issued_certificates = {}


################### ENDPOINTS #################


class CSRRequest(BaseModel):
    csr_pem: str


class CertificateRequest(BaseModel):
    cert_pem: str


@app.post("/generate")
def generate_certificate(csr_request: CSRRequest):
    try:
        # Receive CSR from client
        csr = load_pem_x509_csr(csr_request.csr_pem.encode())

        # Generate certificate
        cert = generator.generate_certificate(csr, ca_cert, ca_private_key)

        # Store issued certificate (replace with proper storage solution in production)
        issued_certificates[cert.subject.serial_number] = cert

        return cert.public_bytes(serialization.Encoding.PEM), 201
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/verify")
def verify_certificate(cert_request: CertificateRequest):
    try:
        # Receive certificate from client
        cert = load_pem_x509_certificate(cert_request.cert_pem.encode())

        # Verify certificate
        verified, error = validator.verify_certificate(cert, ca_cert)

        if verified:
            return {"verified": True}
        else:
            raise HTTPException(status_code=400, detail=f"Certificate verification failed: {error}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/revoke")
def revoke_certificate(cert_request: CertificateRequest):
    try:
        # Receive certificate to revoke from client
        cert = load_pem_x509_certificate(cert_request.cert_pem.encode())

        # Revoke certificate (replace with proper revocation process in production)
        if cert.subject.serial_number in issued_certificates:
            del issued_certificates[cert.subject.serial_number]
            return {"revoked": True}
        else:
            raise HTTPException(status_code=404, detail="Certificate not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#################################################
