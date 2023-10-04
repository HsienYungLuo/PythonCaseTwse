# 載入 #
import pandas as pd
import requests
# 暫時 #
import pymssql

# 載入connection模組
from GetSettings import Connection
from GetSettings import Model

#
from GetIsinTwseData import GetTwseList

#
#from DataBase import UpdataCompanyInformation

#   DB 設定。
_connectionSetting = []

#--- 00 取得設定參數 ---

#   設定檔案路徑與名稱。
_filePath = 'AppSettings.json'

#   取得設定。
try:
    #   取得 DB參數設定。
    _connectionSetting = Connection.GetDatabaseConnectionInfo(_filePath)

except FileNotFoundError as e:
    print(f"錯誤：{e}")
except ValueError as e:
    print(f"錯誤：{e}")
#--- End 00 取得設定參數 ---

#   DB參數測試
print(_connectionSetting.Server)

#   模式測試
ModelInfo = Model.GetModel(_filePath)
print(ModelInfo.Type)
#   強制某個狀態
ModelInfo = 2

#--- 01 取得 TWES資料 ---
twseResult = GetTwseList(ModelInfo)

#   列印測試
#for RowData in twseResult:
#    print(RowData)

#--- End 01 取得 TWES資料 ---

#--- 02 比照資料庫資料並寫入新資料。

#--- 03 取得資料庫股票列表。

#--- 04 取得個股一個月內資料並儲存於資料庫中。


#   暫時
conn = pymssql.connect(
    server = _connectionSetting.Server,
    user = _connectionSetting.User,
    password = _connectionSetting.Password,
    database = _connectionSetting.Database,
    as_dict = True
)

for RowData in twseResult:
    print(RowData[0].split('※')[0])
    
    

    #--- 02 查詢是否存在於資料庫中 ---
    sqlQuery = """Select ISIN_CODE
                    From COMPANY_INFORMATION
                    Where ISIN_CODE = %s;"""
    
    with conn.cursor() as cursor:
        #   執行查詢。
        cursor.execute(sqlQuery, RowData[1])

        row = cursor.fetchone()

        if cursor.fetchone() is not None:
            #   更新
            updateSql = """Update COMPANY_INFORMATION
                              Set SECURITIES_CODE = %s
                              Set TITLE = %s
                              Set TWSE_TYPE = %s
                              Set TWSE_DATE = %s
                            Where ISIN_CODE = %s;"""

            cursor.execute(updateSql, (RowData[0].split('※')[0], RowData[0].split('※')[1]), ModelInfo, RowData[2], RowData[1])
            conn.commit()

        else:
            #   新增
            inserSql = """Insert Into COMPANY_INFORMATION(ISIN_CODE, SECURITIES_CODE, TITLE, TWSE_TYPE, TWSE_DATE)
                          Values (%s, %s, %s, %s, %s);"""
            cursor.execute(inserSql, (RowData[1], RowData[0].split('※')[0], RowData[0].split('※')[1], ModelInfo, RowData[2]))
            conn.commit()

#------
