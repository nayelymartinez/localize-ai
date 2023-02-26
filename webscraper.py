import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


"""
	Homepage scrape using Beautiful Soup.
"""
def homepage_webscrape():
	url = "https://www.getimmigrante.com/"

	homePage = requests.get(url)

	homeSoup = BeautifulSoup(homePage.content, "html.parser")
	hpResults = homeSoup.find(id="SITE_CONTAINER")

	hpTextElements = hpResults.find_all("div", class_="wixui-text")
	with open('homepage.txt', 'w') as f:
		for textElement in hpTextElements:
			print(textElement.text)
			f.write(textElement.text + "\n")

"""
	FAQ page scrape using Selenium to get around iFrames
"""
def faq_webscrape():
	DRIVER_PATH = '/usr/local/bin/chromedriver'
	faqURL = 'https://www.getimmigrante.com/faq'

	options = Options()
	options.headless = True
	options.add_argument("--window-size=1920,1200")

	driver = webdriver.Chrome(executable_path=DRIVER_PATH)
	driver.get(faqURL)
	iframe = driver.find_element(By.TAG_NAME, 'iframe')
	driver.switch_to.frame(iframe)
	faqText = driver.find_element(By.ID, 'accordion').text

	with open('faq.txt', 'w') as f:
		f.write(textElement.text + "\n")

	driver.quit()

if __name__ == '__main__':
	homepage_webscrape()
	faq_webscrape()