import streamlit as st
import requests
import os

# =====================================
# 🚫 Prevent image preview in Streamlit
# =====================================
st.image = lambda *args, **kwargs: None  # Disable image preview

# -------------------------------
# 🚀 Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Autonomous QA Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# 🎨 Global Styling
# -------------------------------
st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f3f8ff, #f6fff9) !important;
        color: #333 !important;
        font-family: 'Poppins', sans-serif;
    }

    [data-testid="stHeader"], [data-testid="viewerToolbar"] {
        background: transparent !important;
    }

    h1, h2 {
        color: #4ca1af !important;
        font-weight: 600 !important;
    }

    /* 💥 Fully centered & elongated buttons */
    div.stButton {
        text-align: center !important;
        display: block !important;
        width: 100% !important;
    }
    div.stButton > button:first-child {
        display: inline-block !important;
        min-width: 360px !important;
        padding: 16px 40px !important;
        background: linear-gradient(135deg, #6bc5d2, #4ca1af) !important;
        color: white !important;
        border-radius: 12px !important;
        font-size: 17px !important;
        font-weight: 600 !important;
        border: none !important;
        box-shadow: 0 6px 14px rgba(76, 161, 175, 0.35) !important;
        transition: 0.3s ease !important;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 24px rgba(76, 161, 175, 0.55) !important;
    }

    /* 📁 File uploader styling with blue tone */
    [data-testid="stFileUploader"] > div:first-child {
        border: 2px dashed #6bc5d2 !important;
        background-color: #ebfaff !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }
    [data-testid="stFileUploader"] button {
        background: linear-gradient(135deg, #4ca1af, #6bc5d2) !important;
        color: white !important;
        font-weight: 600 !important;
        border-radius: 6px !important;
        padding: 6px 14px !important;
    }

    /* Inputs */
    input, textarea {
        background-color: white !important;
        color: black !important;
        border: 1px solid #cfd9e3 !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# 🧠 Title
# -------------------------------
st.markdown("<h1 style='text-align:center;'>🧠 Autonomous QA Agent</h1>", unsafe_allow_html=True)
st.write("")

# Init session
if "run_path" not in st.session_state:
    st.session_state.run_path = None

# -------------------------------
# 📕 Build Knowledge Base
# -------------------------------
st.markdown("## 📕 Build Knowledge Base")
col1, col2 = st.columns(2)
docs = col1.file_uploader("Upload Support Documents", type=["pdf", "md", "txt", "json"], accept_multiple_files=True)
html = col2.file_uploader("Upload checkout.html", type=["html"])

if st.button("📚 Build Knowledge Base"):
    if docs and html:
        with st.spinner("🚀 Building Knowledge Base..."):
            try:
                files = [("files", (d.name, d.read(), "application/octet-stream")) for d in docs]
                files.append(("html", (html.name, html.read(), "text/html")))
                res = requests.post("http://127.0.0.1:5000/upload_files", files=files).json()
                st.success(f"✔ {res.get('message', 'Knowledge Base built successfully')}")
            except Exception as e:
                st.error(f"❌ Backend Error: {e}")
    else:
        st.warning("⚠ Please upload both documents and checkout.html")

# -------------------------------
# 🧪 Test Case Generation
# -------------------------------
st.markdown("## 🧪 Test Case Generation")
query = st.text_input("Enter query for test case generation")
if st.button("🚀 Generate Test Cases"):
    if query.strip():
        try:
            res = requests.post("http://127.0.0.1:5000/generate_test_cases", json={"query": query}).json()
            st.code(res.get("test_cases_markdown", ""), language="markdown")
        except Exception as e:
            st.error(f"❌ Backend Error: {e}")
    else:
        st.warning("⚠ Please enter a query")

# -------------------------------
# 🛠 Selenium Script Generator
# -------------------------------
st.markdown("## 🛠 Selenium Script Generator")
test_case_md = st.text_area("Paste ONE Markdown test case row")

if st.button("🛠 Generate Script"):
    if test_case_md.strip():
        try:
            res = requests.post("http://127.0.0.1:5000/generate_script", json={"test_case_row": test_case_md}).json()
            st.code(res.get("script", ""), language="python")
            st.session_state.run_path = "generated_scripts/selenium_test.py"
            st.success("📁 Script generated and saved!")
        except Exception as e:
            st.error(f"❌ Backend Error: {e}")
    else:
        st.warning("⚠ Please provide a test case")

# -------------------------------
# ▶ Run Test
# -------------------------------
st.markdown("## 📄 Test Execution Output")
if st.session_state.run_path:
    if st.button("▶ Run Selenium Test"):
        with st.spinner("🔄 Running test..."):
            result = os.popen('venv\\Scripts\\python "generated_scripts/selenium_test.py"').read()

        if "Test FAILED" not in result and ("PASSED" in result or "Test PASSED" in result):
            st.success("✔ Test Passed Successfully!")
        else:
            st.error("❌ Test Failed!")

        st.write("")
        st.code(result, language="text")
else:
    st.info("💡 Generate a script to enable test execution")
