
from selenium import webdriver
import time
 
def delete_email():
    browser = webdriver.Firefox()
    browser.get('https://mail.163.com/')
    browser.set_window_size(1500, 900)
    time.sleep(2)
 
    # 定位 iframe
    fm = browser.find_element_by_xpath('//div[@id="loginDiv"]/iframe')
    # 切换 iframe
    browser.switch_to.frame(fm)
 
    # 输入账号密码 点登陆
    browser.find_element_by_name('email').send_keys('17354422606@163.com') # 账号
    browser.find_element_by_name('password').send_keys('xing3239') # 密码
    try:
        browser.find_element_by_id('dologin').click()
    except Exception as e:
        print('有验证码: ', e)
    finally:
        time.sleep(3)
        # 点击收件箱
        browser.find_element_by_id('_mail_component_57_57').click()
        time.sleep(2)
        try:
            time.sleep(1)
            # 选括号
            browser.find_element_by_xpath("//span[@class='nui-chk-symbol']/b").click()
            # 点删除
            browser.find_element_by_xpath('//span[contains(text(),"删 除")]').click()
        except Exception as e:
            print('已经删除 ',e)
 
# 要删除的页数  一次100条
delete_email()


