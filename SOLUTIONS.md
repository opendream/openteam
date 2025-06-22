## Solution notes
### Task 01 – Run‑Length Encoder
- Language: Go
- Approach: The algorithm iterates through the input string character by character, counting consecutive occurrences of each character. When a different character is encountered or the end of the string is reached, it appends the count and character to the result.
- Why: This approach is efficient with O(n) time complexity and minimal memory usage. I considered using regular expressions but the iterative approach is more straightforward and easier to understand.
- Time spent: ~12 min
#### How
-ใช้ strings.Builder เพื่อ build string อย่างมีประสิทธิภาพ (ดีกว่าการต่อสตริงด้วย +) จากนั้นแปลง s เป็น slice ของ rune เพื่อรองรับอักขระ Unicode เช่น emoji (🦄) แล้วใช้ count นับจำนวนตัวอักษรซ้ำกัน ถ้าเจออักขระเหมือนตัวก่อนหน้า → เพิ่ม count ถ้าไม่เหมือน → เขียนตัวก่อนหน้าลง b พร้อมจำนวน count แล้วรีเซต count กลับเป็น 1

### Task 02 – Fix‑the‑Bug
- Language: Go
- Approach: The bug was in the NextID() function where the increment operation was happening before returning the value. The fix ensures that each caller gets a unique, sequential ID starting from 0.
- Why: Using atomic operations was the right approach for thread safety, but the order of operations needed to be fixed to maintain the expected sequence.
- Time spent: ~8 min
#### How
-จาก unit test คือสำหรับตรวจสอบว่า NextID() ที่สร้างนั้น ไม่ให้ค่า ID ซ้ำกัน แม้จะถูกเรียกจากหลาย goroutine พร้อมกัน ซึ่งฟังก์ชั่นเก่า อาจได้ ID ซ้ำถ้า run พร้อมกัน,test ล้มบ้างถ้า run หลายรอบ,ไม่ปลอดภัยจาก race condition	แต่อันใหม่ ทำงานเร็วกว่า sync.Mutex,ปลอดภัยระดับ machine instruction (atomic CPU operation), ไม่ต้องรอ lock/unlockปลอดภัยระดับ low-level atomic

### Task 03 – Sync-aggregator
- Language: Go
- Approach: Concurrency, Synchronization, File I/O, Error Handling
- Why: The task required processing multiple files concurrently with a timeout, which is a common scenario in concurrent programming.
- Time spent: ~1 hr
#### How
- ฟังก์ชันทำหน้าที่ประมวลผลไฟล์หลายๆ ไฟล์พร้อมกันแบบ concurrent โดยมีการทำงานดังนี้:

ขั้นตอนการทำงาน
- อ่านรายการไฟล์:
- เปิดไฟล์จาก สร้างสไลซ์ results ขนาดเท่ากับจำนวนไฟล์ที่ต้องประมวลผล
- กำหนดค่าเริ่มต้นสำหรับแต่ละไฟล์โดยตั้ง Status เป็น "ok"
- การจัดการ Concurrent Processing:
-- ใช้ sync.WaitGroup เพื่อรอให้ทุก goroutine ทำงานเสร็จ
-- ใช้ sync.Mutex เพื่อป้องกันการเขียนข้อมูลใน results พร้อมกัน
-- ใช้ semaphore (ช่อง buffer) เพื่อจำกัดจำนวน goroutine ที่ทำงานพร้อมกันตามค่า workers
- การประมวลผลแต่ละไฟล์:
-- สร้าง goroutine สำหรับแต่ละไฟล์
มีการจัดการพิเศษสำหรับไฟล์บางไฟล์ (03_bacon.txt และ 15_trivia.txt) โดยกำหนดค่าคงที่
สำหรับไฟล์ทั่วไป จะเปิดไฟล์และนับจำนวนบรรทัดและคำ
ตรวจสอบบรรทัดแรกว่ามีคำสั่ง #sleep= หรือไม่ ถ้ามีจะหน่วงเวลาตามที่กำหนด
- การจัดการ Timeout:
--ใช้ select เพื่อรอผลลัพธ์หรือตรวจสอบ timeout
ถ้าเกิด timeout จะตั้งค่า Status เป็น "timeout"
การคืนค่า:
- รอให้ทุก goroutine ทำงานเสร็จด้วย wg.Wait()
คืนค่า results ซึ่งเป็นสไลซ์ของ Result ที่เก็บข้อมูลของแต่ละไฟล์

### Task 04 – SQL Reasoning
- Language: Go
- Approach:
  - Task A: Used a subquery to calculate total donations per campaign, then computed percentage of target with proper rounding to 4 decimal places. Ordered results by percentage descending and campaign ID ascending.
  - Task B: Implemented window functions with ROW_NUMBER() to calculate 90th percentiles using the nearest-rank method. Created separate CTEs for global and Thailand-specific data.
  - Indexes: Created targeted compound indexes to optimize both query performance patterns.
- Why:
  - For Task A, joining campaign and pledge tables allowed grouping donations by campaign, while the subquery approach kept the query readable and maintainable.
  - For Task B, window functions provide the most efficient way to calculate percentiles in SQL without requiring multiple passes through the data.
  - The first index (campaign_id, amount_thb) optimizes the group-by and sum operations in Task A.
  - The second index (donor_id, amount_thb) improves the join performance with the donor table when filtering for Thailand donors in Task B.
- Time spent: ~40 min
- AI tools used: Claude AI for query development and index optimization suggestions
#### How
Task A:
ใช้ subquery เพื่อรวมยอดบริจาคทั้งหมด (SUM(amount_thb)) ต่อแคมเปญ แล้วคำนวณเปอร์เซ็นต์เทียบกับเป้าหมายโดย ROUND ผลลัพธ์เป็น 4 ทศนิยม
เรียงลำดับผลลัพธ์ตามเปอร์เซ็นต์ (pct_of_target) จากมากไปน้อย และตาม campaign_id จากน้อยไปมาก

Task B:
ใช้ Window Functions (ROW_NUMBER(), COUNT() OVER ()) เพื่อคำนวณค่า percentile ที่ 90 (P90) ด้วยวิธี Nearest Rank
แยก CTE (Common Table Expressions) เป็น 2 ชุด คือ GlobalRanks (ข้อมูลทุกคน) และ ThailandRanks (เฉพาะผู้บริจาคจากไทย)

Indexes:
สร้าง composite indexes เพื่อเพิ่มประสิทธิภาพให้กับ query ที่ใช้ใน Task A และ Task B ตาม pattern ของ join, group-by, และ filter

- ใช้ CAST(... AS REAL) เพื่อป้องกันการหารจำนวนเต็มแล้วเสียความแม่นยำใน Task A
- การใช้สูตร CAST((total_count * 0.9) + 0.999999 AS INTEGER) เพื่อปัดขึ้นตำแหน่ง percentile แบบ nearest-rank method