import enum
import os

from twilio.rest import Client
from twilio.rest.verify.v2.service.verification import VerificationInstance
from twilio.rest.verify.v2.service.verification_check import VerificationCheckInstance
from twilio.twiml.messaging_response import Message


class OTPLocationEnum(enum.Enum):
    email = 1
    sms = 2
    voice = 3

    def __str__(self):
        if self == OTPLocationEnum.email:
            return "Email"
        elif self == OTPLocationEnum.sms:
            return "SMS"
        elif self == OTPLocationEnum.voice:
            return "Voice"

    def twilio_keyself(self):
        if self == OTPLocationEnum.email:
            return "email"
        elif self == OTPLocationEnum.sms:
            return "sms"
        elif self == OTPLocationEnum.voice:
            return "call"


class TwilioHelper:
    @staticmethod
    def client() -> Client:
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        client = Client(account_sid, auth_token)

        return client

    @staticmethod
    def request_otp(
            to: str,
            via: OTPLocationEnum
    ) -> VerificationInstance:
        service_sid = os.environ['TWILIO_SERVICE_SID']
        client = TwilioHelper.client()

        # verification_check = client.verify \
        #     .v2 \
        #     .services(service_sid) \
        #     .verification_checks \
        #     .create((to=to, code='[Code]'))

        verification = client.verify \
            .v2 \
            .services(service_sid) \
            .verifications \
            .create(to=to, channel=via.twilio_keyself())

        # print(verification.sid)

        return verification

    @staticmethod
    def verify_code(
            to: str,
            code: str
    ) -> VerificationCheckInstance:
        service_sid = os.environ['TWILIO_SERVICE_SID']
        client = TwilioHelper.client()

        verification_check = client.verify \
            .v2 \
            .services(service_sid) \
            .verification_checks \
            .create(to=to, code=code)

        # print(verification_check.status)

        return verification_check
        
    @staticmethod
    def send_email(
            to_email: str,
            subject: str,
            html_content: str,
            from_email: str = ""
    ) -> bool:
        """
        Generic method to send an email using Twilio SendGrid
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML content of the email
            from_email: Sender email address (defaults to configured email)
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        try:
            # Get the configured sender email or use provided one
            sender = from_email
            if not sender:
                sender = os.environ.get('TWILIO_SENDER_EMAIL', "")
                
            if not sender:
                raise ValueError("Sender email not configured. Set TWILIO_SENDER_EMAIL environment variable or provide from_email.")
            
            # Check if SendGrid is available
            try:
                from sendgrid import SendGridAPIClient
                from sendgrid.helpers.mail import Mail
                
                # Get SendGrid API key
                sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')
                if not sendgrid_api_key:
                    raise ValueError("SendGrid API key not found. Set SENDGRID_API_KEY environment variable.")
                
                # Create message
                message = Mail(
                    from_email=sender,
                    to_emails=to_email,
                    subject=subject,
                    html_content=html_content
                )
                
                # Send email
                sg = SendGridAPIClient(sendgrid_api_key)
                response = sg.send(message)
                
                return response.status_code == 202
            except ImportError:
                raise ImportError("SendGrid package not installed. Install it with: pip install sendgrid")
                
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False
