from utils.rhoodfuncs import *
import json
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
import os.path
from utils.sendmail import send, create_body

body = create_body(test=True)
send("jnasti101@icloud.com", "jo@joeynasti.com", "New AWS Email", body)

"""
response = boto3.sns.client.publish(
    TopicArn='string',
    TargetArn='string',
    PhoneNumber='string',
    Message='string',
    Subject='string',
    MessageStructure='string',
    MessageAttributes={
        'string': {
            'DataType': 'string',
            'StringValue': 'string',
            'BinaryValue': b'bytes'
        }
    },
    MessageDeduplicationId='string',
    MessageGroupId='string'
)

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def main():

  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "windows.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    results = service.users().labels().list(userId="me").execute()
    labels = results.get("labels", [])

    if not labels:
      print("No labels found.")
      return
    print("Labels:")
    for label in labels:
      print(label["name"])

  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()

638631526063-ura0a4rcm9p4duh4n3kb3vcbgoutlopb.apps.googleusercontent.com
login()
options = getOptionsByDate(name="UPRO", date="2024-03-08")
current_price = get_price("UPRO")
market_data = o.get_option_market_data_by_id(options[85]["id"])
print(f'current price = {current_price}')
print(json.dumps(options[85], indent=4))
print(len(options))
print(json.dumps(market_data, indent=4))


def get_days_left():
    curr_date = datetime.now().date()

    two_fridays_out = curr_date - timedelta(days = curr_date.weekday()) + timedelta(days=11)

    days_left = two_fridays_out - curr_date
    print(days_left.days, type(days_left.days))
    return(str(two_fridays_out))

get_days_left()

l = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]

print([(a,b,c,d) for i0, a in enumerate(l) for i1, b in enumerate(l[i0+1:]) for i2, c in enumerate(l[i1+i0+2:]) for d in l[i2+i1+i0+3:]])

print( -1 + 
      (1< 0 and 8) + 
      (1> 0 and 5))

direction = "debit"
price = 2.10
symbol = "TSLA"
quantity = 1
spread = [
    {
        "expirationDate": "2024-03-28",
        "strike":         162.5,
        "optionType":     "call",
        "effect":         "open",
        "action":         "buy"
    },
    {
        "expirationDate": "2024-03-28",
        "strike":         165.0,
        "optionType":     "call",
        "effect":         "open",
        "action":         "sell"
    }
]
login()
print(order_spread(direction, price, symbol, quantity, spread))
"""
