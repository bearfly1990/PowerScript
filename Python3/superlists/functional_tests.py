from selenium import webdriver
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
        self.fail('Finish the test!')

        # invite to input a to do list
          
        # Input "Buy peacock feathers"
        # Her hobby is to fish
          
        # After input enter, page refreshed
        # To-do list show "1:Buy peacock feathers"
          
        # page show another input filed could be type
        # She input "Use peacock feathers to make a fly"
          
        # Page refresh again and to-do list show both two items
          
        # She want to know if this websit will remember this list
          
        # She see the websit generate her own URL and some words to explain this for her
          
        # She visit this URL and find her to-list is still there
          
        # She feel good about this and go to sleep.    
if __name__ == '__main__':
    unittest.main(warnings='ignore')  
