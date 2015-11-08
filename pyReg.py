## pyreg
import datetime
import bs4
import requests
import itertools
import pytz

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
    
def reg_courses(username, password):
    '''
    register for courses
    '''
    session = requests.Session()
    login_to_portal(session, username, password)
    r = session.get('http://bannersv04.colgate.edu:10003/ssomanager/c/SSB')
    REGISTRATION_URL = "https://bannersv04.colgate.edu/prod/bwskfreg.P_AltPin"
    SEARCH_URL = "https://bannersv04.colgate.edu/prod/bwskfcls.p_sel_crse_search"
    form_data = {
        'term_in': 201502
    }
    r = session.post(SEARCH_URL, data=form_data)
    form_data = {
        'sel_subj': "COSC", 
        'term_in' : 201502,
        'sel_crse' : "",
        'sel_title': "",
        'begin_hh' : "",
        'begin_mi' : "",
        'begin_ap': "",
        'sel_day' : "dummy",
        'sel_ptrm' : "dummy",
        'end_hh' : "",
        'end_mi' : "",
        'end_ap' : "",
        'sel_camp' : "dummy",
        'sel_schd' : "dummy",
        'sel_sess' : "dummy",
        'sel_instr' : "dummy",
        'sel_attr' : "dummy",
        'sel_levl' : "dummy",
        'sel_insm' : "dummy",
        'sub_btn' : "Course Search",
        'crn' : "dummy",
        'rsts' : "dummy",
        'path' : "dummy"
    }
    PIN_URL = "https://bannersv04.colgate.edu/prod/bwskfreg.P_CheckAltPin"
    COURSES_URL = "https://bannersv04.colgate.edu/prod/bwskfcls.P_GetCrse"
    r = session.post(COURSES_URL, data=form_data)
    f.write(r.text.encode("utf-8"))
    
reg_courses("mchavinda", "ChavXO93*")
