from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import pymongo
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def data(url):
    req_url = str(url).strip()
    response = requests.get(req_url, verify=False)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        renter = 'NULL'
        renter_id = 'NULL'
        phone = 'NULL'
        rent_type = 'NULL'
        situation = 'NULL'
        requirement = 'NULL'

        if soup.find('div', {'class': 'avatarRight'}) is not None:
            renter = soup.find('div', {'class': 'avatarRight'}).text.replace('\n', '')
            if '(' in renter:
                renter = renter.split('(')[0]
            else:
                renter = renter.split('（')[0]

        if soup.find('div', {'class': 'avatarRight'}) is not None:
            renter_id = soup.find('div', {'class': 'avatarRight'}).text

            if '(' in renter_id:
                renter_id = renter_id.split('(')[1].split(')')[0]
                if '屋主' in renter_id:
                    renter_id = '屋主'
                elif '仲介' in renter_id:
                    renter_id = '仲介'
            else:
                renter_id = renter_id.split('（')[1].split('）')[0]
                if '屋主' in renter_id:
                    renter_id = '屋主'
                elif '仲介' in renter_id:
                    renter_id = '仲介'

        if soup.find('span', {'class': 'dialPhoneNum'}) is not None:
            phone_find = soup.find('span', {'class': 'dialPhoneNum'})
            if phone_find['data-value'] != '':
                phone = phone_find['data-value']

        rent_type_find = soup.find('ul', {'class': 'attr'}).findAll('li')
        for type in rent_type_find:
            if '型態' in type.text.split(':')[0]:
                rent_type = type.text.split(':')[1].replace('\xa0', '')
            if '現況' in type.text.split(':')[0]:
                situation = type.text.split(':')[1].replace('\xa0', '')

        req = soup.find('ul', {'class': 'clearfix labelList labelList-1'})
        req = req.find_all('li', {'class': 'clearfix'})
        for x in req:
            if x.find('div', {'class': 'one'}).text == '性別要求':
                requirement = x.find_next('div', {'class': 'two'})
                requirement = requirement.find_next('em').text
        print(url, renter, renter_id, phone, rent_type, situation, requirement)
        return renter, renter_id, phone, rent_type, situation, requirement


def main():
    i = 1
    while i <= 3:
        driver = webdriver.Chrome(executable_path="/chromedriver")
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

        driver.get("https://rent.591.com.tw/?kind=0&regionid=" + str(i))
        driver.find_element_by_id('area-box-close').click()

        if i == 1:
            location = '台北市'
        elif i == 3:
            location = '新北市'

        soup = BeautifulSoup(driver.page_source, "html.parser")
        pages_total = int(soup.find('span', class_='R').text.split(' ')[-2]) / 30 + 1
        print('Total pages:', int(pages_total))

        for i in range(int(pages_total)):
            room_url_list = []
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            titles = soup.findAll('h3')
            for title in titles:
                room_url = 'http:' + title.find('a').get('href').replace(' ', '')
                room_url_list.append(room_url)

            for url in room_url_list:
                renter, renter_id, phone, rent_type, situation, requirement = data(url)
                col.insert_one({'出租者': renter,
                                '出租者身份': renter_id,
                                '聯絡電話': phone,
                                '型態': rent_type,
                                '現況': situation,
                                '地點': location,
                                '性別要求': requirement,
                                'url': url
                                }
                               )
            if soup.find('a', {'class': 'pageNext last'}):
                pass
            else:
                driver.find_element_by_class_name('pageNext').click()
        i = i + 2


if __name__ == '__main__':
    client = pymongo.MongoClient(
        "mongodb+srv://dbuser:admin123@cluster0-zke9w.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client['591']
    col = db['db']
    main()
    print('\nfinish!')
