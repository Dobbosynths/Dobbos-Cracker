import sys
import os
import subprocess
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import base64	
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.firefox.service import Service as FirefoxService

menu=True
email=""
hashs=""

os.environ['MOZ_HEADLESS'] = '1'
driver = webdriver.Firefox()
actions = ActionChains(driver)

def sprint(text, second=0.007):
    for line in text + '\n':
        sys.stdout.write(line)
        sys.stdout.flush()
        time.sleep(second)

def clearScreen():
    os.system("clear")
    return

url = "https://breachdirectory.p.rapidapi.com/"

headers = {
	"X-RapidAPI-Key": "5b09f05f4fmshc36d848670be752p190f4ajsn62272c9f77c9",
	"X-RapidAPI-Host": "breachdirectory.p.rapidapi.com"
}



while menu == True:
    sprint("______      _     _               _____                _                .--.._⠀ ")          
    sprint("|  _  \    | |   | |             /  __ \              | |               | _   ` ")        
    sprint('| | | |___ | |__ | |__   ___  ___| /  \/_ __ __ _  ___| | _____ _ __    |(")    ')
    sprint("| | | / _ \| '_ \| '_ \ / _ \/ __| |   | '__/ _` |/ __| |/ / _ \ '__|   J' `.   ")
    sprint("| |/ / (_) | |_) | |_) | (_) \__ \ \__/\ | | (_| | (__|   <  __/ |      |/,\'   ")
    sprint("|___/ \___/|_.__/|_.__/ \___/|___/\____/_|  \__,_|\___|_|\_\___|_|      |\|/    ")
    sprint("--------------------------------------------------------------------------------")
    print("1)Search an email for a hash")
    print("2)Enter a hash to be decrypted")
    print("3)Exit app")
    userchoice=int(input("Enter a number to select an option: "))
    if userchoice == 1:
        clearScreen()
        email=str(input("Enter the email you wish to search: "))
        querystring = {"func":"auto","term":email}
        response = requests.get(url, headers=headers, params=querystring)
        print(response.json())
    elif userchoice == 2:
        driver.get("https://hashes.com/en/decrypt/hash")
        captcha = driver.find_element(By.TAG_NAME, "img")
        if captcha.is_displayed():
            img_captcha_base64 = driver.execute_async_script("""
            var ele = arguments[0], callback = arguments[1];
            ele.addEventListener('load', function fn(){
            ele.removeEventListener('load', fn, false);
            var cnv = document.createElement('canvas');
            cnv.width = this.width; cnv.height = this.height;
            cnv.getContext('2d').drawImage(this, 0, 0);
            callback(cnv.toDataURL('image/jpeg').substring(22));
            }, false);
            ele.dispatchEvent(new Event('load'));
            """, captcha)
            with open(r"captcha.jpg", 'wb') as f:
                f.write(base64.b64decode(img_captcha_base64))
            clearScreen()
            code=input("Look in your folder for the captcha image and enter the code: ")
            textForCaptcha = driver.find_element(By.NAME, "captcha")
            textForCaptcha.send_keys(code)
            hashInput = str(input("What is your hash?: "))
            textForHash = driver.find_element(By.XPATH, "//textarea[@id='hashes']")
            textForHash.send_keys(hashInput)
            submit = driver.find_element(By.CSS_SELECTOR, ".px-4.btn.btn-primary")
            actions.click(submit).perform()
            time.sleep(5)
            result = driver.find_element(By.CLASS_NAME, "py-1")
            if result.is_displayed():
                print((result).text)
                driver.quit()
            else:
                print("You have entered the captcha wrong please try again")
                driver.quit()
        else:
            print ("No captcha found")
            hashInput = str(input("What is your hash?: "))
            textForHash = driver.find_element(By.XPATH, "//textarea[@id='hashes']")
            textForHash.send_keys(hashInput)
            result = driver.find_element(By.TAG_NAME, "pre")
            print(result)
            driver.quit()
    else:
        menu == False
        quit()
