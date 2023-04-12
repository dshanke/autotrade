#pip install nsepython
#pip install --upgrade nsepython
#docs: https://forum.unofficed.com/t/nsepython-documentation/376
# python3.8 -m venv pyenv38
# source pyenv38/bin/activate
# python -m pip install --upgrade pip
# pip3 install -r requirements.txt

# source pyenv38/bin/activate
# export PS1='pyenv38>'


from nsepython import *


#need to fix this up
def market_status(): 
    status_list = nse_marketStatus()["marketState"]
    for kvp in status_list:
        if kvp['market'] == 'Capital Market':
            print(f"Market is { 'Closed' if kvp['marketStatus'] == 'Closed' else 'Open' } for Trading Now")
            return False if kvp['marketStatus'] == 'Closed' else True
    raise "nse_marketStatus Failed"

def get_expiry_dates(eq):
    return expiry_list(eq)

def get_next_expiry_date(eq, index):
    return get_expiry_dates(eq)[index]

def get_nse_trading_holiday():
    return nse_holidays('trading')

def get_nse_clearing_holiday():
    return nse_holidays('clearing')

def get_eq_info(eq):
    print(f"eq: {eq}")
    lot_size = nse_get_fno_lot_sizes(eq)
    ltp = nse_eq(eq)['priceInfo']['lastPrice']
    corpus = ltp * lot_size
    print(f"ltp: { ltp }, lot_size: {lot_size}, corpus: { corpus }")
    return ltp, lot_size, corpus

def get_atm_strike_df_record(ltp, oi_df, low_high_sp=False):
    oi_df_subset = oi_df[['Strike Price']]
    prev_diff = diff = 0
    atm_sp = 0
    sp_row_loc_lower = -1
    sp_row_loc_upper = -1
    sp_row_loc = -1
    for rec_loc in range(0, len(oi_df_subset)):
        sp = oi_df_subset.loc[[rec_loc][0]]['Strike Price']
        diff = abs(sp - ltp)
        # print(f"sp: {sp}, ltp: {ltp}, diff: {diff}")
        if prev_diff == 0:
            prev_diff = diff
            atm_sp = sp
            sp_row_loc_lower = sp_row_loc
            sp_row_loc = rec_loc
        elif diff < prev_diff:
            atm_sp = sp
            prev_diff = diff
            sp_row_loc_lower = sp_row_loc
            sp_row_loc = rec_loc
        elif sp_row_loc_upper == -1:
            sp_row_loc_upper = sp_row_loc

    if low_high_sp:
        return oi_df.loc[[sp_row_loc_lower][0]], oi_df.loc[[sp_row_loc_upper][0]], sp_row_loc_lower 
    else:
        return oi_df.loc[[sp_row_loc][0]], oi_df.loc[[sp_row_loc][0]], sp_row_loc 


def get_atm_call_metadata(eq, exp_date="latest", low_high_sp=False):
    oi_df, ltp, crontime = oi_chain_builder(eq,exp_date,"full")
    df_lower_rec, df_higher_rec, sp_loc = get_atm_strike_df_record(ltp=ltp, oi_df=oi_df, low_high_sp=low_high_sp)
    putsp = round(df_lower_rec['Strike Price'], 2)
    callsp = round(df_higher_rec['Strike Price'], 2)
    ce_mid_price = round((df_higher_rec['CALLS_Bid Price'] + df_higher_rec['CALLS_Ask Price'])/2, 2)
    pe_mid_price = round((df_lower_rec['PUTS_Bid Price'] + df_lower_rec['PUTS_Ask Price'])/2, 2)
    print(f"ltp: { ltp }, putsp: { putsp }, callsp: { callsp }, ce_mid_price: { ce_mid_price }, pe_mid_price: { pe_mid_price }")
    return ltp, callsp, putsp, ce_mid_price, pe_mid_price

def get_atm_straddle_stats(eq, lot_size, exp_date="latest", low_high_sp=False):
    ltp, callsp, putsp, ce_mid_price, pe_mid_price = get_atm_call_metadata(eq=eq, exp_date=exp_date, low_high_sp=low_high_sp)
    corpus = round(ltp*lot_size, 2)
    max_premium_collection = round(lot_size * (ce_mid_price+pe_mid_price), 2)
    premium_percent = round(max_premium_collection/corpus*100,2)
    print(f"max_premium_collection: {max_premium_collection}, corpus: {corpus}, collection%: {premium_percent}")
    return ltp, callsp, putsp, ce_mid_price, pe_mid_price, max_premium_collection, corpus, premium_percent


market_status()
fav1 = ['ICICIBANK', 'HDFCBANK']
nse_nifty_stocks = ['ADANIENT','ADANIPORTS','APOLLOHOSP','ASIANPAINT','AXISBANK','BAJAJ-AUTO','BAJFINANCE','BAJAJFINSV','BPCL','BHARTIARTL','BRITANNIA','CIPLA','COALINDIA','DIVISLAB','DRREDDY','EICHERMOT','GRASIM','HCLTECH','HDFCBANK','HDFCLIFE','HEROMOTOCO','HINDALCO','HINDUNILVR','HDFC','ICICIBANK','ITC','INDUSINDBK','INFY','JSWSTEEL','KOTAKBANK','LT','M&M','MARUTI','NTPC','NESTLEIND','ONGC','POWERGRID','RELIANCE','SBILIFE','SBIN','SUNPHARMA','TCS','TATACONSUM','TATAMOTORS','TATASTEEL','TECHM','TITAN','UPL','ULTRACEMCO','WIPRO']

eq_list = fav1
eq_atm_info = []
# exp_date = "latest"
index_to_date = 1 # 0 (current expiry date), 1 (next expiry date), 2 (last expiry date)
get_me_low_high_sp = False

for eq in eq_list:
    exp_date = get_next_expiry_date(eq, index_to_date)
    ltp, lot_size, corpus = get_eq_info(eq)
    ltp, callsp, putsp, ce_mid_price, pe_mid_price, max_premium_collection, corpus, premium_percent = \
        get_atm_straddle_stats(eq, lot_size, exp_date, get_me_low_high_sp)
    eq_atm_info.append((eq, ltp, lot_size, callsp, putsp, ce_mid_price, pe_mid_price, max_premium_collection, corpus, premium_percent))
    print('\n')

print("eq,ltp,lot_size,callsp,putsp,ce_mid_price,pe_mid_price,max_premium_collection,corpus,premium_percent")
for rec in eq_atm_info:
    print(f"{rec[0]},{rec[1]},{rec[2]},{rec[3]},{rec[4]},{rec[5]},{rec[6]},{rec[7]},{rec[8]},{rec[9]}")

