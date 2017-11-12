from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from time import sleep
import unittest
class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        
    def tearDown(self):
        self.browser.quit()
        
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
        
    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('To-Do', self.browser.title)
        #title and header should include "To-Do"
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        # invite to input a to do list
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        # Input "Buy peacock feathers"
        # Her hobby is to fish
        inputbox.send_keys('Buy peacock feathers');
        
        # After input enter, page refreshed
        # To-do list show "1:Buy peacock feathers"
        inputbox.send_keys(Keys.ENTER)
       
        # locator = (By.LINK_TEXT, 'CSDN')
        # locator = (By.ID,'id_list_table')
        # WebDriverWait(self.browser, 20).until(EC.presence_of_element_located(locator))
        sleep(2)
        self.check_for_row_in_list_table('1: Buy peacock feathers');
        # table = self.browser.find_element_by_id('id_list_table')
        # rows = table.find_elements_by_tag_name('tr')
        # self.assertIn('1: Buy peacock feathers', [row.text for row in rows])
        # self.assertTrue(
            # any(row.text == '1: Buy peacock feathers' for row in rows),
            # "New to-do item did not appear in table"
        # )
        # page show another input filed could be type
        # She input "Use peacock feathers to make a fly"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly');
        inputbox.send_keys(Keys.ENTER)
        sleep(2)
        self.check_for_row_in_list_table('1: Buy peacock feathers');
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly');
        sleep(2)
        # table = self.browser.find_element_by_id('id_list_table')
        # rows = table.find_elements_by_tag_name('tr')
        # self.assertIn('1: Buy peacock feathers', [row.text for row in rows])
        # self.assertIn('2: Use peacock feathers to make a fly', [row.text for row in rows])
        # self.fail('Finish the test!')
        # Page refresh again and to-do list show both two items
          
        # She want to know if this websit will remember this list
          
        # She see the websit generate her own URL and some words to explain this for her
          
        # She visit this URL and find her to-list is still there
          
        # She feel good about this and go to sleep.

        
if __name__ == '__main__':
    unittest.main(warnings='ignore')
  
