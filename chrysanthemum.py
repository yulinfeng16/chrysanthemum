import requests
import json
import time,base64
false=False
# 定义要发送的JSON数据
import base64

def send(img_data,male):

    # 3. 将二进制内容转换为Base64编码
    img_base64 = img_data
    if male=='1':
        # 4. 输出或使用Base64编码后的字符串
        data={
          "batch_size": 1,
          "cfg_scale": 7,
          "height": 512,
          "negative_prompt": "chest,short hair",
          "override_settings": {
            "sd_model_checkpoint": "2.5DMiaoKa_reality_v1.0.safetensors [74c2a5723b]",
            "sd_vae": ""
          },
          "clip_skip": 2,
          "prompt": "1little boy,red background,(crew cut no hair:1.2),sneasler,chinese new year,upper_body,(3D eastern golden dragon background:0.95),child,",
          "restore_faces": false,
          "sampler_index": "DPM++ SDE Karras",
          "sampler_name": "",
          "script_args": [
          ],
          "seed": -1,
          "steps": 28,
          "tiling": false,
          "width": 512,
          "alwayson_scripts": {
            "roop":
            {
            "args":[img_base64,"true",0,"F:\\sd-webui-aki-v4.3\\models\\roop\\inswapper_128.onnx","CodeFormer",1,None,1,'None',False,True]
            }
          }
        }
    else:
        # 4. 输出或使用Base64编码后的字符串
        data={
          "batch_size": 1,
          "cfg_scale": 7,
          "height": 512,
          "negative_prompt": "(mask:1.1),NSFW,lowres,racism,",
          "override_settings": {
            "sd_model_checkpoint": "2.5DMiaoKa_reality_v1.0.safetensors [74c2a5723b]",
            "sd_vae": ""
          },
          "clip_skip": 2,
          "prompt": "(1little girl:1.2),middle hair,(chinese new year:1.1),red background,3D eastern golden dragon background,child,black hair,(square face:1.1),thick lips,closed mouth,(upper_body:0.9),(red_neckwear:1.2),dragon_print,realistic,red hanfu,tang style outfits,<lora:hanfuTang_v32:0.7>,smile,blunt bangs,photo_(medium),look_at_viewer,",
          "restore_faces": false,
          "sampler_index": "DPM++ SDE Karras",
          "sampler_name": "",
          "script_args": [
          ],
          "seed": -1,
          "steps": 28,
          "tiling": false,
          "width": 512,
          "alwayson_scripts": {
            "roop":
            {
            "args":[img_base64,"true",0,"F:\\sd-webui-aki-v4.3\\models\\roop\\inswapper_128.onnx","CodeFormer",1,None,1,'None',False,True]
            }
          }
        }
    # 将数据转换为JSON格式
    json_data = json.dumps(data)

    # 发送POST请求
    response_post = requests.post('http://localhost:5001/txt2img', data=json_data)

    if response_post.status_code == 200 or response_post.status_code==201:
        # 解析返回的JSON数据并获取request_id
        response_json_post = response_post.json()
        request_id = response_json_post.get('request_id')
        
        if request_id:
            while True:
                # 发送GET请求查询进度
                response_get = requests.get(f'http://localhost:5001/progress/{request_id}')
                
                if response_get.status_code == 200:
                    # 解析返回的JSON数据
                    response_json_get = response_get.json()
                    print("Progress JSON:", response_json_get)
                    # 检查是否有imagedata项，并进行base64解码
                    imagedat = response_json_get.get('result')
                    imagedata = imagedat.get('images')
                    results=[]
                    if imagedata:
                      for i in range(0,len(imagedata)):
                        image_bytes = base64.b64decode(imagedata[i])
                        results.append(imagedata[i])
                        return results
                    # 根据实际情况决定是否继续轮询，这里假设当某个条件满足时（如：status字段为'completed'）结束轮询
                    
                    
                time.sleep(2)  # 每隔2秒查询一次
        else:
            print("Request ID not found in the POST response.")
    else:
        print(f"POST request failed with status code: {response_post.status_code}")

from flask import Flask, request, jsonify
from flask_cors import CORS
import base64

app = Flask(__name__)
CORS(app)  # 解决跨域问题


@app.route('/process_image', methods=['POST'])
def process_received_image():
    # 检查请求体中是否有'img_base64'字段
    if 'img_base64' not in request.json:
        return jsonify({"error": "Image data not found"}), 400

    # 将Base64编码的图片转换为二进制数据
    img_base64 = request.json['img_base64']
    mmm=request.json['ismale']

    # 调用send函数处理图片
    try:
        result = send(img_base64,mmm)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"result": result}), 200
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=18888, threaded=True)
