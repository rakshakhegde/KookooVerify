import os
import requests
from hacks.kookooverify.config import *

APP_URL = 'https://hacks-rakheg.rhcloud.com/kookooverify/'
DATA_DIR = os.environ.get('OPENSHIFT_DATA_DIR')
DB_FILE_NAME = 'kookooverify.db'
TABLE_REQUEST_ID = 'request_id'
TABLE_CHECKS = 'checks'
validity = 5*60

def sendSms(phone_no, message, api_key):
        msgUrl = 'https://www.kookoo.in/outbound/outbound_sms.php'
        payload = {'phone_no': phone_no, 'message': message, 'api_key': api_key}
        return requests.get(msgUrl, params= payload).text

def makeCall(phone_no, extra_data):
        callUrl = 'http://www.kookoo.in/outbound/outbound.php'
        return requests.get(callUrl, params= {'phone_no': phone_no,
                                                                                  'api_key': kookoo_api_key,
                                                                                  'extra_data': extra_data}).text
def safeClose(DBconn):
        DBconn.commit()
        DBconn.close()

'''
{
  "request_id": "07d36962c01145beba0f2d1e0a825da0",
  "status": "0",
  "event_id": "03000000CA5D8E87",
  "price": "0.10000000",
  "currency": "EUR"
}
{
  "status": "6",
  "error_text": "The Nexmo platform was unable to process this message for the following reason: Request '07d36962c01145beba0f2d1e0a825da0' was not found or it has been verified already."
}
{
  "request_id": "7b4b9b5368804f9fad0d4c5b0902c251",
  "status": "16",
  "error_text": "The code provided does not match the expected value"
}
{
  "request_id": "623d1cf96a124fb0af472f323c93b4e6",
  "account_id": "bd74f216",
  "number": "918553578836",
  "sender_id": "verify",
  "date_submitted": "2016-01-29 16:09:05",
  "date_finalized": "2016-01-29 16:10:48",
  "checks": [
    {
      "date_received": "2016-01-29 16:10:48",
      "code": "2753",
      "status": "VALID",
      "ip_address": ""
    }
  ],
  "first_event_date": "2016-01-29 16:09:05",
  "last_event_date": "2016-01-29 16:09:05",
  "price": "0.10000000",
  "currency": "EUR",
  "status": "SUCCESS"
}
'''
