# ระบบจัดการคำสั่งซื้อและค่าจัดส่ง (Order & Shipping Management System)

เอกสารนี้จัดทำขึ้นเพื่ออธิบาย Domain Model ของระบบจัดการคำสั่งซื้อและค่าจัดส่ง โดยใช้หลักการของ Domain-Driven Design (DDD) เพื่อให้ทุกคนในทีม ทั้งฝั่ง Business และ Development เข้าใจภาพรวม, โครงสร้างข้อมูล, และกฎทางธุรกิจตรงกัน

---

## 1. ภาพรวมของโมเดล (Domain Model Overview)

เพื่อความเข้าใจที่ง่ายขึ้น เราได้แปลงโมเดลทางเทคนิคออกมาเป็นแผนภาพ 3 ส่วนหลัก ดังนี้

### 1.1. แผนที่ขอบเขตของระบบ (Bounded Context Map)

แผนภาพนี้แสดงขอบเขตความรับผิดชอบหลักของระบบ ซึ่งในที่นี้คือ **"การสั่งซื้อและการจัดส่ง (Ordering & Shipping)"** ทำหน้าที่เป็นศูนย์กลางในการจัดการกระบวนการทั้งหมดที่เกี่ยวกับการสั่งซื้อของลูกค้า

- อธิบายอะไร: `boundedContext`
- เหมาะกับใคร: ผู้บริหาร, Project Manager, สถาปนิกซอฟต์แวร์ (Architect)
- ทำไมถึงดี: เป็นภาพที่ high-level ที่สุด แสดงให้เห็นว่าระบบของเรามี "ขอบเขตความรับผิดชอบ" อะไรบ้าง และมันเชื่อมต่อหรือสัมพันธ์กับระบบอื่น (ขอบเขตอื่น) อย่างไร ในกรณีของคุณ เรามีแค่ Context เดียวคือ "การสั่งซื้อและการจัดส่ง (Ordering & Shipping)" แต่ในระบบใหญ่ๆ อาจมี "การจัดการสินค้าคงคลัง (Inventory)" หรือ "การจัดการลูกค้า (CRM)" แยกออกมา ซึ่งแผนภาพนี้จะแสดงให้เห็นว่ามันคุยกันท่าไหน

### 1.2. แผนภาพโครงสร้างข้อมูล (Data Structure Diagram)

แผนภาพนี้แสดงโครงสร้างของข้อมูลทั้งหมดว่ามีอะไรบ้าง (`Customer`, `Product`, `Order`) และมีความสัมพันธ์กันอย่างไร โดยหัวใจหลักคือ **Order Aggregate** (กรอบเส้นประ) ซึ่งแสดงให้เห็นว่า `Order`, `OrderItem`, และ `ShippingAddress` เป็นกลุ่มก้อนที่ต้องจัดการไปพร้อมกันเสมอ

- อธิบายอะไร: `aggregates`, `entities`, `valueObjects` และความสัมพันธ์
- เหมาะกับใคร: ทุกคนในทีม (Business Analyst, Developer, QA, PM)
- ทำไมถึงดี: นี่คือแผนภาพที่ ทรงพลังที่สุด ในการแปลง JSON ของคุณให้เห็นภาพ มันแสดง "โครงสร้าง" ของข้อมูลว่ามีอะไรบ้าง (Order, Customer) และมันเชื่อมโยงกันอย่างไร (Customer หนึ่งคนมีได้หลาย Order)

เทคนิคสำคัญในการวาดเพื่อสื่อสารเรื่อง Aggregate:
ให้วาด "เส้นขอบ" หรือ " tô màu" รอบๆ Aggregate Root (Order) และ Entity/Value Object ที่อยู่ภายใต้มัน (OrderItem, ShippingAddress) เพื่อแสดงให้เห็นว่าทั้งหมดนี้คือ "กลุ่มก้อน" เดียวกันที่ต้องจัดการไปด้วยกันเสมอ

วิธีสร้างจาก JSON ของคุณ:

1.  ดึง Entities/Aggregates ออกมาเป็นกล่อง: สร้างกล่องสำหรับ Order, Customer, Product
2.  ดึง Value Objects ออกมาเป็นกล่อง: สร้างกล่องสำหรับ OrderItem, Address
3.  ใส่ Properties ที่สำคัญ: ไม่ต้องใส่ทั้งหมด เอาแค่ที่จำเป็นต่อการสนทนา
4.  ลากเส้นความสัมพันธ์:

        Customer --< Order (ลูกค้า 1 คน มีได้หลาย Order)

        Order ◆-- OrderItem (Order 1 ใบ ประกอบด้วย Item หลายชิ้น)

        Order --> Address (Order 1 ใบ มีที่อยู่จัดส่ง 1 ที่)

5.  วาดเส้นประรอบ Aggregate: ล้อมกรอบ Order, OrderItem, และ Address เพื่อแสดงว่านี่คือ Aggregate "Order"

### 1.3. ผังการทำงานของกฎทางธุรกิจ (Business Logic Flow)

แผนภาพนี้แสดงขั้นตอนและเงื่อนไขการทำงานของกฎทางธุรกิจที่สำคัญ เช่น การคำนวณส่วนลดและค่าจัดส่งตามประเภทของลูกค้าและยอดสั่งซื้อ

- อธิบายอะไร: businessRules
- เหมาะกับใคร: ทุกคนในทีม โดยเฉพาะฝั่ง Business และ QA
- ทำไมถึงดี: JSON บอกแค่ว่ามี "กฎ" อะไรบ้าง แต่ไม่ได้บอกว่ากฎนั้นถูกนำมาใช้ "เมื่อไหร่" และ "อย่างไร" Flowchart จะแสดงให้เห็นขั้นตอนการตัดสินใจ (Decision Logic) ได้ชัดเจนที่สุด

---

## 2. ตารางสรุปกฎทางธุรกิจ (Business Rules Summary)

ตารางนี้สรุปกฎและเงื่อนไขทางธุรกิจทั้งหมดของระบบเพื่อให้ง่ายต่อการอ้างอิงและตรวจสอบ

| Rule ID     | คำอธิบาย                               | เงื่อนไข / Trigger                      | การกระทำ (Action)                                                |
| :---------- | :------------------------------------- | :-------------------------------------- | :--------------------------------------------------------------- |
| `SHIP-001`  | คำนวณค่าส่งลูกค้าทั่วไป                | ลูกค้า `ทั่วไป` AND ยอดซื้อ `< 500`     | กำหนด `shippingFee = 40`                                         |
| `SHIP-002`  | ยกเว้นค่าส่งลูกค้าทั่วไป               | ลูกค้า `ทั่วไป` AND ยอดซื้อ `>= 500`    | กำหนด `shippingFee = 0`                                          |
| `DISC-001`  | ส่วนลดสำหรับลูกค้า VIP                 | ลูกค้าเป็น `VIP`                        | คำนวณ `discount = rawTotalPrice * 0.10`                          |
| `SHIP-003`  | ยกเว้นค่าส่งลูกค้า VIP                 | ลูกค้าเป็น `VIP`                        | กำหนด `shippingFee = 0`                                          |
| `STOCK-001` | ตรวจสอบสต็อกสินค้าก่อนยืนยันคำสั่งซื้อ | `ก่อนยืนยันคำสั่งซื้อ` (Before Confirm) | ตรวจสอบสต็อกสินค้าทุกรายการ หากไม่พอให้แจ้งเตือนและหยุดดำเนินการ |

---

## 3. โมเดลข้อมูลฉบับเต็ม (Technical JSON Model)

นี่คือโมเดลข้อมูลทางเทคนิคฉบับสมบูรณ์ในรูปแบบ JSON ซึ่งใช้เป็น Source of Truth สำหรับทีมพัฒนา

<details>
<summary><strong>คลิกเพื่อดู JSON Model ฉบับเต็ม</strong></summary>

```json
{
  "boundedContext": "การสั่งซื้อและการจัดส่ง (Ordering & Shipping)",
  "aggregates": [
    {
      "root": "Order",
      "description": "เป็นศูนย์กลางของกระบวนการสั่งซื้อทั้งหมด",
      "entities": ["OrderItem"],
      "properties": [
        {
          "name": "orderId",
          "type": "String"
        },
        {
          "name": "customerId",
          "type": "String"
        },
        {
          "name": "orderItems",
          "type": "List<OrderItem>"
        },
        {
          "name": "shippingAddress",
          "type": "Address"
        },
        {
          "name": "rawTotalPrice",
          "type": "Decimal"
        },
        {
          "name": "discount",
          "type": "Decimal"
        },
        {
          "name": "netTotalPrice",
          "type": "Decimal"
        },
        {
          "name": "shippingFee",
          "type": "Decimal"
        },
        {
          "name": "orderStatus",
          "type": "String"
        }
      ]
    }
  ],
  "entities": [
    {
      "name": "Customer",
      "properties": [
        {
          "name": "customerId",
          "type": "String"
        },
        {
          "name": "name",
          "type": "String"
        },
        {
          "name": "customerType",
          "type": "String",
          "enum": ["ทั่วไป", "VIP"]
        }
      ]
    },
    {
      "name": "Product",
      "properties": [
        {
          "name": "productId",
          "type": "String"
        },
        {
          "name": "name",
          "type": "String"
        },
        {
          "name": "stockQuantity",
          "type": "Integer"
        }
      ]
    }
  ],
  "valueObjects": [
    {
      "name": "OrderItem",
      "properties": [
        {
          "name": "productId",
          "type": "String"
        },
        {
          "name": "productName",
          "type": "String"
        },
        {
          "name": "quantity",
          "type": "Integer"
        },
        {
          "name": "unitPrice",
          "type": "Decimal"
        }
      ]
    },
    {
      "name": "Address",
      "properties": [
        {
          "name": "street",
          "type": "String"
        },
        {
          "name": "city",
          "type": "String"
        },
        {
          "name": "postalCode",
          "type": "String"
        }
      ]
    }
  ],
  "businessRules": [
    {
      "ruleId": "SHIP-001",
      "description": "คำนวณค่าจัดส่งสำหรับลูกค้าทั่วไปที่ยอดซื้อไม่ถึง 500 บาท",
      "condition": "customer.customerType == 'ทั่วไป' AND order.rawTotalPrice < 500",
      "action": "order.shippingFee = 40"
    },
    {
      "ruleId": "SHIP-002",
      "description": "ยกเว้นค่าจัดส่งสำหรับลูกค้าทั่วไปที่ยอดซื้อถึง 500 บาท",
      "condition": "customer.customerType == 'ทั่วไป' AND order.rawTotalPrice >= 500",
      "action": "order.shippingFee = 0"
    },
    {
      "ruleId": "DISC-001",
      "description": "ให้ส่วนลด 10% สำหรับลูกค้า VIP",
      "condition": "customer.customerType == 'VIP'",
      "action": "order.discount = order.rawTotalPrice * 0.10"
    },
    {
      "ruleId": "SHIP-003",
      "description": "ยกเว้นค่าจัดส่งสำหรับลูกค้า VIP เสมอ",
      "condition": "customer.customerType == 'VIP'",
      "action": "order.shippingFee = 0"
    },
    {
      "ruleId": "STOCK-001",
      "description": "ตรวจสอบสต็อกสินค้าก่อนยืนยันคำสั่งซื้อ",
      "trigger": "Before order confirmation",
      "action": "CHECK product.stockQuantity FOR EACH order.orderItems"
    }
  ]
}
```

</details>

---

**คำแนะนำในการใช้เอกสารนี้:**

- **Project Manager / Business Team:** ใช้ **`ส่วนที่ 1 (แผนภาพ)`** และ **`ส่วนที่ 2 (ตารางสรุป)`** เป็นหลัก เพื่อทำความเข้าใจภาพรวมและเงื่อนไขต่างๆ
- **Developers:** ใช้ **`ส่วนที่ 3 (JSON Model)`** เป็น Source of Truth สำหรับการพัฒนา และใช้แผนภาพต่างๆ เพื่อทำความเข้าใจความสัมพันธ์และ Flow การทำงาน
- **QA / Testers:** ใช้ **`ส่วนที่ 1.3 (Flowchart)`** และ **`ส่วนที่ 2 (ตารางสรุป)`** ในการออกแบบ Test Cases เพื่อให้มั่นใจว่าครอบคลุมทุกเงื่อนไข
-

```

```
