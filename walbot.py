from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time


class WalBot:

   def __init__(self, first_name, last_name, email, address, phone, credit_number,
               credit_month, credit_year, credit_ccv, username, password):
      self.first_name = first_name
      self.last_name = last_name
      self.email = email
      self.address = address
      self.phone = phone
      self.credit_number = credit_number
      self.credit_month = credit_month
      self.credit_year = credit_year
      self.credit_ccv = credit_ccv
      self.username = username
      self.password = password
      self.driver = webdriver.Chrome(ChromeDriverManager().install())
      self.driver.get('https://www.walmart.com/ip/Sony-PlayStation-5-Digital-Edition/493824815')

      # Main routines
      self.add_ps5_to_cart_and_checkout()
      self.filling_shipping_info()
      self.fill_out_payment_and_order()

   def add_ps5_to_cart_and_checkout(self):
      addToCart = '//*[@id="add-on-atc-container"]/div[1]/section/div[1]/div[3]/button/span/span'
      checkOut = ('//*[@id="cart-root-container-content-skip"]/div[1]/div/div[2]/div/div/div/div/'
                  'div[3]/div/div/div[2]/div/div[2]/div/button[1]')
      continueWithoutAccount = ('/html/body/div[1]/div/div[1]/div/div[1]/div[3]/div/div/div/div[1]'
                                 '/div/div/div/div/div[3]/div/div[1]/div/section/section/div/button/span')
      username = '//*[@id="sign-in-email"]'
      password = '/html/body/div[1]/div/div[1]/div/div[1]/div[3]/div/div/div/div[1]/div/div/div/div/div[3]/div/div[4]/div/section/div/section/form/div[2]/div/div[1]/label/div[2]/div/input'
      continueWithAccount = '/html/body/div[1]/div/div[1]/div/div[1]/div[3]/div/div/div/div[1]/div/div/div/div/div[3]/div/div[4]/div/section/div/section/form/div[5]/button/span'
      self.clickButton(addToCart)
      self.clickButton(checkOut)
      # self.clickButton(continueWithoutAccount)
      self.enterData(username, self.username)
      self.enterData(password, self.password)
      self.clickButton(continueWithAccount)

   def filling_shipping_info(self):
      # firstContinue = ('/html/body/div[1]/div/div[1]/div/div[1]/div[3]/div/div/div/div[2]/div/div[2]/'
      # 'div/div/div/div[3]/div/div/div[2]/button/span')
      firstContinue = '//button[@aria-label="Continue to Delivery Address"]'
      secondContinue = '//button[@aria-label="Continue to Payment Options"]'
      firstName = '//*[@id="firstName"]'
      lastName = '//*[@id="lastName"]'
      email = '//*[@id="email"]'
      address = '//*[@id="addressLineOne"]'
      phone = '//*[@id="phone"]'
      confirmInfo = ('/html/body/div[1]/div/div[1]/div/div[1]/div[3]/div/div/div/div[3]/div[1]/div[2]/'
                     'div/div/div/div[3]/div/div/div/div/div/form/div[2]/div[2]/button/span')
      self.clickButton(firstContinue)
      self.clickButton(secondContinue)
      # self.enterData(firstName, self.first_name)
      # self.enterData(lastName, self.last_name)
      # self.enterData(phone, self.phone)
      # self.enterData(email, self.email)
      # self.enterData(address, self.address)
      # self.clickButton(confirmInfo)

   def fill_out_payment_and_order(self):  # FILLS OUT PAYMENT
      creditCardNum = '//*[@id="creditCard"]'
      creditExpireMonth = '//*[@id="month-chooser"]'
      creditExpireYear = '//*[@id="year-chooser"]'
      creditCVV = '//*[@id="cvv"]'
      creditCVVConfirm = '//*[@id="cvv-confirm"]'
      reviewOrder = ('/html/body/div[1]/div/div[1]/div/div[1]/div[3]/div/div/div/div[4]/div[1]/div[2]/div/div'
                     '/div/div[3]/div[2]/div/div/div/div[2]/div/div/div/form/div[3]/div/button/span/span/span')
      review = '//button[@aria-label="Review Your Order"]'
      placeOrder = '//button[@aria-label="Place Order"]'
      # self.enterData(creditCardNum, self.credit_number)
      # self.enterData(creditExpireMonth, self.credit_month)
      # self.enterData(creditExpireYear, self.credit_year)
      # self.enterData(creditCVV, self.credit_ccv)
      self.enterData(creditCVVConfirm, self.credit_ccv)
      self.clickButton(review)
      # self.clickButton(placeOrder)

   def clickButton(self, xpath):
      try:
         self.driver.find_element_by_xpath(xpath).click()
      except Exception:
         time.sleep(0.5)
         self.clickButton(xpath)

   def enterData(self, field, data):
      try:
         self.driver.find_element_by_xpath(field).send_keys(data)
         pass
      except Exception:
         time.sleep(0.5)
         self.enterData(field, data)
