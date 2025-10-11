from lxml import etree

# Đọc file XML
tree = etree.parse("quanlybanan.xml")
root = tree.getroot()

# Danh sách truy vấn XPath
queries = {
    "1. Tất cả bàn": "//BANS/BAN",
    "2. Tất cả nhân viên": "//NHANVIENS/NHANVIEN",
    "3. Tên món": "//MONS/MON/TENMON/text()",
    "4. Tên NV có mã NV02": "//NHANVIEN[MANV='NV02']/TENV/text()",
    "5. Tên + SDT NV03": "//NHANVIEN[MANV='NV03']/TENV/text() | //NHANVIEN[MANV='NV03']/SDT/text()",
    "6. Món giá > 50,000": "//MON[number(GIA) > 50000]/TENMON/text()",
    "7. Số bàn HD03": "//HOADON[SOHD='HD03']/SOBAN/text()",
    "8. Tên món M02": "//MON[MAMON='M02']/TENMON/text()",
    "9. Ngày lập HD03": "//HOADON[SOHD='HD03']/NGAYLAP/text()",
    "10. Mã món HD01": "//HOADON[SOHD='HD01']//CTHD/MAMON/text()",
    "11. Tên món HD01": "//MON[MAMON=//HOADON[SOHD='HD01']//CTHD/MAMON]/TENMON/text()",
    "12. Tên NV lập HD02": "//NHANVIEN[MANV=//HOADON[SOHD='HD02']/MANV]/TENV/text()",
    "13. Đếm số bàn": "count(//BANS/BAN)",
    "14. Đếm số HĐ NV01": "count(//HOADON[MANV='NV01'])",
    "15. Tên món bàn 2": "//MON[MAMON=//HOADON[SOBAN=2]//CTHD/MAMON]/TENMON/text()",
    "16. NV phục vụ bàn 3": "//NHANVIEN[MANV=//HOADON[SOBAN=3]/MANV]/TENV/text()",
    "17. Hóa đơn nhân viên nữ": "//HOADON[MANV=//NHANVIEN[GIOITINH='Nữ']/MANV]",
    "18. NV phục vụ bàn 1": "//NHANVIEN[MANV=//HOADON[SOBAN=1]/MANV]/TENV/text()",
    "19. Món gọi > 1 lần": "//MON[MAMON=//CTHD[number(SOLUONG) > 1]/MAMON]/TENMON/text()",
    "20. Tên bàn + ngày lập HD02": "concat(//BANS/BAN[SOBAN=//HOADON[SOHD='HD02']/SOBAN]/TENBAN/text(), ' - ', //HOADON[SOHD='HD02']/NGAYLAP/text())",
}

for name, query in queries.items():
    result = root.xpath(query)
    if isinstance(result, list):
        if all(isinstance(x, etree._Element) for x in result):
            output = [etree.tostring(x, encoding='unicode', pretty_print=True) for x in result]
        else:
            output = result
    else:
        output = [str(result)]
    
    print(f"\n{name}:")
    for item in output:
        print("  ➤", item)
