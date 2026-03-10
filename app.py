import streamlit as st
import google.generativeai as genai
st.set_page_config(page_title="حكايات الصغار الذكية", page_icon="🌙")
st.markdown("<h1 style='text-align: center;'>🌙 مؤلف قصص الأطفال</h1>", unsafe_allow_html=True)
with st.sidebar:
  st.header("⚙️ الإعدادات")
api_key = st.text_input("أدخل مفتاح Gemini API", type="password")
st.info("بعد لصق المفتاح، اضغط Enter")
user_input = st.text_area("عن ماذا تريد قصة اليوم؟", placeholder="مثلاً: مغامرة في أعماق البحار...")
if st.button("تأليف القصة الآن ✨"):
  if not api_key:
st.error("⚠️ من فضلك ضع مفتاح الـ API في القائمة الجانبية أولاً!")
elif not user_input:
st.warning("⚠️ اكتب فكرة للقصة أولاً")
else:
try:
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')
with st.spinner("جاري تأليف قصة جميلة..."):
response = model.generate_content(f"اكتب قصة تربوية للأطفال عن: {user_input}")
st.success("تمت القصة!")
st.markdown("---")
st.write(response.text)
except Exception as e:
st.error(f"حدث خطأ، تأكد من صحة المفتاح: {e}")
