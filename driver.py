import getpass 
import selenium as sl
from selenium.webdriver.common.keys import Keys

class driver():
    def __init__(self, username):
        self.usr = username
        self.driver = sl.webdriver.Chrome()
        self.login(username)

    def login(self, username):
        self.driver.get('https://en.lichess.org/login')
        
        print 'after get'

        name = self.driver.find_element_by_name('username')
        name.clear()
        name.send_keys(self.usr)
        
        passwd = self.driver.find_element_by_name('password')
        passwd.clear()
        password = getpass.getpass()
        passwd.send_keys(password)
        passwd.send_keys(Keys.RETURN)
        

    def __repr__(self):
        return self.driver.get_page_source()

    def close(self):
        self.driver.close()

if __name__ == '__main__':


    d = driver('PenguinArsonist')

    print d

    d.close()
    

