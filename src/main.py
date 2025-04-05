from ntpath import isfile
import os
import shutil

def copy_files(src:str, des:str):
    if not os.path.exists(src) or not os.path.exists(des):
        raise Exception("Not valid filepaths")
    shutil.rmtree(des)
    os.mkdir(des)
    copy_tree(src, des)

def copy_tree(src:str, des:str):
    if os.path.isfile(src):
        shutil.copy(src, des)
        return
    objects = os.listdir(src)
    for obj in objects:
        if os.path.isfile(obj):
            shutil.copy(obj, des)
        else:
            new_des = os.path.join(des, obj)
            os.mkdir(new_des)
            new_src = os.path.join(src,obj)
            copy_tree(new_src, new_des)

if __name__ == "__main__":
    copy_files("static", "public")


