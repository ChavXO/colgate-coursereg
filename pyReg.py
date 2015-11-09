#!/usr/bin/python
import bs4
import requests
import itertools

## temporary file that stores the page so I can later open in
## and analyse its contents
f = open('afterLog.html', 'w')

def login_to_portal(session, username, password):
    LOGIN_URL = 'https://cas.colgate.edu/cas/login'
    
    # to get sessions id cookies `JSESSIONID`
    r = session.get(LOGIN_URL)
    session_id = session.cookies['JSESSIONID']
    
    # to get hidden lt value that needs to be sent with form
    soup = bs4.BeautifulSoup(r.text)
    lt = soup.find('input', attrs={'name': "lt"})['value']

    # to login
    post_url = LOGIN_URL + ';jsessionid=' + session_id
    data = {
        'username': username,
        'password': password,
        'lt': lt,
        'execution': 'e1s1',
        '_eventId': 'submit',
    }
    r = session.post(post_url, data=data)
    
def reg_courses(username, password, pin):
    '''
    register for courses. TODO: Add more parameters
    '''
    session = requests.Session()
    login_to_portal(session, username, password)
    r = session.get('http://bannersv04.colgate.edu:10003/ssomanager/c/SSB')
    REGISTRATION_URL = "https://bannersv04.colgate.edu/prod/bwskfreg.P_AltPin"
    
    # term data to pass into selection form
    form_data = {
        'term_in': 201502
    }
    r = session.post(REGISTRATION_URL, data=form_data)
    
    # alternate pin
    form_data = {
        'pin': int(pin), 
    }
    PIN_URL = "https://bannersv04.colgate.edu/prod/bwskfreg.P_CheckAltPin"
    r = session.post(PIN_URL, data=form_data)
    f.write(r.text.encode("utf-8"))
    return session