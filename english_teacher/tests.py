import unittest

from selenium import webdriver


# driver_two = webdriver.Chrome("/home/vlad/test_TDD/chromedriver")


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox(executable_path="/home/vlad/Django_projects/privatenglish/english/geckodriver")

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('репетитор', self.browser.title)
        self.fail('Закончить тест')


if __name__ == "__main__":
    unittest.main(warnings='ignore')