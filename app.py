import datetime
from googleapiclient.discovery import build
from oauth2client import file, client, tools
from flask import Flask, request, jsonify, abort
import os
import json
import sys

# If modifying these scopes, delete the file token.json.
# SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
SCOPES = 'https://www.googleapis.com/auth/calendar'
MENU_CALENDAR_ID = 'nfdcum6lvge3s6f3mnl78k25ro@group.calendar.google.com'
CALENDAR_SERVICE_URL = 'https://calendar-u4sp7ks5ea-uc.a.run.app'

# VALID-REFERER = https://johnkellerman-u4sp7ks5ea-uc.a.run.app/
VALID_REFERER = os.getenv('VALID_REFERER', None)
# VALID-PW = fred
VALID_PW = os.getenv('VALID_PW', None)

app = Flask(__name__)

@app.before_request
def do_something_whenever_a_request_comes_in():
    args = request.args
    headers = request.headers
    referer = headers.get('Referer')
    if referer is None or referer != VALID_REFERER:
        pw = args.get('pw')
        if pw is None or pw != VALID_PW:
            print('Authentication error')
            return abort(403)

@app.route('/')
def index():
    args = dict(request.args)

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    calendar_service = build('calendar', 'v3', credentials=creds)

    if args.get('test', None) != None:
        testing_results = []
        testing = True
        print("Testing Deployment...")
        build_info_output = build_info()
    else:
        testing = False
    thisday_ordinal = args.get('thisday', None)
    if thisday_ordinal is None:
        thisday_ordinal = datetime.datetime.now().toordinal()
    else:
        thisday_ordinal = int(thisday_ordinal)
    number_successful = 0
    print("Results:")
    for day in range(thisday_ordinal + 1, thisday_ordinal + 8):
        this_day = datetime.datetime.fromordinal(day).strftime("%Y-%m-%d")
        next_day = datetime.datetime.fromordinal(day + 1).strftime("%Y-%m-%d")
        if day == thisday_ordinal + 7:
            new_event = {"start": {"date": this_day}, "end": {"date": next_day},
                         "description": "\n\n<a href=\"%s?thisday=%s&pw=%s\">Create next week\'s entries</a>" % (CALENDAR_SERVICE_URL, str(day), VALID_PW),
                         "notes": day}
        else:
            new_event = {"start": {"date": this_day}, "end": {"date": next_day},
                         "notes": day}
        if not testing:
            insert_result = calendar_service.events().insert(calendarId=MENU_CALENDAR_ID, body=new_event).execute()
            if insert_result.get('status') == 'confirmed':
                number_successful += 1
            print(insert_result)
        else:
            testing_results.append(new_event)
    if not testing:
        return_result = "Created %s calendar entries starting on %s" % \
                    (number_successful, datetime.datetime.fromordinal(thisday_ordinal + 1).strftime("%Y-%m-%d"))
        print(return_result)
        return return_result
    else:
        results = {'Build Info': build_info_output,
                    'Test Results': testing_results}
        return jsonify(results)

# Be sure not to name this method 'build' as it will conflict with the google API
@app.route('/build', methods=['GET', 'POST'])
def build_info():
    try:
        build_file = open('static/build.txt')
        build_stamp = build_file.readlines()[0]
        build_file.close()
    except FileNotFoundError:
        from datetime import date
        build_stamp = generate_build_stamp()
    results = 'Running %s %s.\nBuild %s.\nPython %s.' % (sys.argv[0], app.name, build_stamp, sys.version)
    return results


def generate_build_stamp():
    from datetime import date
    return 'Development build - %s' % date.today().strftime("%m/%d/%y")


print('Starting %s %s' % (sys.argv[0], app.name))
print('Python: ' + sys.version)
try:
    build_file = open('static/build.txt')
    build_stamp = build_file.readlines()[0]
    build_file.close()
except FileNotFoundError:
    from datetime import date
    build_stamp = generate_build_stamp()
print('Running build: %s' % build_stamp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))


