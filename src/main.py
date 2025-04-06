import os
import shutil
import sys

from converter import markdown_to_html_node
from parser import extract_title

def clean_dir(des:str):
    if not os.path.exists(des):
        os.mkdir(des)
        return
    shutil.rmtree(des)
    os.mkdir(des)

def copy_static_files(src:str, des:str):
    if not os.path.exists(src) or not os.path.exists(des):
        raise Exception("Not valid filepaths")
    if os.path.isfile(src):
        shutil.copy(src, des)
        return
    objects = os.listdir(src)
    for obj in objects:
        path = os.path.join(src, obj)
        if os.path.isfile(path):
            print(f"copying file {obj} to {des}")
            shutil.copy(path, des)
        else:
            new_des = os.path.join(des, obj)
            os.mkdir(new_des)
            new_src = os.path.join(src,obj)
            copy_static_files(new_src, new_des)

def generate_pages(src_content:str, template:str, dest:str, basepath:str|None):
    if not os.path.exists(src_content) or not os.path.exists(dest) or not os.path.exists(template):
        raise Exception("Not valid filepaths")
    objects = os.listdir(src_content)
    for obj in objects:
        path = os.path.join(src_content, obj)
        if os.path.isfile(path):
            generate_page(path, template, dest,basepath)
        else:
            new_des = os.path.join(dest, obj)
            os.mkdir(new_des)
            new_src = os.path.join(src_content,obj)
            generate_pages(new_src, template, new_des,basepath)

def generate_page(src:str, template:str, des:str, basepath:str|None):
    if not os.path.exists(src) or not os.path.exists(des) or not os.path.exists(template):
        raise Exception("Not valid filepaths")
    if not os.path.isfile(src):
        return
    print(f"Generating page from {src} to {des} using {template}")
    with open(src, "r") as f:
        markdown = f.read()
    with open(template, "r") as f:
        template = f.read()
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    res = template.replace("{{ Title }}", title)
    res = res.replace("{{ Content }}", html)
    if basepath is not None:
        res = res.replace('href="/', f'href="{basepath}"')
        res = res.replace('src="/', f'src="{basepath}"')
    src_filename = os.path.basename(src).split(".")[0]
    res_path = os.path.join(des, src_filename+".html")
    with open(res_path, "w") as f:
        _ = f.write(res)
    return


if __name__ == "__main__":
    args = sys.argv
    basepath = None
    if len(args) > 1:
        basepath = args[1]
    clean_dir("docs")
    copy_static_files("static", "docs")
    generate_pages("content", "template.html", "docs", basepath)


