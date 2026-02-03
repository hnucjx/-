from tkinter import filedialog
from tkinter import Tk
from PIL import Image
import numpy as np

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

    # 转换为Numpy数组
    img_array = np.array(img_gray)
    print("矩阵中的值:", np.unique(img_array))
    print(img_array)

    # 使用阈值处理（这里使用127作为阈值，可以根据需要调整）
    binary_matrix = np.where(img_array > 210, 1, 0)

    print("矩阵大小:", binary_matrix.shape)
    print("矩阵中的值:", np.unique(binary_matrix))
    print(binary_matrix)

    # 创建新的PIL图像对象 - 确保使用正确的模式('L'表示灰度)
    new_img = Image.fromarray((binary_matrix * 255).astype(np.uint8))

    # 保存图像为BMP格式
    new_img.save("output.bmp")

    # 显示原始图像和新图像的比较
    print("已保存为output.bmp")
    new_img.show()

else:
    print("未选择图像文件")