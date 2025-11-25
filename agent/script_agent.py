# agent/script_agent.py
import os
import json
import tempfile
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def parse_markdown_row(markdown_row):
    parts = [cell.strip() for cell in markdown_row.strip().split("|") if cell.strip()]
    if len(parts) != 5:
        raise ValueError("Invalid markdown format. Expected 5 columns.")
    return {
        "Test_ID": parts[0],
        "Feature": parts[1],
        "Test_Scenario": parts[2],
        "Expected_Result": parts[3],
        "Grounded_In": parts[4]
    }

def generate_selenium_script(markdown_test_case_row, rag):
    try:
        test_case = parse_markdown_row(markdown_test_case_row)
    except Exception as e:
        raise ValueError(f"Invalid test case format! {e}")

    response = rag.retrieve("FILE: checkout.html")
    docs = response.get("documents", [])

    html_content = None
    for doc in docs:
        doc_str = "\n".join(doc) if isinstance(doc, list) else str(doc)
        if "<!DOCTYPE html>" in doc_str or "<html" in doc_str:
            html_content = doc_str
            break

    if not html_content:
        raise ValueError("❌ checkout.html was not found in Knowledge Base!")

    temp_html = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".html", encoding="utf-8")
    temp_html.write(html_content)
    temp_html.close()
    safe_html_path = temp_html.name.replace("\\", "/")

    prompt = f"""
You are an expert Selenium Python automation engineer.

Generate a 100% runnable Selenium script for:
{json.dumps(test_case, indent=2)}

🔹 Use ONLY these exact IDs from checkout.html:
    - addA
    - addB
    - addC
    - discountCode
    - discountMsg
    - cartSummary
    - total
    - payBtn
    - name, email, address

❌ NEVER use or create IDs like:
    'add-product-A', 'remove-product', 'apply-discount-btn', etc.

📍 Load local HTML:
driver.get("file:///{safe_html_path}")

🧠 Strict Script Rules:
- Output ONLY Python (no markdown or ```).
- Must begin with:
    from selenium import webdriver
- Use Chrome flags:
    --headless=new, --disable-gpu, --disable-dev-shm-usage, --no-sandbox
- Use WebDriverWait for interactions.
- Use try/except/finally.
- If test involves cart/discount → click addA first.

🎨 UI Validation:
- Do NOT perform CSS or color checks.
- Do NOT use value_of_css_property.
- Only verify text is present or element is displayed.

📸 On failure:
driver.save_screenshot("{test_case['Test_ID']}_failure_screenshot.png")
print("[ERROR] <Error Message>")

✔ On success:
print("[PASSED] {test_case['Test_ID']} - Test Passed")

📌 End with:
driver.quit()

⚠ Output ONLY the Python code. No explanations.
"""

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)

    script = response.text.strip().replace("```", "").replace("python", "").strip()

    os.makedirs("generated_scripts", exist_ok=True)
    file_path = "generated_scripts/selenium_test.py"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(script)

    return {"script": script, "file_path": file_path}
