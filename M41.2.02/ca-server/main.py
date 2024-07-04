import base64
import os
import payloads
from fastapi import FastAPI
from utils.zip import zip_files
from datetime import datetime, UTC
from utils.file import save_bin_file, save_json_file
from fastapi.responses import FileResponse
from services.revoker import RevokerService
from services.generator import GeneratorService
from services.validator import ValidatorService

################################# CONSTS #################################
ROOT_KEY_PATH = "./certs/root.key"
ROOT_CERT_PATH = "./certs/root.pem"

TEMP_SERVER_FILES = "./tmp"
TEMP_CRL_FILES = f"{TEMP_SERVER_FILES}/crl"
TEMP_GEN_CERTS = f"{TEMP_SERVER_FILES}/certs"

OUTPUT_KEYS_NAME = "cert.key"
OUTPUT_CERTS_NAME = "cert.pem"

os.makedirs(TEMP_GEN_CERTS, exist_ok=True)
os.makedirs(TEMP_CRL_FILES, exist_ok=True)

with open(ROOT_CERT_PATH, "rb") as f:
    root_cert_pem = f.read()

with open(ROOT_KEY_PATH, "rb") as f:
    root_key_pem = f.read()
##########################################################################

################################## APP ###################################
app = FastAPI(
    title="MSI Certificate Authority",
    description="Certificate Authrorithy for MSI - Criptography I course",
)
##########################################################################

################################ SERVICES ################################
revoker = RevokerService(root_cert_pem, root_key_pem, TEMP_CRL_FILES)
validator = ValidatorService(root_cert_pem, TEMP_CRL_FILES)
generator = GeneratorService(root_cert_pem, root_key_pem)
##########################################################################


@app.get("/")
async def root():
    return {"app-name": "MSI Certificate Authority"}


@app.post("/generate")
async def generate_certificate(request: payloads.CertificateRequest):
    private_key, certificate = generator.generate_certificate(request.subject_name)

    # Convert binary data to a suitable format for JSON (e.g., Base64)
    certificate_encoded = certificate.decode("utf-8")
    private_key_encoded = base64.b64encode(private_key).decode("utf-8")
    key_cert_json = {"priv_key": private_key_encoded, "cert_pem": certificate_encoded}

    base_path = os.path.join(TEMP_GEN_CERTS, str(datetime.now(UTC).timestamp()))

    key_path = save_bin_file(certificate, os.path.join(base_path, "cert.pem"))
    cert_path = save_bin_file(private_key, os.path.join(base_path, "cert.key"))
    json_path = save_json_file(key_cert_json, os.path.join(base_path, "cert.json"))

    zip_path = zip_files(
        os.path.join(base_path, "cert.zip"),
        {key_path: "cert.key", cert_path: "cert.pem", json_path: "cert.json"},
    )

    return FileResponse(
        zip_path,
        headers={"Content-Disposition": f"attachment; filename=cert.zip"},
    )


@app.post("/verify")
async def verify_certificate(request: payloads.VerificationRequest):
    is_valid, reason = validator.verify_certificate(request.cert_pem.encode())
    return {"is_valid": is_valid, "message": reason}


@app.post("/revoke")
async def revoke_certificate(request: payloads.RevocationRequest):
    revoker.revoke_certificate(request.cert_pem.encode())
    return {"message": "Certificate revoked"}
