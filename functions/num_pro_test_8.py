# This code calculates balance sheet working capital balances.
pro_cash = pd.DataFrame()
pro_acctsrec = pd.DataFrame()
pro_inven = pd.DataFrame()
pro_acctspay = pd.DataFrame()
pro_wagespay = pd.DataFrame()
pro_equity = pd.DataFrame(index = ['Owners Equity'], columns = proop_exp.columns)

# This code calculates the projected cash balances.

# This code calculates the projected accounts receivable balances.
ending_arbal = (pro_sales.iloc[-1] * workcap_assum.iloc[2, 3]) / ((365/workcap_assum.iloc[2, 5])/12)
ending_arbal.name = "Accts Rec. Balance"
pro_acctsrec = pro_acctsrec.append(ending_arbal.transpose())

# This code calculates the projected inventory balances.
ending_invbal = pro_cogs.iloc[-1] / ((365/workcap_assum.iloc[3, 5])/12)
ending_invbal.name = "Inventory"
pro_inven = pro_inven.append(ending_invbal.transpose())
pro_inven.iat[0, 0] = workcap_assum.iloc[3, 1]

# This code calculates the projected accounts payable balances.
ending_apbal = (pro_cogs.iloc[-1] * workcap_assum.iloc[4, 3]) / ((365/workcap_assum.iloc[4, 5])/12)
ending_apbal.name = "Accts Pay. Balance"
pro_acctspay = pro_acctspay.append(ending_apbal.transpose())

# This code calculates the projected wages payable balances.
ending_wagespay = (pro_wages.iloc[-1] + pro_fringes.iloc[-1]) / ((365/workcap_assum.iloc[5, 5])/12)
ending_wagespay.name = "Wages Payable"
pro_wagespay = pro_wagespay.append(ending_wagespay.transpose())

# This code calculates opening equity balances
for b, col in pro_equity.iteritems():
    pro_equity.loc['Owners Equity', b] = equity_proForma



#ending_arbal
# print commands
#pro_acctsrec.style.format('${:,.2f}')
#pro_inven.style.format('${:,.2f}')
#pro_acctspay.style.format('${:,.2f}')
#pro_wagespay.style.format('${:,.2f}')
#pro_equity.style.format('${:,.2f}')
#equity_proForma
#print(addto)