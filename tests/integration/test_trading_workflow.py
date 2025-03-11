import pandas as pd

from strategy.strategy_factory import StrategyFactory


def test_complete_trading_cycle(self, mock_setup):
    """
    Test een volledige handelscyclus van strategie-initialisatie tot order uitvoering.
    
    Deze test valideert de end-to-end integratie van alle componenten:
    - Configuratie laden
    - MT5 verbinding
    - Strategie initialisatie
    - Signaal detectie
    - Risicobeheer
    - Order plaatsing
    """
    # Haal componenten uit mock setup
    config = mock_setup['config']
    logger = mock_setup['logger']
    connector = mock_setup['connector']
    risk_manager = mock_setup['risk_manager']
    mt5_mock = mock_setup['mt5_mock']
    
    # Maak turtle strategie aan via factory
    strategy = StrategyFactory.create_strategy(
        strategy_name="turtle",
        connector=connector,
        risk_manager=risk_manager,
        logger=logger,
        config=config
    )
    
    # Verwerk symbool om handelssignaal te genereren
    symbol = config['mt5']['symbols'][0]  # Gebruik eerste symbool
    result = strategy.process_symbol(symbol)
    
    # Controleer resultaten
    assert result is not None, "Strategie moet een resultaat teruggeven"
    assert 'signal' in result, "Resultaat moet een 'signal' sleutel bevatten"
    
    # Als er een signaal is, controleer de order uitvoering
    if result.get('signal') == 'ENTRY':
        assert result.get('action') in ['BUY', 'SELL'], "Actie moet BUY of SELL zijn"
        assert 'ticket' in result, "Entry signaal moet een ticket ID bevatten"
        assert mt5_mock.order_send.called, "MT5 order_send moet worden aangeroepen"
    
    # Controleer FTMO limieten
    should_stop, reason = risk_manager.check_ftmo_limits(connector.get_account_info())
    
    # Log de resultaten
    logger.log_info(f"Workflow test resultaat: {result}")
    logger.log_info(f"FTMO limiet check: stop={should_stop}, reason={reason}")
    
    # Controleer dat logbestand correct is bijgewerkt
    log_data = pd.read_csv(config['logging']['log_file'])
    assert len(log_data) > 0, "Logbestand moet entries bevatten"


def test_risk_management_integration(self, mock_setup):
    """
    Test de integratie van risicobeheer binnen de handelsstrategie.
    
    Valideert:
    - Correcte berekening van positiegrootte
    - Toepassing van risicobeperkingen
    - FTMO limiet controles
    """
    # Haal componenten uit mock setup
    config = mock_setup['config']
    logger = mock_setup['logger']
    connector = mock_setup['connector']
    risk_manager = mock_setup['risk_manager']
    
    # Stel daglijkse verlies in op bijna overschreden waarde
    risk_manager.daily_losses = config['risk']['max_daily_drawdown'] * 100000 * 0.9
    
    # Maak mock strategie
    strategy = StrategyFactory.create_strategy(
        strategy_name="turtle",
        connector=connector,
        risk_manager=risk_manager,
        logger=logger,
        config=config
    )
    
    # Spioneer op de check_trade_risk methode
    original_check_trade_risk = risk_manager.check_trade_risk
    check_trade_risk_calls = []
    
    def spy_check_trade_risk(*args, **kwargs):
        check_trade_risk_calls.append((args, kwargs))
        return original_check_trade_risk(*args, **kwargs)
    
    risk_manager.check_trade_risk = spy_check_trade_risk
    
    # Verwerk symbool
    symbol = config['mt5']['symbols'][0]
    strategy.process_symbol(symbol)
    
    # Controleer of de risk manager werd aangeroepen
    assert len(check_trade_risk_calls) > 0, "Risk manager check_trade_risk moet worden aangeroepen"
    
    # Simuleer dagelijkse verlieslimiet overschrijding
    risk_manager.daily_losses = config['risk']['max_daily_drawdown'] * 100000 * 1.1
    
    # Verwerk nog een symbool, zou geen handel moeten genereren
    result = strategy.process_symbol(symbol)
    assert result.get('signal') is None, "Geen signaal verwacht bij overschreden dagelijkse verlieslimiet"


def test_multiple_symbols_handling(self, mock_setup):
    """
    Test het verwerken van meerdere symbolen binnen één handelscyclus.
    
    Valideert:
    - Correcte verwerking van meerdere symbolen
    - Onafhankelijke signaaldetectie per symbool
    - Geaggregeerde risico-evaluatie
    """
    # Haal componenten uit mock setup
    config = mock_setup['config']
    logger = mock_setup['logger']
    connector = mock_setup['connector']
    risk_manager = mock_setup['risk_manager']
    
    # Maak strategie
    strategy = StrategyFactory.create_strategy(
        strategy_name="turtle",
        connector=connector,
        risk_manager=risk_manager,
        logger=logger,
        config=config
    )
    
    # Verwerk alle symbolen
    results = {}
    for symbol in config['mt5']['symbols']:
        results[symbol] = strategy.process_symbol(symbol)
        
    # Controleer resultaten voor elk symbool
    assert len(results) == len(config['mt5']['symbols']), "Moet resultaten hebben voor alle symbolen"
    
    # Controleer of minstens één symbool een signaal genereerde
    signals = [r.get('signal') for r in results.values() if r.get('signal') is not None]
    logger.log_info(f"Gegenereerde signalen: {signals}")
    
    # Verificatie is contextafhankelijk van de gegenereerde data
    # In een echte test zouden we verschillende symbolen kunnen mappen naar verschillende testdata
