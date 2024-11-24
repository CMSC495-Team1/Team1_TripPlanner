import fileinput
import secrets
import os

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(project_root, '.env')

# Generate a secure secret key
secret_key = secrets.token_hex(32)

# Read .env file and update SECRET_KEY
with fileinput.FileInput(env_path, inplace=True) as file:
    for line in file:
        if line.startswith('SECRET_KEY='):
            print(f'SECRET_KEY={secret_key}')
        else:
            print(line, end='')

print(f'\nNew secret key generated: {secret_key}')
print('Your .env file has been updated!')
