#_*_ coding:utf-8 _*_
"""
 @author: LaiJinHan
 @time：2019/9/16 23:02
"""
import os
print(os.path.dirname(__file__))#返回当前文件的上一级地址
images_path=os.path.dirname(__file__)
if not os.path.exists(images_path):
    os.mkdir(images_path)
else:
    print('images文件夹存在')