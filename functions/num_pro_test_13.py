# This code calculates income before taxes and retained earnings

net_inc = pd.DataFrame()
pro_netinc = pd.DataFrame()
incB4_tax = pd.DataFrame()
inc_B4tax = pd.DataFrame()
testcum = pd.DataFrame(index = ['Retained Earnings'])


net_inc = pro_ebit.iloc[-1] + cash_flow.loc['IntExp']
net_inc.name = 'Income before Tax'
pro_netinc = pro_netinc.append(net_inc.transpose())
incB4_tax = pro_netinc.iloc[-1]
incB4_tax.cumsum()
inc_B4tax = inc_B4tax.append(incB4_tax.transpose())

testcum = inc_B4tax.cumsum(axis =1)
test_cum = testcum.copy()
test_cum.index = ['Retained Earnings']



#pro_ebit.style.format('${:,.2f}')
#pro_netinc.style.format('${:,.2f}')
#print(incB4_tax)
#incB4_tax
#inc_B4tax.style.format('${:,.2f}')
#testcum.style.format('${:,.2f}')
#test_cum.style.format('${:,.2f}')