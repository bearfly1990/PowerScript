from selenium import webdriver
brower = webdriver.Firefox()
brower.get('http://localhost:8000')
assert 'Django' in brower.title