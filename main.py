import streamlit as st
import os
from PIL import Image as im
import time as t
import shutil


def button(*args, **kwargs):
    global num
    num += 1
    return st.button(key=num, *args, **kwargs)


def download_button(*args, **kwargs):
    global num
    num += 1
    return st.download_button(key=num, *args, **kwargs)


def image_path(name):
    return f'资源文件\\{name}'


def path_back(path):
    count = 0
    for i in path[::-1]:
        count += 1
        if i == '/':
            break
    else:
        return None
    return path[:-count]


def add(addition):
    origin = st.session_state['path']
    if origin is None:
        return addition
    else:
        return '{}/{}'.format(origin, addition)


def set_session(name):
    if name not in st.session_state:
        st.session_state[name] = None


set_session('path')
set_session('rename')
set_session('delete')


num = 0
st.markdown('''<style>body {{background-color: {#f0f0f0};}}</style>''', unsafe_allow_html=True)
if st.session_state['rename'] is not None:
    tar = st.session_state['rename']
    files = os.listdir(path_back(tar))
    if button('返回'):
        st.session_state['rename'] = None
        st.experimental_rerun()
    st.title('重命名: {}'.format(add(tar)))
    c = st.columns((9, 1))
    with c[0]:
        new_name = st.text_input(label='名称', value=os.path.basename(tar))
    with c[1]:
        if new_name in files or len(new_name) == 0:
            st.image(image_path('error.ico'))
        else:
            st.image(image_path('fine.ico'))

    if button('确定'):
        back = path_back(tar)
        try:
            if back is not None:
                os.rename('{}/{}'.format(back, os.path.basename(tar)), '{}/{}'.format(back, new_name))
            else:
                os.rename(tar, new_name)
            st.success('重命名成功')
            st.session_state['rename'] = None
            st.experimental_rerun()
        except Exception as e:
            st.error(f'重命名失败:{e}')
            st.text('请使用上面的返回按钮返回')


elif st.session_state['delete'] is not None:
    tar = str(st.session_state['delete'])
    type = os.path.isdir(tar)
    if button('返回'):
        st.session_state['delete'] = None
        st.experimental_rerun()
    st.title('删除: {}'.format(add(tar)))
    if type:
        st.subheader('删除后连同文件夹中的文件都将无法恢复，确认删除？')
    else:
        st.subheader('删除后将无法恢复，确认删除？')
    if button('确定'):
        try:
            if type:
                shutil.rmtree(tar)
            else:
                os.remove(tar)
            st.success('删除成功')
            st.session_state['delete'] = None
            t.sleep(.5)
            st.experimental_rerun()
        except Exception as e:
            st.error(f'删除失败:{e}')
            st.text('请使用上面的返回按钮返回')



else:
    st.title('云盘')
    st.subheader('listing:  {}'.format(st.session_state['path']))
    upload_file = st.file_uploader('上传文件')
    path = st.session_state['path']
    if path is not None:
        if button('返回'):
            st.session_state['path'] = path_back(path)
            st.experimental_rerun()
    files = os.listdir(path)
    if button('新建文件夹'):
        if '新建文件夹' in files:
            i = 1
            while '新建文件夹 ({})'.format(i) in files:
                i += 1
            os.mkdir(add('新建文件夹 ({})'.format(i)))
        else:
            os.mkdir(add('新建文件夹'))
        st.experimental_rerun()
    if path is None:
        files.remove('main.py')
        files.remove('资源文件')
        files.remove('README.md')
    for i in files:
        if os.path.isdir(add(i)):
            c = st.columns([10, 55, 15, 10, 10])
            with c[0]:
                st.image('资源文件\\文件夹.png')
            with c[1]:
                st.code(i)
            with c[2]:
                if button('重命名'):
                    st.session_state['rename'] = add(i)
                    st.experimental_rerun()
            with c[3]:
                if button('打开'):
                    st.session_state['path'] = add(i)
                    st.experimental_rerun()
            with c[4]:
                if button('×'):
                    st.session_state['delete'] = add(i)
                    st.experimental_rerun()
    for i in files:
        if os.path.isfile(add(i)):
            c = st.columns([10, 55, 15, 10, 10])
            with c[0]:
                mat = i.split('.')[-1].lower()
                if mat in ('png', 'jpg', 'jpeg', 'bmp', 'gif'):
                    try:
                        th = im.open(add(i))
                        th.thumbnail((240, 240))
                        st.image(th)
                    except:
                        st.image(image_path('图片图标.png'))
                elif mat in ('mp4', 'avy', 'ts'):
                    try:
                        raise ValueError
                    except:
                        st.image(image_path('视频图标.png'))
                elif mat in ('mp3', 'wav', 'm4a'):
                    st.image(image_path('音乐图标.png'))
                elif mat in ('bat'):
                    pass
                elif mat in ('py', 'pyw'):
                    st.image(image_path('.py.pyw.ico'))
                elif mat in ('pyc'):
                    st.image(image_path('.pyc.ico'))
                else:
                    st.image(image_path('未知文件.ico'))


            with c[1]:
                st.code(i + '\n' + '{}  B'.format(os.path.getsize(add(i))))
            with c[2]:
                if button('重命名'):
                    st.session_state['rename'] = add(i)
                    st.experimental_rerun()
            with c[3]:
                download_button('下载', data=open(add(i), 'rb').read(), file_name=i)
            with c[4]:
                if button('×'):
                    st.session_state['delete'] = add(i)
                    st.experimental_rerun()


    if upload_file is not None:
        with open(add(upload_file.name), 'wb') as w:
            w.write(upload_file.getvalue())
