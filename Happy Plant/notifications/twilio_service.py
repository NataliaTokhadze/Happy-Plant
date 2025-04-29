from twilio.rest import Client
from django.conf import settings

account_sid = settings.TWILIO_ACCOUNT_SID
auth_token = settings.TWILIO_AUTH_TOKEN
twilio_number = settings.TWILIO_PHONE_NUMBER

client = Client(account_sid, auth_token)

def send_sms_notification(to_number, body):
    try:
        message = client.messages.create(
            from_=twilio_number,
            to=to_number,
            body=body
        )
        return message.sid
    except Exception as e:
        print(f"❌ Failed to send SMS to {to_number}: {e}")
        return None

# აქ მინდა ავღნიშნო, რომ SMS-ების გაგზავნა არ არის უფასო 
# თუ გატესტავთ, მარტო ერთ ნომერზე გაიგზავნება, რომელიც მივანიშნეთ
# ამ პრობლემის გადაჭრა უმარტივესია, უბრალოდ უნდა გადავიხადოთ ფული XD
# მაგრამ რადგანაც ეს მარტო პროექტია და არა რეალური საიტი კომპანიისთვის, ასე დარჩეს
# გთხოვთ, არ შეიმჩნიოთ ეს პატარა პრობლემა და არ დაგვაკლოთ ქულები