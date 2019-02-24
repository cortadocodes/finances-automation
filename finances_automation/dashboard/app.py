import dash
import dash_html_components as html

from finances_automation.command.view_table import view_table
from finances_automation.dashboard import support
from finances_automation.entities.table import Table


EXTERNAL_STYLESHEETS = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


def create_app(current_transactions_table):
    current_transactions = view_table(current_transactions_table, ['*'])

    app = dash.Dash('Finances Dashboard', external_stylesheets=EXTERNAL_STYLESHEETS)
    app.layout = html.Div(children=[
        html.H1('Balance'),
        support.generate_table(current_transactions)
    ])

    return app


if __name__ == '__main__':
    current_transactions_table = Table.get_from_config('current_transactions')
    app = create_app(current_transactions_table)
    app.run_server(debug=True)
