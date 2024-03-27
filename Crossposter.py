import json
import praw
import requests
import pandas as pd
from time import sleep
import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service


class NRC:
    def __init__(self):
        self.NSFW = True
        self.from_subreddits_list = self.to_subreddits_list = list()
        self.sub_to_data = self.sub_from_data = list()

        self.headers = {
            'authority': 'www.reddit.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-US,en;q=0.9',
        }

        self.params = (('count', '100'),)

        # Time delays
        self.HOW_OFTEN_TO_CHECK_AND_CROSSPOST = 220
        self.delay_inbetween_data_downloads = 10

        # Reddit API Credentials
        self.id = 'TyiRercJZkxYNXryjjvyJQ'
        self.secret = 'gJAVZvC3RmKdlkukxoHNh1cPb_7rJQ'
        self.username = 'Mary65Bates'
        self.password = 'P2PHAGTHOV1FX6A'

        # Data files
        self.sub_to_filename = 'data/sub_to_data.json'
        self.sub_from_filename = 'data/sub_from_data.json'
        self.from_subreddits_file = 'SUB_FROM.txt'
        self.to_subreddits_file = 'SUB_TO.txt'

        # Data url Endpoints
        self.frequencies = ['hot', 'top']

        self.sub_from_data = list()

        # Initialize the reddit api
        self.reddit = praw.Reddit(user_agent='pass',
                                  client_id=self.id,
                                  client_secret=self.secret,
                                  username=self.username,
                                  password=self.password)
        # Main
        try:
            self.initialize()
            self.run()
        except KeyboardInterrupt:
            print('\n\n\nThis program has been stopped.')

    def initialize(self):
        global from_subreddits_list
        with open(self.from_subreddits_file, 'r') as reader:
            self.from_subreddits_list = set(reader.read().strip().split('\n'))

        with open(self.to_subreddits_file, 'r') as reader:
            self.to_subreddits_list = set(reader.read().strip().split('\n'))

    def replace_with_download_data_after_done_testing(self):
        with open(self.sub_to_filename, 'r') as reader:
            self.sub_to_data = json.loads(reader.read())
        with open(self.sub_from_filename, 'r') as reader:
            self.sub_from_data = json.loads(reader.read())

    def download_data(self):
        """
        This can be done better, but it's functioning...so w/e
        """

        # Load the to_subbreddits_json data
        for subreddit in self.to_subreddits_list:
            for frequency in self.frequencies:
                url = f'https://reddit.com/r/{subreddit}/{frequency}/.json'
                r = requests.get(url, headers=self.headers, params=self.params)
                content = r.json()
                sleep(self.delay_inbetween_data_downloads)
                self.sub_to_data.append(content)
                with open(self.sub_to_filename, 'w') as writer:
                    json.dump(self.sub_to_data, writer)

        # Load the from_subbreddits_json data
        for subreddit in self.from_subreddits_list:
            for frequency in self.frequencies:
                url = f'https://reddit.com/r/{subreddit}/{frequency}/.json'
                r = requests.get(url, headers=self.headers, params=self.params)
                content = r.json()
                sleep(self.delay_inbetween_data_downloads)
                self.sub_from_data.append(content)
                with open(self.sub_from_filename, 'w') as writer:
                    json.dump(self.sub_from_data, writer)

    def is_post_already_crossposted(self, check_link):
        for frequency in self.sub_to_data:
            for p in frequency['data']['children']:
                stripped_permalink = p['data']['permalink'].split('/')[-2].split('/')[0]
                if stripped_permalink in check_link:
                    return True
        return False


    def run(self):
        while True:
            print('Starting new loop...')
            sleep(1)
            # print('Loading new data')
            # self.download_data()
            # self.replace_with_download_data_after_done_testing()
            # print("Grabbing and checking top posts...\n\n\n")
            # set options for headless browser
            # options = Options()
            # options.add_argument('--headless')
            s = Service("D:\chromedriver\chromedriver_win32\chromedriver.exe")
            # Set up the driver to use Google Chrome
            # driver = webdriver.Chrome(service=s,options=options)
            driver = webdriver.Chrome(service=s)

            # Navigate to the Reddit login page
            driver.get("https://www.reddit.com/login")


            # Find the email and password fields and enter your login credentials
            email_field = driver.find_element(By.NAME, "username")
            email_field.send_keys("Xunanazamon ")

            password_field = driver.find_element(By.NAME, "password")
            password_field.send_keys("656LAZ9JFOMXDFD")

            # Submit the form to log in
            password_field.send_keys(Keys.RETURN)

            time.sleep(10)
            # maximize the screen
            pyautogui.hotkey('win', 'up')
            for SUB_TO in self.to_subreddits_list:
                subreddit = f"https://www.reddit.com/r/{SUB_TO}/submit?source_id=t3_13bp9sg"
                # Navigate to the post URL
                driver.get(subreddit)
                time.sleep(10)
                # Find all the div elements with a particular class
                post_divs = driver.find_element(By.XPATH, '//div[@class="_1T0P_YQg7fOYLCRoKl_xxO "]')
                post_divs.click()
                print(f'{self.from_subreddits_list} to {SUB_TO}')
                try:
                    if driver.find_element(By.CLASS_NAME,
                                           '_3h_9YwxjuOr77VhScPrjCI').text == "This community has the same crosspost within last 24 hours" or driver.find_element(
                            By.CLASS_NAME,
                            '_3h_9YwxjuOr77VhScPrjCI').text == "This community does not allow for crossposting of any posts"  or driver.find_element(By.CLASS_NAME,'_3h_9YwxjuOr77VhScPrjCI').text =="Please fix the above requirements":
                        print("Skipping ", SUB_TO)
                except:
                    pass
                time.sleep(10)
            break
if __name__ == '__main__':
    NRC()

#   my_dict['Sub'] = SUB_TO
#   my_dict['Link'] = p.permalink
#    df = df.append(my_dict, ignore_index=True)
#    print("appending...")
#    df.to_csv('subreddits_subscriber_count.csv', index=False)

 #                   except:
 #                                      print(f'Skipping {SUB_TO}')
 #                                      pass
#                   except:
#                       print(f'Skipping {SUB_TO}')
#                       pass


#            break
# else:
# print(f"Skipping https://www.reddit.com{str(p.permalink)}...")