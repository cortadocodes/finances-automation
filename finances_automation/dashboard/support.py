import dash
import dash_core_components as dcc
import dash_html_components as html


def generate_html_table_from_dataframe(dataframe, columns=None, max_rows=500):
    columns = columns or dataframe.columns

    header = [html.Tr([html.Th(col) for col in columns])]
    body = [
        html.Tr([html.Td(dataframe.iloc[i][col]) for col in dataframe.columns])
        for i in range(min(len(dataframe), max_rows))
    ]

    return html.Table(header + body)
