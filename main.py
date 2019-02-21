import requests
import datetime
import json
import pandas as pd
import mailer

master_email = ""

def main():
    auth_dic = {
      # Insert key:value, i.e. 'name1':['User ID','API Token]
    }
    email_dic = {
      # 'name of user':'email',
    }

    today = datetime.date.today()

    for name in auth_dic:
        user = hab_user(auth_dic[name])
        user.get_daily()

    for name in email_dic:
        mailer.mailer(email_dic[name],'Habitica {0}'.format(today), master_email)



class hab_user(object):
    def __init__(self, auth):
        self.__user__ = auth[0]
        self.__key__ = auth[1]
        self.__daily__ = {}

    def get_daily(self):
        global master_email
        auth_headers = {'x-api-user': self.__user__, 'x-api-key': self.__key__}
        r = requests.get('https://habitica.com/export/userdata.json', headers=auth_headers)
        if r.status_code != 200:
            input('User "{0}" received Server HTML Response code {1} \n '
                  'Press any button to continue'.format(self.__user__, r.status_code))
            quit()
        user_habitica = json.loads(r.text)
        for daily in range(len(user_habitica['tasks']['dailys'])):
            self.__daily__[user_habitica['tasks']['dailys'][daily]['text']] = \
                [ \
                    user_habitica['tasks']['dailys'][daily]['completed'],\
                    user_habitica['tasks']['dailys'][daily]['yesterDaily'], \
                    user_habitica['tasks']['dailys'][daily]['streak']
                ]

        table = pd.DataFrame.from_dict(data=self.__daily__, orient='index') # Convert __daily__ to dataframe
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        table.columns = [today, yesterday, 'Streak']
        html = table.to_html()
        master_email+= '{0}'.format(self.__user__)
        master_email += html

        
main()
