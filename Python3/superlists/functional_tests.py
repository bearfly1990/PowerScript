from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
    def tearDown(self):
        self.browser.quit()
        
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
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy peacock feathers' for row in rows)
        )
        # page show another input filed could be type
        # She input "Use peacock feathers to make a fly"
        self.fail('Finish the test!')
        # Page refresh again and to-do list show both two items
          
        # She want to know if this websit will remember this list
          
        # She see the websit generate her own URL and some words to explain this for her
          
        # She visit this URL and find her to-list is still there
          
        # She feel good about this and go to sleep.    
if __name__ == '__main__':
    unittest.main(warnings='ignore')  
