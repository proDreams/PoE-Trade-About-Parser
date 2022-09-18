from selenium import webdriver
import time
import pickle

options = webdriver.ChromeOptions()
options.headless = True
url_en = 'https://www.pathofexile.com/trade/about'
url_ru = 'https://ru.pathofexile.com/trade/about'
driver = webdriver.Chrome(executable_path='.\\chromedriver.exe', options=options)


def parsing(url):
    global text
    driver.get(url=url)
    driver.add_cookie({"name": "POESESSID", "domain": ".pathofexile.com", "value": "ENTER POESESSID"})
    driver.get(url=url)
    time.sleep(5)
    first_element = driver.find_element('xpath', '//*[@id="trade"]/div[4]/div[1]/div[2]')
    first_elements = first_element.find_elements('class name', 'filter-group')
    result_dic = {}
    for category in first_elements:
        if ('Item Tags' in category.text and 'Maps' not in category.text and 'Cards' not in category.text) or (
                'Тэги предмета - ' in category.text and 'Карты' not in category.text and 'Гадальные карты' not in category.text):
            if 'Item Tags' in category.text:
                text = category.text.replace('Item Tags - ', '')
            elif 'Тэги предмета' in category.text:
                text = category.text.replace('Тэги предмета - ', '')
            result_dic[text] = {}
            second_element = category.find_element('class name', 'filter-group-body')
            second_elements = second_element.find_elements('class name', 'filter')
            for item in second_elements:
                item_name = item.find_element('class name', 'filter-title').get_attribute('textContent').strip()
                item_alt_name = item.find_element('class name', 'form-control').get_attribute('value')
                if 'whispering' in item_alt_name or 'muttering' in item_alt_name or 'weeping' in item_alt_name or 'wailing' in item_alt_name or 'screaming' in item_alt_name:
                    continue
                result_dic[text].update({item_name: item_alt_name})
        print('Please wait...')
    return result_dic


print('Start parsing English site')
with open('bd_en.pkl', 'wb') as f:
    pickle.dump(parsing(url_en), f)
print('Start parsing Russian site')
with open('bd_ru.pkl', 'wb') as f:
    pickle.dump(parsing(url_ru), f)
print('Parsing complite')
time.sleep(5)
driver.close()
driver.quit()
