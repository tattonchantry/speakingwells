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

def send_welcome_email(to_email: str):
    params = {
        "from": f"SpeakingWells <{FROM_EMAIL}>",
        "to": [to_email],
        "subject": "Welcome to SpeakingWells!",
        "html": f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #e8a838;">Welcome to SpeakingWells! 💛</h2>
            <p>Thank you for signing up. Your account is ready and your card page is live.</p>
            <p style="margin-top: 16px;">Here is what happens next:</p>
            <ol style="margin-top: 12px; line-height: 2;">
                <li>Within 24 hours we will email you a proof of your card design</li>
                <li>Reply to approve it</li>
                <li>250 free cards will be mailed to your address within 5-7 business days</li>
            </ol>
            <p style="margin-top: 24px;">If you have any questions reply to this email and we will get back to you.</p>
            <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
            <p style="color: #999; font-size: 12px;">SpeakingWells - Because everyone deserves to be noticed.</p>
        </div>
        """
    }
    resend.Emails.send(params)

def send_admin_signup_notification(to_email: str, new_user_email: str, shipping_address: str):
    params = {
        "from": f"SpeakingWells <{FROM_EMAIL}>",
        "to": [to_email],
        "subject": "New SpeakingWells signup!",
        "html": f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #e8a838;">New signup! 💛</h2>
            <p>A new family just created a SpeakingWells account.</p>
            <div style="background: #f9f5e7; border-left: 4px solid #e8a838; padding: 15px; margin: 20px 0; border-radius: 4px;">
                <p><strong>Email:</strong> {new_user_email}</p>
                <p><strong>Mailing address:</strong> {shipping_address or 'Not provided'}</p>
            </div>
            <p>Log in to the admin panel to review their card setup once they complete it.</p>
            <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
            <p style="color: #999; font-size: 12px;">SpeakingWells - Because everyone deserves to be noticed.</p>
        </div>
        """
    }
    resend.Emails.send(params)

def send_admin_card_notification(to_email: str, cardholder_name: str, slug: str, user_email: str, shipping_address: str, card_message: str, color_scheme: str):
    params = {
        "from": f"SpeakingWells <{FROM_EMAIL}>",
        "to": [to_email],
        "subject": f"New card setup complete - {cardholder_name}!",
        "html": f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #e8a838;">New card ready to order! 💛</h2>
            <p>A family has completed their card setup and is ready to receive their first 250 cards.</p>
            <div style="background: #f9f5e7; border-left: 4px solid #e8a838; padding: 15px; margin: 20px 0; border-radius: 4px;">
                <p><strong>Cardholder name:</strong> {cardholder_name}</p>
                <p><strong>Card message:</strong> {card_message}</p>
                <p><strong>Color scheme:</strong> {color_scheme}</p>
                <p><strong>Card page:</strong> <a href="https://speakingwells.org/card/{slug}">speakingwells.org/card/{slug}</a></p>
                <p><strong>QR code:</strong> <a href="https://speakingwells.org/card/{slug}/qr.png">Download QR code</a></p>
                <p><strong>Family email:</strong> {user_email}</p>
                <p><strong>Ship cards to:</strong> {shipping_address or 'Not provided'}</p>
            </div>
            <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
            <p style="color: #999; font-size: 12px;">SpeakingWells - Because everyone deserves to be noticed.</p>
        </div>
        """
    }
    resend.Emails.send(params)

def send_password_reset_email(to_email: str, token: str):
    reset_url = f"https://speakingwells.org/reset-password?token={token}"
    params = {
        "from": f"SpeakingWells <{FROM_EMAIL}>",
        "to": [to_email],
        "subject": "Reset your SpeakingWells password",
        "html": f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #e8a838;">Reset your password 💛</h2>
            <p>We received a request to reset your SpeakingWells password. Click the button below to choose a new one.</p>
            <div style="text-align: center; margin: 32px 0;">
                <a href="{reset_url}" style="background: #e8a838; color: white; padding: 16px 32px; border-radius: 8px; text-decoration: none; font-size: 18px;">Reset My Password</a>
            </div>
            <p style="color: #999; font-size: 13px;">This link expires in 1 hour. If you did not request a password reset you can ignore this email.</p>
            <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
            <p style="color: #999; font-size: 12px;">SpeakingWells - Because everyone deserves to be noticed.</p>
        </div>
        """
    }
    resend.Emails.send(params)

def send_verification_email(to_email: str, token: str):
    verify_url = f"https://speakingwells.org/verify?token={token}"
    params = {
        "from": f"SpeakingWells <{FROM_EMAIL}>",
        "to": [to_email],
        "subject": "Please verify your SpeakingWells email",
        "html": f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #e8a838;">Almost there! 💛</h2>
            <p>Thank you for signing up for SpeakingWells. Please verify your email address to get started.</p>
            <div style="text-align: center; margin: 32px 0;">
                <a href="{verify_url}" style="background: #e8a838; color: white; padding: 16px 32px; border-radius: 8px; text-decoration: none; font-size: 18px;">Verify My Email</a>
            </div>
            <p style="color: #999; font-size: 13px;">If you did not create a SpeakingWells account you can ignore this email.</p>
            <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
            <p style="color: #999; font-size: 12px;">SpeakingWells - Because everyone deserves to be noticed.</p>
        </div>
        """
    }
    resend.Emails.send(params)
