import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app
import logging

logger = logging.getLogger(__name__)

def send_email(to, subject, template, **kwargs):
    """
    Send email using SMTP
    
    Args:
        to (str): Recipient email address
        subject (str): Email subject
        template (str): HTML template for email body
        **kwargs: Additional arguments to format the template
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Get email config from environment
        smtp_server = os.environ.get('SMTP_SERVER', 'smtp.example.com')
        smtp_port = int(os.environ.get('SMTP_PORT', 587))
        smtp_username = os.environ.get('SMTP_USERNAME', '')
        smtp_password = os.environ.get('SMTP_PASSWORD', '')
        sender_email = os.environ.get('SENDER_EMAIL', 'noreply@example.com')
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = to
        
        # Format template with kwargs
        html = template.format(**kwargs)
        part = MIMEText(html, 'html')
        msg.attach(part)
        
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            if smtp_username and smtp_password:
                server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, to, msg.as_string())
            
        logger.info(f"Email sent to {to}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return False

def send_password_reset_email(user, token):
    """
    Send password reset email
    
    Args:
        user: User model instance
        token: Password reset token
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    reset_url = f"{current_app.config.get('FRONTEND_URL', '')}/reset-password?token={token}"
    
    template = """
    <html>
    <body>
        <p>Hello {username},</p>
        <p>You requested a password reset. Please click the link below to reset your password:</p>
        <p><a href="{reset_url}">Reset Password</a></p>
        <p>If you did not request this reset, please ignore this email.</p>
        <p>The link will expire in 24 hours.</p>
    </body>
    </html>
    """
    
    return send_email(
        to=user.email,
        subject="Password Reset Request",
        template=template,
        username=user.username,
        reset_url=reset_url
    )

def send_confirmation_email(user, token):
    """
    Send email confirmation email
    
    Args:
        user: User model instance
        token: Email confirmation token
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    confirm_url = f"{current_app.config.get('FRONTEND_URL', '')}/confirm-email?token={token}"
    
    template = """
    <html>
    <body>
        <p>Hello {username},</p>
        <p>Thank you for registering! Please click the link below to confirm your email address:</p>
        <p><a href="{confirm_url}">Confirm Email</a></p>
        <p>If you did not register on our site, please ignore this email.</p>
    </body>
    </html>
    """
    
    return send_email(
        to=user.email,
        subject="Please Confirm Your Email Address",
        template=template,
        username=user.username,
        confirm_url=confirm_url
    )
