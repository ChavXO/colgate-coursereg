#!/usr/bin/python
import bs4
import requests
import itertools
import getpass

## temporary file that stores the page so I can later open in
## and analyse its contents
#f = open('afterLog.html', 'w')
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
    #f.write(r.text.encode("utf-8"))
    return (session, logged_in)

def reg_courses(session, crns, pin):
    # alternate pin
    pin_data = {
        'pin': pin, 
    }
    
    PIN_URL = "https://bannersv04.colgate.edu/prod/bwskfreg.P_CheckAltPin"
    r = session.post(PIN_URL, data=pin_data)
    #f.write(r.text.encode("utf-8"))
    
    #scrape required data from file
    soup = bs4.BeautifulSoup(r.text)
    wait_row = soup.find('input', attrs={'name':'wait_row'})['value']
    add_row = soup.find('input', attrs={'name':'add_row'})['value']
    regs_row = soup.find('input', attrs={'name':'regs_row'})['value']

    rsts_in_dict = soup.find_all('input', attrs={'name':'RSTS_IN'})
    rsts_in = []
    for i in rsts_in_dict:
        rsts_in.append(i['value'])
    
    assoc_term_dict = soup.find_all('input', attrs={'name':'assoc_term_in'})
    assoc_term_in = []
    for i in assoc_term_dict:
        assoc_term_in.append(i['value'])
    
    start_date_dict = soup.find_all('input', attrs={'name':'start_date_in'})
    start_date_in = []
    for i in start_date_dict:
        start_date_in.append(i['value'])
    
    end_date_dict = soup.find_all('input', attrs={'name':'end_date_in'})
    end_date_in = []
    for i in end_date_dict:
        end_date_in.append(i['value'])
    
    crn_dict = soup.find_all('input', attrs={'name':'CRN_IN'})
    crn_in = []
    for i in crn_dict:
        try:
            crn_in.append(i['value'])
        except:
            crn_in.append("")
    crn_in += crns

    subj_dict = soup.find_all('input', attrs={'name':'SUBJ'})
    subj = []
    for i in subj_dict:
        subj.append(i['value'])
    
    crse_dict = soup.find_all('input', attrs={'name':'CRSE'})
    crse = []
    for i in crse_dict:
        crse.append(i['value'])
    
    sec_dict = soup.find_all('input', attrs={'name':'SEC'})
    sec = []
    for i in sec_dict:
        sec.append(i['value'])
    
    levl_dict = soup.find_all('input', attrs={'name':'LEVL'})
    levl = []
    for i in levl_dict:
        levl.append(i['value'])
    
    cred_dict = soup.find_all('input', attrs={'name':'CRED'})
    cred = []
    for i in cred_dict:
        cred.append(i['value'])
    
    gmod_dict = soup.find_all('input', attrs={'name':'GMOD'})
    gmod = []
    for i in gmod_dict:
        gmod.append(i['value'])
    
    title_dict = soup.find_all('input', attrs={'name':'TITLE'})
    title = []
    for i in title_dict:
        title.append(i['value'])
    
    mesg_dict = soup.find_all('input', attrs={'name':'MESG'})
    mesg = []
    for i in mesg_dict:
        mesg.append(i['value'])
    
    reg_btn_dict = soup.find_all('input', attrs={'name':'REG_BTN'})
    reg_btn = []
    for i in reg_btn_dict:
        reg_btn.append(i['value'])
    reg_btn += ["Submit Changes"]
    
    reg_data = {'REG_BTN': ["DUMMY", "Submit Changes"],
        'term_in': 201502,
        'CRN_IN' : crn_in,
        'start_date_in': start_date_in,
        'assoc_term_in': assoc_term_in,
        'CRSE': crse,
        'TITLE': title,
        'GMOD': gmod,
        'MESG': mesg,
        'CRED': cred,
        'LEVL': levl,
        'SUBJ': subj,
        'SEC': sec,
        'REGS_ROW': regs_row,
        'WAIT_ROW': wait_row,
        'ADD_ROW': add_row,
        'end_date_in': end_date_in,
        'RSTS_IN' : rsts_in}
                
    r = session.post(final_reg_URL, data=reg_data)    
    #f.write(r.text.encode("utf-8"))
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
