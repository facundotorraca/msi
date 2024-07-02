import ssl
import uvicorn
from fastapi import FastAPI

app = FastAPI()

KEY_FILE = "./certs/cert.key"
PEM_FILE = "./certs/cert.pem"


@app.get("/")
def read_root():
    return {"message": "Hello, TLS!"}


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=443,
        ssl_keyfile=KEY_FILE,
        ssl_certfile=PEM_FILE,
        ssl_version=ssl.PROTOCOL_TLS,
        ssl_ciphers="ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20",
    )
