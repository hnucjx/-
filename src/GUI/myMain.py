import this
import tkinter as tk
from tkinter import messagebox
from src.DB.DBConnection import DBConnection
from myWMEmbed import MyWMEmbed
from myWMExtract import MyWMExtract
from skimage.metrics import structural_similarity as ssim
from PIL import Image
import numpy as np

class FrmMain():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("主窗口")
        self.root.geometry("600x300")
        self.db_connection = None
        self.create_gui()
        self.root.mainloop()

    def create_gui(self):
        frame_connection = tk.Frame(self.root, bd=1, relief=tk.SOLID)
        frame_connection.place(x=10, y=11, width=284, height=167)
        frame_connection_label = tk.Label(frame_connection, text="  数据库连接  ",
                                          font=("Dialog", 12, "bold italic"), fg="gray")
        frame_connection_label.pack()

        labels = ["服务器:", "用户名:", "密码:", "数据库:"]
        default_values = ["localhost", "root", "123456", "covertype"]
        entries = []

        # 创建变量用于保存用户输入的值
        Server = tk.StringVar()
        User = tk.StringVar()
        Password = tk.StringVar()
        Database = tk.StringVar()
        variables = [Server, User, Password, Database]

        for i, label_text in enumerate(labels):
            label = tk.Label(frame_connection, text=label_text)
            label.place(x=10, y=32 + i * 25)

            if label_text == "密码:":
                entry = tk.Entry(frame_connection, show="*", textvariable=variables[i])  # 密码框
            else:
                entry = tk.Entry(frame_connection, textvariable=variables[i])

            entry.insert(0, default_values[i])
            entry.place(x=77, y=29 + i * 25, width=197)

            entries.append(entry)

        # 创建连接按钮
        def connect_to_db():
            if ButtConnect.cget("text") == "连接":
                if self.db_connection is None:
                    server = Server.get()
                    user = User.get()
                    password = Password.get()
                    database = Database.get()
                    self.db_connection = DBConnection(server, user, password, database)
                    self.db_connection.test()
                    if self.db_connection.getConnection() is not None:
                        ButtConnect.config(text="断开连接")
                        lblStatus.config(fg="green", text="连接中")
                        # 启用其他按钮
                        ButtEmbedWM.config(state=tk.NORMAL)
                    else:
                        messagebox.showerror("连接失败", "连接失败!!!")
                        lblStatus.config(fg="red", text="断开连接")
                        # 禁用其他按钮
                        ButtEmbedWM.config(state=tk.DISABLED)
                else:
                    messagebox.showerror("错误", "已经连接到数据库!")
            else:
                if self.db_connection.getConnection() is not None:
                    try:
                        self.db_connection.getConnection().close()
                        print("连接关闭")
                    except Exception as e:
                        messagebox.showerror("错误", "出现问题!!!")
                        lblStatus.config(fg="red", text="断开连接")
                    self.db_connection = None
                    lblStatus.config(fg="red", text="断开连接")
                    ButtConnect.config(text="连接")

        ButtConnect = tk.Button(frame_connection, text="连接", command=connect_to_db)
        ButtConnect.place(x=150, y=135, width=127, height=23)

        lblStatus = tk.Label(frame_connection, text="未连接", fg="red")
        lblStatus.place(x=54, y=135)

        lblCaption = tk.Label(frame_connection, text="状态：")
        lblCaption.place(x=10, y=135)

        # 创建带边框的容器
        wm_pro = tk.Frame(self.root, bd=1, relief=tk.SOLID)
        wm_pro.place(x=10, y=200, width=580, height=80)

        # 名称
        wm_pro_label = tk.Label(wm_pro, text="水印处理过程",
                                font=("Dialog", 12, "bold italic"),fg="gray")
        wm_pro_label.pack()

        def CreatButtEmbedWM():
            EmbedWM = MyWMEmbed(self.db_connection)

        ButtEmbedWM = tk.Button(wm_pro, text="嵌入水印", command=CreatButtEmbedWM)
        ButtEmbedWM.place(x=30, y=26, width=200, height=35)
        ButtEmbedWM.config(state=tk.NORMAL)

        def CreatButtExtractWM():
            ExtractWM = MyWMExtract(self.db_connection)

        ButtEmbedWM = tk.Button(wm_pro, text="提取水印", command=CreatButtExtractWM)
        ButtEmbedWM.place(x=350, y=26, width=200, height=35)
        ButtEmbedWM.config(state=tk.NORMAL)

        # 图像评估
        fraMetrics = tk.Frame(self.root, bd=1, relief=tk.SOLID)
        fraMetrics.place(x=310, y=11, width=279, height=167)

        labMetrics = tk.Label(fraMetrics, text="图像评估",
                                font=("Dialog", 12, "bold italic"), fg="gray")
        labMetrics.pack()

        # SSIM
        labSSIM = tk.Label(fraMetrics, text="结构相似性指数")
        labSSIM.place(x=18, y=37)
        labSSIM2 = tk.Label(fraMetrics, text="SSIM:")
        labSSIM2.place(x=18, y=67)
        EntrySSIM = tk.Entry(fraMetrics)
        EntrySSIM.delete(0, tk.END)
        EntrySSIM.insert(0, "0")
        EntrySSIM.place(x=61, y=69, width=50, height=20)

        def calculateSSIM():
            imgEmbed = Image.open('../../IMG/embed.bmp')
            npEmbed = np.array(imgEmbed)
            imgExtracted = Image.open('../../IMG/embed - 副本.bmp')
            npExtracted = np.array(imgExtracted)
            print(npExtracted)
            # 使用 SSIM 计算
            SSIM = ssim(npEmbed, npExtracted, win_size=3, multichannel=True)
            EntrySSIM.delete(0, tk.END)
            EntrySSIM.insert(0, SSIM)


        ButtSSIM = tk.Button(fraMetrics, text="计算SSIM", command=calculateSSIM)
        ButtSSIM.place(x=18, y=105, width=90, height=35)
        ButtSSIM.config(state=tk.NORMAL)

        # CF
        labCF = tk.Label(fraMetrics, text="校正系数")
        labCF.place(x=165, y=37)
        labCF2 = tk.Label(fraMetrics, text="CF:")
        labCF2.place(x=165, y=67)
        EntryCF= tk.Entry(fraMetrics)
        EntryCF.delete(0, tk.END)
        EntryCF.insert(0, "0")
        EntryCF.place(x=190, y=69, width=50, height=20)

        def calculateCF():
            imgEmbed = Image.open('../../IMG/embed.bmp')
            npEmbed = np.array(imgEmbed)
            imgExtracted = Image.open('../../IMG/embed - 副本.bmp')
            npExtracted = np.array(imgExtracted)

            # 获取图像的宽度和高度
            originalImgWidth, originalImgHeight = npEmbed.shape[1], npEmbed.shape[0]

            # 初始化累积误差 cumul 和校正因子 cf
            cumul = 0

            # 遍历每一个像素，计算累积误差
            for i in range(originalImgWidth):
                for j in range(originalImgHeight):
                    pixelA = npEmbed[j][i]  # A像素
                    pixelB = npExtracted[j][i]  # B像素
                    if pixelA.any() == pixelB.any():
                        cumul = cumul + 1  # 计算累积误差，按位异或操作

            CF = 100 * cumul / (originalImgWidth * originalImgHeight)
            EntryCF.delete(0, tk.END)
            EntryCF.insert(0, CF)

        ButtCF = tk.Button(fraMetrics, text="计算CF", command=calculateCF)
        ButtCF.place(x=165, y=105, width=90, height=35)
        ButtCF.config(state=tk.NORMAL)

if __name__ == "__main__":
    app = FrmMain()
    app.mainloop()