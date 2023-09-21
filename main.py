import time
from random import randint, random
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
import requests
import glob
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, \
    ElementNotInteractableException
import os
import itertools
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import pyautogui
import re

def upload(videoname, id, username, password):
    print(f"uploading video: {id}")
    titlelist = ["you wont belive this video!!!", "I cant belive this!!!", "you have to see this!!",
                 "look at these adorable animals!!!", "these animals are the cutest thing I've ever seen!!!",
                 "OMG!!!! These animals!!!", "The internets cutest animals!!!"]
    i = 0
    print(f"loging in with {username}")
    while i < 6:
        options = uc.ChromeOptions()
        chromeexecutablepath = "/opt/google/chrome/google-chrome"
        options.add_argument("user-data-dir=/home/dillon/.config/google-chrome/'Guest Profile'")
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        if i == 2 or 4:
            driver = uc.Chrome(chrome_options=options, browser_executable_path=chromeexecutablepath, headless=True)
        else:
            driver = uc.Chrome(chrome_options=options)
        driver.delete_all_cookies()
        driver.get("https://www.youtube.com/upload")
        driver.find_element(By.XPATH,'//*[@id="identifierId"]').send_keys(username) #email field
        driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button').click() #click sign in
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="password"]/div[1]/div/div[1]/input')))
            time.sleep(1)
            driver.find_element(By.XPATH,'//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password) #password input
            break
        except (TimeoutException, ElementNotInteractableException):
            print("login failed trying again")
            i += 1
            if i == 6:
                print("login failed too meny times trying the next profile")
                return
    print("login successful")
    driver.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button').click()
    # WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,)))
    #WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,'/html/body/ytd-app/div[1]/div/ytd-masthead/div[4]/div[3]/div[2]/ytd-topbar-menu-button-renderer[1]/div/a/yt-icon-button/button')))
    #driver.find_element(By.XPATH,'/html/body/ytd-app/div[1]/div/ytd-masthead/div[4]/div[3]/div[2]/ytd-topbar-menu-button-renderer[1]/div/a/yt-icon-button/button').click()
    #WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,'/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown[2]/div/ytd-multi-page-menu-renderer/div[3]/div[1]/yt-multi-page-menu-section-renderer/div[2]/ytd-compact-link-renderer[1]')))
    #driver.find_element(By.XPATH,'/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown[2]/div/ytd-multi-page-menu-renderer/div[3]/div[1]/yt-multi-page-menu-section-renderer/div[2]/ytd-compact-link-renderer[1]').click()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="ytcp-uploads-dialog-file-picker"]')))
    driver.find_element(By.XPATH,"//input[@type='file']").send_keys(f"/home/dillon/PycharmProjects/shortsnetwork/{videoname}") # select upload video /home/dillon/PycharmProjects/shortsnetwork/0.mp4
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[1]/ytcp-social-suggestions-textbox/ytcp-form-input-container/div[1]/div[2]/div/ytcp-social-suggestion-input/div')))
    title = driver.find_element(By.XPATH,'/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[1]/ytcp-social-suggestions-textbox/ytcp-form-input-container/div[1]/div[2]/div/ytcp-social-suggestion-input/div')
    title.send_keys(Keys.CONTROL, 'a')
    title.send_keys(Keys.BACKSPACE)
    title.send_keys(titlelist[randint(0,6)]+f"#{id}") #title
    driver.find_element(By.XPATH,'/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[2]/ytcp-social-suggestions-textbox/ytcp-form-input-container/div[1]/div[2]/div/ytcp-social-suggestion-input/div').send_keys(f"Please like and subscribe!!! it would mean alot!!! I hope the video made your day a little better #animals #animal #funny #funnyanimal #meme #shorts #short #like #subscribe #popular #happy") #description
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,'/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[5]/ytkc-made-for-kids-select/div[4]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[2]')))
    driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[5]/ytkc-made-for-kids-select/div[4]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[2]').click()
    driver.find_element(By.XPATH, '//*[@id="next-button"]').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="next-button"]').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="next-button"]').click()
    driver.find_element(By.XPATH,'/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-review/div[2]/div[1]/ytcp-video-visibility-select/div[2]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[3]').click()
    driver.find_element(By.XPATH,'//*[@id="done-button"]').click()
    time.sleep(5)
    driver.close()
    return


def downloadvid(link, id):
    print(f"downloading vid number: {id}")
    import requests

    #getcookies = requests.get('https://ssstik.io')
    #cookies = getcookies.cookies

    cookies = {
        '__gads': 'ID=061a0dc2e4f7288e-22e2a03f85dc0051:T=1680977114:RT=1680977114:S=ALNI_MbaIVL65-V7382872zaYLlRH5AIRQ',
        '_gid': 'GA1.2.1477568093.1682888190',
        '__gpi': 'UID=00000975bb092481:T=1680977114:RT=1682888189:S=ALNI_MaBaNYrJlm_q4J7GZFBVXghbSR7Hw',
        '__cflb': '02DiuEcwseaiqqyPC5qrDCss6XuWcthYMqAUAyYvKjwXq',
        '_gat_UA-3524196-6': '1',
        '_ga': 'GA1.2.2147425815.1680977112',
        '_ga_ZSF3D6YSLC': 'GS1.1.1682888189.2.1.1682889499.0.0.0',
    }

    headers = {
        'authority': 'ssstik.io',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': '__gads=ID=061a0dc2e4f7288e-22e2a03f85dc0051:T=1680977114:RT=1680977114:S=ALNI_MbaIVL65-V7382872zaYLlRH5AIRQ; _gid=GA1.2.1477568093.1682888190; __gpi=UID=00000975bb092481:T=1680977114:RT=1682888189:S=ALNI_MaBaNYrJlm_q4J7GZFBVXghbSR7Hw; __cflb=02DiuEcwseaiqqyPC5qrDCss6XuWcthYMqAUAyYvKjwXq; _gat_UA-3524196-6=1; _ga=GA1.2.2147425815.1680977112; _ga_ZSF3D6YSLC=GS1.1.1682888189.2.1.1682889499.0.0.0',
        'hx-current-url': 'https://ssstik.io/en',
        'hx-request': 'true',
        'hx-target': 'target',
        'hx-trigger': '_gcaptcha_pt',
        'origin': 'https://ssstik.io',
        'referer': 'https://ssstik.io/en',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    }

    params = {
        'url': 'dl',
    }

    data = {
        'id': link,
        'locale': 'en',
        'tt': 'a1piSzg3',
    }

    response = requests.post('https://ssstik.io/abc', params=params, cookies=cookies, headers=headers, data=data)


    downloadsoup = BeautifulSoup(response.text, "html.parser")
    downloadlink = downloadsoup.a["href"]


    mp4file = urlopen(downloadlink)
    with open(f"{id}.mp4","wb") as output:
        while True:
            data = mp4file.read(4096)
            if data:
                output.write(data)
            else:
                break

    print("finished downloading")


if __name__ == '__main__':
    tiktoktags = ["funnyanimals", "animals", "cuteanimals", "chipmunks", "cats", "cat", "funnycats", "funnycat", "dog",
                  "goodboy", "bestdog", "funnydog", "funnydogs", "monkey", "funnymonkey", "hedgehog", "puppy", "kitten",
                  "animalfail", "ape", "funnyape", "pet", "bird", "funnybird", "birds", "elephant", "rabbit", "mouse",
                  "funnyrabbit", "funnyrabbit", ""]
    userdata = []
    numofaccounts = [0,3,2,1]
    videos = []
    listoflinks = []
    listofvideos = glob.glob('/home/dillon/PycharmProjects/shortsnetwork'+'/*.mp4')
    if len(listofvideos) == 0:
        for i in range(3):
            options = uc.ChromeOptions
            driver = uc.Chrome(chrome_options=options)
            driver.get(f"https://www.tiktok.com/tag/{tiktoktags[randint(0, len(tiktoktags)-1)]}?lang=en")
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            videos = soup.find_all("div", {"class": "tiktok-yz6ijl-DivWrapper e1cg0wnj1"})
            href = videos[1].a["href"]
            driver.close()
            for index, video in enumerate(videos):
                copy = 0
                with open('masterlist',"r") as file:
                    for line in file:
                        if re.search(video.a["href"], line):
                            copy = 1
                        else:
                            lines = file.readlines()
                            num_lines = len(lines)
                if copy == 1:
                    continue
                else:
                    downloadvid(video.a["href"], index)
                    time.sleep(10)
                with open("masterlist", "a") as output:
                    output.write("\n"+video.a["href"])

    else:
        with open('masterlist', "r") as file:
            for t, line in enumerate(file):
                linktouple = (t, line)
                listoflinks.append(linktouple)
        num_lines = len(listoflinks)

        for i in range(0,50):
            if not os.path.exists(f"{i}.mp4"):
                continue
            try:
                user_index = i % len(userdata)
                upload(f"{i}.mp4", num_lines + i, userdata[user_index][0], userdata[user_index][1])
                os.remove(f"{i}.mp4")
            except:
                print("upload failed no file for that mp4 found trying the next one")
                continue

