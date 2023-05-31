import ntpath
import os
import glob
import shutil
 
 
imgpathin='D:\\works\\软件项目管理\\小程序v1\\VOCdevkit\\JPEG'
imgout='D:\\works\\软件项目管理\\小程序v1\\VOCdevkit\\JPEGlmages'
for subdir in os.listdir(imgpathin):
    print(subdir)
    file_path=os.path.join(imgpathin,subdir)
    for subdir1 in os.listdir(file_path):
        print(subdir1)
        file_path1=os.path.join(file_path,subdir1)
        for jpg_file in os.listdir(file_path1):
            src=os.path.join(file_path1,jpg_file)
            new_name=str(subdir+"_"+subdir1+"_"+jpg_file)
            dst=os.path.join(imgout,new_name)
            os.rename(src,dst)