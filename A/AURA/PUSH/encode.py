import base64

def encode_base64url(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

with open('vapid_public.pem', 'rb') as f:
    public_key = f.read()
    
vapid_public_key_encoded = encode_base64url(public_key)
print("VAPID Public Key (Base64 URL Encoded):", vapid_public_key_encoded)
