from lxml import etree
root = etree.Element("family")
# 插入子节点
etree.SubElement(root, "mother")
etree.SubElement(root, "child")
etree.SubElement(root, "child")
etree.SubElement(root, "child")
etree.SubElement(root, "father")

# 输出是bytes 需要转换为utf-8
print(etree.tostring(root, pretty_print=True).decode("utf-8"))
