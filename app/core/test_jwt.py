from security import create_access_token, decode_access_token

token = create_access_token({
    "sub": "rituraj"
})

print("TOKEN:")
print(token)

payload = decode_access_token(token)

print("\nPAYLOAD:")
print(payload)