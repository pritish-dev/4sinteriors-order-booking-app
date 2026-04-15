import urllib.parse

def generate_whatsapp_link(phone, message):
    encoded = urllib.parse.quote(message)
    return f"https://wa.me/91{phone}?text={encoded}"