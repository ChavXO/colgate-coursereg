#!/usr/bin/python
import bs4
import requests
import itertools
import getpass

## temporary file that stores the page so I can later open in
## and analyse its contents
f = open('afterLog.html', 'w')
final_reg_URL = "https://bannersv04.colgate.edu/prod/bwckcoms.P_Regs"

def login_to_portal(username, password):
    session = requests.Session()
    LOGIN_URL = 'https://cas.colgate.edu/cas/login'
    logged_in = False
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
    soup = bs4.BeautifulSoup(r.text)
    # very primitive validation check. Must be a better way to do it with requests
    if str(soup.p)[12: 24] == "successfully":
        logged_in  = True
    f.write(r.text.encode("utf-8"))
    return (session, logged_in)

def reg_courses(session, crns, pin):
    # alternate pin
    pin_data = {
        'pin': pin, 
    }
    
    PIN_URL = "https://bannersv04.colgate.edu/prod/bwskfreg.P_CheckAltPin"
    r = session.post(PIN_URL, data=pin_data)
    f.write(r.text.encode("utf-8"))
    reg_data = {'REG_BTN': "Submit Changes",
		'term_in': 201502,
		'CRN_IN' : crns,
		'start_date_in': "DUMMY",
		'assoc_term_in': "DUMMY",
		'CRSE': "DUMMY",
		'TITLE': "DUMMY",
		'GMOD': "DUMMY",
		'MESG': "DUMMY",
		'CRED': "DUMMY",
		'LEVL': "DUMMY",
		'SUBJ': "DUMMY",
		'SEC': "DUMMY",
		'REGS_ROW': 0,
		'WAIT_ROW': 0,
		'ADD_ROW': 10,
		'end_date_in': "DUMMY",
		'RSTS_IN' : "RE"}
				
    r = session.post(final_reg_URL, data=reg_data)    
    print r.text
    return session

def reg_courses2(username, password, pin, crns):
    '''
    register for courses. TODO: Add more parameters
    '''
    session = login_to_portal(username, password)
    session = login_to_banner(session, pin)
    reg_data = {'REG_BTN': "Submit Changes",
				'CRN_IN' : crns}
				
    r = session.post(final_reg_URL, data=reg_data)
    return session

def login_to_banner(session):
    r = session.get('http://bannersv04.colgate.edu:10003/ssomanager/c/SSB')
    REGISTRATION_URL = "https://bannersv04.colgate.edu/prod/bwskfreg.P_AltPin"
    # term data to pass into selection form
    form_data = {
        'term_in': 201502
    }
    
    r = session.post(REGISTRATION_URL, data=form_data)
    return session

def get_crns():
    crns = []
    i = 1
    while True:
        crn = raw_input(str(i) + ") Enter CRN (Press enter when done.)- ")
        if crn.strip() == "":
	    print "Done."
	    break
        try:
            crns.append(str(int(crn.strip())))
        except:
            print "CRNs must be numbers only."
        i += 1
    return crns

def main():
    username = raw_input("Enter your Colgate Username: ")
    password = getpass.getpass("Enter you Colgate account password: ")
    reg_pin = raw_input("Enter your registration PIN: ")
    crns = get_crns()
    reg_courses(username, password, reg_pin, crns)
    
if __name__ == "__main__":
    main()
