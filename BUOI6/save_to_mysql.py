# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

from lxml import etree
import mysql.connector
from tabulate import tabulate
from colorama import Fore, Style, init

init(autoreset=True)

XML_FILE = "catalog.xml"
XSD_FILE = "catalog.xsd"

print(Fore.CYAN + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print(Fore.CYAN + "🚀  BẮT ĐẦU KIỂM TRA & LƯU DỮ LIỆU XML → MYSQL")
print(Fore.CYAN + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

# =============== 1️⃣ Kiểm tra XML hợp lệ ========================
try:
    xml_doc = etree.parse(XML_FILE)
    xsd_doc = etree.parse(XSD_FILE)
    schema = etree.XMLSchema(xsd_doc)

    if not schema.validate(xml_doc):
        print(Fore.RED + "❌ XML KHÔNG HỢP LỆ VỚI XSD!")
        for error in schema.error_log:
            print(Fore.YELLOW + f"⚠️  Dòng {error.line}: {error.message}")
        sys.exit(1)
    else:
        print(Fore.GREEN + "✅ XML hợp lệ với XSD, tiếp tục xử lý...\n")

except Exception as e:
    print(Fore.RED + "❌ Lỗi khi đọc hoặc kiểm tra XML/XSD:", e)
    sys.exit(1)

# =============== 2️⃣ Kết nối MySQL ==============================
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="catalog_db"
    )
    cursor = conn.cursor()
    print(Fore.GREEN + "✅ Kết nối MySQL thành công!\n")

except Exception as e:
    print(Fore.RED + "❌ Kết nối MySQL thất bại:", e)
    sys.exit(1)

# =============== 3️⃣ Tạo bảng nếu chưa có =======================
cursor.execute("""
CREATE TABLE IF NOT EXISTS Categories (
    id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Products (
    id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100),
    price DECIMAL(10,2),
    currency VARCHAR(10),
    stock INT,
    categoryRef VARCHAR(10),
    FOREIGN KEY (categoryRef) REFERENCES Categories(id)
)
""")
conn.commit()

# =============== 4️⃣ Parse dữ liệu bằng XPath ===================
root = xml_doc.getroot()
categories = root.xpath("//categories/category")
products = root.xpath("//products/product")

# =============== 5️⃣ Insert / Update Categories =================
print(Fore.CYAN + "📂 Cập nhật bảng Categories...")
for c in categories:
    cat_id = c.get("id")
    cat_name = c.text.strip()
    cursor.execute("""
        INSERT INTO Categories (id, name)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE name = VALUES(name)
    """, (cat_id, cat_name))
conn.commit()
print(Fore.GREEN + f"✅ Đã cập nhật {len(categories)} danh mục.\n")

# =============== 6️⃣ Insert / Update Products ===================
print(Fore.CYAN + "🛒 Cập nhật bảng Products...")
for p in products:
    prod_id = p.get("id")
    cat_ref = p.get("categoryRef")
    name = p.findtext("name")
    price = p.findtext("price")
    currency = p.find("price").get("currency")
    stock = p.findtext("stock")

    cursor.execute("""
        INSERT INTO Products (id, name, price, currency, stock, categoryRef)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            name = VALUES(name),
            price = VALUES(price),
            currency = VALUES(currency),
            stock = VALUES(stock),
            categoryRef = VALUES(categoryRef)
    """, (prod_id, name, price, currency, stock, cat_ref))
conn.commit()
print(Fore.GREEN + f"✅ Đã cập nhật {len(products)} sản phẩm.\n")

# =============== 7️⃣ Hiển thị dữ liệu ===========================
print(Fore.CYAN + "📊 DỮ LIỆU HIỆN CÓ TRONG CSDL:\n")

cursor.execute("""
SELECT p.id, p.name, p.price, p.currency, p.stock, c.name AS category
FROM Products p
JOIN Categories c ON p.categoryRef = c.id
""")
rows = cursor.fetchall()

headers = ["ID", "Tên sản phẩm", "Giá", "Tiền tệ", "Tồn kho", "Danh mục"]
print(Fore.LIGHTYELLOW_EX + tabulate(rows, headers, tablefmt="fancy_grid"))

cursor.close()
conn.close()

print("\n" + Fore.GREEN + Style.BRIGHT + "🎉 Hoàn tất: Dữ liệu đã lưu & hiển thị thành công!")
print(Fore.CYAN + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
