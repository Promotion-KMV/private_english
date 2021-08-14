import unittest
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox(executable_path="/home/vlad/Django_projects/privatenglish/english/geckodriver")

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('репетитор', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h3').text
        self.assertIn('Анастасия', header_text)
        input_box = self.browser.find_element_by_id('exampleFormControlInput1')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Как вас зовут',
        )
        button = self.browser.find_element_by_tag_name('button')
        self.assertEqual(
            button.text,
            'Отправить'
        )


if __name__ == "__main__":
    unittest.main(warnings='ignore')