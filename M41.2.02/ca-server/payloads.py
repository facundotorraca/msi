from pydantic import BaseModel, Field


class CertificateRequest(BaseModel):
    subject_name: str = Field(..., description="The subject name for the certificate")
    is_ca: bool = Field(
        default=False, description="Flag indicating if this certificate should be a CA"
    )
    path_length: int | None = Field(
        default=None, description="The path length constraint for CA certificates, if applicable"
    )


class VerificationRequest(BaseModel):
    cert_pem: str = Field(..., description="The PEM formatted certificate to be verified")


class RevocationRequest(BaseModel):
    cert_pem: str = Field(..., description="The PEM formatted certificate to be revoked")
