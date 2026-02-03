from tkinter import filedialog
from tkinter import Tk
from PIL import Image

# 创建一个Tkinter窗口
root = Tk()
root.withdraw()  # 隐藏Tkinter窗口

# 选择图像文件
file_path = filedialog.askopenfilename(title="选择图像文件", filetypes=[("Image files", "*.jpg *.png *.bmp")])

if file_path:
    # 打开图像文件
    img = Image.open(file_path)

    # 先转换为灰度图
    img_gray = img.convert('L')

    # 获取图像的像素值列表
    img_pixels = list(img_gray.getdata())

    # 使用阈值处理（这里使用127作为阈值，可以根据需要调整）
    binary_matrix = [1 if pixel > 127 else 0 for pixel in img_pixels]

    # 获取图像的宽度和高度
    width, height = img_gray.size

    # 将二值化后的矩阵转换为二维列表
    binary_matrix_2d = [binary_matrix[i * width:(i + 1) * width] for i in range(height)]

    # 创建新的PIL图像对象 - 确保使用正确的模式('1'表示二值图像)
    new_img = Image.new('1', (width, height))
    new_img.putdata(binary_matrix)

    # 保存图像为BMP格式
    new_img.save("output.bmp")

    # 显示原始图像和新图像的比较
    print("已保存为output.bmp")
    new_img.show()

else:
    print("未选择图像文件")

# 关闭Tkinter窗口
root.destroy()