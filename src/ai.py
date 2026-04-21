import os
from groq import Groq

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError("GROQ_API_KEY is not set. Please configure it in environment variables.")

client = Groq(api_key=API_KEY)


def fallback_report(inspection_text: str) -> str:
    """
    Used when AI fails or gives weak output.
    Keeps structure intact so pipeline does not break.
    """
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
    """
    Simple rule-based conflict detection.
    Helps AI explicitly mention contradictions.
    """
    insp = inspection_text.lower()
    therm = thermal_text.lower()

    # Basic example rule (can be extended later)
    if ("damp" in insp or "moisture" in insp) and ("dry" in therm or "no moisture" in therm):
        key_points += "\nConflict Detected: Inspection suggests moisture presence, but thermal data indicates dry conditions."

    return key_points


def _ensure_sections(report: str) -> str:
    """
    Ensures all required DDR sections exist.
    Prevents missing sections in final output.
    """
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
    """
    Main function to generate DDR using LLM.
    """

    # Limit input size to control token usage
    inspection_text = inspection_text[:2000]
    thermal_text = thermal_text[:1000]

    # Add conflict signals before sending to model
    key_points = _inject_conflict_signal(inspection_text, thermal_text, key_points)

    prompt = f"""
You are generating a Detailed Diagnostic Report (DDR) for a residential property.

Follow these rules strictly:
- Do not add information that is not present
- If something is missing, write "Not Available"
- If data conflicts, clearly mention "Conflict Detected"
- Keep language simple and client-friendly

Report Structure:

Executive Summary:
Brief overview of key findings.

Property Issue Summary:
List major issues identified.

Area-wise Observations:
Describe issues area-wise.
If image reference is possible, use:
"Refer Image: <image_name>"
Otherwise write: "Image Not Available"

Probable Root Cause:
Explain possible causes.

Severity Assessment:
Classify as Low / Medium / High with reasoning.

Recommended Actions:
Suggest corrective steps.

Additional Notes:
Any extra observations.

Missing or Unclear Information:
Explicitly mention unavailable data.

Input Data:

Key Observations:
{key_points}

Inspection Report:
{inspection_text}

Thermal Report:
{thermal_text}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        report = response.choices[0].message.content.strip()

        # Basic validation of output
        if not report or len(report) < 120:
            return fallback_report(inspection_text)

        return _ensure_sections(report)

    except Exception as e:
        print(f"AI generation failed: {e}")
        return fallback_report(inspection_text)