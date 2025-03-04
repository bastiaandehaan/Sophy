# docs/architecture.md
# TurtleTrader Architectuur

## Overzicht
TurtleTrader is een Python-applicatie die de Turtle Trading strategie implementeert via MetaTrader 5. De applicatie is ontworpen voor gebruik met FTMO-accounts en zorgt voor compliance met FTMO-regels.

## Componenten

### 1. MT5 Connector
Verantwoordelijk voor de communicatie met het MetaTrader 5 platform.

### 2. Strategie
Implementeert de Turtle Trading logica met ondersteuning voor zowel standaard als swing trading modes.

### 3. Risicomanagement
Zorgt voor naleving van risicolimieten en berekent optimale positiegroottes.

### 4. Analyse
Biedt backtesting, optimalisatie en performance-evaluatie.

### 5. FTMO Validatie
Controleert of de trading voldoet aan FTMO-regels en -limieten.

## Dataflow
1. MT5 Connector haalt marktdata op
2. Turtle strategie analyseert data en genereert signalen
3. Risicomanager valideert en past posities aan
4. Orders worden doorgestuurd naar MT5
5. Resultaten worden gelogd en geanalyseerd

## Configuratie
De applicatie gebruikt JSON-configuratiebestanden in de `config/` directory.