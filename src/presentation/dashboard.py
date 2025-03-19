# src/presentation/dashboard.py
from datetime import datetime
from typing import Dict, List, Any, Optional

import dash
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots

from src.utils.logger import Logger
from src.utils.visualizer import Visualizer


class TradingDashboard:
    """
    Enhanced real-time dashboard for monitoring trading performance and FTMO compliance.

    Features:
    - Real-time equity curve monitoring
    - Trade history visualization
    - FTMO compliance tracking
    - Performance metrics
    - Symbol-specific analysis
    - Active positions monitoring
    """

    def __init__(self, config: Dict[str, Any], logger: Logger) -> None:
        """
        Initialize the trading dashboard.

        Args:
            config: Configuration dictionary
            logger: Logger instance for the dashboard
        """
        self.config = config
        self.logger = logger

        # Configuration for the dashboard
        self.log_file = config["logging"].get("log_file", "logs/trading_log.csv")
        self.update_interval = config.get("dashboard", {}).get(
            "update_interval", 5
        )  # in seconds
        self.max_trades_to_display = config.get("dashboard", {}).get("max_trades", 100)
        self.theme = config.get("dashboard", {}).get("theme", "light")

        # Initialize the dashboard
        self.app = dash.Dash(
            __name__,
            title="Sophy Trading Dashboard",
            update_title=None,
            suppress_callback_exceptions=True,
            external_stylesheets=[
                "https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css",
                "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css",
            ],
        )

        # Setup dashboard layout
        self._setup_layout()

        # Setup callbacks for interactive elements
        self._setup_callbacks()

        # Create visualizer
        output_dir = config.get("output", {}).get("data_dir", "data")
        self.visualizer = Visualizer(self.log_file, output_dir)

        # FTMO parameters
        self.ftmo_config = {
            "profit_target": config.get("risk", {}).get("profit_target", 0.10),
            "daily_drawdown_limit": config.get("risk", {}).get(
                "daily_drawdown_limit", 0.05
            ),
            "total_drawdown_limit": config.get("risk", {}).get(
                "total_drawdown_limit", 0.10
            ),
            "min_trading_days": config.get("risk", {}).get("min_trading_days", 4),
            "initial_balance": config.get("risk", {}).get("initial_balance", 100000),
        }

        self.logger.info("Trading dashboard initialized")

    def _setup_layout(self) -> None:
        """Configure the dashboard layout with all components."""
        # Set custom color theme
        if self.theme == "dark":
            colors = {
                "background": "#222222",
                "text": "#FFFFFF",
                "grid": "#333333",
                "profit": "#00FF00",
                "loss": "#FF0000",
                "panel": "#2d3038",
            }
        else:
            colors = {
                "background": "#F8F9FA",
                "text": "#333333",
                "grid": "#DDDDDD",
                "profit": "#28A745",
                "loss": "#DC3545",
                "panel": "#FFFFFF",
            }

        # Define navigation tabs
        tabs = dcc.Tabs(
            id="tabs",
            value="tab-overview",
            children=[
                dcc.Tab(label="Overview", value="tab-overview"),
                dcc.Tab(label="Trade History", value="tab-trade-history"),
                dcc.Tab(label="Symbol Analysis", value="tab-symbol-analysis"),
                dcc.Tab(label="FTMO Compliance", value="tab-ftmo"),
                dcc.Tab(label="Settings", value="tab-settings"),
            ],
            colors={
                "border": colors["grid"],
                "primary": "#007BFF",
                "background": colors["background"],
            },
        )

        # Main layout structure
        self.app.layout = html.Div(
            [
                # Header
                html.Div(
                    [
                        html.H1("Sophy Trading Dashboard", className="display-4"),
                        html.Div(
                            [
                                html.Span(id="current-time", className="mr-3"),
                                html.Span(
                                    id="connection-status",
                                    className="badge badge-success mr-3",
                                ),
                                html.Span(id="balance-display", className="mr-3"),
                                html.Span(id="equity-display", className="mr-3"),
                                html.Span(id="daily-pl-display"),
                            ],
                            className="d-flex align-items-center",
                        ),
                    ],
                    className="jumbotron py-4",
                ),
                # Navigation tabs
                tabs,
                # Content area for each tab
                html.Div(id="tab-content", className="mt-3"),
                # Hidden data stores for sharing between callbacks
                dcc.Store(id="trade-data-store"),
                dcc.Store(id="account-data-store"),
                dcc.Store(id="position-data-store"),
                # Update interval
                dcc.Interval(
                    id="update-interval",
                    interval=self.update_interval * 1000,  # Convert to milliseconds
                    n_intervals=0,
                ),
                # Footer
                html.Footer(
                    [
                        html.Div(
                            [
                                html.Span(
                                    "Sophy Trading System © 2025",
                                    className="text-muted",
                                )
                            ],
                            className="container text-center py-3",
                        )
                    ]
                ),
            ],
            style={
                "backgroundColor": colors["background"],
                "color": colors["text"],
                "minHeight": "100vh",
            },
        )

    def _setup_callbacks(self) -> None:
        """Set up all callbacks for interactive elements."""

        # Update data stores
        @self.app.callback(
            [
                Output("trade-data-store", "data"),
                Output("account-data-store", "data"),
                Output("position-data-store", "data"),
                Output("current-time", "children"),
                Output("connection-status", "children"),
                Output("connection-status", "className"),
                Output("balance-display", "children"),
                Output("equity-display", "children"),
                Output("daily-pl-display", "children"),
            ],
            [Input("update-interval", "n_intervals")],
        )
        def update_data_stores(n):
            """Update all data stores with latest information."""
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            try:
                # Load trade data
                df = self.visualizer.load_trade_data()

                if df.empty:
                    # No data available
                    return (
                        {},
                        {},
                        {},
                        current_time,
                        "Disconnected",
                        "badge badge-danger",
                        "Balance: N/A",
                        "Equity: N/A",
                        "Daily P&L: N/A",
                    )

                # Process trade data
                trade_data = self._process_trade_data(df)

                # Process account data
                account_data = self._process_account_data(df)

                # Process position data
                position_data = self._process_position_data(df)

                # Prepare header displays
                balance = account_data.get("current_balance", 0)
                equity = account_data.get("current_equity", balance)
                daily_pl = account_data.get("daily_pl", 0)

                balance_display = f"Balance: ${balance:,.2f}"
                equity_display = f"Equity: ${equity:,.2f}"

                daily_pl_class = "text-success" if daily_pl >= 0 else "text-danger"
                daily_pl_display = html.Span(
                    f"Daily P&L: ${daily_pl:,.2f} ({daily_pl / account_data.get('initial_balance', 100000) * 100:.2f}%)",
                    className=daily_pl_class,
                )

                # Return all updated data
                return (
                    trade_data,
                    account_data,
                    position_data,
                    current_time,
                    "Connected",
                    "badge badge-success",
                    balance_display,
                    equity_display,
                    daily_pl_display,
                )

            except Exception as e:
                self.logger.error(f"Error updating data stores: {e}")
                return (
                    {},
                    {},
                    {},
                    current_time,
                    "Error",
                    "badge badge-warning",
                    "Balance: Error",
                    "Equity: Error",
                    "Daily P&L: Error",
                )

        # Tab content callback
        @self.app.callback(
            Output("tab-content", "children"),
            [
                Input("tabs", "value"),
                Input("trade-data-store", "data"),
                Input("account-data-store", "data"),
                Input("position-data-store", "data"),
            ],
        )
        def render_tab_content(tab, trade_data, account_data, position_data):
            """Render content for the selected tab."""
            if tab == "tab-overview":
                return self._render_overview_tab(
                    trade_data, account_data, position_data
                )
            elif tab == "tab-trade-history":
                return self._render_trade_history_tab(trade_data)
            elif tab == "tab-symbol-analysis":
                return self._render_symbol_analysis_tab(trade_data)
            elif tab == "tab-ftmo":
                return self._render_ftmo_tab(account_data, trade_data)
            elif tab == "tab-settings":
                return self._render_settings_tab()
            return html.Div("Content not available")

        # Symbol selection callback for symbol analysis tab
        @self.app.callback(
            [
                Output("symbol-equity-graph", "figure"),
                Output("symbol-trades-table", "children"),
            ],
            [Input("symbol-dropdown", "value"), Input("trade-data-store", "data")],
        )
        def update_symbol_analysis(selected_symbol, trade_data):
            """Update symbol-specific analysis based on selection."""
            if not trade_data or not selected_symbol:
                # Return empty figure if no data or no symbol selected
                empty_fig = go.Figure()
                empty_fig.update_layout(
                    title="No symbol selected or no data available",
                    xaxis_title="Date",
                    yaxis_title="Value",
                )
                return empty_fig, html.Div("No data available")

            # Filter trades for selected symbol
            symbol_trades = [
                trade
                for trade in trade_data.get("trades", [])
                if trade.get("symbol") == selected_symbol
            ]

            if not symbol_trades:
                empty_fig = go.Figure()
                empty_fig.update_layout(
                    title=f"No trades for {selected_symbol}",
                    xaxis_title="Date",
                    yaxis_title="Value",
                )
                return empty_fig, html.Div(f"No trades found for {selected_symbol}")

            # Create equity curve for the symbol
            cumulative_pnl = np.cumsum(
                [trade.get("profit_loss", 0) for trade in symbol_trades]
            )
            trade_dates = [
                trade.get("close_time", datetime.now()) for trade in symbol_trades
            ]

            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=trade_dates,
                    y=cumulative_pnl,
                    mode="lines+markers",
                    name="Cumulative P&L",
                    line=dict(color="blue", width=2),
                )
            )

            fig.update_layout(
                title=f"Symbol Equity Curve: {selected_symbol}",
                xaxis_title="Date",
                yaxis_title="Cumulative P&L ($)",
                height=500,
            )

            # Create trade table
            trades_table = self._create_trade_table(symbol_trades)

            return fig, trades_table

    def _render_overview_tab(
        self, trade_data: Dict, account_data: Dict, position_data: Dict
    ) -> html.Div:
        """
        Render content for the overview tab.

        Args:
            trade_data: Processed trade data
            account_data: Processed account data
            position_data: Processed position data

        Returns:
            Dash component with tab content
        """
        # Create equity curve
        equity_curve_fig = self._create_equity_curve(account_data)

        # Create drawdown chart
        drawdown_fig = self._create_drawdown_chart(account_data)

        # Create performance metrics cards
        metrics_cards = self._create_metrics_cards(trade_data, account_data)

        # Create active positions table
        positions_table = self._create_positions_table(position_data)

        # Create recent trades table
        recent_trades = trade_data.get("trades", [])[:5]  # Get most recent 5 trades
        recent_trades_table = self._create_trade_table(recent_trades, "Recent Trades")

        # Combine all components for the overview tab
        return html.Div(
            [
                # Top row: Equity curve and drawdown
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dcc.Graph(
                                            id="equity-curve-graph",
                                            figure=equity_curve_fig,
                                            config={"displayModeBar": False},
                                        )
                                    ],
                                    className="card-body",
                                )
                            ],
                            className="card mb-4",
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dcc.Graph(
                                            id="drawdown-graph",
                                            figure=drawdown_fig,
                                            config={"displayModeBar": False},
                                        )
                                    ],
                                    className="card-body",
                                )
                            ],
                            className="card mb-4",
                        ),
                    ]
                ),
                # Second row: Performance metrics
                html.Div([metrics_cards], className="mb-4"),
                # Third row: Active positions and recent trades
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H5(
                                            "Active Positions", className="card-title"
                                        ),
                                        positions_table,
                                    ],
                                    className="card-body",
                                )
                            ],
                            className="card mb-4 col-md-6",
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H5(
                                            "Recent Trades", className="card-title"
                                        ),
                                        recent_trades_table,
                                    ],
                                    className="card-body",
                                )
                            ],
                            className="card mb-4 col-md-6",
                        ),
                    ],
                    className="row",
                ),
            ]
        )

    def _render_trade_history_tab(self, trade_data: Dict) -> html.Div:
        """
        Render content for the trade history tab.

        Args:
            trade_data: Processed trade data

        Returns:
            Dash component with tab content
        """
        trades = trade_data.get("trades", [])

        # Create filters for the trade table
        filters = html.Div(
            [
                html.Div(
                    [
                        html.Label("Filter by Symbol:"),
                        dcc.Dropdown(
                            id="trade-symbol-filter",
                            options=[
                                {"label": symbol, "value": symbol}
                                for symbol in trade_data.get("symbols", [])
                            ],
                            multi=True,
                            placeholder="Select symbols...",
                        ),
                    ],
                    className="col-md-4",
                ),
                html.Div(
                    [
                        html.Label("Filter by Direction:"),
                        dcc.Dropdown(
                            id="trade-direction-filter",
                            options=[
                                {"label": "BUY", "value": "BUY"},
                                {"label": "SELL", "value": "SELL"},
                            ],
                            multi=True,
                            placeholder="Select directions...",
                        ),
                    ],
                    className="col-md-4",
                ),
                html.Div(
                    [
                        html.Label("Filter by Result:"),
                        dcc.Dropdown(
                            id="trade-result-filter",
                            options=[
                                {"label": "Profitable", "value": "profit"},
                                {"label": "Loss", "value": "loss"},
                            ],
                            multi=True,
                            placeholder="Select results...",
                        ),
                    ],
                    className="col-md-4",
                ),
            ],
            className="row mb-4",
        )

        # Create trade analysis graphs
        trade_analysis = html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(
                                    id="trade-pnl-graph",
                                    figure=self._create_trade_pnl_graph(trades),
                                    config={"displayModeBar": False},
                                )
                            ],
                            className="card-body",
                        )
                    ],
                    className="card mb-4 col-md-6",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(
                                    id="trade-distribution-graph",
                                    figure=self._create_trade_distribution_graph(
                                        trades
                                    ),
                                    config={"displayModeBar": False},
                                )
                            ],
                            className="card-body",
                        )
                    ],
                    className="card mb-4 col-md-6",
                ),
            ],
            className="row mb-4",
        )

        # Create full trade history table
        trade_table = self._create_trade_table(trades, "Trade History")

        return html.Div(
            [
                # Filters
                filters,
                # Trade analysis
                trade_analysis,
                # Trade history table
                html.Div(
                    [
                        html.Div(
                            [
                                html.H5(
                                    "Complete Trade History", className="card-title"
                                ),
                                trade_table,
                            ],
                            className="card-body",
                        )
                    ],
                    className="card mb-4",
                ),
            ]
        )

    def _render_symbol_analysis_tab(self, trade_data: Dict) -> html.Div:
        """
        Render content for the symbol analysis tab.

        Args:
            trade_data: Processed trade data

        Returns:
            Dash component with tab content
        """
        # Symbol selection dropdown
        symbol_dropdown = dcc.Dropdown(
            id="symbol-dropdown",
            options=[
                {"label": symbol, "value": symbol}
                for symbol in trade_data.get("symbols", [])
            ],
            value=(
                trade_data.get("symbols", [""])[0]
                if trade_data.get("symbols", [])
                else None
            ),
            placeholder="Select a symbol...",
            className="mb-4",
        )

        # Empty figure for initial state
        empty_fig = go.Figure()
        empty_fig.update_layout(
            title="Select a symbol to view equity curve",
            xaxis_title="Date",
            yaxis_title="Value",
        )

        # Symbol performance metrics
        symbol_metrics = self._create_symbol_metrics(trade_data)

        return html.Div(
            [
                # Symbol selection
                html.Div(
                    [html.Label("Select Symbol for Analysis:"), symbol_dropdown],
                    className="mb-4",
                ),
                # Symbol performance summary
                html.Div(
                    [
                        html.Div(
                            [
                                html.H5("Symbol Performance", className="card-title"),
                                symbol_metrics,
                            ],
                            className="card-body",
                        )
                    ],
                    className="card mb-4",
                ),
                # Symbol equity curve
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(
                                    id="symbol-equity-graph",
                                    figure=empty_fig,
                                    config={"displayModeBar": False},
                                )
                            ],
                            className="card-body",
                        )
                    ],
                    className="card mb-4",
                ),
                # Symbol trades table (container to be filled by callback)
                html.Div(id="symbol-trades-table"),
            ]
        )

    def _render_ftmo_tab(self, account_data: Dict, trade_data: Dict) -> html.Div:
        """
        Render content for the FTMO compliance tab.

        Args:
            account_data: Processed account data
            trade_data: Processed trade data

        Returns:
            Dash component with tab content
        """
        # Calculate FTMO compliance
        ftmo_compliance = self._calculate_ftmo_compliance(account_data, trade_data)

        # Create FTMO rules reference
        ftmo_rules = html.Div(
            [
                html.Div(
                    [
                        html.H5("FTMO Rules", className="card-title"),
                        html.Ul(
                            [
                                html.Li(
                                    f"Profit Target: {self.ftmo_config['profit_target'] * 100}% of initial balance"
                                ),
                                html.Li(
                                    f"Maximum Daily Loss: {self.ftmo_config['daily_drawdown_limit'] * 100}%"
                                ),
                                html.Li(
                                    f"Maximum Total Loss: {self.ftmo_config['total_drawdown_limit'] * 100}%"
                                ),
                                html.Li(
                                    f"Minimum Trading Days: {self.ftmo_config['min_trading_days']} days"
                                ),
                            ]
                        ),
                    ],
                    className="card-body",
                )
            ],
            className="card mb-4",
        )

        # Create FTMO compliance status card
        compliance_status = ftmo_compliance.get("is_compliant", False)
        status_class = "text-success" if compliance_status else "text-danger"
        status_icon = (
            "fas fa-check-circle" if compliance_status else "fas fa-times-circle"
        )

        compliance_status_card = html.Div(
            [
                html.Div(
                    [
                        html.H5("Compliance Status", className="card-title"),
                        html.Div(
                            [
                                html.I(className=f"{status_icon} fa-2x mr-2"),
                                html.Span(
                                    (
                                        "COMPLIANT"
                                        if compliance_status
                                        else "NON-COMPLIANT"
                                    ),
                                    className=f"{status_class} font-weight-bold h4",
                                ),
                            ],
                            className="d-flex align-items-center",
                        ),
                        (
                            html.Div(
                                [
                                    html.P(reason)
                                    for reason in ftmo_compliance.get("reasons", [])
                                ]
                            )
                            if not compliance_status
                            else None
                        ),
                    ],
                    className="card-body",
                )
            ],
            className="card mb-4",
        )

        # Create FTMO metrics cards
        ftmo_metrics = self._create_ftmo_metrics_cards(ftmo_compliance)

        # Create daily performance chart
        daily_performance_fig = self._create_daily_performance_chart(trade_data)

        return html.Div(
            [
                # Top row: FTMO rules and compliance status
                html.Div(
                    [
                        html.Div([ftmo_rules], className="col-md-6"),
                        html.Div([compliance_status_card], className="col-md-6"),
                    ],
                    className="row mb-4",
                ),
                # Second row: FTMO metrics
                ftmo_metrics,
                # Third row: Daily performance chart
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(
                                    id="daily-performance-graph",
                                    figure=daily_performance_fig,
                                    config={"displayModeBar": False},
                                )
                            ],
                            className="card-body",
                        )
                    ],
                    className="card mb-4",
                ),
            ]
        )

    def _render_settings_tab(self) -> html.Div:
        """
        Render content for the settings tab.

        Returns:
            Dash component with tab content
        """
        return html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.H5("Dashboard Settings", className="card-title"),
                                html.Form(
                                    [
                                        html.Div(
                                            [
                                                html.Label(
                                                    "Update Interval (seconds):"
                                                ),
                                                dcc.Input(
                                                    id="update-interval-input",
                                                    type="number",
                                                    min=1,
                                                    max=300,
                                                    value=self.update_interval,
                                                    className="form-control",
                                                ),
                                            ],
                                            className="form-group",
                                        ),
                                        html.Div(
                                            [
                                                html.Label("Theme:"),
                                                dcc.Dropdown(
                                                    id="theme-dropdown",
                                                    options=[
                                                        {
                                                            "label": "Light",
                                                            "value": "light",
                                                        },
                                                        {
                                                            "label": "Dark",
                                                            "value": "dark",
                                                        },
                                                    ],
                                                    value=self.theme,
                                                    className="form-control",
                                                ),
                                            ],
                                            className="form-group",
                                        ),
                                        html.Div(
                                            [
                                                html.Label("Max Trades to Display:"),
                                                dcc.Input(
                                                    id="max-trades-input",
                                                    type="number",
                                                    min=10,
                                                    max=1000,
                                                    value=self.max_trades_to_display,
                                                    className="form-control",
                                                ),
                                            ],
                                            className="form-group",
                                        ),
                                        html.Button(
                                            "Apply Settings",
                                            id="apply-settings-button",
                                            className="btn btn-primary",
                                        ),
                                    ]
                                ),
                            ],
                            className="card-body",
                        )
                    ],
                    className="card mb-4 col-md-6 offset-md-3",
                )
            ],
            className="row",
        )

    def _process_trade_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Process trade data from the log file.

        Args:
            df: DataFrame with log data

        Returns:
            Processed trade data dictionary
        """
        # Filter only trade entries
        trade_df = df[df["Type"] == "TRADE"].copy()
        if trade_df.empty:
            return {"trades": [], "symbols": [], "summary": {}}

        # Convert columns to proper types
        for col in ["Price", "Volume", "StopLoss", "TakeProfit"]:
            if col in trade_df.columns:
                trade_df[col] = pd.to_numeric(trade_df[col], errors="coerce")

        # Pair entry and exit trades
        trades = []
        open_trades = {}
        symbols = set()

        for _, row in trade_df.iterrows():
            symbol = row.get("Symbol", "Unknown")
            symbols.add(symbol)
            action = row.get("Action", "")
            timestamp = row.get("Timestamp")
            price = row.get("Price", 0)
            volume = row.get("Volume", 0)

            # Entry trades (BUY/SELL)
            if action in ["BUY", "SELL"]:
                # Store the open trade
                if symbol not in open_trades:
                    open_trades[symbol] = []

                open_trades[symbol].append(
                    {
                        "direction": action,
                        "entry_time": timestamp,
                        "entry_price": price,
                        "volume": volume,
                        "stop_loss": row.get("StopLoss", None),
                        "take_profit": row.get("TakeProfit", None),
                    }
                )

            # Exit trades (CLOSE_BUY/CLOSE_SELL)
            elif action in ["CLOSE_BUY", "CLOSE_SELL"]:
                corresponding_action = "BUY" if action == "CLOSE_BUY" else "SELL"

                # Find matching open trade
                if symbol in open_trades and open_trades[symbol]:
                    # Find the first trade matching the direction
                    matching_trades = [
                        (i, t)
                        for i, t in enumerate(open_trades[symbol])
                        if t["direction"] == corresponding_action
                    ]

                    if matching_trades:
                        idx, matching_trade = matching_trades[0]

                        # Calculate profit/loss
                        if corresponding_action == "BUY":
                            # For BUY, profit = exit_price - entry_price
                            profit_loss = (
                                (price - matching_trade["entry_price"])
                                * matching_trade["volume"]
                                * 100000
                            )
                        else:
                            # For SELL, profit = entry_price - exit_price
                            profit_loss = (
                                (matching_trade["entry_price"] - price)
                                * matching_trade["volume"]
                                * 100000
                            )

                        # Create completed trade record
                        trade = {
                            "symbol": symbol,
                            "direction": matching_trade["direction"],
                            "entry_time": matching_trade["entry_time"],
                            "close_time": timestamp,
                            "entry_price": matching_trade["entry_price"],
                            "exit_price": price,
                            "volume": matching_trade["volume"],
                            "profit_loss": profit_loss,
                            "stop_loss": matching_trade["stop_loss"],
                            "take_profit": matching_trade["take_profit"],
                            "duration": (
                                            pd.to_datetime(timestamp)
                                            - pd.to_datetime(
                                            matching_trade["entry_time"])
                                        ).total_seconds()
                                        / 3600,  # in hours
                        }

                        trades.append(trade)

                        # Remove the matched trade
                        open_trades[symbol].pop(idx)

        # Calculate trade summary
        total_trades = len(trades)
        winning_trades = len([t for t in trades if t["profit_loss"] > 0])
        losing_trades = len([t for t in trades if t["profit_loss"] <= 0])
        win_rate = winning_trades / total_trades if total_trades > 0 else 0

        total_profit = sum([t["profit_loss"] for t in trades if t["profit_loss"] > 0])
        total_loss = sum([t["profit_loss"] for t in trades if t["profit_loss"] <= 0])

        avg_profit = total_profit / winning_trades if winning_trades > 0 else 0
        avg_loss = total_loss / losing_trades if losing_trades > 0 else 0

        profit_factor = (
            abs(total_profit / total_loss) if total_loss != 0 else float("inf")
        )

        # Calculate symbol-specific metrics
        symbol_metrics = {}
        for symbol in symbols:
            symbol_trades = [t for t in trades if t["symbol"] == symbol]
            symbol_total = len(symbol_trades)
            symbol_winners = len([t for t in symbol_trades if t["profit_loss"] > 0])

            symbol_metrics[symbol] = {
                "total_trades": symbol_total,
                "winning_trades": symbol_winners,
                "win_rate": symbol_winners / symbol_total if symbol_total > 0 else 0,
                "total_pnl": sum([t["profit_loss"] for t in symbol_trades]),
            }

        # Compile all data
        return {
            "trades": sorted(trades, key=lambda x: x["close_time"], reverse=True),
            "symbols": sorted(list(symbols)),
            "summary": {
                "total_trades": total_trades,
                "winning_trades": winning_trades,
                "losing_trades": losing_trades,
                "win_rate": win_rate,
                "total_profit": total_profit,
                "total_loss": total_loss,
                "avg_profit": avg_profit,
                "avg_loss": avg_loss,
                "profit_factor": profit_factor,
                "net_profit": total_profit + total_loss,
            },
            "symbol_metrics": symbol_metrics,
            "open_trades": open_trades,
        }

    def _process_account_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Process account data from the log file.

        Args:
            df: DataFrame with log data

        Returns:
            Processed account data dictionary
        """
        # Filter STATUS entries
        status_df = df[df["Type"] == "STATUS"].copy()

        if status_df.empty:
            return {
                "initial_balance": self.ftmo_config["initial_balance"],
                "current_balance": self.ftmo_config["initial_balance"],
                "current_equity": self.ftmo_config["initial_balance"],
                "daily_pl": 0,
                "equity_curve": [],
                "drawdowns": [],
            }

        # Try to extract balance from Balance column or Comment
        if "Balance" in status_df.columns:
            status_df["Balance"] = pd.to_numeric(status_df["Balance"], errors="coerce")
        else:
            # Extract from Comment
            balance_values = []
            for comment in status_df["Comment"]:
                if "Balance:" in str(comment):
                    try:
                        balance_str = (
                            str(comment).split("Balance:")[1].split(",")[0].strip()
                        )
                        balance_values.append(float(balance_str.replace(",", "")))
                    except:
                        balance_values.append(None)
                else:
                    balance_values.append(None)

            status_df["Balance"] = balance_values

        # Try to extract equity if available
        equity_values = []
        if "Equity" in status_df.columns:
            status_df["Equity"] = pd.to_numeric(status_df["Equity"], errors="coerce")
        else:
            # Extract from Comment
            for comment in status_df["Comment"]:
                if "Equity:" in str(comment):
                    try:
                        equity_str = (
                            str(comment).split("Equity:")[1].split(",")[0].strip()
                        )
                        equity_values.append(float(equity_str.replace(",", "")))
                    except:
                        equity_values.append(None)
                else:
                    equity_values.append(None)

            if equity_values:
                status_df["Equity"] = equity_values

        # Sort by timestamp
        status_df["Timestamp"] = pd.to_datetime(status_df["Timestamp"])
        status_df = status_df.sort_values("Timestamp")

        # Get initial and current values
        initial_balance = (
            status_df["Balance"].iloc[0]
            if not status_df.empty
            else self.ftmo_config["initial_balance"]
        )
        current_balance = (
            status_df["Balance"].iloc[-1] if not status_df.empty else initial_balance
        )

        # Calculate daily P&L
        status_df["Date"] = status_df["Timestamp"].dt.date
        today = datetime.now().date()

        today_df = status_df[status_df["Date"] == today]
        first_balance_today = (
            today_df["Balance"].iloc[0] if not today_df.empty else current_balance
        )
        daily_pl = current_balance - first_balance_today

        # Calculate equity curve and drawdowns
        equity_curve = []
        drawdowns = []
        peak_balance = initial_balance

        for idx, row in status_df.iterrows():
            timestamp = row["Timestamp"]
            balance = row["Balance"]
            equity = row.get("Equity", balance)

            # Update peak balance
            peak_balance = max(peak_balance, balance)

            # Calculate drawdown
            drawdown_pct = (
                (peak_balance - balance) / peak_balance * 100 if peak_balance > 0 else 0
            )

            # Add to equity curve
            equity_curve.append(
                {"timestamp": timestamp, "balance": balance, "equity": equity}
            )

            # Add to drawdowns if there is a drawdown
            if drawdown_pct > 0:
                drawdowns.append(
                    {
                        "timestamp": timestamp,
                        "balance": balance,
                        "drawdown_pct": drawdown_pct,
                    }
                )

        return {
            "initial_balance": initial_balance,
            "current_balance": current_balance,
            "current_equity": (
                status_df.get("Equity", status_df["Balance"]).iloc[-1]
                if not status_df.empty
                else current_balance
            ),
            "daily_pl": daily_pl,
            "equity_curve": equity_curve,
            "drawdowns": drawdowns,
        }

    def _process_position_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Process active position data from the log file.

        Args:
            df: DataFrame with log data

        Returns:
            Processed position data dictionary
        """
        # This would usually come from MT5 connector or trade processor
        # For now, we'll use the trade_data to reconstruct open positions

        # Filter trade entries
        trade_df = df[df["Type"] == "TRADE"].copy()

        if trade_df.empty:
            return {"positions": []}

        # Track open positions
        open_positions = {}

        for _, row in trade_df.iterrows():
            symbol = row.get("Symbol", "Unknown")
            action = row.get("Action", "")
            price = row.get("Price", 0)
            volume = row.get("Volume", 0)

            # Entry actions
            if action in ["BUY", "SELL"]:
                direction = 1 if action == "BUY" else -1

                # Create or update position
                if symbol not in open_positions:
                    open_positions[symbol] = {
                        "symbol": symbol,
                        "direction": action,
                        "net_volume": direction * volume,
                        "avg_price": price,
                        "entries": [
                            {
                                "time": row.get("Timestamp"),
                                "price": price,
                                "volume": volume,
                            }
                        ],
                    }
                else:
                    # Existing position - update
                    pos = open_positions[symbol]
                    new_volume = pos["net_volume"] + direction * volume

                    # If adding to position
                    if (new_volume > 0 and pos["net_volume"] > 0) or (
                        new_volume < 0 and pos["net_volume"] < 0
                    ):
                        # Calculate new average price
                        pos["avg_price"] = (
                                               pos["avg_price"] * abs(
                                               pos["net_volume"]) + price * volume
                                           ) / (abs(pos["net_volume"]) + volume)
                        pos["net_volume"] = new_volume
                    # If flipping position
                    elif new_volume != 0:
                        pos["avg_price"] = price
                        pos["net_volume"] = new_volume
                        pos["direction"] = "BUY" if new_volume > 0 else "SELL"
                    # If position is closed
                    else:
                        del open_positions[symbol]
                        continue

                    pos["entries"].append(
                        {"time": row.get("Timestamp"), "price": price, "volume": volume}
                    )

            # Close actions
            elif action in ["CLOSE_BUY", "CLOSE_SELL"]:
                if symbol in open_positions:
                    # Check if this closes the whole position
                    if (
                        action == "CLOSE_BUY"
                        and open_positions[symbol]["direction"] == "BUY"
                    ):
                        del open_positions[symbol]
                    elif (
                        action == "CLOSE_SELL"
                        and open_positions[symbol]["direction"] == "SELL"
                    ):
                        del open_positions[symbol]

        # Convert to list and calculate P&L
        positions = []
        for symbol, pos in open_positions.items():
            if pos["net_volume"] != 0:
                positions.append(pos)

        return {"positions": positions}

    def _create_equity_curve(self, account_data: Dict) -> go.Figure:
        """
        Create an equity curve plot.

        Args:
            account_data: Processed account data

        Returns:
            Plotly figure object
        """
        equity_curve = account_data.get("equity_curve", [])

        if not equity_curve:
            # Create empty figure if no data
            fig = go.Figure()
            fig.update_layout(
                title="Equity Curve", xaxis_title="Date", yaxis_title="Value ($)"
            )
            return fig

        # Extract data
        timestamps = [entry["timestamp"] for entry in equity_curve]
        balances = [entry["balance"] for entry in equity_curve]
        equities = [entry.get("equity", entry["balance"]) for entry in equity_curve]

        # Create figure
        fig = go.Figure()

        # Add balance line
        fig.add_trace(
            go.Scatter(
                x=timestamps,
                y=balances,
                mode="lines",
                name="Balance",
                line=dict(color="blue", width=2),
            )
        )

        # Add equity line if different from balance
        if any(abs(e - b) > 0.01 for e, b in zip(equities, balances)):
            fig.add_trace(
                go.Scatter(
                    x=timestamps,
                    y=equities,
                    mode="lines",
                    name="Equity",
                    line=dict(color="green", width=2, dash="dash"),
                )
            )

        # Add initial balance reference line
        initial_balance = account_data.get(
            "initial_balance", equities[0] if equities else 0
        )
        fig.add_trace(
            go.Scatter(
                x=[timestamps[0], timestamps[-1]],
                y=[initial_balance, initial_balance],
                mode="lines",
                name="Initial Balance",
                line=dict(color="gray", width=1, dash="dot"),
            )
        )

        # Add profit target line
        profit_target = initial_balance * (1 + self.ftmo_config["profit_target"])
        fig.add_trace(
            go.Scatter(
                x=[timestamps[0], timestamps[-1]],
                y=[profit_target, profit_target],
                mode="lines",
                name=f"{self.ftmo_config['profit_target'] * 100}% Profit Target",
                line=dict(color="green", width=1, dash="dot"),
            )
        )

        # Add maximum loss line
        max_loss = initial_balance * (1 - self.ftmo_config["total_drawdown_limit"])
        fig.add_trace(
            go.Scatter(
                x=[timestamps[0], timestamps[-1]],
                y=[max_loss, max_loss],
                mode="lines",
                name=f"{self.ftmo_config['total_drawdown_limit'] * 100}% Max Loss",
                line=dict(color="red", width=1, dash="dot"),
            )
        )

        # Format layout
        fig.update_layout(
            title="Equity Curve",
            xaxis_title="Date",
            yaxis_title="Value ($)",
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
            height=400,
            margin=dict(l=40, r=40, t=60, b=40),
        )

        return fig

    def _create_drawdown_chart(self, account_data: Dict) -> go.Figure:
        """
        Create a drawdown chart.

        Args:
            account_data: Processed account data

        Returns:
            Plotly figure object
        """
        drawdowns = account_data.get("drawdowns", [])

        if not drawdowns:
            # Create empty figure if no data
            fig = go.Figure()
            fig.update_layout(
                title="Drawdown", xaxis_title="Date", yaxis_title="Drawdown (%)"
            )
            return fig

        # Extract data
        timestamps = [entry["timestamp"] for entry in drawdowns]
        drawdown_pcts = [entry["drawdown_pct"] for entry in drawdowns]

        # Create figure
        fig = go.Figure()

        # Add drawdown area
        fig.add_trace(
            go.Scatter(
                x=timestamps,
                y=[-d for d in drawdown_pcts],  # Negative for better visualization
                fill="tozeroy",
                mode="lines",
                name="Drawdown",
                line=dict(color="red", width=1),
                fillcolor="rgba(255, 0, 0, 0.2)",
            )
        )

        # Add daily drawdown limit reference line
        daily_limit = -self.ftmo_config["daily_drawdown_limit"] * 100
        fig.add_trace(
            go.Scatter(
                x=[timestamps[0], timestamps[-1]],
                y=[daily_limit, daily_limit],
                mode="lines",
                name=f"{self.ftmo_config['daily_drawdown_limit'] * 100}% Daily Limit",
                line=dict(color="orange", width=1, dash="dot"),
            )
        )

        # Add total drawdown limit reference line
        total_limit = -self.ftmo_config["total_drawdown_limit"] * 100
        fig.add_trace(
            go.Scatter(
                x=[timestamps[0], timestamps[-1]],
                y=[total_limit, total_limit],
                mode="lines",
                name=f"{self.ftmo_config['total_drawdown_limit'] * 100}% Total Limit",
                line=dict(color="red", width=1, dash="dot"),
            )
        )

        # Format layout
        fig.update_layout(
            title="Drawdown",
            xaxis_title="Date",
            yaxis_title="Drawdown (%)",
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
            height=400,
            margin=dict(l=40, r=40, t=60, b=40),
        )

        return fig

    def _create_metrics_cards(self, trade_data: Dict, account_data: Dict) -> html.Div:
        """
        Create performance metrics cards.

        Args:
            trade_data: Processed trade data
            account_data: Processed account data

        Returns:
            Dash component with metrics cards
        """
        summary = trade_data.get("summary", {})

        # Calculate metrics
        total_trades = summary.get("total_trades", 0)
        win_rate = summary.get("win_rate", 0) * 100
        profit_factor = summary.get("profit_factor", 0)
        net_profit = summary.get("net_profit", 0)

        initial_balance = account_data.get("initial_balance", 100000)
        profit_percentage = (
            (net_profit / initial_balance) * 100 if initial_balance > 0 else 0
        )

        # Define card styles
        profit_color = "text-success" if profit_percentage >= 0 else "text-danger"

        # Create metrics cards
        return html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.I(
                                                    className="fas fa-chart-line fa-2x text-primary"
                                                )
                                            ],
                                            className="col-auto",
                                        ),
                                        html.Div(
                                            [
                                                html.H5(
                                                    f"{total_trades}", className="mb-0"
                                                ),
                                                html.Span(
                                                    "Total Trades",
                                                    className="text-muted small",
                                                ),
                                            ],
                                            className="col",
                                        ),
                                    ],
                                    className="row align-items-center",
                                )
                            ],
                            className="card-body",
                        )
                    ],
                    className="card mb-4 col-md-3",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.I(
                                                    className="fas fa-trophy fa-2x text-warning"
                                                )
                                            ],
                                            className="col-auto",
                                        ),
                                        html.Div(
                                            [
                                                html.H5(
                                                    f"{win_rate:.1f}%", className="mb-0"
                                                ),
                                                html.Span(
                                                    "Win Rate",
                                                    className="text-muted small",
                                                ),
                                            ],
                                            className="col",
                                        ),
                                    ],
                                    className="row align-items-center",
                                )
                            ],
                            className="card-body",
                        )
                    ],
                    className="card mb-4 col-md-3",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.I(
                                                    className="fas fa-balance-scale fa-2x text-info"
                                                )
                                            ],
                                            className="col-auto",
                                        ),
                                        html.Div(
                                            [
                                                html.H5(
                                                    f"{profit_factor:.2f}",
                                                    className="mb-0",
                                                ),
                                                html.Span(
                                                    "Profit Factor",
                                                    className="text-muted small",
                                                ),
                                            ],
                                            className="col",
                                        ),
                                    ],
                                    className="row align-items-center",
                                )
                            ],
                            className="card-body",
                        )
                    ],
                    className="card mb-4 col-md-3",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.I(
                                                    className="fas fa-dollar-sign fa-2x text-success"
                                                )
                                            ],
                                            className="col-auto",
                                        ),
                                        html.Div(
                                            [
                                                html.H5(
                                                    f"${net_profit:.2f} ({profit_percentage:.2f}%)",
                                                    className=f"mb-0 {profit_color}",
                                                ),
                                                html.Span(
                                                    "Net Profit",
                                                    className="text-muted small",
                                                ),
                                            ],
                                            className="col",
                                        ),
                                    ],
                                    className="row align-items-center",
                                )
                            ],
                            className="card-body",
                        )
                    ],
                    className="card mb-4 col-md-3",
                ),
            ],
            className="row",
        )

    def _create_positions_table(self, position_data: Dict) -> html.Div:
        """
        Create a table displaying active positions.

        Args:
            position_data: Processed position data

        Returns:
            Dash component with positions table
        """
        positions = position_data.get("positions", [])

        if not positions:
            return html.Div("No active positions")

        # Create table header
        header = html.Thead(
            [
                html.Tr(
                    [
                        html.Th("Symbol"),
                        html.Th("Direction"),
                        html.Th("Size"),
                        html.Th("Avg. Price"),
                        html.Th("Current P&L"),
                    ]
                )
            ]
        )

        # Create table rows
        rows = []
        for pos in positions:
            symbol = pos.get("symbol", "Unknown")
            direction = pos.get("direction", "Unknown")
            volume = abs(pos.get("net_volume", 0))
            avg_price = pos.get("avg_price", 0)

            # In a real implementation, you would get current price from MT5
            # For now, we'll use a dummy value
            current_price = avg_price * (1.001 if direction == "BUY" else 0.999)

            # Calculate P&L
            if direction == "BUY":
                pnl = (current_price - avg_price) * volume * 100000
            else:
                pnl = (avg_price - current_price) * volume * 100000

            # Format row with color based on P&L
            pnl_class = "text-success" if pnl >= 0 else "text-danger"

            row = html.Tr(
                [
                    html.Td(symbol),
                    html.Td(
                        html.Span(
                            direction,
                            className=(
                                "text-success" if direction == "BUY" else "text-danger"
                            ),
                        )
                    ),
                    html.Td(f"{volume:.2f}"),
                    html.Td(f"{avg_price:.5f}"),
                    html.Td(html.Span(f"${pnl:.2f}", className=pnl_class)),
                ]
            )

            rows.append(row)

        # Create table body
        body = html.Tbody(rows)

        # Create complete table
        table = html.Table([header, body], className="table table-striped table-sm")

        return table

    def _create_trade_table(
        self, trades: List[Dict], title: Optional[str] = None
    ) -> html.Div:
        """
        Create a table displaying trade history.

        Args:
            trades: List of trade dictionaries
            title: Optional title for the table

        Returns:
            Dash component with trade table
        """
        if not trades:
            return html.Div("No trades available")

        # Create table header
        header = html.Thead(
            [
                html.Tr(
                    [
                        html.Th("Symbol"),
                        html.Th("Direction"),
                        html.Th("Entry Time"),
                        html.Th("Exit Time"),
                        html.Th("Entry Price"),
                        html.Th("Exit Price"),
                        html.Th("Volume"),
                        html.Th("P&L"),
                        html.Th("Duration"),
                    ]
                )
            ]
        )

        # Create table rows
        rows = []
        for trade in trades:
            symbol = trade.get("symbol", "Unknown")
            direction = trade.get("direction", "Unknown")
            entry_time = trade.get("entry_time", "")
            close_time = trade.get("close_time", "")
            entry_price = trade.get("entry_price", 0)
            exit_price = trade.get("exit_price", 0)
            volume = trade.get("volume", 0)
            profit_loss = trade.get("profit_loss", 0)
            duration = trade.get("duration", 0)

            # Format row with color based on P&L
            pnl_class = "text-success" if profit_loss >= 0 else "text-danger"

            row = html.Tr(
                [
                    html.Td(symbol),
                    html.Td(
                        html.Span(
                            direction,
                            className=(
                                "text-success" if direction == "BUY" else "text-danger"
                            ),
                        )
                    ),
                    html.Td(str(entry_time)),
                    html.Td(str(close_time)),
                    html.Td(f"{entry_price:.5f}"),
                    html.Td(f"{exit_price:.5f}"),
                    html.Td(f"{volume:.2f}"),
                    html.Td(html.Span(f"${profit_loss:.2f}", className=pnl_class)),
                    html.Td(f"{duration:.1f} hrs"),
                ]
            )

            rows.append(row)

        # Create table body
        body = html.Tbody(rows)

        # Create complete table
        table_div = html.Div(
            [html.Table([header, body], className="table table-striped table-sm")],
            className="table-responsive",
        )

        if title:
            return html.Div(
                [html.H5(title, className="card-title") if title else None, table_div]
            )
        else:
            return table_div

    def _create_trade_pnl_graph(self, trades: List[Dict]) -> go.Figure:
        """
        Create a graph showing P&L for each trade.

        Args:
            trades: List of trade dictionaries

        Returns:
            Plotly figure object
        """
        if not trades:
            # Create empty figure if no data
            fig = go.Figure()
            fig.update_layout(
                title="Trade P&L", xaxis_title="Trade #", yaxis_title="P&L ($)"
            )
            return fig

        # Extract data
        trade_numbers = list(range(1, len(trades) + 1))
        profits = [trade.get("profit_loss", 0) for trade in trades]
        symbols = [trade.get("symbol", "Unknown") for trade in trades]
        directions = [trade.get("direction", "Unknown") for trade in trades]

        # Colors based on profit/loss
        colors = ["green" if p >= 0 else "red" for p in profits]

        # Create hover text
        hover_text = [
            f"Symbol: {symbol}<br>"
            f"Direction: {direction}<br>"
            f"P&L: ${profit:.2f}<br>"
            f"Entry: {trade.get('entry_time', '')}<br>"
            f"Exit: {trade.get('close_time', '')}"
            for symbol, direction, profit, trade in zip(
                symbols, directions, profits, trades
            )
        ]

        # Create figure
        fig = go.Figure()

        # Add profit/loss bars
        fig.add_trace(
            go.Bar(
                x=trade_numbers,
                y=profits,
                marker_color=colors,
                hovertext=hover_text,
                hoverinfo="text",
                name="P&L",
            )
        )

        # Add horizontal zero line
        fig.add_shape(
            type="line",
            x0=0,
            y0=0,
            x1=len(trades) + 1,
            y1=0,
            line=dict(color="black", width=1, dash="dash"),
        )

        # Format layout
        fig.update_layout(
            title="Trade P&L",
            xaxis_title="Trade #",
            yaxis_title="P&L ($)",
            height=400,
            margin=dict(l=40, r=40, t=60, b=40),
        )

        return fig

    def _create_trade_distribution_graph(self, trades: List[Dict]) -> go.Figure:
        """
        Create a graph showing the distribution of trade results.

        Args:
            trades: List of trade dictionaries

        Returns:
            Plotly figure object
        """
        if not trades:
            # Create empty figure if no data
            fig = go.Figure()
            fig.update_layout(
                title="Trade Distribution",
                xaxis_title="P&L ($)",
                yaxis_title="Frequency",
            )
            return fig

        # Extract data
        profits = [trade.get("profit_loss", 0) for trade in trades]

        # Create figure
        fig = go.Figure()

        # Add histogram
        fig.add_trace(
            go.Histogram(
                x=profits,
                marker_color=["green" if p >= 0 else "red" for p in profits],
                histnorm="count",
                name="P&L Distribution",
                autobinx=False,
                xbins=dict(
                    start=min(profits) - 10,
                    end=max(profits) + 10,
                    size=(
                        (max(profits) - min(profits)) / 20
                        if max(profits) > min(profits)
                        else 10
                    ),
                ),
            )
        )

        # Add vertical zero line
        fig.add_shape(
            type="line",
            x0=0,
            y0=0,
            x1=0,
            y1=1,
            xref="x",
            yref="paper",
            line=dict(color="black", width=1, dash="dash"),
        )

        # Format layout
        fig.update_layout(
            title="Trade P&L Distribution",
            xaxis_title="P&L ($)",
            yaxis_title="Frequency",
            bargap=0.1,
            height=400,
            margin=dict(l=40, r=40, t=60, b=40),
        )

        return fig

    def _create_symbol_metrics(self, trade_data: Dict) -> html.Div:
        """
        Create a table displaying performance metrics per symbol.

        Args:
            trade_data: Processed trade data

        Returns:
            Dash component with symbol metrics table
        """
        symbol_metrics = trade_data.get("symbol_metrics", {})

        if not symbol_metrics:
            return html.Div("No symbol data available")

        # Create table header
        header = html.Thead(
            [
                html.Tr(
                    [
                        html.Th("Symbol"),
                        html.Th("Total Trades"),
                        html.Th("Win Rate"),
                        html.Th("Net P&L"),
                        html.Th("Performance"),
                    ]
                )
            ]
        )

        # Create table rows
        rows = []
        for symbol, metrics in symbol_metrics.items():
            total_trades = metrics.get("total_trades", 0)
            win_rate = metrics.get("win_rate", 0) * 100
            total_pnl = metrics.get("total_pnl", 0)

            # Format row with color based on P&L
            pnl_class = "text-success" if total_pnl >= 0 else "text-danger"

            # Create progress bar for win rate
            win_rate_bar = html.Div(
                [
                    html.Div(
                        className="progress-bar bg-success",
                        style={"width": f"{win_rate}%"},
                        children=f"{win_rate:.1f}%",
                    )
                ],
                className="progress",
            )

            row = html.Tr(
                [
                    html.Td(symbol),
                    html.Td(total_trades),
                    html.Td(win_rate_bar),
                    html.Td(html.Span(f"${total_pnl:.2f}", className=pnl_class)),
                    html.Td(
                        html.I(
                            className=(
                                "fas fa-circle text-success"
                                if total_pnl >= 0
                                else "fas fa-circle text-danger"
                            )
                        )
                    ),
                ]
            )

            rows.append(row)

        # Create table body
        body = html.Tbody(rows)

        # Create complete table
        table = html.Table([header, body], className="table table-striped")

        return html.Div([table], className="table-responsive")

    def _create_daily_performance_chart(self, trade_data: Dict) -> go.Figure:
        """
        Create a chart showing daily trading performance.

        Args:
            trade_data: Processed trade data

        Returns:
            Plotly figure object
        """
        trades = trade_data.get("trades", [])

        if not trades:
            # Create empty figure if no data
            fig = go.Figure()
            fig.update_layout(
                title="Daily Performance", xaxis_title="Date", yaxis_title="P&L ($)"
            )
            return fig

        # Group trades by day
        daily_pnl = {}
        for trade in trades:
            close_time = trade.get("close_time", "")
            profit_loss = trade.get("profit_loss", 0)

            # Convert close_time to date string
            try:
                if isinstance(close_time, str):
                    close_date = pd.to_datetime(close_time).date().strftime("%Y-%m-%d")
                else:
                    close_date = close_time.date().strftime("%Y-%m-%d")

                if close_date not in daily_pnl:
                    daily_pnl[close_date] = 0

                daily_pnl[close_date] += profit_loss
            except:
                # Skip trades with invalid dates
                continue

        # Sort by date
        dates = sorted(daily_pnl.keys())
        pnls = [daily_pnl[date] for date in dates]

        # Calculate cumulative P&L
        cumulative_pnl = np.cumsum(pnls)

        # Create figure with subplots
        fig = make_subplots(
            rows=2,
            cols=1,
            subplot_titles=("Daily P&L", "Cumulative P&L"),
            vertical_spacing=0.15,
            row_heights=[0.4, 0.6],
        )

        # Add daily P&L bars
        fig.add_trace(
            go.Bar(
                x=dates,
                y=pnls,
                marker_color=["green" if p >= 0 else "red" for p in pnls],
                name="Daily P&L",
            ),
            row=1,
            col=1,
        )

        # Add cumulative P&L line
        fig.add_trace(
            go.Scatter(
                x=dates,
                y=cumulative_pnl,
                mode="lines+markers",
                name="Cumulative P&L",
                line=dict(color="blue", width=2),
            ),
            row=2,
            col=1,
        )

        # Add zero line to daily P&L
        fig.add_shape(
            type="line",
            x0=dates[0],
            y0=0,
            x1=dates[-1],
            y1=0,
            line=dict(color="black", width=1, dash="dash"),
            row=1,
            col=1,
        )

        # Format layout
        fig.update_layout(
            height=600, showlegend=False, margin=dict(l=40, r=40, t=60, b=40)
        )

        # Update y-axis titles
        fig.update_yaxes(title_text="P&L ($)", row=1, col=1)
        fig.update_yaxes(title_text="Cumulative P&L ($)", row=2, col=1)

        return fig

    def _create_ftmo_metrics_cards(self, ftmo_compliance: Dict) -> html.Div:
        """
        Create cards displaying FTMO compliance metrics.

        Args:
            ftmo_compliance: FTMO compliance data

        Returns:
            Dash component with FTMO metrics cards
        """
        # Extract metrics
        profit_percentage = ftmo_compliance.get("profit_percentage", 0)
        profit_target = self.ftmo_config["profit_target"] * 100
        profit_target_met = ftmo_compliance.get("profit_target_met", False)

        max_drawdown = ftmo_compliance.get("max_drawdown", 0)
        total_drawdown_limit = self.ftmo_config["total_drawdown_limit"] * 100
        total_loss_compliant = ftmo_compliance.get("total_loss_compliant", False)

        worst_daily_loss = ftmo_compliance.get("worst_daily_loss", 0)
        daily_drawdown_limit = self.ftmo_config["daily_drawdown_limit"] * 100
        daily_loss_compliant = ftmo_compliance.get("daily_loss_compliant", False)

        unique_trading_days = ftmo_compliance.get("unique_trading_days", 0)
        min_trading_days = self.ftmo_config["min_trading_days"]
        trading_days_compliant = ftmo_compliance.get("trading_days_compliant", False)

        # Create status indicators
        profit_status = (
            html.I(className="fas fa-check text-success mr-2")
            if profit_target_met
            else html.I(className="fas fa-times text-danger mr-2")
        )
        drawdown_status = (
            html.I(className="fas fa-check text-success mr-2")
            if total_loss_compliant
            else html.I(className="fas fa-times text-danger mr-2")
        )
        daily_loss_status = (
            html.I(className="fas fa-check text-success mr-2")
            if daily_loss_compliant
            else html.I(className="fas fa-times text-danger mr-2")
        )
        trading_days_status = (
            html.I(className="fas fa-check text-success mr-2")
            if trading_days_compliant
            else html.I(className="fas fa-times text-danger mr-2")
        )

        # Create metrics cards
        return html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.H5("Profit Target", className="card-title"),
                                html.Div(
                                    [
                                        profit_status,
                                        html.Span(
                                            f"{profit_percentage:.2f}% / {profit_target}%",
                                            className=(
                                                "text-success"
                                                if profit_target_met
                                                else "text-danger"
                                            ),
                                        ),
                                    ],
                                    className="d-flex align-items-center",
                                ),
                                html.Div(
                                    [
                                        dcc.Progress(
                                            value=min(
                                                100,
                                                (profit_percentage / profit_target)
                                                * 100,
                                            ),
                                            className="mt-2",
                                            color=(
                                                "success"
                                                if profit_target_met
                                                else "danger"
                                            ),
                                        )
                                    ]
                                ),
                            ],
                            className="card-body",
                        )
                    ],
                    className="card mb-4 col-md-3",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H5("Maximum Drawdown", className="card-title"),
                                html.Div(
                                    [
                                        drawdown_status,
                                        html.Span(
                                            f"{max_drawdown:.2f}% / {total_drawdown_limit}%",
                                            className=(
                                                "text-success"
                                                if total_loss_compliant
                                                else "text-danger"
                                            ),
                                        ),
                                    ],
                                    className="d-flex align-items-center",
                                ),
                                html.Div(
                                    [
                                        dcc.Progress(
                                            value=min(
                                                100,
                                                (max_drawdown / total_drawdown_limit)
                                                * 100,
                                            ),
                                            className="mt-2",
                                            color=(
                                                "success"
                                                if total_loss_compliant
                                                else "danger"
                                            ),
                                        )
                                    ]
                                ),
                            ],
                            className="card-body",
                        )
                    ],
                    className="card mb-4 col-md-3",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H5("Daily Loss Limit", className="card-title"),
                                html.Div(
                                    [
                                        daily_loss_status,
                                        html.Span(
                                            f"{abs(worst_daily_loss):.2f}% / {daily_drawdown_limit}%",
                                            className=(
                                                "text-success"
                                                if daily_loss_compliant
                                                else "text-danger"
                                            ),
                                        ),
                                    ],
                                    className="d-flex align-items-center",
                                ),
                                html.Div(
                                    [
                                        dcc.Progress(
                                            value=min(
                                                100,
                                                (
                                                    abs(worst_daily_loss)
                                                    / daily_drawdown_limit
                                                )
                                                * 100,
                                            ),
                                            className="mt-2",
                                            color=(
                                                "success"
                                                if daily_loss_compliant
                                                else "danger"
                                            ),
                                        )
                                    ]
                                ),
                            ],
                            className="card-body",
                        )
                    ],
                    className="card mb-4 col-md-3",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H5("Trading Days", className="card-title"),
                                html.Div(
                                    [
                                        trading_days_status,
                                        html.Span(
                                            f"{unique_trading_days} / {min_trading_days}",
                                            className=(
                                                "text-success"
                                                if trading_days_compliant
                                                else "text-danger"
                                            ),
                                        ),
                                    ],
                                    className="d-flex align-items-center",
                                ),
                                html.Div(
                                    [
                                        dcc.Progress(
                                            value=min(
                                                100,
                                                (unique_trading_days / min_trading_days)
                                                * 100,
                                            ),
                                            className="mt-2",
                                            color=(
                                                "success"
                                                if trading_days_compliant
                                                else "danger"
                                            ),
                                        )
                                    ]
                                ),
                            ],
                            className="card-body",
                        )
                    ],
                    className="card mb-4 col-md-3",
                ),
            ],
            className="row",
        )

    def _calculate_ftmo_compliance(self, account_data: Dict, trade_data: Dict) -> Dict:
        """
        Calculate FTMO compliance based on account and trade data.

        Args:
            account_data: Processed account data
            trade_data: Processed trade data

        Returns:
            Dictionary with FTMO compliance results
        """
        # Extract required data
        initial_balance = account_data.get(
            "initial_balance", self.ftmo_config["initial_balance"]
        )
        current_balance = account_data.get("current_balance", initial_balance)
        drawdowns = account_data.get("drawdowns", [])
        trades = trade_data.get("trades", [])

        # Calculate profit percentage
        profit_amount = current_balance - initial_balance
        profit_percentage = (
            (profit_amount / initial_balance) * 100 if initial_balance > 0 else 0
        )

        # Check profit target
        profit_target = self.ftmo_config["profit_target"] * 100
        profit_target_met = profit_percentage >= profit_target

        # Calculate max drawdown
        max_drawdown = (
            max([d.get("drawdown_pct", 0) for d in drawdowns]) if drawdowns else 0
        )

        # Check total drawdown limit
        total_drawdown_limit = self.ftmo_config["total_drawdown_limit"] * 100
        total_loss_compliant = max_drawdown <= total_drawdown_limit

        # Calculate worst daily loss
        daily_pnl = {}
        for trade in trades:
            close_time = trade.get("close_time", "")
            profit_loss = trade.get("profit_loss", 0)

            # Convert close_time to date string
            try:
                if isinstance(close_time, str):
                    close_date = pd.to_datetime(close_time).date().strftime("%Y-%m-%d")
                else:
                    close_date = close_time.date().strftime("%Y-%m-%d")

                if close_date not in daily_pnl:
                    daily_pnl[close_date] = 0

                daily_pnl[close_date] += profit_loss
            except:
                # Skip trades with invalid dates
                continue

        # Calculate worst daily loss as percentage of initial balance
        worst_daily_loss = (
            min(daily_pnl.values()) / initial_balance * 100 if daily_pnl else 0
        )

        # Check daily loss limit
        daily_drawdown_limit = self.ftmo_config["daily_drawdown_limit"] * 100
        daily_loss_compliant = worst_daily_loss > -daily_drawdown_limit

        # Count unique trading days
        unique_trading_days = len(daily_pnl)

        # Check minimum trading days
        min_trading_days = self.ftmo_config["min_trading_days"]
        trading_days_compliant = unique_trading_days >= min_trading_days

        # Overall compliance
        is_compliant = (
            profit_target_met
            and total_loss_compliant
            and daily_loss_compliant
            and trading_days_compliant
        )

        # Create reasons for non-compliance
        reasons = []
        if not profit_target_met:
            reasons.append(
                f"Profit target not met: {profit_percentage:.2f}% < {profit_target}%"
            )
        if not total_loss_compliant:
            reasons.append(
                f"Maximum drawdown exceeded: {max_drawdown:.2f}% > {total_drawdown_limit}%"
            )
        if not daily_loss_compliant:
            reasons.append(
                f"Daily loss limit exceeded: {worst_daily_loss:.2f}% < -{daily_drawdown_limit}%"
            )
        if not trading_days_compliant:
            reasons.append(
                f"Insufficient trading days: {unique_trading_days} < {min_trading_days}"
            )

        return {
            "is_compliant": is_compliant,
            "profit_target_met": profit_target_met,
            "total_loss_compliant": total_loss_compliant,
            "daily_loss_compliant": daily_loss_compliant,
            "trading_days_compliant": trading_days_compliant,
            "profit_percentage": profit_percentage,
            "max_drawdown": max_drawdown,
            "worst_daily_loss": worst_daily_loss,
            "unique_trading_days": unique_trading_days,
            "reasons": reasons if not is_compliant else [],
        }

    def run_server(
        self, debug: bool = False, port: int = 8050, host: str = "0.0.0.0"
    ) -> None:
        """
        Start the dashboard server.

        Args:
            debug: Enable debug mode
            port: Port to run the server on
            host: Host to run the server on
        """
        self.logger.info(f"Starting dashboard server on {host}:{port}")
        self.app.run_server(debug=debug, port=port, host=host)
