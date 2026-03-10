import streamlit as st
import google.generativeai as genai
st.set_page_config(page_title="حكايات الصغار الذكية", page_icon="🌙")
st.markdown("<h1 style='text-align: center; color: #4A90E2;'>🌙 مؤلف قصص الأطفال</h1>", unsafe_allow_html=True)
st.write("اكتب فكرة بسيطة وسأقوم بتحويلها إلى قصة تربوية ممتعة!")
 with st.sidebar:
st.header("⚙️ الإعدادات")
api_key = st.text_input("أدخل مفتاح Gemini API الخاص بك", type="password")
st.info("قم بلصق مفتاحك هنا")
 if api_key:
 try:
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')
 else:
st.warning("⚠️ يرجى إدخال مفتاح الـ API في القائمة الجانبية.")

