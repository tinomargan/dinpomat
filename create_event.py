from datetime import datetime, timedelta
from quickstart import cal_setup
import streamlit as st

def create_event(datum, vrijeme, naziv_predmeta, ucionica, naziv):
    # creates one hour event tomorrow 10 AM IST

    service = cal_setup()
    format_str = '%d.%m.%Y.'  # The format
    datetime_obj = datetime.strptime(datum, format_str)
    start = datetime_obj.isoformat()
    end = (datetime_obj + timedelta(days=1)).isoformat()

    event_result = service.events().insert(calendarId='primary',
                                           body={
                                               "summary": naziv_predmeta + " - "+naziv,
                                               "description": "Vrijeme pisanja: "+vrijeme + "\nUčionica: "+ucionica,
                                               'start': {
                                                   'dateTime': start,  # date here
                                                   'timeZone': 'Europe/Belgrade',
                                               },
                                               'end': {
                                                   'dateTime': end,  # date here
                                                   'timeZone': 'Europe/Belgrade',
                                               },
                                           }
                                           ).execute()

    print("created event")
    print("id: ", event_result['id'])
    print("summary: ", event_result['summary'])
    print("starts at: ", event_result['start']['dateTime'])
    print("ends at: ", event_result['end']['dateTime'])

if __name__ == '__main__':
    create_event()
