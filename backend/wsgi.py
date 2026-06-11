import sys
import os

# 替换为你的 PythonAnywhere 用户名
path = '/home/shuhunb515/shu-blog/backend'
if path not in sys.path:
    sys.path.insert(0, path)

from app import app as application
