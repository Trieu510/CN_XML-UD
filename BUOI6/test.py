from lxml import etree

xml_doc = etree.parse("catalog.xml")
xsd_doc = etree.parse("catalog.xsd")
schema = etree.XMLSchema(xsd_doc)

print("XML hợp lệ với XSD:", schema.validate(xml_doc))
