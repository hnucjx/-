import tkinter as tk
from tkinter import ttk
from src.DB.DBConnection import DBConnection
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk, ImageColor
from src.utils.Util import Util
import datetime
import hashlib
import time

class MyWMEmbed():
    def __init__(self, db_connection):
        self.db_connection = db_connection
        #要用tk.Toplevel()而不是tk.TK()，否则会出现主窗口冲突
        self.root = tk.Toplevel()
        self.root.title('水印的嵌入')
        self.root.geometry("723x561")
        self.imgVector = []
        self.imgIcon = None
        self.oriImg = None
        self.imgWidth = 0
        self.imgHeight = 0

        self.myWMEmbed()
        self.root.mainloop()

    def myWMEmbed(self):
        # 选择要嵌入的表格
        lbRelationToMark = tk.Label(self.root, text="嵌入的数据库表格：")
        lbRelationToMark.place(x=10, y=11, width=110, height=14)
        valueRelationToMark = ["covertype_500", "covertype_1000", "covertype_2000", "covertype_3000", "covertype_10000", "covertype_15000"]
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
        EntryMSB.insert(0, "2")
        EntryMSB.place(x=257, y=35, width=37, height=20)

        # LSB
        lbLSB = tk.Label(self.root, text="LSB:")
        lbLSB.place(x=222, y=61, width=31, height=14)
        EntryLSB = tk.Entry(self.root)
        EntryLSB.delete(0, tk.END)
        EntryLSB.insert(0, "3")
        EntryLSB.place(x=257, y=58, width=37, height=20)

        # 元组分数
        lbFraction = tk.Label(self.root, text="元组分数：")
        lbFraction.place(x=10, y=60, width=110, height=14)
        EntryFraction = tk.Entry(self.root)
        EntryFraction.delete(0, tk.END)
        EntryFraction.insert(0, "1")
        EntryFraction.place(x=123, y=57, width=47, height=20)

        # 图片选择
        frameImage = tk.LabelFrame(self.root, width=204, height=232, text="嵌入的水印图像", labelanchor="n")
        frameImage.place(x=304, y=9)

        lbImg = tk.Label(frameImage, relief="groove", borderwidth=1)
        lbImg.place(x=10, y=13, width=184, height=164)

        def LoadImg():
            returnVal = filedialog.askopenfilename(title="水印的嵌入")
            if returnVal:
                imageFile = returnVal
                try:
                    self.imgVector.clear()
                    imageInfo = Image.open(imageFile)
                    imgRes = imageInfo.resize((lbImg.winfo_width(), lbImg.winfo_height()),
                                              Image.Resampling.LANCZOS)  # 测试多种抗锯齿方法
                    # 函数初始化时要定义imgIcon变量，否则运行完LoadImg方法会被回收，导致无法显示图片
                    self.imgIcon = ImageTk.PhotoImage(imgRes)
                    lbImg.configure(image=self.imgIcon)
                    Util.defineImageArray(imageFile)
                    self.oriImg = Util.getImageMatrix()
                    self.imgWidth = Util.getImageWidth()
                    self.imgHeight = Util.getImageHeight()
                    self.imgVector = Util.getImageVector()
                    EntryTotal.delete(0, tk.END)
                    EntryTotal.insert(0, str(self.imgWidth * self.imgHeight))
                    print(self.imgVector)
                    flag = 0
                    recover = []
                    for i in range(self.imgHeight):
                        rowRecover = []
                        for j in range(self.imgWidth):
                            k = self.imgVector[flag]
                            rowRecover.append(k)
                            flag += 1
                        recover.append(rowRecover)
                    img = Image.new('RGB', (self.imgWidth, self.imgHeight))

                    for i in range(self.imgHeight):
                        for j in range(self.imgWidth):
                            if recover[i][j] == 1:
                                img.putpixel((j, i), ImageColor.getrgb('white'))
                            elif recover[i][j] == 0:
                                img.putpixel((j, i), ImageColor.getrgb('black'))

                except FileNotFoundError:
                    messagebox.showerror("错误", "文件不存在")
                except Exception as e:
                    messagebox.showerror("错误", f"发送错误： {e}")

        btnLoadImg = tk.Button(frameImage, text="加载图像", command=LoadImg)
        btnLoadImg.place(x=9, y=180, width=186, height=23)

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

        fixedFilds = ["ELEVATION", "ASPECT", "SLOPE", "HOR_DIST_TO_HYDROLOGY", "VERT_DIST_TO_HYDROLOGY", "HOR_DIST_TO_ROADWAYS", "HILLSHADE_9AM",
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

        # 开始
        def startWM():
            currentTime = datetime.datetime.now()
            # 格式化时间为 "HH:mm:ss"
            formattedTime = currentTime.strftime("%H:%M:%S")
            print("PROCESS STARTED AT: " + formattedTime)
            # 记录开始时间
            startTime = time.time()

            #验证信号生成
            verSig = ['0' for _ in range(24)]
            # 元组分数
            tf = int(EntryFraction.get())
            # 属性分数
            af = int(EntryFoA.get())
            verSig = Util.buildVerifSignal(verSig, 8, tf)
            verSig = Util.buildVerifSignal(verSig, 16, self.imgHeight)
            verSig = Util.buildVerifSignal(verSig, 24, self.imgWidth)

            # 验证信号嵌入
            attrName = "ELEVATION"
            table = comboRelationToMark.get()
            priKey = EntryPri.get()
            cursor = self.db_connection.getIndex(table, attrName)
            numSign = False
            rows = cursor.fetchall()
            MAE = 0
            # 批量更新的语句
            sqlUpdate = "UPDATE {} SET {} = %s WHERE ID = %s".format(table, attrName)

            if BoolGue.get():
                for row in rows:
                    # 在这里处理每个元组的数据
                    ID = row[0]
                    attr = row[1]
                    tempString = str(ID) + priKey
                    hashValue = hashlib.md5(tempString.encode()).hexdigest()
                    hashValue2 = hashValue + priKey
                    index = int(hashlib.md5(hashValue2.encode()).hexdigest(), 16) % 24
                    if attr > 0:
                        numSign = True
                    # 转换成int类型去掉小数点，再转换成绝对值
                    absAttr = abs(int(attr))
                    # 修改LSB
                    absAttr = (absAttr >> 1) << 1
                    absAttr = absAttr | int(verSig[index])
                    if not numSign:
                        absAttr = -absAttr
                    numSign = False
                    # 执行更新操作
                    self.db_connection.cur.execute(sqlUpdate, (absAttr, ID))
                    print(ID)

                if self.db_connection.getConnection():
                    self.db_connection.myCommit()
                    print("验证信号嵌入成功")
                else:
                    print("数据库连接失败")

            # 水印嵌入
            # 记录嵌入的像素
            embed = []
            for i in range(self.imgHeight):
                rowEmbed = []
                for j in range(self.imgWidth):
                    rowEmbed.append(-1)

                embed.append(rowEmbed)
            # 计算相关元组数量
            totalTup = 0
            markedTup = 0

            attributes = []
            for i in range(len(fixedFilds)):
                if check_vars[i].get():
                    attributes.append(fixedFilds[i])
            print('选择嵌入的属性为：' + str(attributes))

            tuples = self.db_connection.getVPK(table, priKey)
            numSign2 = False
            # 处理每个元组
            for tuple in tuples:
                ID = tuple[0]
                VPK = tuple[1]
                totalTup += 1
                flag = False
                if VPK % tf == 0:
                    print("嵌入的元组ID为：" + str(ID))
                    for attribute in attributes:
                        attrValue = self.db_connection.getAttrValue(table, ID, attribute)
                        # 记录正负
                        if attrValue > 0:
                            numSign2 = True
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
                                    # 判断语句 MSBpos的位置要比len-lsbpos的位置更靠左
                                    if (MSBPos + LSBPos) <= len(binAttr):
                                        msbValue = int(binAttr[MSBPos - 1])
                                        # 判断语句防止错误
                                        if (self.imgWidth * heightPos + widthPos) >= 0:
                                            # 从图片矩阵的[heightPos][widthPos]位置获取像素值
                                            imageEle = self.imgVector[self.imgWidth * heightPos + widthPos]
                                            insertValue = msbValue ^ imageEle
                                            # 嵌入新的比特位，嵌入的位置为二进制串的第lsbpos位置上，从后往前数，从1开始计数
                                            # 创建一个只有 LSBPos 位置是1的 mask
                                            bitMask = 1 << (LSBPos - 1)
                                            # 将 LSBPos 位置清零
                                            newBin = absAttr & ~bitMask
                                            # 将 insertValue 插入到 LSBPos 位置
                                            newBin |= insertValue << (LSBPos - 1)
                                            # 减小数据失真的操作，可选项
                                            if BoolMD.get() and newBin != absAttr:
                                                minPos = EntryLsb2.get()
                                                newBin = Util.minDistortion(newBin, LSBPos, insertValue, minPos)
                                            # 加上正负号
                                            if not numSign2:
                                                realValue = -newBin
                                            else:
                                                realValue = newBin
                                            print('嵌入的属性有：' + attribute
                                                  + '原属性值：' + str(attrValue)
                                                  + '嵌入的值：' + str(insertValue)
                                                  + '修改后的值：' + str(realValue))
                                            # 计算MAE
                                            MAE = MAE + abs(realValue - attrValue)
                                            # 接下来是更新数据库操作
                                            # 批量更新的语句
                                            table = comboRelationToMark.get()
                                            sqlUpdate2 = "UPDATE {} SET {} = %s WHERE ID = %s".format(table, attribute)
                                            # 执行更新操作
                                            self.db_connection.cur.execute(sqlUpdate2, (realValue, ID))
                                            embed[heightPos][widthPos] = imageEle
                                            flag = True
                # 计算相关元组
                if flag:
                    markedTup += 1

            if self.db_connection.getConnection():
                self.db_connection.myCommit()
                print("水印嵌入成功")
            else:
                print("数据库连接失败")

            endTime = time.time()
            executionTime = endTime - startTime
            print(f"代码运行时间：{executionTime} 秒")

            embedded = 0
            for i in range(self.imgHeight):
                for j in range(self.imgWidth):
                    if embed[i][j] != -1:
                        embedded += 1

            # 计算MAE
            MAE = MAE / totalTup

            # 结果显示
            EntryDis.delete(0, tk.END)
            EntryDis.insert(0, str(MAE))

            EntryEbd.delete(0, tk.END)
            EntryEbd.insert(0, str(embedded))

            perEbd = embedded / int(EntryTotal.get()) * 100
            EntryPct.delete(0, tk.END)
            EntryPct.insert(0, str(perEbd))

            EntryTotal2.delete(0, tk.END)
            EntryTotal2.insert(0, str(totalTup))

            EntryMarked.delete(0, tk.END)
            EntryMarked.insert(0, str(markedTup))

            perMark = markedTup / totalTup * 100
            EntryPct2.delete(0, tk.END)
            EntryPct2.insert(0, str(perMark))


            # 图片显示
            img = Image.new('RGB', (self.imgWidth, self.imgHeight))

            for i in range(self.imgHeight):
                for j in range(self.imgWidth):
                    if embed[i][j] == 1:
                        img.putpixel((j, i), ImageColor.getrgb('white'))
                    elif embed[i][j] == 0:
                        img.putpixel((j, i), ImageColor.getrgb('black'))
                    else:
                        img.putpixel((j, i), ImageColor.getrgb('red'))

                    # 转换为 PhotoImage 对象，显示图片
                    imgRes = img.resize((lbEmbImg.winfo_width(), lbEmbImg.winfo_height()),
                                        Image.Resampling.LANCZOS)  # 测试多种抗锯齿方法
                    imgTk = ImageTk.PhotoImage(imgRes)
                    lbEmbImg.config(image=imgTk)
                    lbEmbImg.image = imgTk

            img.save('../../IMG/embed.bmp')

        btnStart = tk.Button(self.root, text="开始", command=startWM)
        btnStart.place(x=513, y=208, width=89, height=23)

        # 退出
        def close_window():
            self.root.destroy()

        btnExit = tk.Button(self.root, text="关闭", command=close_window)
        btnExit.place(x=609, y=208, width=89, height=23)

        # 嵌入效果
        frameResults = tk.LabelFrame(self.root, width=688, height=273, text="  水印嵌入的结果  ",
                                     labelanchor="n")
        frameResults.place(x=10, y=282)

        frameCap = tk.LabelFrame(frameResults, width=503, height=208, text="  嵌入的像素  ", labelanchor="n")
        frameCap.place(x=10, y=23)

        lbEmbImg = tk.Label(frameCap, relief="groove", borderwidth=1)
        lbEmbImg.place(x=10, y=10, width=184, height=164)

        lbTotal = tk.Label(frameCap, text="总数：", anchor="w")
        lbTotal.place(x=402, y=30, width=38, height=14)
        EntryTotal = tk.Entry(frameCap)
        EntryTotal.delete(0, tk.END)
        EntryTotal.insert(0, "0")
        EntryTotal.place(x=442, y=30, width=50, height=20)

        lbEbd = tk.Label(frameCap, text="已嵌入：", anchor="w")
        lbEbd.place(x=390, y=60, width=83, height=14)
        EntryEbd = tk.Entry(frameCap)
        EntryEbd.delete(0, tk.END)
        EntryEbd.insert(0, "0")
        EntryEbd.place(x=442, y=60, width=50, height=20)

        lbLine = tk.Label(frameCap, text="————————————————————————")
        lbLine.place(x=370, y=80, width=120, height=14)

        lbPct = tk.Label(frameCap, text="占比：", anchor="w")
        lbPct.place(x=402, y=95, width=83, height=14)
        EntryPct = tk.Entry(frameCap)
        EntryPct.delete(0, tk.END)
        EntryPct.insert(0, "0")
        EntryPct.place(x=442, y=95, width=50, height=20)

        # 像素值的注解
        frameExp = tk.LabelFrame(frameCap, width=150, height=75, text="  解释  ", labelanchor="n")
        frameExp.place(x=207, y=21)

        canvasR = tk.Canvas(frameExp, width=150, height=75)
        canvasR.pack()
        canvasR.create_rectangle(10, 5, 25, 20, fill="red")
        lbRed = tk.Label(frameExp, text="未嵌入的像素块", anchor="w")
        lbRed.place(x=30, y=5, width=95, height=14)

        lbLine2 = tk.Label(frameExp, text="————————————————————————", anchor="w")
        lbLine2.place(x=7, y=21, width=140, height=8)

        canvasR.create_rectangle(10, 35, 25, 50, fill="black")
        lbBlk = tk.Label(frameExp, text="嵌入的像素值 (1)", anchor="w")
        lbBlk.place(x=30, y=35, width=120, height=14)
        canvasR.create_rectangle(10, 55, 25, 70, fill="white")
        lbBlk = tk.Label(frameExp, text="嵌入的像素值 (0)", anchor="w")
        lbBlk.place(x=30, y=55, width=120, height=14)

        # 失真
        lbDis = tk.Label(frameCap, text="失真MAE值：", anchor="w")
        lbDis.place(x=220, y=130, width=80, height=14)
        EntryDis = tk.Entry(frameCap)
        EntryDis.delete(0, tk.END)
        EntryDis.insert(0, "0")
        EntryDis.place(x=300, y=130, width=50, height=20)

        # 标记的关系元组
        frameRelTup = tk.LabelFrame(frameResults, width=155, height=130, text="  相关的元组  ", labelanchor="n")
        frameRelTup.place(x=523, y=23)

        lbTotal2 = tk.Label(frameRelTup, text="总元组：", anchor="w")
        lbTotal2.place(x=36, y=15, width=59, height=14)
        EntryTotal2 = tk.Entry(frameRelTup)
        EntryTotal2.delete(0, tk.END)
        EntryTotal2.insert(0, "0")
        EntryTotal2.place(x=85, y=15, width=50, height=20)

        lbMarked = tk.Label(frameRelTup, text="标记的元组：", anchor="w")
        lbMarked.place(x=12, y=40, width=69, height=14)
        EntryMarked = tk.Entry(frameRelTup)
        EntryMarked.delete(0, tk.END)
        EntryMarked.insert(0, "0")
        EntryMarked.place(x=85, y=40, width=50, height=20)

        lbLine3 = tk.Label(frameRelTup, text="————————————————————————", anchor="w")
        lbLine3.place(x=20, y=62, width=120, height=8)

        lbPct2 = tk.Label(frameRelTup, text="占比：", anchor="w")
        lbPct2.place(x=47, y=75, width=59, height=14)
        EntryPct2 = tk.Entry(frameRelTup)
        EntryPct2.delete(0, tk.END)
        EntryPct2.insert(0, "0")
        EntryPct2.place(x=85, y=75, width=50, height=20)

        # 算法变形
        frameAlg = tk.LabelFrame(self.root, width=185, height=188, text="  算法拓展  ", labelanchor="n")
        frameAlg.place(x=513, y=9)

        BoolMD = tk.BooleanVar()
        BoolMD.set(0)
        cbMDis = tk.Checkbutton(frameAlg, text="低失真程度", variable=BoolMD, onvalue=1, offvalue=0)
        cbMDis.place(x=17, y=18, width=119, height=23)

        lbBits = tk.Label(frameAlg, text="Bits:", anchor="w")
        lbBits.place(x=21, y=57, width=52, height=14)

        EntryLsb2 = tk.Entry(frameAlg)
        EntryLsb2.delete(0, tk.END)
        EntryLsb2.insert(0, "0")
        EntryLsb2.place(x=60, y=55, width=26, height=20)

        cbLsb = tk.Checkbutton(frameAlg, text="LSB")
        cbLsb.place(x=95, y=53, width=52, height=23)

        lbFoA = tk.Label(frameAlg, text="属性分数：", anchor="w")
        lbFoA.place(x=25, y=90, width=120, height=14)
        EntryFoA = tk.Entry(frameAlg)
        EntryFoA.delete(0, tk.END)
        EntryFoA.insert(0, "1")
        EntryFoA.place(x=105, y=88, width=30, height=20)

        BoolGue = tk.BooleanVar()
        BoolGue.set(0)
        cbGue = tk.Checkbutton(frameAlg, text="值猜测惩罚引擎", variable=BoolGue, onvalue=1, offvalue=0)
        cbGue.place(x=15, y=128, width=145, height=23)


# if __name__ == "__main__":
#     app = MyWMEmbed()
#     app.mainloop()