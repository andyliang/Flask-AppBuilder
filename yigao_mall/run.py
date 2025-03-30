from app import app

#############################################
# 初始化日志相关参数
#############################################
# 获取当前main.py文件所在服务器的绝对路径
import os
import logging.handlers
program_path = os.path.split(os.path.realpath(__file__))[0]
# 如果日志目录log文件夹不存在，则创建日志目录
if not os.path.exists('log'):
    os.mkdir('log')
# 初始化日志目录路径
log_path = os.path.join(program_path, 'log')
filename = "%s/yigao_mall.log" % log_path

# 实例化handler及日志格式、级别
file_handler = logging.handlers.RotatingFileHandler(filename, maxBytes=5*1024*1024, backupCount=5, encoding='UTF-8')
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
file_handler.setFormatter(formatter)
file_handler.setLevel(level=logging.INFO)

# consol_haddler = logging.StreamHandler()  #日志输出到屏幕控制台
# 定义日志输出格式与路径
# logging.basicConfig(filemode='a',filename=filename)
# logging.getLogger('').setLevel(logging.INFO)
logging.getLogger('').addHandler(file_handler)

# 原开发者模式
app.run(host="0.0.0.0", port=8866, debug=True)

# 生产模式
'''
from gevent import pywsgi
server = pywsgi.WSGIServer(('0.0.0.0', 80), app)
print("Serving http on port 80")
server.serve_forever()
'''

# 生产模式2
'''
from wsgiref.simple_server import make_server
httpd = make_server("0.0.0.0", 80, app)
print("Serving http on port 80")
httpd.serve_forever()
'''