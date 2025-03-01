# TurtleTrader MT5 Bot

Een moderne implementatie van de Turtle Trading strategie voor MetaTrader 5, geïmplementeerd in Python.

## Features

- Complete implementatie van de Turtle Trading strategie
- Automatische verbinding met MetaTrader 5
- Geavanceerd risicomanagement
- Uitgebreide logging en rapportage
- Ondersteuning voor meerdere instrumenten

## Configuratie

De configuratie wordt gedaan via het `config/turtle_settings.json` bestand:

```json
{
  "mt5": {
    "login": 1234567,
    "password": "yourpassword",
    "server": "YourBroker-Demo",
    "mt5_pathway": "C:\\Program Files\\MetaTrader 5\\terminal64.exe",
    "symbols": ["EURUSD", "XAUUSD", "US30"],
    "timeframe": "D1",
    "risk_per_trade": 0.01,
    "account_balance": 100000
  }
}