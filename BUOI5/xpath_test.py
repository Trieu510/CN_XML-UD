from lxml import etree

# Đọc file XML
tree = etree.parse("sinhvien.xml")
root = tree.getroot()

# Danh sách truy vấn XPath
queries = {
    "1. Tất cả sinh viên": "//student",
    "2. Tên tất cả sinh viên": "//student/name/text()",
    "3. ID tất cả sinh viên": "//student/id/text()",
    "4. Ngày sinh SV01": "//student[id='SV01']/date/text()",
    "5. Các khóa học": "//enrollment/course/text()",
    "6. Thông tin SV đầu tiên": "//student[1]/*/text()",
    "7. Mã SV đăng ký 'Vatly203'": "//enrollment[course='Vatly203']/studentRef/text()",
    "8. Tên SV học 'Toan101'": "//student[id=//enrollment[course='Toan101']/studentRef]/name/text()",
    "9. Tên SV học 'Vatly203'": "//student[id=//enrollment[course='Vatly203']/studentRef]/name/text()",
    "10. Ngày sinh SV01 (lặp)": "//student[id='SV01']/date/text()",
    "11. Tên và ngày sinh SV sinh năm 1997": "//student[starts-with(date,'1997')]/*/text()",
    "12. Tên SV sinh trước năm 1998": "//student[number(substring(date,1,4)) < 1998]/name/text()",
    "13. Tổng số sinh viên": "count(//student)",
    "14. SV chưa đăng ký môn nào": "//student[not(id=//enrollment/studentRef)]/name/text()",
    "15. <date> sau <name> của SV01": "//student[id='SV01']/name/following-sibling::date[1]/text()",
    "16. <id> trước <name> của SV02": "//student[id='SV02']/name/preceding-sibling::id[1]/text()",
    "17. <course> của SV03": "//enrollment[studentRef='SV03']/course/text()",
    "18. SV họ 'Trần'": "//student[starts-with(name,'Trần')]/name/text()",
    "19. Năm sinh SV01": "substring(//student[id='SV01']/date,1,4)",
}

# In kết quả ra console
for desc, query in queries.items():
    result = root.xpath(query)
    print(f"\n{desc}:")
    if isinstance(result, list):
        if len(result) == 0:
            print("  → Không có kết quả.")
        else:
            for r in result:
                print("  -", r)
    else:
        print("  -", result)
