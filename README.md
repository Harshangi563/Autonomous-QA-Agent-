# 🧠 Autonomous QA Agent  
Automated test case generation, script creation & execution using AI (Gemini) + Selenium

## 📌 Overview
The Autonomous QA Agent automatically:
- Builds a Knowledge Base using uploaded support documents  
- Generates precise test cases using AI  
- Creates runnable Selenium automation scripts  
- Executes the scripts and displays test results  

## 📁 Features
- Upload support docs (specs, UI guidelines, HTML)  
- AI-powered test case generation (Markdown format)  
- AI-generated Selenium Python scripts  
- Run Selenium tests directly from Streamlit UI  
- Failure screenshot capture  

## 🧩 Tech Stack
Streamlit, Flask, Google Gemini, ChromaDB, LangChain, Selenium, PyMuPDF, BeautifulSoup

## 📦 Dependencies
All requirements are available in `requirements.txt`.

## 🛠 Setup & Installation
1. **Clone repository**
2. **Create & activate virtual environment**
   - Windows:  
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - Mac/Linux:  
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```
3. **Install packages**
   ```bash
   pip install -r requirements.txt

4. **Add API Key by Creating a .env file and add:**

GEMINI_API_KEY=your_gemini_key_here


👉 Recommended Python version: 3.10 (Supported: 3.9 – 3.11)

🚀 Running the Application

Start backend (Flask):
   ```bash
python app.py
  ```

Start frontend (Streamlit):
   ```bash
streamlit run ui.py
  ```

⚠ Run Flask first before starting Streamlit.

🔁 Usage Workflow

1️⃣ Upload support docs (PDF, MD, TXT, JSON) and checkout.html
2️⃣ Click Generate Test Cases
3️⃣ Copy a Markdown test case row and paste into input area
4️⃣ Click Generate Script
5️⃣ Click Run Selenium Test
6️⃣ View execution result (PASS/FAIL)

## 📂 Support Document Roles

| File              | Purpose                                      |
|------------------|----------------------------------------------|
| checkout.html     | UI elements, IDs, frontend behavior          |
| product_specs.md  | Pricing logic & discounts                    |
| ui_ux_guide.txt   | UI validation, design & input rules          |
| api_endpoints.json| API reference (optional for backend automation) |

📸 Test Output Information

✔ Pass: "Test PASSED"
❌ Fail: Screenshot saved as Test_ID_failure_screenshot.png

## 📊 Example Test Case Format

| Test_ID | Feature              | Test_Scenario                            | Expected_Result                         | Grounded_In        |
|---------|----------------------|-------------------------------------------|-----------------------------------------|-------------------|
| TC-001 | Payment Button UI     | Verify “Pay Now” button color             | Button appears green as per UI standard | checkout.html     |

