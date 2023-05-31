import unittest
from appium import webdriver
import time
import requests
import json

class TestCrowdControl(unittest.TestCase):

    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '8.0'
        desired_caps['deviceName'] = 'your_device_name'
        desired_caps['appPackage'] = 'your_app_package'
        desired_caps['appActivity'] = 'your_app_activity'
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def test_recommend_crowd_in_favorites(self):
        self.driver.find_element_by_id("favorites_tab").click()
        time.sleep(2)

        fav_list = self.driver.find_element_by_id("favorite_list")
        favorite_places = []
        for item in fav_list.find_elements_by_class_name("list_item"):
            favorite_places.append(item.find_element_by_class_name("item_name").text)

        total_crowd = 0
        for place in favorite_places:
            self.driver.find_element_by_accessibility_id(place).click()
            time.sleep(2)
            crowd_list = self.driver.find_element_by_id("crowd_list")
            crowd_data = []
            for item in crowd_list.find_elements_by_class_name("list_item"):
                crowd_data.append(int(item.find_element_by_class_name("item_value").text))
            total_crowd += sum(crowd_data) / len(crowd_data)
            self.driver.find_element_by_id("back_button").click()
            time.sleep(2)
        avg_crowd = total_crowd / len(favorite_places)

        data = {
            "touser": "",
            "template_id": "your_template_id",
            "page": "",
            "form_id": "",
            "data": {
                "keyword1": {
                    "value": favorite_places[0]
                },
                "keyword2": {
                    "value": str(avg_crowd)
                }
            }
        }
        access_token = "your_access_token"
        mock_request = mock.Mock(return_value={'access_token': access_token})
        requests.get = mock_request

        send_msg_result = requests.post("https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send",
                                        params={'access_token': access_token},
                                        data=json.dumps(data))

        self.assertEqual(send_msg_result.status_code, 200, "发送模板消息失败")

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()



