import requests

FIREBASE_SERVER_KEY = '901298755649'

def send_push_notification(device_token, title, body):
    url = 'https://fcm.googleapis.com/fcm/send'
    headers = {
        'Authorization': f'key={FIREBASE_SERVER_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        'to': device_token,
        'notification': {
            'title': title,
            'body': body,
        },
        'priority': 'high'
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def send_push_to_multiple_devices(tokens, title, body):
    url = 'https://fcm.googleapis.com/fcm/send'
    headers = {
        'Authorization': f'key={FIREBASE_SERVER_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        'registration_ids': tokens,  # list of tokens
        'notification': {
            'title': title,
            'body': body,
        },
        'priority': 'high'
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()
