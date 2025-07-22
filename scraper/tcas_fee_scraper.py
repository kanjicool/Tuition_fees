import requests
import pandas as pd
import re

# URL ที่ได้จากการ inspect (ไฟล์ JSON ใหญ่)
URL = "https://my-tcas.s3.ap-southeast-1.amazonaws.com/mytcas/courses.json"

# คำค้นที่ใช้กรองสาขาที่เกี่ยวข้อง
KEYWORDS = ["วิศวกรรมคอม", "AI", "ปัญญาประดิษฐ์", "Artificial Intelligence", "Computer Engineering"]

def fetch_data():
    print("กำลังดึงข้อมูลจาก TCAS...")
    response = requests.get(URL)
    response.raise_for_status()
    return response.json()

def is_relevant(program_name):
    return any(kw.lower() in program_name.lower() for kw in KEYWORDS)

def extract_fee(text):
    if not text:
        return None
    match = re.search(r"([\d,]+)\s*บาท", text)
    if match:
        return int(match.group(1).replace(",", ""))
    return None

def build_dataset(data):
    print("กำลังกรองเฉพาะสาขาคอมพิวเตอร์/AI...")
    filtered = []
    for entry in data:
        prog_name = entry.get("program_name_th", "")
        if is_relevant(prog_name):
            filtered.append({
                "university": entry.get("university_name_th", ""),
                "faculty": entry.get("faculty_name_th", ""),
                "program": prog_name,
                "campus": entry.get("campus_name_th", ""),
                "tuition_fee_text": entry.get("cost", ""),
                "tuition_fee_numeric": extract_fee(entry.get("cost", "")),
                "more_info_url": entry.get("cost", "").split()[-1] if "http" in entry.get("cost", "") else ""
            })
    return pd.DataFrame(filtered)

def main():
    data = fetch_data()
    df = build_dataset(data)

    print(f"พบทั้งหมด {len(df)} หลักสูตร")

    # บันทึกเป็น Excel
    df.to_excel("data/tuition_fees_comp_ai.xlsx", index=False)
    print("บันทึกเป็นไฟล์ Excel แล้ว")

if __name__ == "__main__":
    main()
