from dotenv import load_dotenv
import os
import google.generativeai as genai
from agent.rag_engine import RAGEngine

# Load credentials
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_test_case(query, rag: RAGEngine):
    """
    Generate precise, scoped test cases in Markdown format.

    Enhancements:
    - Prevents UI + Logic duplication.
    - Only generates the primary scenario relevant to query.
    - Avoids similar test case pairs (e.g., 'Display' and 'Logic' for same action).
    """

    # Retrieve contextual knowledge
    context_response = rag.retrieve(query)
    docs = context_response.get("documents", [])
    context_text = "\n".join(
        str(item)
        for sub in docs
        for item in (sub if isinstance(sub, list) else [sub])
    ) if docs else ""

    prompt = f"""
You are a senior QA automation engineer.

🔎 USER QUERY: "{query}"
Generate test cases ONLY related to this query.

📄 CONTEXT:
{context_text}

🎯 OUTPUT FORMAT (ONLY VALID MARKDOWN TABLE):
| Test_ID | Feature | Test_Scenario | Expected_Result | Grounded_In |

🚫 STRICT RULES:
- NO duplicates (do NOT output both UI + Logic for same scenario unless explicitly asked)
- Do NOT generate a pair like:
    | Add Product A | Display Row... |
    | Add Product A | Total updates... |
  Instead pick the MOST RELEVANT to the query.
- If query = “cart”, prefer functional logic unless user explicitly mentions UI.
- NO JSON, NO comments, NO blank lines, NO code fencing (```).
- Only one correct grounding source per test case.

📌 Grounding Logic:
- Pricing / discount / total → product_specs.md
- UI appearance / styling / placement → checkout.html
- Validation (required fields, character rules) → ui_ux_guide.txt

🎯 IMPORTANT:
Since your query is: **"{query}"**
✔ If query contains “cart”, focus on correct cart logic (pricing first).
✔ Only generate UI test cases if user explicitly requests UI/cart appearance.
✔ Avoid API unless “API” is mentioned in query.

📌 Correct Example for `"cart"` query:
| Test_ID | Feature | Test_Scenario | Expected_Result | Grounded_In |
| TC-001 | Cart Calculation | Add 1x Product A | Total becomes $50. | product_specs.md |
| TC-002 | Cart Calculation | Add 1x Product B | Total becomes $30. | product_specs.md |

🚨 Final Output: ONLY the Markdown table. Nothing else.
"""

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)

    return {"test_cases_markdown": response.text.strip()}
