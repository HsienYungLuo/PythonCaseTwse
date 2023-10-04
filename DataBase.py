import pymssql

        

def UpdataCompanyInformation(connectionSetting ,twseResult):
        #   建立 Connection物件。
        conn = pymssql.connect(
            server = connectionSetting.Server,
            user = connectionSetting.User,
            password = connectionSetting.Password,
            database = connectionSetting.Database,
            as_dict = True
        )

        for RowData in twseResult:
            #--- 02 查詢是否存在於資料庫中 ---
            sql = """   Select ISIN_CODE
                          From COMPANY_INFORMATION
                         Where ISIN_CODE = %s;"""
            
            with conn.cursor() as cursor:

                #   執行查詢。
                cursor.execute(sql, RowData[1])

                row = cursor.fetchone()

                if cursor.fetchone() is not None:
                    #--- 03 - 1 更新已存在的資料 ---
                    print(f"更新 {RowData[1]}")
                else:
                    #--- 03 - 2 新增不存在的資料 ---
                    print(f"新增 {RowData[0]}")
                
        #   無回傳。


def UpdataCompany(companyInfo):
    #     

def AddCompany(companyInfo):
    #