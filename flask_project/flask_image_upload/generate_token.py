from flask_jwt_extended import create_access_token

api_key = '123456'  # Replace with your actual API key
token = create_access_token(identity=api_key)

print(token)
