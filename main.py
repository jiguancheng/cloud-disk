import streamlit as st
import os
from PIL import Image as im
import time as t
import shutil


def download(path):
    try:
        return open(path, 'rb').read()
    except PermissionError:
        st.error('访问被拒')
        return None


def button(*args, **kwargs):
    global num
    num += 1
    return st.button(key=num, use_container_width=True, *args, **kwargs)


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
set_session('login')
set_session('multi_select')
set_session('input_secret')
set_session('update')

num = 0
if st.session_state['rename'] is not None:
    tar = st.session_state['rename']
    files = os.listdir(path_back(tar))
    if button('返回'):
        st.session_state['rename'] = None
        st.experimental_rerun()
    st.title('重命名: {}'.format(tar))
    c = st.columns((9, 1))
    with c[0]:
        new_name = st.text_input(label='名称', value=os.path.basename(tar))
        if new_name == 'private' and '/' not in tar:
            st.session_state['login'] = True
            st.session_state['rename'] = None
            st.experimental_rerun()
    with c[1]:
        if new_name in files or len(new_name) == 0:
            try:
                st.image(image_path('error.ico'))
            except:
                pass
                
        else:
            try:
                st.image(image_path('fine.ico'))
            except:
                pass

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
    st.title('删除: {}'.format(tar))
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


elif st.session_state['login'] is not None:
    if button('返回'):
        st.session_state['login'] = None
        st.experimental_rerun()
    secret = st.text_input(label='输入密码', type='password')
    if secret == st.secrets['sec']:
        st.session_state['path'] = 'private'
        st.session_state['login'] = None
        st.experimental_rerun()

elif st.session_state['multi_select'] is not None:
    path = st.session_state['multi_select']
    st.markdown('<div><h1 style="text-align:center">云盘</h1></div>', unsafe_allow_html=True)
    st.subheader(f'listing: {st.session_state["path"] if st.session_state["path"] is not None else "根目录"}')
    files = os.listdir(path)
    if '.hidden' in files:
        files.remove('.hidden')
        with open(add('.hidden'), 'r', encoding='utf-8') as f:
            for i in f.read().split('\n'):
                if i in files:
                    files.remove(i)
    c = st.columns((1, 1))
    with c[0]:
        if button('删除'):
            pass
    with c[1]:
        if button('下载'):
            pass
    if button('返回'):
        st.session_state['multi_select'] = None
        st.experimental_rerun()
    select = st.multiselect(label='请选择', options=files, max_selections=None, )

elif st.session_state['input_secret'] is not None:
    if button('返回'):
        st.session_state['input_secret'] = None
        st.experimental_rerun()
    secret = st.text_input(label='输入密码', type='password')
    if secret == st.secrets['sec']:
        if button('确认'):
            try:
                os.remove(add('.hidden'))
            except FileNotFoundError:
                pass
            st.session_state['input_secret'] = None
            st.experimental_rerun()

elif st.session_state['update']:
    st.title('上传成功')
    if button('确定'):
        st.session_state['update'] = False
        st.experimental_rerun()

else:
    st.markdown('<div><h1 style="text-align:center">云盘</h1></div>', unsafe_allow_html=True)
    st.subheader(f'listing: {st.session_state["path"] if st.session_state["path"] is not None else "根目录"}')
    upload_file = st.file_uploader('上传文件', accept_multiple_files=True)
    if len(upload_file) != 0:
        for i in upload_file:
            with st.spinner('上传中'):
                with open(add(i.name), 'wb') as w:
                    w.write(i.getvalue())
        st.session_state['update'] = True
        st.experimental_rerun()
    path = st.session_state['path']
    files = os.listdir(path)
    if path is not None:
        if button('返回'):
            st.session_state['path'] = path_back(path)
            st.experimental_rerun()
    else:
        if 'private' not in files:
            os.mkdir('private')
    if '.hidden' in files:
        files.remove('.hidden')
        with open(add('.hidden'), 'r', encoding='utf-8') as f:
            for i in f.read().split('\n'):
                if i in files:
                    files.remove(i)
    c = st.columns((25, 25, 25, 25))
    with c[0]:
        if button('新建文件夹'):
            if '新建文件夹' in files:
                i = 1
                while '新建文件夹 ({})'.format(i) in files:
                    i += 1
                os.mkdir(add('新建文件夹 ({})'.format(i)))
            else:
                os.mkdir(add('新建文件夹'))
            st.experimental_rerun()
    with c[1]:
        if button('多选'):
            st.session_state['multi_select'] = path
            st.experimental_rerun()
    with c[2]:
        if button('显示隐藏文件'):
            st.session_state['input_secret'] = True
            st.experimental_rerun()
    for i in files:
        if os.path.isdir(add(i)):
            c = st.columns([10, 62, 13, 10, 5])
            with c[0]:
                try:
                    st.image(image_path('文件夹.png'))
                except:
                    pass
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
            c = st.columns([10, 62, 13, 10, 5])
            try:
                with c[0]:
                    mat = i.split('.')[-1].lower()
                    if mat in ('png', 'jpg', 'jpeg', 'bmp', 'gif', 'ico'):
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
                        st.image(image_path('py.pyw.ico'))
                    elif mat in ('pyc'):
                        st.image(image_path('pyc.ico'))
                    else:
                        st.image(image_path('未知文件.ico'))
            except:
                pass

            with c[1]:
                st.code(i + '\n' + '{}  B'.format(os.path.getsize(add(i))))
            with c[2]:
                if button('重命名'):
                    st.session_state['rename'] = add(i)
                    st.experimental_rerun()
            with c[3]:
                try:
                    download_button('下载', data=open(add(i), 'rb').read(), file_name=i)
                except PermissionError:
                    st.text('访问被拒')
            with c[4]:
                if button('×'):
                    st.session_state['delete'] = add(i)
                    st.experimental_rerun()

# F:\\python\\Scripts\\streamlit run main.py
