import pyotp
from django.core.mail import send_mail
from core.models import OTP
from twilio.rest import Client
from django.conf import settings
def generate_and_send_otp(user):
    # Generate OTP
    otp_obj = OTP.generate_otp(user)

    # Send OTP via Email (for demonstration, you can use SMS service like Twilio)
    send_mail(
        'Your OTP for verification',
        f'Your OTP is: {otp_obj.otp}',
        settings.FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
    return otp_obj


def send_sms_otp(user):
    # Send OTP via SMS (using Twilio)
    otp_obj = OTP.generate_otp(user)
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        to=user.phone,
        from_=settings.TWILIO_PHONE_NUMBER,
        body=f'Your OTP is: {otp_obj.otp}',
    )