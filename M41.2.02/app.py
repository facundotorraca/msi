import payloads
from fastapi import FastAPI
from services.revoker import RevokerService
from services.generator import GeneratorService
from services.validator import ValidatorService

##################### APP #######################
app = FastAPI("MSI Certificate Authority")
#################################################

################ ROOT CERTIFICATE ###############
ROOT_KEY_PATH = "certs/root-ca.key"
ROOT_CERT_PATH = "certs/root-ca.pem"

with open(ROOT_CERT_PATH, "rb") as f:
    root_cert_pem = f.read()
with open(ROOT_KEY_PATH, "rb") as f:
    root_key_pem = f.read()
#################################################

#################### SERVICES ###################
revoker = RevokerService(root_cert_pem, root_key_pem)
validator = ValidatorService(root_cert_pem)
generator = GeneratorService(root_cert_pem, root_key_pem)
#################################################


@app.post("/generate")
async def generate_certificate(request: payloads.CertificateRequest):
    private_key, certificate = generator.generate_certificate(
        request.subject_name, request.is_ca, request.path_length
    )
    return {"private_key": private_key.decode(), "certificate": certificate.decode()}


@app.post("/verify")
async def verify_certificate(request: payloads.VerificationRequest):
    is_valid = validator.verify_certificate(request.cert_pem.encode())
    return {"is_valid": is_valid}


@app.post("/revoke")
async def revoke_certificate(request: payloads.RevocationRequest):
    crl = revoker.revoke_certificate(request.cert_pem.encode())
    return {"crl": crl.decode()}
