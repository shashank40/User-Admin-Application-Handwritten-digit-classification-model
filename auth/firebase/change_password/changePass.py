import requests

apikey='XXXXXXX' # the web api key
def SendResetEmail(email):
    headers = {
        'Content-Type': 'application/json',
    }
    data={"requestType":"PASSWORD_RESET","email":email}
    r = requests.post('https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={}'.format(apikey), data=data)
    if 'error' in r.json().keys():
        return r.json()['error']['message'], False
    if 'email' in r.json().keys():
        return 'Reset link sent to your email id', True
