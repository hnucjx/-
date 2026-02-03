import hashlib
from PIL import Image
from PIL import ImageOps
import numpy as np
import os

class Util:
    imageFile = None
    matrixWidth = 0
    matrixHeight = 0
    pixelMatrix = None
    vector = []

    @staticmethod
    def clearImage():
        Util.vector.clear()
        Util.pixelMatrix = None

    @staticmethod
    def getImageMatrix():
        return Util.pixelMatrix

    @staticmethod
    def getImageWidth():
        return Util.matrixWidth

    @staticmethod
    def getImageHeight():
        return Util.matrixHeight

    @staticmethod
    def getImageVector():
        return Util.vector

    @staticmethod
    def getPixelMatrix():
        return Util.pixelMatrix

    @staticmethod
    def getMatrixFromImageFile(imgFile):
        try:
            Util.imageFile = imgFile
            img = Image.open(Util.imageFile)
            img = ImageOps.grayscale(img)
            Util.matrixWidth, Util.matrixHeight = img.size
            # 先转换为灰度图
            imgGray = img.convert('L')
            # 转换为Numpy数组
            imgTemp = np.array(imgGray)
            # 使用阈值处理
            Util.pixelMatrix = np.where(imgTemp > 120, 1, 0).tolist()
        except Exception as e:
            raise e

    @staticmethod
    def defineImageArray(imgFile):
        Util.getMatrixFromImageFile(imgFile)
        for y in range(Util.matrixHeight):
            for x in range(Util.matrixWidth):
                Util.vector.append(Util.pixelMatrix[y][x])

    @staticmethod
    def buildVerifSignal(arr, pos, num):
        bin_ft = bin(num)[2:]  # 将整数转换为二进制字符串，去掉前缀"0b"
        pos_bin = 0
        for i in range(pos - len(bin_ft), pos):
            arr[i] = bin_ft[pos_bin]
            pos_bin += 1
        return arr

    @staticmethod
    def buildParamVal(One, Zero, pos):
        start = pos - 8
        final = ['0' for _ in range(8)]
        flag = 0
        for i in range(start, pos):
            if One[i] > Zero[i]:
                final[flag] = '1'
            else:
                final[flag] = '0'
            flag += 1
        result = "".join(final)
        return int(result, 2)


    @staticmethod
    def posHash(value, bucket, seed):
        comString = str(value) + str(seed)
        hashValue = int(hashlib.md5(comString.encode()).hexdigest(), 16)
        result = hashValue % bucket
        return result

    @staticmethod
    def minDistortion(newBin, lsbpos, insertValue, minPos):
        # 二进制形式
        binStr = bin(newBin)[2:]
        counter = 0
        # 循环从二进制串的第lsbpos位的后一位开始，即嵌入比特的位置的后一位，一直到最后一位
        for i in range(len(binStr) - lsbpos + 1, len(binStr)):
            # 如果这一位的值，和新嵌入的value相同，就将其反转
            if int(binStr[i]) == insertValue:
                # 使用位运算
                newBin ^= 1 << (len(binStr) - i - 1)
                counter += 1
                # 如果反转的次数达到上限pos，就退出循环。如果传入的pos是0，则永远不会触发以下这个判断语句，即会走完整个循环，将失真降到最低
                if counter == minPos:
                    break
        return newBin