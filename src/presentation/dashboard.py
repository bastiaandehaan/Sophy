# turtle_trader/presentation/dashboard.py
from datetime import datetime
from typing import Dict

import dash
from dash import dcc, html
from dash.dependencies import Input, Output

from utils.visualizer import Visualizer


class TradingDashboard:
    """Real-time dashboard for monitoring trading presentation"""

    def __init__(self, config: Dict[str, any], logger: any) -> None:
        self.config = config
        self.logger = logger
        self.app = dash.Dash(__name__)
        self._setup_layout()
        self._setup_callbacks()

    def _setup_layout(self) -> None:
        """Configure the dashboard layout"""
        self.app.layout = html.Div([
            html.H1("TurtleTrader Performance Dashboard"),

            html.Div([
                html.Div([
                    html.H3("Account Overview"),
                    dcc.Graph(id='equity-chart'),
                    html.Div(id='account-metrics')
                ], className='six columns'),

                html.Div([
                    html.H3("Trade History"),
                    dcc.Graph(id='trades-chart'),
                    html.Div(id='trade-metrics')
                ], className='six columns'),
            ], className='row'),

            html.Div([
                html.H3("Active Positions"),
                html.Div(id='positions-table')
            ]),

            dcc.Interval(
                id='interval-component',
                interval=5 * 1000,  # in milliseconds (5 seconds)
                n_intervals=0
            )
        ])

    def _setup_callbacks(self) -> None:
        """Set up dashboard update callbacks"""

        @self.app.callback(
            [Output('equity-chart', 'figure'),
             Output('account-metrics', 'children')],
            [Input('interval-component', 'n_intervals')]
        )
        def update_equity_chart(n):
            # Haal de laatste equity data op
            log_file = self.config['logging'].get('log_file', 'logs/trading_log.csv')
            visualizer = Visualizer(log_file)
            df = visualizer.load_trade_data()

            # Maak een figure voor de equity chart
            if df.empty or 'Type' not in df.columns:
                figure = {
                    'data': [],
                    'layout': {'title': 'Geen data beschikbaar'}
                }
            else:
                # Filter op STATUS entries
                status_df = df[df['Type'] == 'STATUS'].copy()

                # Extraheer balance data
                balances = []
                timestamps = []
                for _, row in status_df.iterrows():
                    comment = row['Comment']
                    timestamp = row['Timestamp']
                    if 'Balance: ' in comment:
                        balance_str = comment.split('Balance: ')[1].split(',')[0]
                        try:
                            balances.append(float(balance_str))
                            timestamps.append(timestamp)
                        except:
                            pass

                # Maak figuur
                figure = {
                    'data': [{'x': timestamps, 'y': balances, 'type': 'line', 'name': 'Account Balance'}],
                    'layout': {'title': 'Account Equity Curve'}
                }

            # Maak accountmetrics
            account_metrics = html.Div([
                html.P(f"Laatste update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"),
                html.P(f"Aantal trades: {len(df[df['Type'] == 'TRADE'])}")
            ])

            return figure, account_metrics

    # Fetch latest equity data and update chart
    # ...

    def run_server(self, debug: bool = False, port: int = 8050) -> None:
        """Start the dashboard server"""
        self.app.run_server(debug=debug, port=port)
