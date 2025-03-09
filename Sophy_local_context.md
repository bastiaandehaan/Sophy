Path: .github/workflows/ci.yml

```yaml
# .github/workflows/ci.yml
name: TurtleTrader CI

on:
  push:
    branches: [ main, development ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
          pip install pytest pytest-cov
      - name: Run tests
        run: |
          pytest --cov=src tests/```

-----------

Path: Sophy_context.md

```
Path: .github/workflows/ci.yml

```yaml
# .github/workflows/ci.yml
name: TurtleTrader CI

on:
  push:
    branches: [ main, development ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
          pip install pytest pytest-cov
      - name: Run tests
        run: |
          pytest --cov=src tests/```

-----------

Path: config/settings.json

```json
// config/settings.json
{
  "mt5": {
    "login": 1520533067,
    "password": "YOUR_PASSWORD",
    "server": "FTMO-Demo2",
    "mt5_pathway": "C:\\Program Files\\FTMO MetaTrader 5\\terminal64.exe",
    "symbols": [
      "EURUSD",
      "XAUUSD",
      "US30"
    ],
    "symbol_mapping": {
      "US30": "US30.cash"
    },
    "timeframe": "H4",
    "account_balance": 100000
  },
  "risk": {
    "max_risk_per_trade": 0.015,
    "max_daily_drawdown": 0.05,
    "max_total_drawdown": 0.10,
    "leverage": 30
  },
  "strategy": {
    "name": "turtle_trader",
    "swing_mode": true,
    "entry_period": 40,
    "exit_period": 20,
    "atr_period": 20,
    "atr_multiplier": 2.5
  },
  "logging": {
    "log_file": "logs/trading_log.csv",
    "log_level": "INFO"
  },
  "output": {
    "data_dir": "data"
  }
}```

-----------

Path: config/strategy_config.json

```json
# config/strategy_config.json
{
"turtle_trader": {
"entry_period": 40,
"exit_period": 20,
"atr_period": 20,
"atr_multiplier": 2.5,
"swing_mode": true,
"use_trend_filter": true
}
}```

-----------

Path: docs/FTMO_Rules.txt

```plaintext
1/15
FTMO GENERAL TERMS AND CONDITIONS
These FTMO General Terms and Conditions (the “GTC”) govern rights and obligations in connection
with the use of services provided by FTMO Evaluation Global s.r.o. (the “Services”), offered mainly
through the www.ftmo.com website (the “Website”). Please read these GTC carefully. You are
under no obligation to use the Services if you do not agree or understand any portion of these Terms,
nor should you use the Services unless you understand and agree to these Terms.
1. INTRODUCTORY PROVISIONS
1.1. These GTC govern your (“you”, “your”, or the “Customer”) rights and obligations in
connection with the use of the Services provided by FTMO Evaluation Global s.r.o., with
its registered office at Purkyňova 2121/3, Nové Město, 110 00 Prague 1, Czech Republic,
identification no.: 092 13 651, registered in the Commercial Register maintained
by the Municipal Court in Prague, file no. C 332660 (“we”, “our”, or the “Provider”).
1.2. By registering on the Website or, where registration is not required, not later than by your
first use of the Services, you are entering into a contract with the Provider, the subject of
which is the provision of the Services of your choice. The GTC form an integral part of
such a contract and, by executing the contract with the Provider, you express your
agreement to these GTC.
1.3. The Services are only intended for persons over the age of 18 residing in the country
for which the Services are available. By registering on the Website, you confirm that you
are over 18 years of age. If you are under 18 years of age, you may not use the Services.
You undertake to access the Services solely from one of the countries for which
the Services are available. You acknowledge that your access to and use of the Services
may be restricted or prohibited by law in some countries, and you undertake to only access
and use the Services in accordance with applicable laws.
1.4. The Provider shall not provide Services to Customer that: (i) is of nationality or is residing
in Restricted Jurisdictions; (ii) is established or incorporated, or has a registered office in
Restricted Jurisdictions; (iii) is subject to the relevant international sanctions; or (iv) has
a criminal record related to financial crime or terrorism. Restricted Jurisdictions means
countries determined as such by the Provider and published here on the Website. The
Provider reserves the right to refuse, restrict or terminate the provision of any Services to
Customer as per this Clause 1.4. and such Customer is prohibited to use the Services,
which also includes the use of the Client Section and/or Trading Platform.
1.5. The Services consist of the provision of tools for simulated foreign exchange trading
on the FOREX market or simulated trading with other instruments on other financial
markets, provision of analytical tools, training and educational materials, the access to
the Client Section, and other ancillary services, in particular through the Client Section or
by the provision of access to applications provided by the Provider or third parties.
Financial market information is used in the simulated trading; however, you acknowledge
that any trading that you perform through the Services is not real. You also acknowledge
that the funds provided to you for demo trading are fictitious and that you have no right
to possess those fictitious funds beyond the scope of their use within the Services, and in
particular that they may not be used for any actual trading and that you are not entitled
to the payment of those funds. Unless expressly agreed otherwise, you will not be paid
any remuneration or profits based on the results of your simulated trading, nor will you
be required to pay any losses.
1.6. NONE OF THE SERVICES PROVIDED TO YOU BY THE PROVIDER CAN BE CONSIDERED
INVESTMENT SERVICES IN ACCORDANCE WITH APPLICABLE LAWS. THE PROVIDER DOES
NOT GIVE OR PROVIDE TO YOU ANY GUIDANCE, INSTRUCTIONS, OR INFORMATION
ABOUT HOW OR IN WHICH MANNER YOU SHOULD PERFORM TRANSACTIONS WHEN
USING THE SERVICES OR OTHERWISE, OR ANY OTHER SIMILAR INFORMATION ABOUT
THE INVESTMENT TOOLS TRADED, NOR DOES THE PROVIDER ACCEPT ANY SUCH
GUIDANCE, INSTRUCTIONS, OR INFORMATION FROM YOU. NONE OF THE SERVICES
CONSTITUTE INVESTMENT ADVICE OR RECOMMENDATIONS. NO EMPLOYEES, STAFF, OR
REPRESENTATIVES OF THE PROVIDER ARE AUTHORIZED TO PROVIDE INVESTMENT
ADVICE OR RECOMMENDATIONS. SHOULD ANY INFORMATION OR STATEMENT OF ANY
EMPLOYEE, STAFF, OR REPRESENTATIVES OF THE PROVIDER BE INTERPRETED AS
2/15
INVESTMENT ADVICE OR RECOMMENDATIONS, THE PROVIDER EXPLICITLY DISCLAIMS
THAT THE SAME IS INVESTMENT ADVICE OR RECOMMENDATIONS AND SHALL NOT BE
RESPONSIBLE FOR THEM.
1.7. Your personal data is processed in accordance with the Privacy Policy.
1.8. The meaning of the definitions, expressions, and abbreviations used in these GTC can be
found in clause 18.
2. SERVICES AND THEIR ORDER
2.1. You can order the Services through the Website by completing the appropriate registration
or order form. After registration, we will e-mail you the login details for the Client Section
and/or Trading Platform and allow you to access them.
2.2. The Services include, among other things, the Free Trial, FTMO Challenge, and Verification
products; these products may differ in the scope of the Services provided
(e.g., by analytical tools available to the Customer). With the Free Trial, you may use
some of the Services within a limited scope and for a limited period free of charge.
Completing the Free Trial does not entitle you to access any other Services.
2.3. All data that you provide to us through the registration or order form, the Client Section,
or otherwise must be complete, true, and up to date. You must immediately notify us
of any change in your data or update the data in your Client Section. The Customer is
responsible for all the provided data being accurate and up to date; the Provider is not
obligated to verify the data.
2.4. You acknowledge that if you provide an identification number, tax registration number
or other similar information in the registration or order form or in the Client Section,
or if you state that you are a legal entity, you will be considered as an entrepreneur
(trader) for the purposes of these GTC and when using the Services, and the provisions
of these GTC or the applicable law that grant rights to consumers will not apply to you.
2.5. The fee for the FTMO Challenge varies according to the option selected and depends on
the amount of the initial capital, the degree of the acceptable risk, the parameters that
must be fulfilled so that the conditions of the FTMO Challenge and the subsequent
Verification are met, and possibly other configurations. More detailed information on
individual options and fees for those options are provided on our Website here. The final
fee will be determined based on the option you select when completing the form for
ordering the FTMO Challenge. The Provider reserves the right to also provide the Services
under individually agreed conditions. All individually agreed conditions shall be determined
by the Provider at its own discretion. Individual discounts and other benefits may not be
combined, unless expressly stipulated otherwise by the Provider.
2.6. The fee is paid for allowing you to access the FTMO Challenge, or the Services provided
under the FTMO Challenge. The Customer is not entitled to a refund of the fee, for
example, if the Customer cancels the Customer’s Client Section or requests the
cancellation by e-mail, if the Customer terminates the use of the Services or the contract
(for example, fails to complete the FTMO Challenge or the Verification), fails to meet the
conditions of the FTMO Challenge or the Verification, or violates these GTC.
2.7. If the Customer lodges an unjustifiable complaint regarding the paid fee or disputes
the paid fee with the Customer’s bank or payment service provider (e.g. through
chargeback services, dispute services, or other similar services), on the basis of which
an annulment, cancellation or refund of the fee or any part thereof is requested,
the Provider is entitled, at its own discretion, to stop providing to the Customer any
services and refuse any future provision of any services.
2.8. Your choice of the option of the FTMO Challenge that you select when making an order
shall also apply to the subsequent Verification. You will start the subsequent Verification
and, possibly, other products related thereto, with the parameters and the same currency
that correspond to the option of the FTMO Challenge selected by you. Once you make a
selection, it is not possible to change it.
If you are ordering a new FTMO Challenge, the restrictions specified in this clause 2.8
shall not apply.
3/15
2.9. The Provider reserves the right to unilaterally change the fees and parameters
of the Services at any time, including the parameters for their successful completion.
The change does not affect the Services purchased before the change is notified.
2.10. Any data entered in the order form can be checked, corrected, and amended until
the binding order of the Services. The order of the Services of your choice is made by
submitting the order form. The Provider will immediately confirm the receipt of your order
to your e-mail address. In the case of the Free Trial, the order is completed upon the
delivery of the confirmation to your e-mail address, whereby the contract is executed.
In the case of the FTMO Challenge, the order is completed upon the payment of the fee
for the selected option (more on this in clause 3.4), whereby the contract between you
and the Provider is executed, the subject of which is the provision of the FTMO Challenge
and, if the conditions of the FTMO Challenge are met, the Verification. The contract is
concluded in English. We archive the contract in electronic form and do not allow access
to it.
2.11. You acknowledge that in order to use our Services, you must obtain the appropriate
technical equipment and software, including third-party software (e.g., software for
the use of the Trading Platform), at your own risk and expense. The Website is accessible
from the most commonly used web browsers. The internet access, purchase of the
equipment, and purchase of the web browser and its updates are at your own risk
and expense. The Provider does not warrant or guarantee that the Services will be
compatible with any specific equipment or software. The Provider does not charge any
additional fees for the internet connection.
2.12. You acknowledge that the operators of trading platforms are persons or entities different
from the Provider and that their own terms and conditions and privacy policies will apply
when you use their services and products. Before sending an order form, you are obligated
to read those terms and conditions and privacy policies.
2.13. If the Customer places an unusually large number of orders for the Services within an
unreasonably short period of time, the Provider may notify the Customer through the
Client Section as a protective precaution to mitigate potentially harmful behaviour of the
Customer. If such unreasonable behaviour continuous after such notice, we reserve the
right to suspend any further orders of the Services by the Customer. If we identify that
the unusual behaviour as per this paragraph relates to the Customer’s involvement in
Forbidden Trading Practices, we may take respective actions as perceived in Section 5 of
this GTC. The Provider reserves the right to determine, at its own discretion, the nature
of the behaviour described above and reasonable boundaries for such determination.
3. PAYMENT TERMS
3.1. The amounts of fees for the FTMO Challenge options are in euros. The fee can also be paid
in other currencies that are listed on the Website. If you select any other currency than
the euro, the amount of the fee for the selected option of the FTMO Challenge shall be
converted by our rates and it will automatically display your payment total in your chosen
currency, so you know how much you are paying before you confirm the order. The
Customer acknowledges that if the payment is made in a currency other than the one the
Customer has chosen on the Website, the amount will be converted according to the
current exchange rates valid at the time of payment.
3.2. Service charges are inclusive of all taxes. If the Customer is an entrepreneur (trader), he
is obliged to fulfil all his tax obligations in connection with the use of our Services in
accordance with applicable law, and in the event of an obligation, he is obliged to pay tax
or other fees properly.
3.3. You can pay the fee for the selected option of the FTMO Challenge by a payment card, via
a bank transfer, or using other means of payment that the Provider currently offers on the
Website.
3.4. In the event of payment by a payment card or via any other express payment method,
the payment shall be made immediately. If you select a bank transfer for payment, we
will subsequently send you a proforma invoice in electronic form with the amount of the
fee for the option of the FTMO Challenge you have chosen on the Website. You undertake
to pay the amount within the period specified in the proforma invoice. The fee is
considered paid when its full amount is credited to the Provider’s account. If you do not
4/15
pay the amount on time, the Provider is entitled to cancel your order. Customer bears all
fees charged to Customer by the selected payment service provider (according to the valid
pricelist of the payment service provider) in connection with the transaction and the
Customer is obliged to ensure that the respective fee for the selected FTMO Challenge is
paid in full.
4. CLIENT SECTION AND TRADING PLATFORM
4.1. Only one Client Section is permitted per Customer and all of the Customer’s Services must
be maintained in the Client Section.
4.2. The total number of FTMO Challenges and Verifications per one Client Section may be
limited depending on the total sum of the initial capital amounts of the products ordered
by the Customer or on the basis of other parameters. Unless the Provider grants an
exception to the Customer, the initial capital amounts may not be transferred between the
individual products or mutually combined. You may also not transfer or combine your
performance, Service parameters, data, or any other information between the products.
4.3. Access to the Client Section and Trading Platform is protected by login data, which
the Customer may not make available or share with any third party. If the Customer has
registered as a legal entity, the Customer may allow the use of the Services through the
Customer’s Client Section to the authorized employees and representatives. The Customer
is responsible for all activities that are performed through the Customer’s Client Section
or Trading Platform. The Provider bears no responsibility, and the Customer is not entitled
to any compensation, for any misuse of the Client Section, Trading Platform, or any part
of the Services, nor is the Provider responsible for any negative consequences thereof for
the Customer, if such misuse occurs for any reasons on the part of the Customer.
4.4. The Customer acknowledges that the Services may not be available around the clock,
particularly with respect to maintenance, upgrades, or any other reasons. In particular,
the Provider bears no responsibility, and the Customer is not entitled to any compensation,
for the unavailability of the Client Section or Trading Platform and for damage or loss
of any data or other content that Customer uploads, transfers or saves through the Client
Section or Trading Platform.
4.5. The Customer may at any time request the cancellation of the Client Section by sending
an e-mail to support@ftmo.com. Sending a request for the cancellation of the Client
Section is considered as a request for termination of the contract by the Customer, with
the Customer being no longer entitled to use the Services, including the Client Section
and Trading Platform. The Provider will immediately confirm the receipt of the request to
the Customer by e-mail, whereby the contractual relationship between the Customer and
the Provider will be terminated. In such a case, the Customer is not entitled to any refund
of the fees already paid or costs otherwise incurred.
5. RULES OF DEMO TRADING
5.1. During the demo trading on the Trading Platform, you may perform any transactions,
unless these constitute forbidden trading strategies or practices within the meaning
of clause 5.4. You also agree to follow good market standard rules and practices for trading
on financial markets (e.g., risk management rules). Restrictions may also be imposed by
the trading conditions of the Trading Platform that you have selected for trading.
5.2. You acknowledge that the Provider has access to information about the demo trades that
you perform on the Trading Platform. You grant the Provider your consent to share this
information with persons/entities who are in a group with the Provider or who are
otherwise affiliated with the Provider, and you grant the Provider and these
persons/entities your consent and authorization to handle this information at their own
will. You agree that these activities may be performed automatically without any further
consent, consultation, or approval on your part being necessary, and that you are not
entitled to any remuneration or revenue associated with the use of the data
by the Provider. The Provider is aware that you do not provide the Provider with any
investment advice or recommendations through your demo trading. You acknowledge that
you may suspend your demo trading on the Trading Platform at any time.
5/15
5.3. The Provider bears no responsibility for the information displayed on the Trading Platform,
nor for any interruption of, or delay or inaccuracy in the market information displayed
through your Client Section.
5.4. FORBIDDEN TRADING PRACTICES.
5.4.1. DURING THE DEMO TRADING, IT IS PROHIBITED TO:
(a) KNOWINGLY OR UNKNOWINGLY USE TRADING STRATEGIES THAT
EXPLOIT ERRORS IN THE SERVICES SUCH AS ERRORS IN DISPLAY
OF PRICES OR DELAY IN THEIR UPDATE;
(b) PERFORM TRADES USING AN EXTERNAL OR SLOW DATA FEED;
(c) PERFORM, ALONE OR IN CONCERT WITH ANY OTHER PERSONS,
INCLUDING BETWEEN CONNECTED ACCOUNTS, OR ACCOUNTS HELD
WITH DIFFERENT FTMO ENTITIES, TRADES OR COMBINATIONS OF
TRADES THE PURPOSE OF WHICH IS TO MANIPULATE TRADING, FOR
EXAMPLE BY SIMULTANEOUSLY ENTERING INTO OPPOSITE POSITIONS;
(d) PERFORM TRADES IN CONTRADICTION WITH THE TERMS AND
CONDITIONS OF THE PROVIDER AND THE TRADING PLATFORM;
(e) USE ANY SOFTWARE, ARTIFICIAL INTELLIGENCE, ULTRA-HIGH SPEED,
OR MASS DATA ENTRY WHICH MIGHT MANIPULATE, ABUSE, OR GIVE
YOU AN UNFAIR ADVANTAGE WHEN USING OUR SYSTEMS OR
SERVICES;
(f) PERFORM GAP TRADING BY OPENING TRADE(S):
(I) WHEN MAJOR GLOBAL NEWS, MACROECONOMIC EVENT OR
CORPORATE REPORTS OR EARNINGS (“EVENTS”), THAT MIGHT
AFFECT THE RELEVANT FINANCIAL MARKET (I.E. MARKET THAT
ALLOWS TRADING OF FINANCIAL INSTRUMENTS THAT MIGHT BE
AFFECTED BY THE EVENTS), ARE SCHEDULED; AND
(II)2 HOURS OR LESS BEFORE A RELEVANT FINANCIAL MARKET IS
CLOSED FOR 2 HOURS OR LONGER.; OR
(g) OTHERWISE PERFORM TRADES IN CONTRADICTION WITH HOW
TRADING IS ACTUALLY PERFORMED IN THE FOREX MARKET OR IN ANY
OTHER FINANCIAL MARKET, OR IN A WAY THAT ESTABLISHES
JUSTIFIED CONCERNS THAT THE PROVIDER MIGHT SUFFER FINANCIAL
OR OTHER HARM AS A RESULT OF THE CUSTOMER’S ACTIVITIES (E.G.
OVERLEVERAGING, OVEREXPOSURE, ONE-SIDED BETS, ACCOUNT
ROLLING).
5.4.2. As our Customer, you should understand and agree that all our Services are
for Customer’s personal use only, meaning that only you personally can access
your FTMO Challenge and Verification accounts and perform trades. For that
reason, you should not, and you agree not to,
(a) allow access to and trading on your FTMO Challenge and Verification
accounts by any third party nor you shall engage or cooperate with any
third party in order to have such third party perform trades for you,
whether such third party is a private person or a professional;
(b) access any third-party FTMO Challenge and Verification accounts, trade
on behalf of any third party or perform any account management or
similar services, where you agree to trade, operate or manage the FTMO
Challenge and Verification accounts on behalf of another user, all whether
performed as a professional or otherwise.
Please note that if you act or behave in contradiction with the aforesaid, we
will consider such action/behaviour as a Forbidden Trading Practice under
Section 5.4. with respective consequences as perceived under this GTC.
5.4.3. Furthermore, Customer shall not exploit the Services by performing trades
without applying market standard risk management rules for trading on
financial markets, this includes, among others, the following practices (i)
opening substantially larger position sizes compared to Customer’s other
6/15
trades, whether on this or any other Customer’s account, or (ii) opening
substantially smaller or larger number of positions compared to Customer’s
other trades, whether on this or any other Customer’s account.
The Provider reserves the right to determine, at its own discretion, whether certain trades,
practices, strategies, or situations are Forbidden Trading Practices.
5.5. If the Customer engages in any of the Forbidden Trading Practices described in clause 5.4,
(i) the Provider may consider it as a failure to meet the conditions of the particular FTMO
Challenge or Verification, (ii) the Provider may remove the transactions that violate
the prohibition from the Customer’s trading history and/or not count their results in the
profits and/or losses achieved by the demo trading, (iii) to immediately cancel all Services
provided to the Customer and subsequently terminate this contract, or (iv) reduce the
offered leverage on products to 1:5 on any or all Customer’s accounts.
5.6. In case when some or all Forbidden Trading Practices are executed on one or more FTMO
Challenge and Verification accounts of one Customer, or accounts of various Customers,
or by combining trading through FTMO Challenge and Verification accounts and FTMO
Trader accounts, then the Provider is entitled to cancel all Services and terminate all
respective contracts related to any and all Customer’s FTMO Challenge and Verification
accounts and/or apply other measures in Clause 5.5. The Provider may exercise any and
all actions in Clauses 5.5 and 5.6 at its own discretion.
5.7. If any FTMO Trader accounts were used for or were involved in the Forbidden Trading
Practices, this may and will constitute a breach of respective terms and conditions for
FTMO Trader account with third-party provider and may result in cancellation of all such
user accounts and termination of respective agreements by the third-party provider.
5.8. If the Customer engages in any of the practices described in clause 5.4 repeatedly,
and the Provider has previously notified the Customer thereof, the Provider may prevent
the Customer from accessing all Services or their parts, including access to the Client
Section and Trading Platform, without any compensation. In such a case, the Customer is
not entitled to a refund of the fees paid.
5.9. The Provider does not bear any responsibility for trading or other investment activities
performed by the Customer outside the relationship with the Provider, for example
by using data or other information from the Client Section, Trading Platform, or otherwise
related to the Services in real trading on financial markets, not even if the Customer uses
for such trading the same Trading Platform that the Customer uses for demo trading.
5.10. DEVELOPMENTS IN FINANCIAL MARKETS ARE SUBJECT TO FREQUENT AND ABRUPT
CHANGES. TRADING ON FINANCIAL MARKETS MAY NOT BE PROFITABLE AND CAN LEAD
TO SIGNIFICANT FINANCIAL LOSSES. ANY PREVIOUS PERFORMANCES AND PROFITS OF
THE CUSTOMER’S DEMO TRADING ARE NOT A GUARANTEE OR INDICATION OF ANY
FURTHER PERFORMANCE.
6. FTMO CHALLENGE AND VERIFICATION
6.1. After paying the fee for the selected option of the FTMO Challenge, the Customer will
receive the relevant login data for the Trading Platform at the e-mail address provided by
the Customer or in the Client Section. The Customer activates the FTMO Challenge by
opening the first demo trade in the Trading Platform. YOU ACKNOWLEDGE THAT,
BY OPENING THE FIRST DEMO TRADE, YOU EXPRESSLY DEMAND THE PROVIDER
TO PROVIDE COMPLETE SERVICES. IF YOU ARE A CONSUMER, IT MEANS THE
COMPLETION OF SERVICES BEFORE THE EXPIRY OF THE PERIOD FOR WITHDRAWAL
FROM THE CONTRACT, WHICH AFFECTS YOUR RIGHT TO WITHDRAW FROM
THE CONTRACT, AS SPECIFIED IN MORE DETAIL IN CLAUSE 12. If you do not activate the
FTMO Challenge within 30 calendar days of the date on which it was made available to
you, your access to it will be suspended. You can request the renewal of access via the
Client Section or by sending an e-mail to support@ftmo.com within 6 months of the initial
suspension, otherwise we will terminate the provision of the Services without any right to
a refund of the fee.
6.2. In order for the Customer to meet the conditions of the FTMO Challenge, the Customer
must fulfil all of the following parameters at the same time:
7/15
6.2.1. the Customer has opened at least one demo trade on at least four different
calendar days;
6.2.2. in the course of none of the calendar days during the FTMO Challenge did
the Customer report a loss on any demo trades opened and closed on that
day, which would exceed the percentage of the initial capital for the
respective option as described below:
FTMO Challenge FTMO Challenge
Aggressive FTMO Challenge Swing
in total 5% of the
initial capital
in total 10% of the
initial capital
in total 5% of the
initial capital
6.2.3. at no time during the FTMO Challenge did the Customer report a loss on
any opened and closed demo transactions, which would exceed in total
the percentage of the initial capital for the respective option as described
below:
FTMO Challenge FTMO Challenge
Aggressive FTMO Challenge Swing
in total 10% of the
initial capital
in total 20% of the
initial capital
in total 10% of the
initial capital
6.2.4. the Customer is in a total profit on all closed demo trades amounting to
at least the percentage of the initial capital for the respective option as
described below:
FTMO Challenge FTMO Challenge
Aggressive FTMO Challenge Swing
in total 10% of the
initial capital
in total 20% of the
initial capital
in total 10% of the
initial capital
The above parameters are explained in more detail here on the Website.
6.3. If the Customer has met the conditions of the FTMO Challenge specified in clause 6.2, and
at the same time has not violated these GTC, in particular the rules of demo trading under
clause 5.4, the Provider will evaluate the FTMO Challenge as successful and will make the
Verification available to the Customer free of charge by sending login details to the
Customer’s e-mail address or Client Section. The Provider does not have to evaluate the
FTMO Challenge if the Customer has not closed all trades.
6.4. The Customer activates the Verification by opening the first demo trade in the Trading
Platform. If the Customer does not activate the Verification within 30 calendar days from
the day on which the Customer received the new login data, the Customer’s access to the
Verification will be suspended. The Customer may request the renewal of access via the
Client Section or by sending an e-mail to support@ftmo.com within 6 months of the
suspension, otherwise we will terminate the provision of the Services without any right to
a refund.
6.5. In order for the Customer to meet the conditions of the Verification, the Customer must
fulfil all of the following parameters at the same time:
6.5.1. during the Verification, the Customer has opened at least one demo trade
on at least four different calendar days;
8/15
6.5.2. in the course of none of the calendar days during the Verification did the
Customer report a loss on any demo trades opened and closed on that
day, which would exceed the percentage of the initial capital for the
respective option as described below:
Verification
Verification
Aggressive Verification Swing
in total 5% of the
initial capital
in total 10% of the
initial capital
in total 5% of the
initial capital
6.5.3. at no time during the Verification did the Customer report a loss on the
sum of the opened and closed demo trades, which would exceed in total
the percentage of the initial capital for the respective option as described
below:
Verification
Verification
Aggressive Verification Swing
in total 10% of the
initial capital
in total 20% of the
initial capital
in total 10% of the
initial capital
6.5.4. Customer is in total profit from all closed demo trades amounting to at
least the percentage of the initial capital for the respective option as
described below:
Verification Verification Aggressive Verification Swing
in total 5% of the
initial capital;
in total 10% of the
initial capital
in total 5% of the
initial capital
The above parameters are explained in more detail here on the Website.
6.6. For the Customer to meet conditions of the Verification, the Customer shall comply with
the following:
6.6.1. Customer has met the conditions of the Verification specified in clause
6.5;
6.6.2. Customer has not violated these GTC, in particular, the rules of demo
trading under clause 5.4; and
6.6.3. Customer has not exceeded the maximum total amount of the capital
allocation of USD 400,000 (USD 200,000 for the Aggressive option),
individually or in combination, per Customer or per each trading strategy,
within the meaning of applicable FTMO Trader Program agreement, if
Customer is already participating in the FTMO Trader Program.
If the above conditions are met, the Provider will evaluate the Verification as successful
and will recommend the Customer as a candidate for FTMO Trader program. The Provider
does not have to evaluate the Verification if the Customer has not closed all transactions.
6.7. If during the FTMO Challenge the Customer does not comply with some of the conditions
specified in clause 6.2.2. or 6.2.3., the FTMO Challenge will be evaluated as unsuccessful,
and the Customer will not be allowed access to the subsequent Verification. If during the
Verification the Customer does not comply with any of the conditions specified in clause
6.5.2. or 6.5.3., the Verification will be evaluated as unsuccessful, and the Customer will
not be recommended as a candidate for the FTMO Trader program. In such cases, the
Customer’s account and Services will be cancelled without refund of fees already paid.
9/15
6.8. Provider recommending Customer as a candidate for the FTMO Trader Program in no way
guarantees Customer’s acceptance into the FTMO Trader Program. The Provider is not
responsible for Customer being rejected by the FTMO Trader Program for any or no reason.
7. FTMO TRADER
If the Customer is successful in both the Challenge and Verification, the Customer may be
offered a contract by a third-party company, in its sole discretion to participate in the
FTMO Trader Program. The terms, conditions, and agreement between the Customer and
a third-party company are strictly between the Customer and the third-party company.
FTMO Evaluation Global s.r.o. is in no way involved with the FTMO Trader Program
agreement—or lack thereof—executed between the third-party company and the
Customer. The Customer acknowledges their personal data may be shared with a thirdparty company for purposes of considering offering such a contract.
8. USE OF THE WEBSITE, SERVICES AND OTHER CONTENT
8.1. The Website and all Services, including the Client Section, their appearance
and all applications, data, information, multimedia elements such as texts, drawings,
graphics, design, icons, images, audio and video samples, and any other content that may
form the Website and the Services (collectively as the “Content”), are subject to legal
protection pursuant to copyright laws and other legal regulations and are the property of
the Provider or the Provider’s licensors. The Provider grants you limited, non-exclusive,
non-transferable, non-assignable, non-passable, and revocable permission to use the
Content for the purpose of using the Services for your personal use and in accordance
with the purpose for which the Services are provided. The Content is not sold or otherwise
transferred to you and remains the property of the Provider or the Provider’s licensors.
8.2. All trademarks, logos, trade names, and other designations are the property of the
Provider or Provider’s licensors, and the Provider does not grant you any authorization to
use them.
8.3. Both the Customer and the Provider undertake to act in accordance with the principles
of fair dealing in the performance of the contract and in mutual negotiations and, in
particular, not to damage the good reputation and legitimate interests of the other party.
The Customer and the Provider will resolve any possible disagreements or disputes
between them in accordance with these GTC and the applicable law.
8.4. Except for the rights expressly set out in these GTC, the Provider does not grant you any
other rights relating to the Services and other Content. You may only use the Services
and other Content as set out in these GTC.
8.5. When accessing the Services and other Content, the following is prohibited:
8.5.1. to use any tools that may adversely affect the operation of the
Website and Services or that would be intended to take advantage of
errors, bugs or other deficiencies of the Website and Services;
8.5.2. to circumvent geographical restrictions of availability or any other
technical restrictions;
8.5.3. to make copies or back-ups of the Website and other Content;
8.5.4. to reverse-engineer, decompile, disassemble or otherwise modify
the Website and other Content;
8.5.5. to sell, rent, lend, license, distribute, reproduce, spread, stream,
broadcast or use the Services or other Content otherwise than
as permitted;
8.5.6. to use automated means to view, display or collect information
available through the Website or Services; and
8.5.7. to use any other tools or means the use of which could cause
any damage to the Provider.
8.6. The provisions of clause 8 are not intended to deprive the Customer of the Customer’s
consumer rights which cannot be excluded by law.
10/15
9. DISCLAIMER
9.1. YOU ACKNOWLEDGE THAT THE SERVICES AND OTHER CONTENT ARE PROVIDED “AS IS”
WITH ALL THEIR ERRORS, DEFECTS AND SHORTCOMINGS, AND THAT THEIR USE IS AT
YOUR SOLE RESPONSIBILITY AND RISK. TO THE MAXIMUM EXTENT PERMITTED BY THE
MANDATORY LAWS, THE PROVIDER DISCLAIMS ANY STATUTORY, CONTRACTUAL,
EXPRESS, AND IMPLIED WARRANTIES OF ANY KIND, INCLUDING ANY WARRANTY OF
QUALITY, MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, OR NONINFRINGEMENT OF ANY RIGHTS.
9.2. TO THE EXTENT PERMITTED BY THE MANDATORY PROVISIONS OF THE APPLICABLE
LAWS, THE PROVIDER IS NOT RESPONSIBLE FOR ANY HARM, INCLUDING ANY INDIRECT,
INCIDENTAL, SPECIAL, PUNITIVE OR CONSEQUENTIAL DAMAGES, INCLUDING LOST
PROFIT, LOSS OF DATA, PERSONAL OR OTHER NON-MONETARY HARM OR PROPERTY
DAMAGE CAUSED AS A RESULT OF USE OF THE SERVICES OR RELIANCE ON ANY TOOL,
FUNCTIONALITY, INFORMATION OR ANY OTHER CONTENT AVAILABLE IN CONNECTION
WITH THE USE OF THE SERVICES OR ELSEWHERE ON THE WEBSITE. THE PROVIDER IS
NOT RESPONSIBLE FOR ANY PRODUCTS, SERVICES, APPLICATIONS OR OTHER THIRDPARTY CONTENT THAT THE CUSTOMER USES IN CONNECTION WITH THE SERVICES. IN
CASE THE PROVIDER’S LIABILITY IS INFERRED IN CONNECTION WITH THE OPERATION
OF THE WEBSITE OR PROVISION OF THE SERVICES BY A COURT OF JUSTICE OR ANY
OTHER COMPETENT AUTHORITY, THIS LIABILITY SHALL BE LIMITED TO THE AMOUNT
CORRESPONDING TO THE FEE PAID BY THE CUSTOMER FOR THE SERVICES IN
CONNECTION WITH WHICH THE CUSTOMER HAS INCURRED THE LOSS.
9.3. The Provider reserves the right to modify, change, replace, add, or remove any elements
and functions of the Services at any time without any compensation.
9.4. The Provider is not responsible for its failure to provide the purchased Services if that
failure occurs due to serious technical or operational reasons beyond the Provider’s
control, in the case of any crisis or imminent crisis, natural disaster, war, insurrection,
pandemic, a threat to a large number of people or other force majeure events, and/or
if the Provider is prevented from providing the Services as a result of any obligations
imposed by law or a decision of a public authority.
9.5. The provisions of Clause 9 are not intended to deprive the Customer of the Customer’s
consumer or other rights that cannot be excluded by law.
10. VIOLATION OF THE GTC
10.1. IF THE CUSTOMER VIOLATES ANY PROVISION OF THESE GTC IN A MANNER THAT MAY
CAUSE ANY HARM TO THE PROVIDER, IN PARTICULAR, IF THE CUSTOMER ACCESSES THE
SERVICES IN CONFLICT WITH CLAUSE 1.3 OR 1.4, IF THE CUSTOMER PROVIDES
INCOMPLETE, UNTRUE OR NON-UPDATED INFORMATION IN CONFLICT WITH CLAUSE 2.3,
IF THE CUSTOMER ACTS IN A MANNER THAT MAY DAMAGE THE PROVIDER’S GOOD
REPUTATION, IF THE CUSTOMER VIOLATES THE DEMO TRADING RULES PURSUANT TO
CLAUSE 5.4, IF THE CUSTOMER ACTS IN CONFLICT WITH CLAUSE 8.3, AND/OR
IF THE CUSTOMER PERFORMS ANY OF THE ACTIVITIES REFERRED TO IN CLAUSE 8.5,
THE PROVIDER MAY PREVENT THE CUSTOMER FROM ORDERING ANY OTHER SERVICES
AND COMPLETELY OR PARTIALLY RESTRICT THE CUSTOMER’S ACCESS TO ALL OR ONLY
SOME SERVICES, INCLUDING ACCESS TO THE CLIENT SECTION AND TRADING
PLATFORM, WITHOUT ANY PRIOR NOTICE AND WITHOUT ANY COMPENSATION.
11. COMMUNICATION
11.1. You acknowledge that all communication from the Provider or its partners in connection
with the provision of Services will take place through the Client Section or your e-mail
address, which you register with us. Written electronic communication by e-mail
or through the Client Section is also considered to be written communication.
11.2. Our contact e-mail address is support@ftmo.com and our contact address is Purkynova
2121/3, Prague 1, 11000, Czech Republic.
11/15
12. RIGHT TO WITHDRAW FROM A CONTRACT
12.1. If you are a consumer, you have the right to withdraw from a contract without giving a
reason within 14 days of its execution (see clause 2.10 for details on the time of execution
of the agreement). PLEASE NOTE THAT IF YOU START PERFORMING DEMO TRADES
BEFORE THE EXPIRY OF THE SPECIFIED TIME LIMIT, YOU LOSE YOUR RIGHT TO
WITHDRAW FROM THE CONTRACT.
12.2. Your withdrawal from the contract must be sent to our e-mail address support@ftmo.com
within the specified time limit. You can use the template form available here to withdraw.
We will confirm the receipt of the form to you in text form without undue delay. If you
withdraw from the contract, we will refund you without undue delay (no later than 14 days
after your withdrawal from the contract) all fees we have received from you, in the same
way in which you paid them.
12.3. The Provider is entitled to withdraw from the contract in the case of any breach by the
Customer specified in Clause 10. The withdrawal has effect from the day of its delivery to
the e-mail address of the Customer or through the Client Section.
13. DEFECTIVE PERFORMANCES
13.1. If the Services do not correspond to what was agreed or have not been provided to you,
you can exercise your rights from defective performance. The Provider does not provide
any guarantee for the quality of the services. You must notify us of the defect without
undue delay at our e-mail address or at our address listed in clause 11.2. When exercising
the rights from defective performance, you may request that we remedy the defect
or provide you with a reasonable discount. If the defect cannot be remedied, you can
withdraw from the contract or claim a reasonable discount.
13.2. We will try to resolve any complaint you may lodge as soon as possible (no later than
within 30 calendar days), and we will confirm its receipt and settlement to you in writing.
If we do not settle the complaint in time, you have the right to withdraw from the contract.
You can file a complaint by sending an e-mail to our e-mail address support@ftmo.com.
14. CHANGES TO THE GTC
14.1. The Provider reserves the right to change these GTC from time to time with effect for the
contract previously entered into by the Customer. The Provider will notify the Customer
of the change in the GTC at least 7 days before the change in the GTC is effective, via the
Client Section or by e-mail. If the Customer does not agree with the change, the Customer
is entitled to reject it. The Customer must do so no later than on the last business day
before these changes take effect by sending the rejection to our e-mail address
support@ftmo.com. Upon receiving such rejection, the contract will be terminated. If the
Customer does not reject the change, it is considered that the Customer agrees to the
new version of GTC.
14.2. If the change offers the Customer a new service or other additional functionalities or this
change is solely to their advantage, the Provider can inform the Customer about this
change less than 7 days before the effective date of such change, but no later than the
day before its effectiveness.
14.3. The Provider will mainly change these GTC for the following reasons:
14.3.1. to introduce new services or products or amend existing services or
products;
14.3.2. to reflect legal or regulatory requirements that apply to the Provider;
14.3.3. when the Provider will try to make these GTC easier to understand
or more helpful to the Customer;
14.3.4. to adjust the way our Services are provided, particularly if the change
is needed because of a change in the way the technology is provided
or background processes;
14.3.5. to reflect changes in the cost of running our business.
12/15
15. OUT-OF-COURT CONSUMER DISPUTE SETTLEMENT
15.1. It is our objective that our customers are satisfied with the FTMO services; therefore, if
you have any complaints or suggestions, we will be happy to resolve them directly with
you and you can contact us at our e-mail address or at our address listed in clause 11.2.
15.2. This section 15.2 applies only to a consumer who is at the same time an EU resident. The
Czech Trade Inspection Authority (Česká obchodní inspekce), with its registered office at
Štěpánská 567/15, 120 00 Prague 2, identification no.: 000 20 869, website:
https://www.coi.cz/en/information-about-adr/, is responsible for the out-of-court
settlement of consumer disputes. You can also use the platform at the following website
to resolve disputes online: https://www.ec.europa.eu/consumers/odr.
16. CHOICE OF LAW AND JURISDICTION
16.1. Any legal relations established by these GTC or related to them, as well as any related
non-contractual legal relations, shall be governed by the laws of the Czech Republic.
Any dispute that may arise in connection with these GTC and/or related agreements
will fall within the jurisdiction of the Czech court having local jurisdiction according to
the registered office of the Provider.
16.2. The provisions of clause 16.1 do not deprive the consumers of the protection afforded
to them by the mandatory laws of the relevant Member State of the European Union or any
other jurisdiction.
17. DURATION AND TERMINATION OF THE CONTRACT
17.1. The contract is concluded for a definite period until the FTMO Challenge or Verification is
passed or failed in accordance with the clause 6.2. or 6.5 respectively.
17.2. The contract may be terminated by either party earlier in accordance with these GTC. The
contract terminates automatically and with immediate effect in case the Customer during
FTMO Challenge or Verification does not open at least one demo trade during a period of
30 consecutive days.
17.3. Notwithstanding clause 17.2 the Provider may terminate this contract with cause and
immediate effect when the provision of Services under contract would affect the ability of
the Provider to adhere to its legal obligations or orders or decisions of a governmental
bodies or other regulators
17.4. Either Party may terminate this contract without cause by serving a written notice at least
7 days in advance in accordance with Clause 11 on the other Party.
18. FINAL PROVISIONS
18.1. The Provider has not adopted any consumers codes of conduct.
18.2. These GTC constitute the complete terms and conditions agreed between you and the
Provider and supersede all prior agreements relating to the subject matter of the GTC,
whether verbal or written.
18.3. Nothing in these GTC is intended to limit any legal claims set out elsewhere in these GTC
or arising from the applicable law. If the Provider or any third party authorized thereto
does not enforce the compliance with these GTC, this can in no way be construed
as a waiver of any right or claim.
18.4. The Provider may assign any claim arising to the Provider from these GTC
or any agreement to a third party without your consent. You agree that the Provider may,
as the assignor, transfer its rights and obligations under these GTC or any agreement
or parts thereof to a third party. The Customer is not authorized to transfer or assign
the Customer’s rights and obligations under these GTC or any agreements or parts
thereof, or any receivables arising from them, in whole or in part, to any third party.
18.5. If any provision of the GTC is found to be invalid or ineffective, it shall be replaced
by a provision whose meaning is as close as possible to the invalid provision. The invalidity
13/15
or ineffectiveness of one provision shall not affect the validity of the other provisions.
No past or future practice established between the parties and no custom maintained
in general or in the industry relating to the subject-matter of the performance, which is
not expressly referred to in the GTC, shall be applied and no rights and obligations shall
be derived from them for the parties; in addition, they shall not be taken into account
in the interpretation of manifestations of the will of the parties.
18.6. The schedules to the GTC form integral parts of the GTC. In the event of a conflict between
the wording of the main text of the GTC and any schedule thereof, the main text of the GTC
shall prevail.
18.7. Prior to the mutual acceptance of these GTC, the parties have carefully assessed
the possible risks arising from them and accept those risks.
19. DEFINITIONS, EXPRESSIONS AND ABBREVIATIONS USED
19.1. For the purposes of the GTC, the following definitions shall have the following meanings:
19.1.1. “Client Section” means the user interface located on the Website;
19.1.2. “Content” means the Website and all Services, including the Client
Section, their appearance and all applications, data, information,
multimedia elements such as texts, drawings, graphics, design,
icons, images, audio and video samples and other content that may
form the Website and the Services (as set out in clause 8.1);
19.1.3. “Customer” means the user of the Services (as set out in clause
1.1);
19.1.4. “Events” means events as set out in clause 5.4.1(f)(I);
19.1.5. “FTMO Challenge and Verification account” means trading
accounts related to trading education courses provided as part of the
Services by the Provider;
19.1.6. “FTMO Trader account” means a trading account, which relates to
the FTMO Trader program provided by a third-party provider;
19.1.7. “Forbidden Trading Practices” means trading practices strictly
forbidden while using our Services and are more detailed in Section
5.4 of these GTC;
19.1.8. “GTC” means these General Terms and Conditions of FTMO;
19.1.9. “Provider” means the provider of certain Services (as set out
in clause 1.1);
19.1.10. “Schedules” means Schedule 1 and any other Schedules as
applicable, which are part of these GTC;
19.1.11. “Services” means the Provider’s services as set out in clauses 1.1
and 1.5;
19.1.12. “Trading Platform” means an electronic interface provided
by a third party in which the Customer performs the demo trading;
and
19.1.13. “Website” means the website www.ftmo.com.
19.2. For the purposes of the GTC and their schedules, the following expressions
and abbreviations shall have the following meanings:
19.2.1. “calendar day” means the period from midnight to midnight
of the time currently valid in the Czech Republic (Central European
(Summer) Time, CE(S)T);
19.2.2. “initial capital” means a fictitious amount that the Customer has
chosen when selecting the option of the FTMO Challenge and which
the Customer will use to perform demo trading;
19.2.3. “CZK” means the Czech crown;
14/15
19.2.4. “EUR” means the euro;
19.2.5. “USD” means the United States dollar;
19.2.6. “GBP” means the British pound;
19.2.7. “CAD” means the Canadian dollar;
19.2.8. “AUD” means the Australian dollar;
19.2.9. “NZD” means the New Zealand dollar; and
19.2.10. “CHF” means the Swiss franc.
These GTC shall enter into force and effect on 13 July 2023.
15/15
SCHEDULE 1
OPTIONS OF FTMO CHALLENGES AND VERIFICATIONS
- FTMO Challenge or Verification with an initial capital of EUR 10,000 (or the corresponding
equivalent: USD 10,000, GBP 10,000, CZK 250,000, CHF 10,000, CAD 15,000 or AUD 15,000)
- FTMO Challenge or Verification Aggressive with an initial capital of EUR 10,000 (or the
corresponding equivalent: USD 10,000, GBP 10,000, CZK 250,000, CHF 10,000, CAD 15,000 or AUD
15,000)
- FTMO Challenge or Verification Swing with an initial capital of EUR 10,000 (or the corresponding
equivalent: USD 10,000, GBP 10,000, CZK 250,000, CHF 10,000, CAD 15,000 or AUD 15,000)
- FTMO Challenge or Verification with an initial capital of EUR 20,000 (or the corresponding
equivalent: USD 25,000, GBP 20,000, CZK 500,000, CHF 20,000, CAD 30,000 or AUD 30,000)
- FTMO Challenge or Verification Aggressive with an initial capital of EUR 20,000 (or the
corresponding equivalent: USD 25,000, GBP 20,000, CZK 500,000, CHF 20,000, CAD 30,000 or AUD
30,000)
- FTMO Challenge or Verification Swing with an initial capital of EUR 20,000 (or the corresponding
equivalent: USD 25,000, GBP 20,000, CZK 500,000, CHF 20,000, CAD 30,000 or AUD 30,000)
- FTMO Challenge or Verification with an initial capital of EUR 40,000 (or the corresponding
equivalent: USD 50,000, GBP 35,000, CZK 1,000,000, CHF 40,000, CAD 60,000 or AUD 65,000)
- FTMO Challenge or Verification Aggressive with an initial capital of EUR 40,000 (or the
corresponding equivalent: USD 50,000, GBP 35,000, CZK 1,000,000, CHF 40,000, CAD 60,000 or
AUD 65,000)
FTMO Challenge or Verification Swing with an initial capital of EUR 40,000 (or the corresponding
equivalent: USD 50,000, GBP 35,000, CZK 1,000,000, CHF 40,000, CAD 60,000 or AUD 65,000)
- FTMO Challenge or Verification with an initial capital of EUR 80,000 (or the corresponding
equivalent: USD 100,000, GBP 70,000, CZK 2,000,000, CHF 80,000, CAD 120,000 or AUD 130,000)
- FTMO Challenge or Verification Aggressive with an initial capital of EUR 80,000 (or the
corresponding equivalent: USD 100,000, GBP 70,000, CZK 2,000,000, CHF 80,000, CAD 120,000 or
AUD 130,000)
- FTMO Challenge or Verification Swing with an initial capital of EUR 80,000 (or the corresponding
equivalent: USD 100,000, GBP 70,000, CZK 2,000,000, CHF 80,000, CAD 120,000 or AUD 130,000)
- FTMO Challenge or Verification with an initial capital of EUR 160,000 (or the corresponding
equivalent: USD 200,000, GBP 140,000, CZK 4,000,000, CHF 160,000, CAD 240,000 or AUD
260,000)
- FTMO Challenge or Verification Swing with an initial capital of EUR 160,000 (or the corresponding
equivalent: USD 200,000, GBP 140,000, CZK 4,000,000, CHF 160,000, CAD 240,000 or AUD
260,000)```

-----------

Path: docs/README.md

```
# Sophy Trading System

Een professioneel algoritmisch trading systeem gebouwd in Python dat de Turtle Trading strategie implementeert via
MetaTrader 5, speciaal geoptimaliseerd voor FTMO-accounts.

## Kenmerken

- **Modulaire architectuur** - Duidelijke scheiding van verantwoordelijkheden
- **Meerdere strategieën** - Ondersteunt verschillende trading strategieën met een factory patroon
- **FTMO Compliance** - Ingebouwde controles voor naleving van FTMO-regels
- **Risicomanagement** - Geavanceerd positie-sizing en risicobeheer
- **Backtesting** - Uitgebreide backtesting mogelijkheden
- **Performance analyse** - Gedetailleerde rapportage en visualisatie

## Installatie

```bash
# Kloon de repository
git clone https://github.com/yourusername/sophy.git
cd sophy

# Installeer dependencies
pip install -r requirements.txt

# Optioneel: Installeer in development mode
pip install -e .```

-----------

Path: requirements.txt

```plaintext
��a n y i o = = 4 . 8 . 0  
 a r g o n 2 - c f f i = = 2 3 . 1 . 0  
 a r g o n 2 - c f f i - b i n d i n g s = = 2 1 . 2 . 0  
 a r r o w = = 1 . 3 . 0  
 a s t r o i d = = 3 . 3 . 8  
 a s t t o k e n s = = 3 . 0 . 0  
 a s y n c - l r u = = 2 . 0 . 4  
 a t t r s = = 2 4 . 3 . 0  
 b a b e l = = 2 . 1 6 . 0  
 b a c k t r a d e r = = 1 . 9 . 7 8 . 1 2 3  
 b e a u t i f u l s o u p 4 = = 4 . 1 2 . 3  
 b l a c k = = 2 5 . 1 . 0  
 b l e a c h = = 6 . 2 . 0  
 c e r t i f i = = 2 0 2 4 . 1 2 . 1 4  
 c f f i = = 1 . 1 7 . 1  
 c h a r s e t - n o r m a l i z e r = = 3 . 4 . 1  
 c l i c k = = 8 . 1 . 8  
 c o l o r a m a = = 0 . 4 . 6  
 c o m m = = 0 . 2 . 2  
 c o n t o u r p y = = 1 . 3 . 1  
 c y c l e r = = 0 . 1 2 . 1  
 d e b u g p y = = 1 . 8 . 1 1  
 d e c o r a t o r = = 5 . 1 . 1  
 d e f u s e d x m l = = 0 . 7 . 1  
 d i l l = = 0 . 3 . 9  
 e t _ x m l f i l e = = 2 . 0 . 0  
 e x e c u t i n g = = 2 . 1 . 0  
 f a s t j s o n s c h e m a = = 2 . 2 1 . 1  
 f o n t t o o l s = = 4 . 5 5 . 3  
 f q d n = = 1 . 5 . 1  
 h 1 1 = = 0 . 1 4 . 0  
 h t t p c o r e = = 1 . 0 . 7  
 h t t p x = = 0 . 2 8 . 1  
 i d n a = = 3 . 1 0  
 i p y k e r n e l = = 6 . 2 9 . 5  
 i p y t h o n = = 8 . 3 1 . 0  
 i p y w i d g e t s = = 8 . 1 . 5  
 i s o d u r a t i o n = = 2 0 . 1 1 . 0  
 i s o r t = = 6 . 0 . 1  
 j e d i = = 0 . 1 9 . 2  
 J i n j a 2 = = 3 . 1 . 5  
 j s o n 5 = = 0 . 1 0 . 0  
 j s o n p o i n t e r = = 3 . 0 . 0  
 j s o n s c h e m a = = 4 . 2 3 . 0  
 j s o n s c h e m a - s p e c i f i c a t i o n s = = 2 0 2 4 . 1 0 . 1  
 j u p y t e r = = 1 . 1 . 1  
 j u p y t e r - c o n s o l e = = 6 . 6 . 3  
 j u p y t e r - e v e n t s = = 0 . 1 1 . 0  
 j u p y t e r - l s p = = 2 . 2 . 5  
 j u p y t e r _ c l i e n t = = 8 . 6 . 3  
 j u p y t e r _ c o r e = = 5 . 7 . 2  
 j u p y t e r _ s e r v e r = = 2 . 1 5 . 0  
 j u p y t e r _ s e r v e r _ t e r m i n a l s = = 0 . 5 . 3  
 j u p y t e r l a b = = 4 . 3 . 4  
 j u p y t e r l a b _ p y g m e n t s = = 0 . 3 . 0  
 j u p y t e r l a b _ s e r v e r = = 2 . 2 7 . 3  
 j u p y t e r l a b _ w i d g e t s = = 3 . 0 . 1 3  
 k i w i s o l v e r = = 1 . 4 . 8  
 M a r k u p S a f e = = 3 . 0 . 2  
 m a t p l o t l i b = = 3 . 1 0 . 0  
 m a t p l o t l i b - i n l i n e = = 0 . 1 . 7  
 m c c a b e = = 0 . 7 . 0  
 M e t a T r a d e r 5 = = 5 . 0 . 4 7 3 8  
 m i s t u n e = = 3 . 1 . 0  
 m y p y = = 1 . 1 5 . 0  
 m y p y - e x t e n s i o n s = = 1 . 0 . 0  
 n b c l i e n t = = 0 . 1 0 . 2  
 n b c o n v e r t = = 7 . 1 6 . 5  
 n b f o r m a t = = 5 . 1 0 . 4  
 n e s t - a s y n c i o = = 1 . 6 . 0  
 n o t e b o o k = = 7 . 3 . 2  
 n o t e b o o k _ s h i m = = 0 . 2 . 4  
 n u m p y = = 2 . 2 . 1  
 o p e n p y x l = = 3 . 1 . 5  
 o v e r r i d e s = = 7 . 7 . 0  
 p a c k a g i n g = = 2 4 . 2  
 p a n d a s = = 2 . 2 . 3  
 p a n d o c f i l t e r s = = 1 . 5 . 1  
 p a r s o = = 0 . 8 . 4  
 p a t h s p e c = = 0 . 1 2 . 1  
 p i l l o w = = 1 1 . 1 . 0  
 p l a t f o r m d i r s = = 4 . 3 . 6  
 p r o m e t h e u s _ c l i e n t = = 0 . 2 1 . 1  
 p r o m p t _ t o o l k i t = = 3 . 0 . 4 8  
 p s u t i l = = 6 . 1 . 1  
 p u r e _ e v a l = = 0 . 2 . 3  
 p y c p a r s e r = = 2 . 2 2  
 P y g m e n t s = = 2 . 1 9 . 1  
 p y l i n t = = 3 . 3 . 4  
 p y p a r s i n g = = 3 . 2 . 1  
 p y t h o n - d a t e u t i l = = 2 . 9 . 0 . p o s t 0  
 p y t h o n - j s o n - l o g g e r = = 3 . 2 . 1  
 p y t z = = 2 0 2 4 . 2  
 p y w i n 3 2 = = 3 0 8  
 p y w i n p t y = = 2 . 0 . 1 4  
 P y Y A M L = = 6 . 0 . 2  
 p y z m q = = 2 6 . 2 . 0  
 r e f e r e n c i n g = = 0 . 3 5 . 1  
 r e q u e s t s = = 2 . 3 2 . 3  
 r f c 3 3 3 9 - v a l i d a t o r = = 0 . 1 . 4  
 r f c 3 9 8 6 - v a l i d a t o r = = 0 . 1 . 1  
 r p d s - p y = = 0 . 2 2 . 3  
 S e n d 2 T r a s h = = 1 . 8 . 3  
 s e t u p t o o l s = = 7 5 . 8 . 0  
 s i x = = 1 . 1 7 . 0  
 s n i f f i o = = 1 . 3 . 1  
 s o u p s i e v e = = 2 . 6  
 s t a c k - d a t a = = 0 . 6 . 3  
 t e r m i n a d o = = 0 . 1 8 . 1  
 t i n y c s s 2 = = 1 . 4 . 0  
 t o m l k i t = = 0 . 1 3 . 2  
 t o r n a d o = = 6 . 4 . 2  
 t q d m = = 4 . 6 7 . 1  
 t r a i t l e t s = = 5 . 1 4 . 3  
 t y p e s - p y t h o n - d a t e u t i l = = 2 . 9 . 0 . 2 0 2 4 1 2 0 6  
 t y p i n g _ e x t e n s i o n s = = 4 . 1 2 . 2  
 t z d a t a = = 2 0 2 4 . 2  
 u r i - t e m p l a t e = = 1 . 3 . 0  
 u r l l i b 3 = = 2 . 3 . 0  
 w c w i d t h = = 0 . 2 . 1 3  
 w e b c o l o r s = = 2 4 . 1 1 . 1  
 w e b e n c o d i n g s = = 0 . 5 . 1  
 w e b s o c k e t - c l i e n t = = 1 . 8 . 0  
 w i d g e t s n b e x t e n s i o n = = 4 . 0 . 1 3  
 X l s x W r i t e r = = 3 . 2 . 2  
 ```

-----------

Path: run.py

```python
# run.py
# !/usr/bin/env python3
import argparse
import os
import sys
from datetime import datetime


def setup_environment():
    """Zet de omgeving op voor het uitvoeren van de applicatie"""
    # Voeg de huidige directory toe aan het pythonpath
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Sophy Trading Bot')
    parser.add_argument('--config', type=str, help='Pad naar configuratiebestand')
    parser.add_argument('--backtest', action='store_true', help='Voer backtest uit in plaats van live trading')
    parser.add_argument('--strategy', type=str, help='Te gebruiken strategie')
    parser.add_argument('--symbols', type=str, help='Komma-gescheiden lijst van symbolen')

    return parser.parse_args()


def main():
    """Main entry point for the application"""
    print(f"Sophy Trading Bot - Gestart op {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Setup environment
    setup_environment()

    # Parse arguments
    args = parse_arguments()

    # Set config path if provided
    if args.config:
        os.environ['SOPHY_CONFIG_PATH'] = args.config
        print(f"Gebruik configuratiebestand: {args.config}")

    # Override strategy if provided
    if args.strategy:
        print(f"Overschrijven strategie: {args.strategy}")
        # Dit wordt later in het programma verwerkt

    # Override symbols if provided
    if args.symbols:
        symbols = args.symbols.split(',')
        print(f"Overschrijven symbolen: {symbols}")
        # Dit wordt later in het programma verwerkt

    # Run in backtest mode or live mode
    if args.backtest:
        print("Starten in backtest modus")
        from src.analysis.backtester import run_backtest
        run_backtest()
    else:
        print("Starten in live trading modus")
        from src.main import main as run_live
        run_live()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgramma onderbroken door gebruiker")
        sys.exit(0)
    except Exception as e:
        print(f"\nOnverwachte fout: {str(e)}")
        sys.exit(1)
```

-----------

Path: scripts/__init__.py

```python
```

-----------

Path: scripts/ftmo_check.py

```python
import json
import os
import sys

from utils.ftmo_helper import FTMOHelper


def load_config(config_path):
    """Laad configuratie uit JSON bestand"""
    try:
        with open(config_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Configuratiebestand niet gevonden: {config_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Ongeldige JSON in configuratiebestand: {config_path}")
        sys.exit(1)


def main():
    print("\n==== FTMO Compliance Checker ====")
    print("Dit programma controleert of je trading prestaties voldoen aan de FTMO regels.")

    # Controleer of logbestand bestaat
    log_file = os.path.join('../logs', 'trading_journal.csv')
    if not os.path.exists(log_file):
        print(f"\nError: Log bestand niet gevonden: {log_file}")
        print("Voer eerst de TurtleTrader bot uit om trading data te genereren.")
        return

    # Laad configuratie voor initiële balans
    config_path = os.path.join('Sophy/config', 'settings.json')
    try:
        config = load_config(config_path)
        initial_balance = config['mt5'].get('account_balance', 100000)
    except:
        print("\nWaarschuwing: Kon configuratie niet laden, standaard account balans van $100,000 wordt gebruikt.")
        initial_balance = 100000

    print(f"\nAnalyseren van trading data met initiële balans: ${initial_balance:,.2f}")

    # Initialiseer FTMO helper
    ftmo_helper = FTMOHelper(log_file)

    # Genereer rapport
    print("\nGenereren van gedetailleerd FTMO compliance rapport...")
    ftmo_helper.generate_trading_report(initial_balance)

    print("\nWil je nog meer details zien? (j/n): ", end="")
    if input().lower() == 'j':
        # Voer meer gedetailleerde analyse uit
        compliance = ftmo_helper.check_ftmo_compliance(initial_balance)

        if compliance['details']:
            details = compliance['details']
            daily_stats = details['daily_stats']

            print("\n===== Dagelijkse Statistieken =====")
            print(f"{'Datum':<12} {'Balance':<12} {'Dagelijkse P&L':<15} {'Drawdown':<12}")
            print("-" * 55)

            for _, row in daily_stats.iterrows():
                date_str = row['Date'].strftime('%Y-%m-%d')
                balance = f"${row['close_balance']:,.2f}"
                daily_pnl = f"${row['daily_pnl']:,.2f} ({row['daily_pnl_pct']:.2f}%)"
                drawdown = f"{row['daily_drawdown']:.2f}%"

                print(f"{date_str:<12} {balance:<12} {daily_pnl:<15} {drawdown:<12}")

            print("\nAls je voldoet aan alle FTMO regels, kun je doorgaan naar de volgende fase!")

    print("\nBedankt voor het gebruiken van de FTMO Compliance Checker.")


if __name__ == "__main__":
    main()
```

-----------

Path: scripts/main.py

```python
# src/main.py
import time
from datetime import datetime

from src.connector.mt5_connector import MT5Connector
from src.risk.risk_manager import RiskManager
from src.strategy.strategy_factory import StrategyFactory
from src.utils.config import load_config
from src.utils.logger import Logger


def main():
    """Hoofdfunctie voor de Sophy trading applicatie"""
    # Laad configuratie
    config = load_config()

    # Setup logging
    log_file = config['logging'].get('log_file', 'logs/trading_log.csv')
    logger = Logger(log_file)
    logger.log_info("====== Sophy Trading System ======")
    logger.log_info(f"Sessie gestart op {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Creëer componenten
    connector = MT5Connector(config['mt5'], logger)
    risk_manager = RiskManager(config['risk'], logger)

    # Verbind met MT5
    if not connector.connect():
        logger.log_info("Kon geen verbinding maken met MT5. Programma wordt afgesloten.", level="ERROR")
        return

    logger.log_info(f"Verbonden met MT5: {config['mt5']['server']}")

    # Haal strategie naam uit config
    strategy_name = config['strategy']['name']

    # Creëer strategie via factory
    try:
        strategy = StrategyFactory.create_strategy(strategy_name, connector, risk_manager, logger, config)
        logger.log_info(f"Strategie geladen: {strategy_name}")
    except ValueError as e:
        logger.log_info(f"Kon strategie '{strategy_name}' niet initialiseren: {str(e)}", level="ERROR")
        connector.disconnect()
        return

    # Hoofdloop
    try:
        logger.log_info("Trading loop gestart")

        # Log initiële account status
        account_info = connector.get_account_info()
        open_positions = strategy.get_open_positions() if hasattr(strategy, 'get_open_positions') else {}
        logger.log_status(account_info, open_positions)

        while True:
            # Verwerk symbolen volgens strategie
            for symbol in config['mt5']['symbols']:
                # Pas symbol mapping toe indien nodig
                symbol_map = config['mt5'].get('symbol_mapping', {})
                mapped_symbol = symbol_map.get(symbol, symbol)

                # Verwerk symbool
                strategy.process_symbol(mapped_symbol)

            # Controleer FTMO limieten
            account_info = connector.get_account_info()
            open_positions = strategy.get_open_positions() if hasattr(strategy, 'get_open_positions') else {}
            logger.log_status(account_info, open_positions)

            should_stop, reason = risk_manager.check_ftmo_limits(account_info)
            if should_stop:
                logger.log_info(f"Stop trading: {reason}")
                break

            # Wacht voor volgende cyclus
            interval = config.get('interval', 300)  # Default 5 minuten
            logger.log_info(f"Wacht {interval} seconden tot volgende cyclus")
            time.sleep(interval)

    except KeyboardInterrupt:
        logger.log_info("Trading gestopt door gebruiker.")
    except Exception as e:
        logger.log_info(f"Onverwachte fout: {str(e)}", level="ERROR")
    finally:
        # Cleanup
        connector.disconnect()
        logger.log_info("Sessie afgesloten.")


if __name__ == "__main__":
    main()
```

-----------

Path: setup.py

```python
# setup.py
from setuptools import setup, find_packages

setup(
    name="sophy",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.20.0",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "MetaTrader5>=5.0.0",
    ],
    author="Sophy Trading Systems",
    author_email="info@sophytrading.com",
    description="Een Python-gebaseerd algoritmisch trading systeem met Turtle Trading strategie",
    keywords="trading, algoritm, metatrader, ftmo, turtle",
    url="https://github.com/yourusername/sophy",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.9",
)
```

-----------

Path: src/__init__.py

```python
```

-----------

Path: src/analysis/__init__.py

```python
```

-----------

Path: src/analysis/backtester.py

```python
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.strategy.strategy_factory import StrategyFactory
from src.utils.config import load_config
from src.utils.logger import Logger


class DummyConnector:
    """Dummy connector voor backtest doeleinden met geavanceerde datahandling."""

    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.data_cache: Dict[str, pd.DataFrame] = {}

    def get_historical_data(self, symbol: str, timeframe_str: str, bars_count: int) -> pd.DataFrame:
        """Haal historische data op uit CSV bestanden met caching."""
        cache_key = f"{symbol}_{timeframe_str}"
        if cache_key in self.data_cache:
            df = self.data_cache[cache_key]
            return df.iloc[-bars_count:] if len(df) > bars_count else df.copy()

        filename = f"{symbol}_{timeframe_str}.csv"
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.exists(filepath):
            print(f"Bestand niet gevonden: {filepath}")
            return pd.DataFrame()

        df = pd.read_csv(filepath)
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        elif 'time' in df.columns:
            df['date'] = pd.to_datetime(df['time'])
            df.drop('time', axis=1, inplace=True)

        df.columns = [col.lower() for col in df.columns]
        required_cols = {'open', 'high', 'low', 'close', 'tick_volume'}
        if not all(col in df.columns for col in required_cols):
            print(f"Ongeldige data voor {symbol}: ontbrekende kolommen")
            return pd.DataFrame()

        self.data_cache[cache_key] = df
        return df.iloc[-bars_count:] if len(df) > bars_count else df.copy()

    def get_symbol_tick(self, symbol: str) -> Optional[Any]:
        """Simuleer huidige tick gebaseerd op laatste data."""
        cache_key = f"{symbol}_H4"
        if cache_key not in self.data_cache:
            self.get_historical_data(symbol, "H4", 1000)

        if cache_key not in self.data_cache:
            return None

        df = self.data_cache[cache_key]
        last_row = df.iloc[-1]

        class Tick:
            pass

        tick = Tick()
        tick.ask = last_row['close']
        tick.bid = last_row['close'] * 0.999  # Simpele bid/ask spread
        tick.time = last_row['date'].timestamp()
        return tick

    def get_account_info(self) -> Dict[str, Any]:
        """Geef geüpdatete accountinformatie tijdens backtest."""
        return {
            'balance': 100000,
            'equity': 100000,
            'margin': 0,
            'free_margin': 100000,
            'margin_level': 0,
            'profit': 0
        }

    def get_open_positions(self, symbol: Optional[str] = None) -> List[Dict]:
        """Geef open posities terug."""
        return [pos for pos in self.open_positions.values()] if symbol is None else \
            [pos for pos in self.open_positions.values() if pos.get('symbol') == symbol]

    def place_order(self, action: str, symbol: str, volume: float, stop_loss: float, take_profit: float,
                    comment: str) -> Optional[int]:
        """Simuleer het plaatsen van een order."""
        if action not in ['BUY', 'SELL']:
            return None
        ticket = len(self.open_positions) + 1
        self.open_positions[ticket] = {
            'ticket': ticket,
            'symbol': symbol,
            'type': mt5.POSITION_TYPE_BUY if action == 'BUY' else mt5.POSITION_TYPE_SELL,
            'volume': volume,
            'price_open': self.get_symbol_tick(symbol).ask if action == 'BUY' else self.get_symbol_tick(symbol).bid,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'time': datetime.now().timestamp(),
            'profit': 0.0
        }
        return ticket

    def modify_position(self, ticket: int, stop_loss: float, take_profit: float) -> bool:
        """Simuleer het aanpassen van een positie."""
        if ticket in self.open_positions:
            self.open_positions[ticket]['stop_loss'] = stop_loss
            self.open_positions[ticket]['take_profit'] = take_profit
            return True
        return False

    open_positions = {}


class BacktestStrategy:
    """Wrapper voor strategie tijdens backtesting met geavanceerde logica."""

    def __init__(self, strategy, initial_balance: float = 100000):
        self.strategy = strategy
        self.balance = initial_balance
        self.equity = initial_balance
        self.positions: Dict[int, Dict] = {}
        self.trades: List[Dict] = []
        self.logger = self.strategy.logger  # Gebruik de logger van de strategie

    def process_candle(self, symbol: str, candle: Dict[str, Any]) -> Dict[str, Any]:
        """Verwerk een enkele candle en simuleer trades."""
        result = {'signal': None, 'action': None}
        candle_df = pd.DataFrame([candle])
        indicators = self.strategy.calculate_indicators(candle_df)

        # Simuleer tick-gebaseerde data
        tick = self.strategy.connector.get_symbol_tick(symbol)
        if tick is None:
            return result

        process_result = self.strategy.process_symbol(symbol)
        if process_result.get('signal') == 'ENTRY' and process_result.get('action'):
            action = process_result['action']
            volume = process_result.get('volume', 0.1)
            stop_loss = process_result.get('stop_loss', 0)
            ticket = self.strategy.connector.place_order(action, symbol, volume, stop_loss, 0, "Backtest Trade")
            if ticket:
                self.positions[ticket] = {
                    'symbol': symbol,
                    'action': action,
                    'volume': volume,
                    'entry_price': tick.ask if action == 'BUY' else tick.bid,
                    'stop_loss': stop_loss,
                    'open_time': datetime.fromtimestamp(tick.time)
                }
                self.logger.log_trade(symbol, action, tick.ask, volume, stop_loss, 0, "Backtest Entry")
                result.update(process_result)

        # Beheer open posities
        for ticket, pos in list(self.positions.items()):
            current_price = tick.ask if pos['action'] == 'BUY' else tick.bid
            profit = (current_price - pos['entry_price']) * pos['volume'] * (1 if pos['action'] == 'BUY' else -1)
            pos['profit'] = profit
            self.equity = self.balance + sum(p['profit'] for p in self.positions.values())

            # Simuleer stop loss
            if (pos['action'] == 'BUY' and current_price <= pos['stop_loss']) or \
                    (pos['action'] == 'SELL' and current_price >= pos['stop_loss']):
                self.close_position(ticket, current_price)
                result['signal'] = 'EXIT'
                result['action'] = 'CLOSE'

        return result

    def close_position(self, ticket: int, close_price: float):
        """Sluit een positie en update balans."""
        if ticket in self.positions:
            pos = self.positions[ticket]
            profit = (close_price - pos['entry_price']) * pos['volume'] * (1 if pos['action'] == 'BUY' else -1)
            self.balance += profit
            self.trades.append({
                'symbol': pos['symbol'],
                'action': pos['action'],
                'entry_price': pos['entry_price'],
                'exit_price': close_price,
                'volume': pos['volume'],
                'profit': profit,
                'open_time': pos['open_time'],
                'close_time': datetime.now()
            })
            self.logger.log_trade(pos['symbol'], 'SELL' if pos['action'] == 'BUY' else 'BUY', close_price,
                                  pos['volume'], 0, 0, f"Backtest Exit, Profit: {profit:.2f}")
            del self.positions[ticket]


def run_backtest():
    """Voer een geavanceerde backtest uit met configuratie en analyse."""
    print("Backtester module gestart")

    # Laad configuratie
    config = load_config()

    # Setup logger
    log_file = config['logging'].get('log_file', 'logs/backtest_log.csv')
    logger = Logger(log_file)
    logger.log_info("====== Sophy Backtest Started ======")

    # Haal symbols en timeframe op
    symbols = config['mt5'].get('symbols', ['EURUSD'])
    timeframe = config['mt5'].get('timeframe', 'H4')
    start_date = config.get('backtest', {}).get('start_date',
                                                (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d'))
    end_date = config.get('backtest', {}).get('end_date', datetime.now().strftime('%Y-%m-%d'))

    # Setup dummy connector
    data_dir = config.get('data_dir', 'data')
    connector = DummyConnector(data_dir)
    connector.open_positions = {}  # Initialiseer open posities

    # Laad data
    data = {}
    for symbol in symbols:
        df = connector.get_historical_data(symbol, timeframe, 10000)
        if not df.empty:
            df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
            data[symbol] = df
            logger.log_info(
                f"Geladen: {symbol} {timeframe} - {len(df)} candles van {df['date'].min()} tot {df['date'].max()}")
        else:
            logger.log_info(f"Kon geen data laden voor {symbol} {timeframe}", level="ERROR")
            continue

    if not data:
        logger.log_info("Geen data geladen, backtest gestopt", level="ERROR")
        return

    # Maak strategie aan
    strategy_name = config['strategy'].get('name', 'turtle')
    strategy = StrategyFactory.create_strategy(strategy_name, connector, None, logger, config)
    if not strategy:
        logger.log_info(f"Kon strategie {strategy_name} niet aanmaken", level="ERROR")
        return

    backtest = BacktestStrategy(strategy)
    equity_curve = []

    # Voer backtest uit
    for symbol, df in data.items():
        for _, candle in df.iterrows():
            candle_dict = candle.to_dict()
            result = backtest.process_candle(symbol, candle_dict)
            equity_curve.append(backtest.equity)

            # Log status
            account_info = connector.get_account_info()
            account_info['equity'] = backtest.equity
            account_info['balance'] = backtest.balance
            logger.log_status(account_info, connector.get_open_positions())

    # Analyseer resultaten
    total_profit = backtest.balance - 100000
    trades = len(backtest.trades)
    winning_trades = sum(1 for t in backtest.trades if t['profit'] > 0)
    win_rate = (winning_trades / trades * 100) if trades > 0 else 0
    avg_profit = np.mean([t['profit'] for t in backtest.trades if t['profit'] > 0]) if winning_trades > 0 else 0
    avg_loss = np.mean([t['profit'] for t in backtest.trades if t['profit'] < 0]) if len(
        [t for t in backtest.trades if t['profit'] < 0]) > 0 else 0
    drawdown = min(0, min(equity_curve) - 100000) if equity_curve else 0

    logger.log_performance_metrics({
        'total_trades': trades,
        'winning_trades': winning_trades,
        'win_rate': win_rate,
        'avg_profit': avg_profit,
        'avg_loss': avg_loss,
        'total_profit': total_profit,
        'max_drawdown': drawdown,
        'trade_history': backtest.trades
    })

    # Visualiseer resultaten
    plt.figure(figsize=(12, 6))
    plt.plot(equity_curve, label='Equity Curve')
    plt.title(f'Backtest Resultaten - {strategy_name}')
    plt.xlabel('Candles')
    plt.ylabel('Equity')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(os.path.dirname(log_file), 'backtest_equity_curve.png'))
    plt.close()

    logger.log_info(
        f"Backtest voltooid. Totale winst: {total_profit:.2f}, Win Rate: {win_rate:.2f}%, Max Drawdown: {drawdown:.2f}")
    logger.log_info("====== Sophy Backtest Ended ======")


if __name__ == "__main__":
    run_backtest()
```

-----------

Path: src/analysis/optimizer.py

```python
# src/analysis/turtle_optimizer.py
import json
import logging
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union

import matplotlib.pyplot as plt

from src.analysis.advanced_backtester import Backtester
from src.utils.config import load_config
from src.utils.logger import Logger

# Configureer logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("turtle_optimizer")


class WalkForwardOptimizer:
    """
    Walk-Forward Optimalisatie voor handelssystemen om overfitting te voorkomen.

    Deze klasse implementeert walk-forward optimalisatie met verschillende in-sample/out-of-sample
    periodes om een robuustere set van parameters te vinden die goed generaliseert naar nieuwe data.
    """

    def __init__(self, config=None, logger=None):
        """
        Initialiseer de walk-forward optimizer.

        Parameters:
        -----------
        config : Optional[Dict]
            Configuratie dictionary (als None, dan wordt standaard config geladen)
        logger : Optional[Logger]
            Logger instantie (als None, dan wordt een nieuwe gemaakt)
        """
        self.config = config if config else load_config()
        self.logger = logger if logger else Logger(self.config['logging'].get('log_file', 'logs/optimizer_log.csv'))

        # Output directory
        self.output_dir = self.config.get('output', {}).get('data_dir', 'data/optimization')
        os.makedirs(self.output_dir, exist_ok=True)

        # Maak backtester
        self.backtester = Backtester(self.config, self.logger)

        # Visuele stijl instellen
        plt.style.use('ggplot')
        plt.rcParams['figure.figsize'] = (16, 10)

    def optimize(self, strategy_name: str, symbols: List[str], timeframe: str,
                 param_ranges: Dict[str, List[Any]],
                 start_date: Union[str, datetime], end_date: Union[str, datetime],
                 is_period_days: int = 180, oos_period_days: int = 60,
                 windows: int = 3, metric: str = 'sharpe_ratio',
                 min_trades: int = 10, max_workers: Optional[int] = None) -> Dict[str, Any]:
        """
        Voer walk-forward optimalisatie uit.

        Parameters:
        -----------
        strategy_name : str
            Naam van de strategie
        symbols : List[str]
            Lijst met handelssymbolen
        timeframe : str
            Timeframe voor analyse
        param_ranges : Dict[str, List[Any]]
            Dictionary met parameter namen en mogelijke waarden
        start_date : Union[str, datetime]
            Start datum voor gehele test periode
        end_date : Union[str, datetime]
            Eind datum voor gehele test periode
        is_period_days : int
            Aantal dagen voor in-sample periode
        oos_period_days : int
            Aantal dagen voor out-of-sample periode
        windows : int
            Aantal walk-forward windows
        metric : str
            Prestatiemetric om te optimaliseren
        min_trades : int
            Minimum aantal trades voor een geldige test
        max_workers : Optional[int]
            Maximum aantal workers voor parallellisatie

        Returns:
        --------
        Dict[str, Any] : Resultaten van de walk-forward optimalisatie
        """
        self.logger.log_info(f"===== Starten Walk-Forward Optimalisatie: {strategy_name} =====")
        self.logger.log_info(f"Symbolen: {symbols}, Timeframe: {timeframe}")
        self.logger.log_info(f"Optimalisatie metric: {metric}")

        # Converteer data naar datetime
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # Bereken tijdsperiodes
        total_days = (end_date - start_date).days
        window_size = is_period_days + oos_period_days

        if windows * window_size > total_days:
            windows = total_days // window_size
            self.logger.log_info(f"Aangepast aantal windows naar {windows} om binnen datumbereik te passen")

        if windows < 1:
            self.logger.log_info("Datumbereik te klein voor walk-forward optimalisatie", level="ERROR")
            return {"success": False, "error": "Date range too small"}

        # Genereer datumvensters
        date_windows = []
        current_start = start_date

        for i in range(windows):
            is_end = current_start + timedelta(days=is_period_days)
            oos_end = is_end + timedelta(days=oos_period_days)

            if oos_end > end_date:
                oos_end = end_date

            date_windows.append({
                'window': i + 1,
                'is_start': current_start,
                'is_end': is_end,
                'oos_start': is_end,
                'oos_end': oos_end
            })

            current_start = is_end

        self.logger.log_info(f"Gegenereerd {len(date_windows)} walk-forward vensters")

        # Optimaliseer voor elk venster
        window_results = []
        oos_results = []
        best_params_per_window = []

        for window in date_windows:
            window_num = window['window']
            is_start = window['is_start'].strftime('%Y-%m-%d')
            is_end = window['is_end'].strftime('%Y-%m-%d')
            oos_start = window['oos_start'].strftime('%Y-%m-%d')
            oos_end = window['oos_end'].strftime('%Y-%m-%d')

            self.logger.log_info(f"Window {window_num}: In-sample {is_start} tot {is_end}, "
                                 f"Out-of-sample {oos_start} tot {oos_end}")

            # In-sample optimalisatie
            self.logger.log_info(f"In-sample optimalisatie voor window {window_num}...")

            is_results = self.backtester.run_optimization(
                strategy_name=strategy_name,
                symbols=symbols,
                param_ranges=param_ranges,
                start_date=is_start,
                end_date=is_end,
                metric=metric,
                max_workers=max_workers
            )

            window_results.append(is_results)

            if not is_results['success']:
                self.logger.log_info(f"In-sample optimalisatie mislukt voor window {window_num}", level="ERROR")
                continue

            # Get best parameters
            best_params = is_results['best_parameters']
            best_metrics = is_results['best_metrics']

            self.logger.log_info(f"Beste parameters voor window {window_num}: {best_params}")
            self.logger.log_info(f"In-sample {metric}: {best_metrics.get(metric, 0):.4f}")

            # Valideer op out-of-sample periode
            self.logger.log_info(f"Out-of-sample validatie voor window {window_num}...")

            oos_result = self.backtester.run_backtest(
                strategy_name=strategy_name,
                symbols=symbols,
                timeframe=timeframe,
                start_date=oos_start,
                end_date=oos_end,
                parameters=best_params,
                plot_results=False
            )

            oos_results.append(oos_result)

            if not oos_result['success']:
                self.logger.log_info(f"Out-of-sample validatie mislukt voor window {window_num}", level="ERROR")
                continue

            oos_metrics = oos_result['metrics']

            self.logger.log_info(f"Out-of-sample {metric}: {oos_metrics.get(metric, 0):.4f}")
            self.logger.log_info(f"Out-of-sample net profit: {oos_metrics.get('net_profit_pct', 0):.2f}%")

            # Sla beste params op per window
            best_params_per_window.append({
                'window': window_num,
                'is_start': is_start,
                'is_end': is_end,
                'oos_start': oos_start,
                'oos_end': oos_end,
                'parameters': best_params,
                'is_metric': best_metrics.get(metric, 0),
                'oos_metric': oos_metrics.get(metric, 0),
                'is_profit': best_metrics.get('net_profit_pct', 0),
                'oos_profit': oos_metrics.get('net_profit_pct', 0),
                'is_trades': best_metrics.get('total_trades', 0),
                'oos_trades': oos_metrics.get('total_trades', 0)
            })

        # Analyseer walk-forward resultaten
        if not best_params_per_window:
            self.logger.log_info("Geen geldige resultaten voor analyse", level="ERROR")
            return {"success": False, "error": "No valid results"}

        # Bepaal de meest robuuste parameters
        robust_params = self._find_robust_parameters(best_params_per_window, param_ranges)

        # Valideer de robuuste parameters op de gehele periode
        self.logger.log_info(f"Valideren robuuste parameters {robust_params} op volledige periode...")

        full_result = self.backtester.run_backtest(
            strategy_name=strategy_name,
            symbols=symbols,
            timeframe=timeframe,
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d'),
            parameters=robust_params,
            plot_results=True
        )

        if full_result['success']:
            full_metrics = full_result['metrics']
            self.logger.log_info(f"Robuuste parameters validatie: {metric}={full_metrics.get(metric, 0):.4f}, "
                                 f"Net Profit={full_metrics.get('net_profit_pct', 0):.2f}%")

        # Visualiseer en sla resultaten op
        self._plot_walk_forward_results(best_params_per_window, robust_params, metric)
        self._save_optimization_results(
            strategy_name, symbols, metric, best_params_per_window, robust_params, full_result
        )

        return {
            "success": True,
            "best_params_per_window": best_params_per_window,
            "robust_params": robust_params,
            "full_result": full_result,
            "metric": metric
        }

    def _find_robust_parameters(self, window_results: List[Dict], param_ranges: Dict[str, List[Any]]) -> Dict[str, Any]:
        """
        Vind robuuste parameters die goed werken over meerdere periodes.

        Parameters:
        -----------
        window_results : List[Dict]
            Resultaten per window
        param_ranges : Dict[str, List[Any]]
            Mogelijke parameter waarden

        Returns:
        --------
        Dict[str, Any] : Meest robuuste parameterset
        """
        if not window_results:
            return {}

        # Extraheer parameter keys
        param_keys = list(param_ranges.keys())

        # Bereken hoe vaak elke parameter waarde voorkomt
        param_frequency = {param: {} for param in param_keys}

        for result in window_results:
            params = result['parameters']

            for param, value in params.items():
                if param in param_keys:
                    param_frequency[param][value] = param_frequency[param].get(value, 0) + 1

        # Kies de meest voorkomende waarde voor elke parameter
        robust_params = {}

        for param, freq in param_frequency.items():
            if freq:
                # De meest voorkomende waarde
                most_common = max(freq.items(), key=lambda x: x[1])[0]
                robust_params[param] = most_common
            else:
                # Fallback: gemiddelde waarde uit bereik
                values = param_ranges[param]
                if values and all(isinstance(v, (int, float)) for v in values):
                    robust_params[param] = sum(values) / len(values)
                elif values:
                    robust_params[param] = values[0]  # Eerste waarde als fallback

        return robust_params

    def _plot_walk_forward_results(self, window_results: List[Dict],
                                   robust_params: Dict[str, Any], metric: str) -> str:
        """
        Visualiseer walk-forward optimalisatie resultaten.

        Parameters:
        -----------
        window_results : List[Dict]
            Resultaten per window
        robust_params : Dict[str, Any]
            Meest robuuste parameterset
        metric : str
            Optimalisatiemetric

        Returns:
        --------
        str : Pad naar opgeslagen plot
        """
        if not window_results:
            return ""

        # Maak een figuur met 3 subplots
        fig, axs = plt.subplots(3, 1, figsize=(14, 16), gridspec_kw={'height_ratios': [2, 1, 2]})

        # 1. Plot IS vs OOS performance
        windows = [r['window'] for r in window_results]
        is_metrics = [r['is_metric'] for r in window_results]
        oos_metrics = [r['oos_metric'] for r in window_results]

        axs[0].plot(windows, is_metrics, 'b-', marker='o', label=f'In-Sample {metric}')
        axs[0].plot(windows, oos_metrics, 'r-', marker='x', label=f'Out-of-Sample {metric}')

        axs[0].set_title(f'Walk-Forward Optimalisatie: {metric} per Window', fontsize=16)
        axs[0].set_xlabel('Window #', fontsize=14)
        axs[0].set_ylabel(metric, fontsize=14)
        axs[0].grid(True)
        axs[0].legend(fontsize=12)

        # 2. Plot Profit
        is_profit = [r['is_profit'] for r in window_results]
        oos_profit = [r['oos_profit'] for r in window_results]

        axs[1].plot(windows, is_profit, 'g-', marker='o', label='In-Sample Profit %')
        axs[1].plot(windows, oos_profit, 'm-', marker='x', label='Out-of-Sample Profit %')

        axs[1].set_title('Net Profit % per Window', fontsize=16)
        axs[1].set_xlabel('Window #', fontsize=14)
        axs[1].set_ylabel('Net Profit %', fontsize=14)
        axs[1].grid(True)
        axs[1].legend(fontsize=12)

        # 3. Parameter consistency plot
        param_keys = list(robust_params.keys())

        if param_keys:
            param_values = {param: [] for param in param_keys}

            for result in window_results:
                for param in param_keys:
                    param_values[param].append(result['parameters'].get(param, None))

            # Normalize for plotting
            normalized_values = {}
            for param, values in param_values.items():
                if all(isinstance(v, (int, float)) for v in values if v is not None):
                    min_val = min(v for v in values if v is not None)
                    max_val = max(v for v in values if v is not None)

                    if max_val > min_val:
                        normalized_values[param] = [(v - min_val) / (max_val - min_val) if v is not None else None for v
                                                    in values]
                    else:
                        normalized_values[param] = [0.5 if v is not None else None for v in values]
                else:
                    # Categorische waarden
                    unique_values = list(set(v for v in values if v is not None))
                    normalized_values[param] = [
                        unique_values.index(v) / max(1, len(unique_values) - 1) if v in unique_values else None for v in
                        values]

            # Plot normalized parameters
            for param, values in normalized_values.items():
                valid_points = [(i, v) for i, v in enumerate(values, 1) if v is not None]
                if valid_points:
                    x, y = zip(*valid_points)
                    axs[2].plot(x, y, 'o-', label=param)

            axs[2].set_title('Parameter Consistency Across Windows', fontsize=16)
            axs[2].set_xlabel('Window #', fontsize=14)
            axs[2].set_ylabel('Normalized Parameter Value', fontsize=14)
            axs[2].grid(True)
            axs[2].legend(fontsize=12)

            # Voeg robuuste parameters toe als text box
            param_text = "Robust Parameters:\n" + "\n".join([f"{k}: {v}" for k, v in robust_params.items()])
            axs[2].text(0.02, 0.02, param_text, transform=axs[2].transAxes, fontsize=12,
                        bbox=dict(facecolor='white', alpha=0.7), verticalalignment='bottom')

        plt.tight_layout()

        # Sla plot op
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"walk_forward_results_{timestamp}.png")
        plt.savefig(output_path, dpi=150)
        plt.close()

        return output_path

    def _save_optimization_results(self, strategy_name: str, symbols: List[str],
                                   metric: str, window_results: List[Dict],
                                   robust_params: Dict[str, Any], full_result: Dict) -> str:
        """
        Sla optimalisatie resultaten op in JSON formaat.

        Parameters:
        -----------
        strategy_name : str
            Naam van de strategie
        symbols : List[str]
            Lijst met handelssymbolen
        metric : str
            Optimalisatiemetric
        window_results : List[Dict]
            Resultaten per window
        robust_params : Dict[str, Any]
            Meest robuuste parameterset
        full_result : Dict
            Resultaat van backtest met robuuste parameters

        Returns:
        --------
        str : Pad naar opgeslagen resultaten
        """
        # Maak resultaten dictionary
        results = {
            'strategy': strategy_name,
            'symbols': symbols,
            'metric': metric,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'window_results': window_results,
            'robust_params': robust_params,
            'full_metrics': full_result.get('metrics', {}) if full_result.get('success', False) else {}
        }

        # Sla op als JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"walk_forward_{strategy_name}_{timestamp}.json")

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, default=str)

        self.logger.log_info(f"Walk-forward resultaten opgeslagen als {output_path}")
        return output_path


class BayesianOptimizer:
    """
    Bayesiaanse Optimalisatie voor het efficiënt zoeken naar optimale strategie parameters.

    Deze klasse implementeert Bayesiaanse optimalisatie om efficiënter dan grid search
    optimale parameters te vinden door een surrogaat model te gebruiken.
    """

    def __init__(self, config=None, logger=None):
        """
        Initialiseer de Bayesiaanse optimizer.

        Parameters:
        -----------
        config : Optional[Dict]
            Configuratie dictionary (als None, dan wordt standaard config geladen)
        logger : Optional[Logger]
            Logger instantie (als None, dan wordt een nieuwe gemaakt)
        """
        self.config = config if config else load_config()
        self.logger = logger if logger else Logger(self.config['logging'].get('log_file', 'logs/bayesian_opt_log.csv'))

        # Output directory
        self.output_dir = self.config.get('output', {}).get('data_dir', 'data/optimization')
        os.makedirs(self.output_dir, exist_ok=True)

        # Maak backtester
        self.backtester = Backtester(self.config, self.logger)

        try:
            # Probeer scikit-optimize te importeren
            import skopt
            self.skopt_available = True
        except ImportError:
            self.logger.log_info("scikit-optimize niet beschikbaar. Installeer met: pip install scikit-optimize",
                                 level="WARNING")
            self.skopt_available = False

        # Visuele stijl instellen
        plt.style.use('ggplot')
        plt.rcParams['figure.figsize'] = (16, 10)

    def optimize(self, strategy_name: str, symbols: List[str], timeframe: str,
                 param_space: Dict[str, Any], start_date: Union[str, datetime],
                 end_date: Union[str, datetime], n_calls: int = 30,
                 n_initial_points: int = 10, metric: str = 'sharpe_ratio') -> Dict[str, Any]:
        """
        Voer Bayesiaanse optimalisatie uit.

        Parameters:
        -----------
        strategy_name : str
            Naam van de strategie
        symbols : List[str]
            Lijst met handelssymbolen
        timeframe : str
            Timeframe voor analyse
        param_space : Dict[str, Any]
            Dictionary met parameter namen en bereiken:
            Bijvoorbeeld: {'entry_period': (10, 60), 'atr_multiplier': (1.0, 3.0)}
            Voor categorische: {'swing_mode': ['True', 'False']}
        start_date : Union[str, datetime]
            Start datum
        end_date : Union[str, datetime]
            Eind datum
        n_calls : int
            Aantal evaluatiepunten
        n_initial_points : int
            Aantal initiële random punten
        metric : str
            Prestatiemetric om te optimaliseren (bijv. 'sharpe_ratio', 'profit_factor', etc.)

        Returns:
        --------
        Dict[str, Any] : Resultaten van de optimalisatie
        """
        if not self.skopt_available:
            self.logger.log_info("Kan Bayesiaanse optimalisatie niet uitvoeren zonder scikit-optimize", level="ERROR")
            return {"success": False, "error": "scikit-optimize not available"}

        import skopt
        from skopt import gp_minimize
        from skopt.space import Real, Integer, Categorical
        from skopt.utils import use_named_args

        self.logger.log_info(f"===== Starten Bayesiaanse Optimalisatie: {strategy_name} =====")
        self.logger.log_info(f"Symbolen: {symbols}, Timeframe: {timeframe}")
        self.logger.log_info(f"Optimalisatie metric: {metric}")

        # Definieer parameter space in skopt formaat
        dimensions = []
        dimension_names = []

        for param_name, param_def in param_space.items():
            dimension_names.append(param_name)

            if isinstance(param_def, tuple) and len(param_def) == 2:
                low, high = param_def
                if isinstance(low, int) and isinstance(high, int):
                    dimensions.append(Integer(low, high, name=param_name))
                elif isinstance(low, (int, float)) and isinstance(high, (int, float)):
                    dimensions.append(Real(low, high, name=param_name))
            elif isinstance(param_def, list):
                dimensions.append(Categorical(param_def, name=param_name))

        # Conversie van strings naar booleans voor categorische opties
        def process_param_value(param_name, value):
            if param_name in param_space and isinstance(param_space[param_name], list):
                if value == 'True':
                    return True
                elif value == 'False':
                    return False
            return value

        # Definieer evaluatiefunctie
        @use_named_args(dimensions=dimensions)
        def evaluate_params(**params):
            # Converteer categoriën indien nodig
            processed_params = {
                name: process_param_value(name, value)
                for name, value in params.items()
            }

            self.logger.log_info(f"Evalueren parameters: {processed_params}")

            try:
                result = self.backtester.run_backtest(
                    strategy_name=strategy_name,
                    symbols=symbols,
                    timeframe=timeframe,
                    start_date=start_date,
                    end_date=end_date,
                    parameters=processed_params,
                    plot_results=False
                )

                if not result['success']:
                    return -100  # Penalty voor mislukte backtests

                metrics = result['metrics']

                # We minimaliseren, dus negeer de metric
                metric_value = metrics.get(metric, 0)

                if metric in ['sharpe_ratio', 'profit_factor', 'net_profit', 'net_profit_pct', 'win_rate']:
                    return -metric_value  # Negeer omdat we maximaliseren
                else:
                    return metric_value  # Voor metrics die we minimaliseren

            except Exception as e:
                self.logger.log_info(f"Fout bij evalueren parameters: {str(e)}", level="ERROR")
                return -100  # Penalty voor errors

        # Voer optimalisatie uit
        start_time = time.time()

        result = gp_minimize(
            evaluate_params,
            dimensions=dimensions,
            n_calls=n_calls,
            n_initial_points=n_initial_points,
            acq_func='EI',  # Expected Improvement
            noise=0.01,
            verbose=True
        )

        elapsed = time.time() - start_time
        self.logger.log_info(f"Optimalisatie voltooid in {elapsed:.2f} seconden")

        # Analyseer resultaten
        best_params = dict(zip(dimension_names, result.x))

        # Converteer categoriën indien nodig
        best_params = {
            name: process_param_value(name, value)
            for name, value in best_params.items()
        }

        # Negatief van de score voor metrics die we maximaliseren
        best_score = -result.fun if metric in ['sharpe_ratio', 'profit_factor', 'net_profit', 'net_profit_pct',
                                               'win_rate'] else result.fun

        self.logger.log_info(f"Beste parameters gevonden: {best_params}")
        self.logger.log_info(f"Beste {metric}: {best_score:.4f}")

        # Run final backtest met beste parameters
        final_result = self.backtester.run_backtest(
            strategy_name=strategy_name,
            symbols=symbols,
            timeframe=timeframe,
            start_date=start_date,
            end_date=end_date,
            parameters=best_params,
            plot_results=True
        )

        # Visualiseer resultaten
        self._plot_optimization_results(result, dimension_names, metric)
        self._save_optimization_results(
            strategy_name, symbols, metric, result, dimension_names, best_params, final_result
        )

        return {
            "success": True,
            "best_parameters": best_params,
            "best_score": best_score,
            "optimization_result": result,
            "final_backtest": final_result
        }

    def _plot_optimization_results(self, result, dimension_names: List[str], metric: str) -> str:
        """
        Visualiseer optimalisatie resultaten.

        Parameters:
        -----------
        result : skopt.OptimizeResult
            Resultaat van de optimalisatie
        dimension_names : List[str]
            Namen van de dimensies (parameters)
        metric : str
            Optimalisatiemetric

        Returns:
        --------
        str : Pad naar opgeslagen plot
        """
        try:
            import skopt
            from skopt.plots import plot_convergence, plot_objective, plot_evaluations

            # Maak één figuur met 3 subplots
            fig, axs = plt.subplots(3, 1, figsize=(14, 18))

            # 1. Convergentie plot
            plot_convergence(result, ax=axs[0])
            if metric in ['sharpe_ratio', 'profit_factor', 'net_profit', 'net_profit_pct', 'win_rate']:
                # Converteer y-as labels voor metrics die we maximaliseren
                axs[0].set_ylabel(f"Negative {metric}")

            axs[0].set_title(f"Convergence Plot for {metric} Optimization", fontsize=16)

            # 2. Objective plot (alleen voor 1-2 dimensies)
            if len(dimension_names) <= 2:
                try:
                    plot_objective(result, ax=axs[1])
                    axs[1].set_title(f"Objective Surface for {metric}", fontsize=16)
                except Exception as e:
                    self.logger.log_info(f"Kon objective plot niet maken: {str(e)}", level="WARNING")
                    axs[1].set_visible(False)
            else:
                axs[1].set_visible(False)

            # 3. Evaluations plot
            try:
                plot_evaluations(result, ax=axs[2])
                axs[2].set_title("Parameter Evaluations", fontsize=16)
            except Exception as e:
                self.logger.log_info(f"Kon evaluations plot niet maken: {str(e)}", level="WARNING")
                axs[2].set_visible(False)

            plt.tight_layout()

            # Sla plot op
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(self.output_dir, f"bayesian_optimization_{timestamp}.png")
            plt.savefig(output_path, dpi=150)
            plt.close()

            return output_path

        except Exception as e:
            self.logger.log_info(f"Fout bij plotten optimalisatie resultaten: {str(e)}", level="ERROR")
            return ""

    def _save_optimization_results(self, strategy_name: str, symbols: List[str],
                                   metric: str, result, dimension_names: List[str],
                                   best_params: Dict[str, Any], final_result: Dict) -> str:
        """
        Sla optimalisatie resultaten op in JSON formaat.

        Parameters:
        -----------
        strategy_name : str
            Naam van de strategie
        symbols : List[str]
            Lijst met handelssymbolen
        metric : str
            Optimalisatiemetric
        result : skopt.OptimizeResult
            Resultaat van de optimalisatie
        dimension_names : List[str]
            Namen van de dimensies (parameters)
        best_params : Dict[str, Any]
            Beste gevonden parameters
        final_result : Dict
            Resultaat van backtest met beste parameters

        Returns:
        --------
        str : Pad naar opgeslagen resultaten
        """
        # Maak resultaten dictionary
        optimization_data = {
            'strategy': strategy_name,
            'symbols': symbols,
            'metric': metric,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'best_params': best_params,
            'best_score': -result.fun if metric in ['sharpe_ratio', 'profit_factor', 'net_profit', 'net_profit_pct',
                                                    'win_rate'] else result.fun,
            'function_calls': result.nfev,
            'full_metrics': final_result.get('metrics', {}) if final_result.get('success', False) else {}
        }

        # Voeg alle evaluaties toe
        evaluations = []
        for i, (x, y) in enumerate(zip(result.x_iters, result.func_vals)):
            evaluations.append({
                'iteration': i + 1,
                'parameters': dict(zip(dimension_names, x)),
                'score': -y if metric in ['sharpe_ratio', 'profit_factor', 'net_profit', 'net_profit_pct',
                                          'win_rate'] else y
            })

        optimization_data['evaluations'] = evaluations

        # Sla op als JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"bayesian_opt_{strategy_name}_{timestamp}.json")

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(optimization_data, f, indent=2, default=str)

        self.logger.log_info(f"Bayesiaanse optimalisatie resultaten opgeslagen als {output_path}")
        return output_path


def run_walk_forward_optimization():
    """Voer walk-forward optimalisatie uit vanaf command line."""
    print("Walk-Forward Optimalisatie module gestart")

    # Laad configuratie
    config = load_config()

    # Setup logger
    log_file = config['logging'].get('log_file', 'logs/wf_opt_log.csv')
    logger = Logger(log_file)
    logger.log_info("====== Sophy Walk-Forward Optimalisatie Started ======")

    # Initialiseer optimizer
    optimizer = WalkForwardOptimizer(config, logger)

    # Haal parameters op uit config
    symbols = config['mt5'].get('symbols', ['EURUSD'])
    timeframe = config['mt5'].get('timeframe', 'H4')
    strategy_name = config['strategy'].get('name', 'turtle')

    # Definieer parameter bereiken voor turtle strategy
    param_ranges = {
        'entry_period': [20, 40, 60],
        'exit_period': [10, 20, 30],
        'atr_period': [14, 20, 30],
        'atr_multiplier': [1.5, 2.0, 2.5, 3.0],
        'swing_mode': [True, False]
    }

    # Bereken start en einddatum
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365 * 2)  # 2 jaar data

    # Start optimalisatie
    results = optimizer.optimize(
        strategy_name=strategy_name,
        symbols=symbols,
        timeframe=timeframe,
        param_ranges=param_ranges,
        start_date=start_date,
        end_date=end_date,
        is_period_days=180,  # 6 maanden in-sample
        oos_period_days=60,  # 2 maanden out-of-sample
        windows=3,  # 3 windows
        metric='sharpe_ratio'
    )

    if results['success']:
        logger.log_info("Walk-Forward Optimalisatie voltooid")
        logger.log_info(f"Robuuste parameters gevonden: {results['robust_params']}")
    else:
        logger.log_info(f"Walk-Forward Optimalisatie mislukt: {results.get('error', 'Onbekende fout')}", level="ERROR")

    logger.log_info("====== Sophy Walk-Forward Optimalisatie Ended ======")


def run_bayesian_optimization():
    """Voer Bayesiaanse optimalisatie uit vanaf command line."""
    print("Bayesiaanse Optimalisatie module gestart")

    # Laad configuratie
    config = load_config()

    # Setup logger
    log_file = config['logging'].get('log_file', 'logs/bayes_opt_log.csv')
    logger = Logger(log_file)
    logger.log_info("====== Sophy Bayesiaanse Optimalisatie Started ======")

    # Initialiseer optimizer
    optimizer = BayesianOptimizer(config, logger)

    # Haal parameters op uit config
    symbols = config['mt5'].get('symbols', ['EURUSD'])
    timeframe = config['mt5'].get('timeframe', 'H4')
    strategy_name = config['strategy'].get('name', 'turtle')

    # Definieer parameter bereiken voor turtle strategy
    param_space = {
        'entry_period': (10, 60),
        'exit_period': (5, 30),
        'atr_period': (5, 30),
        'atr_multiplier': (1.0, 4.0),
        'swing_mode': ['True', 'False']
    }

    # Bereken start en einddatum
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)  # 1 jaar data

    # Start optimalisatie
    results = optimizer.optimize(
        strategy_name=strategy_name,
        symbols=symbols,
        timeframe=timeframe,
        param_space=param_space,
        start_date=start_date,
        end_date=end_date,
        n_calls=30,  # 30 evaluatiepunten
        n_initial_points=10,  # 10 initiële random punten
        metric='sharpe_ratio'
    )

    if results['success']:
        logger.log_info("Bayesiaanse Optimalisatie voltooid")
        logger.log_info(f"Beste parameters gevonden: {results['best_parameters']}")
        logger.log_info(f"Beste score: {results['best_score']:.4f}")
    else:
        logger.log_info(f"Bayesiaanse Optimalisatie mislukt: {results.get('error', 'Onbekende fout')}", level="ERROR")

    logger.log_info("====== Sophy Bayesiaanse Optimalisatie Ended ======")


if __name__ == "__main__":
    # Kies welke optimalisatiemethode je wilt uitvoeren
    run_walk_forward_optimization()
    # run_bayesian_optimization()  # Uncomment om Bayesiaanse optimalisatie uit te voeren
```

-----------

Path: src/connector/__init__.py

```python
```

-----------

Path: src/connector/mt5_connector.py

```python
# src/connector/mt5_connector.py
import time
from typing import Dict, List, Optional, Any

import MetaTrader5 as mt5
import pandas as pd


class MT5Connector:
    """Verzorgt alle interacties met het MetaTrader 5 platform"""

    def __init__(self, config: Dict[str, any], logger: any) -> None:
        """
        Initialiseer de MT5 connector met configuratie

        Args:
            config: Configuratie dictionary met MT5 connectie parameters
            logger: Logger instance voor het registreren van gebeurtenissen
        """
        self.config = config
        self.logger = logger
        self.connected = False
        self._initialize_error_messages()
        self.timeframe_map = {
            'M1': mt5.TIMEFRAME_M1,
            'M5': mt5.TIMEFRAME_M5,
            'M15': mt5.TIMEFRAME_M15,
            'M30': mt5.TIMEFRAME_M30,
            'H1': mt5.TIMEFRAME_H1,
            'H4': mt5.TIMEFRAME_H4,
            'D1': mt5.TIMEFRAME_D1,
            'W1': mt5.TIMEFRAME_W1,
            'MN1': mt5.TIMEFRAME_MN1
        }

    def _initialize_error_messages(self) -> None:
        """Initialiseer foutmeldingen voor MT5 verbinding"""
        self.error_messages = {
            10013: "Ongeldige parameters voor verbinding",
            10014: "Verkeerde login of wachtwoord",
            10015: "Verkeerde server opgegeven",
            10016: "MT5 niet geïnstalleerd of niet gevonden",
            10018: "Verbinding met de server mislukt",
            10019: "Geen respons van server"
        }

    def connect(self) -> bool:
        """
        Maak verbinding met MT5 met uitgebreide foutafhandeling

        Returns:
            bool: True als verbinding succesvol, False anders
        """
        # Controleer of MT5 al is geïnitialiseerd
        if mt5.terminal_info() is not None and self.connected:
            self.logger.log_info("Al verbonden met MT5")
            return True

        # Sluit eerder gemaakte verbindingen
        mt5.shutdown()

        # Initialiseer MT5
        self.logger.log_info(f"Verbinden met MT5 op pad: {self.config.get('mt5_pathway', 'standaard pad')}")
        init_result = mt5.initialize(
            path=self.config.get('mt5_pathway'),
            login=self.config.get('login'),
            password=self.config.get('password'),
            server=self.config.get('server')
        )

        if not init_result:
            error_code = mt5.last_error()
            error_message = self.error_messages.get(
                error_code, f"Onbekende MT5 error: {error_code}")
            self.logger.log_info(f"MT5 initialisatie mislukt: {error_message}", level="ERROR")
            return False

        # Controleer verbinding
        if not mt5.terminal_info():
            self.logger.log_info("MT5 terminal info niet beschikbaar", level="ERROR")
            return False

        # Verbinding gemaakt
        self.connected = True
        account_info = mt5.account_info()

        if account_info:
            self.logger.log_info(f"Verbonden met MT5 account: {account_info.login}, "
                                 f"Server: {account_info.server}, "
                                 f"Type: {account_info.trade_mode_description}")
            return True
        else:
            self.logger.log_info("Kon geen account info ophalen", level="ERROR")
            return False

    def disconnect(self) -> None:
        """Sluit verbinding met MT5"""
        if self.connected:
            mt5.shutdown()
            self.connected = False
            self.logger.log_info("Verbinding met MT5 afgesloten")

    def get_account_info(self) -> Dict[str, Any]:
        """
        Haal account informatie op van MT5

        Returns:
            Dict met account eigenschappen
        """
        if not self.connected:
            self.logger.log_info("Niet verbonden met MT5", level="ERROR")
            return {}

        account_info = mt5.account_info()
        if not account_info:
            self.logger.log_info("Kon account informatie niet ophalen", level="ERROR")
            return {}

        # Converteer naar dictionary
        result = {
            'login': account_info.login,
            'balance': account_info.balance,
            'equity': account_info.equity,
            'margin': account_info.margin,
            'free_margin': account_info.margin_free,
            'profit': account_info.profit,
            'margin_level': (account_info.equity / account_info.margin * 100
                             if account_info.margin > 0 else 0)
        }

        return result

    def get_timeframe_constant(self, timeframe_str: str) -> int:
        """
        Converteer timeframe string naar MT5 constante

        Args:
            timeframe_str: Timeframe als string (bijv. 'H4')

        Returns:
            MT5 timeframe constante
        """
        return self.timeframe_map.get(timeframe_str, mt5.TIMEFRAME_H4)

    def get_historical_data(self,
                            symbol: str,
                            timeframe_or_str: Any,
                            bars_count: int = 100) -> pd.DataFrame:
        """
        Haal historische prijsdata op met geoptimaliseerde verwerking

        Args:
            symbol: Handelssymbool
            timeframe_or_str: MT5 timeframe constante of string ('H4', etc.)
            bars_count: Aantal bars om op te halen

        Returns:
            pd.DataFrame: DataFrame met historische data
        """
        if not self.connected:
            self.logger.log_info("Niet verbonden met MT5", level="ERROR")
            return pd.DataFrame()

        # Converteer timeframe string naar constante indien nodig
        timeframe = timeframe_or_str
        if isinstance(timeframe_or_str, str):
            timeframe = self.get_timeframe_constant(timeframe_or_str)

        # Probeer data op te halen met retry mechanisme
        retries = 3
        for attempt in range(retries):
            rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars_count)

            if rates is not None and len(rates) > 0:
                break

            if attempt < retries - 1:
                self.logger.log_info(
                    f"Poging {attempt + 1} mislukt om data op te halen voor {symbol}, opnieuw proberen...")
                time.sleep(1)

        if rates is None or len(rates) == 0:
            self.logger.log_info(f"Kon geen historische data ophalen voor {symbol} na {retries} pogingen",
                                 level="ERROR")
            return pd.DataFrame()

        # Converteer naar pandas DataFrame en bereken extra kolommen
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')

        # Hernoem kolommen naar lowercase voor consistentie
        df.columns = [col.lower() for col in df.columns]

        # Rename 'time' kolom naar 'date' voor consistentie in strategie code
        df.rename(columns={'time': 'date'}, inplace=True)

        return df

    def get_symbol_tick(self, symbol: str) -> Optional[Any]:
        """
        Haal actuele tick data op voor een symbool

        Args:
            symbol: Handelssymbool

        Returns:
            mt5.Tick object of None bij fout
        """
        if not self.connected:
            self.logger.log_info("Niet verbonden met MT5", level="ERROR")
            return None

        tick = mt5.symbol_info_tick(symbol)

        if tick is None:
            error_code = mt5.last_error()
            self.logger.log_info(f"Kon geen tick informatie ophalen voor {symbol}. Error: {error_code}", level="ERROR")
            return None

        return tick

    def get_open_positions(self, symbol: Optional[str] = None) -> List[Any]:
        """
        Haal open posities op

        Args:
            symbol: Optioneel filter op symbool

        Returns:
            Lijst met open posities
        """
        if not self.connected:
            self.logger.log_info("Niet verbonden met MT5", level="ERROR")
            return []

        positions = []

        if symbol:
            positions = mt5.positions_get(symbol=symbol)
        else:
            positions = mt5.positions_get()

        if positions is None:
            error_code = mt5.last_error()
            # Als er geen posities zijn is dit geen error
            if error_code == 0:
                return []
            self.logger.log_info(f"Kon geen posities ophalen. Error: {error_code}", level="ERROR")
            return []

        return list(positions)

    def place_order(self,
                    action: str,
                    symbol: str,
                    volume: float,
                    stop_loss: float = 0,
                    take_profit: float = 0,
                    comment: str = "") -> Optional[int]:
        """
        Plaats een order op het MT5 platform

        Args:
            action: "BUY" of "SELL"
            symbol: Handelssymbool
            volume: Order volume in lots
            stop_loss: Stop loss prijs (0 = geen stop loss)
            take_profit: Take profit prijs (0 = geen take profit)
            comment: Order commentaar

        Returns:
            Order ticket ID of None bij fout
        """
        if not self.connected:
            self.logger.log_info("Niet verbonden met MT5", level="ERROR")
            return None

        # Haal symbool informatie op
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            self.logger.log_info(f"Kon geen informatie krijgen voor symbool {symbol}", level="ERROR")
            return None

        # Controleer of trading mogelijk is voor dit symbool
        if not symbol_info.visible or not symbol_info.trade_allowed:
            self.logger.log_info(f"Trading niet toegestaan voor {symbol}", level="ERROR")
            return None

        # Haal huidige prijs op
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            self.logger.log_info(f"Kon geen tick informatie ophalen voor {symbol}", level="ERROR")
            return None

        # Bepaal order type en prijs
        order_type = None
        price = None

        if action == "BUY":
            order_type = mt5.ORDER_TYPE_BUY
            price = tick.ask
        elif action == "SELL":
            order_type = mt5.ORDER_TYPE_SELL
            price = tick.bid
        else:
            self.logger.log_info(f"Ongeldige actie: {action}", level="ERROR")
            return None

        # Bereid order request voor
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": float(volume),
            "type": order_type,
            "price": price,
            "sl": float(stop_loss) if stop_loss > 0 else 0,
            "tp": float(take_profit) if take_profit > 0 else 0,
            "deviation": 10,  # prijsafwijking in punten
            "magic": 123456,  # magic number voor identificatie
            "comment": comment,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK
        }

        # Stuur order naar MT5
        self.logger.log_info(
            f"Order versturen: {action} {volume} {symbol} @ {price}, SL: {stop_loss}, TP: {take_profit}")
        result = mt5.order_send(request)

        if result is None:
            error_code = mt5.last_error()
            self.logger.log_info(f"Order verzenden mislukt. Error code: {error_code}", level="ERROR")
            return None

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            self.logger.log_info(f"Order mislukt. Retcode: {result.retcode}", level="ERROR")
            return None

        self.logger.log_info(f"Order succesvol geplaatst. Ticket: {result.order}")
        return result.order
```

-----------

Path: src/ftmo/__init__.py

```python
```

-----------

Path: src/ftmo/ftmo_helper.py

```python
import logging
import os
from typing import Dict

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class FTMOHelper:
    """Helper class for FTMO compliance checks and reporting"""

    def __init__(self, log_file: str, output_dir: str = 'data/ftmo_analysis'):
        self.log_file = log_file
        self.output_dir = output_dir

        os.makedirs(output_dir, exist_ok=True)

        # Configure visualization style
        plt.style.use('ggplot')
        plt.rcParams['figure.figsize'] = (16, 10)
        sns.set_style("whitegrid")

        # Logging setup
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        # FTMO rules
        self.ftmo_rules = {
            'profit_target': 0.10,
            'max_daily_loss': -0.05,  # Corrected sign
            'max_total_loss': -0.10,  # Corrected sign
            'min_trading_days': 4,
            'challenge_duration': 30,
            'verification_duration': 60
        }

    def load_trade_data(self) -> pd.DataFrame:
        """Load trading data from log file"""
        try:
            df = pd.read_csv(self.log_file)
            df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
            df['Date'] = df['Timestamp'].dt.date
            return df.dropna(subset=['Timestamp'])  # Verwijder rijen met foutieve timestamps
        except Exception as e:
            logging.error(f"Error loading trading data: {e}")
            return pd.DataFrame()

    def check_ftmo_compliance(self, initial_balance: float) -> Dict:
        """Check FTMO compliance with detailed analysis"""
        df = self.load_trade_data()
        if df.empty:
            return {'compliant': False, 'reason': 'No trading data available', 'details': {}}

        # Extract STATUS entries for balance tracking
        status_df = df[df['Type'] == 'STATUS'].copy()
        if status_df.empty:
            return {'compliant': False, 'reason': 'No account status data available', 'details': {}}

        # Convert balance to numeric
        status_df['Balance'] = pd.to_numeric(status_df['Balance'], errors='coerce')
        status_df.dropna(subset=['Balance'], inplace=True)

        # Compute daily balance statistics
        daily_status = status_df.groupby('Date').agg(
            min_balance=('Balance', 'min'),
            max_balance=('Balance', 'max'),
            close_balance=('Balance', 'last')
        ).reset_index()

        # Ensure we have data before proceeding
        if daily_status.empty:
            return {'compliant': False, 'reason': 'Insufficient balance data available', 'details': {}}

        # Calculate daily P&L and drawdowns
        daily_status['prev_close'] = daily_status['close_balance'].shift(1).fillna(initial_balance)
        daily_status['daily_pnl'] = daily_status['close_balance'] - daily_status['prev_close']
        daily_status['daily_pnl_pct'] = (daily_status['daily_pnl'] / daily_status['prev_close']) * 100
        daily_status['daily_drawdown'] = ((daily_status['min_balance'] - daily_status['prev_close'])
                                          / daily_status['prev_close']) * 100
        daily_status['peak'] = daily_status['close_balance'].cummax()
        daily_status['drawdown_from_peak'] = ((daily_status['close_balance'] - daily_status['peak'])
                                              / daily_status['peak']) * 100

        # Calculate key metrics
        max_drawdown = daily_status['drawdown_from_peak'].min()
        latest_balance = daily_status['close_balance'].iloc[-1]
        total_pnl = latest_balance - initial_balance
        total_pnl_pct = (total_pnl / initial_balance) * 100

        # Check trading days
        trade_df = df[df['Type'] == 'TRADE']
        unique_trading_days = trade_df['Date'].nunique()

        # Check FTMO rules compliance
        profit_target_met = total_pnl_pct >= self.ftmo_rules['profit_target'] * 100
        daily_loss_compliant = daily_status['daily_drawdown'].min() >= self.ftmo_rules['max_daily_loss'] * 100
        total_loss_compliant = max_drawdown >= self.ftmo_rules['max_total_loss'] * 100
        trading_days_compliant = unique_trading_days >= self.ftmo_rules['min_trading_days']

        compliant = profit_target_met and daily_loss_compliant and total_loss_compliant and trading_days_compliant

        # Generate reason for non-compliance if applicable
        reasons = []
        if not profit_target_met:
            reasons.append(f"Profit target not reached: {total_pnl_pct:.2f}% "
                           f"(target: {self.ftmo_rules['profit_target'] * 100}%)")
        if not daily_loss_compliant:
            worst_day_idx = daily_status['daily_drawdown'].idxmin()
            worst_day = daily_status.iloc[worst_day_idx]
            reasons.append(f"Daily loss limit exceeded: {worst_day['daily_drawdown']:.2f}% on {worst_day['Date']}")
        if not total_loss_compliant:
            reasons.append(f"Maximum drawdown exceeded: {max_drawdown:.2f}% "
                           f"(limit: {self.ftmo_rules['max_total_loss'] * 100}%)")
        if not trading_days_compliant:
            reasons.append(f"Insufficient trading days: {unique_trading_days} "
                           f"(minimum: {self.ftmo_rules['min_trading_days']})")

        reason = "; ".join(reasons) if reasons else "Complies with all FTMO rules"

        # Compile results
        details = {
            'initial_balance': initial_balance,
            'final_balance': latest_balance,
            'total_pnl': total_pnl,
            'total_pnl_pct': total_pnl_pct,
            'max_drawdown': max_drawdown,
            'trading_days': unique_trading_days,
            'daily_stats': daily_status.to_dict(orient='records')  # Converted for better JSON compatibility
        }

        return {
            'compliant': compliant,
            'reason': reason,
            'details': details
        }

    def generate_trading_report(self, initial_balance: float) -> bool:
        """Generate detailed FTMO trading report with visualizations"""
        try:
            results = self.check_ftmo_compliance(initial_balance)
            daily_status = pd.DataFrame(results['details'].get('daily_stats', []))

            if daily_status.empty:
                logging.warning("No data available for generating trading report.")
                return False

            # Plot balance over time
            plt.figure(figsize=(12, 6))
            plt.plot(daily_status['Date'], daily_status['close_balance'], marker='o', label='Balance')
            plt.fill_between(daily_status['Date'], daily_status['min_balance'], daily_status['max_balance'],
                             alpha=0.3, color='gray', label="Daily Range")
            plt.axhline(y=initial_balance, color='r', linestyle='--', label="Initial Balance")
            plt.title("Trading Balance Over Time")
            plt.xlabel("Date")
            plt.ylabel("Balance")
            plt.legend()
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Save the figure
            report_path = os.path.join(self.output_dir, "trading_report.png")
            plt.savefig(report_path)
            logging.info(f"Trading report saved at {report_path}")

            return True
        except Exception as e:
            logging.error(f"Error generating trading report: {e}")
            return False
```

-----------

Path: src/ftmo/ftmo_validator.py

```python
# src/ftmo/ftmo_validator.py

import os
import re
from datetime import datetime, date
from typing import Dict, Tuple, Optional, Any

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.utils.logger import Logger  # Importeer de Logger-klasse


class FTMOValidator:
    """Klasse om handelsactiviteit te valideren en analyseren volgens FTMO-regels."""

    def __init__(self, config: Dict[str, Any], log_file: str, output_dir: str = 'data/ftmo_analysis',
                 logger: Optional[Logger] = None) -> None:
        """
        Initialiseer de FTMO Validator met configuratie, logbestand en outputmap.

        Parameters:
        -----------
        config : Dict[str, Any]
            Configuratiedictionary met risicoparameters (bijv. initial_balance).
        log_file : str
            Pad naar het logbestand met handelsdata.
        output_dir : str, optional
            Map voor het opslaan van analyse-uitvoer (default: 'data/ftmo_analysis').
        logger : Logger, optional
            Logging-object voor het bijhouden van gebeurtenissen.
        """
        self.config = config
        self.logger = logger
        self.initial_balance = config['risk'].get('account_balance', 100000)
        # Haal startdatum uit config of bepaal uit logbestand
        self.start_date = datetime.strptime(config.get('ftmo', {}).get('start_date', date.today().strftime('%Y-%m-%d')),
                                            '%Y-%m-%d').date()
        self.trade_days = set()
        self.log_file = log_file
        self.output_dir = output_dir

        # Stel visualisatiestijl in
        plt.style.use('ggplot')
        plt.rcParams['figure.figsize'] = (16, 10)
        plt.rcParams['lines.linewidth'] = 1.5
        sns.set_style("whitegrid")

        # Maak outputmap aan als deze niet bestaat
        os.makedirs(output_dir, exist_ok=True)

        # FTMO-regels
        self.ftmo_rules = {
            'profit_target': 0.10,  # 10% winstdoel
            'max_daily_loss': 0.05,  # 5% maximale dagelijkse drawdown
            'max_total_loss': 0.10,  # 10% maximale totale drawdown
            'min_trading_days': 4,  # Minimaal 4 handelsdagen
            'challenge_duration': 30,  # Challenge-duur van 30 dagen
            'verification_duration': 60  # Verificatie-duur van 60 dagen
        }

    def load_trade_data(self) -> pd.DataFrame:
        """
        Laad handelsdata uit het logbestand.

        Returns:
        --------
        pandas.DataFrame
            DataFrame met handelsdata, of lege DataFrame bij fout.

        Raises:
        -------
        ValueError
            Als het logbestand ongeldig is.
        """
        try:
            if not os.path.exists(self.log_file):
                raise ValueError(f"Logbestand niet gevonden: {self.log_file}")
            df = pd.read_csv(self.log_file)
            if df.empty or 'Timestamp' not in df.columns:
                raise ValueError("Logbestand is leeg of ongeldig formaat")
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            df['Date'] = df['Timestamp'].dt.date
            if self.logger:
                self.logger.log_info(f"Handelsdata geladen uit {self.log_file}")
            return df
        except Exception as e:
            if self.logger:
                self.logger.log_info(f"Fout bij laden handelsdata: {e}", level="ERROR")
            return pd.DataFrame()

    def validate_account_state(self, account_info: Dict[str, float] = None) -> Tuple[bool, Optional[str]]:
        """
        Valideer de accountstatus volgens FTMO-regels.

        Args:
            account_info: Huidige accountinformatie (optioneel).

        Returns:
            Tuple[bool, Optional[str]]: (is_compliant, violation_reason).
        """
        df = self.load_trade_data()
        if df.empty:
            return False, "Geen handelsdata beschikbaar"

        status_df = df[df['Type'] == 'STATUS'].copy()
        if status_df.empty:
            return False, "Geen statusdata beschikbaar"

        # Extraheer balans
        if 'Balance' not in status_df.columns or status_df['Balance'].isna().all():
            def extract_balance(comment):
                if isinstance(comment, str) and 'Balance: ' in comment:
                    match = re.search(r'Balance:\s*([\d,.]+)', comment)
                    return float(match.group(1).replace(',', '')) if match else None
                return None

            status_df['Balance'] = status_df['Comment'].apply(extract_balance)

        if status_df['Balance'].isna().all():
            return False, "Geen balansdata beschikbaar"

        status_df['Balance'] = pd.to_numeric(status_df['Balance'], errors='coerce')
        daily_status = status_df.groupby('Date').agg(close_balance=('Balance', 'last')).reset_index()
        current_equity = daily_status['close_balance'].iloc[-1] if not daily_status.empty else self.initial_balance

        # Registreer handelsdag
        self.trade_days.update(df[df['Type'] == 'TRADE']['Date'].unique())

        # Bereken winst/verlies percentage
        profit_loss_pct = (current_equity - self.initial_balance) / self.initial_balance * 100

        # Controleer FTMO-regels
        if profit_loss_pct >= self.ftmo_rules['profit_target'] * 100:
            return True, "Winstdoel bereikt"

        if profit_loss_pct <= -self.ftmo_rules['max_daily_loss'] * 100:
            return False, "Dagelijkse verlieslimiet overschreden"

        if profit_loss_pct <= -self.ftmo_rules['max_total_loss'] * 100:
            return False, "Maximale drawdown overschreden"

        days_in_challenge = (date.today() - self.start_date).days
        if days_in_challenge >= self.ftmo_rules['challenge_duration'] - 2:
            unique_trading_days = len(self.trade_days)
            if unique_trading_days < self.ftmo_rules['min_trading_days']:
                return False, f"Onvoldoende handelsdagen: {unique_trading_days} (minimaal: {self.ftmo_rules['min_trading_days']})"

        return True, None

    def check_ftmo_compliance(self, initial_balance: float = None) -> Dict:
        """
        Controleer FTMO-naleving met gedetailleerde analyse van handelsdata.

        Parameters:
        -----------
        initial_balance : float, optional
            Initiële accountbalans (default vanuit config).

        Returns:
        --------
        Dict
            Resultaten van naleving met details.
        """
        initial_balance = initial_balance if initial_balance is not None else self.initial_balance
        df = self.load_trade_data()
        if df.empty:
            return {'compliant': False, 'reason': 'Geen handelsdata beschikbaar', 'details': {}}

        status_df = df[df['Type'] == 'STATUS'].copy()
        if status_df.empty:
            return {'compliant': False, 'reason': 'Geen statusdata beschikbaar', 'details': {}}

        # Extraheer balans
        if 'Balance' not in status_df.columns or status_df['Balance'].isna().all():
            def extract_balance(comment):
                if isinstance(comment, str) and 'Balance: ' in comment:
                    match = re.search(r'Balance:\s*([\d,.]+)', comment)
                    return float(match.group(1).replace(',', '')) if match else None
                return None

            status_df['Balance'] = status_df['Comment'].apply(extract_balance)

        if status_df['Balance'].isna().all():
            return {'compliant': False, 'reason': 'Geen balansdata beschikbaar', 'details': {}}

        status_df['Balance'] = pd.to_numeric(status_df['Balance'], errors='coerce')
        daily_status = status_df.groupby('Date').agg(
            min_balance=('Balance', 'min'),
            max_balance=('Balance', 'max'),
            close_balance=('Balance', 'last')
        ).reset_index()

        daily_status['prev_close'] = daily_status['close_balance'].shift(1).fillna(initial_balance)
        daily_status['daily_pnl'] = daily_status['close_balance'] - daily_status['prev_close']
        daily_status['daily_pnl_pct'] = (daily_status['daily_pnl'] / daily_status['prev_close']) * 100
        daily_status['daily_drawdown'] = (daily_status['min_balance'] - daily_status['prev_close']) / daily_status[
            'prev_close'] * 100
        daily_status['peak'] = daily_status['close_balance'].cummax()
        daily_status['drawdown_from_peak'] = (daily_status['close_balance'] - daily_status['peak']) / daily_status[
            'peak'] * 100
        max_drawdown = daily_status['drawdown_from_peak'].min()

        latest_balance = daily_status['close_balance'].iloc[-1]
        total_pnl = latest_balance - initial_balance
        total_pnl_pct = (total_pnl / initial_balance) * 100

        trade_df = df[df['Type'] == 'TRADE']
        unique_trading_days = trade_df['Date'].nunique()

        profit_target_met = total_pnl_pct >= self.ftmo_rules['profit_target'] * 100
        daily_loss_compliant = daily_status['daily_drawdown'].min() > -self.ftmo_rules['max_daily_loss'] * 100
        total_loss_compliant = max_drawdown > -self.ftmo_rules['max_total_loss'] * 100
        trading_days_compliant = unique_trading_days >= self.ftmo_rules['min_trading_days']
        compliant = profit_target_met and daily_loss_compliant and total_loss_compliant and trading_days_compliant

        reasons = []
        if not profit_target_met:
            reasons.append(
                f"Winstdoel niet bereikt: {total_pnl_pct:.2f}% (doel: {self.ftmo_rules['profit_target'] * 100}%)")
        if not daily_loss_compliant:
            worst_day_idx = daily_status['daily_drawdown'].idxmin()
            worst_day = daily_status.iloc[worst_day_idx]
            reasons.append(
                f"Dagelijkse verlieslimiet overschreden: {worst_day['daily_drawdown']:.2f}% op {worst_day['Date']}")
        if not total_loss_compliant:
            reasons.append(
                f"Maximale drawdown overschreden: {max_drawdown:.2f}% (limiet: -{self.ftmo_rules['max_total_loss'] * 100}%)")
        if not trading_days_compliant:
            reasons.append(
                f"Onvoldoende handelsdagen: {unique_trading_days} (minimaal: {self.ftmo_rules['min_trading_days']})")

        reason = "; ".join(reasons) if reasons else "Voldoet aan alle FTMO-regels"

        details = {
            'initial_balance': initial_balance,
            'final_balance': latest_balance,
            'total_pnl': total_pnl,
            'total_pnl_pct': total_pnl_pct,
            'max_drawdown': max_drawdown,
            'trading_days': unique_trading_days,
            'daily_stats': daily_status
        }

        return {'compliant': compliant, 'reason': reason, 'details': details}

    def plot_ftmo_compliance(self, initial_balance: float = None) -> Optional[str]:
        """
        Maak een visualisatie van FTMO-naleving met extra analyses.

        Parameters:
        -----------
        initial_balance : float, optional
            Initiële accountbalans (default vanuit config).

        Returns:
        --------
        str
            Pad naar opgeslagen grafiek, of None bij mislukking.
        """
        initial_balance = initial_balance if initial_balance is not None else self.initial_balance
        compliance = self.check_ftmo_compliance(initial_balance)
        if not compliance['details']:
            if self.logger:
                self.logger.log_info("Onvoldoende data voor FTMO-analyse", level="ERROR")
            return None

        daily_stats = compliance['details']['daily_stats']
        fig = plt.figure(figsize=(16, 16))
        gs = fig.add_gridspec(5, 2, height_ratios=[2, 1, 1, 1, 1])

        # 1. Balansgrafiek
        ax1 = fig.add_subplot(gs[0, :])
        ax1.plot(daily_stats['Date'], daily_stats['close_balance'], 'b-', label='Accountbalans')
        ax1.axhline(y=initial_balance, color='gray', linestyle=':', label='Initiële balans')
        ax1.axhline(y=initial_balance * 1.10, color='green', linestyle='--',
                    label=f"+10% Doel (${initial_balance * 1.10:,.2f})")
        ax1.axhline(y=initial_balance * 0.95, color='orange', linestyle='--',
                    label=f"-5% Daglimiet (${initial_balance * 0.95:,.2f})")
        ax1.axhline(y=initial_balance * 0.90, color='red', linestyle='--',
                    label=f"-10% Max Drawdown (${initial_balance * 0.90:,.2f})")
        ax1.set_title('FTMO Accountbalans Progressie', fontsize=16)
        ax1.set_ylabel('Balans ($)', fontsize=14)
        ax1.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
        ax1.legend(loc='best', fontsize=12)
        ax1.grid(True)

        # 2. Dagelijkse P&L
        ax2 = fig.add_subplot(gs[1, 0])
        colors = ['green' if x >= 0 else 'red' for x in daily_stats['daily_pnl']]
        ax2.bar(daily_stats['Date'], daily_stats['daily_pnl'], color=colors, alpha=0.7)
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax2.set_title('Dagelijkse P&L ($)', fontsize=14)
        ax2.set_ylabel('P&L ($)', fontsize=12)
        ax2.grid(True, axis='y')

        # 3. Dagelijkse drawdown
        ax3 = fig.add_subplot(gs[1, 1])
        ax3.fill_between(daily_stats['Date'], daily_stats['daily_drawdown'], 0,
                         where=(daily_stats['daily_drawdown'] < 0), color='red', alpha=0.3)
        ax3.plot(daily_stats['Date'], daily_stats['daily_drawdown'], 'r-', alpha=0.7)
        ax3.axhline(y=-5, color='orange', linestyle='--', label='-5% Daglimiet')
        ax3.set_title('Dagelijkse Drawdown (%)', fontsize=14)
        ax3.set_ylabel('Drawdown (%)', fontsize=12)
        ax3.set_ylim(max(-15, daily_stats['daily_drawdown'].min() * 1.2), 5)
        ax3.legend(loc='lower right', fontsize=10)
        ax3.grid(True)

        # 4. Cumulatieve drawdown vanaf piek
        ax4 = fig.add_subplot(gs[2, :])
        ax4.fill_between(daily_stats['Date'], daily_stats['drawdown_from_peak'], 0, color='purple', alpha=0.3)
        ax4.plot(daily_stats['Date'], daily_stats['drawdown_from_peak'], 'purple', alpha=0.7)
        ax4.axhline(y=-10, color='red', linestyle='--', label='-10% Max Drawdown')
        ax4.set_title('Maximale Drawdown vanaf Piek (%)', fontsize=14)
        ax4.set_ylabel('Drawdown (%)', fontsize=12)
        ax4.set_ylim(max(-12, daily_stats['drawdown_from_peak'].min() * 1.2), 2)
        ax4.legend(loc='lower right', fontsize=10)
        ax4.grid(True)

        # 5. Win/Loss Ratio
        trade_df = self.load_trade_data()[self.load_trade_data()['Type'] == 'TRADE']
        if not trade_df.empty:
            profits = \
            trade_df[trade_df['Action'].isin(['SELL', 'BUY']) & (trade_df['Price'].shift(-1) - trade_df['Price'] > 0)][
                'Price'].count()
            losses = \
            trade_df[trade_df['Action'].isin(['SELL', 'BUY']) & (trade_df['Price'].shift(-1) - trade_df['Price'] < 0)][
                'Price'].count()
            win_loss_ratio = profits / losses if losses > 0 else float('inf')
            ax5 = fig.add_subplot(gs[3, :])
            ax5.bar(['Wins', 'Losses'], [profits, losses], color=['green', 'red'])
            ax5.set_title('Win/Loss Ratio', fontsize=14)
            ax5.set_ylabel('Aantal Trades', fontsize=12)
            ax5.text(0.5, -0.1, f"Win/Loss Ratio: {win_loss_ratio:.2f}", transform=ax5.transAxes, ha='center')
            ax5.grid(True, axis='y')

        # 6. Nalevingstabel
        ax6 = fig.add_subplot(gs[4, :])
        ax6.axis('off')
        compliance_data = [
            ['Metriek', 'Waarde', 'Vereiste', 'Status'],
            ['Totale P&L', f"{compliance['details']['total_pnl_pct']:.2f}%",
             f"≥ {self.ftmo_rules['profit_target'] * 100}%",
             '✅' if compliance['details']['total_pnl_pct'] >= 10 else '❌'],
            ['Max Dagelijkse Drawdown', f"{daily_stats['daily_drawdown'].min():.2f}%",
             f"> -{self.ftmo_rules['max_daily_loss'] * 100}%",
             '✅' if daily_stats['daily_drawdown'].min() > -5 else '❌'],
            ['Max Totale Drawdown', f"{compliance['details']['max_drawdown']:.2f}%",
             f"> -{self.ftmo_rules['max_total_loss'] * 100}%",
             '✅' if compliance['details']['max_drawdown'] > -10 else '❌'],
            ['Handelsdagen', f"{compliance['details']['trading_days']}",
             f"≥ {self.ftmo_rules['min_trading_days']}",
             '✅' if compliance['details']['trading_days'] >= 4 else '❌']
        ]
        tbl = ax6.table(cellText=compliance_data, loc='center', cellLoc='center', colWidths=[0.25, 0.25, 0.25, 0.15])
        tbl.auto_set_font_size(False)
        tbl.set_fontsize(14)
        tbl.scale(1, 2)

        header_color = '#40466e'
        pass_color = '#d8f3dc'
        fail_color = '#ffcccb'
        for (i, j), cell in tbl.get_celld().items():
            if i == 0:
                cell.set_facecolor(header_color)
                cell.set_text_props(color='white', fontweight='bold')
            elif j == 3:
                cell.set_facecolor(pass_color if compliance_data[i][3] == '✅' else fail_color)

        overall_status = 'GESLAAGD' if compliance['compliant'] else 'GEFAALD'
        status_color = 'green' if compliance['compliant'] else 'red'
        ax6.set_title(f"FTMO Naleving: {overall_status}", fontsize=18, color=status_color, fontweight='bold')
        if not compliance['compliant']:
            ax6.text(0.5, 0.1, compliance['reason'], horizontalalignment='center', fontsize=12, color='red',
                     transform=ax6.transAxes)

        plt.tight_layout()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"ftmo_compliance_{timestamp}.png")
        plt.savefig(output_path, dpi=150)
        plt.close()
        if self.logger:
            self.logger.log_info(f"FTMO nalevingsgrafiek opgeslagen als {output_path}")
        return output_path

    def generate_trading_report(self, initial_balance: float = None) -> bool:
        """
        Genereer een gedetailleerd FTMO handelsrapport met extra metrics.

        Parameters:
        -----------
        initial_balance : float, optional
            Initiële accountbalans (default vanuit config).

        Returns:
        --------
        bool
            True als rapport succesvol gegenereerd.
        """
        initial_balance = initial_balance if initial_balance is not None else self.initial_balance
        try:
            compliance = self.check_ftmo_compliance(initial_balance)
            if not compliance['details']:
                if self.logger:
                    self.logger.log_info("Onvoldoende data voor rapportgeneratie", level="ERROR")
                return False

            compliance_path = self.plot_ftmo_compliance(initial_balance)
            df = self.load_trade_data()
            trade_df = df[df['Type'] == 'TRADE'].copy()

            # Instrumentanalyse
            symbol_stats = {}
            for symbol in trade_df['Symbol'].unique():
                symbol_df = trade_df[trade_df['Symbol'] == symbol]
                wins = len(symbol_df[symbol_df['Action'].isin(['SELL', 'BUY']) & (
                            symbol_df['Price'].shift(-1) - symbol_df['Price'] > 0)])
                losses = len(symbol_df[symbol_df['Action'].isin(['SELL', 'BUY']) & (
                            symbol_df['Price'].shift(-1) - symbol_df['Price'] < 0)])
                symbol_stats[symbol] = {
                    'total_trades': len(symbol_df),
                    'wins': wins,
                    'losses': losses,
                    'win_rate': (wins / (wins + losses) * 100) if (wins + losses) > 0 else 0,
                    'days_traded': symbol_df['Date'].nunique()
                }

            # Rapportweergave
            report = "\n===== FTMO Handelsrapport =====\n"
            report += f"Periode: {df['Timestamp'].min().date() if not df.empty else 'N/A'} tot {df['Timestamp'].max().date() if not df.empty else 'N/A'}\n"
            report += f"Initiële balans: ${initial_balance:,.2f}\n"
            report += f"Eindebalans: ${compliance['details']['final_balance']:,.2f}\n"
            report += f"Totale P&L: ${compliance['details']['total_pnl']:,.2f} ({compliance['details']['total_pnl_pct']:.2f}%)\n"
            report += f"Maximale drawdown: {compliance['details']['max_drawdown']:.2f}%\n"
            report += f"Aantal handelsdagen: {compliance['details']['trading_days']}\n"
            report += "\nInstrumentanalyse:\n"
            for symbol, stats in symbol_stats.items():
                report += f"  {symbol}: {stats['total_trades']} trades ({stats['wins']} wins, {stats['losses']} losses, Win Rate: {stats['win_rate']:.2f}%) over {stats['days_traded']} dagen\n"
            report += f"\nFTMO Naleving: {'GESLAAGD' if compliance['compliant'] else 'GEFAALD'}\n"
            if not compliance['compliant']:
                report += f"Reden: {compliance['reason']}\n"
            if compliance_path:
                report += f"\nNalevingsvisualisatie opgeslagen als: {os.path.basename(compliance_path)}\n"

            # Extra metrics
            total_trades = len(trade_df)
            avg_trade_size = trade_df['Volume'].mean() if not trade_df.empty else 0
            report += f"\nExtra Metrics:\n"
            report += f"  Totaal aantal trades: {total_trades}\n"
            report += f"  Gemiddelde trade grootte: {avg_trade_size:.2f} lots\n"

            print(report)

            if self.logger:
                self.logger.log_info(f"FTMO Rapport gegenereerd - Compliant: {compliance['compliant']}")
                if not compliance['compliant']:
                    self.logger.log_info(f"Reden voor niet-naleving: {compliance['reason']}")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = os.path.join(self.output_dir, f"ftmo_report_{timestamp}.txt")
            with open(report_path, 'w') as f:
                f.write(report)

            return True
        except Exception as e:
            if self.logger:
                self.logger.log_info(f"Fout bij rapportgeneratie: {e}", level="ERROR")
            return False
```

-----------

Path: src/monitoring/__init__.py

```python
```

-----------

Path: src/presentation/__init__.py

```python
```

-----------

Path: src/presentation/dashboard.py

```python
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
```

-----------

Path: src/risk/__init__.py

```python
```

-----------

Path: src/risk/position_sizer.py

```python
def calculate_position_size(
        entry_price: float,
        stop_loss: float,
        account_balance: float,
        risk_percentage: float,
        pip_value: float,
        min_lot: float = 0.01,
        max_lot: float = 10.0
) -> float:
    """
    Calculate optimal position size based on risk parameters

    Args:
        entry_price: Entry price for the position
        stop_loss: Stop loss price
        account_balance: Current account balance
        risk_percentage: Percentage of account to risk (0.01 = 1%)
        pip_value: Value of one pip in account currency
        min_lot: Minimum allowable lot size
        max_lot: Maximum allowable lot size

    Returns:
        Calculated position size in lots
    """
    if entry_price == stop_loss:
        return min_lot  # Avoid division by zero

    # Calculate risk amount in account currency
    risk_amount = account_balance * risk_percentage

    # Calculate pips at risk
    pips_at_risk = abs(entry_price - stop_loss) / 0.0001  # For 4-digit forex pairs

    # Calculate lot size
    lot_size = risk_amount / (pips_at_risk * pip_value)

    # Enforce limits
    lot_size = max(min_lot, min(lot_size, max_lot))

    # Round to 2 decimal places
    lot_size = round(lot_size, 2)

    return lot_size
```

-----------

Path: src/risk/risk_manager.py

```python
# src/risk/risk_manager.py
from datetime import date
from typing import Dict, Optional, Tuple


class RiskManager:
    """
    Risicomanagement met FTMO compliance checks.

    Verantwoordelijk voor het bewaken van risicoparameters zoals dagelijkse verlieslimiet,
    maximale drawdown, en positiegrootte berekeningen volgens risicoregels.
    """

    def __init__(self, config: Dict, logger):
        """Initialiseer met configuratieparameters"""
        self.config = config
        self.logger = logger

        # Extraheer risicoparameters
        self.max_risk_per_trade = self.config.get('max_risk_per_trade', 0.01)
        self.max_daily_drawdown = self.config.get('max_daily_drawdown', 0.05)
        self.max_total_drawdown = self.config.get('max_total_drawdown', 0.10)
        self.leverage = self.config.get('leverage', 30)

        # Initialiseer tracking variabelen
        self.daily_losses = 0
        self.current_date = date.today()
        self.initial_balance = self.config.get('account_balance', 100000)
        self.daily_trades_count = 0
        self.max_daily_trades = self.config.get('max_daily_trades', 10)

        self.logger.log_info(f"RiskManager geïnitialiseerd met max risk per trade: {self.max_risk_per_trade * 100}%, "
                             f"max daily drawdown: {self.max_daily_drawdown * 100}%, "
                             f"max total drawdown: {self.max_total_drawdown * 100}%, "
                             f"leverage: {self.leverage}")

    def check_ftmo_limits(self, account_info: Dict) -> Tuple[bool, Optional[str]]:
        """
        Controleer of huidige accountstatus voldoet aan FTMO-limieten

        Parameters:
        -----------
        account_info : Dict
            Dictionary met huidige accountinformatie

        Returns:
        --------
        Tuple van (stop_trading, reason)
        - stop_trading: True als trading gestopt moet worden
        - reason: Beschrijving waarom trading moet stoppen, of None
        """
        # Reset dagelijkse variabelen als het een nieuwe dag is
        today = date.today()
        if today != self.current_date:
            self.daily_losses = 0
            self.daily_trades_count = 0
            self.current_date = today
            self.logger.log_info("Dagelijkse risico limieten gereset (nieuwe handelsdag)")

        # Haal account data op
        current_balance = account_info.get('balance', 0)
        current_equity = account_info.get('equity', 0)

        # Bereken winst/verlies percentages
        balance_change_pct = (current_balance - self.initial_balance) / self.initial_balance
        equity_change_pct = (current_equity - self.initial_balance) / self.initial_balance

        # Controleer of winstdoel is bereikt (10%)
        if balance_change_pct >= 0.10:
            return True, f"Winstdoel bereikt: {balance_change_pct:.2%}"

        # Controleer dagelijkse verlieslimiet (5%)
        if equity_change_pct <= -self.max_daily_drawdown:
            return True, f"Dagelijkse verlieslimiet bereikt: {equity_change_pct:.2%}"

        # Controleer totale verlieslimiet (10%)
        if equity_change_pct <= -self.max_total_drawdown:
            return True, f"Maximale drawdown bereikt: {equity_change_pct:.2%}"

        # Alles is binnen limieten
        return False, None

    def calculate_position_size(self,
                                symbol: str,
                                entry_price: float,
                                stop_loss: float,
                                account_balance: float,
                                trend_strength: float = 0.5) -> float:
        """
        Bereken optimale positiegrootte gebaseerd op risicoparameters

        Parameters:
        -----------
        symbol : str
            Trading symbool
        entry_price : float
            Ingangsprijs voor de positie
        stop_loss : float
            Stop loss prijs
        account_balance : float
            Huidige account balans
        trend_strength : float
            Sterkte van de trend (0-1), gebruikt voor positiegrootte aanpassing

        Returns:
        --------
        float : Berekende positiegrootte in lots
        """
        if entry_price == 0 or stop_loss == 0:
            self.logger.log_info(f"Ongeldige entry of stop loss voor {symbol}", level="ERROR")
            return 0.01

        # Voorkom delen door nul
        if entry_price == stop_loss:
            self.logger.log_info(f"Entry gelijk aan stop loss voor {symbol}", level="WARNING")
            return 0.01

        # Bereken risicobedrag in accountvaluta
        risk_amount = account_balance * self.max_risk_per_trade

        # Pas risico aan op basis van trendsterkte
        adjusted_risk = risk_amount * (0.5 + trend_strength / 2)  # 50-100% van normaal risico

        # Bereken pips op risico
        pips_at_risk = abs(entry_price - stop_loss) / 0.0001  # Voor 4-cijferige forex paren

        # Pas aan voor goud en indices indien nodig
        if symbol == "XAUUSD":
            pips_at_risk = abs(entry_price - stop_loss) / 0.01  # Voor goud (0.01 = 1 pip)
        elif symbol in ["US30", "US30.cash", "US500", "USTEC"]:
            pips_at_risk = abs(entry_price - stop_loss) / 0.1  # Voor indices

        # Schat pip waarde (kan worden verbeterd met exacte berekening per symbool)
        pip_value = 10.0  # Standaard pip waarde voor 1 lot

        # Bereken lot size
        lot_size = adjusted_risk / (pips_at_risk * pip_value)

        # Rond af naar 2 decimalen en begrens tussen min/max waarden
        min_lot = 0.01
        max_lot = 10.0
        lot_size = max(min_lot, min(lot_size, max_lot))
        lot_size = round(lot_size, 2)

        self.logger.log_info(f"Berekende positiegrootte voor {symbol}: {lot_size} lots "
                             f"(Risk: ${adjusted_risk:.2f}, Pips: {pips_at_risk:.1f})")

        return lot_size

    def check_trade_risk(self,
                         symbol: str,
                         volume: float,
                         entry_price: float,
                         stop_loss: float) -> bool:
        """
        Controleer of een trade binnen de risicolimieten valt

        Parameters:
        -----------
        symbol : str
            Trading symbool
        volume : float
            Positiegrootte in lots
        entry_price : float
            Ingangsprijs voor de positie
        stop_loss : float
            Stop loss prijs

        Returns:
        --------
        bool : True als trade binnen risicolimieten valt, anders False
        """
        # Controleer dagelijks aantal trades
        self.daily_trades_count += 1
        if self.daily_trades_count > self.max_daily_trades:
            self.logger.log_info(f"Maximaal aantal dagelijkse trades bereikt: {self.max_daily_trades}", level="WARNING")
            return False

        # Als er geen stop loss is, is dit een hoog risico en accepteren we de trade niet
        if stop_loss == 0:
            self.logger.log_info(f"Trade geweigerd voor {symbol}: Geen stop loss ingesteld", level="WARNING")
            return False

        # Berekening potentieel verlies
        pip_value = 10.0  # Standaard pip waarde voor 1 lot
        pips_at_risk = abs(entry_price - stop_loss) / 0.0001

        # Pas aan voor goud en indices indien nodig
        if symbol == "XAUUSD":
            pips_at_risk = abs(entry_price - stop_loss) / 0.01
        elif symbol in ["US30", "US30.cash", "US500", "USTEC"]:
            pips_at_risk = abs(entry_price - stop_loss) / 0.1

        potential_loss = pips_at_risk * pip_value * volume

        # Controleer tegen dagelijkse verlieslimiet
        max_daily_loss = self.initial_balance * self.max_daily_drawdown
        if self.daily_losses + potential_loss > max_daily_loss:
            self.logger.log_info(f"Trade geweigerd voor {symbol}: Zou dagelijkse verlieslimiet overschrijden",
                                 level="WARNING")
            return False

        # Extra validatie voor extreem grote posities
        if volume > 5.0:  # Voorbeeld van een arbitraire limiet
            self.logger.log_info(f"Trade geweigerd voor {symbol}: Volume te groot ({volume} lots)", level="WARNING")
            return False

        # Trade geaccepteerd
        return True

    def can_trade(self) -> bool:
        """
        Controleert of trading is toegestaan op basis van huidige limieten

        Returns:
        --------
        bool : True als trading is toegestaan, anders False
        """
        # Reset dagelijkse variabelen als het een nieuwe dag is
        today = date.today()
        if today != self.current_date:
            self.daily_losses = 0
            self.daily_trades_count = 0
            self.current_date = today

        # Controleer dagelijks aantal trades
        if self.daily_trades_count >= self.max_daily_trades:
            return False

        return True

    def update_daily_loss(self, loss_amount: float) -> None:
        """
        Update het dagelijkse verliestotaal

        Parameters:
        -----------
        loss_amount : float
            Verliesbedrag (positief voor verlies, negatief voor winst)
        """
        # Reset als het een nieuwe dag is
        today = date.today()
        if today != self.current_date:
            self.daily_losses = 0
            self.daily_trades_count = 0
            self.current_date = today

        # Update dagelijkse verliezen
        if loss_amount > 0:  # Alleen verliesposities bijhouden
            self.daily_losses += loss_amount
            self.logger.log_info(f"Dagelijks verlies bijgewerkt: ${self.daily_losses:.2f} "
                                 f"(Max: ${self.initial_balance * self.max_daily_drawdown:.2f})")
```

-----------

Path: src/strategy/__init__.py

```python
```

-----------

Path: src/strategy/base_strategy.py

```python
# src/strategy/base_strategy.py
from abc import ABC, abstractmethod
from typing import Dict, Any, List


class Strategy(ABC):
    """
    Abstracte basisklasse voor alle handelsstrategieën.

    Deze klasse definieert de interface die alle strategieën moeten implementeren.
    Door deze basisklasse te gebruiken, kunnen we gemakkelijk nieuwe strategieën
    toevoegen zonder de rest van de code aan te hoeven passen.
    """

    def __init__(self, connector, risk_manager, logger, config):
        """
        Initialiseer de strategie met de benodigde componenten

        Parameters:
        -----------
        connector : Connector naar handelsplatform (bijv. MT5)
        risk_manager : Risicobeheer component
        logger : Logging component
        config : Configuratiegegevens voor de strategie
        """
        self.connector = connector
        self.risk_manager = risk_manager
        self.logger = logger
        self.config = config
        self.name = "Base Strategy"

    @abstractmethod
    def process_symbol(self, symbol: str) -> Dict[str, Any]:
        """
        Verwerk een symbool volgens de strategie regels

        Parameters:
        -----------
        symbol : str
            Het te verwerken symbool

        Returns:
        --------
        Dict : Resultaten van de verwerking, inclusief eventuele signalen
        """
        pass

    @abstractmethod
    def calculate_indicators(self, data: Any) -> Dict[str, Any]:
        """
        Bereken de technische indicatoren voor de strategie

        Parameters:
        -----------
        data : Any
            Prijsgegevens en andere input

        Returns:
        --------
        Dict : Berekende indicatoren
        """
        pass

    def get_name(self) -> str:
        """
        Geef de naam van de strategie terug

        Returns:
        --------
        str : Strategienaam
        """
        return self.name

    def get_open_positions(self) -> Dict[str, List]:
        """
        Haal alle open posities op

        Returns:
        --------
        Dict : Dictionary met open posities per symbool
        """
        return {}
```

-----------

Path: src/strategy/dax_opening.py

```python
```

-----------

Path: src/strategy/strategy_factory.py

```python
# src/strategy/strategy_factory.py
import copy
import importlib
import os
from typing import Optional

from src.strategy.base_strategy import Strategy


class StrategyFactory:
    """Factory voor het creëren van trading strategie-instanties"""

    _strategies = {}

    @classmethod
    def _load_strategies(cls):
        """Laad beschikbare strategieën dynamisch uit de strategy directory"""
        if cls._strategies:
            return

        # Zoek naar strategie modules in de src/strategy directory
        strategy_dir = os.path.dirname(os.path.abspath(__file__))
        for filename in os.listdir(strategy_dir):
            if filename.endswith('_strategy.py') and filename != 'base_strategy.py':
                module_name = filename[:-3]  # Verwijder .py

                try:
                    # Import de module
                    module_path = f"src.strategy.{module_name}"
                    module = importlib.import_module(module_path)

                    # Zoek naar classes die Strategy erven
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if isinstance(attr, type) and issubclass(attr, Strategy) and attr is not Strategy:
                            # Registreer de strategie
                            strategy_key = module_name.replace('_strategy', '')
                            cls._strategies[strategy_key] = attr
                except (ImportError, AttributeError) as e:
                    print(f"Kon strategie module {module_name} niet laden: {e}")

        # Voeg de turtle strategie toe als deze niet automatisch geladen is
        if 'turtle' not in cls._strategies:
            try:
                from src.strategy.turtle_strategy import TurtleStrategy
                cls._strategies['turtle'] = TurtleStrategy
            except ImportError:
                pass

    @classmethod
    def create_strategy(
            cls,
            strategy_name: str,
            connector: Optional[object],
            risk_manager: Optional[object],
            logger: Optional[object],
            config: Optional[dict]
    ) -> Strategy:
        """
        Creëert een instantie van de gevraagde strategie.

        Args:
            strategy_name (str): Naam van de strategie.
            connector: MT5 connector instantie.
            risk_manager: Risk manager instantie.
            logger: Logger instantie.
            config (dict): Configuratieobject.

        Returns:
            Strategy: Een instantie van de gevraagde strategie.

        Raises:
            ValueError: Als de strategie niet bestaat.
        """
        # Laad beschikbare strategieën
        cls._load_strategies()

        # Controleer of de gevraagde strategie bestaat
        if strategy_name not in cls._strategies:
            # Speciale geval: turtle_swing is dezelfde als turtle maar met swing modus
            if strategy_name == 'turtle_swing' and 'turtle' in cls._strategies:
                strategy_name = 'turtle'
                if config and 'strategy' in config:
                    config['strategy']['swing_mode'] = True
            else:
                if logger:
                    logger.log_info(f"Onbekende strategie: {strategy_name}", level="ERROR")
                raise ValueError(f"Onbekende strategie: {strategy_name}")

        strategy_class = cls._strategies[strategy_name]

        # Maak een kopie van de config om mutatie te vermijden
        local_config = copy.deepcopy(config) if config else {}

        return strategy_class(connector, risk_manager, logger, local_config)

    @classmethod
    def list_available_strategies(cls) -> list:
        """Geeft een lijst van beschikbare strategieën."""
        cls._load_strategies()
        return list(cls._strategies.keys())
```

-----------

Path: src/strategy/turtle_strategy.py

```python
from datetime import datetime
from typing import Dict, List, Any

import MetaTrader5 as mt5
import pandas as pd

# Voorbeeld imports (pas aan naar je daadwerkelijke module-structuur)
from src.connector.mt5_connector import MT5Connector  # Placeholder
from src.risk.risk_manager import RiskManager  # Placeholder
from src.strategy.base_strategy import Strategy
from src.utils.logger import Logger  # Placeholder


class TurtleStrategy(Strategy):
    """Implementatie van de Turtle Trading strategie geoptimaliseerd voor FTMO met ondersteuning voor swing modus."""

    def __init__(self, connector: MT5Connector, risk_manager: RiskManager, logger: Logger, config: dict):
        """
        Initialiseer de Turtle strategie.

        Parameters:
        -----------
        connector : MT5Connector
            Verbinding met MetaTrader 5.
        risk_manager : RiskManager
            Risicobeheer component.
        logger : Logger
            Component voor logging.
        config : dict
            Configuratie voor de strategie, inclusief mt5- en strategy-secties.
        """
        super().__init__(connector, risk_manager, logger, config)
        self.name = "Turtle Trading Strategy"
        self.position_initial_volumes: Dict[int, float] = {}  # Ticket -> initiële volume
        self.strategy_config = config.get('strategy', {})
        self.swing_mode = self.strategy_config.get('swing_mode', False)

        # Stel parameters in gebaseerd op modus
        if self.swing_mode:
            self.entry_period = self.strategy_config.get('entry_period', 40)
            self.exit_period = self.strategy_config.get('exit_period', 20)
            self.atr_period = self.strategy_config.get('atr_period', 20)
            self.atr_multiplier = self.strategy_config.get('atr_multiplier', 2.5)
            self.logger.log_info(
                "Strategie geïnitialiseerd in Swing modus met parameters: "
                f"entry_period={self.entry_period}, exit_period={self.exit_period}, "
                f"atr_period={self.atr_period}, atr_multiplier={self.atr_multiplier}"
            )
        else:
            self.entry_period = self.strategy_config.get('entry_period', 20)
            self.exit_period = self.strategy_config.get('exit_period', 10)
            self.atr_period = self.strategy_config.get('atr_period', 20)
            self.atr_multiplier = self.strategy_config.get('atr_multiplier', 2.0)
            self.logger.log_info(
                "Strategie geïnitialiseerd in standaard modus met parameters: "
                f"entry_period={self.entry_period}, exit_period={self.exit_period}, "
                f"atr_period={self.atr_period}, atr_multiplier={self.atr_multiplier}"
            )

        self.use_trend_filter = self.strategy_config.get('use_trend_filter', True)

    def calculate_indicators(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Bereken technische indicatoren voor de Turtle strategie.

        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame met prijsdata (high, low, close, tick_volume).

        Returns:
        --------
        Dict[str, Any]
            Berekende indicatoren voor de laatste rij.
        """
        if df.empty or 'high' not in df.columns or 'low' not in df.columns or 'close' not in df.columns:
            return {}

        # Bereken ATR
        df['atr'] = self.calculate_atr(df)

        # Bereken Donchian kanalen
        df['high_entry'] = df['high'].rolling(window=self.entry_period).max()
        df['low_entry'] = df['low'].rolling(window=self.entry_period).min()
        df['high_exit'] = df['high'].rolling(window=self.exit_period).max()
        df['low_exit'] = df['low'].rolling(window=self.exit_period).min()

        # Voeg volume-indicator toe
        df['vol_avg_50'] = df['tick_volume'].rolling(window=50).mean()
        df['vol_ratio'] = df['tick_volume'] / df['vol_avg_50'].replace(0, 1)  # Vermijd deling door 0

        # Trendfilters
        if len(df) >= 50:
            df['ema_50'] = df['close'].ewm(span=50, adjust=False).mean()
        if len(df) >= 200:
            df['ema_200'] = df['close'].ewm(span=200, adjust=False).mean()

        if 'ema_50' in df.columns:
            df['trend_bullish'] = df['close'] > df['ema_50']
        if 'ema_50' in df.columns and 'ema_200' in df.columns:
            df['strong_trend'] = df['ema_50'] > df['ema_200']
        if 'ema_50' in df.columns:
            df['trend_strength'] = self.calculate_trend_strength(df)
        if 'atr' in df.columns:
            df['high_volatility'] = self.calculate_market_volatility(df)

        # Retourneer laatste waarden
        return {
            'atr': df['atr'].iloc[-1] if 'atr' in df else None,
            'high_entry': df['high_entry'].iloc[-2] if 'high_entry' in df else None,
            'low_entry': df['low_entry'].iloc[-2] if 'low_entry' in df else None,
            'high_exit': df['high_exit'].iloc[-2] if 'high_exit' in df else None,
            'low_exit': df['low_exit'].iloc[-2] if 'low_exit' in df else None,
            'trend_bullish': df['trend_bullish'].iloc[-1] if 'trend_bullish' in df else None,
            'strong_trend': df['strong_trend'].iloc[-1] if 'strong_trend' in df else None,
            'trend_strength': df['trend_strength'].iloc[-1] if 'trend_strength' in df else None,
            'high_volatility': df['high_volatility'].iloc[-1] if 'high_volatility' in df else None,
            'vol_ratio': df['vol_ratio'].iloc[-1] if 'vol_ratio' in df else None
        }

    def calculate_atr(self, df: pd.DataFrame) -> pd.Series:
        """
        Bereken de Average True Range (ATR).

        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame met prijsdata (high, low, close).

        Returns:
        --------
        pd.Series
            ATR waarden.
        """
        if 'close' not in df.columns or df['close'].isna().all():
            return pd.Series([0] * len(df), index=df.index)
        high = df['high']
        low = df['low']
        close = df['close'].shift(1).fillna(method='bfill')

        tr1 = high - low
        tr2 = abs(high - close)
        tr3 = abs(low - close)
        tr = pd.DataFrame({'tr1': tr1, 'tr2': tr2, 'tr3': tr3}).max(axis=1)
        return tr.rolling(window=self.atr_period, min_periods=1).mean()

    def calculate_trend_strength(self, df: pd.DataFrame) -> float:
        """
        Bereken trendsterkte gebaseerd op EMA-afstand en -hoek.

        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame met prijsdata.

        Returns:
        --------
        float
            Trendsterkte (0-1).
        """
        if 'ema_50' not in df.columns or len(df) < 10:
            return 0.0
        latest_close = df['close'].iloc[-1]
        latest_ema = df['ema_50'].iloc[-1]
        ema_slope = (df['ema_50'].iloc[-1] - df['ema_50'].iloc[-10]) / df['ema_50'].iloc[-10] if df['ema_50'].iloc[
                                                                                                     -10] != 0 else 0
        latest_atr = df['atr'].iloc[-1] if 'atr' in df and not pd.isna(df['atr'].iloc[-1]) else latest_close * 0.01
        distance = (latest_close - latest_ema) / latest_atr
        distance_score = min(1.0, max(0.0, distance / 3))
        slope_score = min(1.0, max(0.0, ema_slope * 20))
        return min(1.0, max(0.0, (distance_score * 0.7) + (slope_score * 0.3)))

    def calculate_market_volatility(self, df: pd.DataFrame) -> bool:
        """
        Bepaal of de markt in een hoge volatiliteitsperiode zit.

        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame met prijsdata.

        Returns:
        --------
        bool
            True als volatiliteit hoog is.
        """
        if 'atr' not in df.columns or len(df) < 20:
            return False
        avg_atr = df['atr'].iloc[-20:].mean()
        if pd.isna(avg_atr) or avg_atr == 0:
            return False
        current_atr = df['atr'].iloc[-1]
        return current_atr > (avg_atr * 1.3) if not pd.isna(current_atr) else False

    def process_symbol(self, symbol: str) -> Dict[str, Any]:
        """
        Verwerk een symbool volgens de Turtle strategie.

        Parameters:
        -----------
        symbol : str
            Het te verwerken symbool.

        Returns:
        --------
        Dict[str, Any]
            Resultaten inclusief signaal en actie.
        """
        result = {'signal': None, 'action': None}
        if not self.risk_manager.can_trade():
            self.logger.log_info(f"Dagelijkse risico-limiet bereikt, geen trades voor {symbol}")
            return result

        timeframe_str = self.config.get('mt5', {}).get('timeframe', 'H4')
        bars_needed = 240 if timeframe_str == 'H1' else 150 if timeframe_str == 'H4' else 200
        df = self.connector.get_historical_data(symbol, timeframe_str, bars_needed)
        if df.empty:
            self.logger.log_info(f"Geen historische data beschikbaar voor {symbol}")
            return result

        indicators = self.calculate_indicators(df)
        if not indicators:
            self.logger.log_info(f"Kon indicatoren niet berekenen voor {symbol}")
            return result

        tick = self.connector.get_symbol_tick(symbol)
        if tick is None:
            self.logger.log_info(f"Kon geen tick informatie krijgen voor {symbol}")
            return result

        current_price = tick.ask
        last_high_entry = indicators.get('high_entry')
        last_low_exit = indicators.get('low_exit')
        current_atr = indicators.get('atr')
        if None in (current_atr, last_high_entry, last_low_exit):
            self.logger.log_info(f"Ontbrekende indicator waarden voor {symbol}")
            return result

        trend_bullish = indicators.get('trend_bullish', True)
        strong_trend = indicators.get('strong_trend', True)
        trend_strength = indicators.get('trend_strength', 0.5)
        high_volatility = indicators.get('high_volatility', False)
        volume_ratio = indicators.get('vol_ratio', 1.0)

        price_breakout = current_price > last_high_entry * 1.001
        volume_filter = volume_ratio > 1.1 if not pd.isna(volume_ratio) else True
        entry_conditions = price_breakout and current_atr > 0 and volume_filter

        if self.use_trend_filter:
            entry_conditions = entry_conditions and trend_bullish
        if self.swing_mode:
            entry_conditions = entry_conditions and strong_trend and not high_volatility

        if entry_conditions:
            self.logger.log_info(f"Breakout gedetecteerd voor {symbol} op {current_price}")
            result['signal'] = 'ENTRY'
            result['action'] = 'BUY'

            sl_multiplier = self.atr_multiplier + 0.5 if high_volatility else self.atr_multiplier
            stop_loss = current_price - (sl_multiplier * current_atr)

            account_info = self.connector.get_account_info()
            account_balance = account_info.get('balance', self.config.get('mt5', {}).get('account_balance', 100000))
            lot_size = self.risk_manager.calculate_position_size(symbol, current_price, stop_loss, account_balance,
                                                                 trend_strength)

            if not self.risk_manager.check_trade_risk(symbol, lot_size, current_price, stop_loss):
                self.logger.log_info(f"Trade overschrijdt risicolimiet voor {symbol}")
                return result

            try:
                ticket = self.connector.place_order(
                    "BUY", symbol, lot_size, stop_loss, 0,
                    comment=f"FTMO {'Swing' if self.swing_mode else 'Turtle'}"
                )
                if ticket:
                    self.position_initial_volumes[ticket] = lot_size
                    self.logger.log_trade(
                        symbol, "BUY", current_price, lot_size, stop_loss, 0,
                        f"{'Swing' if self.swing_mode else 'Turtle'} Entry (TS:{trend_strength:.2f})",
                        self.risk_manager.leverage
                    )
                    result['ticket'] = ticket
                    result['volume'] = lot_size
                    result['stop_loss'] = stop_loss
            except Exception as e:
                self.logger.log_error(f"Fout bij plaatsen order voor {symbol}: {e}")
                return result

        self._manage_positions(symbol, current_price, last_low_exit, current_atr)
        return result

    def _manage_positions(self, symbol: str, current_price: float, last_low_exit: float, current_atr: float) -> None:
        """
        Beheer bestaande posities voor een symbool.

        Parameters:
        -----------
        symbol : str
            Trading symbool.
        current_price : float
            Huidige marktprijs.
        last_low_exit : float
            Laatste Donchian kanaal low exit.
        current_atr : float
            Huidige ATR waarde.
        """
        open_positions = self.connector.get_open_positions(symbol)
        if not open_positions:
            return

        for position in open_positions:
            position_age_days = (datetime.now().timestamp() - position.time) / (60 * 60 * 24)
            if position.type != mt5.POSITION_TYPE_BUY:
                continue

            entry_price = position.price_open
            profit_atr = 1.5 if self.swing_mode else 1.0
            profit_target_1 = entry_price + (profit_atr * current_atr)
            profit_target_2 = entry_price + (profit_atr * 2 * current_atr)
            min_hold_time = 2 if self.swing_mode else 1
            time_condition_met = position_age_days >= min_hold_time

            if (
                    time_condition_met and current_price > profit_target_1 and position.ticket in self.position_initial_volumes):
                initial_volume = self.position_initial_volumes[position.ticket]
                partial_volume = round(initial_volume * 0.4, 2)
                if position.volume >= partial_volume and partial_volume >= 0.01:
                    self.logger.log_info(f"Gedeeltelijke winstneming (40%) voor {symbol} op {current_price}")
                    try:
                        partial_result = self.connector.place_order(
                            "SELL", symbol, partial_volume, 0, 0, f"Partial Profit 40% - ticket:{position.ticket}"
                        )
                        if partial_result:
                            self.logger.log_trade(symbol, "SELL", current_price, partial_volume, 0, 0,
                                                  "Partial Profit 40%")
                            remaining_volume = position.volume - partial_volume
                            if remaining_volume >= 0.01:
                                self.connector.modify_position(position.ticket, stop_loss=entry_price, take_profit=0)
                                self.position_initial_volumes[position.ticket] = remaining_volume
                    except Exception as e:
                        self.logger.log_error(f"Fout bij gedeeltelijke winstneming voor {symbol}: {e}")

            elif (
                    time_condition_met and current_price > profit_target_2 and position.ticket in self.position_initial_volumes):
                initial_volume = self.position_initial_volumes[position.ticket]
                remaining_pct = 0.6
                partial_volume = round(initial_volume * remaining_pct * 0.5, 2)
                if position.volume >= partial_volume and partial_volume >= 0.01:
                    self.logger.log_info(f"Gedeeltelijke winstneming (30%) voor {symbol} op {current_price}")
                    try:
                        partial_result = self.connector.place_order(
                            "SELL", symbol, partial_volume, 0, 0, f"Partial Profit 30% - ticket:{position.ticket}"
                        )
                        if partial_result:
                            self.logger.log_trade(symbol, "SELL", current_price, partial_volume, 0, 0,
                                                  "Partial Profit 30%")
                            remaining_volume = position.volume - partial_volume
                            if remaining_volume >= 0.01:
                                new_sl = entry_price + ((current_price - entry_price) * 0.5)
                                self.connector.modify_position(position.ticket, stop_loss=new_sl, take_profit=0)
                                self.position_initial_volumes[position.ticket] = remaining_volume
                    except Exception as e:
                        self.logger.log_error(f"Fout bij tweede winstneming voor {symbol}: {e}")

            elif current_price < last_low_exit:
                self.logger.log_info(f"Exit signaal voor {symbol} op {current_price}")
                try:
                    close_result = self.connector.place_order(
                        "SELL", symbol, position.volume, 0, 0,
                        f"{'Swing' if self.swing_mode else 'Turtle'} Exit - ticket:{position.ticket}"
                    )
                    if close_result:
                        self.logger.log_trade(
                            symbol, "SELL", current_price, position.volume, 0, 0,
                            f"{'Swing' if self.swing_mode else 'Turtle'} System Exit"
                        )
                        if position.ticket in self.position_initial_volumes:
                            del self.position_initial_volumes[position.ticket]
                except Exception as e:
                    self.logger.log_error(f"Fout bij sluiten positie voor {symbol}: {e}")

    def get_open_positions(self) -> Dict[str, List]:
        """
        Haal alle open posities op per symbool.

        Returns:
        --------
        Dict[str, List]
            Dictionary met open posities per symbool.
        """
        result = {}
        symbols = self.config.get('mt5', {}).get('symbols', [])
        for symbol in symbols:
            positions = self.connector.get_open_positions(symbol)
            if positions:
                result[symbol] = positions
        return result
```

-----------

Path: src/utils/__init__.py

```python
```

-----------

Path: src/utils/config.py

```python
# src/utils/config.py
import json
import os
from typing import Dict, Any


def load_config(config_path: str = None) -> Dict[str, Any]:
    """
    Laad configuratie uit JSON bestand met validatie

    Parameters:
    -----------
    config_path : str, optional
        Pad naar het configuratiebestand. Als niet opgegeven wordt standaard pad gebruikt.

    Returns:
    --------
    Dict[str, Any] : Geladen configuratie

    Raises:
    -------
    FileNotFoundError : Als het configuratiebestand niet gevonden kan worden
    ValueError : Als het configuratiebestand ongeldige JSON bevat
    """
    if config_path is None:
        config_path = os.environ.get("SOPHY_CONFIG_PATH", "config/settings.json")

    try:
        with open(config_path, 'r') as file:
            config = json.load(file)

        # Valideer vereiste secties
        required_sections = ['mt5', 'risk', 'strategy']
        for section in required_sections:
            if section not in config:
                raise ValueError(f"Sectie '{section}' ontbreekt in configuratie")

        # Pas standaardwaarden toe
        if 'mt5' in config:
            config['mt5'].setdefault('timeframe', 'H4')
            config['mt5'].setdefault('symbols', ['EURUSD'])
            config['mt5'].setdefault('account_balance', 100000)

        if 'risk' in config:
            config['risk'].setdefault('max_risk_per_trade', 0.01)
            config['risk'].setdefault('max_daily_drawdown', 0.05)
            config['risk'].setdefault('max_total_drawdown', 0.10)
            config['risk'].setdefault('leverage', 30)

        if 'logging' not in config:
            config['logging'] = {'log_file': 'logs/trading_log.csv', 'log_level': 'INFO'}

        return config
    except FileNotFoundError:
        print(f"Configuratiebestand niet gevonden: {config_path}")
        raise
    except json.JSONDecodeError as e:
        print(f"Ongeldige JSON in configuratiebestand: {config_path}")
        raise ValueError(f"Ongeldige JSON in configuratiebestand: {str(e)}")
```

-----------

Path: src/utils/indicators.py

```python
# sophy/utils/indicators.py
from typing import Tuple

import numpy as np
import pandas as pd


def calculate_atr(df: pd.DataFrame, period: int = 14) -> np.ndarray:
    """
    Bereken Average True Range (ATR) met gevectoriseerde operaties

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame met OHLC data
    period : int
        ATR berekening periode

    Returns:
    --------
    np.ndarray : Array met ATR waarden
    """
    high = df['high'].values
    low = df['low'].values
    close = np.roll(df['close'].values, 1)
    close[0] = 0

    # Bereken true range componenten
    tr1 = high - low
    tr2 = np.abs(high - close)
    tr3 = np.abs(low - close)

    # Bereken true range als maximum van componenten
    tr = np.maximum(np.maximum(tr1, tr2), tr3)

    # Bereken ATR met rollend gemiddelde
    atr = np.zeros_like(tr)
    for i in range(len(tr)):
        if i < period:
            atr[i] = np.mean(tr[0:i + 1]) if i > 0 else tr[0]
        else:
            atr[i] = np.mean(tr[i - period + 1:i + 1])

    return atr


def calculate_donchian_channel(df: pd.DataFrame, period: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Bereken Donchian Channel met gevectoriseerde operaties

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame met OHLC data
    period : int
        Lookback periode

    Returns:
    --------
    Tuple[np.ndarray, np.ndarray] : Upper en lower channel waarden
    """
    # Implementatie...
```

-----------

Path: src/utils/logger.py

```python
import csv
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional


class Logger:
    """Verbeterde klasse voor logging van trades en botactiviteit"""

    def __init__(self, log_file_path: str):
        """
        Initialiseer de logger.

        Parameters:
        -----------
        log_file_path : str
            Pad naar het logbestand.
        """
        self.log_file = log_file_path

        # Maak log directory indien nodig
        log_dir = os.path.dirname(log_file_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        self.setup_log_file()

        # Logging voor performance statistieken
        self.stats_file = os.path.join(os.path.dirname(log_file_path), 'performance_stats.json')
        self.initialize_stats()

    def setup_log_file(self):
        """Bereid logbestand voor als het nog niet bestaat."""
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    'Timestamp', 'Type', 'Symbol', 'Action',
                    'Price', 'Volume', 'StopLoss', 'TakeProfit',
                    'Comment', 'Leverage', 'TrendStrength', 'Balance'
                ])
                # Voeg initiële INFO regel toe
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                writer.writerow([
                    timestamp, 'INFO', '', '', '', '', '', '',
                    'Log gestart', '', '', ''
                ])

    def initialize_stats(self):
        """Initialiseer performance statistieken bestand als het nog niet bestaat."""
        if not os.path.exists(self.stats_file):
            default_stats = {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'break_even_trades': 0,
                'win_rate': 0.0,
                'avg_win': 0.0,
                'avg_loss': 0.0,
                'profit_factor': 0.0,
                'max_drawdown': 0.0,
                'net_profit': 0.0,
                'trades_by_symbol': {},
                'daily_performance': {},
                'trade_history': []
            }
            with open(self.stats_file, 'w') as file:
                json.dump(default_stats, file, indent=4)

    def log_trade(self, symbol: str, action: str, price: float, volume: float, sl: float, tp: float,
                  comment: str, leverage: Optional[float] = None, trend_strength: Optional[float] = None,
                  balance: Optional[float] = None):
        """
        Log een trade naar CSV met uitgebreide informatie.

        Parameters:
        -----------
        symbol : str
            Handelssymbool.
        action : str
            Trade actie (BUY, SELL, etc.).
        price : float
            Uitvoeringsprijs.
        volume : float
            Order volume.
        sl : float
            Stop Loss prijs.
        tp : float
            Take Profit prijs.
        comment : str
            Commentaar bij de trade.
        leverage : float, optional
            Gebruikte hefboom.
        trend_strength : float, optional
            Sterkte van de trend op moment van trade.
        balance : float, optional
            Account balans na trade.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp, 'TRADE', symbol, action,
                price, volume, sl, tp, comment,
                leverage if leverage is not None else '', trend_strength if trend_strength is not None else '',
                balance if balance is not None else ''
            ])

        # Log ook naar trade history voor performancetracking
        self.update_trade_stats(timestamp, symbol, action, price, volume, comment)

    def log_info(self, message: str, level: str = "INFO"):
        """
        Log een informatiebericht.

        Parameters:
        -----------
        message : str
            Het te loggen bericht.
        level : str, optional
            Logniveau (INFO, WARNING, ERROR, DEBUG).
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp, level, '', '', '', '', '', '',
                message, '', '', ''
            ])
        print(f"[{timestamp}] {level}: {message}")

    def log_status(self, account_info: Dict[str, Any], open_positions: Dict[str, Any]):
        """
        Log huidige account status.

        Parameters:
        -----------
        account_info : dict
            Informatie over de account.
        open_positions : dict
            Informatie over open posities.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        positions_count = sum(len(pos_list) for pos_list in open_positions.values()) if open_positions else 0
        positions_detail = ", ".join(
            f"{symbol}:{pos.volume}@{((pos.profit / account_info.get('balance', 100000)) * 100):.2f}%"
            for symbol, pos_list in open_positions.items()
            for pos in pos_list
        ) if positions_count > 0 else ""

        equity = account_info.get('equity', 0)
        balance = account_info.get('balance', 0)
        margin = account_info.get('margin', 0)
        margin_level = (equity / margin * 100) if margin > 0 else 0
        floating_pnl = equity - balance

        status_message = (
            f"Balance: {balance}, Equity: {equity}, Floating P/L: {floating_pnl:.2f}, "
            f"Margin Level: {margin_level:.2f}%, Open positions: {positions_count}"
        )
        if positions_detail:
            status_message += f" ({positions_detail})"

        with open(self.log_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp, 'STATUS', '', '', '', '', '', '',
                status_message, '', '', balance
            ])

    def update_trade_stats(self, timestamp: str, symbol: str, action: str, price: float, volume: float,
                           comment: str):
        """
        Update performance statistieken na een trade.

        Parameters:
        -----------
        timestamp : str
            Tijdstempel van de trade.
        symbol : str
            Handelssymbool.
        action : str
            Trade actie (BUY, SELL, etc.).
        price : float
            Uitvoeringsprijs.
        volume : float
            Order volume.
        comment : str
            Commentaar bij de trade.
        """
        try:
            if not os.path.exists(self.stats_file):
                self.initialize_stats()

            with open(self.stats_file, 'r') as file:
                stats = json.load(file)

            # Voeg trade toe aan geschiedenis
            trade_record = {
                'timestamp': timestamp,
                'symbol': symbol,
                'action': action,
                'price': price,
                'volume': volume,
                'comment': comment
            }
            stats['trade_history'].append(trade_record)

            # Bijhouden trades per symbool
            if symbol not in stats['trades_by_symbol']:
                stats['trades_by_symbol'][symbol] = {'total': 0, 'buys': 0, 'sells': 0}
            stats['trades_by_symbol'][symbol]['total'] += 1
            if action == 'BUY':
                stats['trades_by_symbol'][symbol]['buys'] += 1
            elif action == 'SELL':
                stats['trades_by_symbol'][symbol]['sells'] += 1

            # Update algemene statistieken
            stats['total_trades'] += 1

            # Sla bijgewerkte statistieken op
            with open(self.stats_file, 'w') as file:
                json.dump(stats, file, indent=4)
        except json.JSONDecodeError:
            self.initialize_stats()  # Herinitialiseer bij corrupte JSON
            self.log_info("Stats bestand herinitialiseerd vanwege corrupte data", level="WARNING")
        except Exception as e:
            self.log_info(f"Fout bij bijwerken statistieken: {e}", level="ERROR")

    def log_performance_metrics(self, metrics: Dict[str, Any]):
        """
        Log prestatiemetrieken.

        Parameters:
        -----------
        metrics : dict
            Dictionary met prestatiemetrieken.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        metrics_str = ", ".join(f"{k}: {v}" for k, v in metrics.items() if k != 'trade_history')

        try:
            with open(self.log_file, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([timestamp, 'METRICS', '', '', '', '', '', '', metrics_str, '', '', ''])

            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r') as file:
                    stats = json.load(file)
                for k, v in metrics.items():
                    if k in stats and k != 'trade_history':
                        stats[k] = v
                with open(self.stats_file, 'w') as file:
                    json.dump(stats, file, indent=4)
        except Exception as e:
            self.log_info(f"Fout bij loggen van metrics: {e}", level="ERROR")
```

-----------

Path: src/utils/visualizer.py

```python
import json
import os
from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


class Visualizer:
    """Verbeterde klasse voor visualisatie van trading resultaten"""

    def __init__(self, log_file, output_dir='data'):
        """
        Initialiseer de visualizer

        Parameters:
        -----------
        log_file : str
            Pad naar het logbestand
        output_dir : str, optional
            Map voor het opslaan van grafieken
        """
        self.log_file = log_file
        self.output_dir = output_dir

        # Stel visualisatiestijl in
        plt.style.use('ggplot')
        plt.rcParams['figure.figsize'] = (16, 10)
        plt.rcParams['lines.linewidth'] = 1.5
        sns.set_style("whitegrid")

        # Maak output map aan als deze niet bestaat
        os.makedirs(output_dir, exist_ok=True)

        # Pad naar presentation stats file
        log_dir = os.path.dirname(log_file)
        self.stats_file = os.path.join(log_dir, 'performance_stats.json')

    def load_trade_data(self):
        """
        Laad trade data uit het logbestand

        Returns:
        --------
        pandas.DataFrame
            DataFrame met trade data
        """
        try:
            df = pd.read_csv(self.log_file)
            # Converteer timestamp naar datetime
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            return df
        except Exception as e:
            print(f"Fout bij laden van trade data: {e}")
            return pd.DataFrame()

    def load_performance_stats(self):
        """
        Laad presentation statistieken uit JSON bestand

        Returns:
        --------
        dict
            Dictionary met performancestatistieken
        """
        if not os.path.exists(self.stats_file):
            print(f"Performance stats bestand niet gevonden: {self.stats_file}")
            return {}

        try:
            with open(self.stats_file, 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f"Fout bij laden van presentation stats: {e}")
            return {}

    def plot_equity_curve(self, include_drawdown=True):
        """
        Plot de equity curve met uitgebreide metrics

        Parameters:
        -----------
        include_drawdown : bool, optional
            Of drawdown analyse moet worden toegevoegd

        Returns:
        --------
        str
            Pad naar de opgeslagen grafiek
        """
        df = self.load_trade_data()
        if df.empty:
            print("Geen data beschikbaar voor equity curve")
            return None

        # Filter alleen op STATUS rijen
        status_df = df[df['Type'] == 'STATUS'].copy()
        if status_df.empty:
            print("Geen status data beschikbaar voor equity curve")
            return None

        # Extraheer balance en equity uit Comment kolom
        balances = []
        equities = []
        timestamps = []

        for _, row in status_df.iterrows():
            comment = row['Comment']
            timestamp = row['Timestamp']
            balance = row.get('Balance', None)

            # Probeer eerst uit de Balance kolom te halen
            if pd.notna(balance) and balance != '':
                balances.append(float(balance))
                timestamps.append(timestamp)
            else:
                # Als dat niet lukt, probeer uit de Comment te extraheren
                balance_str = comment.split('Balance: ')[1].split(',')[0] if 'Balance: ' in comment else None
                if balance_str and balance_str != 'N/A':
                    balances.append(float(balance_str))
                    timestamps.append(timestamp)

            # Extraheer equity uit comment
            equity_str = comment.split('Equity: ')[1].split(',')[0] if 'Equity: ' in comment else None
            if equity_str and equity_str != 'N/A':
                equities.append(float(equity_str))

        if not balances:
            print("Geen balance data gevonden voor equity curve")
            return None

        # Maak dataframe voor analyse
        equity_df = pd.DataFrame({
            'timestamp': timestamps,
            'balance': balances
        })

        if len(equities) == len(balances):
            equity_df['equity'] = equities

        # Bereken drawdown als die er is
        if 'equity' in equity_df.columns:
            equity_df['peak'] = equity_df['equity'].cummax()
            equity_df['drawdown'] = (equity_df['equity'] - equity_df['peak']) / equity_df['peak'] * 100
        else:
            equity_df['peak'] = equity_df['balance'].cummax()
            equity_df['drawdown'] = (equity_df['balance'] - equity_df['peak']) / equity_df['peak'] * 100

        # Bereken prestatie-metrieken
        initial_balance = equity_df['balance'].iloc[0] if not equity_df.empty else 100000
        final_balance = equity_df['balance'].iloc[-1] if not equity_df.empty else initial_balance
        total_return = ((final_balance / initial_balance) - 1) * 100
        max_drawdown = equity_df['drawdown'].min() if 'drawdown' in equity_df.columns else 0

        # Maak equity curve plot
        fig, axes = plt.subplots(2, 1, figsize=(16, 12), gridspec_kw={'height_ratios': [3, 1]})

        # Bovenste plot: Equity curve
        if 'equity' in equity_df.columns:
            axes[0].plot(equity_df['timestamp'], equity_df['equity'], label='Equity', color='blue', linewidth=2)

        axes[0].plot(equity_df['timestamp'], equity_df['balance'], label='Balance', color='green', linewidth=2)
        axes[0].plot(equity_df['timestamp'], equity_df['peak'], label='Peak Balance', color='darkgreen', linestyle='--',
                     alpha=0.6)

        # Voeg horizontale lijn toe voor beginbalans
        axes[0].axhline(y=initial_balance, color='gray', linestyle=':', alpha=0.8, label='Initial Balance')

        # Voeg horizontale lijnen toe voor 5% en 10% winst
        axes[0].axhline(y=initial_balance * 1.05, color='orange', linestyle=':', alpha=0.8, label='5% Profit')
        axes[0].axhline(y=initial_balance * 1.10, color='darkgreen', linestyle=':', alpha=0.8,
                        label='10% Profit (Target)')

        # Voeg horizontale lijnen toe voor FTMO limieten
        axes[0].axhline(y=initial_balance * 0.95, color='yellow', linestyle=':', alpha=0.8,
                        label='5% Loss (Daily Limit)')
        axes[0].axhline(y=initial_balance * 0.90, color='red', linestyle=':', alpha=0.8,
                        label='10% Loss (Max Drawdown)')

        # Voeg trade markers toe (optioneel)
        trade_df = df[df['Type'] == 'TRADE']
        if not trade_df.empty:
            buy_df = trade_df[trade_df['Action'] == 'BUY']
            sell_df = trade_df[trade_df['Action'] == 'SELL']

            if not buy_df.empty:
                axes[0].scatter(buy_df['Timestamp'], [initial_balance] * len(buy_df), marker='^', color='green',
                                s=80, label='Buy', alpha=0.7)
            if not sell_df.empty:
                axes[0].scatter(sell_df['Timestamp'], [initial_balance] * len(sell_df), marker='v', color='red',
                                s=80, label='Sell', alpha=0.7)

        # Formateer bovenste plot
        axes[0].set_title('Equity Curve & Balance History', fontsize=16)
        axes[0].set_ylabel('Account Value ($)', fontsize=14)
        axes[0].legend(loc='upper left', fontsize=12)
        axes[0].grid(True)

        # Voeg metrics toe aan de plot
        info_text = (
            f"Initial Balance: ${initial_balance:,.2f}\n"
            f"Final Balance: ${final_balance:,.2f}\n"
            f"Total Return: {total_return:.2f}%\n"
            f"Max Drawdown: {max_drawdown:.2f}%"
        )

        # Plaats info tekst in de rechterbovenhoek
        axes[0].text(0.02, 0.02, info_text, transform=axes[0].transAxes, fontsize=12,
                     bbox=dict(facecolor='white', alpha=0.7), verticalalignment='bottom')

        # Onderste plot: Drawdown
        axes[1].fill_between(equity_df['timestamp'], equity_df['drawdown'], 0,
                             color='red', alpha=0.3, label='Drawdown')
        axes[1].plot(equity_df['timestamp'], equity_df['drawdown'], color='red', linewidth=1)

        # Voeg horizontale lijnen toe voor drawdown limieten
        axes[1].axhline(y=-5, color='yellow', linestyle=':', alpha=0.8, label='5% Drawdown (Daily Limit)')
        axes[1].axhline(y=-10, color='red', linestyle=':', alpha=0.8, label='10% Drawdown (Max Limit)')

        # Formateer onderste plot
        axes[1].set_title('Drawdown (%)', fontsize=14)
        axes[1].set_xlabel('Datum', fontsize=14)
        axes[1].set_ylabel('Drawdown (%)', fontsize=14)
        axes[1].legend(loc='lower left', fontsize=12)
        axes[1].set_ylim(min(equity_df['drawdown'].min() * 1.2, -12), 1)  # Zorg voor goede y-as limieten
        axes[1].grid(True)

        # Formateer x-as voor beide plots
        for ax in axes:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax.xaxis.set_major_locator(mdates.AutoDateLocator())
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

        plt.tight_layout()

        # Sla grafiek op
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"equity_curve_{timestamp}.png")
        plt.savefig(output_path, dpi=150)
        plt.close()

        print(f"Equity curve opgeslagen als {output_path}")
        return output_path

    def plot_trade_results(self):
        """
        Plot de resultaten van trades

        Returns:
        --------
        str
            Pad naar de opgeslagen grafiek
        """
        df = self.load_trade_data()
        if df.empty:
            print("Geen data beschikbaar voor trade resultaten")
            return None

        # Filter alleen op TRADE rijen
        trade_df = df[df['Type'] == 'TRADE']
        if trade_df.empty:
            print("Geen trade data beschikbaar")
            return None

        # Groepeer trades per symbool
        symbols = trade_df['Symbol'].unique()

        # Bereken aantal figuren nodig (1 rij per symbool)
        num_symbols = len(symbols)

        # Maak plot voor elk symbool
        fig, axes = plt.subplots(num_symbols, 1, figsize=(16, 6 * num_symbols), squeeze=False)

        for i, symbol in enumerate(symbols):
            symbol_df = trade_df[trade_df['Symbol'] == symbol]

            # Converteer kolommen naar numeriek waar nodig
            for col in ['Price', 'Volume', 'StopLoss', 'TakeProfit', 'Leverage', 'TrendStrength']:
                if col in symbol_df.columns:
                    symbol_df[col] = pd.to_numeric(symbol_df[col], errors='coerce')

            # Filter buys en sells
            buys = symbol_df[symbol_df['Action'] == 'BUY']
            sells = symbol_df[symbol_df['Action'] == 'SELL']

            ax = axes[i, 0]

            # Plot trades
            if not buys.empty:
                ax.scatter(buys['Timestamp'], buys['Price'], color='green', marker='^', s=100, label='Buy')

                # Maak grootte van markers proportioneel aan volume
                if 'Volume' in buys.columns:
                    sizes = buys['Volume'] * 50 + 50  # Schaal volume voor marker grootte
                    ax.scatter(buys['Timestamp'], buys['Price'], s=sizes, color='green', marker='^', alpha=0.5)

                # Plot stop losses voor buy orders
                for _, row in buys.iterrows():
                    if pd.notna(row.get('StopLoss', None)) and row['StopLoss'] > 0:
                        ax.plot([row['Timestamp'], row['Timestamp']],
                                [row['Price'], row['StopLoss']],
                                'r--', alpha=0.5)

            if not sells.empty:
                ax.scatter(sells['Timestamp'], sells['Price'], color='red', marker='v', s=100, label='Sell')

                # Maak grootte van markers proportioneel aan volume
                if 'Volume' in sells.columns:
                    sizes = sells['Volume'] * 50 + 50
                    ax.scatter(sells['Timestamp'], sells['Price'], s=sizes, color='red', marker='v', alpha=0.5)

            # Bereken en toon winst/verlies per trade als mogelijk
            paired_trades = self._pair_trades(symbol_df)
            for pair in paired_trades:
                if len(pair) == 2:  # Alleen complete trade paren
                    buy = pair[0]
                    sell = pair[1]
                    profit_pct = ((sell['Price'] - buy['Price']) / buy['Price']) * 100

                    # Toon label voor het resultaat
                    mid_time = buy['Timestamp'] + (sell['Timestamp'] - buy['Timestamp']) / 2
                    mid_price = (buy['Price'] + sell['Price']) / 2

                    color = 'green' if profit_pct > 0 else 'red'
                    ax.text(mid_time, mid_price, f"{profit_pct:.1f}%",
                            color=color, fontweight='bold', ha='center')

                    # Verbind buy en sell punt met lijn
                    ax.plot([buy['Timestamp'], sell['Timestamp']],
                            [buy['Price'], sell['Price']],
                            color=color, linestyle='-', alpha=0.5)

            # Formateer plot
            ax.set_title(f'Trades voor {symbol}', fontsize=16)
            ax.set_ylabel('Prijs', fontsize=14)

            # Voeg gridlines toe
            ax.grid(True)
            ax.legend(loc='upper left', fontsize=12)

            # Voeg labels toe voor buy/sell punten
            for idx, row in buys.iterrows():
                volume_str = f"{row['Volume']}" if 'Volume' in row else ""
                ax.annotate(volume_str,
                            xy=(row['Timestamp'], row['Price']),
                            xytext=(5, 5), textcoords='offset points',
                            fontsize=9, color='darkgreen')

            for idx, row in sells.iterrows():
                volume_str = f"{row['Volume']}" if 'Volume' in row else ""
                ax.annotate(volume_str,
                            xy=(row['Timestamp'], row['Price']),
                            xytext=(5, -15), textcoords='offset points',
                            fontsize=9, color='darkred')

            # Formateer x-as
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
            ax.xaxis.set_major_locator(mdates.AutoDateLocator())
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

        plt.xlabel('Tijd', fontsize=14)
        plt.tight_layout()

        # Sla grafiek op
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"trade_results_{timestamp}.png")
        plt.savefig(output_path, dpi=150)
        plt.close()

        print(f"Trade resultaten opgeslagen als {output_path}")
        return output_path

    def _pair_trades(self, trade_df):
        """
        Groepeer trades in buy/sell paren

        Parameters:
        -----------
        trade_df : pandas.DataFrame
            DataFrame met trades voor één symbool

        Returns:
        --------
        list
            Lijst met paren van trades (buy/sell)
        """
        # Sorteer trades op tijdstempel
        sorted_trades = trade_df.sort_values('Timestamp').to_dict('records')

        # Verzamel paren
        pairs = []
        current_pair = []

        for trade in sorted_trades:
            if trade['Action'] == 'BUY':
                # Als we al een open pair hebben, sluit deze eerst af
                if current_pair:
                    pairs.append(current_pair)
                    current_pair = [trade]
                else:
                    current_pair = [trade]
            elif trade['Action'] == 'SELL' and current_pair:
                current_pair.append(trade)
                pairs.append(current_pair)
                current_pair = []

        # Voeg laatste onvolledige paar toe indien aanwezig
        if current_pair:
            pairs.append(current_pair)

        return pairs

    def plot_performance_summary(self):
        """
        Plot een samenvatting van de handelsperformance

        Returns:
        --------
        str
            Pad naar de opgeslagen grafiek
        """
        # Laad trade data
        df = self.load_trade_data()
        stats = self.load_performance_stats()

        if df.empty:
            print("Geen data beschikbaar voor presentation summary")
            return None

        # Filter trades
        trade_df = df[df['Type'] == 'TRADE'].copy()

        if trade_df.empty:
            print("Geen trade data beschikbaar voor analyse")
            return None

        # Converteer numerieke kolommen
        for col in ['Price', 'Volume', 'StopLoss', 'TakeProfit']:
            if col in trade_df.columns:
                trade_df[col] = pd.to_numeric(trade_df[col], errors='coerce')

        # Bereken metrics
        trades_by_symbol = {}
        symbol_performance = {}

        for symbol in trade_df['Symbol'].unique():
            symbol_df = trade_df[trade_df['Symbol'] == symbol]

            # Basic count metrics
            buys = symbol_df[symbol_df['Action'] == 'BUY']
            sells = symbol_df[symbol_df['Action'] == 'SELL']

            trades_by_symbol[symbol] = {
                'buys': len(buys),
                'sells': len(sells),
                'total': len(symbol_df)
            }

            # Bereken presentation als mogelijk
            pairs = self._pair_trades(symbol_df)
            wins = 0
            losses = 0
            total_profit_pct = 0
            total_loss_pct = 0

            for pair in pairs:
                if len(pair) == 2:  # Alleen complete trades
                    buy = pair[0]
                    sell = pair[1]

                    profit_pct = ((sell['Price'] - buy['Price']) / buy['Price']) * 100

                    if profit_pct > 0:
                        wins += 1
                        total_profit_pct += profit_pct
                    else:
                        losses += 1
                        total_loss_pct += profit_pct

            total_complete_trades = wins + losses
            win_rate = wins / total_complete_trades if total_complete_trades > 0 else 0
            avg_win = total_profit_pct / wins if wins > 0 else 0
            avg_loss = total_loss_pct / losses if losses > 0 else 0
            profit_factor = abs(total_profit_pct / total_loss_pct) if total_loss_pct < 0 else float('inf')

            symbol_performance[symbol] = {
                'win_rate': win_rate,
                'wins': wins,
                'losses': losses,
                'avg_win': avg_win,
                'avg_loss': avg_loss,
                'profit_factor': profit_factor,
                'net_profit_pct': total_profit_pct + total_loss_pct
            }

        # Maak plot
        fig = plt.figure(figsize=(20, 16))

        # Definieer grid layout
        gs = fig.add_gridspec(3, 2, height_ratios=[1, 1, 1])

        # 1. Win/Loss Ratio per Symbol (Pie chart)
        ax1 = fig.add_subplot(gs[0, 0])

        symbols = list(symbol_performance.keys())
        win_rates = [symbol_performance[s]['win_rate'] * 100 for s in symbols]

        # Kleuren gebaseerd op win rate (rood naar groen)
        colors = [(1 - wr / 100, wr / 100, 0) for wr in win_rates]

        ax1.bar(symbols, win_rates, color=colors)
        ax1.set_title('Win Rate per Symbol (%)', fontsize=14)
        ax1.set_ylim(0, 100)
        ax1.grid(axis='y')

        # Voeg datawaarden toe aan bars
        for i, v in enumerate(win_rates):
            ax1.text(i, v + 1, f"{v:.1f}%", ha='center', fontsize=12)

        # 2. Average Win vs Loss per Symbol
        ax2 = fig.add_subplot(gs[0, 1])

        # Verzamel data
        symbols = list(symbol_performance.keys())
        avg_wins = [symbol_performance[s]['avg_win'] for s in symbols]
        avg_losses = [abs(symbol_performance[s]['avg_loss']) for s in symbols]

        x = np.arange(len(symbols))
        width = 0.35

        ax2.bar(x - width / 2, avg_wins, width, label='Avg Win %', color='green', alpha=0.7)
        ax2.bar(x + width / 2, avg_losses, width, label='Avg Loss %', color='red', alpha=0.7)

        ax2.set_title('Average Win vs Loss (%)', fontsize=14)
        ax2.set_xticks(x)
        ax2.set_xticklabels(symbols)
        ax2.legend()
        ax2.grid(axis='y')

        # 3. Net Profit per Symbol
        ax3 = fig.add_subplot(gs[1, 0])

        net_profits = [symbol_performance[s]['net_profit_pct'] for s in symbols]
        colors = ['green' if p > 0 else 'red' for p in net_profits]

        ax3.bar(symbols, net_profits, color=colors, alpha=0.7)
        ax3.set_title('Net Profit per Symbol (%)', fontsize=14)
        ax3.grid(axis='y')

        # Voeg datawaarden toe
        for i, v in enumerate(net_profits):
            ax3.text(i, v + (0.1 if v >= 0 else -2), f"{v:.1f}%", ha='center', fontsize=12)

        # 4. Trades per Symbol
        ax4 = fig.add_subplot(gs[1, 1])

        # Verzamel data
        buys_per_symbol = [trades_by_symbol[s]['buys'] for s in symbols]
        sells_per_symbol = [trades_by_symbol[s]['sells'] for s in symbols]

        ax4.bar(x - width / 2, buys_per_symbol, width, label='Buy Orders', color='green', alpha=0.7)
        ax4.bar(x + width / 2, sells_per_symbol, width, label='Sell Orders', color='red', alpha=0.7)

        ax4.set_title('Number of Trades per Symbol', fontsize=14)
        ax4.set_xticks(x)
        ax4.set_xticklabels(symbols)
        ax4.legend()
        ax4.grid(axis='y')

        # 5. Overall Performance Metrics Table
        ax5 = fig.add_subplot(gs[2, :])
        ax5.axis('off')

        # Bereken totalen over alle symbolen
        total_trades = sum(trades_by_symbol[s]['total'] for s in symbols)
        total_wins = sum(symbol_performance[s]['wins'] for s in symbols)
        total_losses = sum(symbol_performance[s]['losses'] for s in symbols)

        total_win_rate = total_wins / (total_wins + total_losses) * 100 if (total_wins + total_losses) > 0 else 0
        total_profit = sum(symbol_performance[s]['net_profit_pct'] for s in symbols)

        # Custom tabel
        overall_metrics = [
            ('Total Trades', f"{total_trades}"),
            ('Win Rate', f"{total_win_rate:.1f}%"),
            ('Winning Trades', f"{total_wins}"),
            ('Losing Trades', f"{total_losses}"),
            ('Net Profit %', f"{total_profit:.2f}%"),
        ]

        table_data = []
        for metric, value in overall_metrics:
            table_data.append([metric, value])

        tbl = ax5.table(
            cellText=table_data,
            colLabels=['Metric', 'Value'],
            loc='center',
            cellLoc='center',
            colWidths=[0.3, 0.3]
        )

        tbl.auto_set_font_size(False)
        tbl.set_fontsize(14)
        tbl.scale(1, 2)

        # Stel kleuren in
        header_color = '#40466e'
        cell_color = '#f1f1f2'

        for i, key in enumerate(tbl.get_celld().keys()):
            cell = tbl.get_celld()[key]
            if i == 0:  # Header row
                cell.set_facecolor(header_color)
                cell.set_text_props(color='white', fontweight='bold')
            else:
                cell.set_facecolor(cell_color)

        ax5.set_title('Overall Performance Metrics', fontsize=16, pad=20)

        plt.tight_layout()

        # Sla grafiek op
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"performance_summary_{timestamp}.png")
        plt.savefig(output_path, dpi=150)
        plt.close()

        print(f"Performance samenvatting opgeslagen als {output_path}")
        return output_path
```

-----------

Path: tests/fixtures/__init__.py

```python
```

-----------

Path: tests/integration/test_mt5_connectivity.py

```python
# tests/integration/test_mt5_connectivity.py
from datetime import datetime, timedelta

import pytest
from turtle_trader.data.mt5_connector import MT5Connector
from turtle_trader.utils.config import load_config


@pytest.fixture
def mt5_connector():
    """Create a connector instance with test configuration"""
    config = load_config("tests/config/test_config.json")
    from turtle_trader.utils.logger import Logger
    logger = Logger("tests/logs/test_log.csv")
    return MT5Connector(config['mt5'], logger)


def test_mt5_connection(mt5_connector):
    """Test connection to MT5 platform"""
    # Connect to MT5
    connected = mt5_connector.connect()
    assert connected, "Failed to connect to MT5"

    # Clean up
    mt5_connector.disconnect()


def test_historical_data_retrieval(mt5_connector):
    """Test retrieving historical data from MT5"""
    # Connect to MT5
    connected = mt5_connector.connect()
    assert connected, "Failed to connect to MT5"

    # Get historical data
    symbol = "EURUSD"
    end_date = datetime.now()
    start_date = end_date - timedelta(days=5)

    df = mt5_connector.get_historical_data(symbol, 16, 100)  # 16 = H4 timeframe

    # Validate data
    assert not df.empty, "No historical data retrieved"
    assert 'open' in df.columns, "Data missing expected columns"
    assert 'high' in df.columns, "Data missing expected columns"
    assert 'low' in df.columns, "Data missing expected columns"
    assert 'close' in df.columns, "Data missing expected columns"

    # Clean up
    mt5_connector.disconnect()
```

-----------

Path: tests/performance/__init__.py

```python
```

-----------

Path: tests/unit/__init__.py

```python
```

-----------

Path: tests/unit/test_risk_manager.py

```python
# tests/unit/test_risk_manager.py
import os
import sys
import unittest
from unittest.mock import MagicMock

# Voeg project root toe aan sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.risk.risk_manager import RiskManager


class TestRiskManager(unittest.TestCase):
    def setUp(self):
        # Maak een mock logger
        self.logger = MagicMock()
        self.logger.log_info = MagicMock()

        # Standaard configuratie
        self.config = {
            'max_risk_per_trade': 0.01,
            'max_daily_drawdown': 0.05,
            'max_total_drawdown': 0.10,
            'leverage': 30,
            'account_balance': 100000
        }

        # Initialiseer risk manager
        self.risk_manager = RiskManager(self.config, self.logger)

    def test_check_ftmo_limits_profit_target(self):
        # Test dat winstdoel correct wordt gedetecteerd
        account_info = {
            'balance': 110000,  # 10% winst
            'equity': 110000
        }

        should_stop, reason = self.risk_manager.check_ftmo_limits(account_info)

        self.assertTrue(should_stop)
        self.assertIn("Winstdoel bereikt", reason)

    def test_check_ftmo_limits_daily_drawdown(self):
        # Test dat dagelijkse drawdown limiet correct wordt gedetecteerd
        account_info = {
            'balance': 95000,  # 5% verlies
            'equity': 95000
        }

        should_stop, reason = self.risk_manager.check_ftmo_limits(account_info)

        self.assertTrue(should_stop)
        self.assertIn("Dagelijkse verlieslimiet bereikt", reason)

    def test_check_ftmo_limits_total_drawdown(self):
        # Test dat totale drawdown limiet correct wordt gedetecteerd
        account_info = {
            'balance': 90000,  # 10% verlies
            'equity': 90000
        }

        should_stop, reason = self.risk_manager.check_ftmo_limits(account_info)

        self.assertTrue(should_stop)
        self.assertIn("Maximale drawdown bereikt", reason)

    def test_check_ftmo_limits_no_violations(self):
        # Test dat geen limieten worden geschonden
        account_info = {
            'balance': 105000,  # 5% winst
            'equity': 105000
        }

        should_stop, reason = self.risk_manager.check_ftmo_limits(account_info)

        self.assertFalse(should_stop)
        self.assertIsNone(reason)

    def test_calculate_position_size(self):
        # Test positiegrootte berekening
        entry_price = 1.2000
        stop_loss = 1.1950  # 50 pips
        account_balance = 100000
        trend_strength = 0.8

        position_size = self.risk_manager.calculate_position_size(
            symbol="EURUSD",
            entry_price=entry_price,
            stop_loss=stop_loss,
            account_balance=account_balance,
            trend_strength=trend_strength
        )

        # Handmatige berekening voor vergelijking:
        # risk_amount = 100000 * 0.01 = 1000
        # adjusted_risk = 1000 * (0.5 + 0.8/2) = 1000 * 0.9 = 900
        # pips_at_risk = (1.2000 - 1.1950) / 0.0001 = 50
        # pip_value = 10 (standaard voor 1 lot)
        # lot_size = 900 / (50 * 10) = 1.8

        # We verwachten dat de waarde dichtbij 1.8 ligt (kan afwijken door afrondingen)
        self.assertGreater(position_size, 1.5)
        self.assertLessEqual(position_size, 2.0)

    def test_check_trade_risk(self):
        # Test trade risico validatie
        symbol = "EURUSD"
        volume = 0.5
        entry_price = 1.2000
        stop_loss = 1.1950

        # Reset dagelijkse limieten
        self.risk_manager.daily_trades_count = 0

        result = self.risk_manager.check_trade_risk(symbol, volume, entry_price, stop_loss)

        # We verwachten dat de trade wordt goedgekeurd
        self.assertTrue(result)

        # Test trade limiet per dag
        self.risk_manager.daily_trades_count = self.risk_manager.max_daily_trades

        result = self.risk_manager.check_trade_risk(symbol, volume, entry_price, stop_loss)

        # We verwachten dat de trade wordt afgewezen
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
```

-----------

Path: tests/unit/test_turtle_strategy.py

```python
# tests/unit/test_turtle_strategy.py
import os
import sys
import unittest
from unittest.mock import MagicMock

import numpy as np
import pandas as pd

# Voeg project root toe aan sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.strategy.turtle_strategy import TurtleStrategy


class TestTurtleStrategy(unittest.TestCase):
    def setUp(self):
        # Maak mock objecten
        self.connector = MagicMock()
        self.risk_manager = MagicMock()
        self.logger = MagicMock()

        # Standaard configuratie
        self.config = {
            'mt5': {
                'symbols': ['EURUSD', 'GBPUSD'],
                'timeframe': 'H4',
                'account_balance': 100000
            },
            'strategy': {
                'name': 'turtle',
                'swing_mode': False,
                'entry_period': 20,
                'exit_period': 10,
                'atr_period': 20,
                'atr_multiplier': 2.0
            }
        }

        # Initialiseer strategie
        self.strategy = TurtleStrategy(self.connector, self.risk_manager, self.logger, self.config)

    def test_initialization(self):
        # Test dat de strategie correct wordt geïnitialiseerd
        self.assertEqual(self.strategy.name, "Turtle Trading Strategy")
        self.assertEqual(self.strategy.entry_period, 20)
        self.assertEqual(self.strategy.exit_period, 10)
        self.assertEqual(self.strategy.atr_period, 20)
        self.assertEqual(self.strategy.atr_multiplier, 2.0)
        self.assertFalse(self.strategy.swing_mode)

    def test_swing_mode_initialization(self):
        # Test swing mode initialisatie
        config = self.config.copy()
        config['strategy']['swing_mode'] = True

        strategy = TurtleStrategy(self.connector, self.risk_manager, self.logger, config)

        self.assertTrue(strategy.swing_mode)
        self.assertEqual(strategy.entry_period, 40)  # Standaard voor swing mode

    def test_calculate_indicators(self):
        # Maak test data
        dates = pd.date_range(start='2023-01-01', periods=100, freq='4H')
        high = np.random.normal(1.2, 0.01, 100)
        low = high - np.random.uniform(0.001, 0.005, 100)
        close = low + np.random.uniform(0, 0.003, 100)
        open_prices = high - np.random.uniform(0, 0.003, 100)
        volume = np.random.randint(10, 100, 100)

        df = pd.DataFrame({
            'date': dates,
            'open': open_prices,
            'high': high,
            'low': low,
            'close': close,
            'tick_volume': volume
        })

        # Bereken indicatoren
        indicators = self.strategy.calculate_indicators(df)

        # Test dat de belangrijkste indicatoren aanwezig zijn
        self.assertIn('atr', indicators)
        self.assertIn('high_entry', indicators)
        self.assertIn('low_exit', indicators)

    def test_calculate_atr(self):
        # Maak test data
        dates = pd.date_range(start='2023-01-01', periods=50, freq='4H')
        high = np.random.normal(1.2, 0.01, 50)
        low = high - np.random.uniform(0.001, 0.005, 50)
        close = low + np.random.uniform(0, 0.003, 50)

        df = pd.DataFrame({
            'date': dates,
            'high': high,
            'low': low,
            'close': close
        })

        # Bereken ATR
        atr = self.strategy.calculate_atr(df, 14)

        # Test eigenschappen
        self.assertEqual(len(atr), 50)
        self.assertTrue(atr.iloc[-1] > 0)

    def test_process_symbol_no_data(self):
        # Test gedrag wanneer er geen data is
        self.connector.get_historical_data.return_value = pd.DataFrame()

        result = self.strategy.process_symbol('EURUSD')

        # Test dat er geen signaal is
        self.assertIsNone(result.get('signal'))
        self.logger.log_info.assert_called_with("Geen historische data beschikbaar voor EURUSD")

    def test_process_symbol_with_breakout(self):
        # Configureer mocks voor een breakout scenario
        # 1. Maak test data
        dates = pd.date_range(start='2023-01-01', periods=100, freq='4H')
        high = np.random.normal(1.2, 0.01, 100)
        low = high - np.random.uniform(0.001, 0.005, 100)
        close = low + np.random.uniform(0, 0.003, 100)
        open_prices = high - np.random.uniform(0, 0.003, 100)
        volume = np.random.randint(10, 100, 100)

        df = pd.DataFrame({
            'date': dates,
            'open': open_prices,
            'high': high,
            'low': low,
            'close': close,
            'tick_volume': volume
        })

        # Zorg dat laatste candle een breakout is
        df['high'].iloc[-1] = 1.25  # Hogere high voor breakout

        self.connector.get_historical_data.return_value = df

        # 2. Configureer tick
        tick = MagicMock()
        tick.ask = 1.25
        tick.bid = 1.248
        self.connector.get_symbol_tick.return_value = tick

        # 3. Configureer risicomanager
        self.risk_manager.can_trade.return_value = True
        self.risk_manager.calculate_position_size.return_value = 0.5
        self.risk_manager.check_trade_risk.return_value = True

        # 4. Configureer account info
        account_info = {'balance': 100000, 'equity': 100000}
        self.connector.get_account_info.return_value = account_info

        # 5. Configureer order response
        self.connector.place_order.return_value = 12345  # ticket ID

        # Test de processsymbol functie met de ingerichte mocks
        result = self.strategy.process_symbol('EURUSD')

        # Verwacht een entry signaal
        self.assertEqual(result.get('signal'), 'ENTRY')
        self.assertEqual(result.get('action'), 'BUY')
        self.assertEqual(result.get('ticket'), 12345)

        # Controleer dat de place_order functie werd aangeroepen
        self.connector.place_order.assert_called_once()


if __name__ == '__main__':
    unittest.main()
```

-----------

```

-----------

Path: Sophy_temp/.github/workflows/ci.yml

```yaml
# .github/workflows/ci.yml
name: TurtleTrader CI

on:
  push:
    branches: [ main, development ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
          pip install pytest pytest-cov
      - name: Run tests
        run: |
          pytest --cov=src tests/```

-----------

Path: Sophy_temp/config/settings.json

```json
// config/settings.json
{
  "mt5": {
    "login": 1520533067,
    "password": "YOUR_PASSWORD",
    "server": "FTMO-Demo2",
    "mt5_pathway": "C:\\Program Files\\FTMO MetaTrader 5\\terminal64.exe",
    "symbols": [
      "EURUSD",
      "XAUUSD",
      "US30"
    ],
    "symbol_mapping": {
      "US30": "US30.cash"
    },
    "timeframe": "H4",
    "account_balance": 100000
  },
  "risk": {
    "max_risk_per_trade": 0.015,
    "max_daily_drawdown": 0.05,
    "max_total_drawdown": 0.10,
    "leverage": 30
  },
  "strategy": {
    "name": "turtle_trader",
    "swing_mode": true,
    "entry_period": 40,
    "exit_period": 20,
    "atr_period": 20,
    "atr_multiplier": 2.5
  },
  "logging": {
    "log_file": "logs/trading_log.csv",
    "log_level": "INFO"
  },
  "output": {
    "data_dir": "data"
  }
}```

-----------

Path: Sophy_temp/config/strategy_config.json

```json
# config/strategy_config.json
{
"turtle_trader": {
"entry_period": 40,
"exit_period": 20,
"atr_period": 20,
"atr_multiplier": 2.5,
"swing_mode": true,
"use_trend_filter": true
}
}```

-----------

Path: Sophy_temp/docs/FTMO_Rules.txt

```plaintext
1/15
FTMO GENERAL TERMS AND CONDITIONS
These FTMO General Terms and Conditions (the “GTC”) govern rights and obligations in connection
with the use of services provided by FTMO Evaluation Global s.r.o. (the “Services”), offered mainly
through the www.ftmo.com website (the “Website”). Please read these GTC carefully. You are
under no obligation to use the Services if you do not agree or understand any portion of these Terms,
nor should you use the Services unless you understand and agree to these Terms.
1. INTRODUCTORY PROVISIONS
1.1. These GTC govern your (“you”, “your”, or the “Customer”) rights and obligations in
connection with the use of the Services provided by FTMO Evaluation Global s.r.o., with
its registered office at Purkyňova 2121/3, Nové Město, 110 00 Prague 1, Czech Republic,
identification no.: 092 13 651, registered in the Commercial Register maintained
by the Municipal Court in Prague, file no. C 332660 (“we”, “our”, or the “Provider”).
1.2. By registering on the Website or, where registration is not required, not later than by your
first use of the Services, you are entering into a contract with the Provider, the subject of
which is the provision of the Services of your choice. The GTC form an integral part of
such a contract and, by executing the contract with the Provider, you express your
agreement to these GTC.
1.3. The Services are only intended for persons over the age of 18 residing in the country
for which the Services are available. By registering on the Website, you confirm that you
are over 18 years of age. If you are under 18 years of age, you may not use the Services.
You undertake to access the Services solely from one of the countries for which
the Services are available. You acknowledge that your access to and use of the Services
may be restricted or prohibited by law in some countries, and you undertake to only access
and use the Services in accordance with applicable laws.
1.4. The Provider shall not provide Services to Customer that: (i) is of nationality or is residing
in Restricted Jurisdictions; (ii) is established or incorporated, or has a registered office in
Restricted Jurisdictions; (iii) is subject to the relevant international sanctions; or (iv) has
a criminal record related to financial crime or terrorism. Restricted Jurisdictions means
countries determined as such by the Provider and published here on the Website. The
Provider reserves the right to refuse, restrict or terminate the provision of any Services to
Customer as per this Clause 1.4. and such Customer is prohibited to use the Services,
which also includes the use of the Client Section and/or Trading Platform.
1.5. The Services consist of the provision of tools for simulated foreign exchange trading
on the FOREX market or simulated trading with other instruments on other financial
markets, provision of analytical tools, training and educational materials, the access to
the Client Section, and other ancillary services, in particular through the Client Section or
by the provision of access to applications provided by the Provider or third parties.
Financial market information is used in the simulated trading; however, you acknowledge
that any trading that you perform through the Services is not real. You also acknowledge
that the funds provided to you for demo trading are fictitious and that you have no right
to possess those fictitious funds beyond the scope of their use within the Services, and in
particular that they may not be used for any actual trading and that you are not entitled
to the payment of those funds. Unless expressly agreed otherwise, you will not be paid
any remuneration or profits based on the results of your simulated trading, nor will you
be required to pay any losses.
1.6. NONE OF THE SERVICES PROVIDED TO YOU BY THE PROVIDER CAN BE CONSIDERED
INVESTMENT SERVICES IN ACCORDANCE WITH APPLICABLE LAWS. THE PROVIDER DOES
NOT GIVE OR PROVIDE TO YOU ANY GUIDANCE, INSTRUCTIONS, OR INFORMATION
ABOUT HOW OR IN WHICH MANNER YOU SHOULD PERFORM TRANSACTIONS WHEN
USING THE SERVICES OR OTHERWISE, OR ANY OTHER SIMILAR INFORMATION ABOUT
THE INVESTMENT TOOLS TRADED, NOR DOES THE PROVIDER ACCEPT ANY SUCH
GUIDANCE, INSTRUCTIONS, OR INFORMATION FROM YOU. NONE OF THE SERVICES
CONSTITUTE INVESTMENT ADVICE OR RECOMMENDATIONS. NO EMPLOYEES, STAFF, OR
REPRESENTATIVES OF THE PROVIDER ARE AUTHORIZED TO PROVIDE INVESTMENT
ADVICE OR RECOMMENDATIONS. SHOULD ANY INFORMATION OR STATEMENT OF ANY
EMPLOYEE, STAFF, OR REPRESENTATIVES OF THE PROVIDER BE INTERPRETED AS
2/15
INVESTMENT ADVICE OR RECOMMENDATIONS, THE PROVIDER EXPLICITLY DISCLAIMS
THAT THE SAME IS INVESTMENT ADVICE OR RECOMMENDATIONS AND SHALL NOT BE
RESPONSIBLE FOR THEM.
1.7. Your personal data is processed in accordance with the Privacy Policy.
1.8. The meaning of the definitions, expressions, and abbreviations used in these GTC can be
found in clause 18.
2. SERVICES AND THEIR ORDER
2.1. You can order the Services through the Website by completing the appropriate registration
or order form. After registration, we will e-mail you the login details for the Client Section
and/or Trading Platform and allow you to access them.
2.2. The Services include, among other things, the Free Trial, FTMO Challenge, and Verification
products; these products may differ in the scope of the Services provided
(e.g., by analytical tools available to the Customer). With the Free Trial, you may use
some of the Services within a limited scope and for a limited period free of charge.
Completing the Free Trial does not entitle you to access any other Services.
2.3. All data that you provide to us through the registration or order form, the Client Section,
or otherwise must be complete, true, and up to date. You must immediately notify us
of any change in your data or update the data in your Client Section. The Customer is
responsible for all the provided data being accurate and up to date; the Provider is not
obligated to verify the data.
2.4. You acknowledge that if you provide an identification number, tax registration number
or other similar information in the registration or order form or in the Client Section,
or if you state that you are a legal entity, you will be considered as an entrepreneur
(trader) for the purposes of these GTC and when using the Services, and the provisions
of these GTC or the applicable law that grant rights to consumers will not apply to you.
2.5. The fee for the FTMO Challenge varies according to the option selected and depends on
the amount of the initial capital, the degree of the acceptable risk, the parameters that
must be fulfilled so that the conditions of the FTMO Challenge and the subsequent
Verification are met, and possibly other configurations. More detailed information on
individual options and fees for those options are provided on our Website here. The final
fee will be determined based on the option you select when completing the form for
ordering the FTMO Challenge. The Provider reserves the right to also provide the Services
under individually agreed conditions. All individually agreed conditions shall be determined
by the Provider at its own discretion. Individual discounts and other benefits may not be
combined, unless expressly stipulated otherwise by the Provider.
2.6. The fee is paid for allowing you to access the FTMO Challenge, or the Services provided
under the FTMO Challenge. The Customer is not entitled to a refund of the fee, for
example, if the Customer cancels the Customer’s Client Section or requests the
cancellation by e-mail, if the Customer terminates the use of the Services or the contract
(for example, fails to complete the FTMO Challenge or the Verification), fails to meet the
conditions of the FTMO Challenge or the Verification, or violates these GTC.
2.7. If the Customer lodges an unjustifiable complaint regarding the paid fee or disputes
the paid fee with the Customer’s bank or payment service provider (e.g. through
chargeback services, dispute services, or other similar services), on the basis of which
an annulment, cancellation or refund of the fee or any part thereof is requested,
the Provider is entitled, at its own discretion, to stop providing to the Customer any
services and refuse any future provision of any services.
2.8. Your choice of the option of the FTMO Challenge that you select when making an order
shall also apply to the subsequent Verification. You will start the subsequent Verification
and, possibly, other products related thereto, with the parameters and the same currency
that correspond to the option of the FTMO Challenge selected by you. Once you make a
selection, it is not possible to change it.
If you are ordering a new FTMO Challenge, the restrictions specified in this clause 2.8
shall not apply.
3/15
2.9. The Provider reserves the right to unilaterally change the fees and parameters
of the Services at any time, including the parameters for their successful completion.
The change does not affect the Services purchased before the change is notified.
2.10. Any data entered in the order form can be checked, corrected, and amended until
the binding order of the Services. The order of the Services of your choice is made by
submitting the order form. The Provider will immediately confirm the receipt of your order
to your e-mail address. In the case of the Free Trial, the order is completed upon the
delivery of the confirmation to your e-mail address, whereby the contract is executed.
In the case of the FTMO Challenge, the order is completed upon the payment of the fee
for the selected option (more on this in clause 3.4), whereby the contract between you
and the Provider is executed, the subject of which is the provision of the FTMO Challenge
and, if the conditions of the FTMO Challenge are met, the Verification. The contract is
concluded in English. We archive the contract in electronic form and do not allow access
to it.
2.11. You acknowledge that in order to use our Services, you must obtain the appropriate
technical equipment and software, including third-party software (e.g., software for
the use of the Trading Platform), at your own risk and expense. The Website is accessible
from the most commonly used web browsers. The internet access, purchase of the
equipment, and purchase of the web browser and its updates are at your own risk
and expense. The Provider does not warrant or guarantee that the Services will be
compatible with any specific equipment or software. The Provider does not charge any
additional fees for the internet connection.
2.12. You acknowledge that the operators of trading platforms are persons or entities different
from the Provider and that their own terms and conditions and privacy policies will apply
when you use their services and products. Before sending an order form, you are obligated
to read those terms and conditions and privacy policies.
2.13. If the Customer places an unusually large number of orders for the Services within an
unreasonably short period of time, the Provider may notify the Customer through the
Client Section as a protective precaution to mitigate potentially harmful behaviour of the
Customer. If such unreasonable behaviour continuous after such notice, we reserve the
right to suspend any further orders of the Services by the Customer. If we identify that
the unusual behaviour as per this paragraph relates to the Customer’s involvement in
Forbidden Trading Practices, we may take respective actions as perceived in Section 5 of
this GTC. The Provider reserves the right to determine, at its own discretion, the nature
of the behaviour described above and reasonable boundaries for such determination.
3. PAYMENT TERMS
3.1. The amounts of fees for the FTMO Challenge options are in euros. The fee can also be paid
in other currencies that are listed on the Website. If you select any other currency than
the euro, the amount of the fee for the selected option of the FTMO Challenge shall be
converted by our rates and it will automatically display your payment total in your chosen
currency, so you know how much you are paying before you confirm the order. The
Customer acknowledges that if the payment is made in a currency other than the one the
Customer has chosen on the Website, the amount will be converted according to the
current exchange rates valid at the time of payment.
3.2. Service charges are inclusive of all taxes. If the Customer is an entrepreneur (trader), he
is obliged to fulfil all his tax obligations in connection with the use of our Services in
accordance with applicable law, and in the event of an obligation, he is obliged to pay tax
or other fees properly.
3.3. You can pay the fee for the selected option of the FTMO Challenge by a payment card, via
a bank transfer, or using other means of payment that the Provider currently offers on the
Website.
3.4. In the event of payment by a payment card or via any other express payment method,
the payment shall be made immediately. If you select a bank transfer for payment, we
will subsequently send you a proforma invoice in electronic form with the amount of the
fee for the option of the FTMO Challenge you have chosen on the Website. You undertake
to pay the amount within the period specified in the proforma invoice. The fee is
considered paid when its full amount is credited to the Provider’s account. If you do not
4/15
pay the amount on time, the Provider is entitled to cancel your order. Customer bears all
fees charged to Customer by the selected payment service provider (according to the valid
pricelist of the payment service provider) in connection with the transaction and the
Customer is obliged to ensure that the respective fee for the selected FTMO Challenge is
paid in full.
4. CLIENT SECTION AND TRADING PLATFORM
4.1. Only one Client Section is permitted per Customer and all of the Customer’s Services must
be maintained in the Client Section.
4.2. The total number of FTMO Challenges and Verifications per one Client Section may be
limited depending on the total sum of the initial capital amounts of the products ordered
by the Customer or on the basis of other parameters. Unless the Provider grants an
exception to the Customer, the initial capital amounts may not be transferred between the
individual products or mutually combined. You may also not transfer or combine your
performance, Service parameters, data, or any other information between the products.
4.3. Access to the Client Section and Trading Platform is protected by login data, which
the Customer may not make available or share with any third party. If the Customer has
registered as a legal entity, the Customer may allow the use of the Services through the
Customer’s Client Section to the authorized employees and representatives. The Customer
is responsible for all activities that are performed through the Customer’s Client Section
or Trading Platform. The Provider bears no responsibility, and the Customer is not entitled
to any compensation, for any misuse of the Client Section, Trading Platform, or any part
of the Services, nor is the Provider responsible for any negative consequences thereof for
the Customer, if such misuse occurs for any reasons on the part of the Customer.
4.4. The Customer acknowledges that the Services may not be available around the clock,
particularly with respect to maintenance, upgrades, or any other reasons. In particular,
the Provider bears no responsibility, and the Customer is not entitled to any compensation,
for the unavailability of the Client Section or Trading Platform and for damage or loss
of any data or other content that Customer uploads, transfers or saves through the Client
Section or Trading Platform.
4.5. The Customer may at any time request the cancellation of the Client Section by sending
an e-mail to support@ftmo.com. Sending a request for the cancellation of the Client
Section is considered as a request for termination of the contract by the Customer, with
the Customer being no longer entitled to use the Services, including the Client Section
and Trading Platform. The Provider will immediately confirm the receipt of the request to
the Customer by e-mail, whereby the contractual relationship between the Customer and
the Provider will be terminated. In such a case, the Customer is not entitled to any refund
of the fees already paid or costs otherwise incurred.
5. RULES OF DEMO TRADING
5.1. During the demo trading on the Trading Platform, you may perform any transactions,
unless these constitute forbidden trading strategies or practices within the meaning
of clause 5.4. You also agree to follow good market standard rules and practices for trading
on financial markets (e.g., risk management rules). Restrictions may also be imposed by
the trading conditions of the Trading Platform that you have selected for trading.
5.2. You acknowledge that the Provider has access to information about the demo trades that
you perform on the Trading Platform. You grant the Provider your consent to share this
information with persons/entities who are in a group with the Provider or who are
otherwise affiliated with the Provider, and you grant the Provider and these
persons/entities your consent and authorization to handle this information at their own
will. You agree that these activities may be performed automatically without any further
consent, consultation, or approval on your part being necessary, and that you are not
entitled to any remuneration or revenue associated with the use of the data
by the Provider. The Provider is aware that you do not provide the Provider with any
investment advice or recommendations through your demo trading. You acknowledge that
you may suspend your demo trading on the Trading Platform at any time.
5/15
5.3. The Provider bears no responsibility for the information displayed on the Trading Platform,
nor for any interruption of, or delay or inaccuracy in the market information displayed
through your Client Section.
5.4. FORBIDDEN TRADING PRACTICES.
5.4.1. DURING THE DEMO TRADING, IT IS PROHIBITED TO:
(a) KNOWINGLY OR UNKNOWINGLY USE TRADING STRATEGIES THAT
EXPLOIT ERRORS IN THE SERVICES SUCH AS ERRORS IN DISPLAY
OF PRICES OR DELAY IN THEIR UPDATE;
(b) PERFORM TRADES USING AN EXTERNAL OR SLOW DATA FEED;
(c) PERFORM, ALONE OR IN CONCERT WITH ANY OTHER PERSONS,
INCLUDING BETWEEN CONNECTED ACCOUNTS, OR ACCOUNTS HELD
WITH DIFFERENT FTMO ENTITIES, TRADES OR COMBINATIONS OF
TRADES THE PURPOSE OF WHICH IS TO MANIPULATE TRADING, FOR
EXAMPLE BY SIMULTANEOUSLY ENTERING INTO OPPOSITE POSITIONS;
(d) PERFORM TRADES IN CONTRADICTION WITH THE TERMS AND
CONDITIONS OF THE PROVIDER AND THE TRADING PLATFORM;
(e) USE ANY SOFTWARE, ARTIFICIAL INTELLIGENCE, ULTRA-HIGH SPEED,
OR MASS DATA ENTRY WHICH MIGHT MANIPULATE, ABUSE, OR GIVE
YOU AN UNFAIR ADVANTAGE WHEN USING OUR SYSTEMS OR
SERVICES;
(f) PERFORM GAP TRADING BY OPENING TRADE(S):
(I) WHEN MAJOR GLOBAL NEWS, MACROECONOMIC EVENT OR
CORPORATE REPORTS OR EARNINGS (“EVENTS”), THAT MIGHT
AFFECT THE RELEVANT FINANCIAL MARKET (I.E. MARKET THAT
ALLOWS TRADING OF FINANCIAL INSTRUMENTS THAT MIGHT BE
AFFECTED BY THE EVENTS), ARE SCHEDULED; AND
(II)2 HOURS OR LESS BEFORE A RELEVANT FINANCIAL MARKET IS
CLOSED FOR 2 HOURS OR LONGER.; OR
(g) OTHERWISE PERFORM TRADES IN CONTRADICTION WITH HOW
TRADING IS ACTUALLY PERFORMED IN THE FOREX MARKET OR IN ANY
OTHER FINANCIAL MARKET, OR IN A WAY THAT ESTABLISHES
JUSTIFIED CONCERNS THAT THE PROVIDER MIGHT SUFFER FINANCIAL
OR OTHER HARM AS A RESULT OF THE CUSTOMER’S ACTIVITIES (E.G.
OVERLEVERAGING, OVEREXPOSURE, ONE-SIDED BETS, ACCOUNT
ROLLING).
5.4.2. As our Customer, you should understand and agree that all our Services are
for Customer’s personal use only, meaning that only you personally can access
your FTMO Challenge and Verification accounts and perform trades. For that
reason, you should not, and you agree not to,
(a) allow access to and trading on your FTMO Challenge and Verification
accounts by any third party nor you shall engage or cooperate with any
third party in order to have such third party perform trades for you,
whether such third party is a private person or a professional;
(b) access any third-party FTMO Challenge and Verification accounts, trade
on behalf of any third party or perform any account management or
similar services, where you agree to trade, operate or manage the FTMO
Challenge and Verification accounts on behalf of another user, all whether
performed as a professional or otherwise.
Please note that if you act or behave in contradiction with the aforesaid, we
will consider such action/behaviour as a Forbidden Trading Practice under
Section 5.4. with respective consequences as perceived under this GTC.
5.4.3. Furthermore, Customer shall not exploit the Services by performing trades
without applying market standard risk management rules for trading on
financial markets, this includes, among others, the following practices (i)
opening substantially larger position sizes compared to Customer’s other
6/15
trades, whether on this or any other Customer’s account, or (ii) opening
substantially smaller or larger number of positions compared to Customer’s
other trades, whether on this or any other Customer’s account.
The Provider reserves the right to determine, at its own discretion, whether certain trades,
practices, strategies, or situations are Forbidden Trading Practices.
5.5. If the Customer engages in any of the Forbidden Trading Practices described in clause 5.4,
(i) the Provider may consider it as a failure to meet the conditions of the particular FTMO
Challenge or Verification, (ii) the Provider may remove the transactions that violate
the prohibition from the Customer’s trading history and/or not count their results in the
profits and/or losses achieved by the demo trading, (iii) to immediately cancel all Services
provided to the Customer and subsequently terminate this contract, or (iv) reduce the
offered leverage on products to 1:5 on any or all Customer’s accounts.
5.6. In case when some or all Forbidden Trading Practices are executed on one or more FTMO
Challenge and Verification accounts of one Customer, or accounts of various Customers,
or by combining trading through FTMO Challenge and Verification accounts and FTMO
Trader accounts, then the Provider is entitled to cancel all Services and terminate all
respective contracts related to any and all Customer’s FTMO Challenge and Verification
accounts and/or apply other measures in Clause 5.5. The Provider may exercise any and
all actions in Clauses 5.5 and 5.6 at its own discretion.
5.7. If any FTMO Trader accounts were used for or were involved in the Forbidden Trading
Practices, this may and will constitute a breach of respective terms and conditions for
FTMO Trader account with third-party provider and may result in cancellation of all such
user accounts and termination of respective agreements by the third-party provider.
5.8. If the Customer engages in any of the practices described in clause 5.4 repeatedly,
and the Provider has previously notified the Customer thereof, the Provider may prevent
the Customer from accessing all Services or their parts, including access to the Client
Section and Trading Platform, without any compensation. In such a case, the Customer is
not entitled to a refund of the fees paid.
5.9. The Provider does not bear any responsibility for trading or other investment activities
performed by the Customer outside the relationship with the Provider, for example
by using data or other information from the Client Section, Trading Platform, or otherwise
related to the Services in real trading on financial markets, not even if the Customer uses
for such trading the same Trading Platform that the Customer uses for demo trading.
5.10. DEVELOPMENTS IN FINANCIAL MARKETS ARE SUBJECT TO FREQUENT AND ABRUPT
CHANGES. TRADING ON FINANCIAL MARKETS MAY NOT BE PROFITABLE AND CAN LEAD
TO SIGNIFICANT FINANCIAL LOSSES. ANY PREVIOUS PERFORMANCES AND PROFITS OF
THE CUSTOMER’S DEMO TRADING ARE NOT A GUARANTEE OR INDICATION OF ANY
FURTHER PERFORMANCE.
6. FTMO CHALLENGE AND VERIFICATION
6.1. After paying the fee for the selected option of the FTMO Challenge, the Customer will
receive the relevant login data for the Trading Platform at the e-mail address provided by
the Customer or in the Client Section. The Customer activates the FTMO Challenge by
opening the first demo trade in the Trading Platform. YOU ACKNOWLEDGE THAT,
BY OPENING THE FIRST DEMO TRADE, YOU EXPRESSLY DEMAND THE PROVIDER
TO PROVIDE COMPLETE SERVICES. IF YOU ARE A CONSUMER, IT MEANS THE
COMPLETION OF SERVICES BEFORE THE EXPIRY OF THE PERIOD FOR WITHDRAWAL
FROM THE CONTRACT, WHICH AFFECTS YOUR RIGHT TO WITHDRAW FROM
THE CONTRACT, AS SPECIFIED IN MORE DETAIL IN CLAUSE 12. If you do not activate the
FTMO Challenge within 30 calendar days of the date on which it was made available to
you, your access to it will be suspended. You can request the renewal of access via the
Client Section or by sending an e-mail to support@ftmo.com within 6 months of the initial
suspension, otherwise we will terminate the provision of the Services without any right to
a refund of the fee.
6.2. In order for the Customer to meet the conditions of the FTMO Challenge, the Customer
must fulfil all of the following parameters at the same time:
7/15
6.2.1. the Customer has opened at least one demo trade on at least four different
calendar days;
6.2.2. in the course of none of the calendar days during the FTMO Challenge did
the Customer report a loss on any demo trades opened and closed on that
day, which would exceed the percentage of the initial capital for the
respective option as described below:
FTMO Challenge FTMO Challenge
Aggressive FTMO Challenge Swing
in total 5% of the
initial capital
in total 10% of the
initial capital
in total 5% of the
initial capital
6.2.3. at no time during the FTMO Challenge did the Customer report a loss on
any opened and closed demo transactions, which would exceed in total
the percentage of the initial capital for the respective option as described
below:
FTMO Challenge FTMO Challenge
Aggressive FTMO Challenge Swing
in total 10% of the
initial capital
in total 20% of the
initial capital
in total 10% of the
initial capital
6.2.4. the Customer is in a total profit on all closed demo trades amounting to
at least the percentage of the initial capital for the respective option as
described below:
FTMO Challenge FTMO Challenge
Aggressive FTMO Challenge Swing
in total 10% of the
initial capital
in total 20% of the
initial capital
in total 10% of the
initial capital
The above parameters are explained in more detail here on the Website.
6.3. If the Customer has met the conditions of the FTMO Challenge specified in clause 6.2, and
at the same time has not violated these GTC, in particular the rules of demo trading under
clause 5.4, the Provider will evaluate the FTMO Challenge as successful and will make the
Verification available to the Customer free of charge by sending login details to the
Customer’s e-mail address or Client Section. The Provider does not have to evaluate the
FTMO Challenge if the Customer has not closed all trades.
6.4. The Customer activates the Verification by opening the first demo trade in the Trading
Platform. If the Customer does not activate the Verification within 30 calendar days from
the day on which the Customer received the new login data, the Customer’s access to the
Verification will be suspended. The Customer may request the renewal of access via the
Client Section or by sending an e-mail to support@ftmo.com within 6 months of the
suspension, otherwise we will terminate the provision of the Services without any right to
a refund.
6.5. In order for the Customer to meet the conditions of the Verification, the Customer must
fulfil all of the following parameters at the same time:
6.5.1. during the Verification, the Customer has opened at least one demo trade
on at least four different calendar days;
8/15
6.5.2. in the course of none of the calendar days during the Verification did the
Customer report a loss on any demo trades opened and closed on that
day, which would exceed the percentage of the initial capital for the
respective option as described below:
Verification
Verification
Aggressive Verification Swing
in total 5% of the
initial capital
in total 10% of the
initial capital
in total 5% of the
initial capital
6.5.3. at no time during the Verification did the Customer report a loss on the
sum of the opened and closed demo trades, which would exceed in total
the percentage of the initial capital for the respective option as described
below:
Verification
Verification
Aggressive Verification Swing
in total 10% of the
initial capital
in total 20% of the
initial capital
in total 10% of the
initial capital
6.5.4. Customer is in total profit from all closed demo trades amounting to at
least the percentage of the initial capital for the respective option as
described below:
Verification Verification Aggressive Verification Swing
in total 5% of the
initial capital;
in total 10% of the
initial capital
in total 5% of the
initial capital
The above parameters are explained in more detail here on the Website.
6.6. For the Customer to meet conditions of the Verification, the Customer shall comply with
the following:
6.6.1. Customer has met the conditions of the Verification specified in clause
6.5;
6.6.2. Customer has not violated these GTC, in particular, the rules of demo
trading under clause 5.4; and
6.6.3. Customer has not exceeded the maximum total amount of the capital
allocation of USD 400,000 (USD 200,000 for the Aggressive option),
individually or in combination, per Customer or per each trading strategy,
within the meaning of applicable FTMO Trader Program agreement, if
Customer is already participating in the FTMO Trader Program.
If the above conditions are met, the Provider will evaluate the Verification as successful
and will recommend the Customer as a candidate for FTMO Trader program. The Provider
does not have to evaluate the Verification if the Customer has not closed all transactions.
6.7. If during the FTMO Challenge the Customer does not comply with some of the conditions
specified in clause 6.2.2. or 6.2.3., the FTMO Challenge will be evaluated as unsuccessful,
and the Customer will not be allowed access to the subsequent Verification. If during the
Verification the Customer does not comply with any of the conditions specified in clause
6.5.2. or 6.5.3., the Verification will be evaluated as unsuccessful, and the Customer will
not be recommended as a candidate for the FTMO Trader program. In such cases, the
Customer’s account and Services will be cancelled without refund of fees already paid.
9/15
6.8. Provider recommending Customer as a candidate for the FTMO Trader Program in no way
guarantees Customer’s acceptance into the FTMO Trader Program. The Provider is not
responsible for Customer being rejected by the FTMO Trader Program for any or no reason.
7. FTMO TRADER
If the Customer is successful in both the Challenge and Verification, the Customer may be
offered a contract by a third-party company, in its sole discretion to participate in the
FTMO Trader Program. The terms, conditions, and agreement between the Customer and
a third-party company are strictly between the Customer and the third-party company.
FTMO Evaluation Global s.r.o. is in no way involved with the FTMO Trader Program
agreement—or lack thereof—executed between the third-party company and the
Customer. The Customer acknowledges their personal data may be shared with a thirdparty company for purposes of considering offering such a contract.
8. USE OF THE WEBSITE, SERVICES AND OTHER CONTENT
8.1. The Website and all Services, including the Client Section, their appearance
and all applications, data, information, multimedia elements such as texts, drawings,
graphics, design, icons, images, audio and video samples, and any other content that may
form the Website and the Services (collectively as the “Content”), are subject to legal
protection pursuant to copyright laws and other legal regulations and are the property of
the Provider or the Provider’s licensors. The Provider grants you limited, non-exclusive,
non-transferable, non-assignable, non-passable, and revocable permission to use the
Content for the purpose of using the Services for your personal use and in accordance
with the purpose for which the Services are provided. The Content is not sold or otherwise
transferred to you and remains the property of the Provider or the Provider’s licensors.
8.2. All trademarks, logos, trade names, and other designations are the property of the
Provider or Provider’s licensors, and the Provider does not grant you any authorization to
use them.
8.3. Both the Customer and the Provider undertake to act in accordance with the principles
of fair dealing in the performance of the contract and in mutual negotiations and, in
particular, not to damage the good reputation and legitimate interests of the other party.
The Customer and the Provider will resolve any possible disagreements or disputes
between them in accordance with these GTC and the applicable law.
8.4. Except for the rights expressly set out in these GTC, the Provider does not grant you any
other rights relating to the Services and other Content. You may only use the Services
and other Content as set out in these GTC.
8.5. When accessing the Services and other Content, the following is prohibited:
8.5.1. to use any tools that may adversely affect the operation of the
Website and Services or that would be intended to take advantage of
errors, bugs or other deficiencies of the Website and Services;
8.5.2. to circumvent geographical restrictions of availability or any other
technical restrictions;
8.5.3. to make copies or back-ups of the Website and other Content;
8.5.4. to reverse-engineer, decompile, disassemble or otherwise modify
the Website and other Content;
8.5.5. to sell, rent, lend, license, distribute, reproduce, spread, stream,
broadcast or use the Services or other Content otherwise than
as permitted;
8.5.6. to use automated means to view, display or collect information
available through the Website or Services; and
8.5.7. to use any other tools or means the use of which could cause
any damage to the Provider.
8.6. The provisions of clause 8 are not intended to deprive the Customer of the Customer’s
consumer rights which cannot be excluded by law.
10/15
9. DISCLAIMER
9.1. YOU ACKNOWLEDGE THAT THE SERVICES AND OTHER CONTENT ARE PROVIDED “AS IS”
WITH ALL THEIR ERRORS, DEFECTS AND SHORTCOMINGS, AND THAT THEIR USE IS AT
YOUR SOLE RESPONSIBILITY AND RISK. TO THE MAXIMUM EXTENT PERMITTED BY THE
MANDATORY LAWS, THE PROVIDER DISCLAIMS ANY STATUTORY, CONTRACTUAL,
EXPRESS, AND IMPLIED WARRANTIES OF ANY KIND, INCLUDING ANY WARRANTY OF
QUALITY, MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, OR NONINFRINGEMENT OF ANY RIGHTS.
9.2. TO THE EXTENT PERMITTED BY THE MANDATORY PROVISIONS OF THE APPLICABLE
LAWS, THE PROVIDER IS NOT RESPONSIBLE FOR ANY HARM, INCLUDING ANY INDIRECT,
INCIDENTAL, SPECIAL, PUNITIVE OR CONSEQUENTIAL DAMAGES, INCLUDING LOST
PROFIT, LOSS OF DATA, PERSONAL OR OTHER NON-MONETARY HARM OR PROPERTY
DAMAGE CAUSED AS A RESULT OF USE OF THE SERVICES OR RELIANCE ON ANY TOOL,
FUNCTIONALITY, INFORMATION OR ANY OTHER CONTENT AVAILABLE IN CONNECTION
WITH THE USE OF THE SERVICES OR ELSEWHERE ON THE WEBSITE. THE PROVIDER IS
NOT RESPONSIBLE FOR ANY PRODUCTS, SERVICES, APPLICATIONS OR OTHER THIRDPARTY CONTENT THAT THE CUSTOMER USES IN CONNECTION WITH THE SERVICES. IN
CASE THE PROVIDER’S LIABILITY IS INFERRED IN CONNECTION WITH THE OPERATION
OF THE WEBSITE OR PROVISION OF THE SERVICES BY A COURT OF JUSTICE OR ANY
OTHER COMPETENT AUTHORITY, THIS LIABILITY SHALL BE LIMITED TO THE AMOUNT
CORRESPONDING TO THE FEE PAID BY THE CUSTOMER FOR THE SERVICES IN
CONNECTION WITH WHICH THE CUSTOMER HAS INCURRED THE LOSS.
9.3. The Provider reserves the right to modify, change, replace, add, or remove any elements
and functions of the Services at any time without any compensation.
9.4. The Provider is not responsible for its failure to provide the purchased Services if that
failure occurs due to serious technical or operational reasons beyond the Provider’s
control, in the case of any crisis or imminent crisis, natural disaster, war, insurrection,
pandemic, a threat to a large number of people or other force majeure events, and/or
if the Provider is prevented from providing the Services as a result of any obligations
imposed by law or a decision of a public authority.
9.5. The provisions of Clause 9 are not intended to deprive the Customer of the Customer’s
consumer or other rights that cannot be excluded by law.
10. VIOLATION OF THE GTC
10.1. IF THE CUSTOMER VIOLATES ANY PROVISION OF THESE GTC IN A MANNER THAT MAY
CAUSE ANY HARM TO THE PROVIDER, IN PARTICULAR, IF THE CUSTOMER ACCESSES THE
SERVICES IN CONFLICT WITH CLAUSE 1.3 OR 1.4, IF THE CUSTOMER PROVIDES
INCOMPLETE, UNTRUE OR NON-UPDATED INFORMATION IN CONFLICT WITH CLAUSE 2.3,
IF THE CUSTOMER ACTS IN A MANNER THAT MAY DAMAGE THE PROVIDER’S GOOD
REPUTATION, IF THE CUSTOMER VIOLATES THE DEMO TRADING RULES PURSUANT TO
CLAUSE 5.4, IF THE CUSTOMER ACTS IN CONFLICT WITH CLAUSE 8.3, AND/OR
IF THE CUSTOMER PERFORMS ANY OF THE ACTIVITIES REFERRED TO IN CLAUSE 8.5,
THE PROVIDER MAY PREVENT THE CUSTOMER FROM ORDERING ANY OTHER SERVICES
AND COMPLETELY OR PARTIALLY RESTRICT THE CUSTOMER’S ACCESS TO ALL OR ONLY
SOME SERVICES, INCLUDING ACCESS TO THE CLIENT SECTION AND TRADING
PLATFORM, WITHOUT ANY PRIOR NOTICE AND WITHOUT ANY COMPENSATION.
11. COMMUNICATION
11.1. You acknowledge that all communication from the Provider or its partners in connection
with the provision of Services will take place through the Client Section or your e-mail
address, which you register with us. Written electronic communication by e-mail
or through the Client Section is also considered to be written communication.
11.2. Our contact e-mail address is support@ftmo.com and our contact address is Purkynova
2121/3, Prague 1, 11000, Czech Republic.
11/15
12. RIGHT TO WITHDRAW FROM A CONTRACT
12.1. If you are a consumer, you have the right to withdraw from a contract without giving a
reason within 14 days of its execution (see clause 2.10 for details on the time of execution
of the agreement). PLEASE NOTE THAT IF YOU START PERFORMING DEMO TRADES
BEFORE THE EXPIRY OF THE SPECIFIED TIME LIMIT, YOU LOSE YOUR RIGHT TO
WITHDRAW FROM THE CONTRACT.
12.2. Your withdrawal from the contract must be sent to our e-mail address support@ftmo.com
within the specified time limit. You can use the template form available here to withdraw.
We will confirm the receipt of the form to you in text form without undue delay. If you
withdraw from the contract, we will refund you without undue delay (no later than 14 days
after your withdrawal from the contract) all fees we have received from you, in the same
way in which you paid them.
12.3. The Provider is entitled to withdraw from the contract in the case of any breach by the
Customer specified in Clause 10. The withdrawal has effect from the day of its delivery to
the e-mail address of the Customer or through the Client Section.
13. DEFECTIVE PERFORMANCES
13.1. If the Services do not correspond to what was agreed or have not been provided to you,
you can exercise your rights from defective performance. The Provider does not provide
any guarantee for the quality of the services. You must notify us of the defect without
undue delay at our e-mail address or at our address listed in clause 11.2. When exercising
the rights from defective performance, you may request that we remedy the defect
or provide you with a reasonable discount. If the defect cannot be remedied, you can
withdraw from the contract or claim a reasonable discount.
13.2. We will try to resolve any complaint you may lodge as soon as possible (no later than
within 30 calendar days), and we will confirm its receipt and settlement to you in writing.
If we do not settle the complaint in time, you have the right to withdraw from the contract.
You can file a complaint by sending an e-mail to our e-mail address support@ftmo.com.
14. CHANGES TO THE GTC
14.1. The Provider reserves the right to change these GTC from time to time with effect for the
contract previously entered into by the Customer. The Provider will notify the Customer
of the change in the GTC at least 7 days before the change in the GTC is effective, via the
Client Section or by e-mail. If the Customer does not agree with the change, the Customer
is entitled to reject it. The Customer must do so no later than on the last business day
before these changes take effect by sending the rejection to our e-mail address
support@ftmo.com. Upon receiving such rejection, the contract will be terminated. If the
Customer does not reject the change, it is considered that the Customer agrees to the
new version of GTC.
14.2. If the change offers the Customer a new service or other additional functionalities or this
change is solely to their advantage, the Provider can inform the Customer about this
change less than 7 days before the effective date of such change, but no later than the
day before its effectiveness.
14.3. The Provider will mainly change these GTC for the following reasons:
14.3.1. to introduce new services or products or amend existing services or
products;
14.3.2. to reflect legal or regulatory requirements that apply to the Provider;
14.3.3. when the Provider will try to make these GTC easier to understand
or more helpful to the Customer;
14.3.4. to adjust the way our Services are provided, particularly if the change
is needed because of a change in the way the technology is provided
or background processes;
14.3.5. to reflect changes in the cost of running our business.
12/15
15. OUT-OF-COURT CONSUMER DISPUTE SETTLEMENT
15.1. It is our objective that our customers are satisfied with the FTMO services; therefore, if
you have any complaints or suggestions, we will be happy to resolve them directly with
you and you can contact us at our e-mail address or at our address listed in clause 11.2.
15.2. This section 15.2 applies only to a consumer who is at the same time an EU resident. The
Czech Trade Inspection Authority (Česká obchodní inspekce), with its registered office at
Štěpánská 567/15, 120 00 Prague 2, identification no.: 000 20 869, website:
https://www.coi.cz/en/information-about-adr/, is responsible for the out-of-court
settlement of consumer disputes. You can also use the platform at the following website
to resolve disputes online: https://www.ec.europa.eu/consumers/odr.
16. CHOICE OF LAW AND JURISDICTION
16.1. Any legal relations established by these GTC or related to them, as well as any related
non-contractual legal relations, shall be governed by the laws of the Czech Republic.
Any dispute that may arise in connection with these GTC and/or related agreements
will fall within the jurisdiction of the Czech court having local jurisdiction according to
the registered office of the Provider.
16.2. The provisions of clause 16.1 do not deprive the consumers of the protection afforded
to them by the mandatory laws of the relevant Member State of the European Union or any
other jurisdiction.
17. DURATION AND TERMINATION OF THE CONTRACT
17.1. The contract is concluded for a definite period until the FTMO Challenge or Verification is
passed or failed in accordance with the clause 6.2. or 6.5 respectively.
17.2. The contract may be terminated by either party earlier in accordance with these GTC. The
contract terminates automatically and with immediate effect in case the Customer during
FTMO Challenge or Verification does not open at least one demo trade during a period of
30 consecutive days.
17.3. Notwithstanding clause 17.2 the Provider may terminate this contract with cause and
immediate effect when the provision of Services under contract would affect the ability of
the Provider to adhere to its legal obligations or orders or decisions of a governmental
bodies or other regulators
17.4. Either Party may terminate this contract without cause by serving a written notice at least
7 days in advance in accordance with Clause 11 on the other Party.
18. FINAL PROVISIONS
18.1. The Provider has not adopted any consumers codes of conduct.
18.2. These GTC constitute the complete terms and conditions agreed between you and the
Provider and supersede all prior agreements relating to the subject matter of the GTC,
whether verbal or written.
18.3. Nothing in these GTC is intended to limit any legal claims set out elsewhere in these GTC
or arising from the applicable law. If the Provider or any third party authorized thereto
does not enforce the compliance with these GTC, this can in no way be construed
as a waiver of any right or claim.
18.4. The Provider may assign any claim arising to the Provider from these GTC
or any agreement to a third party without your consent. You agree that the Provider may,
as the assignor, transfer its rights and obligations under these GTC or any agreement
or parts thereof to a third party. The Customer is not authorized to transfer or assign
the Customer’s rights and obligations under these GTC or any agreements or parts
thereof, or any receivables arising from them, in whole or in part, to any third party.
18.5. If any provision of the GTC is found to be invalid or ineffective, it shall be replaced
by a provision whose meaning is as close as possible to the invalid provision. The invalidity
13/15
or ineffectiveness of one provision shall not affect the validity of the other provisions.
No past or future practice established between the parties and no custom maintained
in general or in the industry relating to the subject-matter of the performance, which is
not expressly referred to in the GTC, shall be applied and no rights and obligations shall
be derived from them for the parties; in addition, they shall not be taken into account
in the interpretation of manifestations of the will of the parties.
18.6. The schedules to the GTC form integral parts of the GTC. In the event of a conflict between
the wording of the main text of the GTC and any schedule thereof, the main text of the GTC
shall prevail.
18.7. Prior to the mutual acceptance of these GTC, the parties have carefully assessed
the possible risks arising from them and accept those risks.
19. DEFINITIONS, EXPRESSIONS AND ABBREVIATIONS USED
19.1. For the purposes of the GTC, the following definitions shall have the following meanings:
19.1.1. “Client Section” means the user interface located on the Website;
19.1.2. “Content” means the Website and all Services, including the Client
Section, their appearance and all applications, data, information,
multimedia elements such as texts, drawings, graphics, design,
icons, images, audio and video samples and other content that may
form the Website and the Services (as set out in clause 8.1);
19.1.3. “Customer” means the user of the Services (as set out in clause
1.1);
19.1.4. “Events” means events as set out in clause 5.4.1(f)(I);
19.1.5. “FTMO Challenge and Verification account” means trading
accounts related to trading education courses provided as part of the
Services by the Provider;
19.1.6. “FTMO Trader account” means a trading account, which relates to
the FTMO Trader program provided by a third-party provider;
19.1.7. “Forbidden Trading Practices” means trading practices strictly
forbidden while using our Services and are more detailed in Section
5.4 of these GTC;
19.1.8. “GTC” means these General Terms and Conditions of FTMO;
19.1.9. “Provider” means the provider of certain Services (as set out
in clause 1.1);
19.1.10. “Schedules” means Schedule 1 and any other Schedules as
applicable, which are part of these GTC;
19.1.11. “Services” means the Provider’s services as set out in clauses 1.1
and 1.5;
19.1.12. “Trading Platform” means an electronic interface provided
by a third party in which the Customer performs the demo trading;
and
19.1.13. “Website” means the website www.ftmo.com.
19.2. For the purposes of the GTC and their schedules, the following expressions
and abbreviations shall have the following meanings:
19.2.1. “calendar day” means the period from midnight to midnight
of the time currently valid in the Czech Republic (Central European
(Summer) Time, CE(S)T);
19.2.2. “initial capital” means a fictitious amount that the Customer has
chosen when selecting the option of the FTMO Challenge and which
the Customer will use to perform demo trading;
19.2.3. “CZK” means the Czech crown;
14/15
19.2.4. “EUR” means the euro;
19.2.5. “USD” means the United States dollar;
19.2.6. “GBP” means the British pound;
19.2.7. “CAD” means the Canadian dollar;
19.2.8. “AUD” means the Australian dollar;
19.2.9. “NZD” means the New Zealand dollar; and
19.2.10. “CHF” means the Swiss franc.
These GTC shall enter into force and effect on 13 July 2023.
15/15
SCHEDULE 1
OPTIONS OF FTMO CHALLENGES AND VERIFICATIONS
- FTMO Challenge or Verification with an initial capital of EUR 10,000 (or the corresponding
equivalent: USD 10,000, GBP 10,000, CZK 250,000, CHF 10,000, CAD 15,000 or AUD 15,000)
- FTMO Challenge or Verification Aggressive with an initial capital of EUR 10,000 (or the
corresponding equivalent: USD 10,000, GBP 10,000, CZK 250,000, CHF 10,000, CAD 15,000 or AUD
15,000)
- FTMO Challenge or Verification Swing with an initial capital of EUR 10,000 (or the corresponding
equivalent: USD 10,000, GBP 10,000, CZK 250,000, CHF 10,000, CAD 15,000 or AUD 15,000)
- FTMO Challenge or Verification with an initial capital of EUR 20,000 (or the corresponding
equivalent: USD 25,000, GBP 20,000, CZK 500,000, CHF 20,000, CAD 30,000 or AUD 30,000)
- FTMO Challenge or Verification Aggressive with an initial capital of EUR 20,000 (or the
corresponding equivalent: USD 25,000, GBP 20,000, CZK 500,000, CHF 20,000, CAD 30,000 or AUD
30,000)
- FTMO Challenge or Verification Swing with an initial capital of EUR 20,000 (or the corresponding
equivalent: USD 25,000, GBP 20,000, CZK 500,000, CHF 20,000, CAD 30,000 or AUD 30,000)
- FTMO Challenge or Verification with an initial capital of EUR 40,000 (or the corresponding
equivalent: USD 50,000, GBP 35,000, CZK 1,000,000, CHF 40,000, CAD 60,000 or AUD 65,000)
- FTMO Challenge or Verification Aggressive with an initial capital of EUR 40,000 (or the
corresponding equivalent: USD 50,000, GBP 35,000, CZK 1,000,000, CHF 40,000, CAD 60,000 or
AUD 65,000)
FTMO Challenge or Verification Swing with an initial capital of EUR 40,000 (or the corresponding
equivalent: USD 50,000, GBP 35,000, CZK 1,000,000, CHF 40,000, CAD 60,000 or AUD 65,000)
- FTMO Challenge or Verification with an initial capital of EUR 80,000 (or the corresponding
equivalent: USD 100,000, GBP 70,000, CZK 2,000,000, CHF 80,000, CAD 120,000 or AUD 130,000)
- FTMO Challenge or Verification Aggressive with an initial capital of EUR 80,000 (or the
corresponding equivalent: USD 100,000, GBP 70,000, CZK 2,000,000, CHF 80,000, CAD 120,000 or
AUD 130,000)
- FTMO Challenge or Verification Swing with an initial capital of EUR 80,000 (or the corresponding
equivalent: USD 100,000, GBP 70,000, CZK 2,000,000, CHF 80,000, CAD 120,000 or AUD 130,000)
- FTMO Challenge or Verification with an initial capital of EUR 160,000 (or the corresponding
equivalent: USD 200,000, GBP 140,000, CZK 4,000,000, CHF 160,000, CAD 240,000 or AUD
260,000)
- FTMO Challenge or Verification Swing with an initial capital of EUR 160,000 (or the corresponding
equivalent: USD 200,000, GBP 140,000, CZK 4,000,000, CHF 160,000, CAD 240,000 or AUD
260,000)```

-----------

Path: Sophy_temp/docs/README.md

```
# Sophy Trading System

Een professioneel algoritmisch trading systeem gebouwd in Python dat de Turtle Trading strategie implementeert via
MetaTrader 5, speciaal geoptimaliseerd voor FTMO-accounts.

## Kenmerken

- **Modulaire architectuur** - Duidelijke scheiding van verantwoordelijkheden
- **Meerdere strategieën** - Ondersteunt verschillende trading strategieën met een factory patroon
- **FTMO Compliance** - Ingebouwde controles voor naleving van FTMO-regels
- **Risicomanagement** - Geavanceerd positie-sizing en risicobeheer
- **Backtesting** - Uitgebreide backtesting mogelijkheden
- **Performance analyse** - Gedetailleerde rapportage en visualisatie

## Installatie

```bash
# Kloon de repository
git clone https://github.com/yourusername/sophy.git
cd sophy

# Installeer dependencies
pip install -r requirements.txt

# Optioneel: Installeer in development mode
pip install -e .```

-----------

Path: Sophy_temp/requirements.txt

```plaintext
��a n y i o = = 4 . 8 . 0  
 a r g o n 2 - c f f i = = 2 3 . 1 . 0  
 a r g o n 2 - c f f i - b i n d i n g s = = 2 1 . 2 . 0  
 a r r o w = = 1 . 3 . 0  
 a s t r o i d = = 3 . 3 . 8  
 a s t t o k e n s = = 3 . 0 . 0  
 a s y n c - l r u = = 2 . 0 . 4  
 a t t r s = = 2 4 . 3 . 0  
 b a b e l = = 2 . 1 6 . 0  
 b a c k t r a d e r = = 1 . 9 . 7 8 . 1 2 3  
 b e a u t i f u l s o u p 4 = = 4 . 1 2 . 3  
 b l a c k = = 2 5 . 1 . 0  
 b l e a c h = = 6 . 2 . 0  
 c e r t i f i = = 2 0 2 4 . 1 2 . 1 4  
 c f f i = = 1 . 1 7 . 1  
 c h a r s e t - n o r m a l i z e r = = 3 . 4 . 1  
 c l i c k = = 8 . 1 . 8  
 c o l o r a m a = = 0 . 4 . 6  
 c o m m = = 0 . 2 . 2  
 c o n t o u r p y = = 1 . 3 . 1  
 c y c l e r = = 0 . 1 2 . 1  
 d e b u g p y = = 1 . 8 . 1 1  
 d e c o r a t o r = = 5 . 1 . 1  
 d e f u s e d x m l = = 0 . 7 . 1  
 d i l l = = 0 . 3 . 9  
 e t _ x m l f i l e = = 2 . 0 . 0  
 e x e c u t i n g = = 2 . 1 . 0  
 f a s t j s o n s c h e m a = = 2 . 2 1 . 1  
 f o n t t o o l s = = 4 . 5 5 . 3  
 f q d n = = 1 . 5 . 1  
 h 1 1 = = 0 . 1 4 . 0  
 h t t p c o r e = = 1 . 0 . 7  
 h t t p x = = 0 . 2 8 . 1  
 i d n a = = 3 . 1 0  
 i p y k e r n e l = = 6 . 2 9 . 5  
 i p y t h o n = = 8 . 3 1 . 0  
 i p y w i d g e t s = = 8 . 1 . 5  
 i s o d u r a t i o n = = 2 0 . 1 1 . 0  
 i s o r t = = 6 . 0 . 1  
 j e d i = = 0 . 1 9 . 2  
 J i n j a 2 = = 3 . 1 . 5  
 j s o n 5 = = 0 . 1 0 . 0  
 j s o n p o i n t e r = = 3 . 0 . 0  
 j s o n s c h e m a = = 4 . 2 3 . 0  
 j s o n s c h e m a - s p e c i f i c a t i o n s = = 2 0 2 4 . 1 0 . 1  
 j u p y t e r = = 1 . 1 . 1  
 j u p y t e r - c o n s o l e = = 6 . 6 . 3  
 j u p y t e r - e v e n t s = = 0 . 1 1 . 0  
 j u p y t e r - l s p = = 2 . 2 . 5  
 j u p y t e r _ c l i e n t = = 8 . 6 . 3  
 j u p y t e r _ c o r e = = 5 . 7 . 2  
 j u p y t e r _ s e r v e r = = 2 . 1 5 . 0  
 j u p y t e r _ s e r v e r _ t e r m i n a l s = = 0 . 5 . 3  
 j u p y t e r l a b = = 4 . 3 . 4  
 j u p y t e r l a b _ p y g m e n t s = = 0 . 3 . 0  
 j u p y t e r l a b _ s e r v e r = = 2 . 2 7 . 3  
 j u p y t e r l a b _ w i d g e t s = = 3 . 0 . 1 3  
 k i w i s o l v e r = = 1 . 4 . 8  
 M a r k u p S a f e = = 3 . 0 . 2  
 m a t p l o t l i b = = 3 . 1 0 . 0  
 m a t p l o t l i b - i n l i n e = = 0 . 1 . 7  
 m c c a b e = = 0 . 7 . 0  
 M e t a T r a d e r 5 = = 5 . 0 . 4 7 3 8  
 m i s t u n e = = 3 . 1 . 0  
 m y p y = = 1 . 1 5 . 0  
 m y p y - e x t e n s i o n s = = 1 . 0 . 0  
 n b c l i e n t = = 0 . 1 0 . 2  
 n b c o n v e r t = = 7 . 1 6 . 5  
 n b f o r m a t = = 5 . 1 0 . 4  
 n e s t - a s y n c i o = = 1 . 6 . 0  
 n o t e b o o k = = 7 . 3 . 2  
 n o t e b o o k _ s h i m = = 0 . 2 . 4  
 n u m p y = = 2 . 2 . 1  
 o p e n p y x l = = 3 . 1 . 5  
 o v e r r i d e s = = 7 . 7 . 0  
 p a c k a g i n g = = 2 4 . 2  
 p a n d a s = = 2 . 2 . 3  
 p a n d o c f i l t e r s = = 1 . 5 . 1  
 p a r s o = = 0 . 8 . 4  
 p a t h s p e c = = 0 . 1 2 . 1  
 p i l l o w = = 1 1 . 1 . 0  
 p l a t f o r m d i r s = = 4 . 3 . 6  
 p r o m e t h e u s _ c l i e n t = = 0 . 2 1 . 1  
 p r o m p t _ t o o l k i t = = 3 . 0 . 4 8  
 p s u t i l = = 6 . 1 . 1  
 p u r e _ e v a l = = 0 . 2 . 3  
 p y c p a r s e r = = 2 . 2 2  
 P y g m e n t s = = 2 . 1 9 . 1  
 p y l i n t = = 3 . 3 . 4  
 p y p a r s i n g = = 3 . 2 . 1  
 p y t h o n - d a t e u t i l = = 2 . 9 . 0 . p o s t 0  
 p y t h o n - j s o n - l o g g e r = = 3 . 2 . 1  
 p y t z = = 2 0 2 4 . 2  
 p y w i n 3 2 = = 3 0 8  
 p y w i n p t y = = 2 . 0 . 1 4  
 P y Y A M L = = 6 . 0 . 2  
 p y z m q = = 2 6 . 2 . 0  
 r e f e r e n c i n g = = 0 . 3 5 . 1  
 r e q u e s t s = = 2 . 3 2 . 3  
 r f c 3 3 3 9 - v a l i d a t o r = = 0 . 1 . 4  
 r f c 3 9 8 6 - v a l i d a t o r = = 0 . 1 . 1  
 r p d s - p y = = 0 . 2 2 . 3  
 S e n d 2 T r a s h = = 1 . 8 . 3  
 s e t u p t o o l s = = 7 5 . 8 . 0  
 s i x = = 1 . 1 7 . 0  
 s n i f f i o = = 1 . 3 . 1  
 s o u p s i e v e = = 2 . 6  
 s t a c k - d a t a = = 0 . 6 . 3  
 t e r m i n a d o = = 0 . 1 8 . 1  
 t i n y c s s 2 = = 1 . 4 . 0  
 t o m l k i t = = 0 . 1 3 . 2  
 t o r n a d o = = 6 . 4 . 2  
 t q d m = = 4 . 6 7 . 1  
 t r a i t l e t s = = 5 . 1 4 . 3  
 t y p e s - p y t h o n - d a t e u t i l = = 2 . 9 . 0 . 2 0 2 4 1 2 0 6  
 t y p i n g _ e x t e n s i o n s = = 4 . 1 2 . 2  
 t z d a t a = = 2 0 2 4 . 2  
 u r i - t e m p l a t e = = 1 . 3 . 0  
 u r l l i b 3 = = 2 . 3 . 0  
 w c w i d t h = = 0 . 2 . 1 3  
 w e b c o l o r s = = 2 4 . 1 1 . 1  
 w e b e n c o d i n g s = = 0 . 5 . 1  
 w e b s o c k e t - c l i e n t = = 1 . 8 . 0  
 w i d g e t s n b e x t e n s i o n = = 4 . 0 . 1 3  
 X l s x W r i t e r = = 3 . 2 . 2  
 ```

-----------

Path: Sophy_temp/run.py

```python
# run.py
# !/usr/bin/env python3
import argparse
import os
import sys
from datetime import datetime


def setup_environment():
    """Zet de omgeving op voor het uitvoeren van de applicatie"""
    # Voeg de huidige directory toe aan het pythonpath
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Sophy Trading Bot')
    parser.add_argument('--config', type=str, help='Pad naar configuratiebestand')
    parser.add_argument('--backtest', action='store_true', help='Voer backtest uit in plaats van live trading')
    parser.add_argument('--strategy', type=str, help='Te gebruiken strategie')
    parser.add_argument('--symbols', type=str, help='Komma-gescheiden lijst van symbolen')

    return parser.parse_args()


def main():
    """Main entry point for the application"""
    print(f"Sophy Trading Bot - Gestart op {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Setup environment
    setup_environment()

    # Parse arguments
    args = parse_arguments()

    # Set config path if provided
    if args.config:
        os.environ['SOPHY_CONFIG_PATH'] = args.config
        print(f"Gebruik configuratiebestand: {args.config}")

    # Override strategy if provided
    if args.strategy:
        print(f"Overschrijven strategie: {args.strategy}")
        # Dit wordt later in het programma verwerkt

    # Override symbols if provided
    if args.symbols:
        symbols = args.symbols.split(',')
        print(f"Overschrijven symbolen: {symbols}")
        # Dit wordt later in het programma verwerkt

    # Run in backtest mode or live mode
    if args.backtest:
        print("Starten in backtest modus")
        from src.analysis.backtester import run_backtest
        run_backtest()
    else:
        print("Starten in live trading modus")
        from src.main import main as run_live
        run_live()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgramma onderbroken door gebruiker")
        sys.exit(0)
    except Exception as e:
        print(f"\nOnverwachte fout: {str(e)}")
        sys.exit(1)
```

-----------

Path: Sophy_temp/scripts/__init__.py

```python
```

-----------

Path: Sophy_temp/scripts/ftmo_check.py

```python
import json
import os
import sys

from utils.ftmo_helper import FTMOHelper


def load_config(config_path):
    """Laad configuratie uit JSON bestand"""
    try:
        with open(config_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Configuratiebestand niet gevonden: {config_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Ongeldige JSON in configuratiebestand: {config_path}")
        sys.exit(1)


def main():
    print("\n==== FTMO Compliance Checker ====")
    print("Dit programma controleert of je trading prestaties voldoen aan de FTMO regels.")

    # Controleer of logbestand bestaat
    log_file = os.path.join('../logs', 'trading_journal.csv')
    if not os.path.exists(log_file):
        print(f"\nError: Log bestand niet gevonden: {log_file}")
        print("Voer eerst de TurtleTrader bot uit om trading data te genereren.")
        return

    # Laad configuratie voor initiële balans
    config_path = os.path.join('Sophy/config', 'settings.json')
    try:
        config = load_config(config_path)
        initial_balance = config['mt5'].get('account_balance', 100000)
    except:
        print("\nWaarschuwing: Kon configuratie niet laden, standaard account balans van $100,000 wordt gebruikt.")
        initial_balance = 100000

    print(f"\nAnalyseren van trading data met initiële balans: ${initial_balance:,.2f}")

    # Initialiseer FTMO helper
    ftmo_helper = FTMOHelper(log_file)

    # Genereer rapport
    print("\nGenereren van gedetailleerd FTMO compliance rapport...")
    ftmo_helper.generate_trading_report(initial_balance)

    print("\nWil je nog meer details zien? (j/n): ", end="")
    if input().lower() == 'j':
        # Voer meer gedetailleerde analyse uit
        compliance = ftmo_helper.check_ftmo_compliance(initial_balance)

        if compliance['details']:
            details = compliance['details']
            daily_stats = details['daily_stats']

            print("\n===== Dagelijkse Statistieken =====")
            print(f"{'Datum':<12} {'Balance':<12} {'Dagelijkse P&L':<15} {'Drawdown':<12}")
            print("-" * 55)

            for _, row in daily_stats.iterrows():
                date_str = row['Date'].strftime('%Y-%m-%d')
                balance = f"${row['close_balance']:,.2f}"
                daily_pnl = f"${row['daily_pnl']:,.2f} ({row['daily_pnl_pct']:.2f}%)"
                drawdown = f"{row['daily_drawdown']:.2f}%"

                print(f"{date_str:<12} {balance:<12} {daily_pnl:<15} {drawdown:<12}")

            print("\nAls je voldoet aan alle FTMO regels, kun je doorgaan naar de volgende fase!")

    print("\nBedankt voor het gebruiken van de FTMO Compliance Checker.")


if __name__ == "__main__":
    main()
```

-----------

Path: Sophy_temp/scripts/main.py

```python
# src/main.py
import time
from datetime import datetime

from src.connector.mt5_connector import MT5Connector
from src.risk.risk_manager import RiskManager
from src.strategy.strategy_factory import StrategyFactory
from src.utils.config import load_config
from src.utils.logger import Logger


def main():
    """Hoofdfunctie voor de Sophy trading applicatie"""
    # Laad configuratie
    config = load_config()

    # Setup logging
    log_file = config['logging'].get('log_file', 'logs/trading_log.csv')
    logger = Logger(log_file)
    logger.log_info("====== Sophy Trading System ======")
    logger.log_info(f"Sessie gestart op {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Creëer componenten
    connector = MT5Connector(config['mt5'], logger)
    risk_manager = RiskManager(config['risk'], logger)

    # Verbind met MT5
    if not connector.connect():
        logger.log_info("Kon geen verbinding maken met MT5. Programma wordt afgesloten.", level="ERROR")
        return

    logger.log_info(f"Verbonden met MT5: {config['mt5']['server']}")

    # Haal strategie naam uit config
    strategy_name = config['strategy']['name']

    # Creëer strategie via factory
    try:
        strategy = StrategyFactory.create_strategy(strategy_name, connector, risk_manager, logger, config)
        logger.log_info(f"Strategie geladen: {strategy_name}")
    except ValueError as e:
        logger.log_info(f"Kon strategie '{strategy_name}' niet initialiseren: {str(e)}", level="ERROR")
        connector.disconnect()
        return

    # Hoofdloop
    try:
        logger.log_info("Trading loop gestart")

        # Log initiële account status
        account_info = connector.get_account_info()
        open_positions = strategy.get_open_positions() if hasattr(strategy, 'get_open_positions') else {}
        logger.log_status(account_info, open_positions)

        while True:
            # Verwerk symbolen volgens strategie
            for symbol in config['mt5']['symbols']:
                # Pas symbol mapping toe indien nodig
                symbol_map = config['mt5'].get('symbol_mapping', {})
                mapped_symbol = symbol_map.get(symbol, symbol)

                # Verwerk symbool
                strategy.process_symbol(mapped_symbol)

            # Controleer FTMO limieten
            account_info = connector.get_account_info()
            open_positions = strategy.get_open_positions() if hasattr(strategy, 'get_open_positions') else {}
            logger.log_status(account_info, open_positions)

            should_stop, reason = risk_manager.check_ftmo_limits(account_info)
            if should_stop:
                logger.log_info(f"Stop trading: {reason}")
                break

            # Wacht voor volgende cyclus
            interval = config.get('interval', 300)  # Default 5 minuten
            logger.log_info(f"Wacht {interval} seconden tot volgende cyclus")
            time.sleep(interval)

    except KeyboardInterrupt:
        logger.log_info("Trading gestopt door gebruiker.")
    except Exception as e:
        logger.log_info(f"Onverwachte fout: {str(e)}", level="ERROR")
    finally:
        # Cleanup
        connector.disconnect()
        logger.log_info("Sessie afgesloten.")


if __name__ == "__main__":
    main()
```

-----------

Path: Sophy_temp/setup.py

```python
# setup.py
from setuptools import setup, find_packages

setup(
    name="sophy",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.20.0",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "MetaTrader5>=5.0.0",
    ],
    author="Sophy Trading Systems",
    author_email="info@sophytrading.com",
    description="Een Python-gebaseerd algoritmisch trading systeem met Turtle Trading strategie",
    keywords="trading, algoritm, metatrader, ftmo, turtle",
    url="https://github.com/yourusername/sophy",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.9",
)
```

-----------

Path: Sophy_temp/src/__init__.py

```python
```

-----------

Path: Sophy_temp/src/analysis/__init__.py

```python
```

-----------

Path: Sophy_temp/src/analysis/backtester.py

```python
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.strategy.strategy_factory import StrategyFactory
from src.utils.config import load_config
from src.utils.logger import Logger


class DummyConnector:
    """Dummy connector voor backtest doeleinden met geavanceerde datahandling."""

    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.data_cache: Dict[str, pd.DataFrame] = {}

    def get_historical_data(self, symbol: str, timeframe_str: str, bars_count: int) -> pd.DataFrame:
        """Haal historische data op uit CSV bestanden met caching."""
        cache_key = f"{symbol}_{timeframe_str}"
        if cache_key in self.data_cache:
            df = self.data_cache[cache_key]
            return df.iloc[-bars_count:] if len(df) > bars_count else df.copy()

        filename = f"{symbol}_{timeframe_str}.csv"
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.exists(filepath):
            print(f"Bestand niet gevonden: {filepath}")
            return pd.DataFrame()

        df = pd.read_csv(filepath)
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        elif 'time' in df.columns:
            df['date'] = pd.to_datetime(df['time'])
            df.drop('time', axis=1, inplace=True)

        df.columns = [col.lower() for col in df.columns]
        required_cols = {'open', 'high', 'low', 'close', 'tick_volume'}
        if not all(col in df.columns for col in required_cols):
            print(f"Ongeldige data voor {symbol}: ontbrekende kolommen")
            return pd.DataFrame()

        self.data_cache[cache_key] = df
        return df.iloc[-bars_count:] if len(df) > bars_count else df.copy()

    def get_symbol_tick(self, symbol: str) -> Optional[Any]:
        """Simuleer huidige tick gebaseerd op laatste data."""
        cache_key = f"{symbol}_H4"
        if cache_key not in self.data_cache:
            self.get_historical_data(symbol, "H4", 1000)

        if cache_key not in self.data_cache:
            return None

        df = self.data_cache[cache_key]
        last_row = df.iloc[-1]

        class Tick:
            pass

        tick = Tick()
        tick.ask = last_row['close']
        tick.bid = last_row['close'] * 0.999  # Simpele bid/ask spread
        tick.time = last_row['date'].timestamp()
        return tick

    def get_account_info(self) -> Dict[str, Any]:
        """Geef geüpdatete accountinformatie tijdens backtest."""
        return {
            'balance': 100000,
            'equity': 100000,
            'margin': 0,
            'free_margin': 100000,
            'margin_level': 0,
            'profit': 0
        }

    def get_open_positions(self, symbol: Optional[str] = None) -> List[Dict]:
        """Geef open posities terug."""
        return [pos for pos in self.open_positions.values()] if symbol is None else \
            [pos for pos in self.open_positions.values() if pos.get('symbol') == symbol]

    def place_order(self, action: str, symbol: str, volume: float, stop_loss: float, take_profit: float,
                    comment: str) -> Optional[int]:
        """Simuleer het plaatsen van een order."""
        if action not in ['BUY', 'SELL']:
            return None
        ticket = len(self.open_positions) + 1
        self.open_positions[ticket] = {
            'ticket': ticket,
            'symbol': symbol,
            'type': mt5.POSITION_TYPE_BUY if action == 'BUY' else mt5.POSITION_TYPE_SELL,
            'volume': volume,
            'price_open': self.get_symbol_tick(symbol).ask if action == 'BUY' else self.get_symbol_tick(symbol).bid,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'time': datetime.now().timestamp(),
            'profit': 0.0
        }
        return ticket

    def modify_position(self, ticket: int, stop_loss: float, take_profit: float) -> bool:
        """Simuleer het aanpassen van een positie."""
        if ticket in self.open_positions:
            self.open_positions[ticket]['stop_loss'] = stop_loss
            self.open_positions[ticket]['take_profit'] = take_profit
            return True
        return False

    open_positions = {}


class BacktestStrategy:
    """Wrapper voor strategie tijdens backtesting met geavanceerde logica."""

    def __init__(self, strategy, initial_balance: float = 100000):
        self.strategy = strategy
        self.balance = initial_balance
        self.equity = initial_balance
        self.positions: Dict[int, Dict] = {}
        self.trades: List[Dict] = []
        self.logger = self.strategy.logger  # Gebruik de logger van de strategie

    def process_candle(self, symbol: str, candle: Dict[str, Any]) -> Dict[str, Any]:
        """Verwerk een enkele candle en simuleer trades."""
        result = {'signal': None, 'action': None}
        candle_df = pd.DataFrame([candle])
        indicators = self.strategy.calculate_indicators(candle_df)

        # Simuleer tick-gebaseerde data
        tick = self.strategy.connector.get_symbol_tick(symbol)
        if tick is None:
            return result

        process_result = self.strategy.process_symbol(symbol)
        if process_result.get('signal') == 'ENTRY' and process_result.get('action'):
            action = process_result['action']
            volume = process_result.get('volume', 0.1)
            stop_loss = process_result.get('stop_loss', 0)
            ticket = self.strategy.connector.place_order(action, symbol, volume, stop_loss, 0, "Backtest Trade")
            if ticket:
                self.positions[ticket] = {
                    'symbol': symbol,
                    'action': action,
                    'volume': volume,
                    'entry_price': tick.ask if action == 'BUY' else tick.bid,
                    'stop_loss': stop_loss,
                    'open_time': datetime.fromtimestamp(tick.time)
                }
                self.logger.log_trade(symbol, action, tick.ask, volume, stop_loss, 0, "Backtest Entry")
                result.update(process_result)

        # Beheer open posities
        for ticket, pos in list(self.positions.items()):
            current_price = tick.ask if pos['action'] == 'BUY' else tick.bid
            profit = (current_price - pos['entry_price']) * pos['volume'] * (1 if pos['action'] == 'BUY' else -1)
            pos['profit'] = profit
            self.equity = self.balance + sum(p['profit'] for p in self.positions.values())

            # Simuleer stop loss
            if (pos['action'] == 'BUY' and current_price <= pos['stop_loss']) or \
                    (pos['action'] == 'SELL' and current_price >= pos['stop_loss']):
                self.close_position(ticket, current_price)
                result['signal'] = 'EXIT'
                result['action'] = 'CLOSE'

        return result

    def close_position(self, ticket: int, close_price: float):
        """Sluit een positie en update balans."""
        if ticket in self.positions:
            pos = self.positions[ticket]
            profit = (close_price - pos['entry_price']) * pos['volume'] * (1 if pos['action'] == 'BUY' else -1)
            self.balance += profit
            self.trades.append({
                'symbol': pos['symbol'],
                'action': pos['action'],
                'entry_price': pos['entry_price'],
                'exit_price': close_price,
                'volume': pos['volume'],
                'profit': profit,
                'open_time': pos['open_time'],
                'close_time': datetime.now()
            })
            self.logger.log_trade(pos['symbol'], 'SELL' if pos['action'] == 'BUY' else 'BUY', close_price,
                                  pos['volume'], 0, 0, f"Backtest Exit, Profit: {profit:.2f}")
            del self.positions[ticket]


def run_backtest():
    """Voer een geavanceerde backtest uit met configuratie en analyse."""
    print("Backtester module gestart")

    # Laad configuratie
    config = load_config()

    # Setup logger
    log_file = config['logging'].get('log_file', 'logs/backtest_log.csv')
    logger = Logger(log_file)
    logger.log_info("====== Sophy Backtest Started ======")

    # Haal symbols en timeframe op
    symbols = config['mt5'].get('symbols', ['EURUSD'])
    timeframe = config['mt5'].get('timeframe', 'H4')
    start_date = config.get('backtest', {}).get('start_date',
                                                (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d'))
    end_date = config.get('backtest', {}).get('end_date', datetime.now().strftime('%Y-%m-%d'))

    # Setup dummy connector
    data_dir = config.get('data_dir', 'data')
    connector = DummyConnector(data_dir)
    connector.open_positions = {}  # Initialiseer open posities

    # Laad data
    data = {}
    for symbol in symbols:
        df = connector.get_historical_data(symbol, timeframe, 10000)
        if not df.empty:
            df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
            data[symbol] = df
            logger.log_info(
                f"Geladen: {symbol} {timeframe} - {len(df)} candles van {df['date'].min()} tot {df['date'].max()}")
        else:
            logger.log_info(f"Kon geen data laden voor {symbol} {timeframe}", level="ERROR")
            continue

    if not data:
        logger.log_info("Geen data geladen, backtest gestopt", level="ERROR")
        return

    # Maak strategie aan
    strategy_name = config['strategy'].get('name', 'turtle')
    strategy = StrategyFactory.create_strategy(strategy_name, connector, None, logger, config)
    if not strategy:
        logger.log_info(f"Kon strategie {strategy_name} niet aanmaken", level="ERROR")
        return

    backtest = BacktestStrategy(strategy)
    equity_curve = []

    # Voer backtest uit
    for symbol, df in data.items():
        for _, candle in df.iterrows():
            candle_dict = candle.to_dict()
            result = backtest.process_candle(symbol, candle_dict)
            equity_curve.append(backtest.equity)

            # Log status
            account_info = connector.get_account_info()
            account_info['equity'] = backtest.equity
            account_info['balance'] = backtest.balance
            logger.log_status(account_info, connector.get_open_positions())

    # Analyseer resultaten
    total_profit = backtest.balance - 100000
    trades = len(backtest.trades)
    winning_trades = sum(1 for t in backtest.trades if t['profit'] > 0)
    win_rate = (winning_trades / trades * 100) if trades > 0 else 0
    avg_profit = np.mean([t['profit'] for t in backtest.trades if t['profit'] > 0]) if winning_trades > 0 else 0
    avg_loss = np.mean([t['profit'] for t in backtest.trades if t['profit'] < 0]) if len(
        [t for t in backtest.trades if t['profit'] < 0]) > 0 else 0
    drawdown = min(0, min(equity_curve) - 100000) if equity_curve else 0

    logger.log_performance_metrics({
        'total_trades': trades,
        'winning_trades': winning_trades,
        'win_rate': win_rate,
        'avg_profit': avg_profit,
        'avg_loss': avg_loss,
        'total_profit': total_profit,
        'max_drawdown': drawdown,
        'trade_history': backtest.trades
    })

    # Visualiseer resultaten
    plt.figure(figsize=(12, 6))
    plt.plot(equity_curve, label='Equity Curve')
    plt.title(f'Backtest Resultaten - {strategy_name}')
    plt.xlabel('Candles')
    plt.ylabel('Equity')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(os.path.dirname(log_file), 'backtest_equity_curve.png'))
    plt.close()

    logger.log_info(
        f"Backtest voltooid. Totale winst: {total_profit:.2f}, Win Rate: {win_rate:.2f}%, Max Drawdown: {drawdown:.2f}")
    logger.log_info("====== Sophy Backtest Ended ======")


if __name__ == "__main__":
    run_backtest()
```

-----------

Path: Sophy_temp/src/analysis/optimizer.py

```python
# src/analysis/turtle_optimizer.py
import json
import logging
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union

import matplotlib.pyplot as plt

from src.analysis.advanced_backtester import Backtester
from src.utils.config import load_config
from src.utils.logger import Logger

# Configureer logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("turtle_optimizer")


class WalkForwardOptimizer:
    """
    Walk-Forward Optimalisatie voor handelssystemen om overfitting te voorkomen.

    Deze klasse implementeert walk-forward optimalisatie met verschillende in-sample/out-of-sample
    periodes om een robuustere set van parameters te vinden die goed generaliseert naar nieuwe data.
    """

    def __init__(self, config=None, logger=None):
        """
        Initialiseer de walk-forward optimizer.

        Parameters:
        -----------
        config : Optional[Dict]
            Configuratie dictionary (als None, dan wordt standaard config geladen)
        logger : Optional[Logger]
            Logger instantie (als None, dan wordt een nieuwe gemaakt)
        """
        self.config = config if config else load_config()
        self.logger = logger if logger else Logger(self.config['logging'].get('log_file', 'logs/optimizer_log.csv'))

        # Output directory
        self.output_dir = self.config.get('output', {}).get('data_dir', 'data/optimization')
        os.makedirs(self.output_dir, exist_ok=True)

        # Maak backtester
        self.backtester = Backtester(self.config, self.logger)

        # Visuele stijl instellen
        plt.style.use('ggplot')
        plt.rcParams['figure.figsize'] = (16, 10)

    def optimize(self, strategy_name: str, symbols: List[str], timeframe: str,
                 param_ranges: Dict[str, List[Any]],
                 start_date: Union[str, datetime], end_date: Union[str, datetime],
                 is_period_days: int = 180, oos_period_days: int = 60,
                 windows: int = 3, metric: str = 'sharpe_ratio',
                 min_trades: int = 10, max_workers: Optional[int] = None) -> Dict[str, Any]:
        """
        Voer walk-forward optimalisatie uit.

        Parameters:
        -----------
        strategy_name : str
            Naam van de strategie
        symbols : List[str]
            Lijst met handelssymbolen
        timeframe : str
            Timeframe voor analyse
        param_ranges : Dict[str, List[Any]]
            Dictionary met parameter namen en mogelijke waarden
        start_date : Union[str, datetime]
            Start datum voor gehele test periode
        end_date : Union[str, datetime]
            Eind datum voor gehele test periode
        is_period_days : int
            Aantal dagen voor in-sample periode
        oos_period_days : int
            Aantal dagen voor out-of-sample periode
        windows : int
            Aantal walk-forward windows
        metric : str
            Prestatiemetric om te optimaliseren
        min_trades : int
            Minimum aantal trades voor een geldige test
        max_workers : Optional[int]
            Maximum aantal workers voor parallellisatie

        Returns:
        --------
        Dict[str, Any] : Resultaten van de walk-forward optimalisatie
        """
        self.logger.log_info(f"===== Starten Walk-Forward Optimalisatie: {strategy_name} =====")
        self.logger.log_info(f"Symbolen: {symbols}, Timeframe: {timeframe}")
        self.logger.log_info(f"Optimalisatie metric: {metric}")

        # Converteer data naar datetime
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # Bereken tijdsperiodes
        total_days = (end_date - start_date).days
        window_size = is_period_days + oos_period_days

        if windows * window_size > total_days:
            windows = total_days // window_size
            self.logger.log_info(f"Aangepast aantal windows naar {windows} om binnen datumbereik te passen")

        if windows < 1:
            self.logger.log_info("Datumbereik te klein voor walk-forward optimalisatie", level="ERROR")
            return {"success": False, "error": "Date range too small"}

        # Genereer datumvensters
        date_windows = []
        current_start = start_date

        for i in range(windows):
            is_end = current_start + timedelta(days=is_period_days)
            oos_end = is_end + timedelta(days=oos_period_days)

            if oos_end > end_date:
                oos_end = end_date

            date_windows.append({
                'window': i + 1,
                'is_start': current_start,
                'is_end': is_end,
                'oos_start': is_end,
                'oos_end': oos_end
            })

            current_start = is_end

        self.logger.log_info(f"Gegenereerd {len(date_windows)} walk-forward vensters")

        # Optimaliseer voor elk venster
        window_results = []
        oos_results = []
        best_params_per_window = []

        for window in date_windows:
            window_num = window['window']
            is_start = window['is_start'].strftime('%Y-%m-%d')
            is_end = window['is_end'].strftime('%Y-%m-%d')
            oos_start = window['oos_start'].strftime('%Y-%m-%d')
            oos_end = window['oos_end'].strftime('%Y-%m-%d')

            self.logger.log_info(f"Window {window_num}: In-sample {is_start} tot {is_end}, "
                                 f"Out-of-sample {oos_start} tot {oos_end}")

            # In-sample optimalisatie
            self.logger.log_info(f"In-sample optimalisatie voor window {window_num}...")

            is_results = self.backtester.run_optimization(
                strategy_name=strategy_name,
                symbols=symbols,
                param_ranges=param_ranges,
                start_date=is_start,
                end_date=is_end,
                metric=metric,
                max_workers=max_workers
            )

            window_results.append(is_results)

            if not is_results['success']:
                self.logger.log_info(f"In-sample optimalisatie mislukt voor window {window_num}", level="ERROR")
                continue

            # Get best parameters
            best_params = is_results['best_parameters']
            best_metrics = is_results['best_metrics']

            self.logger.log_info(f"Beste parameters voor window {window_num}: {best_params}")
            self.logger.log_info(f"In-sample {metric}: {best_metrics.get(metric, 0):.4f}")

            # Valideer op out-of-sample periode
            self.logger.log_info(f"Out-of-sample validatie voor window {window_num}...")

            oos_result = self.backtester.run_backtest(
                strategy_name=strategy_name,
                symbols=symbols,
                timeframe=timeframe,
                start_date=oos_start,
                end_date=oos_end,
                parameters=best_params,
                plot_results=False
            )

            oos_results.append(oos_result)

            if not oos_result['success']:
                self.logger.log_info(f"Out-of-sample validatie mislukt voor window {window_num}", level="ERROR")
                continue

            oos_metrics = oos_result['metrics']

            self.logger.log_info(f"Out-of-sample {metric}: {oos_metrics.get(metric, 0):.4f}")
            self.logger.log_info(f"Out-of-sample net profit: {oos_metrics.get('net_profit_pct', 0):.2f}%")

            # Sla beste params op per window
            best_params_per_window.append({
                'window': window_num,
                'is_start': is_start,
                'is_end': is_end,
                'oos_start': oos_start,
                'oos_end': oos_end,
                'parameters': best_params,
                'is_metric': best_metrics.get(metric, 0),
                'oos_metric': oos_metrics.get(metric, 0),
                'is_profit': best_metrics.get('net_profit_pct', 0),
                'oos_profit': oos_metrics.get('net_profit_pct', 0),
                'is_trades': best_metrics.get('total_trades', 0),
                'oos_trades': oos_metrics.get('total_trades', 0)
            })

        # Analyseer walk-forward resultaten
        if not best_params_per_window:
            self.logger.log_info("Geen geldige resultaten voor analyse", level="ERROR")
            return {"success": False, "error": "No valid results"}

        # Bepaal de meest robuuste parameters
        robust_params = self._find_robust_parameters(best_params_per_window, param_ranges)

        # Valideer de robuuste parameters op de gehele periode
        self.logger.log_info(f"Valideren robuuste parameters {robust_params} op volledige periode...")

        full_result = self.backtester.run_backtest(
            strategy_name=strategy_name,
            symbols=symbols,
            timeframe=timeframe,
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d'),
            parameters=robust_params,
            plot_results=True
        )

        if full_result['success']:
            full_metrics = full_result['metrics']
            self.logger.log_info(f"Robuuste parameters validatie: {metric}={full_metrics.get(metric, 0):.4f}, "
                                 f"Net Profit={full_metrics.get('net_profit_pct', 0):.2f}%")

        # Visualiseer en sla resultaten op
        self._plot_walk_forward_results(best_params_per_window, robust_params, metric)
        self._save_optimization_results(
            strategy_name, symbols, metric, best_params_per_window, robust_params, full_result
        )

        return {
            "success": True,
            "best_params_per_window": best_params_per_window,
            "robust_params": robust_params,
            "full_result": full_result,
            "metric": metric
        }

    def _find_robust_parameters(self, window_results: List[Dict], param_ranges: Dict[str, List[Any]]) -> Dict[str, Any]:
        """
        Vind robuuste parameters die goed werken over meerdere periodes.

        Parameters:
        -----------
        window_results : List[Dict]
            Resultaten per window
        param_ranges : Dict[str, List[Any]]
            Mogelijke parameter waarden

        Returns:
        --------
        Dict[str, Any] : Meest robuuste parameterset
        """
        if not window_results:
            return {}

        # Extraheer parameter keys
        param_keys = list(param_ranges.keys())

        # Bereken hoe vaak elke parameter waarde voorkomt
        param_frequency = {param: {} for param in param_keys}

        for result in window_results:
            params = result['parameters']

            for param, value in params.items():
                if param in param_keys:
                    param_frequency[param][value] = param_frequency[param].get(value, 0) + 1

        # Kies de meest voorkomende waarde voor elke parameter
        robust_params = {}

        for param, freq in param_frequency.items():
            if freq:
                # De meest voorkomende waarde
                most_common = max(freq.items(), key=lambda x: x[1])[0]
                robust_params[param] = most_common
            else:
                # Fallback: gemiddelde waarde uit bereik
                values = param_ranges[param]
                if values and all(isinstance(v, (int, float)) for v in values):
                    robust_params[param] = sum(values) / len(values)
                elif values:
                    robust_params[param] = values[0]  # Eerste waarde als fallback

        return robust_params

    def _plot_walk_forward_results(self, window_results: List[Dict],
                                   robust_params: Dict[str, Any], metric: str) -> str:
        """
        Visualiseer walk-forward optimalisatie resultaten.

        Parameters:
        -----------
        window_results : List[Dict]
            Resultaten per window
        robust_params : Dict[str, Any]
            Meest robuuste parameterset
        metric : str
            Optimalisatiemetric

        Returns:
        --------
        str : Pad naar opgeslagen plot
        """
        if not window_results:
            return ""

        # Maak een figuur met 3 subplots
        fig, axs = plt.subplots(3, 1, figsize=(14, 16), gridspec_kw={'height_ratios': [2, 1, 2]})

        # 1. Plot IS vs OOS performance
        windows = [r['window'] for r in window_results]
        is_metrics = [r['is_metric'] for r in window_results]
        oos_metrics = [r['oos_metric'] for r in window_results]

        axs[0].plot(windows, is_metrics, 'b-', marker='o', label=f'In-Sample {metric}')
        axs[0].plot(windows, oos_metrics, 'r-', marker='x', label=f'Out-of-Sample {metric}')

        axs[0].set_title(f'Walk-Forward Optimalisatie: {metric} per Window', fontsize=16)
        axs[0].set_xlabel('Window #', fontsize=14)
        axs[0].set_ylabel(metric, fontsize=14)
        axs[0].grid(True)
        axs[0].legend(fontsize=12)

        # 2. Plot Profit
        is_profit = [r['is_profit'] for r in window_results]
        oos_profit = [r['oos_profit'] for r in window_results]

        axs[1].plot(windows, is_profit, 'g-', marker='o', label='In-Sample Profit %')
        axs[1].plot(windows, oos_profit, 'm-', marker='x', label='Out-of-Sample Profit %')

        axs[1].set_title('Net Profit % per Window', fontsize=16)
        axs[1].set_xlabel('Window #', fontsize=14)
        axs[1].set_ylabel('Net Profit %', fontsize=14)
        axs[1].grid(True)
        axs[1].legend(fontsize=12)

        # 3. Parameter consistency plot
        param_keys = list(robust_params.keys())

        if param_keys:
            param_values = {param: [] for param in param_keys}

            for result in window_results:
                for param in param_keys:
                    param_values[param].append(result['parameters'].get(param, None))

            # Normalize for plotting
            normalized_values = {}
            for param, values in param_values.items():
                if all(isinstance(v, (int, float)) for v in values if v is not None):
                    min_val = min(v for v in values if v is not None)
                    max_val = max(v for v in values if v is not None)

                    if max_val > min_val:
                        normalized_values[param] = [(v - min_val) / (max_val - min_val) if v is not None else None for v
                                                    in values]
                    else:
                        normalized_values[param] = [0.5 if v is not None else None for v in values]
                else:
                    # Categorische waarden
                    unique_values = list(set(v for v in values if v is not None))
                    normalized_values[param] = [
                        unique_values.index(v) / max(1, len(unique_values) - 1) if v in unique_values else None for v in
                        values]

            # Plot normalized parameters
            for param, values in normalized_values.items():
                valid_points = [(i, v) for i, v in enumerate(values, 1) if v is not None]
                if valid_points:
                    x, y = zip(*valid_points)
                    axs[2].plot(x, y, 'o-', label=param)

            axs[2].set_title('Parameter Consistency Across Windows', fontsize=16)
            axs[2].set_xlabel('Window #', fontsize=14)
            axs[2].set_ylabel('Normalized Parameter Value', fontsize=14)
            axs[2].grid(True)
            axs[2].legend(fontsize=12)

            # Voeg robuuste parameters toe als text box
            param_text = "Robust Parameters:\n" + "\n".join([f"{k}: {v}" for k, v in robust_params.items()])
            axs[2].text(0.02, 0.02, param_text, transform=axs[2].transAxes, fontsize=12,
                        bbox=dict(facecolor='white', alpha=0.7), verticalalignment='bottom')

        plt.tight_layout()

        # Sla plot op
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"walk_forward_results_{timestamp}.png")
        plt.savefig(output_path, dpi=150)
        plt.close()

        return output_path

    def _save_optimization_results(self, strategy_name: str, symbols: List[str],
                                   metric: str, window_results: List[Dict],
                                   robust_params: Dict[str, Any], full_result: Dict) -> str:
        """
        Sla optimalisatie resultaten op in JSON formaat.

        Parameters:
        -----------
        strategy_name : str
            Naam van de strategie
        symbols : List[str]
            Lijst met handelssymbolen
        metric : str
            Optimalisatiemetric
        window_results : List[Dict]
            Resultaten per window
        robust_params : Dict[str, Any]
            Meest robuuste parameterset
        full_result : Dict
            Resultaat van backtest met robuuste parameters

        Returns:
        --------
        str : Pad naar opgeslagen resultaten
        """
        # Maak resultaten dictionary
        results = {
            'strategy': strategy_name,
            'symbols': symbols,
            'metric': metric,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'window_results': window_results,
            'robust_params': robust_params,
            'full_metrics': full_result.get('metrics', {}) if full_result.get('success', False) else {}
        }

        # Sla op als JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"walk_forward_{strategy_name}_{timestamp}.json")

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, default=str)

        self.logger.log_info(f"Walk-forward resultaten opgeslagen als {output_path}")
        return output_path


class BayesianOptimizer:
    """
    Bayesiaanse Optimalisatie voor het efficiënt zoeken naar optimale strategie parameters.

    Deze klasse implementeert Bayesiaanse optimalisatie om efficiënter dan grid search
    optimale parameters te vinden door een surrogaat model te gebruiken.
    """

    def __init__(self, config=None, logger=None):
        """
        Initialiseer de Bayesiaanse optimizer.

        Parameters:
        -----------
        config : Optional[Dict]
            Configuratie dictionary (als None, dan wordt standaard config geladen)
        logger : Optional[Logger]
            Logger instantie (als None, dan wordt een nieuwe gemaakt)
        """
        self.config = config if config else load_config()
        self.logger = logger if logger else Logger(self.config['logging'].get('log_file', 'logs/bayesian_opt_log.csv'))

        # Output directory
        self.output_dir = self.config.get('output', {}).get('data_dir', 'data/optimization')
        os.makedirs(self.output_dir, exist_ok=True)

        # Maak backtester
        self.backtester = Backtester(self.config, self.logger)

        try:
            # Probeer scikit-optimize te importeren
            import skopt
            self.skopt_available = True
        except ImportError:
            self.logger.log_info("scikit-optimize niet beschikbaar. Installeer met: pip install scikit-optimize",
                                 level="WARNING")
            self.skopt_available = False

        # Visuele stijl instellen
        plt.style.use('ggplot')
        plt.rcParams['figure.figsize'] = (16, 10)

    def optimize(self, strategy_name: str, symbols: List[str], timeframe: str,
                 param_space: Dict[str, Any], start_date: Union[str, datetime],
                 end_date: Union[str, datetime], n_calls: int = 30,
                 n_initial_points: int = 10, metric: str = 'sharpe_ratio') -> Dict[str, Any]:
        """
        Voer Bayesiaanse optimalisatie uit.

        Parameters:
        -----------
        strategy_name : str
            Naam van de strategie
        symbols : List[str]
            Lijst met handelssymbolen
        timeframe : str
            Timeframe voor analyse
        param_space : Dict[str, Any]
            Dictionary met parameter namen en bereiken:
            Bijvoorbeeld: {'entry_period': (10, 60), 'atr_multiplier': (1.0, 3.0)}
            Voor categorische: {'swing_mode': ['True', 'False']}
        start_date : Union[str, datetime]
            Start datum
        end_date : Union[str, datetime]
            Eind datum
        n_calls : int
            Aantal evaluatiepunten
        n_initial_points : int
            Aantal initiële random punten
        metric : str
            Prestatiemetric om te optimaliseren (bijv. 'sharpe_ratio', 'profit_factor', etc.)

        Returns:
        --------
        Dict[str, Any] : Resultaten van de optimalisatie
        """
        if not self.skopt_available:
            self.logger.log_info("Kan Bayesiaanse optimalisatie niet uitvoeren zonder scikit-optimize", level="ERROR")
            return {"success": False, "error": "scikit-optimize not available"}

        import skopt
        from skopt import gp_minimize
        from skopt.space import Real, Integer, Categorical
        from skopt.utils import use_named_args

        self.logger.log_info(f"===== Starten Bayesiaanse Optimalisatie: {strategy_name} =====")
        self.logger.log_info(f"Symbolen: {symbols}, Timeframe: {timeframe}")
        self.logger.log_info(f"Optimalisatie metric: {metric}")

        # Definieer parameter space in skopt formaat
        dimensions = []
        dimension_names = []

        for param_name, param_def in param_space.items():
            dimension_names.append(param_name)

            if isinstance(param_def, tuple) and len(param_def) == 2:
                low, high = param_def
                if isinstance(low, int) and isinstance(high, int):
                    dimensions.append(Integer(low, high, name=param_name))
                elif isinstance(low, (int, float)) and isinstance(high, (int, float)):
                    dimensions.append(Real(low, high, name=param_name))
            elif isinstance(param_def, list):
                dimensions.append(Categorical(param_def, name=param_name))

        # Conversie van strings naar booleans voor categorische opties
        def process_param_value(param_name, value):
            if param_name in param_space and isinstance(param_space[param_name], list):
                if value == 'True':
                    return True
                elif value == 'False':
                    return False
            return value

        # Definieer evaluatiefunctie
        @use_named_args(dimensions=dimensions)
        def evaluate_params(**params):
            # Converteer categoriën indien nodig
            processed_params = {
                name: process_param_value(name, value)
                for name, value in params.items()
            }

            self.logger.log_info(f"Evalueren parameters: {processed_params}")

            try:
                result = self.backtester.run_backtest(
                    strategy_name=strategy_name,
                    symbols=symbols,
                    timeframe=timeframe,
                    start_date=start_date,
                    end_date=end_date,
                    parameters=processed_params,
                    plot_results=False
                )

                if not result['success']:
                    return -100  # Penalty voor mislukte backtests

                metrics = result['metrics']

                # We minimaliseren, dus negeer de metric
                metric_value = metrics.get(metric, 0)

                if metric in ['sharpe_ratio', 'profit_factor', 'net_profit', 'net_profit_pct', 'win_rate']:
                    return -metric_value  # Negeer omdat we maximaliseren
                else:
                    return metric_value  # Voor metrics die we minimaliseren

            except Exception as e:
                self.logger.log_info(f"Fout bij evalueren parameters: {str(e)}", level="ERROR")
                return -100  # Penalty voor errors

        # Voer optimalisatie uit
        start_time = time.time()

        result = gp_minimize(
            evaluate_params,
            dimensions=dimensions,
            n_calls=n_calls,
            n_initial_points=n_initial_points,
            acq_func='EI',  # Expected Improvement
            noise=0.01,
            verbose=True
        )

        elapsed = time.time() - start_time
        self.logger.log_info(f"Optimalisatie voltooid in {elapsed:.2f} seconden")

        # Analyseer resultaten
        best_params = dict(zip(dimension_names, result.x))

        # Converteer categoriën indien nodig
        best_params = {
            name: process_param_value(name, value)
            for name, value in best_params.items()
        }

        # Negatief van de score voor metrics die we maximaliseren
        best_score = -result.fun if metric in ['sharpe_ratio', 'profit_factor', 'net_profit', 'net_profit_pct',
                                               'win_rate'] else result.fun

        self.logger.log_info(f"Beste parameters gevonden: {best_params}")
        self.logger.log_info(f"Beste {metric}: {best_score:.4f}")

        # Run final backtest met beste parameters
        final_result = self.backtester.run_backtest(
            strategy_name=strategy_name,
            symbols=symbols,
            timeframe=timeframe,
            start_date=start_date,
            end_date=end_date,
            parameters=best_params,
            plot_results=True
        )

        # Visualiseer resultaten
        self._plot_optimization_results(result, dimension_names, metric)
        self._save_optimization_results(
            strategy_name, symbols, metric, result, dimension_names, best_params, final_result
        )

        return {
            "success": True,
            "best_parameters": best_params,
            "best_score": best_score,
            "optimization_result": result,
            "final_backtest": final_result
        }

    def _plot_optimization_results(self, result, dimension_names: List[str], metric: str) -> str:
        """
        Visualiseer optimalisatie resultaten.

        Parameters:
        -----------
        result : skopt.OptimizeResult
            Resultaat van de optimalisatie
        dimension_names : List[str]
            Namen van de dimensies (parameters)
        metric : str
            Optimalisatiemetric

        Returns:
        --------
        str : Pad naar opgeslagen plot
        """
        try:
            import skopt
            from skopt.plots import plot_convergence, plot_objective, plot_evaluations

            # Maak één figuur met 3 subplots
            fig, axs = plt.subplots(3, 1, figsize=(14, 18))

            # 1. Convergentie plot
            plot_convergence(result, ax=axs[0])
            if metric in ['sharpe_ratio', 'profit_factor', 'net_profit', 'net_profit_pct', 'win_rate']:
                # Converteer y-as labels voor metrics die we maximaliseren
                axs[0].set_ylabel(f"Negative {metric}")

            axs[0].set_title(f"Convergence Plot for {metric} Optimization", fontsize=16)

            # 2. Objective plot (alleen voor 1-2 dimensies)
            if len(dimension_names) <= 2:
                try:
                    plot_objective(result, ax=axs[1])
                    axs[1].set_title(f"Objective Surface for {metric}", fontsize=16)
                except Exception as e:
                    self.logger.log_info(f"Kon objective plot niet maken: {str(e)}", level="WARNING")
                    axs[1].set_visible(False)
            else:
                axs[1].set_visible(False)

            # 3. Evaluations plot
            try:
                plot_evaluations(result, ax=axs[2])
                axs[2].set_title("Parameter Evaluations", fontsize=16)
            except Exception as e:
                self.logger.log_info(f"Kon evaluations plot niet maken: {str(e)}", level="WARNING")
                axs[2].set_visible(False)

            plt.tight_layout()

            # Sla plot op
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(self.output_dir, f"bayesian_optimization_{timestamp}.png")
            plt.savefig(output_path, dpi=150)
            plt.close()

            return output_path

        except Exception as e:
            self.logger.log_info(f"Fout bij plotten optimalisatie resultaten: {str(e)}", level="ERROR")
            return ""

    def _save_optimization_results(self, strategy_name: str, symbols: List[str],
                                   metric: str, result, dimension_names: List[str],
                                   best_params: Dict[str, Any], final_result: Dict) -> str:
        """
        Sla optimalisatie resultaten op in JSON formaat.

        Parameters:
        -----------
        strategy_name : str
            Naam van de strategie
        symbols : List[str]
            Lijst met handelssymbolen
        metric : str
            Optimalisatiemetric
        result : skopt.OptimizeResult
            Resultaat van de optimalisatie
        dimension_names : List[str]
            Namen van de dimensies (parameters)
        best_params : Dict[str, Any]
            Beste gevonden parameters
        final_result : Dict
            Resultaat van backtest met beste parameters

        Returns:
        --------
        str : Pad naar opgeslagen resultaten
        """
        # Maak resultaten dictionary
        optimization_data = {
            'strategy': strategy_name,
            'symbols': symbols,
            'metric': metric,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'best_params': best_params,
            'best_score': -result.fun if metric in ['sharpe_ratio', 'profit_factor', 'net_profit', 'net_profit_pct',
                                                    'win_rate'] else result.fun,
            'function_calls': result.nfev,
            'full_metrics': final_result.get('metrics', {}) if final_result.get('success', False) else {}
        }

        # Voeg alle evaluaties toe
        evaluations = []
        for i, (x, y) in enumerate(zip(result.x_iters, result.func_vals)):
            evaluations.append({
                'iteration': i + 1,
                'parameters': dict(zip(dimension_names, x)),
                'score': -y if metric in ['sharpe_ratio', 'profit_factor', 'net_profit', 'net_profit_pct',
                                          'win_rate'] else y
            })

        optimization_data['evaluations'] = evaluations

        # Sla op als JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"bayesian_opt_{strategy_name}_{timestamp}.json")

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(optimization_data, f, indent=2, default=str)

        self.logger.log_info(f"Bayesiaanse optimalisatie resultaten opgeslagen als {output_path}")
        return output_path


def run_walk_forward_optimization():
    """Voer walk-forward optimalisatie uit vanaf command line."""
    print("Walk-Forward Optimalisatie module gestart")

    # Laad configuratie
    config = load_config()

    # Setup logger
    log_file = config['logging'].get('log_file', 'logs/wf_opt_log.csv')
    logger = Logger(log_file)
    logger.log_info("====== Sophy Walk-Forward Optimalisatie Started ======")

    # Initialiseer optimizer
    optimizer = WalkForwardOptimizer(config, logger)

    # Haal parameters op uit config
    symbols = config['mt5'].get('symbols', ['EURUSD'])
    timeframe = config['mt5'].get('timeframe', 'H4')
    strategy_name = config['strategy'].get('name', 'turtle')

    # Definieer parameter bereiken voor turtle strategy
    param_ranges = {
        'entry_period': [20, 40, 60],
        'exit_period': [10, 20, 30],
        'atr_period': [14, 20, 30],
        'atr_multiplier': [1.5, 2.0, 2.5, 3.0],
        'swing_mode': [True, False]
    }

    # Bereken start en einddatum
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365 * 2)  # 2 jaar data

    # Start optimalisatie
    results = optimizer.optimize(
        strategy_name=strategy_name,
        symbols=symbols,
        timeframe=timeframe,
        param_ranges=param_ranges,
        start_date=start_date,
        end_date=end_date,
        is_period_days=180,  # 6 maanden in-sample
        oos_period_days=60,  # 2 maanden out-of-sample
        windows=3,  # 3 windows
        metric='sharpe_ratio'
    )

    if results['success']:
        logger.log_info("Walk-Forward Optimalisatie voltooid")
        logger.log_info(f"Robuuste parameters gevonden: {results['robust_params']}")
    else:
        logger.log_info(f"Walk-Forward Optimalisatie mislukt: {results.get('error', 'Onbekende fout')}", level="ERROR")

    logger.log_info("====== Sophy Walk-Forward Optimalisatie Ended ======")


def run_bayesian_optimization():
    """Voer Bayesiaanse optimalisatie uit vanaf command line."""
    print("Bayesiaanse Optimalisatie module gestart")

    # Laad configuratie
    config = load_config()

    # Setup logger
    log_file = config['logging'].get('log_file', 'logs/bayes_opt_log.csv')
    logger = Logger(log_file)
    logger.log_info("====== Sophy Bayesiaanse Optimalisatie Started ======")

    # Initialiseer optimizer
    optimizer = BayesianOptimizer(config, logger)

    # Haal parameters op uit config
    symbols = config['mt5'].get('symbols', ['EURUSD'])
    timeframe = config['mt5'].get('timeframe', 'H4')
    strategy_name = config['strategy'].get('name', 'turtle')

    # Definieer parameter bereiken voor turtle strategy
    param_space = {
        'entry_period': (10, 60),
        'exit_period': (5, 30),
        'atr_period': (5, 30),
        'atr_multiplier': (1.0, 4.0),
        'swing_mode': ['True', 'False']
    }

    # Bereken start en einddatum
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)  # 1 jaar data

    # Start optimalisatie
    results = optimizer.optimize(
        strategy_name=strategy_name,
        symbols=symbols,
        timeframe=timeframe,
        param_space=param_space,
        start_date=start_date,
        end_date=end_date,
        n_calls=30,  # 30 evaluatiepunten
        n_initial_points=10,  # 10 initiële random punten
        metric='sharpe_ratio'
    )

    if results['success']:
        logger.log_info("Bayesiaanse Optimalisatie voltooid")
        logger.log_info(f"Beste parameters gevonden: {results['best_parameters']}")
        logger.log_info(f"Beste score: {results['best_score']:.4f}")
    else:
        logger.log_info(f"Bayesiaanse Optimalisatie mislukt: {results.get('error', 'Onbekende fout')}", level="ERROR")

    logger.log_info("====== Sophy Bayesiaanse Optimalisatie Ended ======")


if __name__ == "__main__":
    # Kies welke optimalisatiemethode je wilt uitvoeren
    run_walk_forward_optimization()
    # run_bayesian_optimization()  # Uncomment om Bayesiaanse optimalisatie uit te voeren
```

-----------

Path: Sophy_temp/src/connector/__init__.py

```python
```

-----------

Path: Sophy_temp/src/connector/mt5_connector.py

```python
# src/connector/mt5_connector.py
import time
from typing import Dict, List, Optional, Any

import MetaTrader5 as mt5
import pandas as pd


class MT5Connector:
    """Verzorgt alle interacties met het MetaTrader 5 platform"""

    def __init__(self, config: Dict[str, any], logger: any) -> None:
        """
        Initialiseer de MT5 connector met configuratie

        Args:
            config: Configuratie dictionary met MT5 connectie parameters
            logger: Logger instance voor het registreren van gebeurtenissen
        """
        self.config = config
        self.logger = logger
        self.connected = False
        self._initialize_error_messages()
        self.timeframe_map = {
            'M1': mt5.TIMEFRAME_M1,
            'M5': mt5.TIMEFRAME_M5,
            'M15': mt5.TIMEFRAME_M15,
            'M30': mt5.TIMEFRAME_M30,
            'H1': mt5.TIMEFRAME_H1,
            'H4': mt5.TIMEFRAME_H4,
            'D1': mt5.TIMEFRAME_D1,
            'W1': mt5.TIMEFRAME_W1,
            'MN1': mt5.TIMEFRAME_MN1
        }

    def _initialize_error_messages(self) -> None:
        """Initialiseer foutmeldingen voor MT5 verbinding"""
        self.error_messages = {
            10013: "Ongeldige parameters voor verbinding",
            10014: "Verkeerde login of wachtwoord",
            10015: "Verkeerde server opgegeven",
            10016: "MT5 niet geïnstalleerd of niet gevonden",
            10018: "Verbinding met de server mislukt",
            10019: "Geen respons van server"
        }

    def connect(self) -> bool:
        """
        Maak verbinding met MT5 met uitgebreide foutafhandeling

        Returns:
            bool: True als verbinding succesvol, False anders
        """
        # Controleer of MT5 al is geïnitialiseerd
        if mt5.terminal_info() is not None and self.connected:
            self.logger.log_info("Al verbonden met MT5")
            return True

        # Sluit eerder gemaakte verbindingen
        mt5.shutdown()

        # Initialiseer MT5
        self.logger.log_info(f"Verbinden met MT5 op pad: {self.config.get('mt5_pathway', 'standaard pad')}")
        init_result = mt5.initialize(
            path=self.config.get('mt5_pathway'),
            login=self.config.get('login'),
            password=self.config.get('password'),
            server=self.config.get('server')
        )

        if not init_result:
            error_code = mt5.last_error()
            error_message = self.error_messages.get(
                error_code, f"Onbekende MT5 error: {error_code}")
            self.logger.log_info(f"MT5 initialisatie mislukt: {error_message}", level="ERROR")
            return False

        # Controleer verbinding
        if not mt5.terminal_info():
            self.logger.log_info("MT5 terminal info niet beschikbaar", level="ERROR")
            return False

        # Verbinding gemaakt
        self.connected = True
        account_info = mt5.account_info()

        if account_info:
            self.logger.log_info(f"Verbonden met MT5 account: {account_info.login}, "
                                 f"Server: {account_info.server}, "
                                 f"Type: {account_info.trade_mode_description}")
            return True
        else:
            self.logger.log_info("Kon geen account info ophalen", level="ERROR")
            return False

    def disconnect(self) -> None:
        """Sluit verbinding met MT5"""
        if self.connected:
            mt5.shutdown()
            self.connected = False
            self.logger.log_info("Verbinding met MT5 afgesloten")

    def get_account_info(self) -> Dict[str, Any]:
        """
        Haal account informatie op van MT5

        Returns:
            Dict met account eigenschappen
        """
        if not self.connected:
            self.logger.log_info("Niet verbonden met MT5", level="ERROR")
            return {}

        account_info = mt5.account_info()
        if not account_info:
            self.logger.log_info("Kon account informatie niet ophalen", level="ERROR")
            return {}

        # Converteer naar dictionary
        result = {
            'login': account_info.login,
            'balance': account_info.balance,
            'equity': account_info.equity,
            'margin': account_info.margin,
            'free_margin': account_info.margin_free,
            'profit': account_info.profit,
            'margin_level': (account_info.equity / account_info.margin * 100
                             if account_info.margin > 0 else 0)
        }

        return result

    def get_timeframe_constant(self, timeframe_str: str) -> int:
        """
        Converteer timeframe string naar MT5 constante

        Args:
            timeframe_str: Timeframe als string (bijv. 'H4')

        Returns:
            MT5 timeframe constante
        """
        return self.timeframe_map.get(timeframe_str, mt5.TIMEFRAME_H4)

    def get_historical_data(self,
                            symbol: str,
                            timeframe_or_str: Any,
                            bars_count: int = 100) -> pd.DataFrame:
        """
        Haal historische prijsdata op met geoptimaliseerde verwerking

        Args:
            symbol: Handelssymbool
            timeframe_or_str: MT5 timeframe constante of string ('H4', etc.)
            bars_count: Aantal bars om op te halen

        Returns:
            pd.DataFrame: DataFrame met historische data
        """
        if not self.connected:
            self.logger.log_info("Niet verbonden met MT5", level="ERROR")
            return pd.DataFrame()

        # Converteer timeframe string naar constante indien nodig
        timeframe = timeframe_or_str
        if isinstance(timeframe_or_str, str):
            timeframe = self.get_timeframe_constant(timeframe_or_str)

        # Probeer data op te halen met retry mechanisme
        retries = 3
        for attempt in range(retries):
            rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars_count)

            if rates is not None and len(rates) > 0:
                break

            if attempt < retries - 1:
                self.logger.log_info(
                    f"Poging {attempt + 1} mislukt om data op te halen voor {symbol}, opnieuw proberen...")
                time.sleep(1)

        if rates is None or len(rates) == 0:
            self.logger.log_info(f"Kon geen historische data ophalen voor {symbol} na {retries} pogingen",
                                 level="ERROR")
            return pd.DataFrame()

        # Converteer naar pandas DataFrame en bereken extra kolommen
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')

        # Hernoem kolommen naar lowercase voor consistentie
        df.columns = [col.lower() for col in df.columns]

        # Rename 'time' kolom naar 'date' voor consistentie in strategie code
        df.rename(columns={'time': 'date'}, inplace=True)

        return df

    def get_symbol_tick(self, symbol: str) -> Optional[Any]:
        """
        Haal actuele tick data op voor een symbool

        Args:
            symbol: Handelssymbool

        Returns:
            mt5.Tick object of None bij fout
        """
        if not self.connected:
            self.logger.log_info("Niet verbonden met MT5", level="ERROR")
            return None

        tick = mt5.symbol_info_tick(symbol)

        if tick is None:
            error_code = mt5.last_error()
            self.logger.log_info(f"Kon geen tick informatie ophalen voor {symbol}. Error: {error_code}", level="ERROR")
            return None

        return tick

    def get_open_positions(self, symbol: Optional[str] = None) -> List[Any]:
        """
        Haal open posities op

        Args:
            symbol: Optioneel filter op symbool

        Returns:
            Lijst met open posities
        """
        if not self.connected:
            self.logger.log_info("Niet verbonden met MT5", level="ERROR")
            return []

        positions = []

        if symbol:
            positions = mt5.positions_get(symbol=symbol)
        else:
            positions = mt5.positions_get()

        if positions is None:
            error_code = mt5.last_error()
            # Als er geen posities zijn is dit geen error
            if error_code == 0:
                return []
            self.logger.log_info(f"Kon geen posities ophalen. Error: {error_code}", level="ERROR")
            return []

        return list(positions)

    def place_order(self,
                    action: str,
                    symbol: str,
                    volume: float,
                    stop_loss: float = 0,
                    take_profit: float = 0,
                    comment: str = "") -> Optional[int]:
        """
        Plaats een order op het MT5 platform

        Args:
            action: "BUY" of "SELL"
            symbol: Handelssymbool
            volume: Order volume in lots
            stop_loss: Stop loss prijs (0 = geen stop loss)
            take_profit: Take profit prijs (0 = geen take profit)
            comment: Order commentaar

        Returns:
            Order ticket ID of None bij fout
        """
        if not self.connected:
            self.logger.log_info("Niet verbonden met MT5", level="ERROR")
            return None

        # Haal symbool informatie op
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            self.logger.log_info(f"Kon geen informatie krijgen voor symbool {symbol}", level="ERROR")
            return None

        # Controleer of trading mogelijk is voor dit symbool
        if not symbol_info.visible or not symbol_info.trade_allowed:
            self.logger.log_info(f"Trading niet toegestaan voor {symbol}", level="ERROR")
            return None

        # Haal huidige prijs op
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            self.logger.log_info(f"Kon geen tick informatie ophalen voor {symbol}", level="ERROR")
            return None

        # Bepaal order type en prijs
        order_type = None
        price = None

        if action == "BUY":
            order_type = mt5.ORDER_TYPE_BUY
            price = tick.ask
        elif action == "SELL":
            order_type = mt5.ORDER_TYPE_SELL
            price = tick.bid
        else:
            self.logger.log_info(f"Ongeldige actie: {action}", level="ERROR")
            return None

        # Bereid order request voor
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": float(volume),
            "type": order_type,
            "price": price,
            "sl": float(stop_loss) if stop_loss > 0 else 0,
            "tp": float(take_profit) if take_profit > 0 else 0,
            "deviation": 10,  # prijsafwijking in punten
            "magic": 123456,  # magic number voor identificatie
            "comment": comment,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK
        }

        # Stuur order naar MT5
        self.logger.log_info(
            f"Order versturen: {action} {volume} {symbol} @ {price}, SL: {stop_loss}, TP: {take_profit}")
        result = mt5.order_send(request)

        if result is None:
            error_code = mt5.last_error()
            self.logger.log_info(f"Order verzenden mislukt. Error code: {error_code}", level="ERROR")
            return None

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            self.logger.log_info(f"Order mislukt. Retcode: {result.retcode}", level="ERROR")
            return None

        self.logger.log_info(f"Order succesvol geplaatst. Ticket: {result.order}")
        return result.order
```

-----------

Path: Sophy_temp/src/ftmo/__init__.py

```python
```

-----------

Path: Sophy_temp/src/ftmo/ftmo_helper.py

```python
import logging
import os
from typing import Dict

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class FTMOHelper:
    """Helper class for FTMO compliance checks and reporting"""

    def __init__(self, log_file: str, output_dir: str = 'data/ftmo_analysis'):
        self.log_file = log_file
        self.output_dir = output_dir

        os.makedirs(output_dir, exist_ok=True)

        # Configure visualization style
        plt.style.use('ggplot')
        plt.rcParams['figure.figsize'] = (16, 10)
        sns.set_style("whitegrid")

        # Logging setup
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        # FTMO rules
        self.ftmo_rules = {
            'profit_target': 0.10,
            'max_daily_loss': -0.05,  # Corrected sign
            'max_total_loss': -0.10,  # Corrected sign
            'min_trading_days': 4,
            'challenge_duration': 30,
            'verification_duration': 60
        }

    def load_trade_data(self) -> pd.DataFrame:
        """Load trading data from log file"""
        try:
            df = pd.read_csv(self.log_file)
            df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
            df['Date'] = df['Timestamp'].dt.date
            return df.dropna(subset=['Timestamp'])  # Verwijder rijen met foutieve timestamps
        except Exception as e:
            logging.error(f"Error loading trading data: {e}")
            return pd.DataFrame()

    def check_ftmo_compliance(self, initial_balance: float) -> Dict:
        """Check FTMO compliance with detailed analysis"""
        df = self.load_trade_data()
        if df.empty:
            return {'compliant': False, 'reason': 'No trading data available', 'details': {}}

        # Extract STATUS entries for balance tracking
        status_df = df[df['Type'] == 'STATUS'].copy()
        if status_df.empty:
            return {'compliant': False, 'reason': 'No account status data available', 'details': {}}

        # Convert balance to numeric
        status_df['Balance'] = pd.to_numeric(status_df['Balance'], errors='coerce')
        status_df.dropna(subset=['Balance'], inplace=True)

        # Compute daily balance statistics
        daily_status = status_df.groupby('Date').agg(
            min_balance=('Balance', 'min'),
            max_balance=('Balance', 'max'),
            close_balance=('Balance', 'last')
        ).reset_index()

        # Ensure we have data before proceeding
        if daily_status.empty:
            return {'compliant': False, 'reason': 'Insufficient balance data available', 'details': {}}

        # Calculate daily P&L and drawdowns
        daily_status['prev_close'] = daily_status['close_balance'].shift(1).fillna(initial_balance)
        daily_status['daily_pnl'] = daily_status['close_balance'] - daily_status['prev_close']
        daily_status['daily_pnl_pct'] = (daily_status['daily_pnl'] / daily_status['prev_close']) * 100
        daily_status['daily_drawdown'] = ((daily_status['min_balance'] - daily_status['prev_close'])
                                          / daily_status['prev_close']) * 100
        daily_status['peak'] = daily_status['close_balance'].cummax()
        daily_status['drawdown_from_peak'] = ((daily_status['close_balance'] - daily_status['peak'])
                                              / daily_status['peak']) * 100

        # Calculate key metrics
        max_drawdown = daily_status['drawdown_from_peak'].min()
        latest_balance = daily_status['close_balance'].iloc[-1]
        total_pnl = latest_balance - initial_balance
        total_pnl_pct = (total_pnl / initial_balance) * 100

        # Check trading days
        trade_df = df[df['Type'] == 'TRADE']
        unique_trading_days = trade_df['Date'].nunique()

        # Check FTMO rules compliance
        profit_target_met = total_pnl_pct >= self.ftmo_rules['profit_target'] * 100
        daily_loss_compliant = daily_status['daily_drawdown'].min() >= self.ftmo_rules['max_daily_loss'] * 100
        total_loss_compliant = max_drawdown >= self.ftmo_rules['max_total_loss'] * 100
        trading_days_compliant = unique_trading_days >= self.ftmo_rules['min_trading_days']

        compliant = profit_target_met and daily_loss_compliant and total_loss_compliant and trading_days_compliant

        # Generate reason for non-compliance if applicable
        reasons = []
        if not profit_target_met:
            reasons.append(f"Profit target not reached: {total_pnl_pct:.2f}% "
                           f"(target: {self.ftmo_rules['profit_target'] * 100}%)")
        if not daily_loss_compliant:
            worst_day_idx = daily_status['daily_drawdown'].idxmin()
            worst_day = daily_status.iloc[worst_day_idx]
            reasons.append(f"Daily loss limit exceeded: {worst_day['daily_drawdown']:.2f}% on {worst_day['Date']}")
        if not total_loss_compliant:
            reasons.append(f"Maximum drawdown exceeded: {max_drawdown:.2f}% "
                           f"(limit: {self.ftmo_rules['max_total_loss'] * 100}%)")
        if not trading_days_compliant:
            reasons.append(f"Insufficient trading days: {unique_trading_days} "
                           f"(minimum: {self.ftmo_rules['min_trading_days']})")

        reason = "; ".join(reasons) if reasons else "Complies with all FTMO rules"

        # Compile results
        details = {
            'initial_balance': initial_balance,
            'final_balance': latest_balance,
            'total_pnl': total_pnl,
            'total_pnl_pct': total_pnl_pct,
            'max_drawdown': max_drawdown,
            'trading_days': unique_trading_days,
            'daily_stats': daily_status.to_dict(orient='records')  # Converted for better JSON compatibility
        }

        return {
            'compliant': compliant,
            'reason': reason,
            'details': details
        }

    def generate_trading_report(self, initial_balance: float) -> bool:
        """Generate detailed FTMO trading report with visualizations"""
        try:
            results = self.check_ftmo_compliance(initial_balance)
            daily_status = pd.DataFrame(results['details'].get('daily_stats', []))

            if daily_status.empty:
                logging.warning("No data available for generating trading report.")
                return False

            # Plot balance over time
            plt.figure(figsize=(12, 6))
            plt.plot(daily_status['Date'], daily_status['close_balance'], marker='o', label='Balance')
            plt.fill_between(daily_status['Date'], daily_status['min_balance'], daily_status['max_balance'],
                             alpha=0.3, color='gray', label="Daily Range")
            plt.axhline(y=initial_balance, color='r', linestyle='--', label="Initial Balance")
            plt.title("Trading Balance Over Time")
            plt.xlabel("Date")
            plt.ylabel("Balance")
            plt.legend()
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Save the figure
            report_path = os.path.join(self.output_dir, "trading_report.png")
            plt.savefig(report_path)
            logging.info(f"Trading report saved at {report_path}")

            return True
        except Exception as e:
            logging.error(f"Error generating trading report: {e}")
            return False
```

-----------

Path: Sophy_temp/src/ftmo/ftmo_validator.py

```python
# src/ftmo/ftmo_validator.py

import os
import re
from datetime import datetime, date
from typing import Dict, Tuple, Optional, Any

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.utils.logger import Logger  # Importeer de Logger-klasse


class FTMOValidator:
    """Klasse om handelsactiviteit te valideren en analyseren volgens FTMO-regels."""

    def __init__(self, config: Dict[str, Any], log_file: str, output_dir: str = 'data/ftmo_analysis',
                 logger: Optional[Logger] = None) -> None:
        """
        Initialiseer de FTMO Validator met configuratie, logbestand en outputmap.

        Parameters:
        -----------
        config : Dict[str, Any]
            Configuratiedictionary met risicoparameters (bijv. initial_balance).
        log_file : str
            Pad naar het logbestand met handelsdata.
        output_dir : str, optional
            Map voor het opslaan van analyse-uitvoer (default: 'data/ftmo_analysis').
        logger : Logger, optional
            Logging-object voor het bijhouden van gebeurtenissen.
        """
        self.config = config
        self.logger = logger
        self.initial_balance = config['risk'].get('account_balance', 100000)
        # Haal startdatum uit config of bepaal uit logbestand
        self.start_date = datetime.strptime(config.get('ftmo', {}).get('start_date', date.today().strftime('%Y-%m-%d')),
                                            '%Y-%m-%d').date()
        self.trade_days = set()
        self.log_file = log_file
        self.output_dir = output_dir

        # Stel visualisatiestijl in
        plt.style.use('ggplot')
        plt.rcParams['figure.figsize'] = (16, 10)
        plt.rcParams['lines.linewidth'] = 1.5
        sns.set_style("whitegrid")

        # Maak outputmap aan als deze niet bestaat
        os.makedirs(output_dir, exist_ok=True)

        # FTMO-regels
        self.ftmo_rules = {
            'profit_target': 0.10,  # 10% winstdoel
            'max_daily_loss': 0.05,  # 5% maximale dagelijkse drawdown
            'max_total_loss': 0.10,  # 10% maximale totale drawdown
            'min_trading_days': 4,  # Minimaal 4 handelsdagen
            'challenge_duration': 30,  # Challenge-duur van 30 dagen
            'verification_duration': 60  # Verificatie-duur van 60 dagen
        }

    def load_trade_data(self) -> pd.DataFrame:
        """
        Laad handelsdata uit het logbestand.

        Returns:
        --------
        pandas.DataFrame
            DataFrame met handelsdata, of lege DataFrame bij fout.

        Raises:
        -------
        ValueError
            Als het logbestand ongeldig is.
        """
        try:
            if not os.path.exists(self.log_file):
                raise ValueError(f"Logbestand niet gevonden: {self.log_file}")
            df = pd.read_csv(self.log_file)
            if df.empty or 'Timestamp' not in df.columns:
                raise ValueError("Logbestand is leeg of ongeldig formaat")
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            df['Date'] = df['Timestamp'].dt.date
            if self.logger:
                self.logger.log_info(f"Handelsdata geladen uit {self.log_file}")
            return df
        except Exception as e:
            if self.logger:
                self.logger.log_info(f"Fout bij laden handelsdata: {e}", level="ERROR")
            return pd.DataFrame()

    def validate_account_state(self, account_info: Dict[str, float] = None) -> Tuple[bool, Optional[str]]:
        """
        Valideer de accountstatus volgens FTMO-regels.

        Args:
            account_info: Huidige accountinformatie (optioneel).

        Returns:
            Tuple[bool, Optional[str]]: (is_compliant, violation_reason).
        """
        df = self.load_trade_data()
        if df.empty:
            return False, "Geen handelsdata beschikbaar"

        status_df = df[df['Type'] == 'STATUS'].copy()
        if status_df.empty:
            return False, "Geen statusdata beschikbaar"

        # Extraheer balans
        if 'Balance' not in status_df.columns or status_df['Balance'].isna().all():
            def extract_balance(comment):
                if isinstance(comment, str) and 'Balance: ' in comment:
                    match = re.search(r'Balance:\s*([\d,.]+)', comment)
                    return float(match.group(1).replace(',', '')) if match else None
                return None

            status_df['Balance'] = status_df['Comment'].apply(extract_balance)

        if status_df['Balance'].isna().all():
            return False, "Geen balansdata beschikbaar"

        status_df['Balance'] = pd.to_numeric(status_df['Balance'], errors='coerce')
        daily_status = status_df.groupby('Date').agg(close_balance=('Balance', 'last')).reset_index()
        current_equity = daily_status['close_balance'].iloc[-1] if not daily_status.empty else self.initial_balance

        # Registreer handelsdag
        self.trade_days.update(df[df['Type'] == 'TRADE']['Date'].unique())

        # Bereken winst/verlies percentage
        profit_loss_pct = (current_equity - self.initial_balance) / self.initial_balance * 100

        # Controleer FTMO-regels
        if profit_loss_pct >= self.ftmo_rules['profit_target'] * 100:
            return True, "Winstdoel bereikt"

        if profit_loss_pct <= -self.ftmo_rules['max_daily_loss'] * 100:
            return False, "Dagelijkse verlieslimiet overschreden"

        if profit_loss_pct <= -self.ftmo_rules['max_total_loss'] * 100:
            return False, "Maximale drawdown overschreden"

        days_in_challenge = (date.today() - self.start_date).days
        if days_in_challenge >= self.ftmo_rules['challenge_duration'] - 2:
            unique_trading_days = len(self.trade_days)
            if unique_trading_days < self.ftmo_rules['min_trading_days']:
                return False, f"Onvoldoende handelsdagen: {unique_trading_days} (minimaal: {self.ftmo_rules['min_trading_days']})"

        return True, None

    def check_ftmo_compliance(self, initial_balance: float = None) -> Dict:
        """
        Controleer FTMO-naleving met gedetailleerde analyse van handelsdata.

        Parameters:
        -----------
        initial_balance : float, optional
            Initiële accountbalans (default vanuit config).

        Returns:
        --------
        Dict
            Resultaten van naleving met details.
        """
        initial_balance = initial_balance if initial_balance is not None else self.initial_balance
        df = self.load_trade_data()
        if df.empty:
            return {'compliant': False, 'reason': 'Geen handelsdata beschikbaar', 'details': {}}

        status_df = df[df['Type'] == 'STATUS'].copy()
        if status_df.empty:
            return {'compliant': False, 'reason': 'Geen statusdata beschikbaar', 'details': {}}

        # Extraheer balans
        if 'Balance' not in status_df.columns or status_df['Balance'].isna().all():
            def extract_balance(comment):
                if isinstance(comment, str) and 'Balance: ' in comment:
                    match = re.search(r'Balance:\s*([\d,.]+)', comment)
                    return float(match.group(1).replace(',', '')) if match else None
                return None

            status_df['Balance'] = status_df['Comment'].apply(extract_balance)

        if status_df['Balance'].isna().all():
            return {'compliant': False, 'reason': 'Geen balansdata beschikbaar', 'details': {}}

        status_df['Balance'] = pd.to_numeric(status_df['Balance'], errors='coerce')
        daily_status = status_df.groupby('Date').agg(
            min_balance=('Balance', 'min'),
            max_balance=('Balance', 'max'),
            close_balance=('Balance', 'last')
        ).reset_index()

        daily_status['prev_close'] = daily_status['close_balance'].shift(1).fillna(initial_balance)
        daily_status['daily_pnl'] = daily_status['close_balance'] - daily_status['prev_close']
        daily_status['daily_pnl_pct'] = (daily_status['daily_pnl'] / daily_status['prev_close']) * 100
        daily_status['daily_drawdown'] = (daily_status['min_balance'] - daily_status['prev_close']) / daily_status[
            'prev_close'] * 100
        daily_status['peak'] = daily_status['close_balance'].cummax()
        daily_status['drawdown_from_peak'] = (daily_status['close_balance'] - daily_status['peak']) / daily_status[
            'peak'] * 100
        max_drawdown = daily_status['drawdown_from_peak'].min()

        latest_balance = daily_status['close_balance'].iloc[-1]
        total_pnl = latest_balance - initial_balance
        total_pnl_pct = (total_pnl / initial_balance) * 100

        trade_df = df[df['Type'] == 'TRADE']
        unique_trading_days = trade_df['Date'].nunique()

        profit_target_met = total_pnl_pct >= self.ftmo_rules['profit_target'] * 100
        daily_loss_compliant = daily_status['daily_drawdown'].min() > -self.ftmo_rules['max_daily_loss'] * 100
        total_loss_compliant = max_drawdown > -self.ftmo_rules['max_total_loss'] * 100
        trading_days_compliant = unique_trading_days >= self.ftmo_rules['min_trading_days']
        compliant = profit_target_met and daily_loss_compliant and total_loss_compliant and trading_days_compliant

        reasons = []
        if not profit_target_met:
            reasons.append(
                f"Winstdoel niet bereikt: {total_pnl_pct:.2f}% (doel: {self.ftmo_rules['profit_target'] * 100}%)")
        if not daily_loss_compliant:
            worst_day_idx = daily_status['daily_drawdown'].idxmin()
            worst_day = daily_status.iloc[worst_day_idx]
            reasons.append(
                f"Dagelijkse verlieslimiet overschreden: {worst_day['daily_drawdown']:.2f}% op {worst_day['Date']}")
        if not total_loss_compliant:
            reasons.append(
                f"Maximale drawdown overschreden: {max_drawdown:.2f}% (limiet: -{self.ftmo_rules['max_total_loss'] * 100}%)")
        if not trading_days_compliant:
            reasons.append(
                f"Onvoldoende handelsdagen: {unique_trading_days} (minimaal: {self.ftmo_rules['min_trading_days']})")

        reason = "; ".join(reasons) if reasons else "Voldoet aan alle FTMO-regels"

        details = {
            'initial_balance': initial_balance,
            'final_balance': latest_balance,
            'total_pnl': total_pnl,
            'total_pnl_pct': total_pnl_pct,
            'max_drawdown': max_drawdown,
            'trading_days': unique_trading_days,
            'daily_stats': daily_status
        }

        return {'compliant': compliant, 'reason': reason, 'details': details}

    def plot_ftmo_compliance(self, initial_balance: float = None) -> Optional[str]:
        """
        Maak een visualisatie van FTMO-naleving met extra analyses.

        Parameters:
        -----------
        initial_balance : float, optional
            Initiële accountbalans (default vanuit config).

        Returns:
        --------
        str
            Pad naar opgeslagen grafiek, of None bij mislukking.
        """
        initial_balance = initial_balance if initial_balance is not None else self.initial_balance
        compliance = self.check_ftmo_compliance(initial_balance)
        if not compliance['details']:
            if self.logger:
                self.logger.log_info("Onvoldoende data voor FTMO-analyse", level="ERROR")
            return None

        daily_stats = compliance['details']['daily_stats']
        fig = plt.figure(figsize=(16, 16))
        gs = fig.add_gridspec(5, 2, height_ratios=[2, 1, 1, 1, 1])

        # 1. Balansgrafiek
        ax1 = fig.add_subplot(gs[0, :])
        ax1.plot(daily_stats['Date'], daily_stats['close_balance'], 'b-', label='Accountbalans')
        ax1.axhline(y=initial_balance, color='gray', linestyle=':', label='Initiële balans')
        ax1.axhline(y=initial_balance * 1.10, color='green', linestyle='--',
                    label=f"+10% Doel (${initial_balance * 1.10:,.2f})")
        ax1.axhline(y=initial_balance * 0.95, color='orange', linestyle='--',
                    label=f"-5% Daglimiet (${initial_balance * 0.95:,.2f})")
        ax1.axhline(y=initial_balance * 0.90, color='red', linestyle='--',
                    label=f"-10% Max Drawdown (${initial_balance * 0.90:,.2f})")
        ax1.set_title('FTMO Accountbalans Progressie', fontsize=16)
        ax1.set_ylabel('Balans ($)', fontsize=14)
        ax1.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
        ax1.legend(loc='best', fontsize=12)
        ax1.grid(True)

        # 2. Dagelijkse P&L
        ax2 = fig.add_subplot(gs[1, 0])
        colors = ['green' if x >= 0 else 'red' for x in daily_stats['daily_pnl']]
        ax2.bar(daily_stats['Date'], daily_stats['daily_pnl'], color=colors, alpha=0.7)
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax2.set_title('Dagelijkse P&L ($)', fontsize=14)
        ax2.set_ylabel('P&L ($)', fontsize=12)
        ax2.grid(True, axis='y')

        # 3. Dagelijkse drawdown
        ax3 = fig.add_subplot(gs[1, 1])
        ax3.fill_between(daily_stats['Date'], daily_stats['daily_drawdown'], 0,
                         where=(daily_stats['daily_drawdown'] < 0), color='red', alpha=0.3)
        ax3.plot(daily_stats['Date'], daily_stats['daily_drawdown'], 'r-', alpha=0.7)
        ax3.axhline(y=-5, color='orange', linestyle='--', label='-5% Daglimiet')
        ax3.set_title('Dagelijkse Drawdown (%)', fontsize=14)
        ax3.set_ylabel('Drawdown (%)', fontsize=12)
        ax3.set_ylim(max(-15, daily_stats['daily_drawdown'].min() * 1.2), 5)
        ax3.legend(loc='lower right', fontsize=10)
        ax3.grid(True)

        # 4. Cumulatieve drawdown vanaf piek
        ax4 = fig.add_subplot(gs[2, :])
        ax4.fill_between(daily_stats['Date'], daily_stats['drawdown_from_peak'], 0, color='purple', alpha=0.3)
        ax4.plot(daily_stats['Date'], daily_stats['drawdown_from_peak'], 'purple', alpha=0.7)
        ax4.axhline(y=-10, color='red', linestyle='--', label='-10% Max Drawdown')
        ax4.set_title('Maximale Drawdown vanaf Piek (%)', fontsize=14)
        ax4.set_ylabel('Drawdown (%)', fontsize=12)
        ax4.set_ylim(max(-12, daily_stats['drawdown_from_peak'].min() * 1.2), 2)
        ax4.legend(loc='lower right', fontsize=10)
        ax4.grid(True)

        # 5. Win/Loss Ratio
        trade_df = self.load_trade_data()[self.load_trade_data()['Type'] == 'TRADE']
        if not trade_df.empty:
            profits = \
            trade_df[trade_df['Action'].isin(['SELL', 'BUY']) & (trade_df['Price'].shift(-1) - trade_df['Price'] > 0)][
                'Price'].count()
            losses = \
            trade_df[trade_df['Action'].isin(['SELL', 'BUY']) & (trade_df['Price'].shift(-1) - trade_df['Price'] < 0)][
                'Price'].count()
            win_loss_ratio = profits / losses if losses > 0 else float('inf')
            ax5 = fig.add_subplot(gs[3, :])
            ax5.bar(['Wins', 'Losses'], [profits, losses], color=['green', 'red'])
            ax5.set_title('Win/Loss Ratio', fontsize=14)
            ax5.set_ylabel('Aantal Trades', fontsize=12)
            ax5.text(0.5, -0.1, f"Win/Loss Ratio: {win_loss_ratio:.2f}", transform=ax5.transAxes, ha='center')
            ax5.grid(True, axis='y')

        # 6. Nalevingstabel
        ax6 = fig.add_subplot(gs[4, :])
        ax6.axis('off')
        compliance_data = [
            ['Metriek', 'Waarde', 'Vereiste', 'Status'],
            ['Totale P&L', f"{compliance['details']['total_pnl_pct']:.2f}%",
             f"≥ {self.ftmo_rules['profit_target'] * 100}%",
             '✅' if compliance['details']['total_pnl_pct'] >= 10 else '❌'],
            ['Max Dagelijkse Drawdown', f"{daily_stats['daily_drawdown'].min():.2f}%",
             f"> -{self.ftmo_rules['max_daily_loss'] * 100}%",
             '✅' if daily_stats['daily_drawdown'].min() > -5 else '❌'],
            ['Max Totale Drawdown', f"{compliance['details']['max_drawdown']:.2f}%",
             f"> -{self.ftmo_rules['max_total_loss'] * 100}%",
             '✅' if compliance['details']['max_drawdown'] > -10 else '❌'],
            ['Handelsdagen', f"{compliance['details']['trading_days']}",
             f"≥ {self.ftmo_rules['min_trading_days']}",
             '✅' if compliance['details']['trading_days'] >= 4 else '❌']
        ]
        tbl = ax6.table(cellText=compliance_data, loc='center', cellLoc='center', colWidths=[0.25, 0.25, 0.25, 0.15])
        tbl.auto_set_font_size(False)
        tbl.set_fontsize(14)
        tbl.scale(1, 2)

        header_color = '#40466e'
        pass_color = '#d8f3dc'
        fail_color = '#ffcccb'
        for (i, j), cell in tbl.get_celld().items():
            if i == 0:
                cell.set_facecolor(header_color)
                cell.set_text_props(color='white', fontweight='bold')
            elif j == 3:
                cell.set_facecolor(pass_color if compliance_data[i][3] == '✅' else fail_color)

        overall_status = 'GESLAAGD' if compliance['compliant'] else 'GEFAALD'
        status_color = 'green' if compliance['compliant'] else 'red'
        ax6.set_title(f"FTMO Naleving: {overall_status}", fontsize=18, color=status_color, fontweight='bold')
        if not compliance['compliant']:
            ax6.text(0.5, 0.1, compliance['reason'], horizontalalignment='center', fontsize=12, color='red',
                     transform=ax6.transAxes)

        plt.tight_layout()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"ftmo_compliance_{timestamp}.png")
        plt.savefig(output_path, dpi=150)
        plt.close()
        if self.logger:
            self.logger.log_info(f"FTMO nalevingsgrafiek opgeslagen als {output_path}")
        return output_path

    def generate_trading_report(self, initial_balance: float = None) -> bool:
        """
        Genereer een gedetailleerd FTMO handelsrapport met extra metrics.

        Parameters:
        -----------
        initial_balance : float, optional
            Initiële accountbalans (default vanuit config).

        Returns:
        --------
        bool
            True als rapport succesvol gegenereerd.
        """
        initial_balance = initial_balance if initial_balance is not None else self.initial_balance
        try:
            compliance = self.check_ftmo_compliance(initial_balance)
            if not compliance['details']:
                if self.logger:
                    self.logger.log_info("Onvoldoende data voor rapportgeneratie", level="ERROR")
                return False

            compliance_path = self.plot_ftmo_compliance(initial_balance)
            df = self.load_trade_data()
            trade_df = df[df['Type'] == 'TRADE'].copy()

            # Instrumentanalyse
            symbol_stats = {}
            for symbol in trade_df['Symbol'].unique():
                symbol_df = trade_df[trade_df['Symbol'] == symbol]
                wins = len(symbol_df[symbol_df['Action'].isin(['SELL', 'BUY']) & (
                            symbol_df['Price'].shift(-1) - symbol_df['Price'] > 0)])
                losses = len(symbol_df[symbol_df['Action'].isin(['SELL', 'BUY']) & (
                            symbol_df['Price'].shift(-1) - symbol_df['Price'] < 0)])
                symbol_stats[symbol] = {
                    'total_trades': len(symbol_df),
                    'wins': wins,
                    'losses': losses,
                    'win_rate': (wins / (wins + losses) * 100) if (wins + losses) > 0 else 0,
                    'days_traded': symbol_df['Date'].nunique()
                }

            # Rapportweergave
            report = "\n===== FTMO Handelsrapport =====\n"
            report += f"Periode: {df['Timestamp'].min().date() if not df.empty else 'N/A'} tot {df['Timestamp'].max().date() if not df.empty else 'N/A'}\n"
            report += f"Initiële balans: ${initial_balance:,.2f}\n"
            report += f"Eindebalans: ${compliance['details']['final_balance']:,.2f}\n"
            report += f"Totale P&L: ${compliance['details']['total_pnl']:,.2f} ({compliance['details']['total_pnl_pct']:.2f}%)\n"
            report += f"Maximale drawdown: {compliance['details']['max_drawdown']:.2f}%\n"
            report += f"Aantal handelsdagen: {compliance['details']['trading_days']}\n"
            report += "\nInstrumentanalyse:\n"
            for symbol, stats in symbol_stats.items():
                report += f"  {symbol}: {stats['total_trades']} trades ({stats['wins']} wins, {stats['losses']} losses, Win Rate: {stats['win_rate']:.2f}%) over {stats['days_traded']} dagen\n"
            report += f"\nFTMO Naleving: {'GESLAAGD' if compliance['compliant'] else 'GEFAALD'}\n"
            if not compliance['compliant']:
                report += f"Reden: {compliance['reason']}\n"
            if compliance_path:
                report += f"\nNalevingsvisualisatie opgeslagen als: {os.path.basename(compliance_path)}\n"

            # Extra metrics
            total_trades = len(trade_df)
            avg_trade_size = trade_df['Volume'].mean() if not trade_df.empty else 0
            report += f"\nExtra Metrics:\n"
            report += f"  Totaal aantal trades: {total_trades}\n"
            report += f"  Gemiddelde trade grootte: {avg_trade_size:.2f} lots\n"

            print(report)

            if self.logger:
                self.logger.log_info(f"FTMO Rapport gegenereerd - Compliant: {compliance['compliant']}")
                if not compliance['compliant']:
                    self.logger.log_info(f"Reden voor niet-naleving: {compliance['reason']}")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = os.path.join(self.output_dir, f"ftmo_report_{timestamp}.txt")
            with open(report_path, 'w') as f:
                f.write(report)

            return True
        except Exception as e:
            if self.logger:
                self.logger.log_info(f"Fout bij rapportgeneratie: {e}", level="ERROR")
            return False
```

-----------

Path: Sophy_temp/src/monitoring/__init__.py

```python
```

-----------

Path: Sophy_temp/src/presentation/__init__.py

```python
```

-----------

Path: Sophy_temp/src/presentation/dashboard.py

```python
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
```

-----------

Path: Sophy_temp/src/risk/__init__.py

```python
```

-----------

Path: Sophy_temp/src/risk/position_sizer.py

```python
def calculate_position_size(
        entry_price: float,
        stop_loss: float,
        account_balance: float,
        risk_percentage: float,
        pip_value: float,
        min_lot: float = 0.01,
        max_lot: float = 10.0
) -> float:
    """
    Calculate optimal position size based on risk parameters

    Args:
        entry_price: Entry price for the position
        stop_loss: Stop loss price
        account_balance: Current account balance
        risk_percentage: Percentage of account to risk (0.01 = 1%)
        pip_value: Value of one pip in account currency
        min_lot: Minimum allowable lot size
        max_lot: Maximum allowable lot size

    Returns:
        Calculated position size in lots
    """
    if entry_price == stop_loss:
        return min_lot  # Avoid division by zero

    # Calculate risk amount in account currency
    risk_amount = account_balance * risk_percentage

    # Calculate pips at risk
    pips_at_risk = abs(entry_price - stop_loss) / 0.0001  # For 4-digit forex pairs

    # Calculate lot size
    lot_size = risk_amount / (pips_at_risk * pip_value)

    # Enforce limits
    lot_size = max(min_lot, min(lot_size, max_lot))

    # Round to 2 decimal places
    lot_size = round(lot_size, 2)

    return lot_size
```

-----------

Path: Sophy_temp/src/risk/risk_manager.py

```python
# src/risk/risk_manager.py
from datetime import date
from typing import Dict, Optional, Tuple


class RiskManager:
    """
    Risicomanagement met FTMO compliance checks.

    Verantwoordelijk voor het bewaken van risicoparameters zoals dagelijkse verlieslimiet,
    maximale drawdown, en positiegrootte berekeningen volgens risicoregels.
    """

    def __init__(self, config: Dict, logger):
        """Initialiseer met configuratieparameters"""
        self.config = config
        self.logger = logger

        # Extraheer risicoparameters
        self.max_risk_per_trade = self.config.get('max_risk_per_trade', 0.01)
        self.max_daily_drawdown = self.config.get('max_daily_drawdown', 0.05)
        self.max_total_drawdown = self.config.get('max_total_drawdown', 0.10)
        self.leverage = self.config.get('leverage', 30)

        # Initialiseer tracking variabelen
        self.daily_losses = 0
        self.current_date = date.today()
        self.initial_balance = self.config.get('account_balance', 100000)
        self.daily_trades_count = 0
        self.max_daily_trades = self.config.get('max_daily_trades', 10)

        self.logger.log_info(f"RiskManager geïnitialiseerd met max risk per trade: {self.max_risk_per_trade * 100}%, "
                             f"max daily drawdown: {self.max_daily_drawdown * 100}%, "
                             f"max total drawdown: {self.max_total_drawdown * 100}%, "
                             f"leverage: {self.leverage}")

    def check_ftmo_limits(self, account_info: Dict) -> Tuple[bool, Optional[str]]:
        """
        Controleer of huidige accountstatus voldoet aan FTMO-limieten

        Parameters:
        -----------
        account_info : Dict
            Dictionary met huidige accountinformatie

        Returns:
        --------
        Tuple van (stop_trading, reason)
        - stop_trading: True als trading gestopt moet worden
        - reason: Beschrijving waarom trading moet stoppen, of None
        """
        # Reset dagelijkse variabelen als het een nieuwe dag is
        today = date.today()
        if today != self.current_date:
            self.daily_losses = 0
            self.daily_trades_count = 0
            self.current_date = today
            self.logger.log_info("Dagelijkse risico limieten gereset (nieuwe handelsdag)")

        # Haal account data op
        current_balance = account_info.get('balance', 0)
        current_equity = account_info.get('equity', 0)

        # Bereken winst/verlies percentages
        balance_change_pct = (current_balance - self.initial_balance) / self.initial_balance
        equity_change_pct = (current_equity - self.initial_balance) / self.initial_balance

        # Controleer of winstdoel is bereikt (10%)
        if balance_change_pct >= 0.10:
            return True, f"Winstdoel bereikt: {balance_change_pct:.2%}"

        # Controleer dagelijkse verlieslimiet (5%)
        if equity_change_pct <= -self.max_daily_drawdown:
            return True, f"Dagelijkse verlieslimiet bereikt: {equity_change_pct:.2%}"

        # Controleer totale verlieslimiet (10%)
        if equity_change_pct <= -self.max_total_drawdown:
            return True, f"Maximale drawdown bereikt: {equity_change_pct:.2%}"

        # Alles is binnen limieten
        return False, None

    def calculate_position_size(self,
                                symbol: str,
                                entry_price: float,
                                stop_loss: float,
                                account_balance: float,
                                trend_strength: float = 0.5) -> float:
        """
        Bereken optimale positiegrootte gebaseerd op risicoparameters

        Parameters:
        -----------
        symbol : str
            Trading symbool
        entry_price : float
            Ingangsprijs voor de positie
        stop_loss : float
            Stop loss prijs
        account_balance : float
            Huidige account balans
        trend_strength : float
            Sterkte van de trend (0-1), gebruikt voor positiegrootte aanpassing

        Returns:
        --------
        float : Berekende positiegrootte in lots
        """
        if entry_price == 0 or stop_loss == 0:
            self.logger.log_info(f"Ongeldige entry of stop loss voor {symbol}", level="ERROR")
            return 0.01

        # Voorkom delen door nul
        if entry_price == stop_loss:
            self.logger.log_info(f"Entry gelijk aan stop loss voor {symbol}", level="WARNING")
            return 0.01

        # Bereken risicobedrag in accountvaluta
        risk_amount = account_balance * self.max_risk_per_trade

        # Pas risico aan op basis van trendsterkte
        adjusted_risk = risk_amount * (0.5 + trend_strength / 2)  # 50-100% van normaal risico

        # Bereken pips op risico
        pips_at_risk = abs(entry_price - stop_loss) / 0.0001  # Voor 4-cijferige forex paren

        # Pas aan voor goud en indices indien nodig
        if symbol == "XAUUSD":
            pips_at_risk = abs(entry_price - stop_loss) / 0.01  # Voor goud (0.01 = 1 pip)
        elif symbol in ["US30", "US30.cash", "US500", "USTEC"]:
            pips_at_risk = abs(entry_price - stop_loss) / 0.1  # Voor indices

        # Schat pip waarde (kan worden verbeterd met exacte berekening per symbool)
        pip_value = 10.0  # Standaard pip waarde voor 1 lot

        # Bereken lot size
        lot_size = adjusted_risk / (pips_at_risk * pip_value)

        # Rond af naar 2 decimalen en begrens tussen min/max waarden
        min_lot = 0.01
        max_lot = 10.0
        lot_size = max(min_lot, min(lot_size, max_lot))
        lot_size = round(lot_size, 2)

        self.logger.log_info(f"Berekende positiegrootte voor {symbol}: {lot_size} lots "
                             f"(Risk: ${adjusted_risk:.2f}, Pips: {pips_at_risk:.1f})")

        return lot_size

    def check_trade_risk(self,
                         symbol: str,
                         volume: float,
                         entry_price: float,
                         stop_loss: float) -> bool:
        """
        Controleer of een trade binnen de risicolimieten valt

        Parameters:
        -----------
        symbol : str
            Trading symbool
        volume : float
            Positiegrootte in lots
        entry_price : float
            Ingangsprijs voor de positie
        stop_loss : float
            Stop loss prijs

        Returns:
        --------
        bool : True als trade binnen risicolimieten valt, anders False
        """
        # Controleer dagelijks aantal trades
        self.daily_trades_count += 1
        if self.daily_trades_count > self.max_daily_trades:
            self.logger.log_info(f"Maximaal aantal dagelijkse trades bereikt: {self.max_daily_trades}", level="WARNING")
            return False

        # Als er geen stop loss is, is dit een hoog risico en accepteren we de trade niet
        if stop_loss == 0:
            self.logger.log_info(f"Trade geweigerd voor {symbol}: Geen stop loss ingesteld", level="WARNING")
            return False

        # Berekening potentieel verlies
        pip_value = 10.0  # Standaard pip waarde voor 1 lot
        pips_at_risk = abs(entry_price - stop_loss) / 0.0001

        # Pas aan voor goud en indices indien nodig
        if symbol == "XAUUSD":
            pips_at_risk = abs(entry_price - stop_loss) / 0.01
        elif symbol in ["US30", "US30.cash", "US500", "USTEC"]:
            pips_at_risk = abs(entry_price - stop_loss) / 0.1

        potential_loss = pips_at_risk * pip_value * volume

        # Controleer tegen dagelijkse verlieslimiet
        max_daily_loss = self.initial_balance * self.max_daily_drawdown
        if self.daily_losses + potential_loss > max_daily_loss:
            self.logger.log_info(f"Trade geweigerd voor {symbol}: Zou dagelijkse verlieslimiet overschrijden",
                                 level="WARNING")
            return False

        # Extra validatie voor extreem grote posities
        if volume > 5.0:  # Voorbeeld van een arbitraire limiet
            self.logger.log_info(f"Trade geweigerd voor {symbol}: Volume te groot ({volume} lots)", level="WARNING")
            return False

        # Trade geaccepteerd
        return True

    def can_trade(self) -> bool:
        """
        Controleert of trading is toegestaan op basis van huidige limieten

        Returns:
        --------
        bool : True als trading is toegestaan, anders False
        """
        # Reset dagelijkse variabelen als het een nieuwe dag is
        today = date.today()
        if today != self.current_date:
            self.daily_losses = 0
            self.daily_trades_count = 0
            self.current_date = today

        # Controleer dagelijks aantal trades
        if self.daily_trades_count >= self.max_daily_trades:
            return False

        return True

    def update_daily_loss(self, loss_amount: float) -> None:
        """
        Update het dagelijkse verliestotaal

        Parameters:
        -----------
        loss_amount : float
            Verliesbedrag (positief voor verlies, negatief voor winst)
        """
        # Reset als het een nieuwe dag is
        today = date.today()
        if today != self.current_date:
            self.daily_losses = 0
            self.daily_trades_count = 0
            self.current_date = today

        # Update dagelijkse verliezen
        if loss_amount > 0:  # Alleen verliesposities bijhouden
            self.daily_losses += loss_amount
            self.logger.log_info(f"Dagelijks verlies bijgewerkt: ${self.daily_losses:.2f} "
                                 f"(Max: ${self.initial_balance * self.max_daily_drawdown:.2f})")
```

-----------

Path: Sophy_temp/src/strategy/__init__.py

```python
```

-----------

Path: Sophy_temp/src/strategy/base_strategy.py

```python
# src/strategy/base_strategy.py
from abc import ABC, abstractmethod
from typing import Dict, Any, List


class Strategy(ABC):
    """
    Abstracte basisklasse voor alle handelsstrategieën.

    Deze klasse definieert de interface die alle strategieën moeten implementeren.
    Door deze basisklasse te gebruiken, kunnen we gemakkelijk nieuwe strategieën
    toevoegen zonder de rest van de code aan te hoeven passen.
    """

    def __init__(self, connector, risk_manager, logger, config):
        """
        Initialiseer de strategie met de benodigde componenten

        Parameters:
        -----------
        connector : Connector naar handelsplatform (bijv. MT5)
        risk_manager : Risicobeheer component
        logger : Logging component
        config : Configuratiegegevens voor de strategie
        """
        self.connector = connector
        self.risk_manager = risk_manager
        self.logger = logger
        self.config = config
        self.name = "Base Strategy"

    @abstractmethod
    def process_symbol(self, symbol: str) -> Dict[str, Any]:
        """
        Verwerk een symbool volgens de strategie regels

        Parameters:
        -----------
        symbol : str
            Het te verwerken symbool

        Returns:
        --------
        Dict : Resultaten van de verwerking, inclusief eventuele signalen
        """
        pass

    @abstractmethod
    def calculate_indicators(self, data: Any) -> Dict[str, Any]:
        """
        Bereken de technische indicatoren voor de strategie

        Parameters:
        -----------
        data : Any
            Prijsgegevens en andere input

        Returns:
        --------
        Dict : Berekende indicatoren
        """
        pass

    def get_name(self) -> str:
        """
        Geef de naam van de strategie terug

        Returns:
        --------
        str : Strategienaam
        """
        return self.name

    def get_open_positions(self) -> Dict[str, List]:
        """
        Haal alle open posities op

        Returns:
        --------
        Dict : Dictionary met open posities per symbool
        """
        return {}
```

-----------

Path: Sophy_temp/src/strategy/dax_opening.py

```python
```

-----------

Path: Sophy_temp/src/strategy/strategy_factory.py

```python
# src/strategy/strategy_factory.py
import copy
import importlib
import os
from typing import Optional

from src.strategy.base_strategy import Strategy


class StrategyFactory:
    """Factory voor het creëren van trading strategie-instanties"""

    _strategies = {}

    @classmethod
    def _load_strategies(cls):
        """Laad beschikbare strategieën dynamisch uit de strategy directory"""
        if cls._strategies:
            return

        # Zoek naar strategie modules in de src/strategy directory
        strategy_dir = os.path.dirname(os.path.abspath(__file__))
        for filename in os.listdir(strategy_dir):
            if filename.endswith('_strategy.py') and filename != 'base_strategy.py':
                module_name = filename[:-3]  # Verwijder .py

                try:
                    # Import de module
                    module_path = f"src.strategy.{module_name}"
                    module = importlib.import_module(module_path)

                    # Zoek naar classes die Strategy erven
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if isinstance(attr, type) and issubclass(attr, Strategy) and attr is not Strategy:
                            # Registreer de strategie
                            strategy_key = module_name.replace('_strategy', '')
                            cls._strategies[strategy_key] = attr
                except (ImportError, AttributeError) as e:
                    print(f"Kon strategie module {module_name} niet laden: {e}")

        # Voeg de turtle strategie toe als deze niet automatisch geladen is
        if 'turtle' not in cls._strategies:
            try:
                from src.strategy.turtle_strategy import TurtleStrategy
                cls._strategies['turtle'] = TurtleStrategy
            except ImportError:
                pass

    @classmethod
    def create_strategy(
            cls,
            strategy_name: str,
            connector: Optional[object],
            risk_manager: Optional[object],
            logger: Optional[object],
            config: Optional[dict]
    ) -> Strategy:
        """
        Creëert een instantie van de gevraagde strategie.

        Args:
            strategy_name (str): Naam van de strategie.
            connector: MT5 connector instantie.
            risk_manager: Risk manager instantie.
            logger: Logger instantie.
            config (dict): Configuratieobject.

        Returns:
            Strategy: Een instantie van de gevraagde strategie.

        Raises:
            ValueError: Als de strategie niet bestaat.
        """
        # Laad beschikbare strategieën
        cls._load_strategies()

        # Controleer of de gevraagde strategie bestaat
        if strategy_name not in cls._strategies:
            # Speciale geval: turtle_swing is dezelfde als turtle maar met swing modus
            if strategy_name == 'turtle_swing' and 'turtle' in cls._strategies:
                strategy_name = 'turtle'
                if config and 'strategy' in config:
                    config['strategy']['swing_mode'] = True
            else:
                if logger:
                    logger.log_info(f"Onbekende strategie: {strategy_name}", level="ERROR")
                raise ValueError(f"Onbekende strategie: {strategy_name}")

        strategy_class = cls._strategies[strategy_name]

        # Maak een kopie van de config om mutatie te vermijden
        local_config = copy.deepcopy(config) if config else {}

        return strategy_class(connector, risk_manager, logger, local_config)

    @classmethod
    def list_available_strategies(cls) -> list:
        """Geeft een lijst van beschikbare strategieën."""
        cls._load_strategies()
        return list(cls._strategies.keys())
```

-----------

Path: Sophy_temp/src/strategy/turtle_strategy.py

```python
from datetime import datetime
from typing import Dict, List, Any

import MetaTrader5 as mt5
import pandas as pd

# Voorbeeld imports (pas aan naar je daadwerkelijke module-structuur)
from src.connector.mt5_connector import MT5Connector  # Placeholder
from src.risk.risk_manager import RiskManager  # Placeholder
from src.strategy.base_strategy import Strategy
from src.utils.logger import Logger  # Placeholder


class TurtleStrategy(Strategy):
    """Implementatie van de Turtle Trading strategie geoptimaliseerd voor FTMO met ondersteuning voor swing modus."""

    def __init__(self, connector: MT5Connector, risk_manager: RiskManager, logger: Logger, config: dict):
        """
        Initialiseer de Turtle strategie.

        Parameters:
        -----------
        connector : MT5Connector
            Verbinding met MetaTrader 5.
        risk_manager : RiskManager
            Risicobeheer component.
        logger : Logger
            Component voor logging.
        config : dict
            Configuratie voor de strategie, inclusief mt5- en strategy-secties.
        """
        super().__init__(connector, risk_manager, logger, config)
        self.name = "Turtle Trading Strategy"
        self.position_initial_volumes: Dict[int, float] = {}  # Ticket -> initiële volume
        self.strategy_config = config.get('strategy', {})
        self.swing_mode = self.strategy_config.get('swing_mode', False)

        # Stel parameters in gebaseerd op modus
        if self.swing_mode:
            self.entry_period = self.strategy_config.get('entry_period', 40)
            self.exit_period = self.strategy_config.get('exit_period', 20)
            self.atr_period = self.strategy_config.get('atr_period', 20)
            self.atr_multiplier = self.strategy_config.get('atr_multiplier', 2.5)
            self.logger.log_info(
                "Strategie geïnitialiseerd in Swing modus met parameters: "
                f"entry_period={self.entry_period}, exit_period={self.exit_period}, "
                f"atr_period={self.atr_period}, atr_multiplier={self.atr_multiplier}"
            )
        else:
            self.entry_period = self.strategy_config.get('entry_period', 20)
            self.exit_period = self.strategy_config.get('exit_period', 10)
            self.atr_period = self.strategy_config.get('atr_period', 20)
            self.atr_multiplier = self.strategy_config.get('atr_multiplier', 2.0)
            self.logger.log_info(
                "Strategie geïnitialiseerd in standaard modus met parameters: "
                f"entry_period={self.entry_period}, exit_period={self.exit_period}, "
                f"atr_period={self.atr_period}, atr_multiplier={self.atr_multiplier}"
            )

        self.use_trend_filter = self.strategy_config.get('use_trend_filter', True)

    def calculate_indicators(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Bereken technische indicatoren voor de Turtle strategie.

        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame met prijsdata (high, low, close, tick_volume).

        Returns:
        --------
        Dict[str, Any]
            Berekende indicatoren voor de laatste rij.
        """
        if df.empty or 'high' not in df.columns or 'low' not in df.columns or 'close' not in df.columns:
            return {}

        # Bereken ATR
        df['atr'] = self.calculate_atr(df)

        # Bereken Donchian kanalen
        df['high_entry'] = df['high'].rolling(window=self.entry_period).max()
        df['low_entry'] = df['low'].rolling(window=self.entry_period).min()
        df['high_exit'] = df['high'].rolling(window=self.exit_period).max()
        df['low_exit'] = df['low'].rolling(window=self.exit_period).min()

        # Voeg volume-indicator toe
        df['vol_avg_50'] = df['tick_volume'].rolling(window=50).mean()
        df['vol_ratio'] = df['tick_volume'] / df['vol_avg_50'].replace(0, 1)  # Vermijd deling door 0

        # Trendfilters
        if len(df) >= 50:
            df['ema_50'] = df['close'].ewm(span=50, adjust=False).mean()
        if len(df) >= 200:
            df['ema_200'] = df['close'].ewm(span=200, adjust=False).mean()

        if 'ema_50' in df.columns:
            df['trend_bullish'] = df['close'] > df['ema_50']
        if 'ema_50' in df.columns and 'ema_200' in df.columns:
            df['strong_trend'] = df['ema_50'] > df['ema_200']
        if 'ema_50' in df.columns:
            df['trend_strength'] = self.calculate_trend_strength(df)
        if 'atr' in df.columns:
            df['high_volatility'] = self.calculate_market_volatility(df)

        # Retourneer laatste waarden
        return {
            'atr': df['atr'].iloc[-1] if 'atr' in df else None,
            'high_entry': df['high_entry'].iloc[-2] if 'high_entry' in df else None,
            'low_entry': df['low_entry'].iloc[-2] if 'low_entry' in df else None,
            'high_exit': df['high_exit'].iloc[-2] if 'high_exit' in df else None,
            'low_exit': df['low_exit'].iloc[-2] if 'low_exit' in df else None,
            'trend_bullish': df['trend_bullish'].iloc[-1] if 'trend_bullish' in df else None,
            'strong_trend': df['strong_trend'].iloc[-1] if 'strong_trend' in df else None,
            'trend_strength': df['trend_strength'].iloc[-1] if 'trend_strength' in df else None,
            'high_volatility': df['high_volatility'].iloc[-1] if 'high_volatility' in df else None,
            'vol_ratio': df['vol_ratio'].iloc[-1] if 'vol_ratio' in df else None
        }

    def calculate_atr(self, df: pd.DataFrame) -> pd.Series:
        """
        Bereken de Average True Range (ATR).

        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame met prijsdata (high, low, close).

        Returns:
        --------
        pd.Series
            ATR waarden.
        """
        if 'close' not in df.columns or df['close'].isna().all():
            return pd.Series([0] * len(df), index=df.index)
        high = df['high']
        low = df['low']
        close = df['close'].shift(1).fillna(method='bfill')

        tr1 = high - low
        tr2 = abs(high - close)
        tr3 = abs(low - close)
        tr = pd.DataFrame({'tr1': tr1, 'tr2': tr2, 'tr3': tr3}).max(axis=1)
        return tr.rolling(window=self.atr_period, min_periods=1).mean()

    def calculate_trend_strength(self, df: pd.DataFrame) -> float:
        """
        Bereken trendsterkte gebaseerd op EMA-afstand en -hoek.

        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame met prijsdata.

        Returns:
        --------
        float
            Trendsterkte (0-1).
        """
        if 'ema_50' not in df.columns or len(df) < 10:
            return 0.0
        latest_close = df['close'].iloc[-1]
        latest_ema = df['ema_50'].iloc[-1]
        ema_slope = (df['ema_50'].iloc[-1] - df['ema_50'].iloc[-10]) / df['ema_50'].iloc[-10] if df['ema_50'].iloc[
                                                                                                     -10] != 0 else 0
        latest_atr = df['atr'].iloc[-1] if 'atr' in df and not pd.isna(df['atr'].iloc[-1]) else latest_close * 0.01
        distance = (latest_close - latest_ema) / latest_atr
        distance_score = min(1.0, max(0.0, distance / 3))
        slope_score = min(1.0, max(0.0, ema_slope * 20))
        return min(1.0, max(0.0, (distance_score * 0.7) + (slope_score * 0.3)))

    def calculate_market_volatility(self, df: pd.DataFrame) -> bool:
        """
        Bepaal of de markt in een hoge volatiliteitsperiode zit.

        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame met prijsdata.

        Returns:
        --------
        bool
            True als volatiliteit hoog is.
        """
        if 'atr' not in df.columns or len(df) < 20:
            return False
        avg_atr = df['atr'].iloc[-20:].mean()
        if pd.isna(avg_atr) or avg_atr == 0:
            return False
        current_atr = df['atr'].iloc[-1]
        return current_atr > (avg_atr * 1.3) if not pd.isna(current_atr) else False

    def process_symbol(self, symbol: str) -> Dict[str, Any]:
        """
        Verwerk een symbool volgens de Turtle strategie.

        Parameters:
        -----------
        symbol : str
            Het te verwerken symbool.

        Returns:
        --------
        Dict[str, Any]
            Resultaten inclusief signaal en actie.
        """
        result = {'signal': None, 'action': None}
        if not self.risk_manager.can_trade():
            self.logger.log_info(f"Dagelijkse risico-limiet bereikt, geen trades voor {symbol}")
            return result

        timeframe_str = self.config.get('mt5', {}).get('timeframe', 'H4')
        bars_needed = 240 if timeframe_str == 'H1' else 150 if timeframe_str == 'H4' else 200
        df = self.connector.get_historical_data(symbol, timeframe_str, bars_needed)
        if df.empty:
            self.logger.log_info(f"Geen historische data beschikbaar voor {symbol}")
            return result

        indicators = self.calculate_indicators(df)
        if not indicators:
            self.logger.log_info(f"Kon indicatoren niet berekenen voor {symbol}")
            return result

        tick = self.connector.get_symbol_tick(symbol)
        if tick is None:
            self.logger.log_info(f"Kon geen tick informatie krijgen voor {symbol}")
            return result

        current_price = tick.ask
        last_high_entry = indicators.get('high_entry')
        last_low_exit = indicators.get('low_exit')
        current_atr = indicators.get('atr')
        if None in (current_atr, last_high_entry, last_low_exit):
            self.logger.log_info(f"Ontbrekende indicator waarden voor {symbol}")
            return result

        trend_bullish = indicators.get('trend_bullish', True)
        strong_trend = indicators.get('strong_trend', True)
        trend_strength = indicators.get('trend_strength', 0.5)
        high_volatility = indicators.get('high_volatility', False)
        volume_ratio = indicators.get('vol_ratio', 1.0)

        price_breakout = current_price > last_high_entry * 1.001
        volume_filter = volume_ratio > 1.1 if not pd.isna(volume_ratio) else True
        entry_conditions = price_breakout and current_atr > 0 and volume_filter

        if self.use_trend_filter:
            entry_conditions = entry_conditions and trend_bullish
        if self.swing_mode:
            entry_conditions = entry_conditions and strong_trend and not high_volatility

        if entry_conditions:
            self.logger.log_info(f"Breakout gedetecteerd voor {symbol} op {current_price}")
            result['signal'] = 'ENTRY'
            result['action'] = 'BUY'

            sl_multiplier = self.atr_multiplier + 0.5 if high_volatility else self.atr_multiplier
            stop_loss = current_price - (sl_multiplier * current_atr)

            account_info = self.connector.get_account_info()
            account_balance = account_info.get('balance', self.config.get('mt5', {}).get('account_balance', 100000))
            lot_size = self.risk_manager.calculate_position_size(symbol, current_price, stop_loss, account_balance,
                                                                 trend_strength)

            if not self.risk_manager.check_trade_risk(symbol, lot_size, current_price, stop_loss):
                self.logger.log_info(f"Trade overschrijdt risicolimiet voor {symbol}")
                return result

            try:
                ticket = self.connector.place_order(
                    "BUY", symbol, lot_size, stop_loss, 0,
                    comment=f"FTMO {'Swing' if self.swing_mode else 'Turtle'}"
                )
                if ticket:
                    self.position_initial_volumes[ticket] = lot_size
                    self.logger.log_trade(
                        symbol, "BUY", current_price, lot_size, stop_loss, 0,
                        f"{'Swing' if self.swing_mode else 'Turtle'} Entry (TS:{trend_strength:.2f})",
                        self.risk_manager.leverage
                    )
                    result['ticket'] = ticket
                    result['volume'] = lot_size
                    result['stop_loss'] = stop_loss
            except Exception as e:
                self.logger.log_error(f"Fout bij plaatsen order voor {symbol}: {e}")
                return result

        self._manage_positions(symbol, current_price, last_low_exit, current_atr)
        return result

    def _manage_positions(self, symbol: str, current_price: float, last_low_exit: float, current_atr: float) -> None:
        """
        Beheer bestaande posities voor een symbool.

        Parameters:
        -----------
        symbol : str
            Trading symbool.
        current_price : float
            Huidige marktprijs.
        last_low_exit : float
            Laatste Donchian kanaal low exit.
        current_atr : float
            Huidige ATR waarde.
        """
        open_positions = self.connector.get_open_positions(symbol)
        if not open_positions:
            return

        for position in open_positions:
            position_age_days = (datetime.now().timestamp() - position.time) / (60 * 60 * 24)
            if position.type != mt5.POSITION_TYPE_BUY:
                continue

            entry_price = position.price_open
            profit_atr = 1.5 if self.swing_mode else 1.0
            profit_target_1 = entry_price + (profit_atr * current_atr)
            profit_target_2 = entry_price + (profit_atr * 2 * current_atr)
            min_hold_time = 2 if self.swing_mode else 1
            time_condition_met = position_age_days >= min_hold_time

            if (
                    time_condition_met and current_price > profit_target_1 and position.ticket in self.position_initial_volumes):
                initial_volume = self.position_initial_volumes[position.ticket]
                partial_volume = round(initial_volume * 0.4, 2)
                if position.volume >= partial_volume and partial_volume >= 0.01:
                    self.logger.log_info(f"Gedeeltelijke winstneming (40%) voor {symbol} op {current_price}")
                    try:
                        partial_result = self.connector.place_order(
                            "SELL", symbol, partial_volume, 0, 0, f"Partial Profit 40% - ticket:{position.ticket}"
                        )
                        if partial_result:
                            self.logger.log_trade(symbol, "SELL", current_price, partial_volume, 0, 0,
                                                  "Partial Profit 40%")
                            remaining_volume = position.volume - partial_volume
                            if remaining_volume >= 0.01:
                                self.connector.modify_position(position.ticket, stop_loss=entry_price, take_profit=0)
                                self.position_initial_volumes[position.ticket] = remaining_volume
                    except Exception as e:
                        self.logger.log_error(f"Fout bij gedeeltelijke winstneming voor {symbol}: {e}")

            elif (
                    time_condition_met and current_price > profit_target_2 and position.ticket in self.position_initial_volumes):
                initial_volume = self.position_initial_volumes[position.ticket]
                remaining_pct = 0.6
                partial_volume = round(initial_volume * remaining_pct * 0.5, 2)
                if position.volume >= partial_volume and partial_volume >= 0.01:
                    self.logger.log_info(f"Gedeeltelijke winstneming (30%) voor {symbol} op {current_price}")
                    try:
                        partial_result = self.connector.place_order(
                            "SELL", symbol, partial_volume, 0, 0, f"Partial Profit 30% - ticket:{position.ticket}"
                        )
                        if partial_result:
                            self.logger.log_trade(symbol, "SELL", current_price, partial_volume, 0, 0,
                                                  "Partial Profit 30%")
                            remaining_volume = position.volume - partial_volume
                            if remaining_volume >= 0.01:
                                new_sl = entry_price + ((current_price - entry_price) * 0.5)
                                self.connector.modify_position(position.ticket, stop_loss=new_sl, take_profit=0)
                                self.position_initial_volumes[position.ticket] = remaining_volume
                    except Exception as e:
                        self.logger.log_error(f"Fout bij tweede winstneming voor {symbol}: {e}")

            elif current_price < last_low_exit:
                self.logger.log_info(f"Exit signaal voor {symbol} op {current_price}")
                try:
                    close_result = self.connector.place_order(
                        "SELL", symbol, position.volume, 0, 0,
                        f"{'Swing' if self.swing_mode else 'Turtle'} Exit - ticket:{position.ticket}"
                    )
                    if close_result:
                        self.logger.log_trade(
                            symbol, "SELL", current_price, position.volume, 0, 0,
                            f"{'Swing' if self.swing_mode else 'Turtle'} System Exit"
                        )
                        if position.ticket in self.position_initial_volumes:
                            del self.position_initial_volumes[position.ticket]
                except Exception as e:
                    self.logger.log_error(f"Fout bij sluiten positie voor {symbol}: {e}")

    def get_open_positions(self) -> Dict[str, List]:
        """
        Haal alle open posities op per symbool.

        Returns:
        --------
        Dict[str, List]
            Dictionary met open posities per symbool.
        """
        result = {}
        symbols = self.config.get('mt5', {}).get('symbols', [])
        for symbol in symbols:
            positions = self.connector.get_open_positions(symbol)
            if positions:
                result[symbol] = positions
        return result
```

-----------

Path: Sophy_temp/src/utils/__init__.py

```python
```

-----------

Path: Sophy_temp/src/utils/config.py

```python
# src/utils/config.py
import json
import os
from typing import Dict, Any


def load_config(config_path: str = None) -> Dict[str, Any]:
    """
    Laad configuratie uit JSON bestand met validatie

    Parameters:
    -----------
    config_path : str, optional
        Pad naar het configuratiebestand. Als niet opgegeven wordt standaard pad gebruikt.

    Returns:
    --------
    Dict[str, Any] : Geladen configuratie

    Raises:
    -------
    FileNotFoundError : Als het configuratiebestand niet gevonden kan worden
    ValueError : Als het configuratiebestand ongeldige JSON bevat
    """
    if config_path is None:
        config_path = os.environ.get("SOPHY_CONFIG_PATH", "config/settings.json")

    try:
        with open(config_path, 'r') as file:
            config = json.load(file)

        # Valideer vereiste secties
        required_sections = ['mt5', 'risk', 'strategy']
        for section in required_sections:
            if section not in config:
                raise ValueError(f"Sectie '{section}' ontbreekt in configuratie")

        # Pas standaardwaarden toe
        if 'mt5' in config:
            config['mt5'].setdefault('timeframe', 'H4')
            config['mt5'].setdefault('symbols', ['EURUSD'])
            config['mt5'].setdefault('account_balance', 100000)

        if 'risk' in config:
            config['risk'].setdefault('max_risk_per_trade', 0.01)
            config['risk'].setdefault('max_daily_drawdown', 0.05)
            config['risk'].setdefault('max_total_drawdown', 0.10)
            config['risk'].setdefault('leverage', 30)

        if 'logging' not in config:
            config['logging'] = {'log_file': 'logs/trading_log.csv', 'log_level': 'INFO'}

        return config
    except FileNotFoundError:
        print(f"Configuratiebestand niet gevonden: {config_path}")
        raise
    except json.JSONDecodeError as e:
        print(f"Ongeldige JSON in configuratiebestand: {config_path}")
        raise ValueError(f"Ongeldige JSON in configuratiebestand: {str(e)}")
```

-----------

Path: Sophy_temp/src/utils/indicators.py

```python
# sophy/utils/indicators.py
from typing import Tuple

import numpy as np
import pandas as pd


def calculate_atr(df: pd.DataFrame, period: int = 14) -> np.ndarray:
    """
    Bereken Average True Range (ATR) met gevectoriseerde operaties

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame met OHLC data
    period : int
        ATR berekening periode

    Returns:
    --------
    np.ndarray : Array met ATR waarden
    """
    high = df['high'].values
    low = df['low'].values
    close = np.roll(df['close'].values, 1)
    close[0] = 0

    # Bereken true range componenten
    tr1 = high - low
    tr2 = np.abs(high - close)
    tr3 = np.abs(low - close)

    # Bereken true range als maximum van componenten
    tr = np.maximum(np.maximum(tr1, tr2), tr3)

    # Bereken ATR met rollend gemiddelde
    atr = np.zeros_like(tr)
    for i in range(len(tr)):
        if i < period:
            atr[i] = np.mean(tr[0:i + 1]) if i > 0 else tr[0]
        else:
            atr[i] = np.mean(tr[i - period + 1:i + 1])

    return atr


def calculate_donchian_channel(df: pd.DataFrame, period: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Bereken Donchian Channel met gevectoriseerde operaties

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame met OHLC data
    period : int
        Lookback periode

    Returns:
    --------
    Tuple[np.ndarray, np.ndarray] : Upper en lower channel waarden
    """
    # Implementatie...
```

-----------

Path: Sophy_temp/src/utils/logger.py

```python
import csv
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional


class Logger:
    """Verbeterde klasse voor logging van trades en botactiviteit"""

    def __init__(self, log_file_path: str):
        """
        Initialiseer de logger.

        Parameters:
        -----------
        log_file_path : str
            Pad naar het logbestand.
        """
        self.log_file = log_file_path

        # Maak log directory indien nodig
        log_dir = os.path.dirname(log_file_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        self.setup_log_file()

        # Logging voor performance statistieken
        self.stats_file = os.path.join(os.path.dirname(log_file_path), 'performance_stats.json')
        self.initialize_stats()

    def setup_log_file(self):
        """Bereid logbestand voor als het nog niet bestaat."""
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    'Timestamp', 'Type', 'Symbol', 'Action',
                    'Price', 'Volume', 'StopLoss', 'TakeProfit',
                    'Comment', 'Leverage', 'TrendStrength', 'Balance'
                ])
                # Voeg initiële INFO regel toe
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                writer.writerow([
                    timestamp, 'INFO', '', '', '', '', '', '',
                    'Log gestart', '', '', ''
                ])

    def initialize_stats(self):
        """Initialiseer performance statistieken bestand als het nog niet bestaat."""
        if not os.path.exists(self.stats_file):
            default_stats = {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'break_even_trades': 0,
                'win_rate': 0.0,
                'avg_win': 0.0,
                'avg_loss': 0.0,
                'profit_factor': 0.0,
                'max_drawdown': 0.0,
                'net_profit': 0.0,
                'trades_by_symbol': {},
                'daily_performance': {},
                'trade_history': []
            }
            with open(self.stats_file, 'w') as file:
                json.dump(default_stats, file, indent=4)

    def log_trade(self, symbol: str, action: str, price: float, volume: float, sl: float, tp: float,
                  comment: str, leverage: Optional[float] = None, trend_strength: Optional[float] = None,
                  balance: Optional[float] = None):
        """
        Log een trade naar CSV met uitgebreide informatie.

        Parameters:
        -----------
        symbol : str
            Handelssymbool.
        action : str
            Trade actie (BUY, SELL, etc.).
        price : float
            Uitvoeringsprijs.
        volume : float
            Order volume.
        sl : float
            Stop Loss prijs.
        tp : float
            Take Profit prijs.
        comment : str
            Commentaar bij de trade.
        leverage : float, optional
            Gebruikte hefboom.
        trend_strength : float, optional
            Sterkte van de trend op moment van trade.
        balance : float, optional
            Account balans na trade.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp, 'TRADE', symbol, action,
                price, volume, sl, tp, comment,
                leverage if leverage is not None else '', trend_strength if trend_strength is not None else '',
                balance if balance is not None else ''
            ])

        # Log ook naar trade history voor performancetracking
        self.update_trade_stats(timestamp, symbol, action, price, volume, comment)

    def log_info(self, message: str, level: str = "INFO"):
        """
        Log een informatiebericht.

        Parameters:
        -----------
        message : str
            Het te loggen bericht.
        level : str, optional
            Logniveau (INFO, WARNING, ERROR, DEBUG).
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp, level, '', '', '', '', '', '',
                message, '', '', ''
            ])
        print(f"[{timestamp}] {level}: {message}")

    def log_status(self, account_info: Dict[str, Any], open_positions: Dict[str, Any]):
        """
        Log huidige account status.

        Parameters:
        -----------
        account_info : dict
            Informatie over de account.
        open_positions : dict
            Informatie over open posities.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        positions_count = sum(len(pos_list) for pos_list in open_positions.values()) if open_positions else 0
        positions_detail = ", ".join(
            f"{symbol}:{pos.volume}@{((pos.profit / account_info.get('balance', 100000)) * 100):.2f}%"
            for symbol, pos_list in open_positions.items()
            for pos in pos_list
        ) if positions_count > 0 else ""

        equity = account_info.get('equity', 0)
        balance = account_info.get('balance', 0)
        margin = account_info.get('margin', 0)
        margin_level = (equity / margin * 100) if margin > 0 else 0
        floating_pnl = equity - balance

        status_message = (
            f"Balance: {balance}, Equity: {equity}, Floating P/L: {floating_pnl:.2f}, "
            f"Margin Level: {margin_level:.2f}%, Open positions: {positions_count}"
        )
        if positions_detail:
            status_message += f" ({positions_detail})"

        with open(self.log_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp, 'STATUS', '', '', '', '', '', '',
                status_message, '', '', balance
            ])

    def update_trade_stats(self, timestamp: str, symbol: str, action: str, price: float, volume: float,
                           comment: str):
        """
        Update performance statistieken na een trade.

        Parameters:
        -----------
        timestamp : str
            Tijdstempel van de trade.
        symbol : str
            Handelssymbool.
        action : str
            Trade actie (BUY, SELL, etc.).
        price : float
            Uitvoeringsprijs.
        volume : float
            Order volume.
        comment : str
            Commentaar bij de trade.
        """
        try:
            if not os.path.exists(self.stats_file):
                self.initialize_stats()

            with open(self.stats_file, 'r') as file:
                stats = json.load(file)

            # Voeg trade toe aan geschiedenis
            trade_record = {
                'timestamp': timestamp,
                'symbol': symbol,
                'action': action,
                'price': price,
                'volume': volume,
                'comment': comment
            }
            stats['trade_history'].append(trade_record)

            # Bijhouden trades per symbool
            if symbol not in stats['trades_by_symbol']:
                stats['trades_by_symbol'][symbol] = {'total': 0, 'buys': 0, 'sells': 0}
            stats['trades_by_symbol'][symbol]['total'] += 1
            if action == 'BUY':
                stats['trades_by_symbol'][symbol]['buys'] += 1
            elif action == 'SELL':
                stats['trades_by_symbol'][symbol]['sells'] += 1

            # Update algemene statistieken
            stats['total_trades'] += 1

            # Sla bijgewerkte statistieken op
            with open(self.stats_file, 'w') as file:
                json.dump(stats, file, indent=4)
        except json.JSONDecodeError:
            self.initialize_stats()  # Herinitialiseer bij corrupte JSON
            self.log_info("Stats bestand herinitialiseerd vanwege corrupte data", level="WARNING")
        except Exception as e:
            self.log_info(f"Fout bij bijwerken statistieken: {e}", level="ERROR")

    def log_performance_metrics(self, metrics: Dict[str, Any]):
        """
        Log prestatiemetrieken.

        Parameters:
        -----------
        metrics : dict
            Dictionary met prestatiemetrieken.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        metrics_str = ", ".join(f"{k}: {v}" for k, v in metrics.items() if k != 'trade_history')

        try:
            with open(self.log_file, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([timestamp, 'METRICS', '', '', '', '', '', '', metrics_str, '', '', ''])

            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r') as file:
                    stats = json.load(file)
                for k, v in metrics.items():
                    if k in stats and k != 'trade_history':
                        stats[k] = v
                with open(self.stats_file, 'w') as file:
                    json.dump(stats, file, indent=4)
        except Exception as e:
            self.log_info(f"Fout bij loggen van metrics: {e}", level="ERROR")
```

-----------

Path: Sophy_temp/src/utils/visualizer.py

```python
import json
import os
from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


class Visualizer:
    """Verbeterde klasse voor visualisatie van trading resultaten"""

    def __init__(self, log_file, output_dir='data'):
        """
        Initialiseer de visualizer

        Parameters:
        -----------
        log_file : str
            Pad naar het logbestand
        output_dir : str, optional
            Map voor het opslaan van grafieken
        """
        self.log_file = log_file
        self.output_dir = output_dir

        # Stel visualisatiestijl in
        plt.style.use('ggplot')
        plt.rcParams['figure.figsize'] = (16, 10)
        plt.rcParams['lines.linewidth'] = 1.5
        sns.set_style("whitegrid")

        # Maak output map aan als deze niet bestaat
        os.makedirs(output_dir, exist_ok=True)

        # Pad naar presentation stats file
        log_dir = os.path.dirname(log_file)
        self.stats_file = os.path.join(log_dir, 'performance_stats.json')

    def load_trade_data(self):
        """
        Laad trade data uit het logbestand

        Returns:
        --------
        pandas.DataFrame
            DataFrame met trade data
        """
        try:
            df = pd.read_csv(self.log_file)
            # Converteer timestamp naar datetime
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            return df
        except Exception as e:
            print(f"Fout bij laden van trade data: {e}")
            return pd.DataFrame()

    def load_performance_stats(self):
        """
        Laad presentation statistieken uit JSON bestand

        Returns:
        --------
        dict
            Dictionary met performancestatistieken
        """
        if not os.path.exists(self.stats_file):
            print(f"Performance stats bestand niet gevonden: {self.stats_file}")
            return {}

        try:
            with open(self.stats_file, 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f"Fout bij laden van presentation stats: {e}")
            return {}

    def plot_equity_curve(self, include_drawdown=True):
        """
        Plot de equity curve met uitgebreide metrics

        Parameters:
        -----------
        include_drawdown : bool, optional
            Of drawdown analyse moet worden toegevoegd

        Returns:
        --------
        str
            Pad naar de opgeslagen grafiek
        """
        df = self.load_trade_data()
        if df.empty:
            print("Geen data beschikbaar voor equity curve")
            return None

        # Filter alleen op STATUS rijen
        status_df = df[df['Type'] == 'STATUS'].copy()
        if status_df.empty:
            print("Geen status data beschikbaar voor equity curve")
            return None

        # Extraheer balance en equity uit Comment kolom
        balances = []
        equities = []
        timestamps = []

        for _, row in status_df.iterrows():
            comment = row['Comment']
            timestamp = row['Timestamp']
            balance = row.get('Balance', None)

            # Probeer eerst uit de Balance kolom te halen
            if pd.notna(balance) and balance != '':
                balances.append(float(balance))
                timestamps.append(timestamp)
            else:
                # Als dat niet lukt, probeer uit de Comment te extraheren
                balance_str = comment.split('Balance: ')[1].split(',')[0] if 'Balance: ' in comment else None
                if balance_str and balance_str != 'N/A':
                    balances.append(float(balance_str))
                    timestamps.append(timestamp)

            # Extraheer equity uit comment
            equity_str = comment.split('Equity: ')[1].split(',')[0] if 'Equity: ' in comment else None
            if equity_str and equity_str != 'N/A':
                equities.append(float(equity_str))

        if not balances:
            print("Geen balance data gevonden voor equity curve")
            return None

        # Maak dataframe voor analyse
        equity_df = pd.DataFrame({
            'timestamp': timestamps,
            'balance': balances
        })

        if len(equities) == len(balances):
            equity_df['equity'] = equities

        # Bereken drawdown als die er is
        if 'equity' in equity_df.columns:
            equity_df['peak'] = equity_df['equity'].cummax()
            equity_df['drawdown'] = (equity_df['equity'] - equity_df['peak']) / equity_df['peak'] * 100
        else:
            equity_df['peak'] = equity_df['balance'].cummax()
            equity_df['drawdown'] = (equity_df['balance'] - equity_df['peak']) / equity_df['peak'] * 100

        # Bereken prestatie-metrieken
        initial_balance = equity_df['balance'].iloc[0] if not equity_df.empty else 100000
        final_balance = equity_df['balance'].iloc[-1] if not equity_df.empty else initial_balance
        total_return = ((final_balance / initial_balance) - 1) * 100
        max_drawdown = equity_df['drawdown'].min() if 'drawdown' in equity_df.columns else 0

        # Maak equity curve plot
        fig, axes = plt.subplots(2, 1, figsize=(16, 12), gridspec_kw={'height_ratios': [3, 1]})

        # Bovenste plot: Equity curve
        if 'equity' in equity_df.columns:
            axes[0].plot(equity_df['timestamp'], equity_df['equity'], label='Equity', color='blue', linewidth=2)

        axes[0].plot(equity_df['timestamp'], equity_df['balance'], label='Balance', color='green', linewidth=2)
        axes[0].plot(equity_df['timestamp'], equity_df['peak'], label='Peak Balance', color='darkgreen', linestyle='--',
                     alpha=0.6)

        # Voeg horizontale lijn toe voor beginbalans
        axes[0].axhline(y=initial_balance, color='gray', linestyle=':', alpha=0.8, label='Initial Balance')

        # Voeg horizontale lijnen toe voor 5% en 10% winst
        axes[0].axhline(y=initial_balance * 1.05, color='orange', linestyle=':', alpha=0.8, label='5% Profit')
        axes[0].axhline(y=initial_balance * 1.10, color='darkgreen', linestyle=':', alpha=0.8,
                        label='10% Profit (Target)')

        # Voeg horizontale lijnen toe voor FTMO limieten
        axes[0].axhline(y=initial_balance * 0.95, color='yellow', linestyle=':', alpha=0.8,
                        label='5% Loss (Daily Limit)')
        axes[0].axhline(y=initial_balance * 0.90, color='red', linestyle=':', alpha=0.8,
                        label='10% Loss (Max Drawdown)')

        # Voeg trade markers toe (optioneel)
        trade_df = df[df['Type'] == 'TRADE']
        if not trade_df.empty:
            buy_df = trade_df[trade_df['Action'] == 'BUY']
            sell_df = trade_df[trade_df['Action'] == 'SELL']

            if not buy_df.empty:
                axes[0].scatter(buy_df['Timestamp'], [initial_balance] * len(buy_df), marker='^', color='green',
                                s=80, label='Buy', alpha=0.7)
            if not sell_df.empty:
                axes[0].scatter(sell_df['Timestamp'], [initial_balance] * len(sell_df), marker='v', color='red',
                                s=80, label='Sell', alpha=0.7)

        # Formateer bovenste plot
        axes[0].set_title('Equity Curve & Balance History', fontsize=16)
        axes[0].set_ylabel('Account Value ($)', fontsize=14)
        axes[0].legend(loc='upper left', fontsize=12)
        axes[0].grid(True)

        # Voeg metrics toe aan de plot
        info_text = (
            f"Initial Balance: ${initial_balance:,.2f}\n"
            f"Final Balance: ${final_balance:,.2f}\n"
            f"Total Return: {total_return:.2f}%\n"
            f"Max Drawdown: {max_drawdown:.2f}%"
        )

        # Plaats info tekst in de rechterbovenhoek
        axes[0].text(0.02, 0.02, info_text, transform=axes[0].transAxes, fontsize=12,
                     bbox=dict(facecolor='white', alpha=0.7), verticalalignment='bottom')

        # Onderste plot: Drawdown
        axes[1].fill_between(equity_df['timestamp'], equity_df['drawdown'], 0,
                             color='red', alpha=0.3, label='Drawdown')
        axes[1].plot(equity_df['timestamp'], equity_df['drawdown'], color='red', linewidth=1)

        # Voeg horizontale lijnen toe voor drawdown limieten
        axes[1].axhline(y=-5, color='yellow', linestyle=':', alpha=0.8, label='5% Drawdown (Daily Limit)')
        axes[1].axhline(y=-10, color='red', linestyle=':', alpha=0.8, label='10% Drawdown (Max Limit)')

        # Formateer onderste plot
        axes[1].set_title('Drawdown (%)', fontsize=14)
        axes[1].set_xlabel('Datum', fontsize=14)
        axes[1].set_ylabel('Drawdown (%)', fontsize=14)
        axes[1].legend(loc='lower left', fontsize=12)
        axes[1].set_ylim(min(equity_df['drawdown'].min() * 1.2, -12), 1)  # Zorg voor goede y-as limieten
        axes[1].grid(True)

        # Formateer x-as voor beide plots
        for ax in axes:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax.xaxis.set_major_locator(mdates.AutoDateLocator())
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

        plt.tight_layout()

        # Sla grafiek op
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"equity_curve_{timestamp}.png")
        plt.savefig(output_path, dpi=150)
        plt.close()

        print(f"Equity curve opgeslagen als {output_path}")
        return output_path

    def plot_trade_results(self):
        """
        Plot de resultaten van trades

        Returns:
        --------
        str
            Pad naar de opgeslagen grafiek
        """
        df = self.load_trade_data()
        if df.empty:
            print("Geen data beschikbaar voor trade resultaten")
            return None

        # Filter alleen op TRADE rijen
        trade_df = df[df['Type'] == 'TRADE']
        if trade_df.empty:
            print("Geen trade data beschikbaar")
            return None

        # Groepeer trades per symbool
        symbols = trade_df['Symbol'].unique()

        # Bereken aantal figuren nodig (1 rij per symbool)
        num_symbols = len(symbols)

        # Maak plot voor elk symbool
        fig, axes = plt.subplots(num_symbols, 1, figsize=(16, 6 * num_symbols), squeeze=False)

        for i, symbol in enumerate(symbols):
            symbol_df = trade_df[trade_df['Symbol'] == symbol]

            # Converteer kolommen naar numeriek waar nodig
            for col in ['Price', 'Volume', 'StopLoss', 'TakeProfit', 'Leverage', 'TrendStrength']:
                if col in symbol_df.columns:
                    symbol_df[col] = pd.to_numeric(symbol_df[col], errors='coerce')

            # Filter buys en sells
            buys = symbol_df[symbol_df['Action'] == 'BUY']
            sells = symbol_df[symbol_df['Action'] == 'SELL']

            ax = axes[i, 0]

            # Plot trades
            if not buys.empty:
                ax.scatter(buys['Timestamp'], buys['Price'], color='green', marker='^', s=100, label='Buy')

                # Maak grootte van markers proportioneel aan volume
                if 'Volume' in buys.columns:
                    sizes = buys['Volume'] * 50 + 50  # Schaal volume voor marker grootte
                    ax.scatter(buys['Timestamp'], buys['Price'], s=sizes, color='green', marker='^', alpha=0.5)

                # Plot stop losses voor buy orders
                for _, row in buys.iterrows():
                    if pd.notna(row.get('StopLoss', None)) and row['StopLoss'] > 0:
                        ax.plot([row['Timestamp'], row['Timestamp']],
                                [row['Price'], row['StopLoss']],
                                'r--', alpha=0.5)

            if not sells.empty:
                ax.scatter(sells['Timestamp'], sells['Price'], color='red', marker='v', s=100, label='Sell')

                # Maak grootte van markers proportioneel aan volume
                if 'Volume' in sells.columns:
                    sizes = sells['Volume'] * 50 + 50
                    ax.scatter(sells['Timestamp'], sells['Price'], s=sizes, color='red', marker='v', alpha=0.5)

            # Bereken en toon winst/verlies per trade als mogelijk
            paired_trades = self._pair_trades(symbol_df)
            for pair in paired_trades:
                if len(pair) == 2:  # Alleen complete trade paren
                    buy = pair[0]
                    sell = pair[1]
                    profit_pct = ((sell['Price'] - buy['Price']) / buy['Price']) * 100

                    # Toon label voor het resultaat
                    mid_time = buy['Timestamp'] + (sell['Timestamp'] - buy['Timestamp']) / 2
                    mid_price = (buy['Price'] + sell['Price']) / 2

                    color = 'green' if profit_pct > 0 else 'red'
                    ax.text(mid_time, mid_price, f"{profit_pct:.1f}%",
                            color=color, fontweight='bold', ha='center')

                    # Verbind buy en sell punt met lijn
                    ax.plot([buy['Timestamp'], sell['Timestamp']],
                            [buy['Price'], sell['Price']],
                            color=color, linestyle='-', alpha=0.5)

            # Formateer plot
            ax.set_title(f'Trades voor {symbol}', fontsize=16)
            ax.set_ylabel('Prijs', fontsize=14)

            # Voeg gridlines toe
            ax.grid(True)
            ax.legend(loc='upper left', fontsize=12)

            # Voeg labels toe voor buy/sell punten
            for idx, row in buys.iterrows():
                volume_str = f"{row['Volume']}" if 'Volume' in row else ""
                ax.annotate(volume_str,
                            xy=(row['Timestamp'], row['Price']),
                            xytext=(5, 5), textcoords='offset points',
                            fontsize=9, color='darkgreen')

            for idx, row in sells.iterrows():
                volume_str = f"{row['Volume']}" if 'Volume' in row else ""
                ax.annotate(volume_str,
                            xy=(row['Timestamp'], row['Price']),
                            xytext=(5, -15), textcoords='offset points',
                            fontsize=9, color='darkred')

            # Formateer x-as
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
            ax.xaxis.set_major_locator(mdates.AutoDateLocator())
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

        plt.xlabel('Tijd', fontsize=14)
        plt.tight_layout()

        # Sla grafiek op
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"trade_results_{timestamp}.png")
        plt.savefig(output_path, dpi=150)
        plt.close()

        print(f"Trade resultaten opgeslagen als {output_path}")
        return output_path

    def _pair_trades(self, trade_df):
        """
        Groepeer trades in buy/sell paren

        Parameters:
        -----------
        trade_df : pandas.DataFrame
            DataFrame met trades voor één symbool

        Returns:
        --------
        list
            Lijst met paren van trades (buy/sell)
        """
        # Sorteer trades op tijdstempel
        sorted_trades = trade_df.sort_values('Timestamp').to_dict('records')

        # Verzamel paren
        pairs = []
        current_pair = []

        for trade in sorted_trades:
            if trade['Action'] == 'BUY':
                # Als we al een open pair hebben, sluit deze eerst af
                if current_pair:
                    pairs.append(current_pair)
                    current_pair = [trade]
                else:
                    current_pair = [trade]
            elif trade['Action'] == 'SELL' and current_pair:
                current_pair.append(trade)
                pairs.append(current_pair)
                current_pair = []

        # Voeg laatste onvolledige paar toe indien aanwezig
        if current_pair:
            pairs.append(current_pair)

        return pairs

    def plot_performance_summary(self):
        """
        Plot een samenvatting van de handelsperformance

        Returns:
        --------
        str
            Pad naar de opgeslagen grafiek
        """
        # Laad trade data
        df = self.load_trade_data()
        stats = self.load_performance_stats()

        if df.empty:
            print("Geen data beschikbaar voor presentation summary")
            return None

        # Filter trades
        trade_df = df[df['Type'] == 'TRADE'].copy()

        if trade_df.empty:
            print("Geen trade data beschikbaar voor analyse")
            return None

        # Converteer numerieke kolommen
        for col in ['Price', 'Volume', 'StopLoss', 'TakeProfit']:
            if col in trade_df.columns:
                trade_df[col] = pd.to_numeric(trade_df[col], errors='coerce')

        # Bereken metrics
        trades_by_symbol = {}
        symbol_performance = {}

        for symbol in trade_df['Symbol'].unique():
            symbol_df = trade_df[trade_df['Symbol'] == symbol]

            # Basic count metrics
            buys = symbol_df[symbol_df['Action'] == 'BUY']
            sells = symbol_df[symbol_df['Action'] == 'SELL']

            trades_by_symbol[symbol] = {
                'buys': len(buys),
                'sells': len(sells),
                'total': len(symbol_df)
            }

            # Bereken presentation als mogelijk
            pairs = self._pair_trades(symbol_df)
            wins = 0
            losses = 0
            total_profit_pct = 0
            total_loss_pct = 0

            for pair in pairs:
                if len(pair) == 2:  # Alleen complete trades
                    buy = pair[0]
                    sell = pair[1]

                    profit_pct = ((sell['Price'] - buy['Price']) / buy['Price']) * 100

                    if profit_pct > 0:
                        wins += 1
                        total_profit_pct += profit_pct
                    else:
                        losses += 1
                        total_loss_pct += profit_pct

            total_complete_trades = wins + losses
            win_rate = wins / total_complete_trades if total_complete_trades > 0 else 0
            avg_win = total_profit_pct / wins if wins > 0 else 0
            avg_loss = total_loss_pct / losses if losses > 0 else 0
            profit_factor = abs(total_profit_pct / total_loss_pct) if total_loss_pct < 0 else float('inf')

            symbol_performance[symbol] = {
                'win_rate': win_rate,
                'wins': wins,
                'losses': losses,
                'avg_win': avg_win,
                'avg_loss': avg_loss,
                'profit_factor': profit_factor,
                'net_profit_pct': total_profit_pct + total_loss_pct
            }

        # Maak plot
        fig = plt.figure(figsize=(20, 16))

        # Definieer grid layout
        gs = fig.add_gridspec(3, 2, height_ratios=[1, 1, 1])

        # 1. Win/Loss Ratio per Symbol (Pie chart)
        ax1 = fig.add_subplot(gs[0, 0])

        symbols = list(symbol_performance.keys())
        win_rates = [symbol_performance[s]['win_rate'] * 100 for s in symbols]

        # Kleuren gebaseerd op win rate (rood naar groen)
        colors = [(1 - wr / 100, wr / 100, 0) for wr in win_rates]

        ax1.bar(symbols, win_rates, color=colors)
        ax1.set_title('Win Rate per Symbol (%)', fontsize=14)
        ax1.set_ylim(0, 100)
        ax1.grid(axis='y')

        # Voeg datawaarden toe aan bars
        for i, v in enumerate(win_rates):
            ax1.text(i, v + 1, f"{v:.1f}%", ha='center', fontsize=12)

        # 2. Average Win vs Loss per Symbol
        ax2 = fig.add_subplot(gs[0, 1])

        # Verzamel data
        symbols = list(symbol_performance.keys())
        avg_wins = [symbol_performance[s]['avg_win'] for s in symbols]
        avg_losses = [abs(symbol_performance[s]['avg_loss']) for s in symbols]

        x = np.arange(len(symbols))
        width = 0.35

        ax2.bar(x - width / 2, avg_wins, width, label='Avg Win %', color='green', alpha=0.7)
        ax2.bar(x + width / 2, avg_losses, width, label='Avg Loss %', color='red', alpha=0.7)

        ax2.set_title('Average Win vs Loss (%)', fontsize=14)
        ax2.set_xticks(x)
        ax2.set_xticklabels(symbols)
        ax2.legend()
        ax2.grid(axis='y')

        # 3. Net Profit per Symbol
        ax3 = fig.add_subplot(gs[1, 0])

        net_profits = [symbol_performance[s]['net_profit_pct'] for s in symbols]
        colors = ['green' if p > 0 else 'red' for p in net_profits]

        ax3.bar(symbols, net_profits, color=colors, alpha=0.7)
        ax3.set_title('Net Profit per Symbol (%)', fontsize=14)
        ax3.grid(axis='y')

        # Voeg datawaarden toe
        for i, v in enumerate(net_profits):
            ax3.text(i, v + (0.1 if v >= 0 else -2), f"{v:.1f}%", ha='center', fontsize=12)

        # 4. Trades per Symbol
        ax4 = fig.add_subplot(gs[1, 1])

        # Verzamel data
        buys_per_symbol = [trades_by_symbol[s]['buys'] for s in symbols]
        sells_per_symbol = [trades_by_symbol[s]['sells'] for s in symbols]

        ax4.bar(x - width / 2, buys_per_symbol, width, label='Buy Orders', color='green', alpha=0.7)
        ax4.bar(x + width / 2, sells_per_symbol, width, label='Sell Orders', color='red', alpha=0.7)

        ax4.set_title('Number of Trades per Symbol', fontsize=14)
        ax4.set_xticks(x)
        ax4.set_xticklabels(symbols)
        ax4.legend()
        ax4.grid(axis='y')

        # 5. Overall Performance Metrics Table
        ax5 = fig.add_subplot(gs[2, :])
        ax5.axis('off')

        # Bereken totalen over alle symbolen
        total_trades = sum(trades_by_symbol[s]['total'] for s in symbols)
        total_wins = sum(symbol_performance[s]['wins'] for s in symbols)
        total_losses = sum(symbol_performance[s]['losses'] for s in symbols)

        total_win_rate = total_wins / (total_wins + total_losses) * 100 if (total_wins + total_losses) > 0 else 0
        total_profit = sum(symbol_performance[s]['net_profit_pct'] for s in symbols)

        # Custom tabel
        overall_metrics = [
            ('Total Trades', f"{total_trades}"),
            ('Win Rate', f"{total_win_rate:.1f}%"),
            ('Winning Trades', f"{total_wins}"),
            ('Losing Trades', f"{total_losses}"),
            ('Net Profit %', f"{total_profit:.2f}%"),
        ]

        table_data = []
        for metric, value in overall_metrics:
            table_data.append([metric, value])

        tbl = ax5.table(
            cellText=table_data,
            colLabels=['Metric', 'Value'],
            loc='center',
            cellLoc='center',
            colWidths=[0.3, 0.3]
        )

        tbl.auto_set_font_size(False)
        tbl.set_fontsize(14)
        tbl.scale(1, 2)

        # Stel kleuren in
        header_color = '#40466e'
        cell_color = '#f1f1f2'

        for i, key in enumerate(tbl.get_celld().keys()):
            cell = tbl.get_celld()[key]
            if i == 0:  # Header row
                cell.set_facecolor(header_color)
                cell.set_text_props(color='white', fontweight='bold')
            else:
                cell.set_facecolor(cell_color)

        ax5.set_title('Overall Performance Metrics', fontsize=16, pad=20)

        plt.tight_layout()

        # Sla grafiek op
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"performance_summary_{timestamp}.png")
        plt.savefig(output_path, dpi=150)
        plt.close()

        print(f"Performance samenvatting opgeslagen als {output_path}")
        return output_path
```

-----------

Path: Sophy_temp/tests/fixtures/__init__.py

```python
```

-----------

Path: Sophy_temp/tests/integration/test_mt5_connectivity.py

```python
# tests/integration/test_mt5_connectivity.py
from datetime import datetime, timedelta

import pytest
from turtle_trader.data.mt5_connector import MT5Connector
from turtle_trader.utils.config import load_config


@pytest.fixture
def mt5_connector():
    """Create a connector instance with test configuration"""
    config = load_config("tests/config/test_config.json")
    from turtle_trader.utils.logger import Logger
    logger = Logger("tests/logs/test_log.csv")
    return MT5Connector(config['mt5'], logger)


def test_mt5_connection(mt5_connector):
    """Test connection to MT5 platform"""
    # Connect to MT5
    connected = mt5_connector.connect()
    assert connected, "Failed to connect to MT5"

    # Clean up
    mt5_connector.disconnect()


def test_historical_data_retrieval(mt5_connector):
    """Test retrieving historical data from MT5"""
    # Connect to MT5
    connected = mt5_connector.connect()
    assert connected, "Failed to connect to MT5"

    # Get historical data
    symbol = "EURUSD"
    end_date = datetime.now()
    start_date = end_date - timedelta(days=5)

    df = mt5_connector.get_historical_data(symbol, 16, 100)  # 16 = H4 timeframe

    # Validate data
    assert not df.empty, "No historical data retrieved"
    assert 'open' in df.columns, "Data missing expected columns"
    assert 'high' in df.columns, "Data missing expected columns"
    assert 'low' in df.columns, "Data missing expected columns"
    assert 'close' in df.columns, "Data missing expected columns"

    # Clean up
    mt5_connector.disconnect()
```

-----------

Path: Sophy_temp/tests/performance/__init__.py

```python
```

-----------

Path: Sophy_temp/tests/unit/__init__.py

```python
```

-----------

Path: Sophy_temp/tests/unit/test_risk_manager.py

```python
# tests/unit/test_risk_manager.py
import os
import sys
import unittest
from unittest.mock import MagicMock

# Voeg project root toe aan sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.risk.risk_manager import RiskManager


class TestRiskManager(unittest.TestCase):
    def setUp(self):
        # Maak een mock logger
        self.logger = MagicMock()
        self.logger.log_info = MagicMock()

        # Standaard configuratie
        self.config = {
            'max_risk_per_trade': 0.01,
            'max_daily_drawdown': 0.05,
            'max_total_drawdown': 0.10,
            'leverage': 30,
            'account_balance': 100000
        }

        # Initialiseer risk manager
        self.risk_manager = RiskManager(self.config, self.logger)

    def test_check_ftmo_limits_profit_target(self):
        # Test dat winstdoel correct wordt gedetecteerd
        account_info = {
            'balance': 110000,  # 10% winst
            'equity': 110000
        }

        should_stop, reason = self.risk_manager.check_ftmo_limits(account_info)

        self.assertTrue(should_stop)
        self.assertIn("Winstdoel bereikt", reason)

    def test_check_ftmo_limits_daily_drawdown(self):
        # Test dat dagelijkse drawdown limiet correct wordt gedetecteerd
        account_info = {
            'balance': 95000,  # 5% verlies
            'equity': 95000
        }

        should_stop, reason = self.risk_manager.check_ftmo_limits(account_info)

        self.assertTrue(should_stop)
        self.assertIn("Dagelijkse verlieslimiet bereikt", reason)

    def test_check_ftmo_limits_total_drawdown(self):
        # Test dat totale drawdown limiet correct wordt gedetecteerd
        account_info = {
            'balance': 90000,  # 10% verlies
            'equity': 90000
        }

        should_stop, reason = self.risk_manager.check_ftmo_limits(account_info)

        self.assertTrue(should_stop)
        self.assertIn("Maximale drawdown bereikt", reason)

    def test_check_ftmo_limits_no_violations(self):
        # Test dat geen limieten worden geschonden
        account_info = {
            'balance': 105000,  # 5% winst
            'equity': 105000
        }

        should_stop, reason = self.risk_manager.check_ftmo_limits(account_info)

        self.assertFalse(should_stop)
        self.assertIsNone(reason)

    def test_calculate_position_size(self):
        # Test positiegrootte berekening
        entry_price = 1.2000
        stop_loss = 1.1950  # 50 pips
        account_balance = 100000
        trend_strength = 0.8

        position_size = self.risk_manager.calculate_position_size(
            symbol="EURUSD",
            entry_price=entry_price,
            stop_loss=stop_loss,
            account_balance=account_balance,
            trend_strength=trend_strength
        )

        # Handmatige berekening voor vergelijking:
        # risk_amount = 100000 * 0.01 = 1000
        # adjusted_risk = 1000 * (0.5 + 0.8/2) = 1000 * 0.9 = 900
        # pips_at_risk = (1.2000 - 1.1950) / 0.0001 = 50
        # pip_value = 10 (standaard voor 1 lot)
        # lot_size = 900 / (50 * 10) = 1.8

        # We verwachten dat de waarde dichtbij 1.8 ligt (kan afwijken door afrondingen)
        self.assertGreater(position_size, 1.5)
        self.assertLessEqual(position_size, 2.0)

    def test_check_trade_risk(self):
        # Test trade risico validatie
        symbol = "EURUSD"
        volume = 0.5
        entry_price = 1.2000
        stop_loss = 1.1950

        # Reset dagelijkse limieten
        self.risk_manager.daily_trades_count = 0

        result = self.risk_manager.check_trade_risk(symbol, volume, entry_price, stop_loss)

        # We verwachten dat de trade wordt goedgekeurd
        self.assertTrue(result)

        # Test trade limiet per dag
        self.risk_manager.daily_trades_count = self.risk_manager.max_daily_trades

        result = self.risk_manager.check_trade_risk(symbol, volume, entry_price, stop_loss)

        # We verwachten dat de trade wordt afgewezen
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
```

-----------

Path: Sophy_temp/tests/unit/test_turtle_strategy.py

```python
# tests/unit/test_turtle_strategy.py
import os
import sys
import unittest
from unittest.mock import MagicMock

import numpy as np
import pandas as pd

# Voeg project root toe aan sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.strategy.turtle_strategy import TurtleStrategy


class TestTurtleStrategy(unittest.TestCase):
    def setUp(self):
        # Maak mock objecten
        self.connector = MagicMock()
        self.risk_manager = MagicMock()
        self.logger = MagicMock()

        # Standaard configuratie
        self.config = {
            'mt5': {
                'symbols': ['EURUSD', 'GBPUSD'],
                'timeframe': 'H4',
                'account_balance': 100000
            },
            'strategy': {
                'name': 'turtle',
                'swing_mode': False,
                'entry_period': 20,
                'exit_period': 10,
                'atr_period': 20,
                'atr_multiplier': 2.0
            }
        }

        # Initialiseer strategie
        self.strategy = TurtleStrategy(self.connector, self.risk_manager, self.logger, self.config)

    def test_initialization(self):
        # Test dat de strategie correct wordt geïnitialiseerd
        self.assertEqual(self.strategy.name, "Turtle Trading Strategy")
        self.assertEqual(self.strategy.entry_period, 20)
        self.assertEqual(self.strategy.exit_period, 10)
        self.assertEqual(self.strategy.atr_period, 20)
        self.assertEqual(self.strategy.atr_multiplier, 2.0)
        self.assertFalse(self.strategy.swing_mode)

    def test_swing_mode_initialization(self):
        # Test swing mode initialisatie
        config = self.config.copy()
        config['strategy']['swing_mode'] = True

        strategy = TurtleStrategy(self.connector, self.risk_manager, self.logger, config)

        self.assertTrue(strategy.swing_mode)
        self.assertEqual(strategy.entry_period, 40)  # Standaard voor swing mode

    def test_calculate_indicators(self):
        # Maak test data
        dates = pd.date_range(start='2023-01-01', periods=100, freq='4H')
        high = np.random.normal(1.2, 0.01, 100)
        low = high - np.random.uniform(0.001, 0.005, 100)
        close = low + np.random.uniform(0, 0.003, 100)
        open_prices = high - np.random.uniform(0, 0.003, 100)
        volume = np.random.randint(10, 100, 100)

        df = pd.DataFrame({
            'date': dates,
            'open': open_prices,
            'high': high,
            'low': low,
            'close': close,
            'tick_volume': volume
        })

        # Bereken indicatoren
        indicators = self.strategy.calculate_indicators(df)

        # Test dat de belangrijkste indicatoren aanwezig zijn
        self.assertIn('atr', indicators)
        self.assertIn('high_entry', indicators)
        self.assertIn('low_exit', indicators)

    def test_calculate_atr(self):
        # Maak test data
        dates = pd.date_range(start='2023-01-01', periods=50, freq='4H')
        high = np.random.normal(1.2, 0.01, 50)
        low = high - np.random.uniform(0.001, 0.005, 50)
        close = low + np.random.uniform(0, 0.003, 50)

        df = pd.DataFrame({
            'date': dates,
            'high': high,
            'low': low,
            'close': close
        })

        # Bereken ATR
        atr = self.strategy.calculate_atr(df, 14)

        # Test eigenschappen
        self.assertEqual(len(atr), 50)
        self.assertTrue(atr.iloc[-1] > 0)

    def test_process_symbol_no_data(self):
        # Test gedrag wanneer er geen data is
        self.connector.get_historical_data.return_value = pd.DataFrame()

        result = self.strategy.process_symbol('EURUSD')

        # Test dat er geen signaal is
        self.assertIsNone(result.get('signal'))
        self.logger.log_info.assert_called_with("Geen historische data beschikbaar voor EURUSD")

    def test_process_symbol_with_breakout(self):
        # Configureer mocks voor een breakout scenario
        # 1. Maak test data
        dates = pd.date_range(start='2023-01-01', periods=100, freq='4H')
        high = np.random.normal(1.2, 0.01, 100)
        low = high - np.random.uniform(0.001, 0.005, 100)
        close = low + np.random.uniform(0, 0.003, 100)
        open_prices = high - np.random.uniform(0, 0.003, 100)
        volume = np.random.randint(10, 100, 100)

        df = pd.DataFrame({
            'date': dates,
            'open': open_prices,
            'high': high,
            'low': low,
            'close': close,
            'tick_volume': volume
        })

        # Zorg dat laatste candle een breakout is
        df['high'].iloc[-1] = 1.25  # Hogere high voor breakout

        self.connector.get_historical_data.return_value = df

        # 2. Configureer tick
        tick = MagicMock()
        tick.ask = 1.25
        tick.bid = 1.248
        self.connector.get_symbol_tick.return_value = tick

        # 3. Configureer risicomanager
        self.risk_manager.can_trade.return_value = True
        self.risk_manager.calculate_position_size.return_value = 0.5
        self.risk_manager.check_trade_risk.return_value = True

        # 4. Configureer account info
        account_info = {'balance': 100000, 'equity': 100000}
        self.connector.get_account_info.return_value = account_info

        # 5. Configureer order response
        self.connector.place_order.return_value = 12345  # ticket ID

        # Test de processsymbol functie met de ingerichte mocks
        result = self.strategy.process_symbol('EURUSD')

        # Verwacht een entry signaal
        self.assertEqual(result.get('signal'), 'ENTRY')
        self.assertEqual(result.get('action'), 'BUY')
        self.assertEqual(result.get('ticket'), 12345)

        # Controleer dat de place_order functie werd aangeroepen
        self.connector.place_order.assert_called_once()


if __name__ == '__main__':
    unittest.main()
```

-----------

Path: config/settings.json

```json
{
  "mt5": {
    "login": 1520533067,
    "password": "YOUR_PASSWORD",
    "server": "FTMO-Demo2",
    "mt5_pathway": "C:\\Program Files\\FTMO MetaTrader 5\\terminal64.exe",
    "symbols": [
      "EURUSD",
      "XAUUSD",
      "US30"
    ],
    "symbol_mapping": {
      "US30": "US30.cash"
    },
    "timeframe": "H4",
    "account_balance": 100000
  },
  "risk": {
    "max_risk_per_trade": 0.015,
    "max_daily_drawdown": 0.05,
    "max_total_drawdown": 0.10,
    "leverage": 30
  },
  "strategy": {
    "name": "turtle",
    "swing_mode": true,
    "entry_period": 40,
    "exit_period": 20,
    "atr_period": 20,
    "atr_multiplier": 2.5
  },
  "logging": {
    "log_file": "logs/trading_log.csv",
    "log_level": "INFO"
  },
  "output": {
    "data_dir": "data"
  }
}```

-----------

Path: config/strategy_config.json

```json
# config/strategy_config.json
{
"turtle_trader": {
"entry_period": 40,
"exit_period": 20,
"atr_period": 20,
"atr_multiplier": 2.5,
"swing_mode": true,
"use_trend_filter": true
}
}```

-----------

Path: docs/FTMO_Rules.txt

```plaintext
1/15
FTMO GENERAL TERMS AND CONDITIONS
These FTMO General Terms and Conditions (the “GTC”) govern rights and obligations in connection
with the use of services provided by FTMO Evaluation Global s.r.o. (the “Services”), offered mainly
through the www.ftmo.com website (the “Website”). Please read these GTC carefully. You are
under no obligation to use the Services if you do not agree or understand any portion of these Terms,
nor should you use the Services unless you understand and agree to these Terms.
1. INTRODUCTORY PROVISIONS
1.1. These GTC govern your (“you”, “your”, or the “Customer”) rights and obligations in
connection with the use of the Services provided by FTMO Evaluation Global s.r.o., with
its registered office at Purkyňova 2121/3, Nové Město, 110 00 Prague 1, Czech Republic,
identification no.: 092 13 651, registered in the Commercial Register maintained
by the Municipal Court in Prague, file no. C 332660 (“we”, “our”, or the “Provider”).
1.2. By registering on the Website or, where registration is not required, not later than by your
first use of the Services, you are entering into a contract with the Provider, the subject of
which is the provision of the Services of your choice. The GTC form an integral part of
such a contract and, by executing the contract with the Provider, you express your
agreement to these GTC.
1.3. The Services are only intended for persons over the age of 18 residing in the country
for which the Services are available. By registering on the Website, you confirm that you
are over 18 years of age. If you are under 18 years of age, you may not use the Services.
You undertake to access the Services solely from one of the countries for which
the Services are available. You acknowledge that your access to and use of the Services
may be restricted or prohibited by law in some countries, and you undertake to only access
and use the Services in accordance with applicable laws.
1.4. The Provider shall not provide Services to Customer that: (i) is of nationality or is residing
in Restricted Jurisdictions; (ii) is established or incorporated, or has a registered office in
Restricted Jurisdictions; (iii) is subject to the relevant international sanctions; or (iv) has
a criminal record related to financial crime or terrorism. Restricted Jurisdictions means
countries determined as such by the Provider and published here on the Website. The
Provider reserves the right to refuse, restrict or terminate the provision of any Services to
Customer as per this Clause 1.4. and such Customer is prohibited to use the Services,
which also includes the use of the Client Section and/or Trading Platform.
1.5. The Services consist of the provision of tools for simulated foreign exchange trading
on the FOREX market or simulated trading with other instruments on other financial
markets, provision of analytical tools, training and educational materials, the access to
the Client Section, and other ancillary services, in particular through the Client Section or
by the provision of access to applications provided by the Provider or third parties.
Financial market information is used in the simulated trading; however, you acknowledge
that any trading that you perform through the Services is not real. You also acknowledge
that the funds provided to you for demo trading are fictitious and that you have no right
to possess those fictitious funds beyond the scope of their use within the Services, and in
particular that they may not be used for any actual trading and that you are not entitled
to the payment of those funds. Unless expressly agreed otherwise, you will not be paid
any remuneration or profits based on the results of your simulated trading, nor will you
be required to pay any losses.
1.6. NONE OF THE SERVICES PROVIDED TO YOU BY THE PROVIDER CAN BE CONSIDERED
INVESTMENT SERVICES IN ACCORDANCE WITH APPLICABLE LAWS. THE PROVIDER DOES
NOT GIVE OR PROVIDE TO YOU ANY GUIDANCE, INSTRUCTIONS, OR INFORMATION
ABOUT HOW OR IN WHICH MANNER YOU SHOULD PERFORM TRANSACTIONS WHEN
USING THE SERVICES OR OTHERWISE, OR ANY OTHER SIMILAR INFORMATION ABOUT
THE INVESTMENT TOOLS TRADED, NOR DOES THE PROVIDER ACCEPT ANY SUCH
GUIDANCE, INSTRUCTIONS, OR INFORMATION FROM YOU. NONE OF THE SERVICES
CONSTITUTE INVESTMENT ADVICE OR RECOMMENDATIONS. NO EMPLOYEES, STAFF, OR
REPRESENTATIVES OF THE PROVIDER ARE AUTHORIZED TO PROVIDE INVESTMENT
ADVICE OR RECOMMENDATIONS. SHOULD ANY INFORMATION OR STATEMENT OF ANY
EMPLOYEE, STAFF, OR REPRESENTATIVES OF THE PROVIDER BE INTERPRETED AS
2/15
INVESTMENT ADVICE OR RECOMMENDATIONS, THE PROVIDER EXPLICITLY DISCLAIMS
THAT THE SAME IS INVESTMENT ADVICE OR RECOMMENDATIONS AND SHALL NOT BE
RESPONSIBLE FOR THEM.
1.7. Your personal data is processed in accordance with the Privacy Policy.
1.8. The meaning of the definitions, expressions, and abbreviations used in these GTC can be
found in clause 18.
2. SERVICES AND THEIR ORDER
2.1. You can order the Services through the Website by completing the appropriate registration
or order form. After registration, we will e-mail you the login details for the Client Section
and/or Trading Platform and allow you to access them.
2.2. The Services include, among other things, the Free Trial, FTMO Challenge, and Verification
products; these products may differ in the scope of the Services provided
(e.g., by analytical tools available to the Customer). With the Free Trial, you may use
some of the Services within a limited scope and for a limited period free of charge.
Completing the Free Trial does not entitle you to access any other Services.
2.3. All data that you provide to us through the registration or order form, the Client Section,
or otherwise must be complete, true, and up to date. You must immediately notify us
of any change in your data or update the data in your Client Section. The Customer is
responsible for all the provided data being accurate and up to date; the Provider is not
obligated to verify the data.
2.4. You acknowledge that if you provide an identification number, tax registration number
or other similar information in the registration or order form or in the Client Section,
or if you state that you are a legal entity, you will be considered as an entrepreneur
(trader) for the purposes of these GTC and when using the Services, and the provisions
of these GTC or the applicable law that grant rights to consumers will not apply to you.
2.5. The fee for the FTMO Challenge varies according to the option selected and depends on
the amount of the initial capital, the degree of the acceptable risk, the parameters that
must be fulfilled so that the conditions of the FTMO Challenge and the subsequent
Verification are met, and possibly other configurations. More detailed information on
individual options and fees for those options are provided on our Website here. The final
fee will be determined based on the option you select when completing the form for
ordering the FTMO Challenge. The Provider reserves the right to also provide the Services
under individually agreed conditions. All individually agreed conditions shall be determined
by the Provider at its own discretion. Individual discounts and other benefits may not be
combined, unless expressly stipulated otherwise by the Provider.
2.6. The fee is paid for allowing you to access the FTMO Challenge, or the Services provided
under the FTMO Challenge. The Customer is not entitled to a refund of the fee, for
example, if the Customer cancels the Customer’s Client Section or requests the
cancellation by e-mail, if the Customer terminates the use of the Services or the contract
(for example, fails to complete the FTMO Challenge or the Verification), fails to meet the
conditions of the FTMO Challenge or the Verification, or violates these GTC.
2.7. If the Customer lodges an unjustifiable complaint regarding the paid fee or disputes
the paid fee with the Customer’s bank or payment service provider (e.g. through
chargeback services, dispute services, or other similar services), on the basis of which
an annulment, cancellation or refund of the fee or any part thereof is requested,
the Provider is entitled, at its own discretion, to stop providing to the Customer any
services and refuse any future provision of any services.
2.8. Your choice of the option of the FTMO Challenge that you select when making an order
shall also apply to the subsequent Verification. You will start the subsequent Verification
and, possibly, other products related thereto, with the parameters and the same currency
that correspond to the option of the FTMO Challenge selected by you. Once you make a
selection, it is not possible to change it.
If you are ordering a new FTMO Challenge, the restrictions specified in this clause 2.8
shall not apply.
3/15
2.9. The Provider reserves the right to unilaterally change the fees and parameters
of the Services at any time, including the parameters for their successful completion.
The change does not affect the Services purchased before the change is notified.
2.10. Any data entered in the order form can be checked, corrected, and amended until
the binding order of the Services. The order of the Services of your choice is made by
submitting the order form. The Provider will immediately confirm the receipt of your order
to your e-mail address. In the case of the Free Trial, the order is completed upon the
delivery of the confirmation to your e-mail address, whereby the contract is executed.
In the case of the FTMO Challenge, the order is completed upon the payment of the fee
for the selected option (more on this in clause 3.4), whereby the contract between you
and the Provider is executed, the subject of which is the provision of the FTMO Challenge
and, if the conditions of the FTMO Challenge are met, the Verification. The contract is
concluded in English. We archive the contract in electronic form and do not allow access
to it.
2.11. You acknowledge that in order to use our Services, you must obtain the appropriate
technical equipment and software, including third-party software (e.g., software for
the use of the Trading Platform), at your own risk and expense. The Website is accessible
from the most commonly used web browsers. The internet access, purchase of the
equipment, and purchase of the web browser and its updates are at your own risk
and expense. The Provider does not warrant or guarantee that the Services will be
compatible with any specific equipment or software. The Provider does not charge any
additional fees for the internet connection.
2.12. You acknowledge that the operators of trading platforms are persons or entities different
from the Provider and that their own terms and conditions and privacy policies will apply
when you use their services and products. Before sending an order form, you are obligated
to read those terms and conditions and privacy policies.
2.13. If the Customer places an unusually large number of orders for the Services within an
unreasonably short period of time, the Provider may notify the Customer through the
Client Section as a protective precaution to mitigate potentially harmful behaviour of the
Customer. If such unreasonable behaviour continuous after such notice, we reserve the
right to suspend any further orders of the Services by the Customer. If we identify that
the unusual behaviour as per this paragraph relates to the Customer’s involvement in
Forbidden Trading Practices, we may take respective actions as perceived in Section 5 of
this GTC. The Provider reserves the right to determine, at its own discretion, the nature
of the behaviour described above and reasonable boundaries for such determination.
3. PAYMENT TERMS
3.1. The amounts of fees for the FTMO Challenge options are in euros. The fee can also be paid
in other currencies that are listed on the Website. If you select any other currency than
the euro, the amount of the fee for the selected option of the FTMO Challenge shall be
converted by our rates and it will automatically display your payment total in your chosen
currency, so you know how much you are paying before you confirm the order. The
Customer acknowledges that if the payment is made in a currency other than the one the
Customer has chosen on the Website, the amount will be converted according to the
current exchange rates valid at the time of payment.
3.2. Service charges are inclusive of all taxes. If the Customer is an entrepreneur (trader), he
is obliged to fulfil all his tax obligations in connection with the use of our Services in
accordance with applicable law, and in the event of an obligation, he is obliged to pay tax
or other fees properly.
3.3. You can pay the fee for the selected option of the FTMO Challenge by a payment card, via
a bank transfer, or using other means of payment that the Provider currently offers on the
Website.
3.4. In the event of payment by a payment card or via any other express payment method,
the payment shall be made immediately. If you select a bank transfer for payment, we
will subsequently send you a proforma invoice in electronic form with the amount of the
fee for the option of the FTMO Challenge you have chosen on the Website. You undertake
to pay the amount within the period specified in the proforma invoice. The fee is
considered paid when its full amount is credited to the Provider’s account. If you do not
4/15
pay the amount on time, the Provider is entitled to cancel your order. Customer bears all
fees charged to Customer by the selected payment service provider (according to the valid
pricelist of the payment service provider) in connection with the transaction and the
Customer is obliged to ensure that the respective fee for the selected FTMO Challenge is
paid in full.
4. CLIENT SECTION AND TRADING PLATFORM
4.1. Only one Client Section is permitted per Customer and all of the Customer’s Services must
be maintained in the Client Section.
4.2. The total number of FTMO Challenges and Verifications per one Client Section may be
limited depending on the total sum of the initial capital amounts of the products ordered
by the Customer or on the basis of other parameters. Unless the Provider grants an
exception to the Customer, the initial capital amounts may not be transferred between the
individual products or mutually combined. You may also not transfer or combine your
performance, Service parameters, data, or any other information between the products.
4.3. Access to the Client Section and Trading Platform is protected by login data, which
the Customer may not make available or share with any third party. If the Customer has
registered as a legal entity, the Customer may allow the use of the Services through the
Customer’s Client Section to the authorized employees and representatives. The Customer
is responsible for all activities that are performed through the Customer’s Client Section
or Trading Platform. The Provider bears no responsibility, and the Customer is not entitled
to any compensation, for any misuse of the Client Section, Trading Platform, or any part
of the Services, nor is the Provider responsible for any negative consequences thereof for
the Customer, if such misuse occurs for any reasons on the part of the Customer.
4.4. The Customer acknowledges that the Services may not be available around the clock,
particularly with respect to maintenance, upgrades, or any other reasons. In particular,
the Provider bears no responsibility, and the Customer is not entitled to any compensation,
for the unavailability of the Client Section or Trading Platform and for damage or loss
of any data or other content that Customer uploads, transfers or saves through the Client
Section or Trading Platform.
4.5. The Customer may at any time request the cancellation of the Client Section by sending
an e-mail to support@ftmo.com. Sending a request for the cancellation of the Client
Section is considered as a request for termination of the contract by the Customer, with
the Customer being no longer entitled to use the Services, including the Client Section
and Trading Platform. The Provider will immediately confirm the receipt of the request to
the Customer by e-mail, whereby the contractual relationship between the Customer and
the Provider will be terminated. In such a case, the Customer is not entitled to any refund
of the fees already paid or costs otherwise incurred.
5. RULES OF DEMO TRADING
5.1. During the demo trading on the Trading Platform, you may perform any transactions,
unless these constitute forbidden trading strategies or practices within the meaning
of clause 5.4. You also agree to follow good market standard rules and practices for trading
on financial markets (e.g., risk management rules). Restrictions may also be imposed by
the trading conditions of the Trading Platform that you have selected for trading.
5.2. You acknowledge that the Provider has access to information about the demo trades that
you perform on the Trading Platform. You grant the Provider your consent to share this
information with persons/entities who are in a group with the Provider or who are
otherwise affiliated with the Provider, and you grant the Provider and these
persons/entities your consent and authorization to handle this information at their own
will. You agree that these activities may be performed automatically without any further
consent, consultation, or approval on your part being necessary, and that you are not
entitled to any remuneration or revenue associated with the use of the data
by the Provider. The Provider is aware that you do not provide the Provider with any
investment advice or recommendations through your demo trading. You acknowledge that
you may suspend your demo trading on the Trading Platform at any time.
5/15
5.3. The Provider bears no responsibility for the information displayed on the Trading Platform,
nor for any interruption of, or delay or inaccuracy in the market information displayed
through your Client Section.
5.4. FORBIDDEN TRADING PRACTICES.
5.4.1. DURING THE DEMO TRADING, IT IS PROHIBITED TO:
(a) KNOWINGLY OR UNKNOWINGLY USE TRADING STRATEGIES THAT
EXPLOIT ERRORS IN THE SERVICES SUCH AS ERRORS IN DISPLAY
OF PRICES OR DELAY IN THEIR UPDATE;
(b) PERFORM TRADES USING AN EXTERNAL OR SLOW DATA FEED;
(c) PERFORM, ALONE OR IN CONCERT WITH ANY OTHER PERSONS,
INCLUDING BETWEEN CONNECTED ACCOUNTS, OR ACCOUNTS HELD
WITH DIFFERENT FTMO ENTITIES, TRADES OR COMBINATIONS OF
TRADES THE PURPOSE OF WHICH IS TO MANIPULATE TRADING, FOR
EXAMPLE BY SIMULTANEOUSLY ENTERING INTO OPPOSITE POSITIONS;
(d) PERFORM TRADES IN CONTRADICTION WITH THE TERMS AND
CONDITIONS OF THE PROVIDER AND THE TRADING PLATFORM;
(e) USE ANY SOFTWARE, ARTIFICIAL INTELLIGENCE, ULTRA-HIGH SPEED,
OR MASS DATA ENTRY WHICH MIGHT MANIPULATE, ABUSE, OR GIVE
YOU AN UNFAIR ADVANTAGE WHEN USING OUR SYSTEMS OR
SERVICES;
(f) PERFORM GAP TRADING BY OPENING TRADE(S):
(I) WHEN MAJOR GLOBAL NEWS, MACROECONOMIC EVENT OR
CORPORATE REPORTS OR EARNINGS (“EVENTS”), THAT MIGHT
AFFECT THE RELEVANT FINANCIAL MARKET (I.E. MARKET THAT
ALLOWS TRADING OF FINANCIAL INSTRUMENTS THAT MIGHT BE
AFFECTED BY THE EVENTS), ARE SCHEDULED; AND
(II)2 HOURS OR LESS BEFORE A RELEVANT FINANCIAL MARKET IS
CLOSED FOR 2 HOURS OR LONGER.; OR
(g) OTHERWISE PERFORM TRADES IN CONTRADICTION WITH HOW
TRADING IS ACTUALLY PERFORMED IN THE FOREX MARKET OR IN ANY
OTHER FINANCIAL MARKET, OR IN A WAY THAT ESTABLISHES
JUSTIFIED CONCERNS THAT THE PROVIDER MIGHT SUFFER FINANCIAL
OR OTHER HARM AS A RESULT OF THE CUSTOMER’S ACTIVITIES (E.G.
OVERLEVERAGING, OVEREXPOSURE, ONE-SIDED BETS, ACCOUNT
ROLLING).
5.4.2. As our Customer, you should understand and agree that all our Services are
for Customer’s personal use only, meaning that only you personally can access
your FTMO Challenge and Verification accounts and perform trades. For that
reason, you should not, and you agree not to,
(a) allow access to and trading on your FTMO Challenge and Verification
accounts by any third party nor you shall engage or cooperate with any
third party in order to have such third party perform trades for you,
whether such third party is a private person or a professional;
(b) access any third-party FTMO Challenge and Verification accounts, trade
on behalf of any third party or perform any account management or
similar services, where you agree to trade, operate or manage the FTMO
Challenge and Verification accounts on behalf of another user, all whether
performed as a professional or otherwise.
Please note that if you act or behave in contradiction with the aforesaid, we
will consider such action/behaviour as a Forbidden Trading Practice under
Section 5.4. with respective consequences as perceived under this GTC.
5.4.3. Furthermore, Customer shall not exploit the Services by performing trades
without applying market standard risk management rules for trading on
financial markets, this includes, among others, the following practices (i)
opening substantially larger position sizes compared to Customer’s other
6/15
trades, whether on this or any other Customer’s account, or (ii) opening
substantially smaller or larger number of positions compared to Customer’s
other trades, whether on this or any other Customer’s account.
The Provider reserves the right to determine, at its own discretion, whether certain trades,
practices, strategies, or situations are Forbidden Trading Practices.
5.5. If the Customer engages in any of the Forbidden Trading Practices described in clause 5.4,
(i) the Provider may consider it as a failure to meet the conditions of the particular FTMO
Challenge or Verification, (ii) the Provider may remove the transactions that violate
the prohibition from the Customer’s trading history and/or not count their results in the
profits and/or losses achieved by the demo trading, (iii) to immediately cancel all Services
provided to the Customer and subsequently terminate this contract, or (iv) reduce the
offered leverage on products to 1:5 on any or all Customer’s accounts.
5.6. In case when some or all Forbidden Trading Practices are executed on one or more FTMO
Challenge and Verification accounts of one Customer, or accounts of various Customers,
or by combining trading through FTMO Challenge and Verification accounts and FTMO
Trader accounts, then the Provider is entitled to cancel all Services and terminate all
respective contracts related to any and all Customer’s FTMO Challenge and Verification
accounts and/or apply other measures in Clause 5.5. The Provider may exercise any and
all actions in Clauses 5.5 and 5.6 at its own discretion.
5.7. If any FTMO Trader accounts were used for or were involved in the Forbidden Trading
Practices, this may and will constitute a breach of respective terms and conditions for
FTMO Trader account with third-party provider and may result in cancellation of all such
user accounts and termination of respective agreements by the third-party provider.
5.8. If the Customer engages in any of the practices described in clause 5.4 repeatedly,
and the Provider has previously notified the Customer thereof, the Provider may prevent
the Customer from accessing all Services or their parts, including access to the Client
Section and Trading Platform, without any compensation. In such a case, the Customer is
not entitled to a refund of the fees paid.
5.9. The Provider does not bear any responsibility for trading or other investment activities
performed by the Customer outside the relationship with the Provider, for example
by using data or other information from the Client Section, Trading Platform, or otherwise
related to the Services in real trading on financial markets, not even if the Customer uses
for such trading the same Trading Platform that the Customer uses for demo trading.
5.10. DEVELOPMENTS IN FINANCIAL MARKETS ARE SUBJECT TO FREQUENT AND ABRUPT
CHANGES. TRADING ON FINANCIAL MARKETS MAY NOT BE PROFITABLE AND CAN LEAD
TO SIGNIFICANT FINANCIAL LOSSES. ANY PREVIOUS PERFORMANCES AND PROFITS OF
THE CUSTOMER’S DEMO TRADING ARE NOT A GUARANTEE OR INDICATION OF ANY
FURTHER PERFORMANCE.
6. FTMO CHALLENGE AND VERIFICATION
6.1. After paying the fee for the selected option of the FTMO Challenge, the Customer will
receive the relevant login data for the Trading Platform at the e-mail address provided by
the Customer or in the Client Section. The Customer activates the FTMO Challenge by
opening the first demo trade in the Trading Platform. YOU ACKNOWLEDGE THAT,
BY OPENING THE FIRST DEMO TRADE, YOU EXPRESSLY DEMAND THE PROVIDER
TO PROVIDE COMPLETE SERVICES. IF YOU ARE A CONSUMER, IT MEANS THE
COMPLETION OF SERVICES BEFORE THE EXPIRY OF THE PERIOD FOR WITHDRAWAL
FROM THE CONTRACT, WHICH AFFECTS YOUR RIGHT TO WITHDRAW FROM
THE CONTRACT, AS SPECIFIED IN MORE DETAIL IN CLAUSE 12. If you do not activate the
FTMO Challenge within 30 calendar days of the date on which it was made available to
you, your access to it will be suspended. You can request the renewal of access via the
Client Section or by sending an e-mail to support@ftmo.com within 6 months of the initial
suspension, otherwise we will terminate the provision of the Services without any right to
a refund of the fee.
6.2. In order for the Customer to meet the conditions of the FTMO Challenge, the Customer
must fulfil all of the following parameters at the same time:
7/15
6.2.1. the Customer has opened at least one demo trade on at least four different
calendar days;
6.2.2. in the course of none of the calendar days during the FTMO Challenge did
the Customer report a loss on any demo trades opened and closed on that
day, which would exceed the percentage of the initial capital for the
respective option as described below:
FTMO Challenge FTMO Challenge
Aggressive FTMO Challenge Swing
in total 5% of the
initial capital
in total 10% of the
initial capital
in total 5% of the
initial capital
6.2.3. at no time during the FTMO Challenge did the Customer report a loss on
any opened and closed demo transactions, which would exceed in total
the percentage of the initial capital for the respective option as described
below:
FTMO Challenge FTMO Challenge
Aggressive FTMO Challenge Swing
in total 10% of the
initial capital
in total 20% of the
initial capital
in total 10% of the
initial capital
6.2.4. the Customer is in a total profit on all closed demo trades amounting to
at least the percentage of the initial capital for the respective option as
described below:
FTMO Challenge FTMO Challenge
Aggressive FTMO Challenge Swing
in total 10% of the
initial capital
in total 20% of the
initial capital
in total 10% of the
initial capital
The above parameters are explained in more detail here on the Website.
6.3. If the Customer has met the conditions of the FTMO Challenge specified in clause 6.2, and
at the same time has not violated these GTC, in particular the rules of demo trading under
clause 5.4, the Provider will evaluate the FTMO Challenge as successful and will make the
Verification available to the Customer free of charge by sending login details to the
Customer’s e-mail address or Client Section. The Provider does not have to evaluate the
FTMO Challenge if the Customer has not closed all trades.
6.4. The Customer activates the Verification by opening the first demo trade in the Trading
Platform. If the Customer does not activate the Verification within 30 calendar days from
the day on which the Customer received the new login data, the Customer’s access to the
Verification will be suspended. The Customer may request the renewal of access via the
Client Section or by sending an e-mail to support@ftmo.com within 6 months of the
suspension, otherwise we will terminate the provision of the Services without any right to
a refund.
6.5. In order for the Customer to meet the conditions of the Verification, the Customer must
fulfil all of the following parameters at the same time:
6.5.1. during the Verification, the Customer has opened at least one demo trade
on at least four different calendar days;
8/15
6.5.2. in the course of none of the calendar days during the Verification did the
Customer report a loss on any demo trades opened and closed on that
day, which would exceed the percentage of the initial capital for the
respective option as described below:
Verification
Verification
Aggressive Verification Swing
in total 5% of the
initial capital
in total 10% of the
initial capital
in total 5% of the
initial capital
6.5.3. at no time during the Verification did the Customer report a loss on the
sum of the opened and closed demo trades, which would exceed in total
the percentage of the initial capital for the respective option as described
below:
Verification
Verification
Aggressive Verification Swing
in total 10% of the
initial capital
in total 20% of the
initial capital
in total 10% of the
initial capital
6.5.4. Customer is in total profit from all closed demo trades amounting to at
least the percentage of the initial capital for the respective option as
described below:
Verification Verification Aggressive Verification Swing
in total 5% of the
initial capital;
in total 10% of the
initial capital
in total 5% of the
initial capital
The above parameters are explained in more detail here on the Website.
6.6. For the Customer to meet conditions of the Verification, the Customer shall comply with
the following:
6.6.1. Customer has met the conditions of the Verification specified in clause
6.5;
6.6.2. Customer has not violated these GTC, in particular, the rules of demo
trading under clause 5.4; and
6.6.3. Customer has not exceeded the maximum total amount of the capital
allocation of USD 400,000 (USD 200,000 for the Aggressive option),
individually or in combination, per Customer or per each trading strategy,
within the meaning of applicable FTMO Trader Program agreement, if
Customer is already participating in the FTMO Trader Program.
If the above conditions are met, the Provider will evaluate the Verification as successful
and will recommend the Customer as a candidate for FTMO Trader program. The Provider
does not have to evaluate the Verification if the Customer has not closed all transactions.
6.7. If during the FTMO Challenge the Customer does not comply with some of the conditions
specified in clause 6.2.2. or 6.2.3., the FTMO Challenge will be evaluated as unsuccessful,
and the Customer will not be allowed access to the subsequent Verification. If during the
Verification the Customer does not comply with any of the conditions specified in clause
6.5.2. or 6.5.3., the Verification will be evaluated as unsuccessful, and the Customer will
not be recommended as a candidate for the FTMO Trader program. In such cases, the
Customer’s account and Services will be cancelled without refund of fees already paid.
9/15
6.8. Provider recommending Customer as a candidate for the FTMO Trader Program in no way
guarantees Customer’s acceptance into the FTMO Trader Program. The Provider is not
responsible for Customer being rejected by the FTMO Trader Program for any or no reason.
7. FTMO TRADER
If the Customer is successful in both the Challenge and Verification, the Customer may be
offered a contract by a third-party company, in its sole discretion to participate in the
FTMO Trader Program. The terms, conditions, and agreement between the Customer and
a third-party company are strictly between the Customer and the third-party company.
FTMO Evaluation Global s.r.o. is in no way involved with the FTMO Trader Program
agreement—or lack thereof—executed between the third-party company and the
Customer. The Customer acknowledges their personal data may be shared with a thirdparty company for purposes of considering offering such a contract.
8. USE OF THE WEBSITE, SERVICES AND OTHER CONTENT
8.1. The Website and all Services, including the Client Section, their appearance
and all applications, data, information, multimedia elements such as texts, drawings,
graphics, design, icons, images, audio and video samples, and any other content that may
form the Website and the Services (collectively as the “Content”), are subject to legal
protection pursuant to copyright laws and other legal regulations and are the property of
the Provider or the Provider’s licensors. The Provider grants you limited, non-exclusive,
non-transferable, non-assignable, non-passable, and revocable permission to use the
Content for the purpose of using the Services for your personal use and in accordance
with the purpose for which the Services are provided. The Content is not sold or otherwise
transferred to you and remains the property of the Provider or the Provider’s licensors.
8.2. All trademarks, logos, trade names, and other designations are the property of the
Provider or Provider’s licensors, and the Provider does not grant you any authorization to
use them.
8.3. Both the Customer and the Provider undertake to act in accordance with the principles
of fair dealing in the performance of the contract and in mutual negotiations and, in
particular, not to damage the good reputation and legitimate interests of the other party.
The Customer and the Provider will resolve any possible disagreements or disputes
between them in accordance with these GTC and the applicable law.
8.4. Except for the rights expressly set out in these GTC, the Provider does not grant you any
other rights relating to the Services and other Content. You may only use the Services
and other Content as set out in these GTC.
8.5. When accessing the Services and other Content, the following is prohibited:
8.5.1. to use any tools that may adversely affect the operation of the
Website and Services or that would be intended to take advantage of
errors, bugs or other deficiencies of the Website and Services;
8.5.2. to circumvent geographical restrictions of availability or any other
technical restrictions;
8.5.3. to make copies or back-ups of the Website and other Content;
8.5.4. to reverse-engineer, decompile, disassemble or otherwise modify
the Website and other Content;
8.5.5. to sell, rent, lend, license, distribute, reproduce, spread, stream,
broadcast or use the Services or other Content otherwise than
as permitted;
8.5.6. to use automated means to view, display or collect information
available through the Website or Services; and
8.5.7. to use any other tools or means the use of which could cause
any damage to the Provider.
8.6. The provisions of clause 8 are not intended to deprive the Customer of the Customer’s
consumer rights which cannot be excluded by law.
10/15
9. DISCLAIMER
9.1. YOU ACKNOWLEDGE THAT THE SERVICES AND OTHER CONTENT ARE PROVIDED “AS IS”
WITH ALL THEIR ERRORS, DEFECTS AND SHORTCOMINGS, AND THAT THEIR USE IS AT
YOUR SOLE RESPONSIBILITY AND RISK. TO THE MAXIMUM EXTENT PERMITTED BY THE
MANDATORY LAWS, THE PROVIDER DISCLAIMS ANY STATUTORY, CONTRACTUAL,
EXPRESS, AND IMPLIED WARRANTIES OF ANY KIND, INCLUDING ANY WARRANTY OF
QUALITY, MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, OR NONINFRINGEMENT OF ANY RIGHTS.
9.2. TO THE EXTENT PERMITTED BY THE MANDATORY PROVISIONS OF THE APPLICABLE
LAWS, THE PROVIDER IS NOT RESPONSIBLE FOR ANY HARM, INCLUDING ANY INDIRECT,
INCIDENTAL, SPECIAL, PUNITIVE OR CONSEQUENTIAL DAMAGES, INCLUDING LOST
PROFIT, LOSS OF DATA, PERSONAL OR OTHER NON-MONETARY HARM OR PROPERTY
DAMAGE CAUSED AS A RESULT OF USE OF THE SERVICES OR RELIANCE ON ANY TOOL,
FUNCTIONALITY, INFORMATION OR ANY OTHER CONTENT AVAILABLE IN CONNECTION
WITH THE USE OF THE SERVICES OR ELSEWHERE ON THE WEBSITE. THE PROVIDER IS
NOT RESPONSIBLE FOR ANY PRODUCTS, SERVICES, APPLICATIONS OR OTHER THIRDPARTY CONTENT THAT THE CUSTOMER USES IN CONNECTION WITH THE SERVICES. IN
CASE THE PROVIDER’S LIABILITY IS INFERRED IN CONNECTION WITH THE OPERATION
OF THE WEBSITE OR PROVISION OF THE SERVICES BY A COURT OF JUSTICE OR ANY
OTHER COMPETENT AUTHORITY, THIS LIABILITY SHALL BE LIMITED TO THE AMOUNT
CORRESPONDING TO THE FEE PAID BY THE CUSTOMER FOR THE SERVICES IN
CONNECTION WITH WHICH THE CUSTOMER HAS INCURRED THE LOSS.
9.3. The Provider reserves the right to modify, change, replace, add, or remove any elements
and functions of the Services at any time without any compensation.
9.4. The Provider is not responsible for its failure to provide the purchased Services if that
failure occurs due to serious technical or operational reasons beyond the Provider’s
control, in the case of any crisis or imminent crisis, natural disaster, war, insurrection,
pandemic, a threat to a large number of people or other force majeure events, and/or
if the Provider is prevented from providing the Services as a result of any obligations
imposed by law or a decision of a public authority.
9.5. The provisions of Clause 9 are not intended to deprive the Customer of the Customer’s
consumer or other rights that cannot be excluded by law.
10. VIOLATION OF THE GTC
10.1. IF THE CUSTOMER VIOLATES ANY PROVISION OF THESE GTC IN A MANNER THAT MAY
CAUSE ANY HARM TO THE PROVIDER, IN PARTICULAR, IF THE CUSTOMER ACCESSES THE
SERVICES IN CONFLICT WITH CLAUSE 1.3 OR 1.4, IF THE CUSTOMER PROVIDES
INCOMPLETE, UNTRUE OR NON-UPDATED INFORMATION IN CONFLICT WITH CLAUSE 2.3,
IF THE CUSTOMER ACTS IN A MANNER THAT MAY DAMAGE THE PROVIDER’S GOOD
REPUTATION, IF THE CUSTOMER VIOLATES THE DEMO TRADING RULES PURSUANT TO
CLAUSE 5.4, IF THE CUSTOMER ACTS IN CONFLICT WITH CLAUSE 8.3, AND/OR
IF THE CUSTOMER PERFORMS ANY OF THE ACTIVITIES REFERRED TO IN CLAUSE 8.5,
THE PROVIDER MAY PREVENT THE CUSTOMER FROM ORDERING ANY OTHER SERVICES
AND COMPLETELY OR PARTIALLY RESTRICT THE CUSTOMER’S ACCESS TO ALL OR ONLY
SOME SERVICES, INCLUDING ACCESS TO THE CLIENT SECTION AND TRADING
PLATFORM, WITHOUT ANY PRIOR NOTICE AND WITHOUT ANY COMPENSATION.
11. COMMUNICATION
11.1. You acknowledge that all communication from the Provider or its partners in connection
with the provision of Services will take place through the Client Section or your e-mail
address, which you register with us. Written electronic communication by e-mail
or through the Client Section is also considered to be written communication.
11.2. Our contact e-mail address is support@ftmo.com and our contact address is Purkynova
2121/3, Prague 1, 11000, Czech Republic.
11/15
12. RIGHT TO WITHDRAW FROM A CONTRACT
12.1. If you are a consumer, you have the right to withdraw from a contract without giving a
reason within 14 days of its execution (see clause 2.10 for details on the time of execution
of the agreement). PLEASE NOTE THAT IF YOU START PERFORMING DEMO TRADES
BEFORE THE EXPIRY OF THE SPECIFIED TIME LIMIT, YOU LOSE YOUR RIGHT TO
WITHDRAW FROM THE CONTRACT.
12.2. Your withdrawal from the contract must be sent to our e-mail address support@ftmo.com
within the specified time limit. You can use the template form available here to withdraw.
We will confirm the receipt of the form to you in text form without undue delay. If you
withdraw from the contract, we will refund you without undue delay (no later than 14 days
after your withdrawal from the contract) all fees we have received from you, in the same
way in which you paid them.
12.3. The Provider is entitled to withdraw from the contract in the case of any breach by the
Customer specified in Clause 10. The withdrawal has effect from the day of its delivery to
the e-mail address of the Customer or through the Client Section.
13. DEFECTIVE PERFORMANCES
13.1. If the Services do not correspond to what was agreed or have not been provided to you,
you can exercise your rights from defective performance. The Provider does not provide
any guarantee for the quality of the services. You must notify us of the defect without
undue delay at our e-mail address or at our address listed in clause 11.2. When exercising
the rights from defective performance, you may request that we remedy the defect
or provide you with a reasonable discount. If the defect cannot be remedied, you can
withdraw from the contract or claim a reasonable discount.
13.2. We will try to resolve any complaint you may lodge as soon as possible (no later than
within 30 calendar days), and we will confirm its receipt and settlement to you in writing.
If we do not settle the complaint in time, you have the right to withdraw from the contract.
You can file a complaint by sending an e-mail to our e-mail address support@ftmo.com.
14. CHANGES TO THE GTC
14.1. The Provider reserves the right to change these GTC from time to time with effect for the
contract previously entered into by the Customer. The Provider will notify the Customer
of the change in the GTC at least 7 days before the change in the GTC is effective, via the
Client Section or by e-mail. If the Customer does not agree with the change, the Customer
is entitled to reject it. The Customer must do so no later than on the last business day
before these changes take effect by sending the rejection to our e-mail address
support@ftmo.com. Upon receiving such rejection, the contract will be terminated. If the
Customer does not reject the change, it is considered that the Customer agrees to the
new version of GTC.
14.2. If the change offers the Customer a new service or other additional functionalities or this
change is solely to their advantage, the Provider can inform the Customer about this
change less than 7 days before the effective date of such change, but no later than the
day before its effectiveness.
14.3. The Provider will mainly change these GTC for the following reasons:
14.3.1. to introduce new services or products or amend existing services or
products;
14.3.2. to reflect legal or regulatory requirements that apply to the Provider;
14.3.3. when the Provider will try to make these GTC easier to understand
or more helpful to the Customer;
14.3.4. to adjust the way our Services are provided, particularly if the change
is needed because of a change in the way the technology is provided
or background processes;
14.3.5. to reflect changes in the cost of running our business.
12/15
15. OUT-OF-COURT CONSUMER DISPUTE SETTLEMENT
15.1. It is our objective that our customers are satisfied with the FTMO services; therefore, if
you have any complaints or suggestions, we will be happy to resolve them directly with
you and you can contact us at our e-mail address or at our address listed in clause 11.2.
15.2. This section 15.2 applies only to a consumer who is at the same time an EU resident. The
Czech Trade Inspection Authority (Česká obchodní inspekce), with its registered office at
Štěpánská 567/15, 120 00 Prague 2, identification no.: 000 20 869, website:
https://www.coi.cz/en/information-about-adr/, is responsible for the out-of-court
settlement of consumer disputes. You can also use the platform at the following website
to resolve disputes online: https://www.ec.europa.eu/consumers/odr.
16. CHOICE OF LAW AND JURISDICTION
16.1. Any legal relations established by these GTC or related to them, as well as any related
non-contractual legal relations, shall be governed by the laws of the Czech Republic.
Any dispute that may arise in connection with these GTC and/or related agreements
will fall within the jurisdiction of the Czech court having local jurisdiction according to
the registered office of the Provider.
16.2. The provisions of clause 16.1 do not deprive the consumers of the protection afforded
to them by the mandatory laws of the relevant Member State of the European Union or any
other jurisdiction.
17. DURATION AND TERMINATION OF THE CONTRACT
17.1. The contract is concluded for a definite period until the FTMO Challenge or Verification is
passed or failed in accordance with the clause 6.2. or 6.5 respectively.
17.2. The contract may be terminated by either party earlier in accordance with these GTC. The
contract terminates automatically and with immediate effect in case the Customer during
FTMO Challenge or Verification does not open at least one demo trade during a period of
30 consecutive days.
17.3. Notwithstanding clause 17.2 the Provider may terminate this contract with cause and
immediate effect when the provision of Services under contract would affect the ability of
the Provider to adhere to its legal obligations or orders or decisions of a governmental
bodies or other regulators
17.4. Either Party may terminate this contract without cause by serving a written notice at least
7 days in advance in accordance with Clause 11 on the other Party.
18. FINAL PROVISIONS
18.1. The Provider has not adopted any consumers codes of conduct.
18.2. These GTC constitute the complete terms and conditions agreed between you and the
Provider and supersede all prior agreements relating to the subject matter of the GTC,
whether verbal or written.
18.3. Nothing in these GTC is intended to limit any legal claims set out elsewhere in these GTC
or arising from the applicable law. If the Provider or any third party authorized thereto
does not enforce the compliance with these GTC, this can in no way be construed
as a waiver of any right or claim.
18.4. The Provider may assign any claim arising to the Provider from these GTC
or any agreement to a third party without your consent. You agree that the Provider may,
as the assignor, transfer its rights and obligations under these GTC or any agreement
or parts thereof to a third party. The Customer is not authorized to transfer or assign
the Customer’s rights and obligations under these GTC or any agreements or parts
thereof, or any receivables arising from them, in whole or in part, to any third party.
18.5. If any provision of the GTC is found to be invalid or ineffective, it shall be replaced
by a provision whose meaning is as close as possible to the invalid provision. The invalidity
13/15
or ineffectiveness of one provision shall not affect the validity of the other provisions.
No past or future practice established between the parties and no custom maintained
in general or in the industry relating to the subject-matter of the performance, which is
not expressly referred to in the GTC, shall be applied and no rights and obligations shall
be derived from them for the parties; in addition, they shall not be taken into account
in the interpretation of manifestations of the will of the parties.
18.6. The schedules to the GTC form integral parts of the GTC. In the event of a conflict between
the wording of the main text of the GTC and any schedule thereof, the main text of the GTC
shall prevail.
18.7. Prior to the mutual acceptance of these GTC, the parties have carefully assessed
the possible risks arising from them and accept those risks.
19. DEFINITIONS, EXPRESSIONS AND ABBREVIATIONS USED
19.1. For the purposes of the GTC, the following definitions shall have the following meanings:
19.1.1. “Client Section” means the user interface located on the Website;
19.1.2. “Content” means the Website and all Services, including the Client
Section, their appearance and all applications, data, information,
multimedia elements such as texts, drawings, graphics, design,
icons, images, audio and video samples and other content that may
form the Website and the Services (as set out in clause 8.1);
19.1.3. “Customer” means the user of the Services (as set out in clause
1.1);
19.1.4. “Events” means events as set out in clause 5.4.1(f)(I);
19.1.5. “FTMO Challenge and Verification account” means trading
accounts related to trading education courses provided as part of the
Services by the Provider;
19.1.6. “FTMO Trader account” means a trading account, which relates to
the FTMO Trader program provided by a third-party provider;
19.1.7. “Forbidden Trading Practices” means trading practices strictly
forbidden while using our Services and are more detailed in Section
5.4 of these GTC;
19.1.8. “GTC” means these General Terms and Conditions of FTMO;
19.1.9. “Provider” means the provider of certain Services (as set out
in clause 1.1);
19.1.10. “Schedules” means Schedule 1 and any other Schedules as
applicable, which are part of these GTC;
19.1.11. “Services” means the Provider’s services as set out in clauses 1.1
and 1.5;
19.1.12. “Trading Platform” means an electronic interface provided
by a third party in which the Customer performs the demo trading;
and
19.1.13. “Website” means the website www.ftmo.com.
19.2. For the purposes of the GTC and their schedules, the following expressions
and abbreviations shall have the following meanings:
19.2.1. “calendar day” means the period from midnight to midnight
of the time currently valid in the Czech Republic (Central European
(Summer) Time, CE(S)T);
19.2.2. “initial capital” means a fictitious amount that the Customer has
chosen when selecting the option of the FTMO Challenge and which
the Customer will use to perform demo trading;
19.2.3. “CZK” means the Czech crown;
14/15
19.2.4. “EUR” means the euro;
19.2.5. “USD” means the United States dollar;
19.2.6. “GBP” means the British pound;
19.2.7. “CAD” means the Canadian dollar;
19.2.8. “AUD” means the Australian dollar;
19.2.9. “NZD” means the New Zealand dollar; and
19.2.10. “CHF” means the Swiss franc.
These GTC shall enter into force and effect on 13 July 2023.
15/15
SCHEDULE 1
OPTIONS OF FTMO CHALLENGES AND VERIFICATIONS
- FTMO Challenge or Verification with an initial capital of EUR 10,000 (or the corresponding
equivalent: USD 10,000, GBP 10,000, CZK 250,000, CHF 10,000, CAD 15,000 or AUD 15,000)
- FTMO Challenge or Verification Aggressive with an initial capital of EUR 10,000 (or the
corresponding equivalent: USD 10,000, GBP 10,000, CZK 250,000, CHF 10,000, CAD 15,000 or AUD
15,000)
- FTMO Challenge or Verification Swing with an initial capital of EUR 10,000 (or the corresponding
equivalent: USD 10,000, GBP 10,000, CZK 250,000, CHF 10,000, CAD 15,000 or AUD 15,000)
- FTMO Challenge or Verification with an initial capital of EUR 20,000 (or the corresponding
equivalent: USD 25,000, GBP 20,000, CZK 500,000, CHF 20,000, CAD 30,000 or AUD 30,000)
- FTMO Challenge or Verification Aggressive with an initial capital of EUR 20,000 (or the
corresponding equivalent: USD 25,000, GBP 20,000, CZK 500,000, CHF 20,000, CAD 30,000 or AUD
30,000)
- FTMO Challenge or Verification Swing with an initial capital of EUR 20,000 (or the corresponding
equivalent: USD 25,000, GBP 20,000, CZK 500,000, CHF 20,000, CAD 30,000 or AUD 30,000)
- FTMO Challenge or Verification with an initial capital of EUR 40,000 (or the corresponding
equivalent: USD 50,000, GBP 35,000, CZK 1,000,000, CHF 40,000, CAD 60,000 or AUD 65,000)
- FTMO Challenge or Verification Aggressive with an initial capital of EUR 40,000 (or the
corresponding equivalent: USD 50,000, GBP 35,000, CZK 1,000,000, CHF 40,000, CAD 60,000 or
AUD 65,000)
FTMO Challenge or Verification Swing with an initial capital of EUR 40,000 (or the corresponding
equivalent: USD 50,000, GBP 35,000, CZK 1,000,000, CHF 40,000, CAD 60,000 or AUD 65,000)
- FTMO Challenge or Verification with an initial capital of EUR 80,000 (or the corresponding
equivalent: USD 100,000, GBP 70,000, CZK 2,000,000, CHF 80,000, CAD 120,000 or AUD 130,000)
- FTMO Challenge or Verification Aggressive with an initial capital of EUR 80,000 (or the
corresponding equivalent: USD 100,000, GBP 70,000, CZK 2,000,000, CHF 80,000, CAD 120,000 or
AUD 130,000)
- FTMO Challenge or Verification Swing with an initial capital of EUR 80,000 (or the corresponding
equivalent: USD 100,000, GBP 70,000, CZK 2,000,000, CHF 80,000, CAD 120,000 or AUD 130,000)
- FTMO Challenge or Verification with an initial capital of EUR 160,000 (or the corresponding
equivalent: USD 200,000, GBP 140,000, CZK 4,000,000, CHF 160,000, CAD 240,000 or AUD
260,000)
- FTMO Challenge or Verification Swing with an initial capital of EUR 160,000 (or the corresponding
equivalent: USD 200,000, GBP 140,000, CZK 4,000,000, CHF 160,000, CAD 240,000 or AUD
260,000)```

-----------

Path: docs/README.md

```
# Sophy Trading System

Een professioneel algoritmisch trading systeem gebouwd in Python dat de Turtle Trading strategie implementeert via
MetaTrader 5, speciaal geoptimaliseerd voor FTMO-accounts.

## Kenmerken

- **Modulaire architectuur** - Duidelijke scheiding van verantwoordelijkheden
- **Meerdere strategieën** - Ondersteunt verschillende trading strategieën met een factory patroon
- **FTMO Compliance** - Ingebouwde controles voor naleving van FTMO-regels
- **Risicomanagement** - Geavanceerd positie-sizing en risicobeheer
- **Backtesting** - Uitgebreide backtesting mogelijkheden
- **Performance analyse** - Gedetailleerde rapportage en visualisatie

## Installatie

```bash
# Kloon de repository
git clone https://github.com/yourusername/sophy.git
cd sophy

# Installeer dependencies
pip install -r requirements.txt

# Optioneel: Installeer in development mode
pip install -e .```

-----------

Path: requirements.txt

```plaintext
��a n y i o = = 4 . 8 . 0  
 a r g o n 2 - c f f i = = 2 3 . 1 . 0  
 a r g o n 2 - c f f i - b i n d i n g s = = 2 1 . 2 . 0  
 a r r o w = = 1 . 3 . 0  
 a s t r o i d = = 3 . 3 . 8  
 a s t t o k e n s = = 3 . 0 . 0  
 a s y n c - l r u = = 2 . 0 . 4  
 a t t r s = = 2 4 . 3 . 0  
 b a b e l = = 2 . 1 6 . 0  
 b a c k t r a d e r = = 1 . 9 . 7 8 . 1 2 3  
 b e a u t i f u l s o u p 4 = = 4 . 1 2 . 3  
 b l a c k = = 2 5 . 1 . 0  
 b l e a c h = = 6 . 2 . 0  
 c e r t i f i = = 2 0 2 4 . 1 2 . 1 4  
 c f f i = = 1 . 1 7 . 1  
 c h a r s e t - n o r m a l i z e r = = 3 . 4 . 1  
 c l i c k = = 8 . 1 . 8  
 c o l o r a m a = = 0 . 4 . 6  
 c o m m = = 0 . 2 . 2  
 c o n t o u r p y = = 1 . 3 . 1  
 c y c l e r = = 0 . 1 2 . 1  
 d e b u g p y = = 1 . 8 . 1 1  
 d e c o r a t o r = = 5 . 1 . 1  
 d e f u s e d x m l = = 0 . 7 . 1  
 d i l l = = 0 . 3 . 9  
 e t _ x m l f i l e = = 2 . 0 . 0  
 e x e c u t i n g = = 2 . 1 . 0  
 f a s t j s o n s c h e m a = = 2 . 2 1 . 1  
 f o n t t o o l s = = 4 . 5 5 . 3  
 f q d n = = 1 . 5 . 1  
 h 1 1 = = 0 . 1 4 . 0  
 h t t p c o r e = = 1 . 0 . 7  
 h t t p x = = 0 . 2 8 . 1  
 i d n a = = 3 . 1 0  
 i p y k e r n e l = = 6 . 2 9 . 5  
 i p y t h o n = = 8 . 3 1 . 0  
 i p y w i d g e t s = = 8 . 1 . 5  
 i s o d u r a t i o n = = 2 0 . 1 1 . 0  
 i s o r t = = 6 . 0 . 1  
 j e d i = = 0 . 1 9 . 2  
 J i n j a 2 = = 3 . 1 . 5  
 j s o n 5 = = 0 . 1 0 . 0  
 j s o n p o i n t e r = = 3 . 0 . 0  
 j s o n s c h e m a = = 4 . 2 3 . 0  
 j s o n s c h e m a - s p e c i f i c a t i o n s = = 2 0 2 4 . 1 0 . 1  
 j u p y t e r = = 1 . 1 . 1  
 j u p y t e r - c o n s o l e = = 6 . 6 . 3  
 j u p y t e r - e v e n t s = = 0 . 1 1 . 0  
 j u p y t e r - l s p = = 2 . 2 . 5  
 j u p y t e r _ c l i e n t = = 8 . 6 . 3  
 j u p y t e r _ c o r e = = 5 . 7 . 2  
 j u p y t e r _ s e r v e r = = 2 . 1 5 . 0  
 j u p y t e r _ s e r v e r _ t e r m i n a l s = = 0 . 5 . 3  
 j u p y t e r l a b = = 4 . 3 . 4  
 j u p y t e r l a b _ p y g m e n t s = = 0 . 3 . 0  
 j u p y t e r l a b _ s e r v e r = = 2 . 2 7 . 3  
 j u p y t e r l a b _ w i d g e t s = = 3 . 0 . 1 3  
 k i w i s o l v e r = = 1 . 4 . 8  
 M a r k u p S a f e = = 3 . 0 . 2  
 m a t p l o t l i b = = 3 . 1 0 . 0  
 m a t p l o t l i b - i n l i n e = = 0 . 1 . 7  
 m c c a b e = = 0 . 7 . 0  
 M e t a T r a d e r 5 = = 5 . 0 . 4 7 3 8  
 m i s t u n e = = 3 . 1 . 0  
 m y p y = = 1 . 1 5 . 0  
 m y p y - e x t e n s i o n s = = 1 . 0 . 0  
 n b c l i e n t = = 0 . 1 0 . 2  
 n b c o n v e r t = = 7 . 1 6 . 5  
 n b f o r m a t = = 5 . 1 0 . 4  
 n e s t - a s y n c i o = = 1 . 6 . 0  
 n o t e b o o k = = 7 . 3 . 2  
 n o t e b o o k _ s h i m = = 0 . 2 . 4  
 n u m p y = = 2 . 2 . 1  
 o p e n p y x l = = 3 . 1 . 5  
 o v e r r i d e s = = 7 . 7 . 0  
 p a c k a g i n g = = 2 4 . 2  
 p a n d a s = = 2 . 2 . 3  
 p a n d o c f i l t e r s = = 1 . 5 . 1  
 p a r s o = = 0 . 8 . 4  
 p a t h s p e c = = 0 . 1 2 . 1  
 p i l l o w = = 1 1 . 1 . 0  
 p l a t f o r m d i r s = = 4 . 3 . 6  
 p r o m e t h e u s _ c l i e n t = = 0 . 2 1 . 1  
 p r o m p t _ t o o l k i t = = 3 . 0 . 4 8  
 p s u t i l = = 6 . 1 . 1  
 p u r e _ e v a l = = 0 . 2 . 3  
 p y c p a r s e r = = 2 . 2 2  
 P y g m e n t s = = 2 . 1 9 . 1  
 p y l i n t = = 3 . 3 . 4  
 p y p a r s i n g = = 3 . 2 . 1  
 p y t h o n - d a t e u t i l = = 2 . 9 . 0 . p o s t 0  
 p y t h o n - j s o n - l o g g e r = = 3 . 2 . 1  
 p y t z = = 2 0 2 4 . 2  
 p y w i n 3 2 = = 3 0 8  
 p y w i n p t y = = 2 . 0 . 1 4  
 P y Y A M L = = 6 . 0 . 2  
 p y z m q = = 2 6 . 2 . 0  
 r e f e r e n c i n g = = 0 . 3 5 . 1  
 r e q u e s t s = = 2 . 3 2 . 3  
 r f c 3 3 3 9 - v a l i d a t o r = = 0 . 1 . 4  
 r f c 3 9 8 6 - v a l i d a t o r = = 0 . 1 . 1  
 r p d s - p y = = 0 . 2 2 . 3  
 S e n d 2 T r a s h = = 1 . 8 . 3  
 s e t u p t o o l s = = 7 5 . 8 . 0  
 s i x = = 1 . 1 7 . 0  
 s n i f f i o = = 1 . 3 . 1  
 s o u p s i e v e = = 2 . 6  
 s t a c k - d a t a = = 0 . 6 . 3  
 t e r m i n a d o = = 0 . 1 8 . 1  
 t i n y c s s 2 = = 1 . 4 . 0  
 t o m l k i t = = 0 . 1 3 . 2  
 t o r n a d o = = 6 . 4 . 2  
 t q d m = = 4 . 6 7 . 1  
 t r a i t l e t s = = 5 . 1 4 . 3  
 t y p e s - p y t h o n - d a t e u t i l = = 2 . 9 . 0 . 2 0 2 4 1 2 0 6  
 t y p i n g _ e x t e n s i o n s = = 4 . 1 2 . 2  
 t z d a t a = = 2 0 2 4 . 2  
 u r i - t e m p l a t e = = 1 . 3 . 0  
 u r l l i b 3 = = 2 . 3 . 0  
 w c w i d t h = = 0 . 2 . 1 3  
 w e b c o l o r s = = 2 4 . 1 1 . 1  
 w e b e n c o d i n g s = = 0 . 5 . 1  
 w e b s o c k e t - c l i e n t = = 1 . 8 . 0  
 w i d g e t s n b e x t e n s i o n = = 4 . 0 . 1 3  
 X l s x W r i t e r = = 3 . 2 . 2  
 ```

-----------

Path: run.py

```python
#!/usr/bin/env python3
"""
Sophy Trading System - Hoofdscript

Dit script start het Sophy trading systeem in live of backtest modus
en zorgt voor de integratie van alle componenten.
"""
import argparse
import os
import sys
import time
from datetime import datetime


def setup_environment():
    """Zet de omgeving op voor het uitvoeren van de applicatie"""
    # Voeg de huidige directory toe aan het pythonpath
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)

    # Maak log directory aan indien nodig
    log_dir = os.path.join(script_dir, 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Maak data directory aan indien nodig
    data_dir = os.path.join(script_dir, 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)


def parse_arguments():
    """Parse command line arguments met uitgebreide opties"""
    parser = argparse.ArgumentParser(description='Sophy Trading System')
    parser.add_argument('--config', type=str, help='Pad naar configuratiebestand')
    parser.add_argument('--mode', type=str, choices=['live', 'backtest', 'paper'],
                        default='backtest', help='Trading modus (default: backtest)')
    parser.add_argument('--strategy', type=str, help='Te gebruiken strategie')
    parser.add_argument('--symbols', type=str, help='Komma-gescheiden lijst van symbolen')
    parser.add_argument('--interval', type=int, help='Update interval in seconden')
    parser.add_argument('--initial_balance', type=float, help='Initiële account balans voor backtest')
    parser.add_argument('--swing', action='store_true', help='Gebruik swing modus voor Turtle strategie')
    parser.add_argument('--start_date', type=str, help='Startdatum voor backtest (YYYY-MM-DD)')
    parser.add_argument('--end_date', type=str, help='Einddatum voor backtest (YYYY-MM-DD)')
    parser.add_argument('--optimize', action='store_true', help='Voer parameteroptimalisatie uit')
    parser.add_argument('--validate', action='store_true', help='Valideer FTMO compliance')
    parser.add_argument('--visualize', action='store_true', help='Genereer visualisaties na afloop')
    parser.add_argument('--verbose', action='store_true', help='Toon gedetailleerde log output')

    return parser.parse_args()


def load_config(config_path=None):
    """Laad configuratie met mogelijkheid tot pad-override"""
    from src.utils.config import load_config as load_config_util

    try:
        return load_config_util(config_path)
    except Exception as e:
        print(f"Fout bij laden configuratie: {e}")
        sys.exit(1)


def create_logger(config):
    """Maak logger instance gebaseerd op configuratie"""
    from src.utils.logger import Logger

    log_file = config['logging'].get('log_file', 'logs/trading_log.csv')
    return Logger(log_file)


def run_backtest(config, args, logger):
    """Voer backtesting uit met opgegeven configuratie"""
    print(f"Starten in backtest modus - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        from src.analysis.backtester import run_backtest

        # Override config met command line argumenten
        if args.symbols:
            config['mt5']['symbols'] = args.symbols.split(',')
        if args.initial_balance:
            config['mt5']['account_balance'] = args.initial_balance
        if args.strategy:
            config['strategy']['name'] = args.strategy
        if args.swing:
            config['strategy']['swing_mode'] = True
        if args.start_date or args.end_date:
            if 'backtest' not in config:
                config['backtest'] = {}
            if args.start_date:
                config['backtest']['start_date'] = args.start_date
            if args.end_date:
                config['backtest']['end_date'] = args.end_date

        # Log configuratie
        logger.log_info(f"Backtest configuratie: strategie={config['strategy']['name']}, "
                        f"symbolen={config['mt5']['symbols']}")

        # Voer backtest uit
        run_backtest()

        # Voer FTMO validatie uit indien gewenst
        if args.validate:
            from src.ftmo.ftmo_validator import FTMOValidator
            validator = FTMOValidator(config, logger.log_file, logger=logger)
            validator.generate_trading_report()
            logger.log_info("FTMO validatie rapport gegenereerd")

        # Genereer visualisaties indien gewenst
        if args.visualize:
            from src.utils.visualizer import Visualizer
            visualizer = Visualizer(logger.log_file)
            visualizer.plot_equity_curve()
            visualizer.plot_trade_results()
            visualizer.plot_performance_summary()
            logger.log_info("Visualisaties gegenereerd")

        print("Backtest voltooid")

    except Exception as e:
        logger.log_info(f"Fout tijdens backtest: {str(e)}", level="ERROR")
        print(f"Fout tijdens backtest: {str(e)}")
        return False

    return True


def run_live_trading(config, args, logger):
    """Start live trading met opgegeven configuratie"""
    print(f"Starten in live trading modus - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        from src.connector.mt5_connector import MT5Connector
        from src.risk.risk_manager import RiskManager
        from src.strategy.strategy_factory import StrategyFactory

        # Override config met command line argumenten
        if args.symbols:
            config['mt5']['symbols'] = args.symbols.split(',')
        if args.strategy:
            config['strategy']['name'] = args.strategy
        if args.swing:
            config['strategy']['swing_mode'] = True
        if args.interval:
            config['interval'] = args.interval

        # Log configuratie
        logger.log_info(f"Live trading configuratie: strategie={config['strategy']['name']}, "
                        f"symbolen={config['mt5']['symbols']}")

        # Maak componenten aan
        connector = MT5Connector(config['mt5'], logger)
        risk_manager = RiskManager(config['risk'], logger)

        # Maak verbinding met MT5
        if not connector.connect():
            logger.log_info("Kan geen verbinding maken met MT5", level="ERROR")
            return False

        # Creëer strategie
        strategy_name = config['strategy']['name']
        try:
            strategy = StrategyFactory.create_strategy(
                strategy_name, connector, risk_manager, logger, config
            )
        except ValueError as e:
            logger.log_info(f"Kan strategie '{strategy_name}' niet maken: {e}", level="ERROR")
            connector.disconnect()
            return False

        # Start trading loop
        logger.log_info("Trading loop gestart")

        stop_trading = False
        while not stop_trading:
            try:
                # Verwerk alle symbolen
                for symbol in config['mt5']['symbols']:
                    # Pas symbol mapping toe indien nodig
                    symbol_map = config['mt5'].get('symbol_mapping', {})
                    mapped_symbol = symbol_map.get(symbol, symbol)

                    # Verwerk symbool volgens strategie
                    result = strategy.process_symbol(mapped_symbol)

                    if result.get('signal'):
                        logger.log_info(
                            f"Signaal voor {mapped_symbol}: {result['signal']} {result.get('action', '')}"
                        )

                # Controleer account status en FTMO limieten
                account_info = connector.get_account_info()
                positions = strategy.get_open_positions()
                logger.log_status(account_info, positions)

                should_stop, reason = risk_manager.check_ftmo_limits(account_info)
                if should_stop:
                    logger.log_info(f"Trading gestopt: {reason}")
                    break

                # Wacht tot volgende cyclus
                interval = config.get('interval', 300)  # Default 5 minuten
                logger.log_info(f"Wacht {interval} seconden tot volgende cyclus")
                time.sleep(interval)

            except KeyboardInterrupt:
                logger.log_info("Trading gestopt door gebruiker")
                stop_trading = True
            except Exception as e:
                logger.log_info(f"Fout in trading loop: {str(e)}", level="ERROR")
                # Bij ernstige fouten, stop trading
                if "MT5 connection" in str(e):
                    stop_trading = True

        # Cleanup
        connector.disconnect()
        logger.log_info("Trading sessie afgesloten")

    except Exception as e:
        logger.log_info(f"Fout tijdens live trading: {str(e)}", level="ERROR")
        print(f"Fout tijdens live trading: {str(e)}")
        return False

    return True


def main():
    """Hoofdfunctie voor de Sophy trading applicatie"""
    # Setup
    setup_environment()

    # Parse arguments
    args = parse_arguments()

    # Stel config pad in indien opgegeven
    config_path = args.config
    if config_path and not os.path.exists(config_path):
        print(f"Waarschuwing: Opgegeven configuratiebestand {config_path} bestaat niet")
        config_path = None

    # Laad configuratie
    config = load_config(config_path)

    # Maak logger
    logger = create_logger(config)
    logger.log_info("====== Sophy Trading System ======")
    logger.log_info(f"Opgestart op {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Bepaal modus en start juiste functie
    mode = args.mode.lower()

    if mode == 'backtest':
        success = run_backtest(config, args, logger)
    elif mode in ('live', 'paper'):
        success = run_live_trading(config, args, logger)
    else:
        logger.log_info(f"Onbekende modus: {mode}", level="ERROR")
        success = False

    # Afsluiten
    logger.log_info(f"Sophy Trading System afgesloten - Status: {'Succes' if success else 'Fout'}")
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgramma onderbroken door gebruiker")
        sys.exit(0)
    except Exception as e:
        print(f"\nOnverwachte fout: {str(e)}")
        sys.exit(1)```

-----------

Path: scripts/__init__.py

```python
```

-----------

Path: scripts/ftmo_check.py

```python
import json
import os
import sys

from utils.ftmo_helper import FTMOHelper


def load_config(config_path):
    """Laad configuratie uit JSON bestand"""
    try:
        with open(config_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Configuratiebestand niet gevonden: {config_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Ongeldige JSON in configuratiebestand: {config_path}")
        sys.exit(1)


def main():
    print("\n==== FTMO Compliance Checker ====")
    print("Dit programma controleert of je trading prestaties voldoen aan de FTMO regels.")

    # Controleer of logbestand bestaat
    log_file = os.path.join('../logs', 'trading_journal.csv')
    if not os.path.exists(log_file):
        print(f"\nError: Log bestand niet gevonden: {log_file}")
        print("Voer eerst de TurtleTrader bot uit om trading data te genereren.")
        return

    # Laad configuratie voor initiële balans
    config_path = os.path.join('Sophy/config', 'settings.json')
    try:
        config = load_config(config_path)
        initial_balance = config['mt5'].get('account_balance', 100000)
    except:
        print("\nWaarschuwing: Kon configuratie niet laden, standaard account balans van $100,000 wordt gebruikt.")
        initial_balance = 100000

    print(f"\nAnalyseren van trading data met initiële balans: ${initial_balance:,.2f}")

    # Initialiseer FTMO helper
    ftmo_helper = FTMOHelper(log_file)

    # Genereer rapport
    print("\nGenereren van gedetailleerd FTMO compliance rapport...")
    ftmo_helper.generate_trading_report(initial_balance)

    print("\nWil je nog meer details zien? (j/n): ", end="")
    if input().lower() == 'j':
        # Voer meer gedetailleerde analyse uit
        compliance = ftmo_helper.check_ftmo_compliance(initial_balance)

        if compliance['details']:
            details = compliance['details']
            daily_stats = details['daily_stats']

            print("\n===== Dagelijkse Statistieken =====")
            print(f"{'Datum':<12} {'Balance':<12} {'Dagelijkse P&L':<15} {'Drawdown':<12}")
            print("-" * 55)

            for _, row in daily_stats.iterrows():
                date_str = row['Date'].strftime('%Y-%m-%d')
                balance = f"${row['close_balance']:,.2f}"
                daily_pnl = f"${row['daily_pnl']:,.2f} ({row['daily_pnl_pct']:.2f}%)"
                drawdown = f"{row['daily_drawdown']:.2f}%"

                print(f"{date_str:<12} {balance:<12} {daily_pnl:<15} {drawdown:<12}")

            print("\nAls je voldoet aan alle FTMO regels, kun je doorgaan naar de volgende fase!")

    print("\nBedankt voor het gebruiken van de FTMO Compliance Checker.")


if __name__ == "__main__":
    main()
```

-----------

Path: scripts/main.py

```python
# src/main.py
import time
from datetime import datetime

from src.connector.mt5_connector import MT5Connector
from src.risk.risk_manager import RiskManager
from src.strategy.strategy_factory import StrategyFactory
from src.utils.config import load_config
from src.utils.logger import Logger


def main():
    """Hoofdfunctie voor de Sophy trading applicatie"""
    # Laad configuratie
    config = load_config()

    # Setup logging
    log_file = config['logging'].get('log_file', 'logs/trading_log.csv')
    logger = Logger(log_file)
    logger.log_info("====== Sophy Trading System ======")
    logger.log_info(f"Sessie gestart op {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Creëer componenten
    connector = MT5Connector(config['mt5'], logger)
    risk_manager = RiskManager(config['risk'], logger)

    # Verbind met MT5
    if not connector.connect():
        logger.log_info("Kon geen verbinding maken met MT5. Programma wordt afgesloten.", level="ERROR")
        return

    logger.log_info(f"Verbonden met MT5: {config['mt5']['server']}")

    # Haal strategie naam uit config
    strategy_name = config['strategy']['name']

    # Creëer strategie via factory
    try:
        strategy = StrategyFactory.create_strategy(strategy_name, connector, risk_manager, logger, config)
        logger.log_info(f"Strategie geladen: {strategy_name}")
    except ValueError as e:
        logger.log_info(f"Kon strategie '{strategy_name}' niet initialiseren: {str(e)}", level="ERROR")
        connector.disconnect()
        return

    # Hoofdloop
    try:
        logger.log_info("Trading loop gestart")

        # Log initiële account status
        account_info = connector.get_account_info()
        open_positions = strategy.get_open_positions() if hasattr(strategy, 'get_open_positions') else {}
        logger.log_status(account_info, open_positions)

        while True:
            # Verwerk symbolen volgens strategie
            for symbol in config['mt5']['symbols']:
                # Pas symbol mapping toe indien nodig
                symbol_map = config['mt5'].get('symbol_mapping', {})
                mapped_symbol = symbol_map.get(symbol, symbol)

                # Verwerk symbool
                strategy.process_symbol(mapped_symbol)

            # Controleer FTMO limieten
            account_info = connector.get_account_info()
            open_positions = strategy.get_open_positions() if hasattr(strategy, 'get_open_positions') else {}
            logger.log_status(account_info, open_positions)

            should_stop, reason = risk_manager.check_ftmo_limits(account_info)
            if should_stop:
                logger.log_info(f"Stop trading: {reason}")
                break

            # Wacht voor volgende cyclus
            interval = config.get('interval', 300)  # Default 5 minuten
            logger.log_info(f"Wacht {interval} seconden tot volgende cyclus")
            time.sleep(interval)

    except KeyboardInterrupt:
        logger.log_info("Trading gestopt door gebruiker.")
    except Exception as e:
        logger.log_info(f"Onverwachte fout: {str(e)}", level="ERROR")
    finally:
        # Cleanup
        connector.disconnect()
        logger.log_info("Sessie afgesloten.")


if __name__ == "__main__":
    main()
```

-----------

Path: setup.py

```python
# setup.py
from setuptools import setup, find_packages

setup(
    name="sophy",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.20.0",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "MetaTrader5>=5.0.0",
    ],
    author="Sophy Trading Systems",
    author_email="info@sophytrading.com",
    description="Een Python-gebaseerd algoritmisch trading systeem met Turtle Trading strategie",
    keywords="trading, algoritm, metatrader, ftmo, turtle",
    url="https://github.com/yourusername/sophy",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.9",
)
```

-----------

Path: src/__init__.py

```python
```

-----------

Path: src/analysis/__init__.py

```python
```

-----------

Path: src/analysis/backtester.py

```python
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.strategy.strategy_factory import StrategyFactory
from src.utils.config import load_config
from src.utils.logger import Logger


class DummyConnector:
    """Dummy connector voor backtest doeleinden met geavanceerde datahandling."""

    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.data_cache: Dict[str, pd.DataFrame] = {}

    def get_historical_data(self, symbol: str, timeframe_str: str, bars_count: int) -> pd.DataFrame:
        """Haal historische data op uit CSV bestanden met caching."""
        cache_key = f"{symbol}_{timeframe_str}"
        if cache_key in self.data_cache:
            df = self.data_cache[cache_key]
            return df.iloc[-bars_count:] if len(df) > bars_count else df.copy()

        filename = f"{symbol}_{timeframe_str}.csv"
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.exists(filepath):
            print(f"Bestand niet gevonden: {filepath}")
            return pd.DataFrame()

        df = pd.read_csv(filepath)
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        elif 'time' in df.columns:
            df['date'] = pd.to_datetime(df['time'])
            df.drop('time', axis=1, inplace=True)

        df.columns = [col.lower() for col in df.columns]
        required_cols = {'open', 'high', 'low', 'close', 'tick_volume'}
        if not all(col in df.columns for col in required_cols):
            print(f"Ongeldige data voor {symbol}: ontbrekende kolommen")
            return pd.DataFrame()

        self.data_cache[cache_key] = df
        return df.iloc[-bars_count:] if len(df) > bars_count else df.copy()

    def get_symbol_tick(self, symbol: str) -> Optional[Any]:
        """Simuleer huidige tick gebaseerd op laatste data."""
        cache_key = f"{symbol}_H4"
        if cache_key not in self.data_cache:
            self.get_historical_data(symbol, "H4", 1000)

        if cache_key not in self.data_cache:
            return None

        df = self.data_cache[cache_key]
        last_row = df.iloc[-1]

        class Tick:
            pass

        tick = Tick()
        tick.ask = last_row['close']
        tick.bid = last_row['close'] * 0.999  # Simpele bid/ask spread
        tick.time = last_row['date'].timestamp()
        return tick

    def get_account_info(self) -> Dict[str, Any]:
        """Geef geüpdatete accountinformatie tijdens backtest."""
        return {
            'balance': 100000,
            'equity': 100000,
            'margin': 0,
            'free_margin': 100000,
            'margin_level': 0,
            'profit': 0
        }

    def get_open_positions(self, symbol: Optional[str] = None) -> List[Dict]:
        """Geef open posities terug."""
        return [pos for pos in self.open_positions.values()] if symbol is None else \
            [pos for pos in self.open_positions.values() if pos.get('symbol') == symbol]

    def place_order(self, action: str, symbol: str, volume: float, stop_loss: float, take_profit: float,
                    comment: str) -> Optional[int]:
        """Simuleer het plaatsen van een order."""
        if action not in ['BUY', 'SELL']:
            return None
        ticket = len(self.open_positions) + 1
        self.open_positions[ticket] = {
            'ticket': ticket,
            'symbol': symbol,
            'type': mt5.POSITION_TYPE_BUY if action == 'BUY' else mt5.POSITION_TYPE_SELL,
            'volume': volume,
            'price_open': self.get_symbol_tick(symbol).ask if action == 'BUY' else self.get_symbol_tick(symbol).bid,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'time': datetime.now().timestamp(),
            'profit': 0.0
        }
        return ticket

    def modify_position(self, ticket: int, stop_loss: float, take_profit: float) -> bool:
        """Simuleer het aanpassen van een positie."""
        if ticket in self.open_positions:
            self.open_positions[ticket]['stop_loss'] = stop_loss
            self.open_positions[ticket]['take_profit'] = take_profit
            return True
        return False

    open_positions = {}


class BacktestStrategy:
    """Wrapper voor strategie tijdens backtesting met geavanceerde logica."""

    def __init__(self, strategy, initial_balance: float = 100000):
        self.strategy = strategy
        self.balance = initial_balance
        self.equity = initial_balance
        self.positions: Dict[int, Dict] = {}
        self.trades: List[Dict] = []
        self.logger = self.strategy.logger  # Gebruik de logger van de strategie

    def process_candle(self, symbol: str, candle: Dict[str, Any]) -> Dict[str, Any]:
        """Verwerk een enkele candle en simuleer trades."""
        result = {'signal': None, 'action': None}
        candle_df = pd.DataFrame([candle])
        indicators = self.strategy.calculate_indicators(candle_df)

        # Simuleer tick-gebaseerde data
        tick = self.strategy.connector.get_symbol_tick(symbol)
        if tick is None:
            return result

        process_result = self.strategy.process_symbol(symbol)
        if process_result.get('signal') == 'ENTRY' and process_result.get('action'):
            action = process_result['action']
            volume = process_result.get('volume', 0.1)
            stop_loss = process_result.get('stop_loss', 0)
            ticket = self.strategy.connector.place_order(action, symbol, volume, stop_loss, 0, "Backtest Trade")
            if ticket:
                self.positions[ticket] = {
                    'symbol': symbol,
                    'action': action,
                    'volume': volume,
                    'entry_price': tick.ask if action == 'BUY' else tick.bid,
                    'stop_loss': stop_loss,
                    'open_time': datetime.fromtimestamp(tick.time)
                }
                self.logger.log_trade(symbol, action, tick.ask, volume, stop_loss, 0, "Backtest Entry")
                result.update(process_result)

        # Beheer open posities
        for ticket, pos in list(self.positions.items()):
            current_price = tick.ask if pos['action'] == 'BUY' else tick.bid
            profit = (current_price - pos['entry_price']) * pos['volume'] * (1 if pos['action'] == 'BUY' else -1)
            pos['profit'] = profit
            self.equity = self.balance + sum(p['profit'] for p in self.positions.values())

            # Simuleer stop loss
            if (pos['action'] == 'BUY' and current_price <= pos['stop_loss']) or \
                    (pos['action'] == 'SELL' and current_price >= pos['stop_loss']):
                self.close_position(ticket, current_price)
                result['signal'] = 'EXIT'
                result['action'] = 'CLOSE'

        return result

    def close_position(self, ticket: int, close_price: float):
        """Sluit een positie en update balans."""
        if ticket in self.positions:
            pos = self.positions[ticket]
            profit = (close_price - pos['entry_price']) * pos['volume'] * (1 if pos['action'] == 'BUY' else -1)
            self.balance += profit
            self.trades.append({
                'symbol': pos['symbol'],
                'action': pos['action'],
                'entry_price': pos['entry_price'],
                'exit_price': close_price,
                'volume': pos['volume'],
                'profit': profit,
                'open_time': pos['open_time'],
                'close_time': datetime.now()
            })
            self.logger.log_trade(pos['symbol'], 'SELL' if pos['action'] == 'BUY' else 'BUY', close_price,
                                  pos['volume'], 0, 0, f"Backtest Exit, Profit: {profit:.2f}")
            del self.positions[ticket]


def run_backtest():
    """Voer een geavanceerde backtest uit met configuratie en analyse."""
    print("Backtester module gestart")

    # Laad configuratie
    config = load_config()

    # Setup logger
    log_file = config['logging'].get('log_file', 'logs/backtest_log.csv')
    logger = Logger(log_file)
    logger.log_info("====== Sophy Backtest Started ======")

    # Haal symbols en timeframe op
    symbols = config['mt5'].get('symbols', ['EURUSD'])
    timeframe = config['mt5'].get('timeframe', 'H4')
    start_date = config.get('backtest', {}).get('start_date',
                                                (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d'))
    end_date = config.get('backtest', {}).get('end_date', datetime.now().strftime('%Y-%m-%d'))

    # Setup dummy connector
    data_dir = config.get('data_dir', 'data')
    connector = DummyConnector(data_dir)
    connector.open_positions = {}  # Initialiseer open posities

    # Laad data
    data = {}
    for symbol in symbols:
        df = connector.get_historical_data(symbol, timeframe, 10000)
        if not df.empty:
            df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
            data[symbol] = df
            logger.log_info(
                f"Geladen: {symbol} {timeframe} - {len(df)} candles van {df['date'].min()} tot {df['date'].max()}")
        else:
            logger.log_info(f"Kon geen data laden voor {symbol} {timeframe}", level="ERROR")
            continue

    if not data:
        logger.log_info("Geen data geladen, backtest gestopt", level="ERROR")
        return

    # Maak strategie aan
    strategy_name = config['strategy'].get('name', 'turtle')
    strategy = StrategyFactory.create_strategy(strategy_name, connector, None, logger, config)
    if not strategy:
        logger.log_info(f"Kon strategie {strategy_name} niet aanmaken", level="ERROR")
        return

    backtest = BacktestStrategy(strategy)
    equity_curve = []

    # Voer backtest uit
    for symbol, df in data.items():
        for _, candle in df.iterrows():
            candle_dict = candle.to_dict()
            result = backtest.process_candle(symbol, candle_dict)
            equity_curve.append(backtest.equity)

            # Log status
            account_info = connector.get_account_info()
            account_info['equity'] = backtest.equity
            account_info['balance'] = backtest.balance
            logger.log_status(account_info, connector.get_open_positions())

    # Analyseer resultaten
    total_profit = backtest.balance - 100000
    trades = len(backtest.trades)
    winning_trades = sum(1 for t in backtest.trades if t['profit'] > 0)
    win_rate = (winning_trades / trades * 100) if trades > 0 else 0
    avg_profit = np.mean([t['profit'] for t in backtest.trades if t['profit'] > 0]) if winning_trades > 0 else 0
    avg_loss = np.mean([t['profit'] for t in backtest.trades if t['profit'] < 0]) if len(
        [t for t in backtest.trades if t['profit'] < 0]) > 0 else 0
    drawdown = min(0, min(equity_curve) - 100000) if equity_curve else 0

    logger.log_performance_metrics({
        'total_trades': trades,
        'winning_trades': winning_trades,
        'win_rate': win_rate,
        'avg_profit': avg_profit,
        'avg_loss': avg_loss,
        'total_profit': total_profit,
        'max_drawdown': drawdown,
        'trade_history': backtest.trades
    })

    # Visualiseer resultaten
    plt.figure(figsize=(12, 6))
    plt.plot(equity_curve, label='Equity Curve')
    plt.title(f'Backtest Resultaten - {strategy_name}')
    plt.xlabel('Candles')
    plt.ylabel('Equity')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(os.path.dirname(log_file), 'backtest_equity_curve.png'))
    plt.close()

    logger.log_info(
        f"Backtest voltooid. Totale winst: {total_profit:.2f}, Win Rate: {win_rate:.2f}%, Max Drawdown: {drawdown:.2f}")
    logger.log_info("====== Sophy Backtest Ended ======")


if __name__ == "__main__":
    run_backtest()
```

-----------

Path: src/analysis/optimizer.py

```python
# src/analysis/turtle_optimizer.py
import json
import logging
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union

import matplotlib.pyplot as plt

from src.analysis.advanced_backtester import Backtester
from src.utils.config import load_config
from src.utils.logger import Logger

# Configureer logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("turtle_optimizer")


class WalkForwardOptimizer:
    """
    Walk-Forward Optimalisatie voor handelssystemen om overfitting te voorkomen.

    Deze klasse implementeert walk-forward optimalisatie met verschillende in-sample/out-of-sample
    periodes om een robuustere set van parameters te vinden die goed generaliseert naar nieuwe data.
    """

    def __init__(self, config=None, logger=None):
        """
        Initialiseer de walk-forward optimizer.

        Parameters:
        -----------
        config : Optional[Dict]
            Configuratie dictionary (als None, dan wordt standaard config geladen)
        logger : Optional[Logger]
            Logger instantie (als None, dan wordt een nieuwe gemaakt)
        """
        self.config = config if config else load_config()
        self.logger = logger if logger else Logger(self.config['logging'].get('log_file', 'logs/optimizer_log.csv'))

        # Output directory
        self.output_dir = self.config.get('output', {}).get('data_dir', 'data/optimization')
        os.makedirs(self.output_dir, exist_ok=True)

        # Maak backtester
        self.backtester = Backtester(self.config, self.logger)

        # Visuele stijl instellen
        plt.style.use('ggplot')
        plt.rcParams['figure.figsize'] = (16, 10)

    def optimize(self, strategy_name: str, symbols: List[str], timeframe: str,
                 param_ranges: Dict[str, List[Any]],
                 start_date: Union[str, datetime], end_date: Union[str, datetime],
                 is_period_days: int = 180, oos_period_days: int = 60,
                 windows: int = 3, metric: str = 'sharpe_ratio',
                 min_trades: int = 10, max_workers: Optional[int] = None) -> Dict[str, Any]:
        """
        Voer walk-forward optimalisatie uit.

        Parameters:
        -----------
        strategy_name : str
            Naam van de strategie
        symbols : List[str]
            Lijst met handelssymbolen
        timeframe : str
            Timeframe voor analyse
        param_ranges : Dict[str, List[Any]]
            Dictionary met parameter namen en mogelijke waarden
        start_date : Union[str, datetime]
            Start datum voor gehele test periode
        end_date : Union[str, datetime]
            Eind datum voor gehele test periode
        is_period_days : int
            Aantal dagen voor in-sample periode
        oos_period_days : int
            Aantal dagen voor out-of-sample periode
        windows : int
            Aantal walk-forward windows
        metric : str
            Prestatiemetric om te optimaliseren
        min_trades : int
            Minimum aantal trades voor een geldige test
        max_workers : Optional[int]
            Maximum aantal workers voor parallellisatie

        Returns:
        --------
        Dict[str, Any] : Resultaten van de walk-forward optimalisatie
        """
        self.logger.log_info(f"===== Starten Walk-Forward Optimalisatie: {strategy_name} =====")
        self.logger.log_info(f"Symbolen: {symbols}, Timeframe: {timeframe}")
        self.logger.log_info(f"Optimalisatie metric: {metric}")

        # Converteer data naar datetime
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # Bereken tijdsperiodes
        total_days = (end_date - start_date).days
        window_size = is_period_days + oos_period_days

        if windows * window_size > total_days:
            windows = total_days // window_size
            self.logger.log_info(f"Aangepast aantal windows naar {windows} om binnen datumbereik te passen")

        if windows < 1:
            self.logger.log_info("Datumbereik te klein voor walk-forward optimalisatie", level="ERROR")
            return {"success": False, "error": "Date range too small"}

        # Genereer datumvensters
        date_windows = []
        current_start = start_date

        for i in range(windows):
            is_end = current_start + timedelta(days=is_period_days)
            oos_end = is_end + timedelta(days=oos_period_days)

            if oos_end > end_date:
                oos_end = end_date

            date_windows.append({
                'window': i + 1,
                'is_start': current_start,
                'is_end': is_end,
                'oos_start': is_end,
                'oos_end': oos_end
            })

            current_start = is_end

        self.logger.log_info(f"Gegenereerd {len(date_windows)} walk-forward vensters")

        # Optimaliseer voor elk venster
        window_results = []
        oos_results = []
        best_params_per_window = []

        for window in date_windows:
            window_num = window['window']
            is_start = window['is_start'].strftime('%Y-%m-%d')
            is_end = window['is_end'].strftime('%Y-%m-%d')
            oos_start = window['oos_start'].strftime('%Y-%m-%d')
            oos_end = window['oos_end'].strftime('%Y-%m-%d')

            self.logger.log_info(f"Window {window_num}: In-sample {is_start} tot {is_end}, "
                                 f"Out-of-sample {oos_start} tot {oos_end}")

            # In-sample optimalisatie
            self.logger.log_info(f"In-sample optimalisatie voor window {window_num}...")

            is_results = self.backtester.run_optimization(
                strategy_name=strategy_name,
                symbols=symbols,
                param_ranges=param_ranges,
                start_date=is_start,
                end_date=is_end,
                metric=metric,
                max_workers=max_workers
            )

            window_results.append(is_results)

            if not is_results['success']:
                self.logger.log_info(f"In-sample optimalisatie mislukt voor window {window_num}", level="ERROR")
                continue

            # Get best parameters
            best_params = is_results['best_parameters']
            best_metrics = is_results['best_metrics']

            self.logger.log_info(f"Beste parameters voor window {window_num}: {best_params}")
            self.logger.log_info(f"In-sample {metric}: {best_metrics.get(metric, 0):.4f}")

            # Valideer op out-of-sample periode
            self.logger.log_info(f"Out-of-sample validatie voor window {window_num}...")

            oos_result = self.backtester.run_backtest(
                strategy_name=strategy_name,
                symbols=symbols,
                timeframe=timeframe,
                start_date=oos_start,
                end_date=oos_end,
                parameters=best_params,
                plot_results=False
            )

            oos_results.append(oos_result)

            if not oos_result['success']:
                self.logger.log_info(f"Out-of-sample validatie mislukt voor window {window_num}", level="ERROR")
                continue

            oos_metrics = oos_result['metrics']

            self.logger.log_info(f"Out-of-sample {metric}: {oos_metrics.get(metric, 0):.4f}")
            self.logger.log_info(f"Out-of-sample net profit: {oos_metrics.get('net_profit_pct', 0):.2f}%")

            # Sla beste params op per window
            best_params_per_window.append({
                'window': window_num,
                'is_start': is_start,
                'is_end': is_end,
                'oos_start': oos_start,
                'oos_end': oos_end,
                'parameters': best_params,
                'is_metric': best_metrics.get(metric, 0),
                'oos_metric': oos_metrics.get(metric, 0),
                'is_profit': best_metrics.get('net_profit_pct', 0),
                'oos_profit': oos_metrics.get('net_profit_pct', 0),
                'is_trades': best_metrics.get('total_trades', 0),
                'oos_trades': oos_metrics.get('total_trades', 0)
            })

        # Analyseer walk-forward resultaten
        if not best_params_per_window:
            self.logger.log_info("Geen geldige resultaten voor analyse", level="ERROR")
            return {"success": False, "error": "No valid results"}

        # Bepaal de meest robuuste parameters
        robust_params = self._find_robust_parameters(best_params_per_window, param_ranges)

        # Valideer de robuuste parameters op de gehele periode
        self.logger.log_info(f"Valideren robuuste parameters {robust_params} op volledige periode...")

        full_result = self.backtester.run_backtest(
            strategy_name=strategy_name,
            symbols=symbols,
            timeframe=timeframe,
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d'),
            parameters=robust_params,
            plot_results=True
        )

        if full_result['success']:
            full_metrics = full_result['metrics']
            self.logger.log_info(f"Robuuste parameters validatie: {metric}={full_metrics.get(metric, 0):.4f}, "
                                 f"Net Profit={full_metrics.get('net_profit_pct', 0):.2f}%")

        # Visualiseer en sla resultaten op
        self._plot_walk_forward_results(best_params_per_window, robust_params, metric)
        self._save_optimization_results(
            strategy_name, symbols, metric, best_params_per_window, robust_params, full_result
        )

        return {
            "success": True,
            "best_params_per_window": best_params_per_window,
            "robust_params": robust_params,
            "full_result": full_result,
            "metric": metric
        }

    def _find_robust_parameters(self, window_results: List[Dict], param_ranges: Dict[str, List[Any]]) -> Dict[str, Any]:
        """
        Vind robuuste parameters die goed werken over meerdere periodes.

        Parameters:
        -----------
        window_results : List[Dict]
            Resultaten per window
        param_ranges : Dict[str, List[Any]]
            Mogelijke parameter waarden

        Returns:
        --------
        Dict[str, Any] : Meest robuuste parameterset
        """
        if not window_results:
            return {}

        # Extraheer parameter keys
        param_keys = list(param_ranges.keys())

        # Bereken hoe vaak elke parameter waarde voorkomt
        param_frequency = {param: {} for param in param_keys}

        for result in window_results:
            params = result['parameters']

            for param, value in params.items():
                if param in param_keys:
                    param_frequency[param][value] = param_frequency[param].get(value, 0) + 1

        # Kies de meest voorkomende waarde voor elke parameter
        robust_params = {}

        for param, freq in param_frequency.items():
            if freq:
                # De meest voorkomende waarde
                most_common = max(freq.items(), key=lambda x: x[1])[0]
                robust_params[param] = most_common
            else:
                # Fallback: gemiddelde waarde uit bereik
                values = param_ranges[param]
                if values and all(isinstance(v, (int, float)) for v in values):
                    robust_params[param] = sum(values) / len(values)
                elif values:
                    robust_params[param] = values[0]  # Eerste waarde als fallback

        return robust_params

    def _plot_walk_forward_results(self, window_results: List[Dict],
                                   robust_params: Dict[str, Any], metric: str) -> str:
        """
        Visualiseer walk-forward optimalisatie resultaten.

        Parameters:
        -----------
        window_results : List[Dict]
            Resultaten per window
        robust_params : Dict[str, Any]
            Meest robuuste parameterset
        metric : str
            Optimalisatiemetric

        Returns:
        --------
        str : Pad naar opgeslagen plot
        """
        if not window_results:
            return ""

        # Maak een figuur met 3 subplots
        fig, axs = plt.subplots(3, 1, figsize=(14, 16), gridspec_kw={'height_ratios': [2, 1, 2]})

        # 1. Plot IS vs OOS performance
        windows = [r['window'] for r in window_results]
        is_metrics = [r['is_metric'] for r in window_results]
        oos_metrics = [r['oos_metric'] for r in window_results]

        axs[0].plot(windows, is_metrics, 'b-', marker='o', label=f'In-Sample {metric}')
        axs[0].plot(windows, oos_metrics, 'r-', marker='x', label=f'Out-of-Sample {metric}')

        axs[0].set_title(f'Walk-Forward Optimalisatie: {metric} per Window', fontsize=16)
        axs[0].set_xlabel('Window #', fontsize=14)
        axs[0].set_ylabel(metric, fontsize=14)
        axs[0].grid(True)
        axs[0].legend(fontsize=12)

        # 2. Plot Profit
        is_profit = [r['is_profit'] for r in window_results]
        oos_profit = [r['oos_profit'] for r in window_results]

        axs[1].plot(windows, is_profit, 'g-', marker='o', label='In-Sample Profit %')
        axs[1].plot(windows, oos_profit, 'm-', marker='x', label='Out-of-Sample Profit %')

        axs[1].set_title('Net Profit % per Window', fontsize=16)
        axs[1].set_xlabel('Window #', fontsize=14)
        axs[1].set_ylabel('Net Profit %', fontsize=14)
        axs[1].grid(True)
        axs[1].legend(fontsize=12)

        # 3. Parameter consistency plot
        param_keys = list(robust_params.keys())

        if param_keys:
            param_values = {param: [] for param in param_keys}

            for result in window_results:
                for param in param_keys:
                    param_values[param].append(result['parameters'].get(param, None))

            # Normalize for plotting
            normalized_values = {}
            for param, values in param_values.items():
                if all(isinstance(v, (int, float)) for v in values if v is not None):
                    min_val = min(v for v in values if v is not None)
                    max_val = max(v for v in values if v is not None)

                    if max_val > min_val:
                        normalized_values[param] = [(v - min_val) / (max_val - min_val) if v is not None else None for v
                                                    in values]
                    else:
                        normalized_values[param] = [0.5 if v is not None else None for v in values]
                else:
                    # Categorische waarden
                    unique_values = list(set(v for v in values if v is not None))
                    normalized_values[param] = [
                        unique_values.index(v) / max(1, len(unique_values) - 1) if v in unique_values else None for v in
                        values]

            # Plot normalized parameters
            for param, values in normalized_values.items():
                valid_points = [(i, v) for i, v in enumerate(values, 1) if v is not None]
                if valid_points:
                    x, y = zip(*valid_points)
                    axs[2].plot(x, y, 'o-', label=param)

            axs[2].set_title('Parameter Consistency Across Windows', fontsize=16)
            axs[2].set_xlabel('Window #', fontsize=14)
            axs[2].set_ylabel('Normalized Parameter Value', fontsize=14)
            axs[2].grid(True)
            axs[2].legend(fontsize=12)

            # Voeg robuuste parameters toe als text box
            param_text = "Robust Parameters:\n" + "\n".join([f"{k}: {v}" for k, v in robust_params.items()])
            axs[2].text(0.02, 0.02, param_text, transform=axs[2].transAxes, fontsize=12,
                        bbox=dict(facecolor='white', alpha=0.7), verticalalignment='bottom')

        plt.tight_layout()

        # Sla plot op
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"walk_forward_results_{timestamp}.png")
        plt.savefig(output_path, dpi=150)
        plt.close()

        return output_path

    def _save_optimization_results(self, strategy_name: str, symbols: List[str],
                                   metric: str, window_results: List[Dict],
                                   robust_params: Dict[str, Any], full_result: Dict) -> str:
        """
        Sla optimalisatie resultaten op in JSON formaat.

        Parameters:
        -----------
        strategy_name : str
            Naam van de strategie
        symbols : List[str]
            Lijst met handelssymbolen
        metric : str
            Optimalisatiemetric
        window_results : List[Dict]
            Resultaten per window
        robust_params : Dict[str, Any]
            Meest robuuste parameterset
        full_result : Dict
            Resultaat van backtest met robuuste parameters

        Returns:
        --------
        str : Pad naar opgeslagen resultaten
        """
        # Maak resultaten dictionary
        results = {
            'strategy': strategy_name,
            'symbols': symbols,
            'metric': metric,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'window_results': window_results,
            'robust_params': robust_params,
            'full_metrics': full_result.get('metrics', {}) if full_result.get('success', False) else {}
        }

        # Sla op als JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"walk_forward_{strategy_name}_{timestamp}.json")

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, default=str)

        self.logger.log_info(f"Walk-forward resultaten opgeslagen als {output_path}")
        return output_path


class BayesianOptimizer:
    """
    Bayesiaanse Optimalisatie voor het efficiënt zoeken naar optimale strategie parameters.

    Deze klasse implementeert Bayesiaanse optimalisatie om efficiënter dan grid search
    optimale parameters te vinden door een surrogaat model te gebruiken.
    """

    def __init__(self, config=None, logger=None):
        """
        Initialiseer de Bayesiaanse optimizer.

        Parameters:
        -----------
        config : Optional[Dict]
            Configuratie dictionary (als None, dan wordt standaard config geladen)
        logger : Optional[Logger]
            Logger instantie (als None, dan wordt een nieuwe gemaakt)
        """
        self.config = config if config else load_config()
        self.logger = logger if logger else Logger(self.config['logging'].get('log_file', 'logs/bayesian_opt_log.csv'))

        # Output directory
        self.output_dir = self.config.get('output', {}).get('data_dir', 'data/optimization')
        os.makedirs(self.output_dir, exist_ok=True)

        # Maak backtester
        self.backtester = Backtester(self.config, self.logger)

        try:
            # Probeer scikit-optimize te importeren
            import skopt
            self.skopt_available = True
        except ImportError:
            self.logger.log_info("scikit-optimize niet beschikbaar. Installeer met: pip install scikit-optimize",
                                 level="WARNING")
            self.skopt_available = False

        # Visuele stijl instellen
        plt.style.use('ggplot')
        plt.rcParams['figure.figsize'] = (16, 10)

    def optimize(self, strategy_name: str, symbols: List[str], timeframe: str,
                 param_space: Dict[str, Any], start_date: Union[str, datetime],
                 end_date: Union[str, datetime], n_calls: int = 30,
                 n_initial_points: int = 10, metric: str = 'sharpe_ratio') -> Dict[str, Any]:
        """
        Voer Bayesiaanse optimalisatie uit.

        Parameters:
        -----------
        strategy_name : str
            Naam van de strategie
        symbols : List[str]
            Lijst met handelssymbolen
        timeframe : str
            Timeframe voor analyse
        param_space : Dict[str, Any]
            Dictionary met parameter namen en bereiken:
            Bijvoorbeeld: {'entry_period': (10, 60), 'atr_multiplier': (1.0, 3.0)}
            Voor categorische: {'swing_mode': ['True', 'False']}
        start_date : Union[str, datetime]
            Start datum
        end_date : Union[str, datetime]
            Eind datum
        n_calls : int
            Aantal evaluatiepunten
        n_initial_points : int
            Aantal initiële random punten
        metric : str
            Prestatiemetric om te optimaliseren (bijv. 'sharpe_ratio', 'profit_factor', etc.)

        Returns:
        --------
        Dict[str, Any] : Resultaten van de optimalisatie
        """
        if not self.skopt_available:
            self.logger.log_info("Kan Bayesiaanse optimalisatie niet uitvoeren zonder scikit-optimize", level="ERROR")
            return {"success": False, "error": "scikit-optimize not available"}

        import skopt
        from skopt import gp_minimize
        from skopt.space import Real, Integer, Categorical
        from skopt.utils import use_named_args

        self.logger.log_info(f"===== Starten Bayesiaanse Optimalisatie: {strategy_name} =====")
        self.logger.log_info(f"Symbolen: {symbols}, Timeframe: {timeframe}")
        self.logger.log_info(f"Optimalisatie metric: {metric}")

        # Definieer parameter space in skopt formaat
        dimensions = []
        dimension_names = []

        for param_name, param_def in param_space.items():
            dimension_names.append(param_name)

            if isinstance(param_def, tuple) and len(param_def) == 2:
                low, high = param_def
                if isinstance(low, int) and isinstance(high, int):
                    dimensions.append(Integer(low, high, name=param_name))
                elif isinstance(low, (int, float)) and isinstance(high, (int, float)):
                    dimensions.append(Real(low, high, name=param_name))
            elif isinstance(param_def, list):
                dimensions.append(Categorical(param_def, name=param_name))

        # Conversie van strings naar booleans voor categorische opties
        def process_param_value(param_name, value):
            if param_name in param_space and isinstance(param_space[param_name], list):
                if value == 'True':
                    return True
                elif value == 'False':
                    return False
            return value

        # Definieer evaluatiefunctie
        @use_named_args(dimensions=dimensions)
        def evaluate_params(**params):
            # Converteer categoriën indien nodig
            processed_params = {
                name: process_param_value(name, value)
                for name, value in params.items()
            }

            self.logger.log_info(f"Evalueren parameters: {processed_params}")

            try:
                result = self.backtester.run_backtest(
                    strategy_name=strategy_name,
                    symbols=symbols,
                    timeframe=timeframe,
                    start_date=start_date,
                    end_date=end_date,
                    parameters=processed_params,
                    plot_results=False
                )

                if not result['success']:
                    return -100  # Penalty voor mislukte backtests

                metrics = result['metrics']

                # We minimaliseren, dus negeer de metric
                metric_value = metrics.get(metric, 0)

                if metric in ['sharpe_ratio', 'profit_factor', 'net_profit', 'net_profit_pct', 'win_rate']:
                    return -metric_value  # Negeer omdat we maximaliseren
                else:
                    return metric_value  # Voor metrics die we minimaliseren

            except Exception as e:
                self.logger.log_info(f"Fout bij evalueren parameters: {str(e)}", level="ERROR")
                return -100  # Penalty voor errors

        # Voer optimalisatie uit
        start_time = time.time()

        result = gp_minimize(
            evaluate_params,
            dimensions=dimensions,
            n_calls=n_calls,
            n_initial_points=n_initial_points,
            acq_func='EI',  # Expected Improvement
            noise=0.01,
            verbose=True
        )

        elapsed = time.time() - start_time
        self.logger.log_info(f"Optimalisatie voltooid in {elapsed:.2f} seconden")

        # Analyseer resultaten
        best_params = dict(zip(dimension_names, result.x))

        # Converteer categoriën indien nodig
        best_params = {
            name: process_param_value(name, value)
            for name, value in best_params.items()
        }

        # Negatief van de score voor metrics die we maximaliseren
        best_score = -result.fun if metric in ['sharpe_ratio', 'profit_factor', 'net_profit', 'net_profit_pct',
                                               'win_rate'] else result.fun

        self.logger.log_info(f"Beste parameters gevonden: {best_params}")
        self.logger.log_info(f"Beste {metric}: {best_score:.4f}")

        # Run final backtest met beste parameters
        final_result = self.backtester.run_backtest(
            strategy_name=strategy_name,
            symbols=symbols,
            timeframe=timeframe,
            start_date=start_date,
            end_date=end_date,
            parameters=best_params,
            plot_results=True
        )

        # Visualiseer resultaten
        self._plot_optimization_results(result, dimension_names, metric)
        self._save_optimization_results(
            strategy_name, symbols, metric, result, dimension_names, best_params, final_result
        )

        return {
            "success": True,
            "best_parameters": best_params,
            "best_score": best_score,
            "optimization_result": result,
            "final_backtest": final_result
        }

    def _plot_optimization_results(self, result, dimension_names: List[str], metric: str) -> str:
        """
        Visualiseer optimalisatie resultaten.

        Parameters:
        -----------
        result : skopt.OptimizeResult
            Resultaat van de optimalisatie
        dimension_names : List[str]
            Namen van de dimensies (parameters)
        metric : str
            Optimalisatiemetric

        Returns:
        --------
        str : Pad naar opgeslagen plot
        """
        try:
            import skopt
            from skopt.plots import plot_convergence, plot_objective, plot_evaluations

            # Maak één figuur met 3 subplots
            fig, axs = plt.subplots(3, 1, figsize=(14, 18))

            # 1. Convergentie plot
            plot_convergence(result, ax=axs[0])
            if metric in ['sharpe_ratio', 'profit_factor', 'net_profit', 'net_profit_pct', 'win_rate']:
                # Converteer y-as labels voor metrics die we maximaliseren
                axs[0].set_ylabel(f"Negative {metric}")

            axs[0].set_title(f"Convergence Plot for {metric} Optimization", fontsize=16)

            # 2. Objective plot (alleen voor 1-2 dimensies)
            if len(dimension_names) <= 2:
                try:
                    plot_objective(result, ax=axs[1])
                    axs[1].set_title(f"Objective Surface for {metric}", fontsize=16)
                except Exception as e:
                    self.logger.log_info(f"Kon objective plot niet maken: {str(e)}", level="WARNING")
                    axs[1].set_visible(False)
            else:
                axs[1].set_visible(False)

            # 3. Evaluations plot
            try:
                plot_evaluations(result, ax=axs[2])
                axs[2].set_title("Parameter Evaluations", fontsize=16)
            except Exception as e:
                self.logger.log_info(f"Kon evaluations plot niet maken: {str(e)}", level="WARNING")
                axs[2].set_visible(False)

            plt.tight_layout()

            # Sla plot op
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(self.output_dir, f"bayesian_optimization_{timestamp}.png")
            plt.savefig(output_path, dpi=150)
            plt.close()

            return output_path

        except Exception as e:
            self.logger.log_info(f"Fout bij plotten optimalisatie resultaten: {str(e)}", level="ERROR")
            return ""

    def _save_optimization_results(self, strategy_name: str, symbols: List[str],
                                   metric: str, result, dimension_names: List[str],
                                   best_params: Dict[str, Any], final_result: Dict) -> str:
        """
        Sla optimalisatie resultaten op in JSON formaat.

        Parameters:
        -----------
        strategy_name : str
            Naam van de strategie
        symbols : List[str]
            Lijst met handelssymbolen
        metric : str
            Optimalisatiemetric
        result : skopt.OptimizeResult
            Resultaat van de optimalisatie
        dimension_names : List[str]
            Namen van de dimensies (parameters)
        best_params : Dict[str, Any]
            Beste gevonden parameters
        final_result : Dict
            Resultaat van backtest met beste parameters

        Returns:
        --------
        str : Pad naar opgeslagen resultaten
        """
        # Maak resultaten dictionary
        optimization_data = {
            'strategy': strategy_name,
            'symbols': symbols,
            'metric': metric,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'best_params': best_params,
            'best_score': -result.fun if metric in ['sharpe_ratio', 'profit_factor', 'net_profit', 'net_profit_pct',
                                                    'win_rate'] else result.fun,
            'function_calls': result.nfev,
            'full_metrics': final_result.get('metrics', {}) if final_result.get('success', False) else {}
        }

        # Voeg alle evaluaties toe
        evaluations = []
        for i, (x, y) in enumerate(zip(result.x_iters, result.func_vals)):
            evaluations.append({
                'iteration': i + 1,
                'parameters': dict(zip(dimension_names, x)),
                'score': -y if metric in ['sharpe_ratio', 'profit_factor', 'net_profit', 'net_profit_pct',
                                          'win_rate'] else y
            })

        optimization_data['evaluations'] = evaluations

        # Sla op als JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"bayesian_opt_{strategy_name}_{timestamp}.json")

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(optimization_data, f, indent=2, default=str)

        self.logger.log_info(f"Bayesiaanse optimalisatie resultaten opgeslagen als {output_path}")
        return output_path


def run_walk_forward_optimization():
    """Voer walk-forward optimalisatie uit vanaf command line."""
    print("Walk-Forward Optimalisatie module gestart")

    # Laad configuratie
    config = load_config()

    # Setup logger
    log_file = config['logging'].get('log_file', 'logs/wf_opt_log.csv')
    logger = Logger(log_file)
    logger.log_info("====== Sophy Walk-Forward Optimalisatie Started ======")

    # Initialiseer optimizer
    optimizer = WalkForwardOptimizer(config, logger)

    # Haal parameters op uit config
    symbols = config['mt5'].get('symbols', ['EURUSD'])
    timeframe = config['mt5'].get('timeframe', 'H4')
    strategy_name = config['strategy'].get('name', 'turtle')

    # Definieer parameter bereiken voor turtle strategy
    param_ranges = {
        'entry_period': [20, 40, 60],
        'exit_period': [10, 20, 30],
        'atr_period': [14, 20, 30],
        'atr_multiplier': [1.5, 2.0, 2.5, 3.0],
        'swing_mode': [True, False]
    }

    # Bereken start en einddatum
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365 * 2)  # 2 jaar data

    # Start optimalisatie
    results = optimizer.optimize(
        strategy_name=strategy_name,
        symbols=symbols,
        timeframe=timeframe,
        param_ranges=param_ranges,
        start_date=start_date,
        end_date=end_date,
        is_period_days=180,  # 6 maanden in-sample
        oos_period_days=60,  # 2 maanden out-of-sample
        windows=3,  # 3 windows
        metric='sharpe_ratio'
    )

    if results['success']:
        logger.log_info("Walk-Forward Optimalisatie voltooid")
        logger.log_info(f"Robuuste parameters gevonden: {results['robust_params']}")
    else:
        logger.log_info(f"Walk-Forward Optimalisatie mislukt: {results.get('error', 'Onbekende fout')}", level="ERROR")

    logger.log_info("====== Sophy Walk-Forward Optimalisatie Ended ======")


def run_bayesian_optimization():
    """Voer Bayesiaanse optimalisatie uit vanaf command line."""
    print("Bayesiaanse Optimalisatie module gestart")

    # Laad configuratie
    config = load_config()

    # Setup logger
    log_file = config['logging'].get('log_file', 'logs/bayes_opt_log.csv')
    logger = Logger(log_file)
    logger.log_info("====== Sophy Bayesiaanse Optimalisatie Started ======")

    # Initialiseer optimizer
    optimizer = BayesianOptimizer(config, logger)

    # Haal parameters op uit config
    symbols = config['mt5'].get('symbols', ['EURUSD'])
    timeframe = config['mt5'].get('timeframe', 'H4')
    strategy_name = config['strategy'].get('name', 'turtle')

    # Definieer parameter bereiken voor turtle strategy
    param_space = {
        'entry_period': (10, 60),
        'exit_period': (5, 30),
        'atr_period': (5, 30),
        'atr_multiplier': (1.0, 4.0),
        'swing_mode': ['True', 'False']
    }

    # Bereken start en einddatum
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)  # 1 jaar data

    # Start optimalisatie
    results = optimizer.optimize(
        strategy_name=strategy_name,
        symbols=symbols,
        timeframe=timeframe,
        param_space=param_space,
        start_date=start_date,
        end_date=end_date,
        n_calls=30,  # 30 evaluatiepunten
        n_initial_points=10,  # 10 initiële random punten
        metric='sharpe_ratio'
    )

    if results['success']:
        logger.log_info("Bayesiaanse Optimalisatie voltooid")
        logger.log_info(f"Beste parameters gevonden: {results['best_parameters']}")
        logger.log_info(f"Beste score: {results['best_score']:.4f}")
    else:
        logger.log_info(f"Bayesiaanse Optimalisatie mislukt: {results.get('error', 'Onbekende fout')}", level="ERROR")

    logger.log_info("====== Sophy Bayesiaanse Optimalisatie Ended ======")


if __name__ == "__main__":
    # Kies welke optimalisatiemethode je wilt uitvoeren
    run_walk_forward_optimization()
    # run_bayesian_optimization()  # Uncomment om Bayesiaanse optimalisatie uit te voeren
```

-----------

Path: src/analysis/turtle-backtrader-implementation_claude.py

```python
"""
TurtleTrader Backtrader Implementatie
------------------------------------
Een implementatie van de Turtle Trading-strategie met Backtrader, inclusief MT5-integratie.

Auteur: Senior Python Developer
Versie: 1.0.0
"""

import os
import datetime as dt
import argparse
import logging
import pandas as pd
import numpy as np
import yaml
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Union

# Backtrader en gerelateerde imports
import backtrader as bt
import backtrader.analyzers as btanalyzers
import backtrader.feeds as btfeeds
import backtrader.indicators as btind
import backtrader.strategies as btstrats

# MetaTrader 5 import - mogelijk pas inladen wanneer nodig om afhankelijkheid te verminderen
try:
    import MetaTrader5 as mt5
except ImportError:
    logging.warning("MetaTrader5 module niet gevonden. Alleen offline backtesting beschikbaar.")
    mt5 = None

# Configureer logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("turtletrader_backtest.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("TurtleTrader")

# ---------------------------------
# Data Feed voor MetaTrader 5
# ---------------------------------

class MT5DataFeed(btfeeds.PandasData):
    """
    Klasse voor het verkrijgen van data uit MetaTrader 5 en het omzetten naar
    een Backtrader-compatibel formaat.
    """
    
    params = (
        ('datetime', None),  # Datetime kolom (standaard None gebruikt de index)
        ('open', 'open'),    # Open prijskolom
        ('high', 'high'),    # High prijskolom
        ('low', 'low'),      # Low prijskolom
        ('close', 'close'),  # Close prijskolom
        ('volume', 'tick_volume'),  # Volume kolom
        ('openinterest', None),     # Open interest kolom (niet gebruikt in forex)
    )
    
    @staticmethod
    def fetch_mt5_data(
        symbol: str, 
        timeframe: str, 
        start_date: dt.datetime, 
        end_date: dt.datetime,
        cache_dir: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Haal data op van MetaTrader 5.
        
        Args:
            symbol: Het handelssymbool (bijv. 'EURUSD')
            timeframe: De tijdsinterval in MT5-formaat
            start_date: Startdatum voor de historische data
            end_date: Einddatum voor de historische data
            cache_dir: Directory voor het cachen van data (optioneel)
            
        Returns:
            DataFrame met OHLCV-data
        """
        # Controleer of we de data uit de cache kunnen halen
        if cache_dir:
            cache_path = Path(cache_dir)
            if not cache_path.exists():
                cache_path.mkdir(parents=True)
            
            cache_file = cache_path / f"{symbol}_{timeframe}_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv"
            
            if cache_file.exists():
                logger.info(f"Data geladen uit cache: {cache_file}")
                return pd.read_csv(cache_file, index_col=0, parse_dates=True)
        
        # Controleer of MT5 beschikbaar is
        if mt5 is None:
            raise ImportError("MetaTrader5 module is niet geïnstalleerd of niet beschikbaar.")
        
        # Initialiseer MT5 indien nog niet geïnitialiseerd
        if not mt5.initialize():
            raise ConnectionError(f"Kan niet verbinden met MetaTrader 5: {mt5.last_error()}")
        
        # Vertaal timeframe string naar MT5 timeframe
        timeframe_map = {
            "M1": mt5.TIMEFRAME_M1,
            "M5": mt5.TIMEFRAME_M5,
            "M15": mt5.TIMEFRAME_M15,
            "M30": mt5.TIMEFRAME_M30,
            "H1": mt5.TIMEFRAME_H1,
            "H4": mt5.TIMEFRAME_H4,
            "D1": mt5.TIMEFRAME_D1,
            "W1": mt5.TIMEFRAME_W1,
            "MN1": mt5.TIMEFRAME_MN1
        }
        
        mt5_timeframe = timeframe_map.get(timeframe, mt5.TIMEFRAME_D1)
        
        # Haal data op met extra marge voor indicatoren
        start_with_margin = start_date - dt.timedelta(days=50)  # Extra dagen voor indicators
        
        logger.info(f"Data ophalen van MT5: {symbol}, {timeframe}, {start_date} tot {end_date}")
        
        rates = mt5.copy_rates_range(
            symbol,
            mt5_timeframe,
            start_with_margin,
            end_date
        )
        
        mt5.shutdown()
        
        if rates is None or len(rates) == 0:
            raise ValueError(f"Geen data gevonden voor {symbol} in opgegeven periode.")
        
        # Converteer naar pandas DataFrame
        df = pd.DataFrame(rates)
        
        # Converteer 'time' kolom naar datetime en gebruik als index
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.set_index('time', inplace=True)
        
        # Filter data om alleen de opgegeven range te behouden
        df = df.loc[start_date:end_date]
        
        # Cache de data indien nodig
        if cache_dir:
            df.to_csv(cache_file)
            logger.info(f"Data opgeslagen in cache: {cache_file}")
        
        return df

    @classmethod
    def from_mt5(
        cls, 
        symbol: str,
        timeframe: str,
        start_date: dt.datetime,
        end_date: dt.datetime,
        cache_dir: Optional[str] = None,
        **kwargs
    ) -> 'MT5DataFeed':
        """
        Creëert een Backtrader-datafeed van MT5-data.
        
        Args:
            symbol: Het handelssymbool
            timeframe: De tijdsinterval in MT5-formaat
            start_date: Startdatum voor de historische data
            end_date: Einddatum voor de historische data
            cache_dir: Directory voor het cachen van data (optioneel)
            **kwargs: Extra parameters voor de datafeed
            
        Returns:
            MT5DataFeed object dat kan worden toegevoegd aan een Cerebro-instance
        """
        # Haal data op van MT5
        df = cls.fetch_mt5_data(symbol, timeframe, start_date, end_date, cache_dir)
        
        # Creëer datafeed object
        data_feed = cls(
            dataname=df,
            name=symbol,
            **kwargs
        )
        
        return data_feed

# ---------------------------------
# Turtle Trading Strategie
# ---------------------------------

class TurtleStrategy(bt.Strategy):
    """
    Een implementatie van de Turtle Trading strategie volgens de originele regels,
    aangepast voor gebruik met Backtrader.
    """
    
    params = (
        # Entry parameters
        ('entry_atr_period', 20),     # ATR periode voor entry
        ('n_entry_donchian', 20),     # 20-day breakout voor entry
        
        # Exit parameters
        ('exit_atr_period', 10),      # ATR periode voor exit
        ('n_exit_donchian', 10),      # 10-day breakout voor exit
        
        # Position sizing
        ('atr_position_size', 1.0),   # Percentage van account te riskeren per trade
        ('max_pyramid_units', 4),     # Maximum aantal eenheden per richting
        ('pyramid_delay', 5),         # Minimaal aantal bars tussen pyramiding
        
        # FMTO Trading Regels
        ('profit_target_pct', 10.0),   # Winstdoel: 10% van initieel saldo
        ('max_daily_loss', 5.0),       # Maximaal Dagelijks Verlies: 5% van initieel saldo
        ('max_total_loss', 10.0),      # Maximaal Totaal Verlies: 10% van initieel saldo
        ('min_trading_days', 4),       # Minimaal Handelsdagen: 4 dagen met trades
        
        # MT5 specifieke parameters
        ('commission_per_lot', 7.0),   # Commissie per lot in account currency
        ('slippage_pips', 1.0),        # Slippage in pips
        
        # Verbosity
        ('printlog', False),           # Print log output
    )
    
    def log(self, txt, dt=None):
        """Logging functie voor de strategie."""
        if self.params.printlog:
            dt = dt or self.datas[0].datetime.date(0)
            print(f'{dt.isoformat()}: {txt}')
    
    def __init__(self):
        """Initialiseer de strategie en de indicatoren."""
        # Houd trading tellers bij
        self.order = None  # Huidige lopende order
        self.units_long = {}  # Aantal long posities per data
        self.units_short = {}  # Aantal short posities per data
        self.last_entry_bar = {}  # Laatste bar waar een entry plaatsvond
        self.trade_dates = set()  # Set van datums waarop we hebben gehandeld
        self.initial_balance = self.broker.getvalue()  # Startbalans voor FMTO regels
        self.daily_pnl = {}  # Dict met dagelijkse P&L
        
        # Initialiseer voor elke data
        for i, data in enumerate(self.datas):
            # Sla symbool op in datainfo voor makkelijk refereren
            data.symbol = data._name
            
            # Initialiseer tellers per symbool
            self.units_long[data] = 0
            self.units_short[data] = 0
            self.last_entry_bar[data] = 0
            
            # Donchian Channel voor entry signalen
            data.dc_high_entry = btind.Highest(data.high, period=self.params.n_entry_donchian)
            data.dc_low_entry = btind.Lowest(data.low, period=self.params.n_entry_donchian)
            
            # Donchian Channel voor exit signalen
            data.dc_high_exit = btind.Highest(data.high, period=self.params.n_exit_donchian)
            data.dc_low_exit = btind.Lowest(data.low, period=self.params.n_exit_donchian)
            
            # ATR voor position sizing
            data.atr_entry = btind.ATR(data, period=self.params.entry_atr_period)
            data.atr_exit = btind.ATR(data, period=self.params.exit_atr_period)
    
    def notify_order(self, order):
        """Ontvang meldingen over order status wijzigingen."""
        if order.status in [order.Submitted, order.Accepted]:
            # Order is ingediend/geaccepteerd - nog niet uitgevoerd
            return
        
        # Check of order is voltooid
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'KOOP UITGEVOERD - Prijs: {order.executed.price:.5f}, Kosten: {order.executed.value:.2f}, Comm: {order.executed.comm:.2f}')
            elif order.issell():
                self.log(f'VERKOOP UITGEVOERD - Prijs: {order.executed.price:.5f}, Kosten: {order.executed.value:.2f}, Comm: {order.executed.comm:.2f}')
            
            # Update de datum waarop we hebben gehandeld
            current_date = self.datas[0].datetime.date(0)
            self.trade_dates.add(current_date)
        
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log(f'Order {order.Status[order.status]}')
        
        # Reset het order object
        self.order = None
    
    def notify_trade(self, trade):
        """Ontvang meldingen over afgeronde trades."""
        if trade.isclosed:
            self.log(f'HANDEL GESLOTEN - Bruto W/V: {trade.pnl:.2f}, Netto W/V: {trade.pnlcomm:.2f}')
            
            # Update dagelijkse P&L
            current_date = self.datas[0].datetime.date(0)
            if current_date not in self.daily_pnl:
                self.daily_pnl[current_date] = 0.0
            self.daily_pnl[current_date] += trade.pnlcomm
    
    def prenext(self):
        """Schakel door naar next() zodra er voldoende data is voor alle indicatoren."""
        self.next()
    
    def is_trend_following_allowed(self):
        """
        Controleert of we mogen handelen volgens de FMTO-regels.
        
        Returns:
            bool: True als handelen is toegestaan, False anders
        """
        current_balance = self.broker.getvalue()
        
        # Check profit target
        if (current_balance - self.initial_balance) >= (self.params.profit_target_pct / 100) * self.initial_balance:
            self.log(f"Winstdoel bereikt: {current_balance:.2f}, gestopt met handelen")
            return False
        
        # Check maximum totale verlies
        if (self.initial_balance - current_balance) >= (self.params.max_total_loss / 100) * self.initial_balance:
            self.log(f"Maximum totale verlies bereikt: {current_balance:.2f}, gestopt met handelen")
            return False
        
        # Check dagelijks verlies
        current_date = self.datas[0].datetime.date(0)
        daily_loss = self.daily_pnl.get(current_date, 0.0)
        
        if daily_loss < -(self.params.max_daily_loss / 100) * self.initial_balance:
            self.log(f"Dagelijks verlies limiet bereikt: {daily_loss:.2f}, gestopt met handelen op deze dag")
            return False
        
        return True
    
    def next(self):
        """
        Hoofdlogica van de Turtle Trading strategie die elke bar wordt uitgevoerd.
        """
        # Controleer FMTO regels
        if not self.is_trend_following_allowed():
            return
        
        # Verwerk elke data stream (elk symbool)
        for i, data in enumerate(self.datas):
            # Skip als we nog niet genoeg bars hebben voor de indicatoren
            if len(data) < max(self.params.n_entry_donchian, self.params.n_exit_donchian):
                continue
            
            # Skip als we al een order hebben lopen voor dit instrument
            if self.order:
                continue
            
            # Haal positie voor dit symbool op
            pos = self.getposition(data)
            
            # Entry logica
            if not pos:  # Geen positie, check voor nieuwe entry
                # Long entry: prijs breekt boven donchian high
                if data.close[0] > data.dc_high_entry[-1]:
                    # Check of we minder dan het maximum aantal units hebben
                    if self.units_long[data] < self.params.max_pyramid_units:
                        self.go_long(data)
                
                # Short entry: prijs breekt onder donchian low
                elif data.close[0] < data.dc_low_entry[-1]:
                    # Check of we minder dan het maximum aantal units hebben
                    if self.units_short[data] < self.params.max_pyramid_units:
                        self.go_short(data)
            
            # Exit logica voor bestaande posities
            else:
                # Long positie exit
                if pos.size > 0 and data.close[0] < data.dc_low_exit[0]:
                    self.log(f'LONG EXIT SIGNAAL - {data.symbol}')
                    self.order = self.close(data=data)
                    self.units_long[data] = 0
                
                # Short positie exit
                elif pos.size < 0 and data.close[0] > data.dc_high_exit[0]:
                    self.log(f'SHORT EXIT SIGNAAL - {data.symbol}')
                    self.order = self.close(data=data)
                    self.units_short[data] = 0
                
                # Pyramiding voor long posities
                elif pos.size > 0 and data.close[0] > data.dc_high_entry[-1]:
                    # Check pyramiding voorwaarden
                    current_bar = len(data)
                    if (self.units_long[data] < self.params.max_pyramid_units and 
                        current_bar > self.last_entry_bar[data] + self.params.pyramid_delay):
                        self.go_long(data)
                
                # Pyramiding voor short posities
                elif pos.size < 0 and data.close[0] < data.dc_low_entry[-1]:
                    # Check pyramiding voorwaarden
                    current_bar = len(data)
                    if (self.units_short[data] < self.params.max_pyramid_units and 
                        current_bar > self.last_entry_bar[data] + self.params.pyramid_delay):
                        self.go_short(data)
    
    def get_position_size(self, data, is_long=True):
        """
        Bereken positiegrootte gebaseerd op ATR en accountbalans.
        
        Args:
            data: Datafeed voor het instrument
            is_long: True voor long posities, False voor short posities
            
        Returns:
            float: Aantal contracten/lots om te verhandelen
        """
        # Bepaal risicobedrag (% van account)
        risk_amount = self.broker.getvalue() * (self.params.atr_position_size / 100)
        
        # Gebruik current ATR
        atr_value = data.atr_entry[0]
        
        # Bepaal stop loss afstand (2 * ATR)
        stop_distance = 2 * atr_value
        
        # Bereken positiegrootte (risico / stop afstand)
        # In Backtrader worden contractgrootte en heboom in de Broker-instellingen afgehandeld
        # Voor Forex: 1 lot = 100,000 eenheden van de basisvaluta
        position_size = risk_amount / stop_distance
        
        # Pas commission aan (eventueel)
        
        return position_size
    
    def go_long(self, data):
        """
        Open een long positie.
        
        Args:
            data: De datafeed voor het instrument
        """
        price = data.close[0]
        size = self.get_position_size(data, is_long=True)
        
        self.log(f'LONG ENTRY SIGNAAL - {data.symbol}, Prijs: {price:.5f}, Grootte: {size:.2f}')
        
        # Plaats de order
        self.order = self.buy(data=data, size=size)
        
        # Update tellers
        self.units_long[data] += 1
        self.last_entry_bar[data] = len(data)
    
    def go_short(self, data):
        """
        Open een short positie.
        
        Args:
            data: De datafeed voor het instrument
        """
        price = data.close[0]
        size = self.get_position_size(data, is_long=False)
        
        self.log(f'SHORT ENTRY SIGNAAL - {data.symbol}, Prijs: {price:.5f}, Grootte: {size:.2f}')
        
        # Plaats de order
        self.order = self.sell(data=data, size=size)
        
        # Update tellers
        self.units_short[data] += 1
        self.last_entry_bar[data] = len(data)
    
    def stop(self):
        """Wordt aangeroepen aan het einde van de backtest."""
        # Check of we aan de minimale handelsdagen-eis hebben voldaan
        if len(self.trade_dates) < self.params.min_trading_days:
            self.log(f"Waarschuwing: Niet voldaan aan minimale handelsdagen eis. Gehandeld op {len(self.trade_dates)} dagen, minimum is {self.params.min_trading_days}")
        
        # Print eindresultaat
        self.log(f'Backtest voltooid. Eindbalans: {self.broker.getvalue():.2f}')

# ---------------------------------
# Backtest Runner
# ---------------------------------

class TurtleBacktester:
    """
    Hoofdklasse voor het uitvoeren van backtests met de Turtle Trading strategie.
    """
    
    def __init__(self, config=None, config_file=None):
        """
        Initialiseer de backtester met een configuratie.
        
        Args:
            config: Dictionary met configuratie-instellingen
            config_file: Pad naar een YAML-configuratiebestand
        """
        if config_file:
            with open(config_file, 'r') as f:
                self.config = yaml.safe_load(f)
        else:
            self.config = config or {}
        
        # Stel defaults in voor missende configuratiewaarden
        self._set_config_defaults()
    
    def _set_config_defaults(self):
        """Stel default waarden in voor missende configuratie-items."""
        defaults = {
            'market_data': {
                'symbols': ['EURUSD'],
                'start_date': dt.datetime.now() - dt.timedelta(days=365),
                'end_date': dt.datetime.now(),
                'timeframe': 'D1',
                'data_directory': './data_cache',
                'cache_data': True,
            },
            'account': {
                'initial_balance': 10000.0,
                'commission_per_lot': 7.0,
                'slippage_pips': 1.0,
                'leverage': 100.0,
            },
            'fmto_rules': {
                'profit_target_pct': 10.0,
                'max_daily_loss_pct': 5.0,
                'max_total_loss_pct': 10.0,
                'min_trading_days': 4,
            },
            'turtle_parameters': {
                'entry_atr_period': 20,
                'n_entry_donchian': 20,
                'exit_atr_period': 10,
                'n_exit_donchian': 10,
                'atr_position_size_factor': 1.0,
                'max_pyramid_units': 4,
                'pyramid_delay': 5,
            },
            'output': {
                'save_results': True,
                'results_dir': './results',
                'plot_results': True,
                'print_log': False,
            }
        }
        
        # Controleer en vul ontbrekende configuratiewaarden aan
        for section, section_defaults in defaults.items():
            if section not in self.config:
                self.config[section] = {}
            
            for key, value in section_defaults.items():
                if key not in self.config[section]:
                    self.config[section][key] = value
    
    def run_backtest(self):
        """
        Voer de backtest uit met de opgegeven configuratie.
        
        Returns:
            Dict met de resultaten van de backtest
        """
        # Initialiseer Cerebro
        cerebro = bt.Cerebro()
        
        # Voeg strategie toe met parameters uit config
        cerebro.addstrategy(
            TurtleStrategy,
            # Strategie parameters
            entry_atr_period=self.config['turtle_parameters']['entry_atr_period'],
            n_entry_donchian=self.config['turtle_parameters']['n_entry_donchian'],
            exit_atr_period=self.config['turtle_parameters']['exit_atr_period'],
            n_exit_donchian=self.config['turtle_parameters']['n_exit_donchian'],
            atr_position_size=self.config['turtle_parameters']['atr_position_size_factor'],
            max_pyramid_units=self.config['turtle_parameters']['max_pyramid_units'],
            pyramid_delay=self.config['turtle_parameters']['pyramid_delay'],
            
            # FMTO regels
            profit_target_pct=self.config['fmto_rules']['profit_target_pct'],
            max_daily_loss=self.config['fmto_rules']['max_daily_loss_pct'],
            max_total_loss=self.config['fmto_rules']['max_total_loss_pct'],
            min_trading_days=self.config['fmto_rules']['min_trading_days'],
            
            # MT5 parameters
            commission_per_lot=self.config['account']['commission_per_lot'],
            slippage_pips=self.config['account']['slippage_pips'],
            
            # Logging
            printlog=self.config['output']['print_log']
        )
        
        # Converteer datums als nodig
        start_date = self.config['market_data']['start_date']
        end_date = self.config['market_data']['end_date']
        
        if isinstance(start_date, str):
            start_date = dt.datetime.fromisoformat(start_date)
        if isinstance(end_date, str):
            end_date = dt.datetime.fromisoformat(end_date)
        
        # Voeg data toe voor elk symbool
        symbols = self.config['market_data']['symbols']
        timeframe = self.config['market_data']['timeframe']
        cache_dir = self.config['market_data']['data_directory'] if self.config['market_data']['cache_data'] else None
        
        for symbol in symbols:
            # Probeer data uit MT5 te krijgen
            try:
                data = MT5DataFeed.from_mt5(
                    symbol=symbol,
                    timeframe=timeframe,
                    start_date=start_date,
                    end_date=end_date,
                    cache_dir=cache_dir
                )
                cerebro.adddata(data)
                logger.info(f"Data toegevoegd voor {symbol}")
            except Exception as e:
                logger.error(f"Fout bij toevoegen van {symbol}: {e}")
                # Hier zou je kunnen kiezen om CSV of andere databronnen te proberen als MT5 faalt
        
        # Stel broker parameters in
        cerebro.broker.setcash(self.config['account']['initial_balance'])
        cerebro.broker.setcommission(commission=self.config['account']['commission_per_lot'] / 100000)  # Commissie per eenheid van de basisvaluta
        
        # Leverage instellen voor Forex
        # In backtrader impliceert leverage eigenlijk marginvereisten
        # bijv. leverage 100 betekent 1% margin requirement
        cerebro.broker.set_leverage(self.config['account']['leverage'])
        
        # Voeg analyzers toe voor prestatiemeeting
        cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='sharpe')
        cerebro.addanalyzer(btanalyzers.DrawDown, _name='drawdown')
        cerebro.addanalyzer(btanalyzers.Returns, _name='returns')
        cerebro.addanalyzer(btanalyzers.TradeAnalyzer, _name='trades')
        cerebro.addanalyzer(btanalyzers.SQN, _name='sqn')
        
        # Voer backtest uit
        logger.info("Start backtest uitvoering")
        start_value = self.config['account']['initial_balance']
        results = cerebro.run()
        end_value = cerebro.broker.getvalue()
        
        # Haal resultaten op uit analyzers
        strat = results[0]
        
        sharpe = strat.analyzers.sharpe.get_analysis()
        drawdown = strat.analyzers.drawdown.get_analysis()
        returns = strat.analyzers.returns.get_analysis()
        trades = strat.analyzers.trades.get_analysis()
        sqn = strat.analyzers.sqn.get_analysis()
        
        # Verzamel statistieken
        stats = {
            'initial_balance': start_value,
            'final_balance': end_value,
            'net_profit': end_value - start_value,
            'return_pct': ((end_value / start_value) - 1) * 100,
            'max_drawdown_pct': drawdown['max']['drawdown'] * 100 if 'max' in drawdown else 0,
            'max_drawdown_money': drawdown['max']['moneydown'] if 'max' in drawdown else 0,
            'sharpe_ratio': sharpe['sharperatio'] if 'sharperatio' in sharpe else 0,
            'sqn': sqn['sqn'] if 'sqn' in sqn else 0,
            'total_trades': trades['total']['total'] if 'total' in trades else 0,
            'win_rate': (trades['won']['total'] / trades['total']['total'] * 100) if 'won' in trades and 'total' in trades and trades['total']['total'] > 0 else 0,
            'profit_factor': trades['won']['pnl']['gross'] / abs(trades['lost']['pnl']['gross']) if 'won' in trades and 'lost' in trades and 'pnl' in trades['lost'] and trades['lost']['pnl']['gross'] != 0 else 0,
        }
        
                    # Plot resultaten als gewenst
        if self.config['output']['plot_results']:
            cerebro.plot(style='candle', barup='green', bardown='red', volume=True)
        
        # Sla resultaten op als gewenst
        if self.config['output']['save_results']:
            output_dir = Path(self.config['output']['results_dir'])
            if not output_dir.exists():
                output_dir.mkdir(parents=True)
            
            # Genereer bestandsnaam
            symbols_str = "_".join(symbols)
            timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Sla statistieken op als JSON
            stats_file = output_dir / f"backtest_stats_{symbols_str}_{timestamp}.json"
            with open(stats_file, 'w') as f:
                json.dump(stats, f, indent=4)
            
            logger.info(f"Statistieken opgeslagen in {stats_file}")
        
        logger.info(f"Backtest voltooid. Beginbalans: ${start_value:.2f}, Eindbalans: ${end_value:.2f}, "
                  f"Rendement: {stats['return_pct']:.2f}%, Max Drawdown: {stats['max_drawdown_pct']:.2f}%")
        
        return stats
    
    def run_parameter_optimization(self, parameter_name, parameter_range):
        """
        Voer optimalisatie uit voor een specifieke parameter.
        
        Args:
            parameter_name: Naam van de parameter om te optimaliseren
            parameter_range: Lijst met waarden om te testen
            
        Returns:
            List met resultaten voor elke parameter waarde
        """
        results = []
        
        for param_value in parameter_range:
            logger.info(f"Optimalisatie: Testen {parameter_name} = {param_value}")
            
            # Maak kopie van config en update de parameter
            config_copy = self.config.copy()
            
            # Zoek de juiste sectie voor de parameter
            for section in config_copy:
                if isinstance(config_copy[section], dict) and parameter_name in config_copy[section]:
                    config_copy[section][parameter_name] = param_value
                    break
            
            # Maak backtester met nieuwe config
            backtester = TurtleBacktester(config=config_copy)
            
            # Run backtest en voeg resultaten toe
            try:
                stats = backtester.run_backtest()
                stats['parameter'] = parameter_name
                stats['value'] = param_value
                results.append(stats)
            except Exception as e:
                logger.error(f"Fout bij optimalisatie {parameter_name}={param_value}: {e}")
        
        # Sorteer resultaten op rendement
        results.sort(key=lambda x: x['return_pct'], reverse=True)
        
        # Toon beste resultaten
        if results:
            logger.info(f"Optimalisatie resultaten voor {parameter_name}:")
            logger.info(f"Beste waarde: {results[0]['value']}, Rendement: {results[0]['return_pct']:.2f}%")
        
        return results
    
    @staticmethod
    def plot_optimization_results(results, parameter_name, output_dir=None):
        """
        Plot de resultaten van de parameteroptimalisatie.
        
        Args:
            results: Lijst met resultaten dictionaries
            parameter_name: Naam van de geoptimaliseerde parameter
            output_dir: Directory om plots op te slaan (optioneel)
        """
        import matplotlib.pyplot as plt
        
        # Controleer of er resultaten zijn
        if not results:
            logger.warning("Geen resultaten om te plotten")
            return
        
        # Sorteer resultaten op parameterwaarde
        results.sort(key=lambda x: x['value'])
        
        # Haal waarden op voor plot
        param_values = [r['value'] for r in results]
        returns = [r['return_pct'] for r in results]
        drawdowns = [r['max_drawdown_pct'] for r in results]
        sharpes = [r['sharpe_ratio'] for r in results]
        
        # Maak plot
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 15), sharex=True)
        
        # Plot rendement vs parameter
        ax1.plot(param_values, returns, 'o-', color='blue')
        ax1.set_ylabel('Rendement (%)')
        ax1.set_title(f'Optimalisatie van {parameter_name}')
        ax1.grid(True)
        
        # Plot drawdown vs parameter
        ax2.plot(param_values, drawdowns, 'o-', color='red')
        ax2.set_ylabel('Max Drawdown (%)')
        ax2.grid(True)
        
        # Plot Sharpe ratio vs parameter
        ax3.plot(param_values, sharpes, 'o-', color='green')
        ax3.set_xlabel(parameter_name)
        ax3.set_ylabel('Sharpe Ratio')
        ax3.grid(True)
        
        plt.tight_layout()
        
        # Sla plot op indien gewenst
        if output_dir:
            output_path = Path(output_dir)
            if not output_path.exists():
                output_path.mkdir(parents=True)
            
            timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
            plot_file = output_path / f"optimization_{parameter_name}_{timestamp}.png"
            plt.savefig(plot_file)
            logger.info(f"Optimalisatieplot opgeslagen in {plot_file}")
        
        plt.show()

# ---------------------------------
# Command Line Interface
# ---------------------------------

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='TurtleTrader Backtrader')
    
    parser.add_argument('--config', type=str, default='config.yaml',
                      help='Pad naar configuratiebestand (default: config.yaml)')
    
    parser.add_argument('--optimize', type=str, default=None,
                      help='Parameter om te optimaliseren')
    
    parser.add_argument('--range', type=str, default=None,
                      help='Range voor optimalisatie (komma-gescheiden waarden)')
    
    parser.add_argument('--symbols', type=str, default=None,
                      help='Handelssymbolen (komma-gescheiden)')
    
    parser.add_argument('--start', type=str, default=None,
                      help='Startdatum (YYYY-MM-DD)')
    
    parser.add_argument('--end', type=str, default=None,
                      help='Einddatum (YYYY-MM-DD)')
    
    parser.add_argument('--timeframe', type=str, default=None,
                      choices=['M1', 'M5', 'M15', 'M30', 'H1', 'H4', 'D1', 'W1', 'MN1'],
                      help='Timeframe voor backtesting')
    
    return parser.parse_args()

def create_default_config():
    """Creëer een default configuratiebestand."""
    config = {
        'market_data': {
            'symbols': ['EURUSD'],
            'start_date': (dt.datetime.now() - dt.timedelta(days=365)).strftime('%Y-%m-%d'),
            'end_date': dt.datetime.now().strftime('%Y-%m-%d'),
            'timeframe': 'D1',
            'data_directory': './data_cache',
            'cache_data': True,
        },
        'account': {
            'initial_balance': 10000.0,
            'commission_per_lot': 7.0,
            'slippage_pips': 1.0,
            'leverage': 100.0,
        },
        'fmto_rules': {
            'profit_target_pct': 10.0,
            'max_daily_loss_pct': 5.0,
            'max_total_loss_pct': 10.0,
            'min_trading_days': 4,
        },
        'turtle_parameters': {
            'entry_atr_period': 20,
            'n_entry_donchian': 20,
            'exit_atr_period': 10,
            'n_exit_donchian': 10,
            'atr_position_size_factor': 1.0,
            'max_pyramid_units': 4,
            'pyramid_delay': 5,
        },
        'output': {
            'save_results': True,
            'results_dir': './results',
            'plot_results': True,
            'print_log': False,
        }
    }
    
    return config

def main():
    """Hoofdfunctie voor command line gebruik."""
    # Parse command line argumenten
    args = parse_args()
    
    # Bepaal configuratie
    if os.path.exists(args.config):
        logger.info(f"Configuratiebestand laden: {args.config}")
        backtester = TurtleBacktester(config_file=args.config)
    else:
        logger.warning(f"Configuratiebestand {args.config} niet gevonden, gebruik defaults")
        config = create_default_config()
        backtester = TurtleBacktester(config=config)
    
    # Override configuratie met command line argumenten
    if args.symbols:
        backtester.config['market_data']['symbols'] = args.symbols.split(',')
    
    if args.start:
        backtester.config['market_data']['start_date'] = dt.datetime.strptime(args.start, '%Y-%m-%d')
    
    if args.end:
        backtester.config['market_data']['end_date'] = dt.datetime.strptime(args.end, '%Y-%m-%d')
    
    if args.timeframe:
        backtester.config['market_data']['timeframe'] = args.timeframe
    
    # Toon configuratie
    logger.info("Gebruik de volgende configuratie:")
    for section, items in backtester.config.items():
        logger.info(f"{section}:")
        for key, value in items.items():
            logger.info(f"  {key}: {value}")
    
    # Voer optimalisatie uit indien gevraagd
    if args.optimize and args.range:
        logger.info(f"Start optimalisatie van {args.optimize}")
        param_range = [float(x) if '.' in x else int(x) for x in args.range.split(',')]
        results = backtester.run_parameter_optimization(args.optimize, param_range)
        
        # Plot optimalisatieresultaten
        TurtleBacktester.plot_optimization_results(
            results, 
            args.optimize, 
            backtester.config['output']['results_dir']
        )
    else:
        # Voer normale backtest uit
        logger.info("Start backtest")
        stats = backtester.run_backtest()
        
        # Toon resultaten
        logger.info("==== Backtest Resultaten ====")
        logger.info(f"Rendement: {stats['return_pct']:.2f}%")
        logger.info(f"Sharpe Ratio: {stats['sharpe_ratio']:.2f}")
        logger.info(f"Max Drawdown: {stats['max_drawdown_pct']:.2f}%")
        logger.info(f"Totaal aantal trades: {stats['total_trades']}")
        logger.info(f"Win percentage: {stats['win_rate']:.2f}%")
        logger.info(f"Profit Factor: {stats['profit_factor']:.2f}")
        logger.info(f"SQN: {stats['sqn']:.2f}")

if __name__ == "__main__":
    main()
```

-----------

Path: src/connector/__init__.py

```python
```

-----------

Path: src/connector/mt5_connector.py

```python
# src/connector/mt5_connector.py
import time
from typing import Dict, List, Optional, Any

import MetaTrader5 as mt5
import pandas as pd


class MT5Connector:
    """Verzorgt alle interacties met het MetaTrader 5 platform"""

    def __init__(self, config: Dict[str, any], logger: any) -> None:
        """
        Initialiseer de MT5 connector met configuratie

        Args:
            config: Configuratie dictionary met MT5 connectie parameters
            logger: Logger instance voor het registreren van gebeurtenissen
        """
        self.config = config
        self.logger = logger
        self.connected = False
        self._initialize_error_messages()
        self.timeframe_map = {
            'M1': mt5.TIMEFRAME_M1,
            'M5': mt5.TIMEFRAME_M5,
            'M15': mt5.TIMEFRAME_M15,
            'M30': mt5.TIMEFRAME_M30,
            'H1': mt5.TIMEFRAME_H1,
            'H4': mt5.TIMEFRAME_H4,
            'D1': mt5.TIMEFRAME_D1,
            'W1': mt5.TIMEFRAME_W1,
            'MN1': mt5.TIMEFRAME_MN1
        }

    def _initialize_error_messages(self) -> None:
        """Initialiseer foutmeldingen voor MT5 verbinding"""
        self.error_messages = {
            10013: "Ongeldige parameters voor verbinding",
            10014: "Verkeerde login of wachtwoord",
            10015: "Verkeerde server opgegeven",
            10016: "MT5 niet geïnstalleerd of niet gevonden",
            10018: "Verbinding met de server mislukt",
            10019: "Geen respons van server"
        }

    def connect(self) -> bool:
        """
        Maak verbinding met MT5 met uitgebreide foutafhandeling

        Returns:
            bool: True als verbinding succesvol, False anders
        """
        # Controleer of MT5 al is geïnitialiseerd
        if mt5.terminal_info() is not None and self.connected:
            self.logger.log_info("Al verbonden met MT5")
            return True

        # Sluit eerder gemaakte verbindingen
        mt5.shutdown()

        # Initialiseer MT5
        self.logger.log_info(f"Verbinden met MT5 op pad: {self.config.get('mt5_pathway', 'standaard pad')}")
        init_result = mt5.initialize(
            path=self.config.get('mt5_pathway'),
            login=self.config.get('login'),
            password=self.config.get('password'),
            server=self.config.get('server')
        )

        if not init_result:
            error_code = mt5.last_error()
            error_message = self.error_messages.get(
                error_code, f"Onbekende MT5 error: {error_code}")
            self.logger.log_info(f"MT5 initialisatie mislukt: {error_message}", level="ERROR")
            return False

        # Controleer verbinding
        if not mt5.terminal_info():
            self.logger.log_info("MT5 terminal info niet beschikbaar", level="ERROR")
            return False

        # Verbinding gemaakt
        self.connected = True
        account_info = mt5.account_info()

        if account_info:
            self.logger.log_info(f"Verbonden met MT5 account: {account_info.login}, "
                                 f"Server: {account_info.server}, "
                                 f"Type: {account_info.trade_mode_description}")
            return True
        else:
            self.logger.log_info("Kon geen account info ophalen", level="ERROR")
            return False

    def disconnect(self) -> None:
        """Sluit verbinding met MT5"""
        if self.connected:
            mt5.shutdown()
            self.connected = False
            self.logger.log_info("Verbinding met MT5 afgesloten")

    def get_account_info(self) -> Dict[str, Any]:
        """
        Haal account informatie op van MT5

        Returns:
            Dict met account eigenschappen
        """
        if not self.connected:
            self.logger.log_info("Niet verbonden met MT5", level="ERROR")
            return {}

        account_info = mt5.account_info()
        if not account_info:
            self.logger.log_info("Kon account informatie niet ophalen", level="ERROR")
            return {}

        # Converteer naar dictionary
        result = {
            'login': account_info.login,
            'balance': account_info.balance,
            'equity': account_info.equity,
            'margin': account_info.margin,
            'free_margin': account_info.margin_free,
            'profit': account_info.profit,
            'margin_level': (account_info.equity / account_info.margin * 100
                             if account_info.margin > 0 else 0)
        }

        return result

    def get_timeframe_constant(self, timeframe_str: str) -> int:
        """
        Converteer timeframe string naar MT5 constante

        Args:
            timeframe_str: Timeframe als string (bijv. 'H4')

        Returns:
            MT5 timeframe constante
        """
        return self.timeframe_map.get(timeframe_str, mt5.TIMEFRAME_H4)

    def get_historical_data(self,
                            symbol: str,
                            timeframe_or_str: Any,
                            bars_count: int = 100) -> pd.DataFrame:
        """
        Haal historische prijsdata op met geoptimaliseerde verwerking

        Args:
            symbol: Handelssymbool
            timeframe_or_str: MT5 timeframe constante of string ('H4', etc.)
            bars_count: Aantal bars om op te halen

        Returns:
            pd.DataFrame: DataFrame met historische data
        """
        if not self.connected:
            self.logger.log_info("Niet verbonden met MT5", level="ERROR")
            return pd.DataFrame()

        # Converteer timeframe string naar constante indien nodig
        timeframe = timeframe_or_str
        if isinstance(timeframe_or_str, str):
            timeframe = self.get_timeframe_constant(timeframe_or_str)

        # Probeer data op te halen met retry mechanisme
        retries = 3
        for attempt in range(retries):
            rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars_count)

            if rates is not None and len(rates) > 0:
                break

            if attempt < retries - 1:
                self.logger.log_info(
                    f"Poging {attempt + 1} mislukt om data op te halen voor {symbol}, opnieuw proberen...")
                time.sleep(1)

        if rates is None or len(rates) == 0:
            self.logger.log_info(f"Kon geen historische data ophalen voor {symbol} na {retries} pogingen",
                                 level="ERROR")
            return pd.DataFrame()

        # Converteer naar pandas DataFrame en bereken extra kolommen
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')

        # Hernoem kolommen naar lowercase voor consistentie
        df.columns = [col.lower() for col in df.columns]

        # Rename 'time' kolom naar 'date' voor consistentie in strategie code
        df.rename(columns={'time': 'date'}, inplace=True)

        return df

    def get_symbol_tick(self, symbol: str) -> Optional[Any]:
        """
        Haal actuele tick data op voor een symbool

        Args:
            symbol: Handelssymbool

        Returns:
            mt5.Tick object of None bij fout
        """
        if not self.connected:
            self.logger.log_info("Niet verbonden met MT5", level="ERROR")
            return None

        tick = mt5.symbol_info_tick(symbol)

        if tick is None:
            error_code = mt5.last_error()
            self.logger.log_info(f"Kon geen tick informatie ophalen voor {symbol}. Error: {error_code}", level="ERROR")
            return None

        return tick

    def get_open_positions(self, symbol: Optional[str] = None) -> List[Any]:
        """
        Haal open posities op

        Args:
            symbol: Optioneel filter op symbool

        Returns:
            Lijst met open posities
        """
        if not self.connected:
            self.logger.log_info("Niet verbonden met MT5", level="ERROR")
            return []

        positions = []

        if symbol:
            positions = mt5.positions_get(symbol=symbol)
        else:
            positions = mt5.positions_get()

        if positions is None:
            error_code = mt5.last_error()
            # Als er geen posities zijn is dit geen error
            if error_code == 0:
                return []
            self.logger.log_info(f"Kon geen posities ophalen. Error: {error_code}", level="ERROR")
            return []

        return list(positions)

    def place_order(self,
                    action: str,
                    symbol: str,
                    volume: float,
                    stop_loss: float = 0,
                    take_profit: float = 0,
                    comment: str = "") -> Optional[int]:
        """
        Plaats een order op het MT5 platform

        Args:
            action: "BUY" of "SELL"
            symbol: Handelssymbool
            volume: Order volume in lots
            stop_loss: Stop loss prijs (0 = geen stop loss)
            take_profit: Take profit prijs (0 = geen take profit)
            comment: Order commentaar

        Returns:
            Order ticket ID of None bij fout
        """
        if not self.connected:
            self.logger.log_info("Niet verbonden met MT5", level="ERROR")
            return None

        # Haal symbool informatie op
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            self.logger.log_info(f"Kon geen informatie krijgen voor symbool {symbol}", level="ERROR")
            return None

        # Controleer of trading mogelijk is voor dit symbool
        if not symbol_info.visible or not symbol_info.trade_allowed:
            self.logger.log_info(f"Trading niet toegestaan voor {symbol}", level="ERROR")
            return None

        # Haal huidige prijs op
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            self.logger.log_info(f"Kon geen tick informatie ophalen voor {symbol}", level="ERROR")
            return None

        # Bepaal order type en prijs
        order_type = None
        price = None

        if action == "BUY":
            order_type = mt5.ORDER_TYPE_BUY
            price = tick.ask
        elif action == "SELL":
            order_type = mt5.ORDER_TYPE_SELL
            price = tick.bid
        else:
            self.logger.log_info(f"Ongeldige actie: {action}", level="ERROR")
            return None

        # Bereid order request voor
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": float(volume),
            "type": order_type,
            "price": price,
            "sl": float(stop_loss) if stop_loss > 0 else 0,
            "tp": float(take_profit) if take_profit > 0 else 0,
            "deviation": 10,  # prijsafwijking in punten
            "magic": 123456,  # magic number voor identificatie
            "comment": comment,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK
        }

        # Stuur order naar MT5
        self.logger.log_info(
            f"Order versturen: {action} {volume} {symbol} @ {price}, SL: {stop_loss}, TP: {take_profit}")
        result = mt5.order_send(request)

        if result is None:
            error_code = mt5.last_error()
            self.logger.log_info(f"Order verzenden mislukt. Error code: {error_code}", level="ERROR")
            return None

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            self.logger.log_info(f"Order mislukt. Retcode: {result.retcode}", level="ERROR")
            return None

        self.logger.log_info(f"Order succesvol geplaatst. Ticket: {result.order}")
        return result.order
```

-----------

Path: src/ftmo/__init__.py

```python
```

-----------

Path: src/ftmo/ftmo_helper.py

```python
import logging
import os
from typing import Dict

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class FTMOHelper:
    """Helper class for FTMO compliance checks and reporting"""

    def __init__(self, log_file: str, output_dir: str = 'data/ftmo_analysis'):
        self.log_file = log_file
        self.output_dir = output_dir

        os.makedirs(output_dir, exist_ok=True)

        # Configure visualization style
        plt.style.use('ggplot')
        plt.rcParams['figure.figsize'] = (16, 10)
        sns.set_style("whitegrid")

        # Logging setup
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        # FTMO rules
        self.ftmo_rules = {
            'profit_target': 0.10,
            'max_daily_loss': -0.05,  # Corrected sign
            'max_total_loss': -0.10,  # Corrected sign
            'min_trading_days': 4,
            'challenge_duration': 30,
            'verification_duration': 60
        }

    def load_trade_data(self) -> pd.DataFrame:
        """Load trading data from log file"""
        try:
            df = pd.read_csv(self.log_file)
            df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
            df['Date'] = df['Timestamp'].dt.date
            return df.dropna(subset=['Timestamp'])  # Verwijder rijen met foutieve timestamps
        except Exception as e:
            logging.error(f"Error loading trading data: {e}")
            return pd.DataFrame()

    def check_ftmo_compliance(self, initial_balance: float) -> Dict:
        """Check FTMO compliance with detailed analysis"""
        df = self.load_trade_data()
        if df.empty:
            return {'compliant': False, 'reason': 'No trading data available', 'details': {}}

        # Extract STATUS entries for balance tracking
        status_df = df[df['Type'] == 'STATUS'].copy()
        if status_df.empty:
            return {'compliant': False, 'reason': 'No account status data available', 'details': {}}

        # Convert balance to numeric
        status_df['Balance'] = pd.to_numeric(status_df['Balance'], errors='coerce')
        status_df.dropna(subset=['Balance'], inplace=True)

        # Compute daily balance statistics
        daily_status = status_df.groupby('Date').agg(
            min_balance=('Balance', 'min'),
            max_balance=('Balance', 'max'),
            close_balance=('Balance', 'last')
        ).reset_index()

        # Ensure we have data before proceeding
        if daily_status.empty:
            return {'compliant': False, 'reason': 'Insufficient balance data available', 'details': {}}

        # Calculate daily P&L and drawdowns
        daily_status['prev_close'] = daily_status['close_balance'].shift(1).fillna(initial_balance)
        daily_status['daily_pnl'] = daily_status['close_balance'] - daily_status['prev_close']
        daily_status['daily_pnl_pct'] = (daily_status['daily_pnl'] / daily_status['prev_close']) * 100
        daily_status['daily_drawdown'] = ((daily_status['min_balance'] - daily_status['prev_close'])
                                          / daily_status['prev_close']) * 100
        daily_status['peak'] = daily_status['close_balance'].cummax()
        daily_status['drawdown_from_peak'] = ((daily_status['close_balance'] - daily_status['peak'])
                                              / daily_status['peak']) * 100

        # Calculate key metrics
        max_drawdown = daily_status['drawdown_from_peak'].min()
        latest_balance = daily_status['close_balance'].iloc[-1]
        total_pnl = latest_balance - initial_balance
        total_pnl_pct = (total_pnl / initial_balance) * 100

        # Check trading days
        trade_df = df[df['Type'] == 'TRADE']
        unique_trading_days = trade_df['Date'].nunique()

        # Check FTMO rules compliance
        profit_target_met = total_pnl_pct >= self.ftmo_rules['profit_target'] * 100
        daily_loss_compliant = daily_status['daily_drawdown'].min() >= self.ftmo_rules['max_daily_loss'] * 100
        total_loss_compliant = max_drawdown >= self.ftmo_rules['max_total_loss'] * 100
        trading_days_compliant = unique_trading_days >= self.ftmo_rules['min_trading_days']

        compliant = profit_target_met and daily_loss_compliant and total_loss_compliant and trading_days_compliant

        # Generate reason for non-compliance if applicable
        reasons = []
        if not profit_target_met:
            reasons.append(f"Profit target not reached: {total_pnl_pct:.2f}% "
                           f"(target: {self.ftmo_rules['profit_target'] * 100}%)")
        if not daily_loss_compliant:
            worst_day_idx = daily_status['daily_drawdown'].idxmin()
            worst_day = daily_status.iloc[worst_day_idx]
            reasons.append(f"Daily loss limit exceeded: {worst_day['daily_drawdown']:.2f}% on {worst_day['Date']}")
        if not total_loss_compliant:
            reasons.append(f"Maximum drawdown exceeded: {max_drawdown:.2f}% "
                           f"(limit: {self.ftmo_rules['max_total_loss'] * 100}%)")
        if not trading_days_compliant:
            reasons.append(f"Insufficient trading days: {unique_trading_days} "
                           f"(minimum: {self.ftmo_rules['min_trading_days']})")

        reason = "; ".join(reasons) if reasons else "Complies with all FTMO rules"

        # Compile results
        details = {
            'initial_balance': initial_balance,
            'final_balance': latest_balance,
            'total_pnl': total_pnl,
            'total_pnl_pct': total_pnl_pct,
            'max_drawdown': max_drawdown,
            'trading_days': unique_trading_days,
            'daily_stats': daily_status.to_dict(orient='records')  # Converted for better JSON compatibility
        }

        return {
            'compliant': compliant,
            'reason': reason,
            'details': details
        }

    def generate_trading_report(self, initial_balance: float) -> bool:
        """Generate detailed FTMO trading report with visualizations"""
        try:
            results = self.check_ftmo_compliance(initial_balance)
            daily_status = pd.DataFrame(results['details'].get('daily_stats', []))

            if daily_status.empty:
                logging.warning("No data available for generating trading report.")
                return False

            # Plot balance over time
            plt.figure(figsize=(12, 6))
            plt.plot(daily_status['Date'], daily_status['close_balance'], marker='o', label='Balance')
            plt.fill_between(daily_status['Date'], daily_status['min_balance'], daily_status['max_balance'],
                             alpha=0.3, color='gray', label="Daily Range")
            plt.axhline(y=initial_balance, color='r', linestyle='--', label="Initial Balance")
            plt.title("Trading Balance Over Time")
            plt.xlabel("Date")
            plt.ylabel("Balance")
            plt.legend()
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Save the figure
            report_path = os.path.join(self.output_dir, "trading_report.png")
            plt.savefig(report_path)
            logging.info(f"Trading report saved at {report_path}")

            return True
        except Exception as e:
            logging.error(f"Error generating trading report: {e}")
            return False
```

-----------

Path: src/ftmo/ftmo_validator.py

```python
# src/ftmo/ftmo_validator.py

import os
import re
from datetime import datetime, date
from typing import Dict, Tuple, Optional, Any

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.utils.logger import Logger  # Importeer de Logger-klasse


class FTMOValidator:
    """Klasse om handelsactiviteit te valideren en analyseren volgens FTMO-regels."""

    def __init__(self, config: Dict[str, Any], log_file: str, output_dir: str = 'data/ftmo_analysis',
                 logger: Optional[Logger] = None) -> None:
        """
        Initialiseer de FTMO Validator met configuratie, logbestand en outputmap.

        Parameters:
        -----------
        config : Dict[str, Any]
            Configuratiedictionary met risicoparameters (bijv. initial_balance).
        log_file : str
            Pad naar het logbestand met handelsdata.
        output_dir : str, optional
            Map voor het opslaan van analyse-uitvoer (default: 'data/ftmo_analysis').
        logger : Logger, optional
            Logging-object voor het bijhouden van gebeurtenissen.
        """
        self.config = config
        self.logger = logger
        self.initial_balance = config['risk'].get('account_balance', 100000)
        # Haal startdatum uit config of bepaal uit logbestand
        self.start_date = datetime.strptime(config.get('ftmo', {}).get('start_date', date.today().strftime('%Y-%m-%d')),
                                            '%Y-%m-%d').date()
        self.trade_days = set()
        self.log_file = log_file
        self.output_dir = output_dir

        # Stel visualisatiestijl in
        plt.style.use('ggplot')
        plt.rcParams['figure.figsize'] = (16, 10)
        plt.rcParams['lines.linewidth'] = 1.5
        sns.set_style("whitegrid")

        # Maak outputmap aan als deze niet bestaat
        os.makedirs(output_dir, exist_ok=True)

        # FTMO-regels
        self.ftmo_rules = {
            'profit_target': 0.10,  # 10% winstdoel
            'max_daily_loss': 0.05,  # 5% maximale dagelijkse drawdown
            'max_total_loss': 0.10,  # 10% maximale totale drawdown
            'min_trading_days': 4,  # Minimaal 4 handelsdagen
            'challenge_duration': 30,  # Challenge-duur van 30 dagen
            'verification_duration': 60  # Verificatie-duur van 60 dagen
        }

    def load_trade_data(self) -> pd.DataFrame:
        """
        Laad handelsdata uit het logbestand.

        Returns:
        --------
        pandas.DataFrame
            DataFrame met handelsdata, of lege DataFrame bij fout.

        Raises:
        -------
        ValueError
            Als het logbestand ongeldig is.
        """
        try:
            if not os.path.exists(self.log_file):
                raise ValueError(f"Logbestand niet gevonden: {self.log_file}")
            df = pd.read_csv(self.log_file)
            if df.empty or 'Timestamp' not in df.columns:
                raise ValueError("Logbestand is leeg of ongeldig formaat")
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            df['Date'] = df['Timestamp'].dt.date
            if self.logger:
                self.logger.log_info(f"Handelsdata geladen uit {self.log_file}")
            return df
        except Exception as e:
            if self.logger:
                self.logger.log_info(f"Fout bij laden handelsdata: {e}", level="ERROR")
            return pd.DataFrame()

    def validate_account_state(self, account_info: Dict[str, float] = None) -> Tuple[bool, Optional[str]]:
        """
        Valideer de accountstatus volgens FTMO-regels.

        Args:
            account_info: Huidige accountinformatie (optioneel).

        Returns:
            Tuple[bool, Optional[str]]: (is_compliant, violation_reason).
        """
        df = self.load_trade_data()
        if df.empty:
            return False, "Geen handelsdata beschikbaar"

        status_df = df[df['Type'] == 'STATUS'].copy()
        if status_df.empty:
            return False, "Geen statusdata beschikbaar"

        # Extraheer balans
        if 'Balance' not in status_df.columns or status_df['Balance'].isna().all():
            def extract_balance(comment):
                if isinstance(comment, str) and 'Balance: ' in comment:
                    match = re.search(r'Balance:\s*([\d,.]+)', comment)
                    return float(match.group(1).replace(',', '')) if match else None
                return None

            status_df['Balance'] = status_df['Comment'].apply(extract_balance)

        if status_df['Balance'].isna().all():
            return False, "Geen balansdata beschikbaar"

        status_df['Balance'] = pd.to_numeric(status_df['Balance'], errors='coerce')
        daily_status = status_df.groupby('Date').agg(close_balance=('Balance', 'last')).reset_index()
        current_equity = daily_status['close_balance'].iloc[-1] if not daily_status.empty else self.initial_balance

        # Registreer handelsdag
        self.trade_days.update(df[df['Type'] == 'TRADE']['Date'].unique())

        # Bereken winst/verlies percentage
        profit_loss_pct = (current_equity - self.initial_balance) / self.initial_balance * 100

        # Controleer FTMO-regels
        if profit_loss_pct >= self.ftmo_rules['profit_target'] * 100:
            return True, "Winstdoel bereikt"

        if profit_loss_pct <= -self.ftmo_rules['max_daily_loss'] * 100:
            return False, "Dagelijkse verlieslimiet overschreden"

        if profit_loss_pct <= -self.ftmo_rules['max_total_loss'] * 100:
            return False, "Maximale drawdown overschreden"

        days_in_challenge = (date.today() - self.start_date).days
        if days_in_challenge >= self.ftmo_rules['challenge_duration'] - 2:
            unique_trading_days = len(self.trade_days)
            if unique_trading_days < self.ftmo_rules['min_trading_days']:
                return False, f"Onvoldoende handelsdagen: {unique_trading_days} (minimaal: {self.ftmo_rules['min_trading_days']})"

        return True, None

    def check_ftmo_compliance(self, initial_balance: float = None) -> Dict:
        """
        Controleer FTMO-naleving met gedetailleerde analyse van handelsdata.

        Parameters:
        -----------
        initial_balance : float, optional
            Initiële accountbalans (default vanuit config).

        Returns:
        --------
        Dict
            Resultaten van naleving met details.
        """
        initial_balance = initial_balance if initial_balance is not None else self.initial_balance
        df = self.load_trade_data()
        if df.empty:
            return {'compliant': False, 'reason': 'Geen handelsdata beschikbaar', 'details': {}}

        status_df = df[df['Type'] == 'STATUS'].copy()
        if status_df.empty:
            return {'compliant': False, 'reason': 'Geen statusdata beschikbaar', 'details': {}}

        # Extraheer balans
        if 'Balance' not in status_df.columns or status_df['Balance'].isna().all():
            def extract_balance(comment):
                if isinstance(comment, str) and 'Balance: ' in comment:
                    match = re.search(r'Balance:\s*([\d,.]+)', comment)
                    return float(match.group(1).replace(',', '')) if match else None
                return None

            status_df['Balance'] = status_df['Comment'].apply(extract_balance)

        if status_df['Balance'].isna().all():
            return {'compliant': False, 'reason': 'Geen balansdata beschikbaar', 'details': {}}

        status_df['Balance'] = pd.to_numeric(status_df['Balance'], errors='coerce')
        daily_status = status_df.groupby('Date').agg(
            min_balance=('Balance', 'min'),
            max_balance=('Balance', 'max'),
            close_balance=('Balance', 'last')
        ).reset_index()

        daily_status['prev_close'] = daily_status['close_balance'].shift(1).fillna(initial_balance)
        daily_status['daily_pnl'] = daily_status['close_balance'] - daily_status['prev_close']
        daily_status['daily_pnl_pct'] = (daily_status['daily_pnl'] / daily_status['prev_close']) * 100
        daily_status['daily_drawdown'] = (daily_status['min_balance'] - daily_status['prev_close']) / daily_status[
            'prev_close'] * 100
        daily_status['peak'] = daily_status['close_balance'].cummax()
        daily_status['drawdown_from_peak'] = (daily_status['close_balance'] - daily_status['peak']) / daily_status[
            'peak'] * 100
        max_drawdown = daily_status['drawdown_from_peak'].min()

        latest_balance = daily_status['close_balance'].iloc[-1]
        total_pnl = latest_balance - initial_balance
        total_pnl_pct = (total_pnl / initial_balance) * 100

        trade_df = df[df['Type'] == 'TRADE']
        unique_trading_days = trade_df['Date'].nunique()

        profit_target_met = total_pnl_pct >= self.ftmo_rules['profit_target'] * 100
        daily_loss_compliant = daily_status['daily_drawdown'].min() > -self.ftmo_rules['max_daily_loss'] * 100
        total_loss_compliant = max_drawdown > -self.ftmo_rules['max_total_loss'] * 100
        trading_days_compliant = unique_trading_days >= self.ftmo_rules['min_trading_days']
        compliant = profit_target_met and daily_loss_compliant and total_loss_compliant and trading_days_compliant

        reasons = []
        if not profit_target_met:
            reasons.append(
                f"Winstdoel niet bereikt: {total_pnl_pct:.2f}% (doel: {self.ftmo_rules['profit_target'] * 100}%)")
        if not daily_loss_compliant:
            worst_day_idx = daily_status['daily_drawdown'].idxmin()
            worst_day = daily_status.iloc[worst_day_idx]
            reasons.append(
                f"Dagelijkse verlieslimiet overschreden: {worst_day['daily_drawdown']:.2f}% op {worst_day['Date']}")
        if not total_loss_compliant:
            reasons.append(
                f"Maximale drawdown overschreden: {max_drawdown:.2f}% (limiet: -{self.ftmo_rules['max_total_loss'] * 100}%)")
        if not trading_days_compliant:
            reasons.append(
                f"Onvoldoende handelsdagen: {unique_trading_days} (minimaal: {self.ftmo_rules['min_trading_days']})")

        reason = "; ".join(reasons) if reasons else "Voldoet aan alle FTMO-regels"

        details = {
            'initial_balance': initial_balance,
            'final_balance': latest_balance,
            'total_pnl': total_pnl,
            'total_pnl_pct': total_pnl_pct,
            'max_drawdown': max_drawdown,
            'trading_days': unique_trading_days,
            'daily_stats': daily_status
        }

        return {'compliant': compliant, 'reason': reason, 'details': details}

    def plot_ftmo_compliance(self, initial_balance: float = None) -> Optional[str]:
        """
        Maak een visualisatie van FTMO-naleving met extra analyses.

        Parameters:
        -----------
        initial_balance : float, optional
            Initiële accountbalans (default vanuit config).

        Returns:
        --------
        str
            Pad naar opgeslagen grafiek, of None bij mislukking.
        """
        initial_balance = initial_balance if initial_balance is not None else self.initial_balance
        compliance = self.check_ftmo_compliance(initial_balance)
        if not compliance['details']:
            if self.logger:
                self.logger.log_info("Onvoldoende data voor FTMO-analyse", level="ERROR")
            return None

        daily_stats = compliance['details']['daily_stats']
        fig = plt.figure(figsize=(16, 16))
        gs = fig.add_gridspec(5, 2, height_ratios=[2, 1, 1, 1, 1])

        # 1. Balansgrafiek
        ax1 = fig.add_subplot(gs[0, :])
        ax1.plot(daily_stats['Date'], daily_stats['close_balance'], 'b-', label='Accountbalans')
        ax1.axhline(y=initial_balance, color='gray', linestyle=':', label='Initiële balans')
        ax1.axhline(y=initial_balance * 1.10, color='green', linestyle='--',
                    label=f"+10% Doel (${initial_balance * 1.10:,.2f})")
        ax1.axhline(y=initial_balance * 0.95, color='orange', linestyle='--',
                    label=f"-5% Daglimiet (${initial_balance * 0.95:,.2f})")
        ax1.axhline(y=initial_balance * 0.90, color='red', linestyle='--',
                    label=f"-10% Max Drawdown (${initial_balance * 0.90:,.2f})")
        ax1.set_title('FTMO Accountbalans Progressie', fontsize=16)
        ax1.set_ylabel('Balans ($)', fontsize=14)
        ax1.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
        ax1.legend(loc='best', fontsize=12)
        ax1.grid(True)

        # 2. Dagelijkse P&L
        ax2 = fig.add_subplot(gs[1, 0])
        colors = ['green' if x >= 0 else 'red' for x in daily_stats['daily_pnl']]
        ax2.bar(daily_stats['Date'], daily_stats['daily_pnl'], color=colors, alpha=0.7)
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax2.set_title('Dagelijkse P&L ($)', fontsize=14)
        ax2.set_ylabel('P&L ($)', fontsize=12)
        ax2.grid(True, axis='y')

        # 3. Dagelijkse drawdown
        ax3 = fig.add_subplot(gs[1, 1])
        ax3.fill_between(daily_stats['Date'], daily_stats['daily_drawdown'], 0,
                         where=(daily_stats['daily_drawdown'] < 0), color='red', alpha=0.3)
        ax3.plot(daily_stats['Date'], daily_stats['daily_drawdown'], 'r-', alpha=0.7)
        ax3.axhline(y=-5, color='orange', linestyle='--', label='-5% Daglimiet')
        ax3.set_title('Dagelijkse Drawdown (%)', fontsize=14)
        ax3.set_ylabel('Drawdown (%)', fontsize=12)
        ax3.set_ylim(max(-15, daily_stats['daily_drawdown'].min() * 1.2), 5)
        ax3.legend(loc='lower right', fontsize=10)
        ax3.grid(True)

        # 4. Cumulatieve drawdown vanaf piek
        ax4 = fig.add_subplot(gs[2, :])
        ax4.fill_between(daily_stats['Date'], daily_stats['drawdown_from_peak'], 0, color='purple', alpha=0.3)
        ax4.plot(daily_stats['Date'], daily_stats['drawdown_from_peak'], 'purple', alpha=0.7)
        ax4.axhline(y=-10, color='red', linestyle='--', label='-10% Max Drawdown')
        ax4.set_title('Maximale Drawdown vanaf Piek (%)', fontsize=14)
        ax4.set_ylabel('Drawdown (%)', fontsize=12)
        ax4.set_ylim(max(-12, daily_stats['drawdown_from_peak'].min() * 1.2), 2)
        ax4.legend(loc='lower right', fontsize=10)
        ax4.grid(True)

        # 5. Win/Loss Ratio
        trade_df = self.load_trade_data()[self.load_trade_data()['Type'] == 'TRADE']
        if not trade_df.empty:
            profits = \
            trade_df[trade_df['Action'].isin(['SELL', 'BUY']) & (trade_df['Price'].shift(-1) - trade_df['Price'] > 0)][
                'Price'].count()
            losses = \
            trade_df[trade_df['Action'].isin(['SELL', 'BUY']) & (trade_df['Price'].shift(-1) - trade_df['Price'] < 0)][
                'Price'].count()
            win_loss_ratio = profits / losses if losses > 0 else float('inf')
            ax5 = fig.add_subplot(gs[3, :])
            ax5.bar(['Wins', 'Losses'], [profits, losses], color=['green', 'red'])
            ax5.set_title('Win/Loss Ratio', fontsize=14)
            ax5.set_ylabel('Aantal Trades', fontsize=12)
            ax5.text(0.5, -0.1, f"Win/Loss Ratio: {win_loss_ratio:.2f}", transform=ax5.transAxes, ha='center')
            ax5.grid(True, axis='y')

        # 6. Nalevingstabel
        ax6 = fig.add_subplot(gs[4, :])
        ax6.axis('off')
        compliance_data = [
            ['Metriek', 'Waarde', 'Vereiste', 'Status'],
            ['Totale P&L', f"{compliance['details']['total_pnl_pct']:.2f}%",
             f"≥ {self.ftmo_rules['profit_target'] * 100}%",
             '✅' if compliance['details']['total_pnl_pct'] >= 10 else '❌'],
            ['Max Dagelijkse Drawdown', f"{daily_stats['daily_drawdown'].min():.2f}%",
             f"> -{self.ftmo_rules['max_daily_loss'] * 100}%",
             '✅' if daily_stats['daily_drawdown'].min() > -5 else '❌'],
            ['Max Totale Drawdown', f"{compliance['details']['max_drawdown']:.2f}%",
             f"> -{self.ftmo_rules['max_total_loss'] * 100}%",
             '✅' if compliance['details']['max_drawdown'] > -10 else '❌'],
            ['Handelsdagen', f"{compliance['details']['trading_days']}",
             f"≥ {self.ftmo_rules['min_trading_days']}",
             '✅' if compliance['details']['trading_days'] >= 4 else '❌']
        ]
        tbl = ax6.table(cellText=compliance_data, loc='center', cellLoc='center', colWidths=[0.25, 0.25, 0.25, 0.15])
        tbl.auto_set_font_size(False)
        tbl.set_fontsize(14)
        tbl.scale(1, 2)

        header_color = '#40466e'
        pass_color = '#d8f3dc'
        fail_color = '#ffcccb'
        for (i, j), cell in tbl.get_celld().items():
            if i == 0:
                cell.set_facecolor(header_color)
                cell.set_text_props(color='white', fontweight='bold')
            elif j == 3:
                cell.set_facecolor(pass_color if compliance_data[i][3] == '✅' else fail_color)

        overall_status = 'GESLAAGD' if compliance['compliant'] else 'GEFAALD'
        status_color = 'green' if compliance['compliant'] else 'red'
        ax6.set_title(f"FTMO Naleving: {overall_status}", fontsize=18, color=status_color, fontweight='bold')
        if not compliance['compliant']:
            ax6.text(0.5, 0.1, compliance['reason'], horizontalalignment='center', fontsize=12, color='red',
                     transform=ax6.transAxes)

        plt.tight_layout()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"ftmo_compliance_{timestamp}.png")
        plt.savefig(output_path, dpi=150)
        plt.close()
        if self.logger:
            self.logger.log_info(f"FTMO nalevingsgrafiek opgeslagen als {output_path}")
        return output_path

    def generate_trading_report(self, initial_balance: float = None) -> bool:
        """
        Genereer een gedetailleerd FTMO handelsrapport met extra metrics.

        Parameters:
        -----------
        initial_balance : float, optional
            Initiële accountbalans (default vanuit config).

        Returns:
        --------
        bool
            True als rapport succesvol gegenereerd.
        """
        initial_balance = initial_balance if initial_balance is not None else self.initial_balance
        try:
            compliance = self.check_ftmo_compliance(initial_balance)
            if not compliance['details']:
                if self.logger:
                    self.logger.log_info("Onvoldoende data voor rapportgeneratie", level="ERROR")
                return False

            compliance_path = self.plot_ftmo_compliance(initial_balance)
            df = self.load_trade_data()
            trade_df = df[df['Type'] == 'TRADE'].copy()

            # Instrumentanalyse
            symbol_stats = {}
            for symbol in trade_df['Symbol'].unique():
                symbol_df = trade_df[trade_df['Symbol'] == symbol]
                wins = len(symbol_df[symbol_df['Action'].isin(['SELL', 'BUY']) & (
                            symbol_df['Price'].shift(-1) - symbol_df['Price'] > 0)])
                losses = len(symbol_df[symbol_df['Action'].isin(['SELL', 'BUY']) & (
                            symbol_df['Price'].shift(-1) - symbol_df['Price'] < 0)])
                symbol_stats[symbol] = {
                    'total_trades': len(symbol_df),
                    'wins': wins,
                    'losses': losses,
                    'win_rate': (wins / (wins + losses) * 100) if (wins + losses) > 0 else 0,
                    'days_traded': symbol_df['Date'].nunique()
                }

            # Rapportweergave
            report = "\n===== FTMO Handelsrapport =====\n"
            report += f"Periode: {df['Timestamp'].min().date() if not df.empty else 'N/A'} tot {df['Timestamp'].max().date() if not df.empty else 'N/A'}\n"
            report += f"Initiële balans: ${initial_balance:,.2f}\n"
            report += f"Eindebalans: ${compliance['details']['final_balance']:,.2f}\n"
            report += f"Totale P&L: ${compliance['details']['total_pnl']:,.2f} ({compliance['details']['total_pnl_pct']:.2f}%)\n"
            report += f"Maximale drawdown: {compliance['details']['max_drawdown']:.2f}%\n"
            report += f"Aantal handelsdagen: {compliance['details']['trading_days']}\n"
            report += "\nInstrumentanalyse:\n"
            for symbol, stats in symbol_stats.items():
                report += f"  {symbol}: {stats['total_trades']} trades ({stats['wins']} wins, {stats['losses']} losses, Win Rate: {stats['win_rate']:.2f}%) over {stats['days_traded']} dagen\n"
            report += f"\nFTMO Naleving: {'GESLAAGD' if compliance['compliant'] else 'GEFAALD'}\n"
            if not compliance['compliant']:
                report += f"Reden: {compliance['reason']}\n"
            if compliance_path:
                report += f"\nNalevingsvisualisatie opgeslagen als: {os.path.basename(compliance_path)}\n"

            # Extra metrics
            total_trades = len(trade_df)
            avg_trade_size = trade_df['Volume'].mean() if not trade_df.empty else 0
            report += f"\nExtra Metrics:\n"
            report += f"  Totaal aantal trades: {total_trades}\n"
            report += f"  Gemiddelde trade grootte: {avg_trade_size:.2f} lots\n"

            print(report)

            if self.logger:
                self.logger.log_info(f"FTMO Rapport gegenereerd - Compliant: {compliance['compliant']}")
                if not compliance['compliant']:
                    self.logger.log_info(f"Reden voor niet-naleving: {compliance['reason']}")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = os.path.join(self.output_dir, f"ftmo_report_{timestamp}.txt")
            with open(report_path, 'w') as f:
                f.write(report)

            return True
        except Exception as e:
            if self.logger:
                self.logger.log_info(f"Fout bij rapportgeneratie: {e}", level="ERROR")
            return False
```

-----------

Path: src/monitoring/__init__.py

```python
```

-----------

Path: src/presentation/__init__.py

```python
```

-----------

Path: src/presentation/dashboard.py

```python
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
```

-----------

Path: src/risk/__init__.py

```python
```

-----------

Path: src/risk/position_sizer.py

```python
def calculate_position_size(
        entry_price: float,
        stop_loss: float,
        account_balance: float,
        risk_percentage: float,
        pip_value: float,
        min_lot: float = 0.01,
        max_lot: float = 10.0
) -> float:
    """
    Calculate optimal position size based on risk parameters

    Args:
        entry_price: Entry price for the position
        stop_loss: Stop loss price
        account_balance: Current account balance
        risk_percentage: Percentage of account to risk (0.01 = 1%)
        pip_value: Value of one pip in account currency
        min_lot: Minimum allowable lot size
        max_lot: Maximum allowable lot size

    Returns:
        Calculated position size in lots
    """
    if entry_price == stop_loss:
        return min_lot  # Avoid division by zero

    # Calculate risk amount in account currency
    risk_amount = account_balance * risk_percentage

    # Calculate pips at risk
    pips_at_risk = abs(entry_price - stop_loss) / 0.0001  # For 4-digit forex pairs

    # Calculate lot size
    lot_size = risk_amount / (pips_at_risk * pip_value)

    # Enforce limits
    lot_size = max(min_lot, min(lot_size, max_lot))

    # Round to 2 decimal places
    lot_size = round(lot_size, 2)

    return lot_size
```

-----------

Path: src/risk/risk_manager.py

```python
# src/risk/risk_manager.py
from datetime import date
from typing import Dict, Optional, Tuple


class RiskManager:
    """
    Risicomanagement met FTMO compliance checks.

    Verantwoordelijk voor het bewaken van risicoparameters zoals dagelijkse verlieslimiet,
    maximale drawdown, en positiegrootte berekeningen volgens risicoregels.
    """

    def __init__(self, config: Dict, logger):
        """Initialiseer met configuratieparameters"""
        self.config = config
        self.logger = logger

        # Extraheer risicoparameters
        self.max_risk_per_trade = self.config.get('max_risk_per_trade', 0.01)
        self.max_daily_drawdown = self.config.get('max_daily_drawdown', 0.05)
        self.max_total_drawdown = self.config.get('max_total_drawdown', 0.10)
        self.leverage = self.config.get('leverage', 30)

        # Initialiseer tracking variabelen
        self.daily_losses = 0
        self.current_date = date.today()
        self.initial_balance = self.config.get('account_balance', 100000)
        self.daily_trades_count = 0
        self.max_daily_trades = self.config.get('max_daily_trades', 10)

        self.logger.log_info(f"RiskManager geïnitialiseerd met max risk per trade: {self.max_risk_per_trade * 100}%, "
                             f"max daily drawdown: {self.max_daily_drawdown * 100}%, "
                             f"max total drawdown: {self.max_total_drawdown * 100}%, "
                             f"leverage: {self.leverage}")

    def check_ftmo_limits(self, account_info: Dict) -> Tuple[bool, Optional[str]]:
        """
        Controleer of huidige accountstatus voldoet aan FTMO-limieten

        Parameters:
        -----------
        account_info : Dict
            Dictionary met huidige accountinformatie

        Returns:
        --------
        Tuple van (stop_trading, reason)
        - stop_trading: True als trading gestopt moet worden
        - reason: Beschrijving waarom trading moet stoppen, of None
        """
        # Reset dagelijkse variabelen als het een nieuwe dag is
        today = date.today()
        if today != self.current_date:
            self.daily_losses = 0
            self.daily_trades_count = 0
            self.current_date = today
            self.logger.log_info("Dagelijkse risico limieten gereset (nieuwe handelsdag)")

        # Haal account data op
        current_balance = account_info.get('balance', 0)
        current_equity = account_info.get('equity', 0)

        # Bereken winst/verlies percentages
        balance_change_pct = (current_balance - self.initial_balance) / self.initial_balance
        equity_change_pct = (current_equity - self.initial_balance) / self.initial_balance

        # Controleer of winstdoel is bereikt (10%)
        if balance_change_pct >= 0.10:
            return True, f"Winstdoel bereikt: {balance_change_pct:.2%}"

        # Controleer dagelijkse verlieslimiet (5%)
        if equity_change_pct <= -self.max_daily_drawdown:
            return True, f"Dagelijkse verlieslimiet bereikt: {equity_change_pct:.2%}"

        # Controleer totale verlieslimiet (10%)
        if equity_change_pct <= -self.max_total_drawdown:
            return True, f"Maximale drawdown bereikt: {equity_change_pct:.2%}"

        # Alles is binnen limieten
        return False, None

    def calculate_position_size(self,
                                symbol: str,
                                entry_price: float,
                                stop_loss: float,
                                account_balance: float,
                                trend_strength: float = 0.5) -> float:
        """
        Bereken optimale positiegrootte gebaseerd op risicoparameters

        Parameters:
        -----------
        symbol : str
            Trading symbool
        entry_price : float
            Ingangsprijs voor de positie
        stop_loss : float
            Stop loss prijs
        account_balance : float
            Huidige account balans
        trend_strength : float
            Sterkte van de trend (0-1), gebruikt voor positiegrootte aanpassing

        Returns:
        --------
        float : Berekende positiegrootte in lots
        """
        if entry_price == 0 or stop_loss == 0:
            self.logger.log_info(f"Ongeldige entry of stop loss voor {symbol}", level="ERROR")
            return 0.01

        # Voorkom delen door nul
        if entry_price == stop_loss:
            self.logger.log_info(f"Entry gelijk aan stop loss voor {symbol}", level="WARNING")
            return 0.01

        # Bereken risicobedrag in accountvaluta
        risk_amount = account_balance * self.max_risk_per_trade

        # Pas risico aan op basis van trendsterkte
        adjusted_risk = risk_amount * (0.5 + trend_strength / 2)  # 50-100% van normaal risico

        # Bereken pips op risico
        pips_at_risk = abs(entry_price - stop_loss) / 0.0001  # Voor 4-cijferige forex paren

        # Pas aan voor goud en indices indien nodig
        if symbol == "XAUUSD":
            pips_at_risk = abs(entry_price - stop_loss) / 0.01  # Voor goud (0.01 = 1 pip)
        elif symbol in ["US30", "US30.cash", "US500", "USTEC"]:
            pips_at_risk = abs(entry_price - stop_loss) / 0.1  # Voor indices

        # Schat pip waarde (kan worden verbeterd met exacte berekening per symbool)
        pip_value = 10.0  # Standaard pip waarde voor 1 lot

        # Bereken lot size
        lot_size = adjusted_risk / (pips_at_risk * pip_value)

        # Rond af naar 2 decimalen en begrens tussen min/max waarden
        min_lot = 0.01
        max_lot = 10.0
        lot_size = max(min_lot, min(lot_size, max_lot))
        lot_size = round(lot_size, 2)

        self.logger.log_info(f"Berekende positiegrootte voor {symbol}: {lot_size} lots "
                             f"(Risk: ${adjusted_risk:.2f}, Pips: {pips_at_risk:.1f})")

        return lot_size

    def check_trade_risk(self,
                         symbol: str,
                         volume: float,
                         entry_price: float,
                         stop_loss: float) -> bool:
        """
        Controleer of een trade binnen de risicolimieten valt

        Parameters:
        -----------
        symbol : str
            Trading symbool
        volume : float
            Positiegrootte in lots
        entry_price : float
            Ingangsprijs voor de positie
        stop_loss : float
            Stop loss prijs

        Returns:
        --------
        bool : True als trade binnen risicolimieten valt, anders False
        """
        # Controleer dagelijks aantal trades
        self.daily_trades_count += 1
        if self.daily_trades_count > self.max_daily_trades:
            self.logger.log_info(f"Maximaal aantal dagelijkse trades bereikt: {self.max_daily_trades}", level="WARNING")
            return False

        # Als er geen stop loss is, is dit een hoog risico en accepteren we de trade niet
        if stop_loss == 0:
            self.logger.log_info(f"Trade geweigerd voor {symbol}: Geen stop loss ingesteld", level="WARNING")
            return False

        # Berekening potentieel verlies
        pip_value = 10.0  # Standaard pip waarde voor 1 lot
        pips_at_risk = abs(entry_price - stop_loss) / 0.0001

        # Pas aan voor goud en indices indien nodig
        if symbol == "XAUUSD":
            pips_at_risk = abs(entry_price - stop_loss) / 0.01
        elif symbol in ["US30", "US30.cash", "US500", "USTEC"]:
            pips_at_risk = abs(entry_price - stop_loss) / 0.1

        potential_loss = pips_at_risk * pip_value * volume

        # Controleer tegen dagelijkse verlieslimiet
        max_daily_loss = self.initial_balance * self.max_daily_drawdown
        if self.daily_losses + potential_loss > max_daily_loss:
            self.logger.log_info(f"Trade geweigerd voor {symbol}: Zou dagelijkse verlieslimiet overschrijden",
                                 level="WARNING")
            return False

        # Extra validatie voor extreem grote posities
        if volume > 5.0:  # Voorbeeld van een arbitraire limiet
            self.logger.log_info(f"Trade geweigerd voor {symbol}: Volume te groot ({volume} lots)", level="WARNING")
            return False

        # Trade geaccepteerd
        return True

    def can_trade(self) -> bool:
        """
        Controleert of trading is toegestaan op basis van huidige limieten

        Returns:
        --------
        bool : True als trading is toegestaan, anders False
        """
        # Reset dagelijkse variabelen als het een nieuwe dag is
        today = date.today()
        if today != self.current_date:
            self.daily_losses = 0
            self.daily_trades_count = 0
            self.current_date = today

        # Controleer dagelijks aantal trades
        if self.daily_trades_count >= self.max_daily_trades:
            return False

        return True

    def update_daily_loss(self, loss_amount: float) -> None:
        """
        Update het dagelijkse verliestotaal

        Parameters:
        -----------
        loss_amount : float
            Verliesbedrag (positief voor verlies, negatief voor winst)
        """
        # Reset als het een nieuwe dag is
        today = date.today()
        if today != self.current_date:
            self.daily_losses = 0
            self.daily_trades_count = 0
            self.current_date = today

        # Update dagelijkse verliezen
        if loss_amount > 0:  # Alleen verliesposities bijhouden
            self.daily_losses += loss_amount
            self.logger.log_info(f"Dagelijks verlies bijgewerkt: ${self.daily_losses:.2f} "
                                 f"(Max: ${self.initial_balance * self.max_daily_drawdown:.2f})")
```

-----------

Path: src/strategy/__init__.py

```python
```

-----------

Path: src/strategy/base_strategy.py

```python
# src/strategy/base_strategy.py
from abc import ABC, abstractmethod
from typing import Dict, Any, List


class Strategy(ABC):
    """
    Abstracte basisklasse voor alle handelsstrategieën.

    Deze klasse definieert de interface die alle strategieën moeten implementeren.
    Door deze basisklasse te gebruiken, kunnen we gemakkelijk nieuwe strategieën
    toevoegen zonder de rest van de code aan te hoeven passen.
    """

    def __init__(self, connector, risk_manager, logger, config):
        """
        Initialiseer de strategie met de benodigde componenten

        Parameters:
        -----------
        connector : Connector naar handelsplatform (bijv. MT5)
        risk_manager : Risicobeheer component
        logger : Logging component
        config : Configuratiegegevens voor de strategie
        """
        self.connector = connector
        self.risk_manager = risk_manager
        self.logger = logger
        self.config = config
        self.name = "Base Strategy"

    @abstractmethod
    def process_symbol(self, symbol: str) -> Dict[str, Any]:
        """
        Verwerk een symbool volgens de strategie regels

        Parameters:
        -----------
        symbol : str
            Het te verwerken symbool

        Returns:
        --------
        Dict : Resultaten van de verwerking, inclusief eventuele signalen
        """
        pass

    @abstractmethod
    def calculate_indicators(self, data: Any) -> Dict[str, Any]:
        """
        Bereken de technische indicatoren voor de strategie

        Parameters:
        -----------
        data : Any
            Prijsgegevens en andere input

        Returns:
        --------
        Dict : Berekende indicatoren
        """
        pass

    def get_name(self) -> str:
        """
        Geef de naam van de strategie terug

        Returns:
        --------
        str : Strategienaam
        """
        return self.name

    def get_open_positions(self) -> Dict[str, List]:
        """
        Haal alle open posities op

        Returns:
        --------
        Dict : Dictionary met open posities per symbool
        """
        return {}
```

-----------

Path: src/strategy/dax_opening.py

```python
```

-----------

Path: src/strategy/strategy_factory.py

```python
# src/strategy/strategy_factory.py
import copy
import importlib
import os
from typing import Optional

from src.strategy.base_strategy import Strategy


class StrategyFactory:
    """Factory voor het creëren van trading strategie-instanties"""

    _strategies = {}

    @classmethod
    def _load_strategies(cls):
        """Laad beschikbare strategieën dynamisch uit de strategy directory"""
        if cls._strategies:
            return

        # Zoek naar strategie modules in de src/strategy directory
        strategy_dir = os.path.dirname(os.path.abspath(__file__))
        for filename in os.listdir(strategy_dir):
            if filename.endswith('_strategy.py') and filename != 'base_strategy.py':
                module_name = filename[:-3]  # Verwijder .py

                try:
                    # Import de module
                    module_path = f"src.strategy.{module_name}"
                    module = importlib.import_module(module_path)

                    # Zoek naar classes die Strategy erven
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if isinstance(attr, type) and issubclass(attr, Strategy) and attr is not Strategy:
                            # Registreer de strategie
                            strategy_key = module_name.replace('_strategy', '')
                            cls._strategies[strategy_key] = attr
                except (ImportError, AttributeError) as e:
                    print(f"Kon strategie module {module_name} niet laden: {e}")

        # Voeg de turtle strategie toe als deze niet automatisch geladen is
        if 'turtle' not in cls._strategies:
            try:
                from src.strategy.turtle_strategy import TurtleStrategy
                cls._strategies['turtle'] = TurtleStrategy
            except ImportError:
                pass

    @classmethod
    def create_strategy(
            cls,
            strategy_name: str,
            connector: Optional[object],
            risk_manager: Optional[object],
            logger: Optional[object],
            config: Optional[dict]
    ) -> Strategy:
        """
        Creëert een instantie van de gevraagde strategie.

        Args:
            strategy_name (str): Naam van de strategie.
            connector: MT5 connector instantie.
            risk_manager: Risk manager instantie.
            logger: Logger instantie.
            config (dict): Configuratieobject.

        Returns:
            Strategy: Een instantie van de gevraagde strategie.

        Raises:
            ValueError: Als de strategie niet bestaat.
        """
        # Laad beschikbare strategieën
        cls._load_strategies()

        # Controleer of de gevraagde strategie bestaat
        if strategy_name not in cls._strategies:
            # Speciale geval: turtle_swing is dezelfde als turtle maar met swing modus
            if strategy_name == 'turtle_swing' and 'turtle' in cls._strategies:
                strategy_name = 'turtle'
                if config and 'strategy' in config:
                    config['strategy']['swing_mode'] = True
            else:
                if logger:
                    logger.log_info(f"Onbekende strategie: {strategy_name}", level="ERROR")
                raise ValueError(f"Onbekende strategie: {strategy_name}")

        strategy_class = cls._strategies[strategy_name]

        # Maak een kopie van de config om mutatie te vermijden
        local_config = copy.deepcopy(config) if config else {}

        return strategy_class(connector, risk_manager, logger, local_config)

    @classmethod
    def list_available_strategies(cls) -> list:
        """Geeft een lijst van beschikbare strategieën."""
        cls._load_strategies()
        return list(cls._strategies.keys())
```

-----------

Path: src/strategy/turtle_strategy.py

```python
from datetime import datetime
from typing import Dict, List, Any

import MetaTrader5 as mt5
import pandas as pd

# Voorbeeld imports (pas aan naar je daadwerkelijke module-structuur)
from src.connector.mt5_connector import MT5Connector  # Placeholder
from src.risk.risk_manager import RiskManager  # Placeholder
from src.strategy.base_strategy import Strategy
from src.utils.logger import Logger  # Placeholder


class TurtleStrategy(Strategy):
    """Implementatie van de Turtle Trading strategie geoptimaliseerd voor FTMO met ondersteuning voor swing modus."""

    def __init__(self, connector: MT5Connector, risk_manager: RiskManager, logger: Logger, config: dict):
        """
        Initialiseer de Turtle strategie.

        Parameters:
        -----------
        connector : MT5Connector
            Verbinding met MetaTrader 5.
        risk_manager : RiskManager
            Risicobeheer component.
        logger : Logger
            Component voor logging.
        config : dict
            Configuratie voor de strategie, inclusief mt5- en strategy-secties.
        """
        super().__init__(connector, risk_manager, logger, config)
        self.name = "Turtle Trading Strategy"
        self.position_initial_volumes: Dict[int, float] = {}  # Ticket -> initiële volume
        self.strategy_config = config.get('strategy', {})
        self.swing_mode = self.strategy_config.get('swing_mode', False)

        # Stel parameters in gebaseerd op modus
        if self.swing_mode:
            self.entry_period = self.strategy_config.get('entry_period', 40)
            self.exit_period = self.strategy_config.get('exit_period', 20)
            self.atr_period = self.strategy_config.get('atr_period', 20)
            self.atr_multiplier = self.strategy_config.get('atr_multiplier', 2.5)
            self.logger.log_info(
                "Strategie geïnitialiseerd in Swing modus met parameters: "
                f"entry_period={self.entry_period}, exit_period={self.exit_period}, "
                f"atr_period={self.atr_period}, atr_multiplier={self.atr_multiplier}"
            )
        else:
            self.entry_period = self.strategy_config.get('entry_period', 20)
            self.exit_period = self.strategy_config.get('exit_period', 10)
            self.atr_period = self.strategy_config.get('atr_period', 20)
            self.atr_multiplier = self.strategy_config.get('atr_multiplier', 2.0)
            self.logger.log_info(
                "Strategie geïnitialiseerd in standaard modus met parameters: "
                f"entry_period={self.entry_period}, exit_period={self.exit_period}, "
                f"atr_period={self.atr_period}, atr_multiplier={self.atr_multiplier}"
            )

        self.use_trend_filter = self.strategy_config.get('use_trend_filter', True)

    def calculate_indicators(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Bereken technische indicatoren voor de Turtle strategie.

        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame met prijsdata (high, low, close, tick_volume).

        Returns:
        --------
        Dict[str, Any]
            Berekende indicatoren voor de laatste rij.
        """
        if df.empty or 'high' not in df.columns or 'low' not in df.columns or 'close' not in df.columns:
            return {}

        # Bereken ATR
        df['atr'] = self.calculate_atr(df)

        # Bereken Donchian kanalen
        df['high_entry'] = df['high'].rolling(window=self.entry_period).max()
        df['low_entry'] = df['low'].rolling(window=self.entry_period).min()
        df['high_exit'] = df['high'].rolling(window=self.exit_period).max()
        df['low_exit'] = df['low'].rolling(window=self.exit_period).min()

        # Voeg volume-indicator toe
        df['vol_avg_50'] = df['tick_volume'].rolling(window=50).mean()
        df['vol_ratio'] = df['tick_volume'] / df['vol_avg_50'].replace(0, 1)  # Vermijd deling door 0

        # Trendfilters
        if len(df) >= 50:
            df['ema_50'] = df['close'].ewm(span=50, adjust=False).mean()
        if len(df) >= 200:
            df['ema_200'] = df['close'].ewm(span=200, adjust=False).mean()

        if 'ema_50' in df.columns:
            df['trend_bullish'] = df['close'] > df['ema_50']
        if 'ema_50' in df.columns and 'ema_200' in df.columns:
            df['strong_trend'] = df['ema_50'] > df['ema_200']
        if 'ema_50' in df.columns:
            df['trend_strength'] = self.calculate_trend_strength(df)
        if 'atr' in df.columns:
            df['high_volatility'] = self.calculate_market_volatility(df)

        # Retourneer laatste waarden
        return {
            'atr': df['atr'].iloc[-1] if 'atr' in df else None,
            'high_entry': df['high_entry'].iloc[-2] if 'high_entry' in df else None,
            'low_entry': df['low_entry'].iloc[-2] if 'low_entry' in df else None,
            'high_exit': df['high_exit'].iloc[-2] if 'high_exit' in df else None,
            'low_exit': df['low_exit'].iloc[-2] if 'low_exit' in df else None,
            'trend_bullish': df['trend_bullish'].iloc[-1] if 'trend_bullish' in df else None,
            'strong_trend': df['strong_trend'].iloc[-1] if 'strong_trend' in df else None,
            'trend_strength': df['trend_strength'].iloc[-1] if 'trend_strength' in df else None,
            'high_volatility': df['high_volatility'].iloc[-1] if 'high_volatility' in df else None,
            'vol_ratio': df['vol_ratio'].iloc[-1] if 'vol_ratio' in df else None
        }

    def calculate_atr(self, df: pd.DataFrame) -> pd.Series:
        """
        Bereken de Average True Range (ATR).

        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame met prijsdata (high, low, close).

        Returns:
        --------
        pd.Series
            ATR waarden.
        """
        if 'close' not in df.columns or df['close'].isna().all():
            return pd.Series([0] * len(df), index=df.index)
        high = df['high']
        low = df['low']
        close = df['close'].shift(1).fillna(method='bfill')

        tr1 = high - low
        tr2 = abs(high - close)
        tr3 = abs(low - close)
        tr = pd.DataFrame({'tr1': tr1, 'tr2': tr2, 'tr3': tr3}).max(axis=1)
        return tr.rolling(window=self.atr_period, min_periods=1).mean()

    def calculate_trend_strength(self, df: pd.DataFrame) -> float:
        """
        Bereken trendsterkte gebaseerd op EMA-afstand en -hoek.

        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame met prijsdata.

        Returns:
        --------
        float
            Trendsterkte (0-1).
        """
        if 'ema_50' not in df.columns or len(df) < 10:
            return 0.0
        latest_close = df['close'].iloc[-1]
        latest_ema = df['ema_50'].iloc[-1]
        ema_slope = (df['ema_50'].iloc[-1] - df['ema_50'].iloc[-10]) / df['ema_50'].iloc[-10] if df['ema_50'].iloc[
                                                                                                     -10] != 0 else 0
        latest_atr = df['atr'].iloc[-1] if 'atr' in df and not pd.isna(df['atr'].iloc[-1]) else latest_close * 0.01
        distance = (latest_close - latest_ema) / latest_atr
        distance_score = min(1.0, max(0.0, distance / 3))
        slope_score = min(1.0, max(0.0, ema_slope * 20))
        return min(1.0, max(0.0, (distance_score * 0.7) + (slope_score * 0.3)))

    def calculate_market_volatility(self, df: pd.DataFrame) -> bool:
        """
        Bepaal of de markt in een hoge volatiliteitsperiode zit.

        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame met prijsdata.

        Returns:
        --------
        bool
            True als volatiliteit hoog is.
        """
        if 'atr' not in df.columns or len(df) < 20:
            return False
        avg_atr = df['atr'].iloc[-20:].mean()
        if pd.isna(avg_atr) or avg_atr == 0:
            return False
        current_atr = df['atr'].iloc[-1]
        return current_atr > (avg_atr * 1.3) if not pd.isna(current_atr) else False

    def process_symbol(self, symbol: str) -> Dict[str, Any]:
        """
        Verwerk een symbool volgens de Turtle strategie.

        Parameters:
        -----------
        symbol : str
            Het te verwerken symbool.

        Returns:
        --------
        Dict[str, Any]
            Resultaten inclusief signaal en actie.
        """
        result = {'signal': None, 'action': None}
        if not self.risk_manager.can_trade():
            self.logger.log_info(f"Dagelijkse risico-limiet bereikt, geen trades voor {symbol}")
            return result

        timeframe_str = self.config.get('mt5', {}).get('timeframe', 'H4')
        bars_needed = 240 if timeframe_str == 'H1' else 150 if timeframe_str == 'H4' else 200
        df = self.connector.get_historical_data(symbol, timeframe_str, bars_needed)
        if df.empty:
            self.logger.log_info(f"Geen historische data beschikbaar voor {symbol}")
            return result

        indicators = self.calculate_indicators(df)
        if not indicators:
            self.logger.log_info(f"Kon indicatoren niet berekenen voor {symbol}")
            return result

        tick = self.connector.get_symbol_tick(symbol)
        if tick is None:
            self.logger.log_info(f"Kon geen tick informatie krijgen voor {symbol}")
            return result

        current_price = tick.ask
        last_high_entry = indicators.get('high_entry')
        last_low_exit = indicators.get('low_exit')
        current_atr = indicators.get('atr')
        if None in (current_atr, last_high_entry, last_low_exit):
            self.logger.log_info(f"Ontbrekende indicator waarden voor {symbol}")
            return result

        trend_bullish = indicators.get('trend_bullish', True)
        strong_trend = indicators.get('strong_trend', True)
        trend_strength = indicators.get('trend_strength', 0.5)
        high_volatility = indicators.get('high_volatility', False)
        volume_ratio = indicators.get('vol_ratio', 1.0)

        price_breakout = current_price > last_high_entry * 1.001
        volume_filter = volume_ratio > 1.1 if not pd.isna(volume_ratio) else True
        entry_conditions = price_breakout and current_atr > 0 and volume_filter

        if self.use_trend_filter:
            entry_conditions = entry_conditions and trend_bullish
        if self.swing_mode:
            entry_conditions = entry_conditions and strong_trend and not high_volatility

        if entry_conditions:
            self.logger.log_info(f"Breakout gedetecteerd voor {symbol} op {current_price}")
            result['signal'] = 'ENTRY'
            result['action'] = 'BUY'

            sl_multiplier = self.atr_multiplier + 0.5 if high_volatility else self.atr_multiplier
            stop_loss = current_price - (sl_multiplier * current_atr)

            account_info = self.connector.get_account_info()
            account_balance = account_info.get('balance', self.config.get('mt5', {}).get('account_balance', 100000))
            lot_size = self.risk_manager.calculate_position_size(symbol, current_price, stop_loss, account_balance,
                                                                 trend_strength)

            if not self.risk_manager.check_trade_risk(symbol, lot_size, current_price, stop_loss):
                self.logger.log_info(f"Trade overschrijdt risicolimiet voor {symbol}")
                return result

            try:
                ticket = self.connector.place_order(
                    "BUY", symbol, lot_size, stop_loss, 0,
                    comment=f"FTMO {'Swing' if self.swing_mode else 'Turtle'}"
                )
                if ticket:
                    self.position_initial_volumes[ticket] = lot_size
                    self.logger.log_trade(
                        symbol, "BUY", current_price, lot_size, stop_loss, 0,
                        f"{'Swing' if self.swing_mode else 'Turtle'} Entry (TS:{trend_strength:.2f})",
                        self.risk_manager.leverage
                    )
                    result['ticket'] = ticket
                    result['volume'] = lot_size
                    result['stop_loss'] = stop_loss
            except Exception as e:
                self.logger.log_error(f"Fout bij plaatsen order voor {symbol}: {e}")
                return result

        self._manage_positions(symbol, current_price, last_low_exit, current_atr)
        return result

    def _manage_positions(self, symbol: str, current_price: float, last_low_exit: float, current_atr: float) -> None:
        """
        Beheer bestaande posities voor een symbool.

        Parameters:
        -----------
        symbol : str
            Trading symbool.
        current_price : float
            Huidige marktprijs.
        last_low_exit : float
            Laatste Donchian kanaal low exit.
        current_atr : float
            Huidige ATR waarde.
        """
        open_positions = self.connector.get_open_positions(symbol)
        if not open_positions:
            return

        for position in open_positions:
            position_age_days = (datetime.now().timestamp() - position.time) / (60 * 60 * 24)
            if position.type != mt5.POSITION_TYPE_BUY:
                continue

            entry_price = position.price_open
            profit_atr = 1.5 if self.swing_mode else 1.0
            profit_target_1 = entry_price + (profit_atr * current_atr)
            profit_target_2 = entry_price + (profit_atr * 2 * current_atr)
            min_hold_time = 2 if self.swing_mode else 1
            time_condition_met = position_age_days >= min_hold_time

            if (
                    time_condition_met and current_price > profit_target_1 and position.ticket in self.position_initial_volumes):
                initial_volume = self.position_initial_volumes[position.ticket]
                partial_volume = round(initial_volume * 0.4, 2)
                if position.volume >= partial_volume and partial_volume >= 0.01:
                    self.logger.log_info(f"Gedeeltelijke winstneming (40%) voor {symbol} op {current_price}")
                    try:
                        partial_result = self.connector.place_order(
                            "SELL", symbol, partial_volume, 0, 0, f"Partial Profit 40% - ticket:{position.ticket}"
                        )
                        if partial_result:
                            self.logger.log_trade(symbol, "SELL", current_price, partial_volume, 0, 0,
                                                  "Partial Profit 40%")
                            remaining_volume = position.volume - partial_volume
                            if remaining_volume >= 0.01:
                                self.connector.modify_position(position.ticket, stop_loss=entry_price, take_profit=0)
                                self.position_initial_volumes[position.ticket] = remaining_volume
                    except Exception as e:
                        self.logger.log_error(f"Fout bij gedeeltelijke winstneming voor {symbol}: {e}")

            elif (
                    time_condition_met and current_price > profit_target_2 and position.ticket in self.position_initial_volumes):
                initial_volume = self.position_initial_volumes[position.ticket]
                remaining_pct = 0.6
                partial_volume = round(initial_volume * remaining_pct * 0.5, 2)
                if position.volume >= partial_volume and partial_volume >= 0.01:
                    self.logger.log_info(f"Gedeeltelijke winstneming (30%) voor {symbol} op {current_price}")
                    try:
                        partial_result = self.connector.place_order(
                            "SELL", symbol, partial_volume, 0, 0, f"Partial Profit 30% - ticket:{position.ticket}"
                        )
                        if partial_result:
                            self.logger.log_trade(symbol, "SELL", current_price, partial_volume, 0, 0,
                                                  "Partial Profit 30%")
                            remaining_volume = position.volume - partial_volume
                            if remaining_volume >= 0.01:
                                new_sl = entry_price + ((current_price - entry_price) * 0.5)
                                self.connector.modify_position(position.ticket, stop_loss=new_sl, take_profit=0)
                                self.position_initial_volumes[position.ticket] = remaining_volume
                    except Exception as e:
                        self.logger.log_error(f"Fout bij tweede winstneming voor {symbol}: {e}")

            elif current_price < last_low_exit:
                self.logger.log_info(f"Exit signaal voor {symbol} op {current_price}")
                try:
                    close_result = self.connector.place_order(
                        "SELL", symbol, position.volume, 0, 0,
                        f"{'Swing' if self.swing_mode else 'Turtle'} Exit - ticket:{position.ticket}"
                    )
                    if close_result:
                        self.logger.log_trade(
                            symbol, "SELL", current_price, position.volume, 0, 0,
                            f"{'Swing' if self.swing_mode else 'Turtle'} System Exit"
                        )
                        if position.ticket in self.position_initial_volumes:
                            del self.position_initial_volumes[position.ticket]
                except Exception as e:
                    self.logger.log_error(f"Fout bij sluiten positie voor {symbol}: {e}")

    def get_open_positions(self) -> Dict[str, List]:
        """
        Haal alle open posities op per symbool.

        Returns:
        --------
        Dict[str, List]
            Dictionary met open posities per symbool.
        """
        result = {}
        symbols = self.config.get('mt5', {}).get('symbols', [])
        for symbol in symbols:
            positions = self.connector.get_open_positions(symbol)
            if positions:
                result[symbol] = positions
        return result
```

-----------

Path: src/utils/__init__.py

```python
```

-----------

Path: src/utils/config.py

```python
# src/utils/config.py
import json
import os
from typing import Dict, Any


def load_config(config_path: str = None) -> Dict[str, Any]:
    """
    Laad configuratie uit JSON bestand met validatie

    Parameters:
    -----------
    config_path : str, optional
        Pad naar het configuratiebestand. Als niet opgegeven wordt standaard pad gebruikt.

    Returns:
    --------
    Dict[str, Any] : Geladen configuratie

    Raises:
    -------
    FileNotFoundError : Als het configuratiebestand niet gevonden kan worden
    ValueError : Als het configuratiebestand ongeldige JSON bevat
    """
    if config_path is None:
        config_path = os.environ.get("SOPHY_CONFIG_PATH", "config/settings.json")

    try:
        with open(config_path, 'r') as file:
            config = json.load(file)

        # Valideer vereiste secties
        required_sections = ['mt5', 'risk', 'strategy']
        for section in required_sections:
            if section not in config:
                raise ValueError(f"Sectie '{section}' ontbreekt in configuratie")

        # Pas standaardwaarden toe
        if 'mt5' in config:
            config['mt5'].setdefault('timeframe', 'H4')
            config['mt5'].setdefault('symbols', ['EURUSD'])
            config['mt5'].setdefault('account_balance', 100000)

        if 'risk' in config:
            config['risk'].setdefault('max_risk_per_trade', 0.01)
            config['risk'].setdefault('max_daily_drawdown', 0.05)
            config['risk'].setdefault('max_total_drawdown', 0.10)
            config['risk'].setdefault('leverage', 30)

        if 'logging' not in config:
            config['logging'] = {'log_file': 'logs/trading_log.csv', 'log_level': 'INFO'}

        return config
    except FileNotFoundError:
        print(f"Configuratiebestand niet gevonden: {config_path}")
        raise
    except json.JSONDecodeError as e:
        print(f"Ongeldige JSON in configuratiebestand: {config_path}")
        raise ValueError(f"Ongeldige JSON in configuratiebestand: {str(e)}")
```

-----------

Path: src/utils/indicators.py

```python
# sophy/utils/indicators.py
from typing import Tuple

import numpy as np
import pandas as pd


def calculate_atr(df: pd.DataFrame, period: int = 14) -> np.ndarray:
    """
    Bereken Average True Range (ATR) met gevectoriseerde operaties

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame met OHLC data
    period : int
        ATR berekening periode

    Returns:
    --------
    np.ndarray : Array met ATR waarden
    """
    high = df['high'].values
    low = df['low'].values
    close = np.roll(df['close'].values, 1)
    close[0] = 0

    # Bereken true range componenten
    tr1 = high - low
    tr2 = np.abs(high - close)
    tr3 = np.abs(low - close)

    # Bereken true range als maximum van componenten
    tr = np.maximum(np.maximum(tr1, tr2), tr3)

    # Bereken ATR met rollend gemiddelde
    atr = np.zeros_like(tr)
    for i in range(len(tr)):
        if i < period:
            atr[i] = np.mean(tr[0:i + 1]) if i > 0 else tr[0]
        else:
            atr[i] = np.mean(tr[i - period + 1:i + 1])

    return atr


def calculate_donchian_channel(df: pd.DataFrame, period: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Bereken Donchian Channel met gevectoriseerde operaties

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame met OHLC data
    period : int
        Lookback periode

    Returns:
    --------
    Tuple[np.ndarray, np.ndarray] : Upper en lower channel waarden
    """
    # Implementatie...
```

-----------

Path: src/utils/logger.py

```python
import csv
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional


class Logger:
    """Verbeterde klasse voor logging van trades en botactiviteit"""

    def __init__(self, log_file_path: str):
        """
        Initialiseer de logger.

        Parameters:
        -----------
        log_file_path : str
            Pad naar het logbestand.
        """
        self.log_file = log_file_path

        # Maak log directory indien nodig
        log_dir = os.path.dirname(log_file_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        self.setup_log_file()

        # Logging voor performance statistieken
        self.stats_file = os.path.join(os.path.dirname(log_file_path), 'performance_stats.json')
        self.initialize_stats()

    def setup_log_file(self):
        """Bereid logbestand voor als het nog niet bestaat."""
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    'Timestamp', 'Type', 'Symbol', 'Action',
                    'Price', 'Volume', 'StopLoss', 'TakeProfit',
                    'Comment', 'Leverage', 'TrendStrength', 'Balance'
                ])
                # Voeg initiële INFO regel toe
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                writer.writerow([
                    timestamp, 'INFO', '', '', '', '', '', '',
                    'Log gestart', '', '', ''
                ])

    def initialize_stats(self):
        """Initialiseer performance statistieken bestand als het nog niet bestaat."""
        if not os.path.exists(self.stats_file):
            default_stats = {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'break_even_trades': 0,
                'win_rate': 0.0,
                'avg_win': 0.0,
                'avg_loss': 0.0,
                'profit_factor': 0.0,
                'max_drawdown': 0.0,
                'net_profit': 0.0,
                'trades_by_symbol': {},
                'daily_performance': {},
                'trade_history': []
            }
            with open(self.stats_file, 'w') as file:
                json.dump(default_stats, file, indent=4)

    def log_trade(self, symbol: str, action: str, price: float, volume: float, sl: float, tp: float,
                  comment: str, leverage: Optional[float] = None, trend_strength: Optional[float] = None,
                  balance: Optional[float] = None):
        """
        Log een trade naar CSV met uitgebreide informatie.

        Parameters:
        -----------
        symbol : str
            Handelssymbool.
        action : str
            Trade actie (BUY, SELL, etc.).
        price : float
            Uitvoeringsprijs.
        volume : float
            Order volume.
        sl : float
            Stop Loss prijs.
        tp : float
            Take Profit prijs.
        comment : str
            Commentaar bij de trade.
        leverage : float, optional
            Gebruikte hefboom.
        trend_strength : float, optional
            Sterkte van de trend op moment van trade.
        balance : float, optional
            Account balans na trade.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp, 'TRADE', symbol, action,
                price, volume, sl, tp, comment,
                leverage if leverage is not None else '', trend_strength if trend_strength is not None else '',
                balance if balance is not None else ''
            ])

        # Log ook naar trade history voor performancetracking
        self.update_trade_stats(timestamp, symbol, action, price, volume, comment)

    def log_info(self, message: str, level: str = "INFO"):
        """
        Log een informatiebericht.

        Parameters:
        -----------
        message : str
            Het te loggen bericht.
        level : str, optional
            Logniveau (INFO, WARNING, ERROR, DEBUG).
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp, level, '', '', '', '', '', '',
                message, '', '', ''
            ])
        print(f"[{timestamp}] {level}: {message}")

    def log_status(self, account_info: Dict[str, Any], open_positions: Dict[str, Any]):
        """
        Log huidige account status met verbeterde positieverwerking.

        Parameters:
        -----------
        account_info : Dict[str, Any]
            Informatie over de account.
        open_positions : Dict[str, Any]
            Informatie over open posities.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        positions_count = sum(len(pos_list) for pos_list in open_positions.values()) if open_positions else 0
        positions_detail = ""

        if positions_count > 0:
            position_parts = []
            for symbol, pos_list in open_positions.items():
                for pos in pos_list:
                    # Controleer of we met een dict of een object werken
                    if isinstance(pos, dict):
                        vol = pos.get('volume', 0)
                        profit_pct = (pos.get('profit', 0) / account_info.get('balance', 100000)) * 100
                    else:
                        # Object met attributen (zoals MT5 positie object)
                        vol = getattr(pos, 'volume', 0)
                        profit_pct = (getattr(pos, 'profit', 0) / account_info.get('balance', 100000)) * 100

                    position_parts.append(f"{symbol}:{vol}@{profit_pct:.2f}%")

            positions_detail = ", ".join(position_parts)

        equity = account_info.get('equity', 0)
        balance = account_info.get('balance', 0)
        margin = account_info.get('margin', 0)
        margin_level = (equity / margin * 100) if margin > 0 else 0
        floating_pnl = equity - balance

        status_message = (
            f"Balance: {balance}, Equity: {equity}, Floating P/L: {floating_pnl:.2f}, "
            f"Margin Level: {margin_level:.2f}%, Open positions: {positions_count}"
        )
        if positions_detail:
            status_message += f" ({positions_detail})"

        with open(self.log_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp, 'STATUS', '', '', '', '', '', '',
                status_message, '', '', balance
            ])

    def update_trade_stats(self, timestamp: str, symbol: str, action: str, price: float, volume: float,
                           comment: str):
        """
        Update performance statistieken na een trade.

        Parameters:
        -----------
        timestamp : str
            Tijdstempel van de trade.
        symbol : str
            Handelssymbool.
        action : str
            Trade actie (BUY, SELL, etc.).
        price : float
            Uitvoeringsprijs.
        volume : float
            Order volume.
        comment : str
            Commentaar bij de trade.
        """
        try:
            if not os.path.exists(self.stats_file):
                self.initialize_stats()

            with open(self.stats_file, 'r') as file:
                stats = json.load(file)

            # Voeg trade toe aan geschiedenis
            trade_record = {
                'timestamp': timestamp,
                'symbol': symbol,
                'action': action,
                'price': price,
                'volume': volume,
                'comment': comment
            }
            stats['trade_history'].append(trade_record)

            # Bijhouden trades per symbool
            if symbol not in stats['trades_by_symbol']:
                stats['trades_by_symbol'][symbol] = {'total': 0, 'buys': 0, 'sells': 0}
            stats['trades_by_symbol'][symbol]['total'] += 1
            if action == 'BUY':
                stats['trades_by_symbol'][symbol]['buys'] += 1
            elif action == 'SELL':
                stats['trades_by_symbol'][symbol]['sells'] += 1

            # Update algemene statistieken
            stats['total_trades'] += 1

            # Sla bijgewerkte statistieken op
            with open(self.stats_file, 'w') as file:
                json.dump(stats, file, indent=4)
        except json.JSONDecodeError:
            self.initialize_stats()  # Herinitialiseer bij corrupte JSON
            self.log_info("Stats bestand herinitialiseerd vanwege corrupte data", level="WARNING")
        except Exception as e:
            self.log_info(f"Fout bij bijwerken statistieken: {e}", level="ERROR")

    def log_performance_metrics(self, metrics: Dict[str, Any]):
        """
        Log prestatiemetrieken.

        Parameters:
        -----------
        metrics : dict
            Dictionary met prestatiemetrieken.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        metrics_str = ", ".join(f"{k}: {v}" for k, v in metrics.items() if k != 'trade_history')

        try:
            with open(self.log_file, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([timestamp, 'METRICS', '', '', '', '', '', '', metrics_str, '', '', ''])

            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r') as file:
                    stats = json.load(file)
                for k, v in metrics.items():
                    if k in stats and k != 'trade_history':
                        stats[k] = v
                with open(self.stats_file, 'w') as file:
                    json.dump(stats, file, indent=4)
        except Exception as e:
            self.log_info(f"Fout bij loggen van metrics: {e}", level="ERROR")```

-----------

Path: src/utils/visualizer.py

```python
import json
import os
from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


class Visualizer:
    """Verbeterde klasse voor visualisatie van trading resultaten"""

    def __init__(self, log_file, output_dir='data'):
        """
        Initialiseer de visualizer

        Parameters:
        -----------
        log_file : str
            Pad naar het logbestand
        output_dir : str, optional
            Map voor het opslaan van grafieken
        """
        self.log_file = log_file
        self.output_dir = output_dir

        # Stel visualisatiestijl in
        plt.style.use('ggplot')
        plt.rcParams['figure.figsize'] = (16, 10)
        plt.rcParams['lines.linewidth'] = 1.5
        sns.set_style("whitegrid")

        # Maak output map aan als deze niet bestaat
        os.makedirs(output_dir, exist_ok=True)

        # Pad naar presentation stats file
        log_dir = os.path.dirname(log_file)
        self.stats_file = os.path.join(log_dir, 'performance_stats.json')

    def load_trade_data(self):
        """
        Laad trade data uit het logbestand

        Returns:
        --------
        pandas.DataFrame
            DataFrame met trade data
        """
        try:
            df = pd.read_csv(self.log_file)
            # Converteer timestamp naar datetime
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            return df
        except Exception as e:
            print(f"Fout bij laden van trade data: {e}")
            return pd.DataFrame()

    def load_performance_stats(self):
        """
        Laad presentation statistieken uit JSON bestand

        Returns:
        --------
        dict
            Dictionary met performancestatistieken
        """
        if not os.path.exists(self.stats_file):
            print(f"Performance stats bestand niet gevonden: {self.stats_file}")
            return {}

        try:
            with open(self.stats_file, 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f"Fout bij laden van presentation stats: {e}")
            return {}

    def plot_equity_curve(self, include_drawdown=True):
        """
        Plot de equity curve met uitgebreide metrics

        Parameters:
        -----------
        include_drawdown : bool, optional
            Of drawdown analyse moet worden toegevoegd

        Returns:
        --------
        str
            Pad naar de opgeslagen grafiek
        """
        df = self.load_trade_data()
        if df.empty:
            print("Geen data beschikbaar voor equity curve")
            return None

        # Filter alleen op STATUS rijen
        status_df = df[df['Type'] == 'STATUS'].copy()
        if status_df.empty:
            print("Geen status data beschikbaar voor equity curve")
            return None

        # Extraheer balance en equity uit Comment kolom
        balances = []
        equities = []
        timestamps = []

        for _, row in status_df.iterrows():
            comment = row['Comment']
            timestamp = row['Timestamp']
            balance = row.get('Balance', None)

            # Probeer eerst uit de Balance kolom te halen
            if pd.notna(balance) and balance != '':
                balances.append(float(balance))
                timestamps.append(timestamp)
            else:
                # Als dat niet lukt, probeer uit de Comment te extraheren
                balance_str = comment.split('Balance: ')[1].split(',')[0] if 'Balance: ' in comment else None
                if balance_str and balance_str != 'N/A':
                    balances.append(float(balance_str))
                    timestamps.append(timestamp)

            # Extraheer equity uit comment
            equity_str = comment.split('Equity: ')[1].split(',')[0] if 'Equity: ' in comment else None
            if equity_str and equity_str != 'N/A':
                equities.append(float(equity_str))

        if not balances:
            print("Geen balance data gevonden voor equity curve")
            return None

        # Maak dataframe voor analyse
        equity_df = pd.DataFrame({
            'timestamp': timestamps,
            'balance': balances
        })

        if len(equities) == len(balances):
            equity_df['equity'] = equities

        # Bereken drawdown als die er is
        if 'equity' in equity_df.columns:
            equity_df['peak'] = equity_df['equity'].cummax()
            equity_df['drawdown'] = (equity_df['equity'] - equity_df['peak']) / equity_df['peak'] * 100
        else:
            equity_df['peak'] = equity_df['balance'].cummax()
            equity_df['drawdown'] = (equity_df['balance'] - equity_df['peak']) / equity_df['peak'] * 100

        # Bereken prestatie-metrieken
        initial_balance = equity_df['balance'].iloc[0] if not equity_df.empty else 100000
        final_balance = equity_df['balance'].iloc[-1] if not equity_df.empty else initial_balance
        total_return = ((final_balance / initial_balance) - 1) * 100
        max_drawdown = equity_df['drawdown'].min() if 'drawdown' in equity_df.columns else 0

        # Maak equity curve plot
        fig, axes = plt.subplots(2, 1, figsize=(16, 12), gridspec_kw={'height_ratios': [3, 1]})

        # Bovenste plot: Equity curve
        if 'equity' in equity_df.columns:
            axes[0].plot(equity_df['timestamp'], equity_df['equity'], label='Equity', color='blue', linewidth=2)

        axes[0].plot(equity_df['timestamp'], equity_df['balance'], label='Balance', color='green', linewidth=2)
        axes[0].plot(equity_df['timestamp'], equity_df['peak'], label='Peak Balance', color='darkgreen', linestyle='--',
                     alpha=0.6)

        # Voeg horizontale lijn toe voor beginbalans
        axes[0].axhline(y=initial_balance, color='gray', linestyle=':', alpha=0.8, label='Initial Balance')

        # Voeg horizontale lijnen toe voor 5% en 10% winst
        axes[0].axhline(y=initial_balance * 1.05, color='orange', linestyle=':', alpha=0.8, label='5% Profit')
        axes[0].axhline(y=initial_balance * 1.10, color='darkgreen', linestyle=':', alpha=0.8,
                        label='10% Profit (Target)')

        # Voeg horizontale lijnen toe voor FTMO limieten
        axes[0].axhline(y=initial_balance * 0.95, color='yellow', linestyle=':', alpha=0.8,
                        label='5% Loss (Daily Limit)')
        axes[0].axhline(y=initial_balance * 0.90, color='red', linestyle=':', alpha=0.8,
                        label='10% Loss (Max Drawdown)')

        # Voeg trade markers toe (optioneel)
        trade_df = df[df['Type'] == 'TRADE']
        if not trade_df.empty:
            buy_df = trade_df[trade_df['Action'] == 'BUY']
            sell_df = trade_df[trade_df['Action'] == 'SELL']

            if not buy_df.empty:
                axes[0].scatter(buy_df['Timestamp'], [initial_balance] * len(buy_df), marker='^', color='green',
                                s=80, label='Buy', alpha=0.7)
            if not sell_df.empty:
                axes[0].scatter(sell_df['Timestamp'], [initial_balance] * len(sell_df), marker='v', color='red',
                                s=80, label='Sell', alpha=0.7)

        # Formateer bovenste plot
        axes[0].set_title('Equity Curve & Balance History', fontsize=16)
        axes[0].set_ylabel('Account Value ($)', fontsize=14)
        axes[0].legend(loc='upper left', fontsize=12)
        axes[0].grid(True)

        # Voeg metrics toe aan de plot
        info_text = (
            f"Initial Balance: ${initial_balance:,.2f}\n"
            f"Final Balance: ${final_balance:,.2f}\n"
            f"Total Return: {total_return:.2f}%\n"
            f"Max Drawdown: {max_drawdown:.2f}%"
        )

        # Plaats info tekst in de rechterbovenhoek
        axes[0].text(0.02, 0.02, info_text, transform=axes[0].transAxes, fontsize=12,
                     bbox=dict(facecolor='white', alpha=0.7), verticalalignment='bottom')

        # Onderste plot: Drawdown
        axes[1].fill_between(equity_df['timestamp'], equity_df['drawdown'], 0,
                             color='red', alpha=0.3, label='Drawdown')
        axes[1].plot(equity_df['timestamp'], equity_df['drawdown'], color='red', linewidth=1)

        # Voeg horizontale lijnen toe voor drawdown limieten
        axes[1].axhline(y=-5, color='yellow', linestyle=':', alpha=0.8, label='5% Drawdown (Daily Limit)')
        axes[1].axhline(y=-10, color='red', linestyle=':', alpha=0.8, label='10% Drawdown (Max Limit)')

        # Formateer onderste plot
        axes[1].set_title('Drawdown (%)', fontsize=14)
        axes[1].set_xlabel('Datum', fontsize=14)
        axes[1].set_ylabel('Drawdown (%)', fontsize=14)
        axes[1].legend(loc='lower left', fontsize=12)
        axes[1].set_ylim(min(equity_df['drawdown'].min() * 1.2, -12), 1)  # Zorg voor goede y-as limieten
        axes[1].grid(True)

        # Formateer x-as voor beide plots
        for ax in axes:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax.xaxis.set_major_locator(mdates.AutoDateLocator())
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

        plt.tight_layout()

        # Sla grafiek op
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"equity_curve_{timestamp}.png")
        plt.savefig(output_path, dpi=150)
        plt.close()

        print(f"Equity curve opgeslagen als {output_path}")
        return output_path

    def plot_trade_results(self):
        """
        Plot de resultaten van trades

        Returns:
        --------
        str
            Pad naar de opgeslagen grafiek
        """
        df = self.load_trade_data()
        if df.empty:
            print("Geen data beschikbaar voor trade resultaten")
            return None

        # Filter alleen op TRADE rijen
        trade_df = df[df['Type'] == 'TRADE']
        if trade_df.empty:
            print("Geen trade data beschikbaar")
            return None

        # Groepeer trades per symbool
        symbols = trade_df['Symbol'].unique()

        # Bereken aantal figuren nodig (1 rij per symbool)
        num_symbols = len(symbols)

        # Maak plot voor elk symbool
        fig, axes = plt.subplots(num_symbols, 1, figsize=(16, 6 * num_symbols), squeeze=False)

        for i, symbol in enumerate(symbols):
            symbol_df = trade_df[trade_df['Symbol'] == symbol]

            # Converteer kolommen naar numeriek waar nodig
            for col in ['Price', 'Volume', 'StopLoss', 'TakeProfit', 'Leverage', 'TrendStrength']:
                if col in symbol_df.columns:
                    symbol_df[col] = pd.to_numeric(symbol_df[col], errors='coerce')

            # Filter buys en sells
            buys = symbol_df[symbol_df['Action'] == 'BUY']
            sells = symbol_df[symbol_df['Action'] == 'SELL']

            ax = axes[i, 0]

            # Plot trades
            if not buys.empty:
                ax.scatter(buys['Timestamp'], buys['Price'], color='green', marker='^', s=100, label='Buy')

                # Maak grootte van markers proportioneel aan volume
                if 'Volume' in buys.columns:
                    sizes = buys['Volume'] * 50 + 50  # Schaal volume voor marker grootte
                    ax.scatter(buys['Timestamp'], buys['Price'], s=sizes, color='green', marker='^', alpha=0.5)

                # Plot stop losses voor buy orders
                for _, row in buys.iterrows():
                    if pd.notna(row.get('StopLoss', None)) and row['StopLoss'] > 0:
                        ax.plot([row['Timestamp'], row['Timestamp']],
                                [row['Price'], row['StopLoss']],
                                'r--', alpha=0.5)

            if not sells.empty:
                ax.scatter(sells['Timestamp'], sells['Price'], color='red', marker='v', s=100, label='Sell')

                # Maak grootte van markers proportioneel aan volume
                if 'Volume' in sells.columns:
                    sizes = sells['Volume'] * 50 + 50
                    ax.scatter(sells['Timestamp'], sells['Price'], s=sizes, color='red', marker='v', alpha=0.5)

            # Bereken en toon winst/verlies per trade als mogelijk
            paired_trades = self._pair_trades(symbol_df)
            for pair in paired_trades:
                if len(pair) == 2:  # Alleen complete trade paren
                    buy = pair[0]
                    sell = pair[1]
                    profit_pct = ((sell['Price'] - buy['Price']) / buy['Price']) * 100

                    # Toon label voor het resultaat
                    mid_time = buy['Timestamp'] + (sell['Timestamp'] - buy['Timestamp']) / 2
                    mid_price = (buy['Price'] + sell['Price']) / 2

                    color = 'green' if profit_pct > 0 else 'red'
                    ax.text(mid_time, mid_price, f"{profit_pct:.1f}%",
                            color=color, fontweight='bold', ha='center')

                    # Verbind buy en sell punt met lijn
                    ax.plot([buy['Timestamp'], sell['Timestamp']],
                            [buy['Price'], sell['Price']],
                            color=color, linestyle='-', alpha=0.5)

            # Formateer plot
            ax.set_title(f'Trades voor {symbol}', fontsize=16)
            ax.set_ylabel('Prijs', fontsize=14)

            # Voeg gridlines toe
            ax.grid(True)
            ax.legend(loc='upper left', fontsize=12)

            # Voeg labels toe voor buy/sell punten
            for idx, row in buys.iterrows():
                volume_str = f"{row['Volume']}" if 'Volume' in row else ""
                ax.annotate(volume_str,
                            xy=(row['Timestamp'], row['Price']),
                            xytext=(5, 5), textcoords='offset points',
                            fontsize=9, color='darkgreen')

            for idx, row in sells.iterrows():
                volume_str = f"{row['Volume']}" if 'Volume' in row else ""
                ax.annotate(volume_str,
                            xy=(row['Timestamp'], row['Price']),
                            xytext=(5, -15), textcoords='offset points',
                            fontsize=9, color='darkred')

            # Formateer x-as
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
            ax.xaxis.set_major_locator(mdates.AutoDateLocator())
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

        plt.xlabel('Tijd', fontsize=14)
        plt.tight_layout()

        # Sla grafiek op
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"trade_results_{timestamp}.png")
        plt.savefig(output_path, dpi=150)
        plt.close()

        print(f"Trade resultaten opgeslagen als {output_path}")
        return output_path

    def _pair_trades(self, trade_df):
        """
        Groepeer trades in buy/sell paren

        Parameters:
        -----------
        trade_df : pandas.DataFrame
            DataFrame met trades voor één symbool

        Returns:
        --------
        list
            Lijst met paren van trades (buy/sell)
        """
        # Sorteer trades op tijdstempel
        sorted_trades = trade_df.sort_values('Timestamp').to_dict('records')

        # Verzamel paren
        pairs = []
        current_pair = []

        for trade in sorted_trades:
            if trade['Action'] == 'BUY':
                # Als we al een open pair hebben, sluit deze eerst af
                if current_pair:
                    pairs.append(current_pair)
                    current_pair = [trade]
                else:
                    current_pair = [trade]
            elif trade['Action'] == 'SELL' and current_pair:
                current_pair.append(trade)
                pairs.append(current_pair)
                current_pair = []

        # Voeg laatste onvolledige paar toe indien aanwezig
        if current_pair:
            pairs.append(current_pair)

        return pairs

    def plot_performance_summary(self):
        """
        Plot een samenvatting van de handelsperformance

        Returns:
        --------
        str
            Pad naar de opgeslagen grafiek
        """
        # Laad trade data
        df = self.load_trade_data()
        stats = self.load_performance_stats()

        if df.empty:
            print("Geen data beschikbaar voor presentation summary")
            return None

        # Filter trades
        trade_df = df[df['Type'] == 'TRADE'].copy()

        if trade_df.empty:
            print("Geen trade data beschikbaar voor analyse")
            return None

        # Converteer numerieke kolommen
        for col in ['Price', 'Volume', 'StopLoss', 'TakeProfit']:
            if col in trade_df.columns:
                trade_df[col] = pd.to_numeric(trade_df[col], errors='coerce')

        # Bereken metrics
        trades_by_symbol = {}
        symbol_performance = {}

        for symbol in trade_df['Symbol'].unique():
            symbol_df = trade_df[trade_df['Symbol'] == symbol]

            # Basic count metrics
            buys = symbol_df[symbol_df['Action'] == 'BUY']
            sells = symbol_df[symbol_df['Action'] == 'SELL']

            trades_by_symbol[symbol] = {
                'buys': len(buys),
                'sells': len(sells),
                'total': len(symbol_df)
            }

            # Bereken presentation als mogelijk
            pairs = self._pair_trades(symbol_df)
            wins = 0
            losses = 0
            total_profit_pct = 0
            total_loss_pct = 0

            for pair in pairs:
                if len(pair) == 2:  # Alleen complete trades
                    buy = pair[0]
                    sell = pair[1]

                    profit_pct = ((sell['Price'] - buy['Price']) / buy['Price']) * 100

                    if profit_pct > 0:
                        wins += 1
                        total_profit_pct += profit_pct
                    else:
                        losses += 1
                        total_loss_pct += profit_pct

            total_complete_trades = wins + losses
            win_rate = wins / total_complete_trades if total_complete_trades > 0 else 0
            avg_win = total_profit_pct / wins if wins > 0 else 0
            avg_loss = total_loss_pct / losses if losses > 0 else 0
            profit_factor = abs(total_profit_pct / total_loss_pct) if total_loss_pct < 0 else float('inf')

            symbol_performance[symbol] = {
                'win_rate': win_rate,
                'wins': wins,
                'losses': losses,
                'avg_win': avg_win,
                'avg_loss': avg_loss,
                'profit_factor': profit_factor,
                'net_profit_pct': total_profit_pct + total_loss_pct
            }

        # Maak plot
        fig = plt.figure(figsize=(20, 16))

        # Definieer grid layout
        gs = fig.add_gridspec(3, 2, height_ratios=[1, 1, 1])

        # 1. Win/Loss Ratio per Symbol (Pie chart)
        ax1 = fig.add_subplot(gs[0, 0])

        symbols = list(symbol_performance.keys())
        win_rates = [symbol_performance[s]['win_rate'] * 100 for s in symbols]

        # Kleuren gebaseerd op win rate (rood naar groen)
        colors = [(1 - wr / 100, wr / 100, 0) for wr in win_rates]

        ax1.bar(symbols, win_rates, color=colors)
        ax1.set_title('Win Rate per Symbol (%)', fontsize=14)
        ax1.set_ylim(0, 100)
        ax1.grid(axis='y')

        # Voeg datawaarden toe aan bars
        for i, v in enumerate(win_rates):
            ax1.text(i, v + 1, f"{v:.1f}%", ha='center', fontsize=12)

        # 2. Average Win vs Loss per Symbol
        ax2 = fig.add_subplot(gs[0, 1])

        # Verzamel data
        symbols = list(symbol_performance.keys())
        avg_wins = [symbol_performance[s]['avg_win'] for s in symbols]
        avg_losses = [abs(symbol_performance[s]['avg_loss']) for s in symbols]

        x = np.arange(len(symbols))
        width = 0.35

        ax2.bar(x - width / 2, avg_wins, width, label='Avg Win %', color='green', alpha=0.7)
        ax2.bar(x + width / 2, avg_losses, width, label='Avg Loss %', color='red', alpha=0.7)

        ax2.set_title('Average Win vs Loss (%)', fontsize=14)
        ax2.set_xticks(x)
        ax2.set_xticklabels(symbols)
        ax2.legend()
        ax2.grid(axis='y')

        # 3. Net Profit per Symbol
        ax3 = fig.add_subplot(gs[1, 0])

        net_profits = [symbol_performance[s]['net_profit_pct'] for s in symbols]
        colors = ['green' if p > 0 else 'red' for p in net_profits]

        ax3.bar(symbols, net_profits, color=colors, alpha=0.7)
        ax3.set_title('Net Profit per Symbol (%)', fontsize=14)
        ax3.grid(axis='y')

        # Voeg datawaarden toe
        for i, v in enumerate(net_profits):
            ax3.text(i, v + (0.1 if v >= 0 else -2), f"{v:.1f}%", ha='center', fontsize=12)

        # 4. Trades per Symbol
        ax4 = fig.add_subplot(gs[1, 1])

        # Verzamel data
        buys_per_symbol = [trades_by_symbol[s]['buys'] for s in symbols]
        sells_per_symbol = [trades_by_symbol[s]['sells'] for s in symbols]

        ax4.bar(x - width / 2, buys_per_symbol, width, label='Buy Orders', color='green', alpha=0.7)
        ax4.bar(x + width / 2, sells_per_symbol, width, label='Sell Orders', color='red', alpha=0.7)

        ax4.set_title('Number of Trades per Symbol', fontsize=14)
        ax4.set_xticks(x)
        ax4.set_xticklabels(symbols)
        ax4.legend()
        ax4.grid(axis='y')

        # 5. Overall Performance Metrics Table
        ax5 = fig.add_subplot(gs[2, :])
        ax5.axis('off')

        # Bereken totalen over alle symbolen
        total_trades = sum(trades_by_symbol[s]['total'] for s in symbols)
        total_wins = sum(symbol_performance[s]['wins'] for s in symbols)
        total_losses = sum(symbol_performance[s]['losses'] for s in symbols)

        total_win_rate = total_wins / (total_wins + total_losses) * 100 if (total_wins + total_losses) > 0 else 0
        total_profit = sum(symbol_performance[s]['net_profit_pct'] for s in symbols)

        # Custom tabel
        overall_metrics = [
            ('Total Trades', f"{total_trades}"),
            ('Win Rate', f"{total_win_rate:.1f}%"),
            ('Winning Trades', f"{total_wins}"),
            ('Losing Trades', f"{total_losses}"),
            ('Net Profit %', f"{total_profit:.2f}%"),
        ]

        table_data = []
        for metric, value in overall_metrics:
            table_data.append([metric, value])

        tbl = ax5.table(
            cellText=table_data,
            colLabels=['Metric', 'Value'],
            loc='center',
            cellLoc='center',
            colWidths=[0.3, 0.3]
        )

        tbl.auto_set_font_size(False)
        tbl.set_fontsize(14)
        tbl.scale(1, 2)

        # Stel kleuren in
        header_color = '#40466e'
        cell_color = '#f1f1f2'

        for i, key in enumerate(tbl.get_celld().keys()):
            cell = tbl.get_celld()[key]
            if i == 0:  # Header row
                cell.set_facecolor(header_color)
                cell.set_text_props(color='white', fontweight='bold')
            else:
                cell.set_facecolor(cell_color)

        ax5.set_title('Overall Performance Metrics', fontsize=16, pad=20)

        plt.tight_layout()

        # Sla grafiek op
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"performance_summary_{timestamp}.png")
        plt.savefig(output_path, dpi=150)
        plt.close()

        print(f"Performance samenvatting opgeslagen als {output_path}")
        return output_path
```

-----------

Path: testbacktrader.py

```python
import backtrader as bt
import MetaTrader5 as mt5
import pandas as pd
import datetime
import logging
import os
from pathlib import Path

# Configureer logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("BacktraderMT5")


# Custom Data Feed voor MT5
class MT5DataFeed(bt.feed.DataBase):
    params = (
        ('symbol', 'EURUSD'),
        ('timeframe', mt5.TIMEFRAME_H1),
        ('start_date', datetime.datetime(2022, 1, 1)),
        ('end_date', datetime.datetime(2023, 1, 1)),
        ('data_directory', './data_cache'),
        ('cache_data', True),
    )

    def __init__(self):
        super(MT5DataFeed, self).__init__()
        self.data_cache = {}
        self.cache_dir = Path(self.p.data_directory)

        if self.p.cache_data and not self.cache_dir.exists():
            self.cache_dir.mkdir(parents=True)

    def _get_cache_filename(self):
        start_str = self.p.start_date.strftime("%Y%m%d")
        end_str = self.p.end_date.strftime("%Y%m%d")
        return self.cache_dir / f"{self.p.symbol}_{self.p.timeframe}_{start_str}_{end_str}.pkl"

    def _load_from_cache(self):
        if not self.p.cache_data:
            return None
        cache_file = self._get_cache_filename()
        if cache_file.exists():
            try:
                data = pd.read_pickle(cache_file)
                logger.info(f"Data geladen uit cache: {cache_file}")
                return data
            except Exception as e:
                logger.warning(f"Fout bij laden uit cache {cache_file}: {e}")
        return None

    def _save_to_cache(self, data):
        if not self.p.cache_data:
            return
        cache_file = self._get_cache_filename()
        data.to_pickle(cache_file)
        logger.info(f"Data opgeslagen in cache: {cache_file}")

    def start(self):
        if not mt5.initialize():
            raise ConnectionError(f"Kan niet verbinden met MetaTrader 5: {mt5.last_error()}")

        cached_data = self._load_from_cache()
        if cached_data is not None:
            self._set_data(cached_data)
            return

        logger.info(f"Ophalen data voor {self.p.symbol}, timeframe: {self.p.timeframe}")
        start_with_margin = self.p.start_date - datetime.timedelta(days=50)

        rates = mt5.copy_rates_range(
            self.p.symbol,
            self.p.timeframe,
            int(start_with_margin.timestamp()),
            int(self.p.end_date.timestamp())
        )

        if rates is None or len(rates) == 0:
            mt5.shutdown()
            raise ValueError(f"Geen data gevonden voor {self.p.symbol} in opgegeven periode.")

        data = pd.DataFrame(rates)
        data['time'] = pd.to_datetime(data['time'], unit='s')
        data.set_index('time', inplace=True)
        data = data.loc[self.p.start_date:self.p.end_date]

        data = data.rename(columns={
            'open': 'open',
            'high': 'high',
            'low': 'low',
            'close': 'close',
            'tick_volume': 'volume'
        })

        # Controleer de data
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        if not all(col in data.columns for col in required_columns):
            raise ValueError(f"Data mist een of meer vereiste kolommen: {required_columns}")

        self._save_to_cache(data)
        self._set_data(data)

    def _set_data(self, data):
        # Zet de volledige dataset in één keer
        dates = data.index
        self.lines.datetime[:] = [bt.utils.date2num(d) for d in dates]
        self.lines.open[:] = data['open'].values
        self.lines.high[:] = data['high'].values
        self.lines.low[:] = data['low'].values
        self.lines.close[:] = data['close'].values
        self.lines.volume[:] = data['volume'].values

    def stop(self):
        mt5.shutdown()


# Turtle Trading Strategy
class TurtleStrategy(bt.Strategy):
    params = (
        ('entry_period', 20),
        ('exit_period', 10),
        ('atr_period', 20),
        ('risk_factor', 1.0),
        ('max_units', 4),
        ('pyramid_delay', 5),
    )

    def __init__(self):
        self.dc_high_entry = bt.indicators.Highest(self.data.high, period=self.params.entry_period)
        self.dc_low_entry = bt.indicators.Lowest(self.data.low, period=self.params.entry_period)
        self.dc_high_exit = bt.indicators.Highest(self.data.high, period=self.params.exit_period)
        self.dc_low_exit = bt.indicators.Lowest(self.data.low, period=self.params.exit_period)
        self.atr = bt.indicators.ATR(self.data, period=self.params.atr_period)
        self.units_long = 0
        self.units_short = 0
        self.last_entry_bar = 0
        self.bar_count = 0

    def next(self):
        self.bar_count += 1
        price = self.data.close[0]
        atr = self.atr[0]

        account_value = self.broker.getvalue()
        risk_per_trade = account_value * (self.params.risk_factor / 100)
        lot_size = 100000  # Standaard forex lotgrootte
        position_size = risk_per_trade / (atr * 2 * lot_size)  # Aantal lots

        if self.position.size == 0 or self.units_long < self.params.max_units:
            if price > self.dc_high_entry[0] and self.units_long < self.params.max_units:
                if self.units_long > 0:
                    bars_since_entry = self.bar_count - self.last_entry_bar
                    if bars_since_entry < self.params.pyramid_delay:
                        return
                self.buy(size=position_size)
                self.units_long += 1
                self.last_entry_bar = self.bar_count

        if self.position.size == 0 or self.units_short < self.params.max_units:
            if price < self.dc_low_entry[0] and self.units_short < self.params.max_units:
                if self.units_short > 0:
                    bars_since_entry = self.bar_count - self.last_entry_bar
                    if bars_since_entry < self.params.pyramid_delay:
                        return
                self.sell(size=position_size)
                self.units_short += 1
                self.last_entry_bar = self.bar_count

        if self.position.size > 0 and price < self.dc_low_exit[0]:
            self.close()
            self.units_long = 0
        elif self.position.size < 0 and price > self.dc_high_exit[0]:
            self.close()
            self.units_short = 0


# Maak en run de backtest
if __name__ == '__main__':
    cerebro = bt.Cerebro()

    data_feed = MT5DataFeed(
        symbol='EURUSD',
        timeframe=mt5.TIMEFRAME_H1,
        start_date=datetime.datetime(2022, 1, 1),
        end_date=datetime.datetime(2023, 1, 1),
        data_directory='./data_cache',
        cache_data=True
    )
    cerebro.adddata(data_feed)

    cerebro.addstrategy(TurtleStrategy)
    cerebro.broker.setcash(10000.0)
    cerebro.addsizer(bt.sizers.FixedSize, stake=1)

    print("Start backtest...")
    cerebro.run()
    print("Backtest voltooid. Plotten van resultaten...")
    cerebro.plot()```

-----------

Path: tests/conftest.py

```python
"""
Shared pytest fixtures and configuration voor het Sophy framework.
"""
import pytest
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import MagicMock


# Zorg ervoor dat logs directory bestaat
@pytest.fixture(scope="session", autouse=True)
def ensure_logs_dir():
    """Zorg ervoor dat de logs directory bestaat voor tests."""
    logs_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(logs_dir, exist_ok=True)
    return logs_dir


# Configuratie fixtures
@pytest.fixture
def test_config():
    """Standaard testconfiguratie voor componenten."""
    return {
        'mt5': {
            'symbols': ['EURUSD', 'GBPUSD', 'XAUUSD'],
            'timeframe': 'H4',
            'account_balance': 100000
        },
        'risk': {
            'max_risk_per_trade': 0.01,
            'max_daily_drawdown': 0.05,
            'max_total_drawdown': 0.10,
            'leverage': 30
        },
        'strategy': {
            'name': 'turtle',
            'swing_mode': False,
            'entry_period': 20,
            'exit_period': 10,
            'atr_period': 20,
            'atr_multiplier': 2.0
        },
        'logging': {
            'log_file': 'tests/logs/test_log.csv',
            'log_level': 'INFO'
        }
    }


# Data generator fixtures
@pytest.fixture
def generate_ohlc_data():
    """Functie voor het genereren van synthetische OHLC data."""

    def _generate(bars=100, base_price=1.2000, trend=0.0, volatility=0.002,
                  include_breakout=False, breakout_bar=80, breakout_strength=0.01):
        """
        Genereer synthetische OHLC data.

        Args:
            bars: Aantal bars om te genereren
            base_price: Startprijs
            trend: Trendfactor (-0.1 tot 0.1)
            volatility: Prijsvolatiliteit
            include_breakout: Of een breakout moet worden ingevoegd
            breakout_bar: Bar nummer voor breakout
            breakout_strength: Sterkte van de breakout

        Returns:
            DataFrame met OHLC data
        """
        date_range = pd.date_range(end=datetime.now(), periods=bars, freq='4H')

        # Genereer prijzen met wat random walk + trend
        np.random.seed(42)  # Voor reproduceerbaarheid
        random_walk = np.random.normal(0, volatility, bars).cumsum()
        trend_component = np.linspace(0, trend, bars)
        price_movement = random_walk + trend_component

        close_prices = base_price * (1 + price_movement)
        high_prices = close_prices * (1 + np.random.uniform(0, volatility, bars))
        low_prices = close_prices * (1 - np.random.uniform(0, volatility, bars))
        open_prices = close_prices.copy()
        open_prices[1:] = close_prices[:-1]  # Open price is previous close
        open_prices[0] = base_price
        volumes = np.random.randint(100, 1000, bars)

        # Voeg breakout toe indien gewenst
        if include_breakout and breakout_bar < bars:
            close_prices[breakout_bar:] *= (1 + breakout_strength)
            high_prices[breakout_bar:] *= (1 + breakout_strength * 1.2)
            low_prices[breakout_bar:] *= (1 + breakout_strength * 0.8)

        data = {
            'date': date_range,
            'open': open_prices,
            'high': high_prices,
            'low': low_prices,
            'close': close_prices,
            'tick_volume': volumes
        }

        return pd.DataFrame(data)

    return _generate```

-----------

Path: tests/fixtures/__init__.py

```python
```

-----------

Path: tests/integration/test_mt5_connectivity.py

```python
# tests/integration/test_mt5_connectivity.py
from datetime import datetime, timedelta

import pytest
from turtle_trader.data.mt5_connector import MT5Connector
from turtle_trader.utils.config import load_config


@pytest.fixture
def mt5_connector():
    """Create a connector instance with test configuration"""
    config = load_config("tests/config/test_config.json")
    from turtle_trader.utils.logger import Logger
    logger = Logger("tests/logs/test_log.csv")
    return MT5Connector(config['mt5'], logger)


def test_mt5_connection(mt5_connector):
    """Test connection to MT5 platform"""
    # Connect to MT5
    connected = mt5_connector.connect()
    assert connected, "Failed to connect to MT5"

    # Clean up
    mt5_connector.disconnect()


def test_historical_data_retrieval(mt5_connector):
    """Test retrieving historical data from MT5"""
    # Connect to MT5
    connected = mt5_connector.connect()
    assert connected, "Failed to connect to MT5"

    # Get historical data
    symbol = "EURUSD"
    end_date = datetime.now()
    start_date = end_date - timedelta(days=5)

    df = mt5_connector.get_historical_data(symbol, 16, 100)  # 16 = H4 timeframe

    # Validate data
    assert not df.empty, "No historical data retrieved"
    assert 'open' in df.columns, "Data missing expected columns"
    assert 'high' in df.columns, "Data missing expected columns"
    assert 'low' in df.columns, "Data missing expected columns"
    assert 'close' in df.columns, "Data missing expected columns"

    # Clean up
    mt5_connector.disconnect()
```

-----------

Path: tests/integration/test_trading_workflow.py

```python
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
```

-----------

Path: tests/performance/__init__.py

```python
```

-----------

Path: tests/unit/__init__.py

```python
```

-----------

Path: tests/unit/risk/__init__.py

```python
```

-----------

Path: tests/unit/risk/test_position_sizer.py

```python
import pytest
from src.risk.position_sizer import calculate_position_size


class TestPositionSizer:
    def test_normal_market_conditions(self):
        """Test positiegrootte onder normale marktcondities."""
        # 50 pips stop loss op een forex pair
        result = calculate_position_size(
            entry_price=1.2000,
            stop_loss=1.1950,  # 50 pips SL
            account_balance=100000,
            risk_percentage=0.01,  # 1% risico
            pip_value=10.0
        )
        # Verwacht ~1.0 lot (100000 * 0.01 / (50 * 10))
        assert 0.9 <= result <= 1.1

    def test_high_volatility_conditions(self):
        """Test positiegrootte bij hoge volatiliteit (wijdere stop loss)."""
        # 100 pips stop loss op een forex pair
        result = calculate_position_size(
            entry_price=1.2000,
            stop_loss=1.1900,  # 100 pips SL
            account_balance=100000,
            risk_percentage=0.01,  # 1% risico
            pip_value=10.0
        )
        # Verwacht ~0.5 lot (100000 * 0.01 / (100 * 10))
        assert 0.4 <= result <= 0.6

    def test_gold_instrument(self):
        """Test positiegrootte voor XAUUSD."""
        # Goud heeft andere pip waarde berekening
        result = calculate_position_size(
            entry_price=1800.00,
            stop_loss=1790.00,  # $10 verschil
            account_balance=100000,
            risk_percentage=0.01,  # 1% risico
            pip_value=10.0,
            min_lot=0.01,
            max_lot=10.0
        )
        # Verifieer correcte positiegrootte voor goud
        assert 0.08 <= result <= 0.12

    def test_minimum_lot_size(self):
        """Test minimale lotgrootte restrictie."""
        # Zeer wijde stop loss die zou leiden tot kleine positiegrootte
        result = calculate_position_size(
            entry_price=1.2000,
            stop_loss=1.1500,  # 500 pips SL
            account_balance=100000,
            risk_percentage=0.01,  # 1% risico
            pip_value=10.0,
            min_lot=0.01,
            max_lot=10.0
        )
        # Moet minimaal 0.01 lot zijn, ongeacht berekening
        assert result == 0.01

    def test_maximum_lot_size(self):
        """Test maximale lotgrootte restrictie."""
        # Zeer nauwe stop loss of hoog risicopercentage
        result = calculate_position_size(
            entry_price=1.2000,
            stop_loss=1.1990,  # 10 pips SL
            account_balance=100000,
            risk_percentage=0.05,  # 5% risico
            pip_value=10.0,
            min_lot=0.01,
            max_lot=10.0
        )
        # Moet maximaal 10.0 lot zijn, ongeacht berekening
        assert result == 10.0

    def test_zero_stop_loss(self):
        """Test het geval waar stop loss gelijk is aan entry (zou deling door nul veroorzaken)."""
        result = calculate_position_size(
            entry_price=1.2000,
            stop_loss=1.2000,  # Identiek aan entry
            account_balance=100000,
            risk_percentage=0.01,
            pip_value=10.0
        )
        # Moet minimale lotgrootte teruggeven om deling door nul te voorkomen
        assert result == 0.01```

-----------

Path: tests/unit/risk/test_risk_manager.py

```python
import pytest
from datetime import datetime, timedelta
from src.risk.risk_manager import RiskManager
from src.utils.logger import Logger


@pytest.fixture
def risk_manager():
    """Fixture voor het creëren van een RiskManager instantie."""
    config = {
        "max_risk_per_trade": 0.01,
        "max_daily_drawdown": 0.05,
        "max_total_drawdown": 0.10,
        "leverage": 30,
        "account_balance": 100000
    }
    logger = Logger("tests/logs/test_log.csv")
    return RiskManager(config, logger)


class TestRiskManager:
    def test_ftmo_limits_normal_conditions(self, risk_manager):
        """Test FTMO limieten onder normale omstandigheden."""
        account_info = {
            "balance": 100000,
            "equity": 100000
        }
        should_stop, reason = risk_manager.check_ftmo_limits(account_info)
        assert not should_stop
        assert reason is None

    def test_ftmo_limits_profit_target_reached(self, risk_manager):
        """Test dat handelssysteem stopt wanneer winstdoel is bereikt."""
        account_info = {
            "balance": 110000,  # 10% winst
            "equity": 110000
        }
        should_stop, reason = risk_manager.check_ftmo_limits(account_info)
        assert should_stop
        assert "winstdoel" in reason.lower()

    def test_ftmo_limits_daily_drawdown_exceeded(self, risk_manager):
        """Test dat handelssysteem stopt wanneer dagelijkse drawdown limiet is overschreden."""
        account_info = {
            "balance": 100000,
            "equity": 94900  # 5.1% drawdown
        }
        should_stop, reason = risk_manager.check_ftmo_limits(account_info)
        assert should_stop
        assert "dagelijkse verlieslimiet" in reason.lower()

    def test_ftmo_limits_total_drawdown_exceeded(self, risk_manager):
        """Test dat handelssysteem stopt wanneer totale drawdown limiet is overschreden."""
        account_info = {
            "balance": 100000,
            "equity": 89900  # 10.1% drawdown
        }
        should_stop, reason = risk_manager.check_ftmo_limits(account_info)
        assert should_stop
        assert "maximale drawdown" in reason.lower()

    def test_daily_limits_reset(self, risk_manager, monkeypatch):
        """Test dat dagelijkse limieten worden gereset na een nieuwe dag."""
        # Simuleer een eerdere datum
        yesterday = datetime.now() - timedelta(days=1)
        monkeypatch.setattr(risk_manager, "current_date", yesterday.date())

        # Stel limieten in op bijna overschreden waarden
        risk_manager.daily_losses = 4900  # Net onder 5% van 100k
        risk_manager.daily_trades_count = 9  # Net onder max_daily_trades (10)

        # Controleer of limieten worden gereset bij controle op nieuwe dag
        assert risk_manager.can_trade()
        assert risk_manager.daily_losses == 0
        assert risk_manager.daily_trades_count == 0```

-----------

Path: tests/unit/strategy/__init__.py

```python
```

-----------

Path: tests/unit/test_turtle_strategy.py

```python
import pytest
import pandas as pd
import numpy as np
from unittest.mock import MagicMock
from src.strategy.turtle_strategy import TurtleStrategy


@pytest.fixture
def mock_connector():
    """Fixture voor het creëren van een mock connector."""
    connector = MagicMock()

    # Configureer de get_historical_data methode om testdata terug te geven
    def mock_get_historical_data(symbol, timeframe, bars):
        # Creëer synthetische OHLC data
        date_range = pd.date_range(end=pd.Timestamp.now(), periods=bars, freq='4H')
        base_price = 1.2000

        # Creëer een standaard range met lichte opwaartse trend
        data = {
            'date': date_range,
            'open': np.linspace(base_price, base_price * 1.05, bars),
            'high': np.linspace(base_price, base_price * 1.05, bars) * 1.002,
            'low': np.linspace(base_price, base_price * 1.05, bars) * 0.998,
            'close': np.linspace(base_price, base_price * 1.05, bars) * 1.001,
            'tick_volume': np.random.randint(100, 1000, bars)
        }

        # Voeg duidelijke breakout toe rond bar 80
        if bars > 80:
            breakout_idx = 80
            data['high'][breakout_idx:] *= 1.01  # Verhoog highs na breakout
            data['low'][breakout_idx:] *= 1.005  # Verhoog lows na breakout
            data['close'][breakout_idx:] *= 1.008  # Verhoog close na breakout

        return pd.DataFrame(data)

    connector.get_historical_data.side_effect = mock_get_historical_data

    # Mock tick data
    tick = MagicMock()
    tick.ask = 1.2100
    tick.bid = 1.2095
    connector.get_symbol_tick.return_value = tick

    # Mock account info
    connector.get_account_info.return_value = {
        "balance": 100000,
        "equity": 100000,
        "margin": 1000,
        "free_margin": 99000
    }

    return connector


@pytest.fixture
def mock_risk_manager():
    """Fixture voor het creëren van een mock risk manager."""
    risk_manager = MagicMock()
    risk_manager.can_trade.return_value = True
    risk_manager.calculate_position_size.return_value = 1.0
    risk_manager.check_trade_risk.return_value = True
    return risk_manager


@pytest.fixture
def mock_logger():
    """Fixture voor het creëren van een mock logger."""
    return MagicMock()


@pytest.fixture
def turtle_strategy(mock_connector, mock_risk_manager, mock_logger):
    """Fixture voor het creëren van de te testen TurtleStrategy."""
    config = {
        'mt5': {
            'symbols': ['EURUSD'],
            'timeframe': 'H4'
        },
        'strategy': {
            'name': 'turtle',
            'swing_mode': False,
            'entry_period': 20,
            'exit_period': 10,
            'atr_period': 20,
            'atr_multiplier': 2.0,
            'use_trend_filter': True
        }
    }
    return TurtleStrategy(mock_connector, mock_risk_manager, mock_logger, config)


class TestTurtleStrategy:
    def test_calculate_atr(self, turtle_strategy):
        """Test ATR berekening."""
        # Creëer testdata
        data = pd.DataFrame({
            'high': [1.2010, 1.2020, 1.2030, 1.2025, 1.2040],
            'low': [1.1990, 1.2000, 1.2010, 1.2000, 1.2020],
            'close': [1.2000, 1.2010, 1.2020, 1.2015, 1.2030]
        })

        # Bereken ATR
        atr = turtle_strategy.calculate_atr(data)

        # Verifieer resultaten
        assert len(atr) == len(data)
        assert all(atr > 0)  # ATR moet altijd positief zijn
        # Handmatige berekening voor laatste waarde
        true_range = max(data['high'].iloc[-1] - data['low'].iloc[-1],
                         abs(data['high'].iloc[-1] - data['close'].iloc[-2]),
                         abs(data['low'].iloc[-1] - data['close'].iloc[-2]))
        expected_atr = (atr.iloc[-2] * (turtle_strategy.atr_period - 1) + true_range) / turtle_strategy.atr_period
        assert abs(atr.iloc[-1] - expected_atr) < 0.0001

    def test_calculate_indicators(self, turtle_strategy, mock_connector):
        """Test indicator berekeningen."""
        # Haal testdata op via de mock connector
        df = mock_connector.get_historical_data('EURUSD', 'H4', 100)

        # Bereken indicators
        indicators = turtle_strategy.calculate_indicators(df)

        # Verifieer resultaten
        assert 'atr' in indicators
        assert indicators['atr'] > 0
        assert 'high_entry' in indicators
        assert 'low_entry' in indicators
        assert 'high_exit' in indicators
        assert 'low_exit' in indicators
        assert 'trend_bullish' in indicators

        # Verifieer dat high_entry hoger is dan low_entry
        assert indicators['high_entry'] > indicators['low_entry']

    def test_process_symbol_breakout(self, turtle_strategy, mock_connector):
        """Test verwerking van een breakout signaal."""
        # Configureer de mock om een breakout te simuleren
        tick = mock_connector.get_symbol_tick.return_value
        tick.ask = 1.2200  # Hoge prijs die boven entry niveau ligt

        # Configureer place_order om een ticket te returnen
        mock_connector.place_order.return_value = 12345

        # Verwerk symbool
        result = turtle_strategy.process_symbol('EURUSD')

        # Verifieer resultaten
        assert result['signal'] == 'ENTRY'
        assert result['action'] == 'BUY'
        assert result['ticket'] == 12345

        # Verifieer dat place_order werd aangeroepen
        mock_connector.place_order.assert_called_once()

        # Controleer parameters voor de order
        args, kwargs = mock_connector.place_order.call_args
        assert args[0] == 'BUY'  # Actie
        assert args[1] == 'EURUSD'  # Symbool
        assert args[2] == 1.0  # Volume (van mock risk manager)

    def test_process_symbol_no_signal(self, turtle_strategy, mock_connector):
        """Test verwerking zonder handelssignaal."""
        # Configureer de mock voor een normale prijs zonder breakout
        tick = mock_connector.get_symbol_tick.return_value
        tick.ask = 1.2000  # Prijs onder entry niveau

        # Verwerk symbool
        result = turtle_strategy.process_symbol('EURUSD')

        # Verifieer resultaten
        assert result['signal'] is None
        assert result['action'] is None

        # Verifieer dat place_order niet werd aangeroepen
        mock_connector.place_order.assert_not_called()```

-----------

Path: verify_sophy.py

```python
#!/usr/bin/env python3
"""
Sophy Framework Verificatiescript

Dit script voert een reeks tests uit om te controleren of de Sophy Trading Framework
correct is geïnstalleerd en de basisfunctionaliteit werkt.
"""
import os
import sys
import json
import importlib
from datetime import datetime, timedelta

# Voeg src directory toe aan Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(script_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)


def log_step(msg):
    """Log een stap naar console met duidelijke opmaak"""
    print(f"\n{'-' * 80}\n>> {msg}\n{'-' * 80}")


def log_pass(msg):
    """Log een succesvolle test"""
    print(f"✅ {msg}")


def log_fail(msg):
    """Log een mislukte test"""
    print(f"❌ {msg}")


def test_imports():
    """Test of alle benodigde modules kunnen worden geïmporteerd"""
    log_step("Testen van module imports...")

    modules_to_test = [
        "src.utils.config",
        "src.utils.logger",
        "src.connector.mt5_connector",
        "src.risk.risk_manager",
        "src.strategy.turtle_strategy",
        "src.strategy.strategy_factory",
        "src.analysis.backtester",
        "src.ftmo.ftmo_validator"
    ]

    all_passed = True
    for module_name in modules_to_test:
        try:
            module = importlib.import_module(module_name)
            log_pass(f"Module {module_name} succesvol geïmporteerd")
        except ImportError as e:
            log_fail(f"Kan module {module_name} niet importeren: {e}")
            all_passed = False

    return all_passed


def test_config_loading():
    """Test of de configuratie correct kan worden geladen"""
    log_step("Testen van configuratie laden...")

    from src.utils.config import load_config

    # Test standaard config
    try:
        default_config = load_config()
        if default_config and isinstance(default_config, dict):
            log_pass("Standaard configuratie succesvol geladen")
        else:
            log_fail("Standaard configuratie niet correct geladen")
            return False
    except Exception as e:
        log_fail(f"Fout bij laden standaard configuratie: {e}")
        return False

    # Maak een test config file
    test_config_path = os.path.join(script_dir, "test_config.json")
    test_config = {
        "mt5": {
            "login": 1234567,
            "password": "test_password",
            "server": "Demo-Server",
            "symbols": ["EURUSD", "GBPUSD"],
            "timeframe": "H4",
            "account_balance": 100000
        },
        "risk": {
            "max_risk_per_trade": 0.01,
            "max_daily_drawdown": 0.05,
            "max_total_drawdown": 0.10,
            "leverage": 30
        },
        "strategy": {
            "name": "turtle",
            "swing_mode": False,
            "entry_period": 20,
            "exit_period": 10,
            "atr_period": 20,
            "atr_multiplier": 2.0
        },
        "logging": {
            "log_file": "logs/test_log.csv",
            "log_level": "INFO"
        }
    }

    try:
        with open(test_config_path, "w") as f:
            json.dump(test_config, f, indent=4)

        # Laad test config
        test_loaded_config = load_config(test_config_path)
        if test_loaded_config and isinstance(test_loaded_config, dict):
            log_pass("Test configuratie succesvol geladen")
        else:
            log_fail("Test configuratie niet correct geladen")
            return False

        # Verwijder test config file
        os.remove(test_config_path)

    except Exception as e:
        log_fail(f"Fout bij test configuratie: {e}")
        if os.path.exists(test_config_path):
            os.remove(test_config_path)
        return False

    return True


def test_logger():
    """Test of de logger correct werkt"""
    log_step("Testen van logger...")

    from src.utils.logger import Logger

    log_dir = os.path.join(script_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "test_log.csv")

    try:
        # Maak logger aan
        logger = Logger(log_file)

        # Test logging methoden
        logger.log_info("Test info bericht")
        logger.log_info("Test warning bericht", level="WARNING")
        logger.log_info("Test error bericht", level="ERROR")

        logger.log_trade("EURUSD", "BUY", 1.2000, 0.1, 1.1950, 1.2100, "Test trade")

        account_info = {
            "balance": 100000,
            "equity": 100050,
            "margin": 500,
            "free_margin": 99550,
            "margin_level": 20010.0,
            "profit": 50
        }
        open_positions = {
            "EURUSD": [{
                "symbol": "EURUSD",
                "volume": 0.1,
                "profit": 50
            }]
        }
        logger.log_status(account_info, open_positions)

        # Controleer of bestand is aangemaakt
        if os.path.exists(log_file):
            log_pass(f"Logger heeft succesvol geschreven naar {log_file}")
        else:
            log_fail(f"Logger kon niet schrijven naar {log_file}")
            return False

    except Exception as e:
        log_fail(f"Fout bij testen logger: {e}")
        return False

    return True


def test_risk_manager():
    """Test of de RiskManager correct werkt"""
    log_step("Testen van RiskManager...")

    from src.risk.risk_manager import RiskManager
    from src.utils.logger import Logger

    log_file = os.path.join(script_dir, "logs", "test_log.csv")
    logger = Logger(log_file)

    config = {
        "max_risk_per_trade": 0.01,
        "max_daily_drawdown": 0.05,
        "max_total_drawdown": 0.10,
        "leverage": 30,
        "account_balance": 100000
    }

    try:
        risk_manager = RiskManager(config, logger)

        # Test positiegrootte berekening
        position_size = risk_manager.calculate_position_size(
            symbol="EURUSD",
            entry_price=1.2000,
            stop_loss=1.1950,
            account_balance=100000,
            trend_strength=0.5
        )

        if position_size > 0:
            log_pass(f"Positiegrootte berekening succesvol: {position_size} lots")
        else:
            log_fail(f"Positiegrootte berekening onjuist: {position_size}")
            return False

        # Test FTMO limieten checks
        account_info = {"balance": 100000, "equity": 100000}
        should_stop, reason = risk_manager.check_ftmo_limits(account_info)

        if not should_stop:
            log_pass("FTMO limieten check succesvol (geen limieten overschreden)")
        else:
            log_fail(f"FTMO limieten check onjuist: {reason}")
            return False

        # Test trade risico check
        result = risk_manager.check_trade_risk("EURUSD", 0.1, 1.2000, 1.1950)

        if result:
            log_pass("Trade risico check succesvol")
        else:
            log_fail("Trade risico check gefaald")
            return False

    except Exception as e:
        log_fail(f"Fout bij testen RiskManager: {e}")
        return False

    return True


def test_strategy_factory():
    """Test of de StrategyFactory correct werkt"""
    log_step("Testen van StrategyFactory...")

    from src.strategy.strategy_factory import StrategyFactory
    from src.utils.logger import Logger

    log_file = os.path.join(script_dir, "logs", "test_log.csv")
    logger = Logger(log_file)

    config = {
        "mt5": {
            "login": 1234567,
            "password": "test_password",
            "server": "Demo-Server",
            "symbols": ["EURUSD", "GBPUSD"],
            "timeframe": "H4",
            "account_balance": 100000
        },
        "risk": {
            "max_risk_per_trade": 0.01,
            "max_daily_drawdown": 0.05,
            "max_total_drawdown": 0.10,
            "leverage": 30
        },
        "strategy": {
            "name": "turtle",
            "swing_mode": False,
            "entry_period": 20,
            "exit_period": 10,
            "atr_period": 20,
            "atr_multiplier": 2.0
        }
    }

    try:
        # Test beschikbare strategieën ophalen
        available_strategies = StrategyFactory.list_available_strategies()

        if "turtle" in available_strategies:
            log_pass(f"StrategyFactory lijst van strategieën succesvol: {available_strategies}")
        else:
            log_fail(f"StrategyFactory lijst van strategieën mist 'turtle': {available_strategies}")
            return False

        # Test strategie maken
        # Maak dummy connector en risk manager
        connector = type('DummyConnector', (), {})()
        risk_manager = type('DummyRiskManager', (), {})()

        strategy = StrategyFactory.create_strategy(
            strategy_name="turtle",
            connector=connector,
            risk_manager=risk_manager,
            logger=logger,
            config=config
        )

        if strategy and strategy.get_name() == "Turtle Trading Strategy":
            log_pass("StrategyFactory succesvol strategie aangemaakt")
        else:
            log_fail(
                f"StrategyFactory kon geen strategie aanmaken of verkeerde naam: {strategy.get_name() if strategy else None}")
            return False

    except Exception as e:
        log_fail(f"Fout bij testen StrategyFactory: {e}")
        return False

    return True


def run_tests():
    """Voer alle tests uit en rapporteer resultaten"""
    print("\n" + "=" * 80)
    print(f"SOPHY FRAMEWORK VERIFICATIE - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    tests = [
        ("Module imports", test_imports),
        ("Config laden", test_config_loading),
        ("Logger", test_logger),
        ("RiskManager", test_risk_manager),
        ("StrategyFactory", test_strategy_factory),
    ]

    results = {}
    all_passed = True

    for test_name, test_func in tests:
        print(f"\nUitvoeren test: {test_name}")
        try:
            result = test_func()
            results[test_name] = result
            if not result:
                all_passed = False
        except Exception as e:
            print(f"❌ Onverwachte fout bij test {test_name}: {e}")
            results[test_name] = False
            all_passed = False

    # Samenvattingsrapport
    print("\n" + "=" * 80)
    print("TESTRESULTATEN SAMENVATTING")
    print("=" * 80)

    for test_name, result in results.items():
        status = "PASSED" if result else "FAILED"
        print(f"{status:10} - {test_name}")

    print("\n" + "=" * 80)
    overall_status = "PASSED" if all_passed else "FAILED"
    print(f"EINDRESULTAAT: {overall_status}")
    print("=" * 80 + "\n")

    return all_passed


if __name__ == "__main__":
    run_tests()```

-----------

