import os
import aiosmtplib
from email.message import EmailMessage

from jinja2 import Environment, FileSystemLoader, select_autoescape
from app.core.vault import *
from pathlib import Path

SMTP_HOST = get_smtp_host()
SMTP_PORT = get_smtp_port()
SMTP_USER = get_smtp_user()
SMTP_PASS = get_smtp_pass()

TEMPLATES_DIR = Path(__file__).resolve().parents[2] / "html_templates"

_jinja = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=select_autoescape(["html", "xml"]),
)

def _render_register_html(code: str) -> str:
    template = _jinja.get_template("register.html")
    return template.render(code=code)

async def send_email_verification(to: str, subject: str, code: str):
    message = EmailMessage()
    message["From"] = SMTP_USER
    message["To"] = to
    message["Subject"] = subject
    message.set_content(_render_register_html(code), subtype="html")

    await aiosmtplib.send(
        message,
        hostname=SMTP_HOST,
        port=SMTP_PORT,
        username=SMTP_USER,
        password=SMTP_PASS,
        start_tls=True,
        timeout=20,
    )