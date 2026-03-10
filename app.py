import streamlit as st
import google.generativeai as genai
st.set_page_config(page_title="حكايات الصغار الذكية", page_icon="🌙")
st.markdown("<h1 style='text-align: center;'>🌙 مؤلف قصص الأطفال</h1>", unsafe_allow_html=True)
with st.sidebar:
  st.header("⚙️ الإعدادات")
  api_key = st.text_input("أدخل مفتاح Gemini API", type="password")
  st.info("بعد لصق المفتاح، اضغط Enter")
  user_input = st.text_area("عن ماذا تريد قصة اليوم؟", placeholder="مثلاً: قصة عن حب الأطفال لآبائهم")
  if st.button("تأليف القصة الآن ✨"):
    if not api_key:
      st.error("⚠️ من فضلك ضع مفتاح الـ API أولاً!")
    elif not user_input:
      st.warning("⚠️ اكتب فكرة للقصة أولاً")
    else:
      try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        with st.spinner("جاري تأليف القصة..."):
          response = model.generate_content(f"اكتب قصة تربوية ممتعة للأطفال عن: {user_input} باللغة العربية")
          st.success("تمت القصة بنجاح!")
          st.markdown("---")
          st.write(response.text)
      except Exception as e:
        st.error(f"حدث خطأ في الاتصال: {e}")
