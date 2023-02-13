import pymysql
import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
    req = requests.get('https://franchise.ftc.go.kr/mnu/00013/program/userRqst/list.do?searchCondition=&searchKeyword=&column=&selUpjong=&selIndus=&pageUnit=12300&pageIndex=1',
                       headers=header)

    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    notices = soup.select('#frm > table > tbody > tr')

    bun = []
    sang = []
    young = []
    dae = []
    deung = []
    choi = []
    eop = []

    for n in notices:
        bun.append(n.select_one("td:nth-child(1)").text.strip())
        sang.append(n.select_one("td:nth-child(2)").text.strip())
        young.append(n.select_one("td:nth-child(3)").text.strip())
        dae.append(n.select_one("td:nth-child(4)").text.strip())
        deung.append(n.select_one("td:nth-child(5)").text.strip())
        choi.append(n.select_one("td:nth-child(6)").text.strip())
        eop.append(n.select_one("td:nth-child(7)").text.strip())

    items = [item for item in zip(bun, sang, young, dae, deung, choi, eop)]

conn = pymysql.connect(
    user="root",
    passwd="0000",
    host="localhost",
    db="crawl_data",
    charset='utf8'
)

cursor = conn.cursor()

# 실행할 때마다 다른값이 나오지 않게 테이블을 제거해두기
cursor.execute("DROP TABLE IF EXISTS franchise_info")

# 테이블 생성하기
cursor.execute("CREATE TABLE franchise_info (번호 text,상호 text,영업표지 text,대표자 text,등록번호 text,최초등록일 text,업종 text)")

# 데이터 저장하기
for item in items:
    cursor.execute(
        f"INSERT INTO franchise_info VALUES(\"{item[0]}\",\"{item[1]}\",\"{item[2]}\",\"{item[3]}\",\"{item[4]}\",\"{item[5]}\",\"{item[6]}\")")

# 커밋하기
conn.commit()
# 연결종료하기
conn.close()
