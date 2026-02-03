import hashlib

import pymysql


class DBConnection:
    def __init__(self, server, user, password, database):
        try:
            self.conn = pymysql.connect(host=server,
                                        user=user,
                                        password=password,
                                        database=database,
                                        port=3306,
                                        charset='utf8')
            if self.conn is not None:
                print("You made it, take control your database now!")
            else:
                print("Failed to make connection!")
            self.cur = self.conn.cursor()

        except Exception as ex:
            print(ex)

    def getTableStructure(self, tableName):
        self.cur.execute(f"DESC `{tableName}`")
        result = self.cur.fetchall()
        return result

    def getConnection(self):
        return self.conn

    def myCommit(self):
        self.conn.commit()
        print("commit success!!")

    # 验证信号使用，获取所有元组的指定属性值和对应ID
    def getIndex(self, tableName, attr):
        # 构建 SQL 查询语句
        query = f"""
           SELECT ID, {attr} FROM {tableName};
           """
        # 执行查询
        self.cur.execute(query)
        return self.cur

    # 嵌入水印使用。获取所有元组的ID和虚拟主键VPK，返回列表
    def getVPK(self, tableName, priKey):
        # 构建 SQL 查询语句
        query = f"""
                   SELECT ID FROM {tableName};
                   """
        # 执行查询
        self.cur.execute(query)
        rows = self.cur.fetchall()
        results = []
        for row in rows:
            ID = row[0]
            tempString = str(ID) + priKey
            hashValue = hashlib.md5(tempString.encode()).hexdigest()
            hashValue2 = hashValue + priKey
            VPK = int(hashlib.md5(hashValue2.encode()).hexdigest(), 16)
            results.append((ID, VPK))
        return results

    # 嵌入水印使用。通过ID和属性名获取属性值，返回属性值的FLOAT变量
    def getAttrValue(self, tableName, ID, attr):
        # 构建 SQL 查询语句
        query = f"""
                    SELECT {attr} FROM {tableName} WHERE ID = {ID};
                    """
        # 执行查询
        self.cur.execute(query)
        row = self.cur.fetchone()
        if row is not None:
            attrValue = row[0]
            return attrValue
        else:
            return None

    def test(self):
        attr = 'ELEVATION'
        tableName = 'covertype_1000'
        ID = "2"
        query = f"""
                    SELECT {attr} FROM {tableName} WHERE ID = {ID};
                            """
        # 执行查询
        self.cur.execute(query)
        row = self.cur.fetchone()
        if row is not None:
            attrValue = row[0]
            print(attrValue)

    # Usage example
# if __name__ == "__main__":
#     db = DBConnection("localhost", "root", "123456", "covertype")
#     # 获取表结构
#     table_name = 'covertype_1000'
#     cursor = db.getIndex(table_name, "ELEVATION")
#
#     for row in cursor:
#         # 在这里处理每行数据
#         id_value = row[0]
#         attr_value = row[1]
#         print(f"ID: {id_value}, Attribute: {attr_value}")
#privKey, vsLength,