from soium.webdriver.appium.webdriver import WebDriver

a = WebDriver('Safari')
d = a.remote(udid='iPad Pro', host='10.102.16.74')
d.get('https://www.baidu.com')
d.execute_script('window.stop();')
d.quit()

