import requests
import os

API_TOKEN = 'eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJjNjMzYzRlZC1mOGI2LTRlMWQtODRmOS0zZDM1Zjg1YzZlYzIiLCJzdWIiOiJhcGlVc2VyIiwidXNlcklkIjoyLCJjbGllbnRJZCI6MiwidG9rZW5UeXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc4MjU4Nzg1fQ.q3bGF_ekdXrPGvFpsHzozvIh-XNVky1Jp_mDRW6Woro'

api_url = 'https://backend.thestage.ai/user-api/v1/elastic-model/local-run-bundle/get-available-options'
headers = {
    'accept': '*/*',
    'Authorization': f'Bearer {API_TOKEN}'
}
response = requests.post(api_url, headers=headers, json='')
print(response.json())