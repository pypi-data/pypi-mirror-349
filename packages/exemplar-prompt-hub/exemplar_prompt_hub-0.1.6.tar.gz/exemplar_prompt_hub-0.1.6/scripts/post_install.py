import shutil
import os

def copy_env_file():
    if not os.path.exists('.env'):
        shutil.copy('.env.example', '.env')
        print("Created .env file from .env.example")

if __name__ == '__main__':
    copy_env_file() 