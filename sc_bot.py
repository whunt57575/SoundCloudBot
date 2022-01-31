# pip install webdriver-manager
import time
import sys
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

DEFAULT_RUN = 1
LOADING_TIMEOUT = 10
PLAY_TIME = 10
PAUSE_TIME = 5
DEFAULT_URL = "https://soundcloud.com/decentral-mike/basshead-mix2"
PLAY_BUTTON_XPATH = '//*[@id="content"]/div/div[2]/div/div[2]/div[2]/div/div/div[1]'
VOLUME_BUTTON_XPATH= '//*[@id="app"]/div[4]/section/div/div[3]/div[5]/div/div[2]/button'

class SoundCloudBot:
    def __init__(self, count, url):
        self.count = count
        self.url = url

    def run(self):
        for cur_run in range(self.count):
            self.one_run()

    def one_run(self):
            self.__start()
            self.__wait_till_ready()
            self.__mute()
            self.__play()
            self.__pause()
            self.print_play_count()
            self.__close()

    def __start(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get(self.url)

    def __wait_till_ready(self):
        try:
            element_present = EC.presence_of_element_located((By.XPATH, PLAY_BUTTON_XPATH))
            WebDriverWait(self.driver, LOADING_TIMEOUT).until(element_present)
            print("Play button loaded.")
        except TimeoutException:
            print("Timed out waiting for page to load.")

        try:
            element_present = EC.presence_of_element_located((By.XPATH, VOLUME_BUTTON_XPATH))
            WebDriverWait(self.driver, LOADING_TIMEOUT).until(element_present)
            print("Volume button loaded.")
        except TimeoutException:
            print("Timed out waiting for page to load.")

    def __mute(self):
        self.volume_button = self.driver.find_element(By.XPATH, VOLUME_BUTTON_XPATH)
        self.volume_button.click()

    def __play(self):
        self.play_button = self.driver.find_element(By.XPATH, PLAY_BUTTON_XPATH)
        self.play_button.click()
        time.sleep(PLAY_TIME)

    def __pause(self):
        self.pause_button = self.driver.find_element(By.XPATH, PLAY_BUTTON_XPATH)
        self.pause_button.click()
        time.sleep(PAUSE_TIME)
    
    def print_play_count(self):
        play_count_tab = self.driver.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div[1]/div/div[1]/div/div/div[2]/ul/li[1]/span/span[1]')
        print("Current track played count: " + play_count_tab.text)

    def __close(self):
        self.driver.quit()

def main():
    run_count = DEFAULT_RUN
    url = DEFAULT_URL
    if len(sys.argv) > 1:
        run_count = int(sys.argv[1])
    if len(sys.argv) > 2:
        url = sys.argv[2]
    print("Run: " + str(run_count))
    print("Url: " + url)

    bot = SoundCloudBot(run_count, url)
    bot.run()

if __name__ == "__main__":
    main()