import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import cv2
import torch
import base64

import sys
sys.path.append(os.path.dirname( os.path.abspath(__file__) ) + "\\yolov5")
print(sys.path)

from yolov5.models.experimental import attempt_load
from yolov5.utils.general import non_max_suppression, scale_boxes
from yolov5.utils.torch_utils import select_device

app = Flask(__name__)
CORS(app)

device = select_device('')

# 加载模型
model = attempt_load('yolov5s.pt', device=device)
model.to(device).eval()

# 场所和图片映射
place_image_map = {
    '图书馆': 'library.jpg',
    '操场': 'playground.jpg',
    '食堂': 'canteen.jpg'
}

# 获取实时人数和画好bounding box的图片
def get_realtime_info(place):
    image_path = os.path.join('images', place_image_map[place])
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_tensor = torch.from_numpy(image.transpose(2, 0, 1)).float().div(255.0).unsqueeze(0).to(device)
    pred = model(image_tensor)[0]
    pred = non_max_suppression(pred, conf_thres=0.5, iou_thres=0.5, classes=None, agnostic=False, max_det=1000)
    bboxes = []
    for i, det in enumerate(pred):
        if det is not None and len(det):
            det[:, :4] = scale_boxes(image_tensor.shape[2:], det[:, :4], image.shape).round()
            for *xyxy, conf, cls in reversed(det):
                label = f"{cls.item():.0f}"
                bboxes.append(xyxy)
                cv2.rectangle(image, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (0, 255, 0), 2)
                cv2.putText(image, label, (int(xyxy[0]), int(xyxy[1] - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    realtime_num = len(bboxes)
    _, img_encoded = cv2.imencode('.jpg', image)
    img_base64 = str(base64.b64encode(img_encoded))[2:-1]
    return {'realtime_num': realtime_num, 'realtime_image': f"data:image/jpeg;base64,{img_base64}"}

# API接口
@app.route('/get_realtime_info', methods=['POST'])
def get_realtime_info_api():
    place = request.json['place']
    return jsonify(get_realtime_info(place))

if __name__ == '__main__':
    app.run(debug=True)
