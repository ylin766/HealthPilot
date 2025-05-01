# plugins/smtp_plugin.py
import smtplib
import ssl
from email.message import EmailMessage
from semantic_kernel.functions import kernel_function
import os
import chainlit as cl
from typing import Optional
from dotenv import load_dotenv # Make sure dotenv is loaded if running standalone

# Load .env if not loaded globally elsewhere in your app entry point
load_dotenv()

class SmtpPlugin:
    """Plugin for sending emails via Gmail SMTP using App Password."""

    def __init__(self):
        # Load Gmail credentials from environment variables
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 465 # Standard port for SMTP_SSL with Gmail
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.app_password = os.getenv("APP_PASSWORD") # Use the App Password here

        if not all([self.sender_email, self.app_password]):
            print("Warning: Gmail SMTP environment variables (GMAIL_SENDER_EMAIL, GMAIL_APP_PASSWORD) not fully configured.")
            # Decide how to handle this - maybe raise an error or disable the plugin

    @kernel_function(
        name="send_email_smtp", # Keep the generic name or change to send_email_gmail if preferred
        description="Sends an email using the configured Gmail account via SMTP."
    )
    async def send_email_smtp(
        self,
        to_recipients: str, # Comma-separated list of email addresses
        subject: str,
        body_content: str,
        is_html: bool = False, # Set to True if body_content is HTML
        cc_recipients: Optional[str] = None,
        bcc_recipients: Optional[str] = None
    ) -> str:
        """
        Sends an email via Gmail SMTP using App Password.

        Args:
            to_recipients: Comma-separated recipient email addresses.
            subject: The subject of the email.
            body_content: The content of the email body (plain text or HTML).
            is_html: Set to True if body_content is HTML. Default is False.
            cc_recipients: Optional comma-separated CC recipient email addresses.
            bcc_recipients: Optional comma-separated BCC recipient email addresses.

        Returns:
            A confirmation or error message string.
        """
        if not all([self.sender_email, self.app_password]):
             return "❌ Gmail SMTP service not configured. Set GMAIL_SENDER_EMAIL and GMAIL_APP_PASSWORD."

        async with cl.Step(name="Sending Email via Gmail SMTP", type="tool") as step:
            try:
                msg = EmailMessage()
                msg['Subject'] = subject
                msg['From'] = self.sender_email
                msg['To'] = to_recipients # Comma-separated string is usually handled correctly

                all_rcpt = to_recipients.split(',')
                if cc_recipients:
                    msg['Cc'] = cc_recipients
                    all_rcpt.extend(cc.strip() for cc in cc_recipients.split(','))
                if bcc_recipients:
                    # BCC recipients are NOT put in the header, they are passed to send_message
                    all_rcpt.extend(bcc.strip() for bcc in bcc_recipients.split(','))

                # Filter out any empty strings that might result from splitting
                all_rcpt = [r.strip() for r in all_rcpt if r.strip()]


                if is_html:
                    msg.set_content("Please enable HTML to view this email.") # Fallback content
                    msg.add_alternative(body_content, subtype='html')
                else:
                    msg.set_content(body_content)

                # Establish secure SSL connection directly
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                    server.login(self.sender_email, self.app_password) # Login with email and App Password
                    server.send_message(msg, from_addr=self.sender_email, to_addrs=all_rcpt)

                step.output = f"Email sent successfully via Gmail to {to_recipients}."
                return f"✅ Email sent successfully via Gmail to {to_recipients}."

            except smtplib.SMTPAuthenticationError as e:
                 error_msg = f"❌ Gmail SMTP Authentication Error: Check email/App Password and ensure 'Less secure app access' is NOT needed (App Passwords bypass this). Original error: {e}"
                 step.output = error_msg
                 print(error_msg)
                 return error_msg
            except Exception as e:
                error_msg = f"❌ Error sending Gmail email: {e}"
                step.output = error_msg
                print(error_msg)
                return error_msg