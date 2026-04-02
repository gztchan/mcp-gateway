import os
import requests

def gamma_request(path: str, method: str, params: dict = None, headers: dict = None):
    response = requests.request(
      url=f"{os.getenv('GAMMA_API_URL')}/{path}",
      method=method,
      params=params,
      headers=headers,
    )
    return response.json()

def clob_request(path: str, method: str, params: dict = None, headers: dict = None):
    response = requests.request(
      url=f"{os.getenv('CLOB_API_URL')}/{path}",
      method=method,
      params=params,
      headers=headers,
    )
    return response.json()