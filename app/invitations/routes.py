import smtplib
import os
from flask import Blueprint, request, jsonify
from email.mime.text import MIMEText
from app.extensions import mongo
from bson import ObjectId

invite_bp = Blueprint('invite', __name__)

@invite_bp.route('/invite', methods=['POST'])
def invite_user():
    data = request.get_json()
    email = data.get('email')
    sender_id = ObjectId(data.get('sender_id'))

    mongo.db.invitations.insert_one({
        "sender_id": sender_id,
        "email": email
    })

    # Load SMTP config
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_user = os.getenv("SMTP_USERNAME")
    smtp_pass = os.getenv("SMTP_PASSWORD")

    if not all([smtp_server, smtp_port, smtp_user, smtp_pass]):
        return jsonify({
            "message": "Invitation saved, but email failed: missing SMTP configuration"
        }), 500

    try:
        smtp_port = int(smtp_port)
    except ValueError:
        return jsonify({
            "message": "Invitation saved, but email failed: invalid SMTP_PORT"
        }), 500

    # Build and send email
    subject = "You've been invited to Combly 🐝"
    body = f"You've been invited to join Combly. Visit: https://combly.vercel.app"
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, [email], msg.as_string())
    except Exception as e:
        return jsonify({
            "message": f"Invitation saved, but email failed: {str(e)}"
        }), 500

    return jsonify({"message": "Invitation sent successfully"}), 201
