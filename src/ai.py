import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY is not set. Please configure it in environment variables.")


def call_llm(prompt: str) -> str:
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "meta-llama/llama-3-8b-instruct",

                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.2
            }
        )

        if response.status_code != 200:
            raise Exception(f"HTTP Error {response.status_code}: {response.text}")

        result = response.json()

        if "choices" not in result:
            raise Exception(f"LLM Error: {result}")

        return result["choices"][0]["message"]["content"].strip()

    except Exception as e:
        raise Exception(f"LLM Call Failed: {e}")


def fallback_report(inspection_text: str) -> str:
    return f"""
Detailed Diagnostic Report (DDR)

Executive Summary:
Limited processing due to system fallback.

Property Issue Summary:
Basic issues observed from available inspection data.

Area-wise Observations:
{inspection_text[:400]}

Probable Root Cause:
Not Available

Severity Assessment:
Medium (estimated due to incomplete data)

Recommended Actions:
Further inspection required for accurate assessment.

Additional Notes:
This report was generated using fallback logic due to AI failure.

Missing or Unclear Information:
Not Available
"""

def _inject_conflict_signal(inspection_text: str, thermal_text: str, key_points: str) -> str:
    insp = inspection_text.lower()
    therm = thermal_text.lower()

    if ("damp" in insp or "moisture" in insp) and ("dry" in therm or "no moisture" in therm):
        key_points += "\nConflict Detected: Inspection suggests moisture presence, but thermal data indicates dry conditions."

    return key_points


def _ensure_sections(report: str) -> str:
    required_sections = [
        "Executive Summary",
        "Property Issue Summary",
        "Area-wise Observations",
        "Probable Root Cause",
        "Severity Assessment",
        "Recommended Actions",
        "Additional Notes",
        "Missing or Unclear Information",
    ]

    for section in required_sections:
        if section not in report:
            report += f"\n\n{section}:\nNot Available"

    return report


def generate_ddr(inspection_text: str, thermal_text: str, key_points: str) -> str:

    # Limit size (important for token control)
    inspection_text = inspection_text[:2000]
    thermal_text = thermal_text[:1000]

    key_points = _inject_conflict_signal(inspection_text, thermal_text, key_points)

    prompt = f"""
You are generating a HIGH-QUALITY Detailed Diagnostic Report (DDR).

STRICT RULES:
- Do NOT invent facts
- If missing → write "Not Available"
- If conflict → clearly write "Conflict Detected"
- Keep language simple and client-friendly
- Avoid technical jargon

STRUCTURE (VERY IMPORTANT):

Executive Summary:
Clear 3–4 line overview.

Property Issue Summary:
Bullet points of key issues.

Area-wise Observations:
Group by area (Hall, Kitchen, Bathroom etc.)
Each must include:
- Issue
- Explanation
- "Refer Image: <image_name>" OR "Image Not Available"

Probable Root Cause:
Explain logically.

Severity Assessment:
Low / Medium / High + reason.

Recommended Actions:
Step-by-step fixes.

Additional Notes:
Extra insights.

Missing or Unclear Information:
Explicit missing data.

INPUT:

Key Observations:
{key_points}

Inspection Report:
{inspection_text}

Thermal Report:
{thermal_text}
"""

    try:
        print(" Calling OpenRouter API...")

        report = call_llm(prompt)

        print("AI Response Length:", len(report))

        if not report or len(report) < 150:
            print("⚠ Weak AI output → using fallback")
            return fallback_report(inspection_text)

        print("AI Report Generated Successfully")

        return _ensure_sections(report)

    except Exception as e:
        print(f"AI generation failed: {e}")
        return fallback_report(inspection_text)