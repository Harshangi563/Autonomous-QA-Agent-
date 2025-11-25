🧠 Autonomous QA Agent:-
Automated Test Case Generation, Script Creation & Execution using AI (Gemini) + Selenium

📌 Overview:-
The Autonomous QA Agent automatically:
✔ Builds a Knowledge Base using uploaded support documents
✔ Generates precise test cases using AI
✔ Creates runnable Selenium automation scripts
✔ Executes the scripts and displays test results.

📁 Features:-
🔹 Upload support docs (specs, UI guidelines, HTML)
🔹 AI-powered test case generation (Markdown format)
🔹 AI-generated Selenium Python scripts
🔹 Test execution from Streamlit UI
🔹 Displays results with screenshot capture on failure

🧩Tech Stack:-

Streamlit, Flask, Google Gemini, ChromaDB, LangChain, Selenium, PyMuPDF, BeautifulSoup.

📦 Dependencies:-
All required libraries are listed in requirements.txt

🛠️ Setup & Installation :-
Clone the Repository and Create & Activate Virtual Environment by command:
python -m venv venv

#For windows run:-venv\Scripts\activate
#For macOS/Linus run:-source venv/bin/activate  

:-Install Requirements
pip install -r requirements.txt

:-Add API Key and create a .env file and add

GEMINI_API_KEY=your_gemini_key_here

Make sure your Python version is 3.9 – 3.11 (recommended: 3.10).

Running the Application
-Start Backend (Flask):-
python app.py

-Start Frontend (Streamlit):-
streamlit run ui.py
###Ensure you start Flask first.###

🚀 Usage Workflow:-
1️⃣	Upload support docs (PDF, MD, TXT, JSON) + checkout.html
2️⃣	Click Generate Test Cases
3️⃣	Copy a test case row → paste in text area
4️⃣	Click Generate Script
5️⃣	Click Run Selenium Test
6️⃣	View real-time output (PASS/FAIL)

📁 Support Document Roles:-

checkout.html:- UI elements, IDs, frontend behavior.
product_specs.md:- Pricing calculation & discount logic.
ui_ux_guide.txt	:-  UI validation, design & input rules.
api_endpoints.json:- API reference (optional for backened automation).

📸 Test Output Info
On success: "Test PASSED" message.
On failure: Screenshot saved as <Test_ID>_failure_screenshot.png.

##Example Test Case Format##
| Test_ID | Feature | Test_Scenario | Expected_Result | Grounded_In |
| TC-001 | Cart | Add 1x Product A | Total becomes $50. | product_specs.md |
