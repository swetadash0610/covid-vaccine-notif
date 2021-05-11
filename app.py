from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from cowin_api import CoWinAPI
import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)
from_ = os.environ['FROM']
to = os.environ['TO']

district_id = os.environ['DIST']
min_age_limit = os.environ['AGE']
pin_code = os.environ['PIN']
cowin = CoWinAPI()
available_centers = cowin.get_availability_by_district(
    district_id, min_age_limit)
available_centers = available_centers['centers']

# If successfully connected , you will receive this message on first run
success = "You are successsfully connected to vaccine slot notifier. You will receive a message if slots are available in district ID "+str(district_id)+" and has a minimum age limit of "+str(min_age_limit)+" years"
message = client.messages.create(
    body=success,
    from_=from_,
    to=to
)

def notify():
    print("called") 
    for value in available_centers:
        for session in value['sessions']:
            body = str(value['name'])+" Date: "+str(session['date']) + \
                " Slots: "+str(session['available_capacity'])
            if session['min_age_limit'] == int(min_age_limit) and session['available_capacity'] != 0:
                message = client.messages.create(
                    body=body,
                    from_=from_,
                    to=to
                )

sched = BackgroundScheduler(daemon=True)
sched.add_job(notify, 'interval', minutes=0)
sched.start()
app = Flask(__name__)

@app.route("/")
def index():
    return "COVID VACCINE NOTIFIER!"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True)