import os
from groq import Groq


API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError("GROQ_API_KEY is not set. Please configure it in environment variables.")

client = Groq(api_key=API_KEY)



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

    
    inspection_text = inspection_text[:2000]
    thermal_text = thermal_text[:1000]

    key_points = _inject_conflict_signal(inspection_text, thermal_text, key_points)

    prompt = f"""
You are generating a Detailed Diagnostic Report (DDR) for a residential property.

STRICT RULES:
- Do NOT invent information
- If data is missing → write "Not Available"
- If data conflicts → clearly mention "Conflict Detected"
- Keep language simple and client-friendly

STRUCTURE:

Executive Summary:
Brief overview.

Property Issue Summary:
List key issues.

Area-wise Observations:
Group issues by area.
If image available:
"Refer Image: <image_name>"
Else:
"Image Not Available"

Probable Root Cause:
Explain causes.

Severity Assessment:
Low / Medium / High with reasoning.

Recommended Actions:
Suggest fixes.

Additional Notes:
Extra info.

Missing or Unclear Information:
Mention missing data.

INPUT DATA:

Key Observations:
{key_points}

Inspection Report:
{inspection_text}

Thermal Report:
{thermal_text}
"""

    try:
        print("Calling GROQ API...")

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        report = response.choices[0].message.content.strip()

        # Validate output
        if not report or len(report) < 120:
            print("⚠ Weak AI response → using fallback")
            return fallback_report(inspection_text)

        print(" AI Report Generated Successfully")
        return _ensure_sections(report)

    except Exception as e:
        print(f" AI generation failed: {e}")
        return fallback_report(inspection_text)