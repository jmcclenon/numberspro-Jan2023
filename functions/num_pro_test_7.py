#this module calculates EBIT & Net Income

ebit = pd.DataFrame()
pro_ebit = pd.DataFrame()
net_inc = pd.DataFrame()
pro_netinc = pd.DataFrame()
incB4_tax = pd.DataFrame()
inc_B4tax = pd.DataFrame()
testcum = pd.DataFrame(index = ['Retained Earnings'])


ebit = pro_gross.iloc[-1] - proop_exp.iloc[-1]
ebit.name = 'EBIT'
ebit.index.name = 'Ebit'
pro_ebit = pro_ebit.append(ebit.transpose())

#ebit
#pro_ebit.style.format('${:,.2f}')
#pro_netinc.style.format('${:,.2f}')
#print(incB4_tax)
#incB4_tax
#inc_B4tax.style.format('${:,.2f}')
#testcum.style.format('${:,.2f}')
#test_cum.style.format('${:,.2f}')