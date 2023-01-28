# This module creates the projected income statement based on the schedules created above.

proinc_stmt = pd.DataFrame()

proinc_stmt = proinc_stmt.append(pro_sales)
proinc_stmt = proinc_stmt.append(pro_cogs)
proinc_stmt = proinc_stmt.append(pro_gross)
proinc_stmt = proinc_stmt.append(proop_exp)
proinc_stmt = proinc_stmt.append(pro_ebit)

#incomestmt = proinc_stmt.copy()
proinc_stmt = proinc_stmt.append(cash_flow.loc['IntExp'])

proinc_stmt = proinc_stmt.append(pro_netinc.iloc[-1])

proinc_stmt.index.name = 'Projected Income Statement'

proinc_stmt.style.format('${:,.2f}')



#incomestmt.style.format('${:,.2f}')
#proinc_stmt.index.name = 'Projected Income STMT'
proinc_stmt.style.format('${:,.2f}')
#proinc_stmt = proinc_stmt.append(pro_gross.iloc[-1])
#proinc_stmt