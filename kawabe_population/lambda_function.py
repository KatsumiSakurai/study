import sqlite3
from numpy import unique
import pandas as pd
import json
from datetime import datetime


def lambda_handler(event, context):
    with sqlite3.connect('kawabe.sqlite3') as conn:
        df = pd.read_sql('select * from 地区別人口', conn, index_col='index')
        df = df.sort_values('確認日')
        df = df.reset_index()

        # 地区別グラフデータ
        area_data = {}
        df['確認日'] = pd.to_datetime(df['確認日'])
        area_data['labels'] = list(unique(df['確認日'].dt.strftime('%Y/%m').values))
        area_data['datasets'] = []
        for area in unique(df['地区'].values):
            tdf = df[df['地区'] == area]
            tdf = tdf['日本人'] + tdf['外国人']
            area_data['datasets'].append({
                'type': 'line',
                'label': area,
                'data': [int(x) for x in list(tdf.astype('int').values)],
                'yAxisID': 'y-axis-1'
            })
        tdf = df.groupby('確認日').sum()
        tdf = tdf['日本人'] + tdf['外国人']
        area_data['datasets'].append({
            'type': 'line',
            'label': '全体',
            'data': [int(x) for x in list(tdf.astype('int').values)],
            'yAxisID': 'y-axis-1'
        })

        area_option = {
            'plugins': {
                'colorschemes': {
                    'scheme': 'brewer.Paired12'
                }
            },
            'title': {
                'display': True,
                'fontSize': 24,
                'text': '地区別人口推移'
            },
            'responsive': True,
            'scales': {
                'yAxes': [{
                    'id': 'y-axis-1',
                    'scaleLabel': {
                        'display': True,
                        'labelString': '人口(人)'
                    },
                    'type': 'linear',
                    'position': 'left',
                }]
            }
        }

        # 日本人、外国人別グラフデータ
        foreigner_data = {}
        foreigner_data['labels'] = list(unique(df['確認日'].dt.strftime('%Y/%m').values))
        foreigner_data['datasets'] = []
        tdf = df.groupby('確認日').sum()
        foreigner_data['datasets'].append({
            'type': 'line',
            'label': '日本人',
            'data': [int(x) for x in list(tdf['日本人'].astype('int').values)],
            'yAxisID': 'y-axis-1'
        })
        foreigner_data['datasets'].append({
            'type': 'line',
            'label': '外国人',
            'data': [int(x) for x in list(tdf['外国人'].astype('int').values)],
            'yAxisID': 'y-axis-1'
        })
        tdf = tdf['日本人'] + tdf['外国人']
        foreigner_data['datasets'].append({
            'type': 'line',
            'label': '全体',
            'data': [int(x) for x in list(tdf.astype('int').values)],
            'yAxisID': 'y-axis-1'
        })

        foreigner_option = {
            'plugins': {
                'colorschemes': {
                    'scheme': 'brewer.Paired12'
                }
            },
            'title': {
                'display': True,
                'fontSize': 24,
                'text': '日本人、外国人別人口推移'
            },
            'responsive': True,
            'scales': {
                'yAxes': [{
                    'id': 'y-axis-1',
                    'scaleLabel': {
                        'display': True,
                        'labelString': '人口(人)'
                    },
                    'type': 'linear',
                    'position': 'left',
                }]
            }
        }

        # 年齢別グラフデータ
        df = pd.read_sql('select * from 年齢別人口', conn, index_col='index')
        df = df.sort_values('確認日', ascending=False)
        df = df.reset_index()

        df['確認日'] = pd.to_datetime(df['確認日'])
        df['年齢'] = df['年齢'].astype(int)
        df['合計'] = df['合計'].astype(int)
        df['男性'] = df['男性'].astype(int)
        df['女性'] = df['女性'].astype(int)
        max_population = int(df['合計'].max())
        age_datas = []
        age_options = []
        for m in list(sorted(unique(df['確認日'].dt.strftime('%Y/%m').values), reverse=True)):
            year, month = m.split('/')
            print(year, month)
            print(datetime.now().year)
            if int(year) != datetime.now().year and month != '01':
                print('continue')
                continue
            age_data = {}
            age_option = {}

            tdf = df[df['確認日'] == m]
            tdf = tdf.sort_values('年齢')
            tdf = tdf.reset_index(drop=False)
            age_data['labels'] = [int(x) for x in list(tdf['年齢'].values)]
            # print(age_data['labels'])
            total = tdf['合計'].sum()

            age_data['datasets'] = []
            '''
            age_data['datasets'].append({
                'type': 'bar',
                'label': '全体',
                'data': [int(x) for x in list(tdf['合計'].astype('int').values)],
                'yAxisID': 'y-axis-1'
            })
            '''
            age_data['datasets'].append({
                'type': 'bar',
                'label': '男性',
                'data': [int(x) for x in list(tdf['男性'].values)],
                'yAxisID': 'y-axis-1'
            })
            age_data['datasets'].append({
                'type': 'bar',
                'label': '女性',
                'data': [int(x) for x in list(tdf['女性'].values)],
                'yAxisID': 'y-axis-1'
            })
    
            age_option = {
                'plugins': {
                    'colorschemes': {
                        'scheme': 'brewer.Paired12'
                    }
                },
                'title': {
                    'display': True,
                    'fontSize': 24,
                    'text': '{}年{}月年齢別人口({}人)'.format(year, month, total)
                },
                'responsive': True,
                'scales': {
                    'xAxes': [{
                        'stacked': True,
                        'categoryPercentage': 0.9,
                        'barPercentage': 0.9,
                        'ticks': {
                            'maxTicksLimit': 10,
                        }
                    }],
                    'yAxes': [{
                        'stacked': True,
                        'id': 'y-axis-1',
                        'scaleLabel': {
                            'display': True,
                            'labelString': '人口(人)'
                        },
                        'type': 'linear',
                        'position': 'left',
                        'ticks': {
                            'beginAtZero': True,
                            'min': 0,
                            'max': max_population
                        }
                    }]
                }
            }
            age_datas.append(age_data)
            age_options.append(age_option)

        '''
        # 年齢別グラフデータ
        df = pd.read_sql('select * from 年齢別人口', conn, index_col='index')
        df = df.sort_values('確認日')
        df = df.reset_index()

        df['確認日'] = pd.to_datetime(df['確認日'])
        df['年齢'] = df['年齢'].astype(int)
        df['合計'] = df['合計'].astype(int)
        df['男性'] = df['男性'].astype(int)
        df['女性'] = df['女性'].astype(int)
        max_population = int(df['合計'].max())
        age_data2 = {}
        age_option2 = {}
        age_data2['labels'] = list(unique(df['確認日'].dt.strftime('%Y/%m').values))
        age_data2['datasets'] = []
        for m in list(unique(df['確認日'].dt.strftime('%Y/%m').values)):
            tdf = df[df['確認日'] == m]
            for a in tdf['年齢'].values:
                age_data2['datasets'].append({
                    'type': 'bar',
                    'label': int(a),
                    'data': [int(x) for x in list(tdf['合計'].values)],
                    'yAxisID': 'y-axis-1'
                })

        age_option2 = {
            'plugins': {
                'colorschemes': {
                    'scheme': 'brewer.Paired12'
                }
            },
            'title': {
                'display': True,
                'fontSize': 24,
                'text': '年齢別人口推移'
            },
            'responsive': True,
            'scales': {
                'yAxes': [{
                    'id': 'y-axis-1',
                    'scaleLabel': {
                        'display': True,
                        'labelString': '人口(人)'
                    },
                    'type': 'linear',
                    'position': 'left',
                }]
            }
        }
        '''

    jarea_data = json.dumps(area_data)
    jarea_option = json.dumps(area_option)
    jforeigner_data = json.dumps(foreigner_data)
    jforeigner_option = json.dumps(foreigner_option)
    jage_datas = json.dumps(age_datas)
    jage_options = json.dumps(age_options)
    # jage_data2 = json.dumps(age_data2)
    # jage_option2 = json.dumps(age_option2)

    html = '''
<html>
<head>
  <meta http-equiv="content-type" charset="utf-8">
  <title>川辺町地区別人口推移</title>
  <script src="https://code.jquery.com/jquery-3.3.1.js"></script>
  <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.2/Chart.min.js"></script>
  <script src="https://unpkg.com/chartjs-plugin-colorschemes"></script>
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
  <script>
  $(function() {{
    let population = document.getElementById("population");
    let population_graph = new Chart(population, {{
       type: 'bar',
       data: JSON.parse('{}'),
       options: JSON.parse('{}')
    }});
    let foreigner = document.getElementById("foreigner");
    let foreigner_graph = new Chart(foreigner, {{
       type: 'bar',
       data: JSON.parse('{}'),
       options: JSON.parse('{}')
    }});

    let age_datas = JSON.parse('{}')
    let age_options = JSON.parse('{}')
    for (var i = 0; i < age_datas.length; i++) {{
        age_data = age_datas[i];
        age_option = age_options[i];

        $('#age_div').append('<div class="col-12 col-xl-6"><canvas id="age_' + i + '"></canvas></div>');
        let age_canvas = document.getElementById('age_' + i);
        let age_graph = new Chart(age_canvas, {{
            type: 'bar',
            data: age_data,
            options: age_option
        }});
    }}
  }});
  </script>
</head>
<body>
<h1>川辺町人口推移</h1>
<div class="container-fluid">
  <div class="row">
    <div class="col-12 col-xl-6">
      <canvas id="population"></canvas>
    </div>
    <div class="col-12 col-xl-6">
      <canvas id="foreigner"></canvas>
    </div>
  </div>
  <div class="row" id="age_div">
  </div>
</div>
</body>
</html>
    '''.format(jarea_data, jarea_option, jforeigner_data, jforeigner_option, jage_datas, jage_options)

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html',
        },
        'body': html,
    }

if __name__ == '__main__':
    lambda_handler(None, None)
