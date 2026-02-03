import tkinter as tk
import random
from tkinter import ttk
from src.DB.DBConnection import DBConnection
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk, ImageColor
from src.utils.Util import Util
import datetime
import hashlib


class MyWMExtract():
    def __init__(self, db_connection):
        self.db_connection = db_connection
        # 要用tk.Toplevel()而不是tk.TK()，否则会出现主窗口冲突
        self.root = tk.Toplevel()
        self.root.title('水印的提取')
        self.root.geometry("723x425")
        self.imgVector = []
        self.imgIcon = None
        self.oriImg = None
        self.imgWidth = 0
        self.imgHeight = 0

        self.myWMExtract()
        self.root.mainloop()

    def myWMExtract(self):
        # 选择要嵌入的表格
        lbRelationToMark = tk.Label(self.root, text="提取的数据库表格：")
        lbRelationToMark.place(x=10, y=11, width=110, height=14)
        valueRelationToMark = ["covertype_1000", "covertype_2000", "covertype_3000", "covertype_10000", "covertype_15000"]
        comboRelationToMark = ttk.Combobox(
            master=self.root,
            width=21,
            height=20,
            state='readonly',
            cursor='arrow',
            values=valueRelationToMark,
        )
        comboRelationToMark.place(x=123, y=8)

        # 私钥
        lbPri = tk.Label(self.root, text="密钥：")
        lbPri.place(x=10, y=37, width=110, height=14)
        EntryPri = tk.Entry(self.root)
        EntryPri.delete(0, tk.END)
        EntryPri.insert(0, "Secu3960422323K")
        EntryPri.place(x=123, y=34, width=85, height=20)

        # MSB
        lbMSB = tk.Label(self.root, text="MSB:")
        lbMSB.place(x=222, y=38, width=31, height=14)
        EntryMSB = tk.Entry(self.root)
        EntryMSB.delete(0, tk.END)
        EntryMSB.insert(0, "3")
        EntryMSB.place(x=257, y=35, width=37, height=20)

        # LSB
        lbLSB = tk.Label(self.root, text="LSB:")
        lbLSB.place(x=222, y=61, width=31, height=14)
        EntryLSB = tk.Entry(self.root)
        EntryLSB.delete(0, tk.END)
        EntryLSB.insert(0, "2")
        EntryLSB.place(x=257, y=58, width=37, height=20)

        # 元组分数
        lbFraction = tk.Label(self.root, text="元组分数：")
        lbFraction.place(x=10, y=60, width=110, height=14)
        EntryFraction = tk.Entry(self.root)
        EntryFraction.delete(0, tk.END)
        EntryFraction.insert(0, "4")
        EntryFraction.place(x=123, y=57, width=47, height=20)

        # 提取出的图片
        frameImage = tk.LabelFrame(self.root, width=387, height=232, text="提取的水印图像", labelanchor="n")
        frameImage.place(x=304, y=9)

        lbImg = tk.Label(frameImage, relief="groove", borderwidth=1)
        lbImg.place(x=10, y=33, width=184, height=164)

        # 图片的尺寸，手动输入
        lbHeight = tk.Label(frameImage, text="图像高：")
        lbHeight.place(x=10, y=7, width=47, height=14)
        EntryHeight = tk.Entry(frameImage)
        EntryHeight.insert(0, "50")
        EntryHeight.place(x=58, y=6, width=37, height=20)

        lbWidth = tk.Label(frameImage, text="图像宽：")
        lbWidth.place(x=110, y=7, width=45, height=14)
        EntryWidth = tk.Entry(frameImage)
        EntryWidth.insert(0, "49")
        EntryWidth.place(x=155, y=6, width=37, height=20)

        # 像素值的注解
        frameExp = tk.LabelFrame(frameImage, width=150, height=75, text="  解释  ", labelanchor="n")
        frameExp.place(x=207, y=24)

        canvasR = tk.Canvas(frameExp, width=150, height=75)
        canvasR.pack()
        canvasR.create_rectangle(10, 5, 25, 20, fill="red")
        lbRed = tk.Label(frameExp, text="未提取的像素块", anchor="w")
        lbRed.place(x=30, y=5, width=95, height=14)

        lbLine2 = tk.Label(frameExp, text="————————————————————————", anchor="w")
        lbLine2.place(x=7, y=21, width=140, height=8)

        canvasR.create_rectangle(10, 35, 25, 50, fill="black")
        lbBlk = tk.Label(frameExp, text="提取的像素值 (1)", anchor="w")
        lbBlk.place(x=30, y=35, width=120, height=14)
        canvasR.create_rectangle(10, 55, 25, 70, fill="white")
        lbBlk = tk.Label(frameExp, text="提取的像素值 (0)", anchor="w")
        lbBlk.place(x=30, y=55, width=120, height=14)

        # 提取的像素值统计
        lbTotal = tk.Label(frameImage, text="总数：", anchor="w")
        lbTotal.place(x=274, y=132, width=38, height=14)
        EntryTotal = tk.Entry(frameImage)
        EntryTotal.insert(0, "0")
        EntryTotal.place(x=314, y=130, width=50, height=20)

        lbExt = tk.Label(frameImage, text="已提取：", anchor="w")
        lbExt.place(x=262, y=156, width=83, height=14)
        EntryExt = tk.Entry(frameImage)
        EntryExt.insert(0, "0")
        EntryExt.place(x=314, y=154, width=50, height=20)

        lbLine = tk.Label(frameImage, text="————————————————————————")
        lbLine.place(x=245, y=169, width=120, height=14)

        lbPct = tk.Label(frameImage, text="占比：", anchor="w")
        lbPct.place(x=275, y=184, width=83, height=14)
        EntryPct = tk.Entry(frameImage)
        EntryPct.insert(0, "0")
        EntryPct.place(x=314, y=182, width=50, height=20)

        # 考虑嵌入的属性
        frameFtE = tk.LabelFrame(self.root, width=284, height=156, text="  考虑嵌入的属性列  ", labelanchor="n")
        frameFtE.place(x=10, y=85)
        tbFtE = ttk.Treeview(frameFtE, columns=("Get", "Name", "Type"), show="headings")
        tbFtE.heading("Get", text="Get")
        tbFtE.heading("Name", text="Name")
        tbFtE.heading("Type", text="Type")
        tbFtE.column("Get", width=37, anchor="w")
        tbFtE.column("Name", width=145, anchor="w")
        tbFtE.column("Type", width=64, anchor="w")

        fixedFilds = ["ELEVATION", "ASPECT", "SLOPE", "HOR_DIST_TO_HYDROLOGY", "VERT_DIST_TO_HYDROLOGY", "HOR_DIST_TO_ROADWAYS",
                      "HILLSHADE_9AM",
                      "HILLSHADE_NOON", "HILLSHADE_3PM", "HOR_DIST_TO_FIRE_POINTS"]
        # 存储复选框变量
        check_vars = []

        for field in fixedFilds:
            var = tk.BooleanVar(value=True)  # 默认选中
            check_vars.append(var)
            tbFtE.insert("", "end", values=("✔", field, "FLOAT"))

        def toggleCheckbox(event):
            """单击 Treeview 行时切换复选框状态"""
            itemId = tbFtE.identify_row(event.y)  # 获取点击的行 ID
            if itemId:
                index = tbFtE.index(itemId)  # 获取行索引
                currentState = check_vars[index].get()
                check_vars[index].set(not currentState)  # 切换选中状态
                new_value = "✔" if not currentState else ""  # 更新 UI 显示
                tbFtE.item(itemId, values=(new_value, fixedFilds[index], "FLOAT"))

        # 绑定 Treeview 点击事件，切换复选框
        tbFtE.bind("<ButtonRelease-1>", toggleCheckbox)

        # 滚动条
        scrollbar = ttk.Scrollbar(frameFtE, orient="vertical", command=tbFtE.yview)
        tbFtE.configure(yscrollcommand=scrollbar.set)
        tbFtE.place(x=10, y=10, width=260, height=110)
        scrollbar.place(x=260, y=10, height=110)

        # 算法变形
        frameAlg = tk.LabelFrame(self.root, width=284, height=100, text="  算法拓展  ", labelanchor="n")
        frameAlg.place(x=10, y=250)

        lbFoA = tk.Label(frameAlg, text="属性分数：", anchor="w")
        lbFoA.place(x=65, y=12, width=130, height=14)
        EntryFoA = tk.Entry(frameAlg)
        EntryFoA.insert(0, "4")
        EntryFoA.place(x=140, y=11, width=30, height=20)

        BoolGue = tk.BooleanVar()
        BoolGue.set(0)
        cbGue = tk.Checkbutton(frameAlg, text="值猜测引擎", variable=BoolGue, onvalue=1, offvalue=0)
        cbGue.place(x=42, y=45, width=145, height=23)

        # 标记的关系元组
        frameRelTup = tk.LabelFrame(self.root, width=387, height=100, text="  相关的元组  ", labelanchor="n")
        frameRelTup.place(x=304, y=250)

        lbTotal2 = tk.Label(frameRelTup, text="总元组：", anchor="w")
        lbTotal2.place(x=24, y=27, width=59, height=14)
        EntryTotal2 = tk.Entry(frameRelTup)
        EntryTotal2.insert(0, "0")
        EntryTotal2.place(x=70, y=25, width=50, height=20)

        lbMarked = tk.Label(frameRelTup, text="标记的元组：", anchor="w")
        lbMarked.place(x=130, y=27, width=70, height=14)
        EntryMarked = tk.Entry(frameRelTup)
        EntryMarked.insert(0, "0")
        EntryMarked.place(x=205, y=25, width=50, height=20)

        lbPct2 = tk.Label(frameRelTup, text="占比：", anchor="w")
        lbPct2.place(x=270, y=27, width=65, height=14)
        EntryPct2 = tk.Entry(frameRelTup)
        EntryPct2.insert(0, "0")
        EntryPct2.place(x=306, y=25, width=50, height=20)

        # 开始
        def startWM():
            currentTime = datetime.datetime.now()
            # 格式化时间为 "HH:mm:ss"
            formattedTime = currentTime.strftime("%H:%M:%S")
            print("PROCESS STARTED AT: " + formattedTime)
            print("-----------------------------------------------")

            # 是否开启猜测惩罚机制
            guessCheck = False
            if BoolGue.get():
                guessCheck = True
                print('------开启惩罚引擎-------')
            # 噪声添加
            noise = False

            # 验证信号容器定义，投票机制
            verSigOne = [0 for _ in range(24)]
            verSigZero = [0 for _ in range(24)]
            # 验证信号提取
            attrName = "ELEVATION"
            table = comboRelationToMark.get()
            priKey = EntryPri.get()
            cursor = self.db_connection.getIndex(table, attrName)
            rows = cursor.fetchall()

            for row in rows:
                # 在这里处理每个元组的数据
                ID = row[0]
                attr = row[1]
                # 计算虚拟主键值
                tempString = str(ID) + priKey
                hashValue = hashlib.md5(tempString.encode()).hexdigest()
                hashValue2 = hashValue + priKey
                # 计算索引值
                index = int(hashlib.md5(hashValue2.encode()).hexdigest(), 16) % 24
                # 转换成int类型去掉小数点，再转换成绝对值
                absAttr = abs(int(attr))
                # 通过位运算获取LSB
                lsb = absAttr & 1
                if lsb == 1:
                    verSigOne[index] += 1
                else:
                    verSigZero[index] += 1

            # 获取元组分数、图片高、图片宽
            vsTF = Util.buildParamVal(verSigOne, verSigZero, 8)
            vsH = Util.buildParamVal(verSigOne, verSigZero, 16)
            vsW = Util.buildParamVal(verSigOne, verSigZero, 24)
            print("已提取正确参数")
            print(vsTF)
            print(vsH)
            print(vsW)

            tf = int(EntryFraction.get())
            self.imgHeight = int(EntryHeight.get())
            self.imgWidth = int(EntryWidth.get())

            if guessCheck:
                if tf != vsTF:
                    messagebox.showerror("错误", "TF不匹配，提取过程将添加噪声")
                    noise = True
                if self.imgHeight != vsH:
                    messagebox.showerror("错误", "图片高度不匹配，提取过程将添加噪声")
                    noise = True
                if self.imgWidth != vsW:
                    messagebox.showerror("错误", "图片宽度不匹配，提取过程将添加噪声")
                    noise = True

            # 创建recover图片数组、zero和one投票数组
            zero = []
            one = []
            recover = []
            for i in range(self.imgHeight):
                rowZero = []
                rowOne = []
                rowRecover = []
                for j in range(self.imgWidth):
                    rowZero.append(0)
                    rowOne.append(0)
                    rowRecover.append(-1)

                zero.append(rowZero)
                one.append(rowOne)
                recover.append(rowRecover)

            # 提取水印
            # 计算相关元组数量
            totalTup = 0
            markedTup = 0
            attributes = []
            for i in range(len(fixedFilds)):
                if check_vars[i].get():
                    attributes.append(fixedFilds[i])
            print('选择提取的属性为：' + str(attributes))
            # 属性分数
            af = int(EntryFoA.get())
            tuples = self.db_connection.getVPK(table, priKey)
            for tuple in tuples:
                consFact = 0
                totalTup = totalTup + 1
                flag = False
                if guessCheck:
                    if noise:
                        consFact = int(random.random() * tf)
                    else:
                        consFact = 0
                ID = tuple[0]
                VPK = tuple[1]
                if VPK % tf == consFact:
                    print("提取的元组ID为：" + str(ID))
                    for attribute in attributes:
                        attrValue = self.db_connection.getAttrValue(table, ID, attribute)
                        absAttr = abs(int(attrValue))
                        binAttr = bin(absAttr)[2:]
                        LSB = int(EntryLSB.get())
                        MSB = int(EntryMSB.get())
                        # 判断属性的二进制的长度是否符合
                        if len(binAttr) >= MSB + LSB:
                            # 去掉LSB的几位，得到aV
                            aV = absAttr >> LSB
                            tempString = str(ID) + priKey + str(aV)
                            hashValue = hashlib.md5(tempString.encode()).hexdigest()
                            hashValue2 = hashValue + priKey
                            # 计算aH
                            aH = int(hashlib.md5(hashValue2.encode()).hexdigest(), 16)
                            # 通过属性分数筛选属性
                            if aH % af == 0:
                                # 判断语句，避免出现lsb过长错误
                                if LSB * 2 < len(binAttr):
                                    # 计算嵌入水印的相应参数
                                    seedH = aH % (af + 1) + 1
                                    heightPos = Util.posHash(aH, self.imgHeight, seedH)
                                    seedW = aH % (af + 1) + 2
                                    widthPos = Util.posHash(aH, self.imgWidth, seedW)
                                    seedLSB = aH % (af + 1) + 3
                                    # 函数可能返回0值，而Pos是从1开始计数，因此值要加1
                                    LSBPos = Util.posHash(aH, LSB, seedLSB) + 1
                                    seedMSB = aH % (af + 1) + 4
                                    MSBPos = Util.posHash(aH, MSB, seedMSB) + 1
                                    # 噪声的处理
                                    if guessCheck and noise:
                                        LSBPos = int(random.random() * (len(binAttr) - 1)) + 1
                                        MSBPos = int(random.random() * (len(binAttr) - 1)) + 1
                                    # 判断语句 MSBpos的位置要比len-lsbpos的位置更靠左
                                    if (MSBPos + LSBPos) <= len(binAttr):
                                        msbValue = int(binAttr[MSBPos - 1])
                                        # 判断语句防止错误
                                        if (self.imgWidth * heightPos + widthPos) >= 0:
                                            lsbValue = int(binAttr[len(binAttr) - LSBPos])
                                            imageEle = msbValue ^ lsbValue
                                            # 投票机制
                                            if imageEle == 1:
                                                one[heightPos][widthPos] += 1
                                            else:
                                                zero[heightPos][widthPos] += 1

                                        flag = True
                                        print('提取的属性有：' + attribute
                                              + '属性值为：' + str(attrValue)
                                              + '提取的值：' + str(lsbValue)
                                              + '对应的像素值：' + str(imageEle)
                                              + '纵向位置为：' + str(heightPos)
                                              + '横向位置为：' + str(widthPos))
                if flag:
                    markedTup += 1

            EntryTotal2.delete(0, tk.END)
            EntryTotal2.insert(0, str(totalTup))

            EntryMarked.delete(0, tk.END)
            EntryMarked.insert(0, str(markedTup))

            perMark = markedTup / totalTup * 100
            EntryPct2.delete(0, tk.END)
            EntryPct2.insert(0, str(perMark))

            # 投票决定图片矩阵
            for i in range(self.imgHeight):
                for j in range(self.imgWidth):
                    # 若都为0，表示这个像素位置没有被嵌入
                    if one[i][j] != 0 or zero[i][j] != 0:
                        if one[i][j] > zero[i][j]:
                            recover[i][j] = 1
                        else:
                            recover[i][j] = 0

            # 计算提取的像素数量
            pixNum = 0
            for i in range(self.imgHeight):
                for j in range(self.imgWidth):
                    if recover[i][j] != -1:
                        pixNum += 1

            # 生成图片
            img = Image.new('RGB', (self.imgWidth, self.imgHeight))

            for i in range(self.imgHeight):
                for j in range(self.imgWidth):
                    if recover[i][j] == 1:
                        img.putpixel((j, i), ImageColor.getrgb('white'))
                    elif recover[i][j] == 0:
                        img.putpixel((j, i), ImageColor.getrgb('black'))
                    else:
                        img.putpixel((j, i), ImageColor.getrgb('red'))

            # 转换为 PhotoImage 对象，显示图片
            imgRes = img.resize((lbImg.winfo_width(), lbImg.winfo_height()),
                                Image.Resampling.LANCZOS)  # 测试多种抗锯齿方法
            imgTk = ImageTk.PhotoImage(imgRes)
            lbImg.config(image=imgTk)
            lbImg.image = imgTk

            # 显示像素的数量
            EntryTotal.delete(0, tk.END)
            EntryTotal.insert(0, str(self.imgWidth * self.imgHeight))
            EntryExt.delete(0, tk.END)
            EntryExt.insert(0, str(pixNum))
            pct1 = (pixNum * 100) / (self.imgWidth * self.imgHeight)
            EntryPct.delete(0, tk.END)
            EntryPct.insert(0, str(pct1))

            img.save('../../IMG/extracted.bmp')

        btnStart = tk.Button(self.root, text="开始", command=startWM)
        btnStart.place(x=10, y=370, width=100, height=40)

        # 退出
        def close_window():
            self.root.destroy()

        btnExit = tk.Button(self.root, text="关闭", command=close_window)
        btnExit.place(x=590, y=370, width=100, height=40)


if __name__ == "__main__":
    app = MyWMExtract()
    app.mainloop()
