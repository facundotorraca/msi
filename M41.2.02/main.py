import os
import payloads
from fastapi import FastAPI
from utils.zip import zip_files
from utils.file import save_file
from datetime import datetime, UTC
from fastapi.responses import FileResponse
from services.revoker import RevokerService
from services.generator import GeneratorService
from services.validator import ValidatorService

#################### CONSTS #####################
ROOT_KEY_PATH = "./certs/root-ca.key"
ROOT_CERT_PATH = "./certs/root-ca.pem"

TEMP_SERVER_FILES = "./tmp"
TEMP_GEN_CERTS = f"{TEMP_SERVER_FILES}/gencerts"

OUTPUT_KEYS_NAME = "cert.key"
OUTPUT_CERTS_NAME = "cert.pem"

os.makedirs(TEMP_GEN_CERTS, exist_ok=True)
#################################################

##################### APP #######################
app = FastAPI(
    title="MSI Certificate Authority",
    description="Simple Certificate Authrorithy for MSI - Criptography I course",
)
#################################################

################ ROOT CERTIFICATE ###############
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


@app.get("/")
async def root():
    return {"app-name": "MSI Certificate Authority"}


@app.post("/generate")
async def generate_certificate(request: payloads.CertificateRequest):
    private_key, certificate = generator.generate_certificate(
        request.subject_name, request.is_ca, request.path_length
    )

    base_path = os.path.join(TEMP_GEN_CERTS, str(datetime.now(UTC).timestamp()))

    key_path = save_file(certificate, os.path.join(base_path, "cert.pem"))
    cert_path = save_file(private_key, os.path.join(base_path, "cert.key"))

    zip_path = zip_files(
        os.path.join(base_path, "cert.zip"),
        {key_path: "cert.key", cert_path: "cert.pem"},
    )

    return FileResponse(
        zip_path,
        headers={"Content-Disposition": f"attachment; filename=cert.zip"},
    )


@app.post("/verify")
async def verify_certificate(request: payloads.VerificationRequest):
    is_valid = validator.verify_certificate(request.cert_pem.encode())
    return {"is_valid": is_valid}


@app.post("/revoke")
async def revoke_certificate(request: payloads.RevocationRequest):
    crl = revoker.revoke_certificate(request.cert_pem.encode())
    return {"crl": crl.decode()}
