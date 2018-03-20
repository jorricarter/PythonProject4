from unittest import TestCase, main
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class MyTestCase(TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.get('http://127.0.0.1:5000')
        self.browser.implicitly_wait(300)

        self.addCleanup(self.browser.quit)

    # tests if page loads and the title is "Meme Finder"
    def test_page_title(self):
        self.assertIn('Meme Finder', self.browser.title)    # your title here

    # tests if you click links at the footer, it will redirect properly
    def test_links(self):
        self.browser.find_element_by_id("memebox_link").click()
        self.assertIn('memebox', self.browser.current_url)

        self.browser.find_element_by_id("about_link").click()
        self.assertIn('about', self.browser.current_url)

        self.browser.find_element_by_id("main_link").click()
        self.assertEqual('Get meme!', self.browser.find_element_by_xpath("//form[1]/input[2]").get_attribute('value'))

    # tests search function
    def test_search(self):
        # search 'cat'
        keyword_box = self.browser.find_element_by_name('keyword')
        self.browser.implicitly_wait(200)
        keyword_box.send_keys('cat')
        keyword_box.send_keys(Keys.RETURN)
        self.browser.implicitly_wait(200)

        # verify 'CAT' is in the keyword display
        self.assertEqual('CAT', self.browser.find_element_by_css_selector('#memes > h1:nth-child(1)').text)

    # search cat meme, add all 3 memes to MemeBox, and test if those memes are found in MemeBox
    def test_add_to_memebox(self):
        wait = WebDriverWait(self.browser, 10)
        # search cat
        keyword_box = self.browser.find_element_by_name('keyword')
        keyword_box.send_keys('cat')
        keyword_box.send_keys(Keys.RETURN)

        # click giphy/imgur/reddit "I like this meme!" button to add to MemeBox
        giphy_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#giphy\ button')))
        giphy_button.click()
        self.browser.implicitly_wait(200)
        self.browser.switch_to.alert.accept()
        imgur_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#imgur\ button')))
        imgur_button.click()
        self.browser.implicitly_wait(200)
        self.browser.switch_to.alert.accept()
        reddit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#reddit\ button')))
        reddit_button.click()
        self.browser.implicitly_wait(200)
        self.browser.switch_to.alert.accept()
        self.browser.implicitly_wait(200)

        # save the title for the memes as variable values
        giphy_title = self.browser.find_element_by_xpath('/html/body/div/table/tbody/tr[3]/td[1]').text
        imgur_title = self.browser.find_element_by_xpath('/html/body/div/table/tbody/tr[3]/td[2]').text
        reddit_title = self.browser.find_element_by_xpath('/html/body/div/table/tbody/tr[3]/td[3]').text

        # go to MemeBox using the footer link
        self.browser.find_element_by_id("memebox_link").click()
        self.assertIn('memebox', self.browser.current_url)
        self.browser.implicitly_wait(200)

        # verify that meme titles just added are in MemeBox
        self.assertIn(giphy_title, self.browser.find_element_by_xpath('/html/body/div/form/table/tbody/tr[5]/td').text)
        self.assertIn(imgur_title, self.browser.find_element_by_xpath('/html/body/div/form/table/tbody/tr[3]/td').text)
        self.assertIn(reddit_title, self.browser.find_element_by_xpath('/html/body/div/form/table/tbody/tr[1]/td').text)

    #TODO: only works half the time
    def test_delete_meme(self):
        # search cat
        wait = WebDriverWait(self.browser, 10)
        keyword_box = self.browser.find_element_by_name('keyword')
        keyword_box.send_keys('cat')
        keyword_box.send_keys(Keys.RETURN)

        # click giphy "I like this meme!" button to add to MemeBox
        giphy_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#giphy\ button')))
        giphy_button.click()
        self.browser.implicitly_wait(100)
        self.browser.switch_to.alert.accept()

        # save the giphy meme title
        giphy_title = self.browser.find_element_by_xpath('/html/body/div/table/tbody/tr[3]/td[1]').text
        print(giphy_title)

        # go to MemeBox using the footer link
        self.browser.find_element_by_id("memebox_link").click()
        self.assertIn('memebox', self.browser.current_url)
        self.browser.implicitly_wait(300)

        # verify that meme titles just added are in MemeBox
        self.assertIn(giphy_title, self.browser.find_element_by_xpath('/html/body/div/form/table/tbody/tr[1]/td').text)

        self.browser.implicitly_wait(300)
        delete_button = wait.until(EC.element_to_be_clickable((By.NAME, '0')))
        delete_button.click()
        self.browser.implicitly_wait(500)
        self.browser.switch_to.alert.accept()
        self.browser.implicitly_wait(500)
        self.assertNotIn(giphy_title, self.browser.find_element_by_xpath('/html/body/div/form/table/tbody/tr[1]/td').text)


if __name__ == '__main__':
    main(verbosity=2)