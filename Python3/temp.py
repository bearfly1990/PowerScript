from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt

def add_border_to_existing_images(doc_path, output_path, border_color="000000", border_width=Pt(2)):
    doc = Document(doc_path)
    
    # 定义命名空间（避免重复解析）
    namespaces = {
        "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
        "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
        "pic": "http://schemas.openxmlformats.org/drawingml/2006/picture"
    }

    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            # 查找图片元素
            inline = run._element.find(".//wp:inline", namespaces=namespaces)
            if inline is not None:
                # 获取图形和图片元素
                graphic = inline.find(".//a:graphic", namespaces=namespaces)
                pic = graphic.find(".//pic:pic", namespaces=namespaces)
                
                # 创建边框属性
                spPr = OxmlElement("pic:spPr")
                ln = OxmlElement("a:ln")
                ln.set(qn("a:w"), str(int(border_width)))  # 正确使用命名空间前缀

                # 设置颜色
                solidFill = OxmlElement("a:solidFill")
                srgbClr = OxmlElement("a:srgbClr")
                srgbClr.set(qn("a:val"), border_color)  # 指定命名空间前缀
                solidFill.append(srgbClr)
                ln.append(solidFill)
                spPr.append(ln)

                # 插入边框属性
                existing_spPr = pic.find(".//pic:spPr", namespaces=namespaces)
                if existing_spPr is not None:
                    pic.replace(existing_spPr, spPr)
                else:
                    pic.insert(0, spPr)

    doc.save(output_path)

# 使用示例
add_border_to_existing_images("input.docx", "output.docx", border_color="FF0000", border_width=Pt(4))
