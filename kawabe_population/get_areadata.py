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
        # https://pdfminersix.readthedocs.io/en/latest/api/composable.html#
        laparams = LAParams(
            all_texts=True,
        )
        rsrcmgr = PDFResourceManager()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
            layout = device.get_result()
            results = []
            print('objs-------------------------')
            get_objs(layout, results)
            return results


def adjust_data(results):
    results = sorted(results, key=lambda x:x['bbox'][1], reverse=True)
    data = {}
    for r in results:
        bbox = r['bbox']
        if bbox[1] > 680:
            continue
        if data.get(bbox[1]) is None:
            data[bbox[1]] = {}
        data[bbox[1]][bbox[0]] = r['text']
    texts = []
    for k,v  in data.items():
        lines = []
        data[k] = [ x[1] for x in sorted(data[k].items())]
        for t in data[k]:
            lines.extend(t.replace('\n', '').split(' '))
        texts.append(lines)
    datas = []
    for i in range(len(texts)//3):
        d1 = texts[i*3]
        d2 = texts[i*3+1]
        d3 = texts[i*3+2]
        if d2[0] == '計':
            break
        data = []
        data.append(d2[0])
        data.append(int(d1[0].replace('人', '').replace(',', '')))
        data.append(int(d1[1].replace('人', '').replace(',', '')))
        data.append(int(d1[2].replace('人', '').replace(',', '')))
        data.append(int(d1[3].replace('世帯', '').replace(',', '')))
        data.append(int(d3[0].replace('人', '').replace(',', '')))
        data.append(int(d3[1].replace('人', '').replace(',', '')))
        data.append(int(d3[2].replace('人', '').replace(',', '')))
        data.append(int(d3[3].replace('世帯', '').replace(',', '')))
        datas.append(data)
    return pd.DataFrame(datas, columns=['地区', '日本人男性', '日本人女性', '日本人', '日本人世帯数', '外国人男性', '外国人女性', '外国人', '外国人世帯数'])

def get_pdf_data(year, month):
    urlbase = 'https://www.kawabe-gifu.jp/wp-content/uploads'
    if year == 2015:
        url = '{}/2013/03/（掲示用）最新の地区別{}.pdf'.format(urlbase, 32 + month - 4)
    elif year == 2016 and month <=3:
        url = '{}/2013/03/（掲示用）最新の地区別{}.pdf'.format(urlbase, 40 + month)
    elif year == 2016 and month <=11:
        url = '{}/2013/03/（掲示用）最新の地区別-{}.pdf'.format(urlbase, month - 3)
    elif year == 2016:
        url = '{}/2013/03/（掲示用）最新の地区別-{}.pdf'.format(urlbase, month - 2)
    elif year == 2017 and month == 1:
        url = '{}/2013/03/（掲示用）最新の地区別-{}.pdf'.format(urlbase, 14)
    elif year == 2017 and month == 2:
        url = '{}/2013/03/（掲示用）最新の地区別-{}.pdf'.format(urlbase, 12)
    elif year == 2017:
        url = '{}/2013/03/（掲示用）最新の地区別-{}.pdf'.format(urlbase, 12 + month)
    elif year == 2018 and month == 1:
        url = '{}/{:04}/02/（掲示用）最新の地区別A.pdf'.format(urlbase, year)
    elif year == 2018 and month in [2, 3, 5]:
        url = '{}/{:04}/{:02}/（掲示用）最新の地区別-1.pdf'.format(urlbase, year, month)
    elif year == 2018 and month == 6:
        url = '{}/{:04}/{:02}/（掲示用）最新の地区別-1.pdf'.format(urlbase, year, month - 1)
    elif year == 2018:
        url = '{}/{:04}/{:02}/（掲示用）最新の地区別.pdf'.format(urlbase, year, month)
    elif year == 2019 and month == 1:
        url = '{}/{:04}/02/（掲示用）最新の地区別1.pdf'.format(urlbase, year)
    elif year == 2019 and month == 2:
        url = '{}/{:04}/{:02}/（掲示用）最新の地区別1.pdf'.format(urlbase, year, month)
    elif year == 2019:
        url = '{}/{:04}/{:02}/（掲示用）最新の地区別.pdf'.format(urlbase, year, month)
    elif year == 2020 and month == 5:
        url = '{}/{:04}/{:02}/TIKUBETU-1.pdf'.format(urlbase, year, month - 1)
    elif year >= 2020:
        url = '{}/{:04}/{:02}/TIKUBETU.pdf'.format(urlbase, year, month)
    print(url)
    r = requests.get(url)

    with open('tmp.pdf', 'wb') as f:
        f.write(r.content)

    result = read_pdf('tmp.pdf')
    df = adjust_data(result)
    df['確認日'] = datetime(year, month, 1)
    return df


def main():
    with sqlite3.connect('kawabe.sqlite3') as conn:
        # 最初のデータから取得する場合
        start = datetime(2015, 4, 1)
        end = datetime(2015, 4, 1)
        # start = datetime.now()
        # end = datetime.now()
        dt = start
        while dt <= end:
            year = dt.year
            month = dt.month

            print('========{}/{}========'.format(year, month))
            df = get_pdf_data(year, month)
            # df.to_sql('地区別人口', conn, if_exists='append')
            df.to_csv('地区別人口.csv')
            print(df)

            dt += relativedelta(months=1)



if __name__ == '__main__':
    main()
