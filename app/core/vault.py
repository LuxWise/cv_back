import os
import hvac
from dotenv import load_dotenv

load_dotenv()

VAULT_URL = os.getenv("VAULT_ADDR")
VAULT_TOKEN = os.getenv("VAULT_TOKEN")
VAULT_KV_MOUNT=os.getenv("VAULT_KV_MOUNT")
VAULT_JWT_CV_BACK_PATH=os.getenv("VAULT_JWT_CV_BACK_PATH")
VAULT_CV_BACK_PATH=os.getenv("VAULT_CV_BACK_PATH")

def _client() -> hvac.Client:
    if not VAULT_URL or not VAULT_TOKEN:
        raise ValueError("Vault URL or Token not set in environment variables.")
    
    client = hvac.Client(url=VAULT_URL, token=VAULT_TOKEN)
    if not client.is_authenticated():
        raise ConnectionError("Failed to authenticate with Vault.")
    
    return client

def _get_KV(mount: str, path: str):
    client = _client()
    read_response = client.secrets.kv.v2.read_secret_version(
        mount_point=mount,
        path=path
    )
    return read_response['data']['data']

# JWT Secrets
def _get_JWT_secret():
    return _get_KV(VAULT_KV_MOUNT, VAULT_JWT_CV_BACK_PATH)

def get_JWT_private_key():
    jwt_secrets = _get_JWT_secret()
    return jwt_secrets.get("private_key")

def get_JWT_issuer():
    jwt_secrets = _get_JWT_secret()
    return jwt_secrets.get("issuer")

def get_JWT_audience():
    jwt_secrets = _get_JWT_secret()
    return jwt_secrets.get("audience")

# CV Back Secrets
def _get_secret():
    return _get_KV(VAULT_KV_MOUNT, VAULT_CV_BACK_PATH)

def get_jwt_secret_key():
    secrets = _get_secret()
    return secrets.get("jwt_secret_key")

def get_smtp_host():
    secrets = _get_secret()
    return secrets.get("SMTP_HOST")

def get_smtp_port():
    secrets = _get_secret()
    return secrets.get("SMTP_PORT")

def get_smtp_user():
    secrets = _get_secret()
    return secrets.get("SMTP_USER")

def get_smtp_pass():
    secrets = _get_secret()
    return secrets.get("SMTP_PASS")

def get_url_groq_service():
    secrets = _get_secret()
    return secrets.get("URL_GROQ_SERVICE")
