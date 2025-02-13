from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt

def add_border_to_existing_images(doc_path, output_path, border_color="000000", border_width=Pt(2)):
    # 打开文档
    doc = Document(doc_path)

    # 遍历文档中的所有段落
    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            # 检查是否有图片
            if run._element.xpath(".//wp:inline"):
                # 获取图片的XML元素
                inline = run._element.xpath(".//wp:inline")[0]
                drawing = inline.xpath(".//a:graphic", namespaces=inline.nsmap)[0]

                # 创建边框属性
                spPr = OxmlElement("pic:spPr")
                ln = OxmlElement("a:ln")
                ln.set(qn("w"), str(int(border_width)))  # 边框宽度（单位：1/12700英寸）

                # 设置边框颜色（默认黑色）
                solidFill = OxmlElement("a:solidFill")
                srgbClr = OxmlElement("a:srgbClr")
                srgbClr.set(qn("val"), border_color)
                solidFill.append(srgbClr)
                ln.append(solidFill)

                # 将边框属性添加到图形属性
                spPr.append(ln)

                # 找到图片的图形属性并替换
                pic = drawing.xpath(".//pic:pic", namespaces=drawing.nsmap)[0]
                pic.insert(0, spPr)

    # 保存文档
    doc.save(output_path)

# 使用示例
add_border_to_existing_images("input.docx", "output.docx", border_color="FF0000", border_width=Pt(4))  # 红色4磅边框
