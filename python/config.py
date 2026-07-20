import os

OPCUA_ENDPOINT = os.getenv("OPCUA_ENDPOINT", "opc.tcp://LAMS:4840")
OPCUA_USERNAME = os.getenv("OPCUA_USERNAME", "Administrator")
OPCUA_PASSWORD = os.getenv("OPCUA_PASSWORD", "")
CLIENT_APPLICATION_URI = os.getenv("OPCUA_CLIENT_URI", "urn:industrial-ot-it-pipeline:python-client")

CERT_DIR = os.path.join(os.path.dirname(__file__), "certs")
CLIENT_CERT_PATH = os.path.join(CERT_DIR, "client_certificate.der")
CLIENT_KEY_PATH = os.path.join(CERT_DIR, "client_private_key.pem")

_BASE = "ns=4;s=|var|CODESYS Control Win V3 x64.Application.GVL."

NODE_IDS = {
    "Line_State": _BASE + "Line_State",
    "Belt_Speed_PV": _BASE + "Belt_Speed_PV",
    "Piece_Count": _BASE + "Piece_Count",
    "Alarm_Active": _BASE + "Alarm_Active",
    "Belt_Speed_SP": _BASE + "Belt_Speed_SP"
}

DB_DIR = os.path.join(os.path.dirname(__file__), "data")
DB_PATH = os.path.join(DB_DIR, "historico.db")