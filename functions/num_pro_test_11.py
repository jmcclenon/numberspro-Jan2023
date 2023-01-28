# This code creates holding rows for variables that may be used in the future.

mat_stdebt = pd.DataFrame(np.zeros((1,55)))
new_stdebt = pd.DataFrame(np.zeros((1,55)))
cap_ex = pd.DataFrame(np.zeros((1,55)))
lt_invest = pd.DataFrame(np.zeros((1,55)))
new_equity = pd.DataFrame(np.zeros((1,55)))
new_ltdebt = pd.DataFrame(np.zeros((1,55)))

mat_stdebt.index = ['Mat of ST Debt']

cap_ex.index = ['Capital Expenditures']
#cap_ex.index.name = 'CAP EX'

lt_invest.index = ['LT Investment']
#lt_invest.index.name = 'LT Investment'

new_equity.index = ['New Equity']
#new_equity.index.name = 'New Equity'

new_ltdebt.index = ['New LT Debt']
#new_ltdebt.index.name = 'New LT Debt'

#cash_bal.columns = add_cols
#cash_bal.head()

mat_stdebt.columns = add_cols
mat_stdebt.head()

new_stdebt.columns = add_cols
new_stdebt.head()

cap_ex.columns = add_cols
cap_ex.head()

lt_invest.columns = add_cols
lt_invest.head()

new_equity.columns = add_cols
new_equity.head()

new_ltdebt.columns = add_cols
new_ltdebt.head()

#cash_bal.style.format('${:,.2f}')
#mat_stdebt.style.format('${:,.2f}')
#new_stdebt
#cap_ex.style.format('${:,.2f}')
#lt_invest.style.format('${:,.2f}')
#new_equity.style.format('${:,.2f}')
#new_ltdebt.style.format('${:,.2f}')