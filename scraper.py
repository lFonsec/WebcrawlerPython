import csv
import time
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

chromedriver_path = 'C:/Users/lucas/Documents/Python/Webdriver/chromedriver.exe'
brave_path = 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe'
s = Service(chromedriver_path)
option = webdriver.ChromeOptions()
option.binary_location = brave_path
browser = webdriver.Chrome(service=s, options=option)
url = 'https://www.paodeacucar.com/adega/secoes/6511/Cervejas?default_filters=%7B%22isRoot%22%3Atrue%2C%22filterId%22%3A%22categoria' \
      '%22%2C%22filterValue%22%3A%22cervejas%22%7D%3B&sort=price%252Brev'
browser.get(url)

lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
match = False
while match is False:
    lastCount = lenOfPage
    time.sleep(1.5)
    lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    if lastCount == lenOfPage:
        match = True

data = datetime.datetime.now()
soup = BeautifulSoup(browser.page_source, 'html.parser')
product_card = soup.find_all('div', {"class": "product-cardstyles__InnerContainer-sc-1uwpde0-4 ggdQez"})
nome_produto = []
preco_produto = []
filename = 'Scrapper ' + str(data.day) + '_' + str(data.month) + '.csv'

with open(filename, 'w', encoding='latin-1') as csvfile:
    fieldnames = ['Nome', 'Precos']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for valor in product_card:

        nome_produto = valor.find('a', {"class": "product-cardstyles__Link-sc-1uwpde0-6 kJkixe hyperlinkstyles__Link-j02w35-0 cZAwm"}).contents
        aux = valor.find('span', {"class": "buttonstyles__Text-sc-1mux0mx-1 jBMxTB"}).string  # pega o valor do botao
        checa_botao = str(aux)  # e muda pra string
        preco_produto = valor.find('div', {"class": "seal-sale-box-divided__Value-pf7r6x-3 bgtGEw"})

        if preco_produto is not None:
            preco_produto = preco_produto.contents
        elif checa_botao == "Indispon??vel":  # checa se botao ta indisponivel
            preco_produto = ['R$00,00']
        else:
            preco_produto = valor.find("div", {"class": "price-tag-normal__LabelPrice-fb5itg-0 iFihUZ"}).contents

        writer.writerow({'Nome': nome_produto, 'Precos': preco_produto})

browser.close()

