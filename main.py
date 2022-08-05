from selenium import webdriver
import time
import pickle

url = 'https://www.pathofexile.com/trade/about'
driver = webdriver.Chrome(executable_path='.\\chromedriver.exe')

driver.get(url=url)
time.sleep(5)
first_element = driver.find_element('xpath', '//*[@id="trade"]/div[4]/div[1]/div[2]')
first_elements = first_element.find_elements('class name', 'filter-group')
result_dic = {}
for category in first_elements:
    if 'Item Tags' in category.text and 'Maps' not in category.text and 'Cards' not in category.text:
        text = category.text.replace('Item Tags - ', '')
        result_dic[text] = {}
        second_element = category.find_element('class name', 'filter-group-body')
        second_elements = second_element.find_elements('class name', 'filter')
        for item in second_elements:
            item_name = item.find_element('class name', 'filter-title').get_attribute('textContent').strip()
            item_alt_name = item.find_element('class name', 'form-control').get_attribute('value')
            result_dic[text].update({item_name: item_alt_name})
with open('bd.pkl', 'wb') as f:
    pickle.dump(result_dic, f)
time.sleep(5)
driver.close()
driver.quit()
