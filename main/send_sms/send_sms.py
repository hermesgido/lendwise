import requests
from decouple import config

from BeemAfrica import Authorize, AirTime, OTP, SMS
Authorize(config("BEEM_API_KEY"), config("BEEM_SECRET_KEY"))
response = SMS.send_sms('hello pythonista', '255621189850')
print(response)

def send_sms_beem(message, recipients= [], ):
    Authorize(config("BEEM_API_KEY"), config("BEEM_SECRET_KEY"))
    response = SMS.send_sms('hello pythonista', '255621189850')
    print(response)
    URL = 'https://apisms.beem.africa/v1/send'
    #replace below parameters
    api_key = config("BEEM_API_KEY")
    secret_key = config("BEEM_SECRET_KEY")
    source_addr = "HERYINC"

    session = requests.Session()
    session.auth = (api_key, secret_key)

    response = session.post(URL, data={
                "source_addr": source_addr,
                "encoding": "0",
                "message": message,
                "recipients": recipients
    })
    print(response)
    return response