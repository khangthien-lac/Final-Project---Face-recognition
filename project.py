import streamlit as st
from deepface import DeepFace
import cv2
import numpy as np

def face_count(face_pic):
	bytes_data = face_pic.getvalue()
	img_arr = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
	facecount = len(DeepFace.extract_faces(img_arr))
	if facecount == 1: return 1
	return 0
def face_reg(face_pic):
	bytes_data = face_pic.getvalue()
	img_arr = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
	return DeepFace.extract_faces(img_arr)[0].get('face')
def face_verification(face,face_need_to_verify):
	for x,y in face.items():	
		Same_or_not = DeepFace.verify(y,face_need_to_verify,enforce_detection=False)[0].get('verified')
		date,time = time_log()
		if Same_or_not == True: 
			st.success('Bạn đã điểm danh thành công')
			return Same_or_not,x,date,time
		else: 
			st.warning('Xin hãy đăng kí')
def verified(image):
	count = face_count(image)
	return count,face_reg(image)	
def time_log():
	current_datetime = datetime.datetime.now()
	date_str = current_datetime.strftime("%Y-%m-%d")
	time_str = current_datetime.strftime("%H:%M:%S")
	return date_str,time_str
		
face = {}
st.title('Trang web điểm danh')
tab1, tab2, tab3 = st.tabs([ 'Registration','Verification','Time log'])

with tab1:
	username = st.text_input(label='Username',value=None)
	image = st.camera_input('Đăng kí')
	if username == None or username =='':
		st.error('Bạn chưa nhập username', icon="🚨")
	elif username != None or username !='':
		onlyOne, face_arr = verified(image)
		if onlyOne == 0: st.warning('Trong ảnh chỉ được có 1 người')
		else: 
			face[username] = face_arr
			st.success('Bạn đã đăng kí thành công')
with tab2:
	if face != []:
		cur_image = st.camera_input('Đăng nhập')
		face_verify = face_reg(cur_image)
		verify,cur_username,date,time = face_verification(face,face_verify)
with tab3:
	if face != []:
		st.write(cur_username,':',time,',',date)
