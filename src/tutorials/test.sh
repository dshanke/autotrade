TICKER=NIFTYBEES.NS
CASH=2500000
for YYYY in {2011..2022}
do
    echo $YYYY
    echo "VSIP: $(python3 _backtest_VSIP.py --ticker $TICKER --cash $CASH --start "${YYYY}-01-01" --end "${YYYY}-12-31" | tail -1)"
    echo "BDSP: $(python3 _backtest_BuyDaily_SellOnProfit.py --ticker $TICKER --cash $CASH --start "${YYYY}-01-01" --end "${YYYY}-12-31" | tail -1)"
done

SY="2011"
EY="2022"
echo "VSIP: $(python3 _backtest_VSIP.py --ticker $TICKER --cash $CASH --start "${SY}-01-01" --end "${EY}-12-31" | tail -1)"
echo "BDSP: $(python3 _backtest_BuyDaily_SellOnProfit.py --ticker $TICKER --cash $CASH --start "${SY}-01-01" --end "${EY}-12-31" | tail -1)"

#echo VSIP: python3 _backtest_VSIP.py --ticker $TICKER --cash $CASH --start "${YYYY}-01-01" --end "${YYYY}-12-31"
#echo BDSP: python3 _backtest_BuyDaily_SellOnProfit.py --ticker $TICKER --cash $CASH --start "${YYYY}-01-01" --end "${YYYY}-12-31"
