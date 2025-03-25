#!/usr/bin/env python3
import secrets
import os

api_key = secrets.token_hex(32)

print("\n=========================================")
print(f"API Key generada: {api_key}")
print("=========================================")
print("\nPara usar esta clave, añádela al archivo .env:")
print('API_KEY="' + api_key + '"\n')

update_env = input(
    "¿Quieres actualizar el archivo .env automáticamente? (s/n): ").lower()

if update_env == 's' or update_env == 'si':
    env_path = os.path.join(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))), '.env')

    if os.path.exists(env_path):
        with open(env_path, 'r') as file:
            env_content = file.read()

        if 'API_KEY=' in env_content:
            env_content = "\n".join([
                line if not line.startswith(
                    'API_KEY=') else f'API_KEY="{api_key}"'
                for line in env_content.split('\n')
            ])
        else:
            env_content += f'\nAPI_KEY="{api_key}"\n'

        with open(env_path, 'w') as file:
            file.write(env_content)
            print(f"El archivo .env ha sido actualizado con la nueva API Key.")
    else:
        print(f"No se encontró el archivo .env en {env_path}")
