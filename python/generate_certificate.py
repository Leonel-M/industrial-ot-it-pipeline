import datetime
import os

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

from config import CERT_DIR, CLIENT_CERT_PATH, CLIENT_KEY_PATH, CLIENT_APPLICATION_URI

def generate(hostname: str = "localhost"):
    os.makedirs(CERT_DIR, exist_ok=True)

    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, "industrial-ot-it-pipeline-python-client"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Portfolio Project"),
    ])

    san = x509.SubjectAlternativeName([
        x509.UniformResourceIdentifier(CLIENT_APPLICATION_URI),
        x509.DNSName(hostname),
    ])

    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.now(datetime.timezone.utc))
        .not_valid_after(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=825))
        .add_extension(san, critical=False)
        .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
        .sign(key, hashes.SHA256())
    )

    with open(CLIENT_CERT_PATH, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.DER))

    with open(CLIENT_KEY_PATH, "wb") as f:
        f.write(
            key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )
    
    print(f"Certificado generado: {CLIENT_CERT_PATH}")
    print(f"Llave privada generada: {CLIENT_KEY_PATH}")
    print(f"Application URI horneado en el SAN: {CLIENT_APPLICATION_URI}")
    print("\nSiguiente paso: correr opcua_client.py y confiar el certificado en CODESYS.")

if __name__ == "__main__":
    generate()