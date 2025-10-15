import xml.etree.ElementTree as ET
import mysql.connector
from mysql.connector import Error

# 1️⃣ Đọc XML
tree = ET.parse('catalog.xml')
root = tree.getroot()

# 2️⃣ Kết nối MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',      # nếu bạn có mật khẩu, điền vào đây
    database='catalog_db'
)
cursor = conn.cursor()

# 3️⃣ Thêm hoặc cập nhật Categories
for category in root.find('categories').findall('category'):
    cat_id = category.get('id')
    name = category.text

    cursor.execute("""
        INSERT INTO Categories (id, name)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE name = VALUES(name)
    """, (cat_id, name))

# 4️⃣ Thêm hoặc cập nhật Products
for product in root.find('products').findall('product'):
    prod_id = product.get('id')
    category_ref = product.get('categoryRef')
    name = product.find('name').text
    price = product.find('price').text
    currency = product.find('price').get('currency')
    stock = product.find('stock').text

    cursor.execute("""
        INSERT INTO Products (id, name, price, currency, stock, categoryRef)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            name = VALUES(name),
            price = VALUES(price),
            currency = VALUES(currency),
            stock = VALUES(stock),
            categoryRef = VALUES(categoryRef)
    """, (prod_id, name, price, currency, stock, category_ref))

# 5️⃣ Lưu thay đổi
conn.commit()
print("✅ Dữ liệu đã được chèn/cập nhật thành công!")

# 6️⃣ Đóng kết nối
cursor.close()
conn.close()
