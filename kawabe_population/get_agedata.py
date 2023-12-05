import requests
from pdfminer.high_level import extract_text
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import (
    LAParams,
    LTContainer,
    LTTextLine,
)
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import sqlite3

def get_objs(layout, results):
    if not isinstance(layout, LTContainer):
        return
    for obj in layout:
        if isinstance(obj, LTTextLine):
            results.append({'bbox': obj.bbox, 'text' : obj.get_text(), 'type' : type(obj)})
        get_objs(obj, results)


def read_pdf(path):
    with open(path, "rb") as f:
        parser = PDFParser(f)
        document = PDFDocument(parser)
        if not document.is_extractable:
            raise PDFTextExtractionNotAllowed
        laparams = LAParams(
            all_texts=True,
        )
        rsrcmgr = PDFResourceManager()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        data = []
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
            layout = device.get_result()
            results = []
            get_objs(layout, results)
            data.extend(adjust_data(results))
        return pd.DataFrame(data, columns=['年齢', '男性', '女性', '合計'])


def adjust_data(results):
    results = sorted(results, key=lambda x:x['bbox'][1], reverse=True)
    data = {}
    for r in results:
        bbox = r['bbox']
        y = int(bbox[1])
        if data.get(y):
            actual_y = y
        elif data.get(y - 1):
            actual_y = y - 1
        elif data.get(y + 1):
            actual_y = y + 1
        else:
            actual_y = y
            data[actual_y] = {}
        data[actual_y][bbox[0]] = r['text']
    for k, v in data.items():
        if len(v) < 2:
            continue
        data[k] = [x[1] for x in sorted(data[k].items(), key=lambda x:x[0])]

    datas = []
    for k, v in data.items():
        if type(v) is dict:
            continue
        if len(v) < 1:
            continue
        x = v[0].split(' ')
        if len(x) > 1:
            v[0] = x[0]
            for i in range(1, len(x)):
                v.insert(1, x[i])
        if len(v) < 2:
            continue
        x = v[1].split(' ')
        if len(x) > 1:
            v[1] = x[0]
            for i in range(1, len(x)):
                v.insert(2, x[i])
        if len(v) < 3:
            continue
        x = v[2].split(' ')
        if len(x) > 1:
            v[2] = x[0]
            for i in range(1, len(x)):
                v.insert(3, x[i])
        if len(v) < 4:
            continue
        x = v[3].split(' ')
        if len(x) > 1:
            v[3] = x[0]
            for i in range(1, len(x)):
                v.insert(4, x[i])
        if not v[0][0].isdigit():
            continue
        v[0] = v[0].replace('歳', '')
        v[0] = v[0].replace('以上', '')
        v[0] = v[0].replace('\n', '')
        v[1] = v[1].replace('人', '')
        v[1] = v[1].replace('\n', '')
        v[2] = v[2].replace('人', '')
        v[2] = v[2].replace('\n', '')
        v[3] = v[3].replace('人', '')
        v[3] = v[3].replace('\n', '')
        datas.append(v[:4])
    return datas


def get_pdf_data(year, month):
    urlbase = 'https://www.kawabe-gifu.jp/wp-content/uploads'
    if year == 2015 or (year == 2016 and month <= 3):
        url = '{}/2013/03/（掲示用）最新の年齢別{}.pdf'.format(urlbase, 21 + month)
    elif year == 2016 and month >= 4:
        url = '{}/2013/03/（掲示用）最新の年齢別-{}.pdf'.format(urlbase, month - 3)
    elif year == 2017 and month == 1:
        url = '{}/2013/03/（掲示用）最新の年齢別-{}.pdf'.format(urlbase, 18)
    elif year == 2017 and month == 2:
        url = '{}/2013/03/（掲示用）最新の年齢別-{}.pdf'.format(urlbase, 12)
    elif year == 2017 and month in [3, 4]:
        url = '{}/2013/03/（掲示用）最新の年齢別-{}.pdf'.format(urlbase, 16 + month - 3)
    elif year == 2017 and month >= 5:
        url = '{}/2013/03/（掲示用）最新の年齢別-{}.pdf'.format(urlbase, 16 + month - 2)
    elif year == 2018 and month == 1:
        url = '{}/{:04}/02/H30.1.1現在.pdf'.format(urlbase, year)
    elif year == 2018 and month in [2, 3]:
        url = '{}/{:04}/{:02}/（掲示用）最新の年齢別-{}.pdf'.format(urlbase, year, month, month - 1)
    elif year == 2018 and month in [6]:
        url = '{}/{:04}/{:02}/（掲示用）最新の年齢別-1.pdf'.format(urlbase, year, month - 1)
    elif year == 2018 and month in [11]:
        url = '{}/{:04}/{:02}/（掲示用）最新の年齢別-1.pdf'.format(urlbase, year, month)
    elif year == 2018:
        url = '{}/{:04}/{:02}/（掲示用）最新の年齢別.pdf'.format(urlbase, year, month)
    elif year == 2019 and month == 1:
        url = '{}/{:04}/02/（掲示用）最新の年齢別1.pdf'.format(urlbase, year, month)
    elif year == 2019:
        url = '{}/{:04}/{:02}/（掲示用）最新の年齢別.pdf'.format(urlbase, year, month)
    elif year == 2020 and month == 5:
        url = '{}/{:04}/{:02}/NENREIBETU-1.pdf'.format(urlbase, year, month - 1)
    elif year >= 2020:
        url = '{}/{:04}/{:02}/NENREIBETU.pdf'.format(urlbase, year, month)
    print(url)
    r = requests.get(url)

    with open('tmp.pdf', 'wb') as f:
        f.write(r.content)

    df = read_pdf('tmp.pdf')
    df['確認日'] = datetime(year, month, 1)
    return df


def main():
    with sqlite3.connect('kawabe.sqlite3') as conn:
        # 最初のデータから取得する場合
        start = datetime(2015, 4, 1)
        end = datetime.now()
        dt = start
        while dt <= end:
            year = dt.year
            month = dt.month

            print('========{}/{}========'.format(year, month))
            df = get_pdf_data(year, month)
            df.to_sql('年齢別人口', conn, if_exists='append')
            print(df)
            dt += relativedelta(months=1)



if __name__ == '__main__':
    main()
