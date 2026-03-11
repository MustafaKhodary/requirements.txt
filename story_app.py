"""
story_app.py — حكايات الصغار الذكية
────────────────────────────────────
Arabic children's story generator using Gemini API.

Usage:
    streamlit run story_app.py
"""
import streamlit as st
import google.generativeai as genai

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="حكايات الصغار الذكية", page_icon="🌙", layout="centered")

# ─── Session State ───────────────────────────────────────────────────────────
# Keep the generated story across re-runs so it doesn't vanish on widget interaction
if "story" not in st.session_state:
    st.session_state.story = ""
if "story_topic" not in st.session_state:
    st.session_state.story_topic = ""

# ─── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Tajawal', sans-serif;
    direction: rtl;
}

.main-title {
    text-align: center;
    font-size: 2.2rem;
    font-weight: 700;
    margin-bottom: 0.2rem;
}

.sub-title {
    text-align: center;
    color: #888;
    font-size: 1rem;
    margin-bottom: 1.5rem;
}

.story-box {
    background: #1e1e2e;
    border: 1px solid #3a3a5c;
    border-radius: 12px;
    padding: 1.5rem;
    line-height: 2;
    font-size: 1.15rem;
    color: #e0e0e0;
    direction: rtl;
    text-align: right;
    white-space: pre-wrap;
}
</style>
""", unsafe_allow_html=True)

# ─── Header ─────────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">🌙 مؤلف قصص الأطفال</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">اكتب فكرتك وخلّ الذكاء الاصطناعي يؤلف لك قصة ممتعة</div>', unsafe_allow_html=True)

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ الإعدادات")
    api_key = st.text_input("🔑 مفتاح Gemini API", type="password",
                            help="احصل على مفتاح من https://aistudio.google.com/app/apikey")
    st.info("بعد لصق المفتاح، اضغط Enter")
    st.markdown("---")
    st.markdown("**💡 أمثلة لأفكار:**")
    st.markdown("- قصة عن حب الأطفال لآبائهم")
    st.markdown("- قصة عن أهمية الصدق")
    st.markdown("- قصة عن طفل يحلم أن يصبح طبيباً")
    st.markdown("- قصة عن صداقة بين قطة وعصفور")

# ─── Main Input ──────────────────────────────────────────────────────────────
user_input = st.text_area("✏️ عن ماذا تريد قصة اليوم؟",
                          placeholder="مثلاً: قصة عن حب الأطفال لآبائهم",
                          height=100)

generate_btn = st.button("✨ تأليف القصة الآن", use_container_width=True, type="primary")

# ─── Generation Logic ────────────────────────────────────────────────────────
if generate_btn:
    # Validate inputs
    if not api_key or not api_key.strip():
        st.error("⚠️ من فضلك ضع مفتاح الـ API أولاً في الشريط الجانبي!")
    elif not user_input or not user_input.strip():
        st.warning("⚠️ اكتب فكرة للقصة أولاً!")
    else:
        try:
            genai.configure(api_key=api_key.strip())

            # Use a current, working model name.
            # gemini-pro is DEPRECATED and will fail — use gemini-2.0-flash instead.
            model = genai.GenerativeModel("gemini-2.0-flash")

            prompt = (
                "أنت كاتب قصص أطفال محترف باللغة العربية الفصحى البسيطة. "
                "اكتب قصة تربوية ممتعة للأطفال (عمر 4-10 سنوات) عن الموضوع التالي:\n\n"
                f"{user_input.strip()}\n\n"
                "القصة يجب أن تكون:\n"
                "- مكتوبة بالعربية الفصحى السهلة\n"
                "- تحتوي على شخصيات محببة\n"
                "- فيها درس أو قيمة تربوية\n"
                "- طولها مناسب (حوالي 300-500 كلمة)\n"
                "- لا تستخدم عناوين أو ترقيم، فقط سرد قصصي سلس\n"
            )

            with st.spinner("📝 جاري تأليف القصة..."):
                response = model.generate_content(prompt)

                # Safely extract text — handle blocked / empty responses
                story_text = ""
                if response and response.parts:
                    story_text = response.text
                elif response and response.prompt_feedback:
                    # The prompt might have been blocked by safety filters
                    st.error("⚠️ تم حظر الطلب من فلاتر الأمان. جرب صياغة مختلفة.")
                    st.stop()

                if not story_text or not story_text.strip():
                    st.error("⚠️ لم يتم توليد قصة. جرب مرة أخرى أو غيّر الفكرة.")
                    st.stop()

                # Save to session state so it persists
                st.session_state.story = story_text.strip()
                st.session_state.story_topic = user_input.strip()
                st.success("✅ تمت القصة بنجاح!")

        except genai.types.BlockedPromptException:
            st.error("⚠️ تم حظر الطلب بسبب فلاتر الأمان. جرب صياغة مختلفة.")
        except Exception as e:
            error_msg = str(e).lower()
            if "api_key" in error_msg or "api key" in error_msg or "401" in error_msg:
                st.error("⚠️ مفتاح الـ API غير صحيح. تأكد من المفتاح وحاول مرة أخرى.")
            elif "404" in error_msg or "not found" in error_msg:
                st.error("⚠️ الموديل غير موجود. تأكد من اتصالك بالإنترنت وحاول مرة أخرى.")
            elif "429" in error_msg or "quota" in error_msg or "rate" in error_msg:
                st.error("⚠️ تم تجاوز حد الاستخدام. انتظر قليلاً وحاول مرة أخرى.")
            elif "timeout" in error_msg or "deadline" in error_msg:
                st.error("⚠️ انتهت مهلة الاتصال. تأكد من الإنترنت وحاول مرة أخرى.")
            else:
                st.error(f"⚠️ حدث خطأ: {e}")

# ─── Display the story (persists across re-runs) ────────────────────────────
if st.session_state.story:
    st.markdown("---")
    if st.session_state.story_topic:
        st.markdown(f"**📖 قصة عن:** {st.session_state.story_topic}")

    st.markdown(
        f'<div class="story-box">{st.session_state.story}</div>',
        unsafe_allow_html=True
    )

    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="📥 تحميل القصة",
            data=st.session_state.story,
            file_name="قصة.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with col2:
        if st.button("🗑️ مسح القصة", use_container_width=True):
            st.session_state.story = ""
            st.session_state.story_topic = ""
            st.rerun()
