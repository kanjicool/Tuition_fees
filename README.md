# สำรวจและเปรียบเทียบค่าเทอมสายคอม/AI จาก MyTCAS(68)

## สรุปขึ้นตอนการทำและจุดเด่น

### 1. การดึงข้อมูล
- ใช้ Python script (`tcas_fee_scraper.py`) ดึงข้อมูลหลักสูตรจากไฟล์ JSON ของ MyTCAS
- กรองเฉพาะสาขาที่เกี่ยวข้อง เช่น วิศวกรรมคอมพิวเตอร์, AI, ปัญญาประดิษฐ์ ฯลฯ
- ดึงข้อมูลสำคัญ เช่น มหาวิทยาลัย คณะ หลักสูตร วิทยาเขต ค่าเทอม

### 2. การจัดการข้อมูล
- ใช้ Jupyter Notebook (`cleaning_data.ipynb`) แปลงค่าเทอมให้อยู่ในรูป "ต่อภาคการศึกษา"
- ใช้ keywords เช่น "ตลอดหลักสูตร", "ต่อภาค", "เทอมแรก...เทอมต่อไป..." ในการหาค่าเทอมที่ถูกต้อง
- ไฮไลท์ข้อมูลที่ไม่สมบูรณ์ใน Excel ด้วยสีเหลือง

### 3. Dashboard
- สร้างด้วย Dash (Plotly) ในไฟล์ `university_tuition.py`
- ฟีเจอร์เด่น:
    - เลือกคณะและช่วงค่าเทอมที่สนใจ
    - ปุ่มดู Top 10 แพงสุด/ถูกสุด หรือดูทั้งหมด
    - สถิติสำคัญ: จำนวนหลักสูตร, ค่าเทอมเฉลี่ย, สูงสุด, ต่ำสุด, จำนวนมหาวิทยาลัย
    - กราฟเปรียบเทียบค่าเทอมแต่ละมหาวิทยาลัย
    - มีตารางสรุปข้อมูลหลักสูตร
- เหมาะกับนักเรียน/นักศึกษาใช้เปรียบเทียบและวางแผนเลือกมหาวิทยาลัยสายคอม/AI

---

# Tuition Fees Explorer for Computer/AI Programs from MyTCAS(68)

## Overview & Highlights

### 1. Data Collection
- Python script (`tcas_fee_scraper.py`) fetches course data from MyTCAS JSON
- Filters only relevant programs (e.g., Computer Engineering, AI, Artificial Intelligence)
- Extracts key fields: university, faculty, program, campus, tuition fee

### 2. Data Processing
- Jupyter Notebook (`cleaning_data.ipynb`) standardizes tuition to "per semester" for fair comparison
- Handles various text formats (total program, per semester, first/next semester, etc.)
- Highlights incomplete data in Excel (yellow)

### 3. Dashboard
- Built with Dash (Plotly) in `university_tuition.py`
- Features:
    - Faculty and tuition range selection
    - Quick buttons: Top 10 most expensive/cheapest or show all
    - Key stats: number of programs, average, max, min tuition, number of universities
    - Tuition comparison chart
    - Summary table of programs
- Perfect for students to compare and plan university choices in Computer/AI fields

---