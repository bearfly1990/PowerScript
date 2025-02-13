from docx import Document
from docx.shared import Inches, Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def add_border_to_image(document, image_path, border_color="000000", border_width=Pt(2)):
    # 添加图片到文档
    paragraph = document.add_paragraph()
    run = paragraph.add_run()
    run.add_picture(image_path, width=Inches(2.0))

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

# 使用示例
doc = Document()
add_border_to_image(doc, "your_image.jpg", border_color="FF0000", border_width=Pt(4))  # 红色4磅边框
doc.save("image_with_border.docx")
