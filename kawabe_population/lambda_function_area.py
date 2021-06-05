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
        area_datas = []
        area_options = []

        df['確認日'] = pd.to_datetime(df['確認日'])
        for area in unique(df['地区'].values):
            area_data = {}
            area_data['labels'] = list(unique(df['確認日'].dt.strftime('%Y/%m').values))
            tdf = df[df['地区'] == area]
            tdf = tdf['日本人'] + tdf['外国人']
            area_data['datasets'] = [{
                'type': 'line',
                'label': area,
                'data': [int(x) for x in list(tdf.astype('int').values)],
                'yAxisID': 'y-axis-1'
            }]
            area_option = {
                'plugins': {
                    'colorschemes': {
                        'scheme': 'brewer.Paired12'
                    }
                },
                'title': {
                    'display': False,
                    'fontSize': 24,
                    'text': f'{area}の人口推移'
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
            area_datas.append(area_data)
            area_options.append(area_option)

        area_data = {}
        area_data['labels'] = list(unique(df['確認日'].dt.strftime('%Y/%m').values))
        tdf = df.groupby('確認日').sum()
        tdf = tdf['日本人'] + tdf['外国人']
        area_data['datasets'] = [{
            'type': 'line',
            'label': '川辺町全体',
            'data': [int(x) for x in list(tdf.astype('int').values)],
            'yAxisID': 'y-axis-1'
        }]
        area_option = {
            'plugins': {
                'colorschemes': {
                    'scheme': 'brewer.Paired12'
                }
            },
            'title': {
                'display': False,
                'fontSize': 24,
                'text': f'川辺町全体の人口推移'
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
        area_datas.append(area_data)
        area_options.append(area_option)

    jarea_datas = json.dumps(area_datas)
    jarea_options = json.dumps(area_options)

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
    let area_datas = JSON.parse('{}')
    let area_options = JSON.parse('{}')
    for (var i = 0; i < area_datas.length; i++) {{
        area_data = area_datas[i];
        area_option = area_options[i];

        $('#area_div').append('<div class="col-6 col-xl-4"><canvas id="area_' + i + '"></canvas></div>');
        let area_canvas = document.getElementById('area_' + i);
        let area_graph = new Chart(area_canvas, {{
            type: 'bar',
            data: area_data,
            options: area_option
        }});
    }}
  }});
  </script>
</head>
<body>
<h1>川辺町地区別人口推移</h1>
<div class="container-fluid">
  <div class="row" id="area_div">
  </div>
</div>
</body>
</html>
    '''.format(jarea_datas, jarea_options)

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html',
        },
        'body': html,
    }

if __name__ == '__main__':
    lambda_handler(None, None)
