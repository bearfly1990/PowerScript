from openpyxl import load_workbook
from openpyxl.drawing.image import Image
from openpyxl.drawing.shapes import LineProperties
from openpyxl.drawing.colors import RGBColor

def add_border_shadow_to_excel_images(excel_path, output_path):
    # 加载Excel工作簿（只读模式关闭，才能修改）
    wb = load_workbook(excel_path, read_only=False, data_only=False)
    
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        # 遍历工作表中所有图片（openpyxl通过_shapes属性获取）
        for shape in ws._shapes:
            # 仅处理图片类型（排除图表、形状等）
            if hasattr(shape, "anchor") and shape.__class__.__name__ in ["Image", "Drawing"]:
                # 1. 设置图片边框（黑色、2磅粗细）
                if hasattr(shape, "line"):
                    shape.line = LineProperties(
                        width=20000,  # 1磅=10000EMU，2磅=20000
                        solidFill=RGBColor(0, 0, 0)  # 黑色边框
                    )
                
                # 2. 设置阴影效果（外阴影、灰色、偏移+模糊）
                if hasattr(shape, "shadow"):
                    shape.shadow = {
                        "visible": True,
                        "blur": 6,  # 阴影模糊度
                        "distance": 3,  # 阴影偏移距离
                        "direction": 270,  # 阴影方向（270=向下）
                        "color": RGBColor(128, 128, 128)  # 灰色阴影
                    }
    
    # 保存修改后的Excel文件
    wb.save(output_path)
    print(f"处理完成！文件已保存到：{output_path}")

# ------------------- 运行代码 -------------------
if __name__ == "__main__":
    # 替换为你的Excel文件路径和输出路径
    INPUT_EXCEL = "input.xlsx"   # 原始Excel文件
    OUTPUT_EXCEL = "output.xlsx" # 处理后的Excel文件
    add_border_shadow_to_excel_images(INPUT_EXCEL, OUTPUT_EXCEL)

