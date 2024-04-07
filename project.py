import streamlit as st
from deepface import DeepFace
from PIL import Image
import cv2
import numpy as np
import os
from numpy.linalg import norm
from streamlit_option_menu import option_menu

def register(face_pic,username):
    bytes_data = face_pic.getvalue()
    img_arr = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    user_face = len(DeepFace.extract_faces(img_arr,enforce_detection=False))
    if user_face > 1: return 0
    else: 
        cv2.imwrite(f'{username}.jpg',img_arr)
        return 1
def face_recog(face_need_to_verify):
    return DeepFace.extract_faces(face_need_to_verify,enforce_detection=True,grayscale=True)[0].get('face')
def face_verify(face_need_to_verify,folder):
    user_dict = load_images_from_folder(folder)
    cur_user = face_recog(face_need_to_verify)
    for x,y in user_dict.items():
        similarity = y@cur_user/(norm(y)*norm(cur_user))
        if similarity > 0.6: return round(similarity,2),x
    return 0,0
def load_images_from_folder(folder):
    image = {}
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            imgs = face_recog(img)
            username = os.path.splitext(filename)
            image[username[0]] = imgs
    return image
def happy(face_pic):
    emotion = DeepFace.analyze(face_pic,actions='emotion',enforce_detection=False)[0].get('dominant_emotion')
    if emotion == 'happy': 
        score = DeepFace.analyze(face_pic,actions='emotion',enforce_detection=False)[0].get('emotion').get('happy')*100000
        return round(score,1)
    return 0
def game(submit,camera):
    count = 0
    scores = []
    if submit == True:
        count = count + 1
        score = game_function(count,camera)
        scores.append(score)
    if count == 3: return max(scores)

def game_function(count,camera):
    if camera is not None:  
        bytes_data = camera.getvalue()
        img_arr = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        cv2.imwrite(f'cached_{count}.jpg',img_arr)
        score = happy(img_arr)
        st.success(f'Diem so cua ban la {score}')
        if count == 3: return score
        st.write(f'Ban con {3-count} lan nua')
        return score


folder = r'Final-Project---Face-recognition/pic'
os.chdir(folder)
with st.sidebar:
    selected = option_menu("Main Menu", ['Main Screen',"Home", 'Settings'], 
        icons=['house','fire', 'gear'], menu_icon="cast", default_index=1)
    selected
if selected == 'Main Screen':
    title_format = f'<p style="text-align: center; font-family: ' \
               f'Arial; color: #FFBF00; font-size: 100px; ' \
               f'font-weight: bold;">HAPPY APP</p>'

    st.markdown(title_format, unsafe_allow_html=True)
if selected == 'Home':
    tab1, tab2 = st.tabs(['Registration','Verification'])
    with tab1:
        username = st.text_input(label='Username',value=None)
        image = st.camera_input('Đăng kí')
        if image is not None:
            if username == None or username =='':
                st.error('Bạn chưa nhập username', icon="🚨")
            elif username != None or username !='':
                registered = register(image,username)
                if registered == 0: st.warning('Trong ảnh chỉ được có 1 người')
                else: st.success('Bạn đã đăng kí thành công')
    with tab2:
        if image is not None:
            cur_image = st.camera_input('Đăng nhập')
            if cur_image is not None:
                bytes_data = cur_image.getvalue()
                img_arr = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
                similarity,username = face_verify(img_arr,folder)
                if similarity == 0: st.warning('Xin hay dang ki')
                else:
                    st.success(f'{username}: {similarity}')
if selected == 'Settings':
    st.success('Xin hay cuoi')
    camera = st.camera_input('Cuoi')
    count = 0
    scores = []
    submit = st.button('Submit')
    while 1:
        if submit == True:
            count = count + 1
            score = game_function(count,camera)
            scores.append(score)
        if count == 3: 
            st.write(f'{max(scores)}')
            break
