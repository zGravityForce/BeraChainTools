import requests

# 设置socks5代理地址和认证信息
# 格式为 socks5://用户名:密码@代理服务器IP:端口
proxy = 'socks5://Sj83dW:txuTWd@45.80.229.120:8000'

# 配置requests使用socks5代理
proxies = {
    'http': proxy,
    'https': proxy,
}
# ip:45.80.229.120
# port:8000
# username:Sj83dW
# password:txuTWd


# 发起请求到 httpbin.org/ip，所有请求都将通过配置的socks5代理进行
try:
    response = requests.get('https://httpbin.org/ip', proxies=proxies)
    print(f'Success: Your IP is {response.json()}')
except requests.exceptions.RequestException as e:
    print(f'Request failed: {e}')


# 创建Session对象
session = requests.Session()

# # 配置Session使用socks5代理
# proxies = {
#     'http': proxy,
#     'https': proxy,
# }

# 为Session对象配置代理
session.proxies.update(proxies)

# 使用配置好的Session对象发起请求
try:
    response = session.get('https://httpbin.org/ip')
    print(f'Success: {response.json()}')
except requests.exceptions.RequestException as e:
    print(f'Request failed: {e}')