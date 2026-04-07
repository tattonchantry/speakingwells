import resend
import os
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")

def send_message_notification(to_email: str, cardholder_name: str, sender_name: str, sender_email: str, message_body: str):
    sender_display = sender_name or "Someone"
    reply_to = sender_email or FROM_EMAIL
    
    params = {
        "from": f"SpeakingWells <{FROM_EMAIL}>",
        "to": [to_email],
        "reply_to": reply_to,
        "subject": f"Someone noticed {cardholder_name} today!",
        "html": f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #e8a838;">Someone noticed {cardholder_name}! 💛</h2>
            <p><strong>{sender_display}</strong> scanned {cardholder_name}'s card and sent this message:</p>
            <div style="background: #f9f5e7; border-left: 4px solid #e8a838; padding: 15px; margin: 20px 0; border-radius: 4px;">
                <p style="font-size: 16px; font-style: italic;">"{message_body}"</p>
            </div>
            {'<p>You can reply directly to this email to respond to ' + sender_name + '.</p>' if sender_email else ''}
            <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
            <p style="color: #999; font-size: 12px;">SpeakingWells — Because everyone deserves to be noticed.</p>
        </div>
        """
    }
    
    resend.Emails.send(params)
