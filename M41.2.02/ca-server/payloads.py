from pydantic import BaseModel, Field


class CertificateRequest(BaseModel):
    subject_name: str = Field(..., description="The subject name for the certificate")


class VerificationRequest(BaseModel):
    cert_pem: str = Field(..., description="The PEM formatted certificate to be verified")


class RevocationRequest(BaseModel):
    cert_pem: str = Field(..., description="The PEM formatted certificate to be revoked")
