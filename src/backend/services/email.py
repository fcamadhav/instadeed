import logging
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional

logger = logging.getLogger("instadeed")

SMTP_HOST = os.environ.get("SMTP_HOST", "")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")
SMTP_FROM = os.environ.get("SMTP_FROM", "noreply@instadeed.io")

def send_email(to: str, subject: str, body_text: str, body_html: Optional[str] = None) -> bool:
    if not SMTP_HOST or not SMTP_USER:
        logger.warning("SMTP not configured. Would send email to %s: %s", to, subject)
        logger.warning("Email body: %s", body_text[:200])
        return False
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = SMTP_FROM
        msg["To"] = to
        msg.attach(MIMEText(body_text, "plain"))
        if body_html:
            msg.attach(MIMEText(body_html, "html"))
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        logger.info("Email sent to %s: %s", to, subject)
        return True
    except Exception as e:
        logger.error("Failed to send email to %s: %s", to, e)
        return False

def send_otp_email(to: str, otp: str) -> bool:
    subject = "Your Instadeed OTP Code"
    body_text = f"Your OTP for Instadeed is: {otp}\n\nThis code expires in 5 minutes.\n\n- Instadeed Team"
    body_html = f"""
    <html><body style="font-family:Arial,sans-serif;padding:20px;background:#f8fafc;">
    <div style="max-width:480px;margin:0 auto;background:white;border-radius:12px;padding:24px;border:1px solid #e2e8f0;">
    <h2 style="color:#1e3a5f;margin-bottom:16px;">🔐 Instadeed OTP</h2>
    <p style="color:#475569;margin-bottom:20px;">Use the code below to sign in. Expires in 5 minutes.</p>
    <div style="text-align:center;font-size:32px;font-weight:bold;letter-spacing:8px;color:#2563eb;background:#eff6ff;padding:16px;border-radius:8px;margin-bottom:20px;">{otp}</div>
    <p style="color:#94a3b8;font-size:12px;margin-top:20px;">If you didn't request this, ignore this email.<br>&copy; 2026 Instadeed Legal Suite</p>
    </div></body></html>"""
    return send_email(to, subject, body_text, body_html)
