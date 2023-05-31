import unittest
from appium import webdriver
import time
import requests
import json


class TestCrowdControl(unittest.TestCase):
    user_favorites = ['place1', 'place2', 'place3']
    places_data = {
        'place1': {'image_path': '/path/to/place1/image.jpg'},
        'place2': {'image_path': '/path/to/place2/image.jpg'},
        'place3': {'image_path': '/path/to/place3/image.jpg'}
    }

    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '8.0'
        desired_caps['deviceName'] = 'your_device_name'
        desired_caps['appPackage'] = 'your_app_package'
        desired_caps['appActivity'] = 'your_app_activity'
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def test_recommend_least_crowded_place(self):
        least_crowded_place = None
        least_crowded_place_crowd_data = float('inf')
        for place in self.user_favorites:
            self.driver.find_element_by_accessibility_id(place).click()
            time.sleep(2)
            image_path = self.places_data[place]['image_path']
            self.driver.find_element_by_id("camera_button").click()
            self.driver.find_element_by_id("photo_button").click()
            self.driver.find_element_by_id("image_view").click()
            self.driver.find_element_by_id("image_view").send_keys(image_path)
            time.sleep(2)
            self.driver.find_element_by_id("upload_button").click()
            time.sleep(30)

            api_url = 'your_yolov5_api_url'
            image_url = 'your_your_wechat_image_url'
            response = requests.post(api_url, data={'image_url': image_url})
            crowd_data = response.json()['crowd_data']
            if crowd_data < least_crowded_place_crowd_data:
                least_crowded_place = place
                least_crowded_place_crowd_data = crowd_data

        data = {
            "touser": "",
            "template_id": "your_template_id",
            "page": "",
            "form_id": "",
            "data": {
                "keyword1": {
                    "value": least_crowded_place
                },
                "keyword2": {
                    "value": str(least_crowded_place_crowd_data)
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

