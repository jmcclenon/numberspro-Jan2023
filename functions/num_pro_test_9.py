#This code creates Current Assets less cash schedule for use in cash flow statement

curr_ass = pd.DataFrame()
curr_liab = pd.DataFrame()
chg_currass = pd.DataFrame()
chg_currliab = pd.DataFrame()

curr_ass = curr_ass.append(pro_acctsrec)
curr_ass = curr_ass.append(pro_inven)
curr_ass = curr_ass.append(pro_prepaidbal)

totcurr_ass = curr_ass.sum()
totcurr_ass.name = 'Current less cash'
curr_ass = curr_ass.append(totcurr_ass.transpose())

chg_curass = curr_ass.loc['Current less cash'].diff()
chg_curass.name = 'Chg in Assets'
curr_ass = curr_ass.append(-chg_curass.transpose())
curr_ass.index.name = 'Curr Assets Chg'


curr_liab = curr_liab.append(pro_acctspay)
curr_liab = curr_liab.append(pro_wagespay)

totcurr_liab = curr_liab.sum()
totcurr_liab.name = 'Current Liab.'
curr_liab = curr_liab.append(totcurr_liab.transpose())

chg_currliab = curr_liab.loc['Current Liab.'].diff()
chg_currliab.name = 'Chg in Liab.'
curr_liab = curr_liab.append(chg_currliab.transpose())
curr_liab.index.name = 'Curr Liab. Chg'
#chg_currliab.at['Chg in Liab.', 'ProForma'] = 0

#totcurr_liab
#chg_curliab

#curr_ass.style.format('${:,.2f}')
#curr_liab.style.format('${:,.2f}')
#chg_currass.style.format('${:,.2f}')