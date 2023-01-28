# This code creates the balance sheet

addbal_rows = balance_sheet.index

bal_sheet = pd.DataFrame()

bal_sheet = bal_sheet.append(cash_flow.iloc[-1])
bal_sheet = bal_sheet.append(pro_acctsrec)
bal_sheet = bal_sheet.append(pro_inven)
bal_sheet = bal_sheet.append(pro_prepaidbal)
totcurrass = bal_sheet.loc['CashBal': 'Insurance'].sum()
totcurrass.name = 'Total Current Assets'
bal_sheet = bal_sheet.append(totcurrass.transpose())
bal_sheet = bal_sheet.append(pro_fixass.iloc[-1])
bal_sheet = bal_sheet.append(pro_cons.iloc[-1])
bal_sheet = bal_sheet.append(-pro_deprebal.iloc[-1])
netfixedass = bal_sheet.loc['Total Fixed Assets': 'Accumulated Depreciation'].sum()
netfixedass.name = 'Net Fixed Assets'
bal_sheet = bal_sheet.append(netfixedass.transpose())
bal_sheet = bal_sheet.append(pro_netorg.iloc[-1])
bal_sheet = bal_sheet.append(pro_othass.iloc[-2])
totalassets = bal_sheet.loc['Net Fixed Assets': 'Total Other Assets'].sum() + bal_sheet.loc['Total Current Assets']
totalassets.name = 'Total Assets'
bal_sheet = bal_sheet.append(totalassets.transpose())

bal_sheet = bal_sheet.append(pro_wagespay.iloc[-1])
bal_sheet = bal_sheet.append(pro_acctspay)
bal_sheet = bal_sheet.append(cash_flow.loc['ReqSTD'])
bal_sheet = bal_sheet.append(curpor_debt.iloc[-3])
bal_sheet = bal_sheet.append(curpor_debt.iloc[-2])
totcurrliab = bal_sheet.loc['Wages Payable': 'Cur Chase'].sum()
totcurrliab.name = 'Total Current Liabilities'
bal_sheet = bal_sheet.append(totcurrliab.transpose())
bal_sheet = bal_sheet.append(ltpor_debt.iloc[-3])
bal_sheet = bal_sheet.append(ltpor_debt.iloc[-2])
totalliab = bal_sheet.loc['Total Current Liabilities': 'LT Chase'].sum()
totalliab.name = 'Total Liabilities'
bal_sheet = bal_sheet.append(totalliab.transpose())
bal_sheet = bal_sheet.append(pro_equity)
bal_sheet = bal_sheet.append(test_cum)
totalequity = bal_sheet.loc['Owners Equity': 'Retained Earnings'].sum()
totalequity.name = 'Total Equity'
bal_sheet = bal_sheet.append(totalequity.transpose())

totalliabequity = bal_sheet.loc['Total Liabilities'] + bal_sheet.loc['Total Equity']
totalliabequity.name = 'Total Liabilities Equity'
bal_sheet = bal_sheet.append(totalliabequity.transpose())




#bal_sheet = proinc_stmt.append(pro_cogs)
#bal_sheet = proinc_stmt.append(pro_cogs)

#bal_sheet = proinc_stmt.append(pro_cogs)

bal_sheet.style.format('${:,.2f}')
