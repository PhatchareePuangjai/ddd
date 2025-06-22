"""
Domain-Driven Design (DDD) Analyzer

This script analyzes a Thai language requirements document and extracts DDD components
using a simulated LLM (Language Learning Model).

How to run:
-----------
From the command line, run:
    python src/main.py <path_to_requirements_file>

Examples:
---------
    python src/main.py data/requirements/requirement_01.txt

The output will be saved in the 'outputs' folder with a filename based on the input file.
"""

import json
import os
import time
import argparse
import sys


def read_text_file(file_path: str) -> str:
    """
    อ่านเนื้อหาจากไฟล์ text ที่ระบุ

    Args:
        file_path (str): เส้นทางไปยังไฟล์

    Returns:
        str: เนื้อหาภายในไฟล์ หรือ None หากเกิดข้อผิดพลาด
    """
    print(f"[INFO] กำลังอ่านไฟล์จาก: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"[ERROR] ไม่พบไฟล์ที่ระบุ: {file_path}")
        return None
    except Exception as e:
        print(f"[ERROR] ไม่สามารถอ่านไฟล์ได้: {e}")
        return None


def analyze_with_llm_mock(requirement_text: str) -> dict:
    """
    *** ฟังก์ชันจำลอง (Mock Function) ***
    ฟังก์ชันนี้จำลองการส่งข้อความไปให้ LLM วิเคราะห์และรอรับผลลัพธ์
    ในอนาคต ควรนำเข้าจาก module ที่พัฒนาใน Jupyter Notebook
    
    ดูการพัฒนาและทดสอบเพิ่มเติมได้ที่:
    notebooks/llm_model_development.ipynb
    """
    print("[INFO] กำลังส่งข้อมูลเพื่อวิเคราะห์ด้วย LLM (จำลอง)...")
    # จำลองดีเลย์ เหมือนกำลังรอผลจาก LLM
    for i in range(3):
        time.sleep(0.5)
        print("...")

    print("[INFO] ได้รับผลลัพธ์จาก LLM (จำลอง) เรียบร้อยแล้ว")

    # --- ผลลัพธ์ตัวอย่างที่ Hardcode ไว้ ---
    # ในการใช้งานจริง ผลลัพธ์นี้จะมาจาก LLM โดยตรง
    mock_response = {
        "boundedContext": "การสั่งซื้อและการจัดส่ง (Ordering & Shipping)",
        "aggregates": [
            {
                "root": "Order",
                "description": "เป็นศูนย์กลางของกระบวนการสั่งซื้อสินค้าทั้งหมด",
                "entities": ["OrderItem"],
                "properties": [
                    {"name": "orderId", "type": "String"},
                    {"name": "customerId", "type": "String"},
                    {"name": "shippingAddress", "type": "Address"},
                    {"name": "totalPrice", "type": "Decimal"},
                ],
            }
        ],
        "entities": [
            {
                "name": "Customer",
                "properties": [
                    {"name": "customerId", "type": "String"},
                    {"name": "customerType", "type": "String", "enum": ["ทั่วไป", "VIP"]},
                ],
            }
        ],
        "businessRules": [
            {
                "ruleId": "SHIP-001",
                "description": "คำนวณค่าจัดส่งสำหรับลูกค้าทั่วไปที่ยอดซื้อไม่ถึง 500 บาท",
                "condition": "customer.customerType == 'ทั่วไป' AND order.totalPrice < 500",
                "action": "order.shippingFee = 40",
            },
            {
                "ruleId": "DISC-001",
                "description": "ให้ส่วนลด 10% และส่งฟรีสำหรับลูกค้า VIP",
                "condition": "customer.customerType == 'VIP'",
                "action": "order.discount = order.totalPrice * 0.10; order.shippingFee = 0",
            },
        ],
    }
    return mock_response


def save_output_to_json(data: dict, input_path: str, output_dir: str = "outputs"):
    """
    บันทึกข้อมูล dictionary ลงในไฟล์ JSON ในโฟลเดอร์ outputs

    Args:
        data (dict): ข้อมูลที่ต้องการบันทึก
        input_path (str): เส้นทางของไฟล์ input เพื่อใช้สร้างชื่อไฟล์ output
        output_dir (str): ไดเรกทอรีที่ต้องการบันทึกไฟล์ (ค่าเริ่มต้นคือ 'outputs')
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"[INFO] สร้างไดเรกทอรีใหม่: {output_dir}")

    base_name = os.path.basename(input_path)
    file_name_without_ext = os.path.splitext(base_name)[0]
    output_filename = f"output_{file_name_without_ext}.json"
    output_path = os.path.join(output_dir, output_filename)

    print(f"[INFO] กำลังบันทึกผลลัพธ์ไปที่: {output_path}")
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"[SUCCESS] บันทึกไฟล์ '{output_filename}' เรียบร้อย!")
    except Exception as e:
        print(f"[ERROR] ไม่สามารถบันทึกไฟล์ JSON ได้: {e}")


def main():
    """
    ฟังก์ชันหลักสำหรับรันโปรแกรมผ่าน Command Line
    """
    parser = argparse.ArgumentParser(
        description="วิเคราะห์เอกสาร Requirement ภาษาไทยเพื่อสกัดองค์ประกอบ DDD โดยใช้ LLM (เวอร์ชันจำลอง)"
    )
    parser.add_argument(
        "input_file",
        type=str,
        help="เส้นทาง (path) ไปยังไฟล์ requirement.txt ที่ต้องการวิเคราะห์",
    )
    args = parser.parse_args()

    # 1. อ่านไฟล์ Input
    requirement_content = read_text_file(args.input_file)

    if requirement_content:
        # 2. วิเคราะห์ด้วย LLM (เวอร์ชันจำลอง)
        ddd_model = analyze_with_llm_mock(requirement_content)

        # 3. บันทึกผลลัพธ์
        if ddd_model:
            save_output_to_json(ddd_model, args.input_file)


if __name__ == "__main__":
    main()
