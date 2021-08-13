from selenium import webdriver

browser = webdriver.Firefox(executable_path="/home/vlad/Django_projects/privatenglish/english/geckodriver")
# driver_two = webdriver.Chrome("/home/vlad/test_TDD/chromedriver")
browser.get('http://localhost:8000')
assert 'репетитор' in browser.title
