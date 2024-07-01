import os
import zipfile
import payloads
from fastapi import FastAPI
from datetime import datetime, UTC
from fastapi.responses import FileResponse
from services.revoker import RevokerService
from services.generator import GeneratorService
from services.validator import ValidatorService

##################### APP #######################
app = FastAPI(
    title="MSI Certificate Authority",
    description="Simple Certificate Authrorithy for MSI - Criptography I course",
)
#################################################

################ ROOT CERTIFICATE ###############
ROOT_KEY_PATH = "./certs/root-ca.key"
ROOT_CERT_PATH = "./certs/root-ca.pem"

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

    unix_time = datetime.now(UTC).timestamp()
    key_filename = "cert.key"
    cert_filename = "cert.pem"
    zip_filename = f"{unix_time}.zip"

    zip_path = os.path.join("./tmp/gencerts", zip_filename)
    key_path = os.path.join("./tmp/gencerts", key_filename)
    cert_path = os.path.join("./tmp/gencerts", cert_filename)

    os.makedirs("./tmp/gencerts", exist_ok=True)

    with open(key_path, "wb") as key_file:
        key_file.write(private_key)
    with open(cert_path, "wb") as cert_file:
        cert_file.write(certificate)

    with zipfile.ZipFile(zip_path, "w") as zipf:
        zipf.write(key_path, key_filename)
        zipf.write(cert_path, cert_filename)

    return FileResponse(
        cert_path,
        headers={"Content-Disposition": f"attachment; filename={zip_filename}"},
    )


@app.post("/verify")
async def verify_certificate(request: payloads.VerificationRequest):
    is_valid = validator.verify_certificate(request.cert_pem.encode())
    return {"is_valid": is_valid}


@app.post("/revoke")
async def revoke_certificate(request: payloads.RevocationRequest):
    crl = revoker.revoke_certificate(request.cert_pem.encode())
    return {"crl": crl.decode()}
