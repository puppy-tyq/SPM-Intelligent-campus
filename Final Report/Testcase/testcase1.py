import unittest
from appium import webdriver
import time
import requests
import json


class TestCrowdControl(unittest.TestCase):
    test_image_path = '/path/to/test/image.jpg'
    actual_number_of_people = 5

    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '8.0'
        desired_caps['deviceName'] = 'your_device_name'
        desired_caps['appPackage'] = 'your_app_package'
        desired_caps['appActivity'] = 'your_app_activity'
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def test_detect_people_on_cloudy_day(self):
        self.driver.find_element_by_id("camera_button").click()
        self.driver.find_element_by_id("photo_button").click()
        self.driver.find_element_by_id("image_view").click()
        self.driver.find_element_by_id("image_view").send_keys(self.test_image_path)
        time.sleep(2)
        self.driver.find_element_by_id("upload_button").click()
        time.sleep(30)

        api_url = 'your_yolov5_api_url'
        image_url = 'your_your_wechat_image_url'
        response = requests.post(api_url, data={'image_url': image_url})
        result = response.json()
        detected_people = result['crowd_data']

        error_rate = abs(self.actual_number_of_people - detected_people) / self.actual_number_of_people

        data = {
            "touser": "",
            "template_id": "your_template_id",
            "page": "",
            "form_id": "",
            "data": {
                "keyword1": {
                    "value": str(detected_people)
                },
                "keyword2": {
                    "value": str(error_rate)
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
