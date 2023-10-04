#   取得資料；參考資料：https://blog.gtwang.org/programming/python-beautiful-soup-module-scrape-web-pages-tutorial/
from bs4 import BeautifulSoup
import requests

def __init__(Self, Mode):
        Self.Mode = Mode

def GetTwseList(Mode):

    url = f"http://isin.twse.com.tw/isin/C_public.jsp?strMode={Mode}"
    response = requests.get(url, verify = False)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    result = []
    #   選取器；尋找 table標籤並函 class = h4的區段。
    Table = soup.find("table", {"class" : "h4"})

    for Row in Table.find_all("tr"):
        RowData = []
        for Col in Row.find_all('td'):
            Col.attrs = {}
            #   轉換分割符號。
            RowData.append(Col.text.strip().replace('\u3000', '※'))
        
        if '※' in RowData[0]:
            result.append(RowData)
        else:
            pass # title 股票, 上市認購(售)權證, ...

    #   回傳結果。
    return result

#測試使用
#GetTwseList(1)
