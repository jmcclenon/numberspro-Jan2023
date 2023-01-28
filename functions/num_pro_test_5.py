# this module calculates values for organizational costs variables.
pro_orcostamor = pd.DataFrame()
pro_calmonamor = pd.DataFrame()
pro_monamor = pd.DataFrame()
add_tooamor = pd.DataFrame()
pro_orcost = pd.DataFrame()
gross_netorg = pd.DataFrame()
pro_netorg = pd.DataFrame()

multipliers = range(0, 55, 1)
for i in multipliers:
    if i == 0:
        pro_orcostamor[f'ProForma'] = orgcost_assum['Adjuster']
        pro_orcost[f'ProForma'] = (orgcost_assum['Costs'])

    else:
        pro_orcostamor[f'per_{i}'] = (orgcost_assum['Costs']) / (orgcost_assum['Use_Life'] * 12)
        pro_orcost[f'per_{i}'] = (orgcost_assum['Costs'])

pro_orcostamor.index = orgcost_assum.index
pro_orcostamor.index.name = 'Projected Org Cost Amortization'
pro_orcostamor.loc['Total Org Costs Amort'] = pro_orcostamor.sum(numeric_only=True, axis=0)
add_tooamor = pro_orcostamor.iloc[-1]
add_tooamor = add_tooamor.cumsum()

pro_calmonamor = pro_orcostamor.iloc[-1]

pro_monamor = pro_monamor.append(pro_calmonamor.transpose())

# This code Calculates the Organizational Costs balance sheet balance.
pro_orcost.index = orgcost_assum.index

pro_orcost.index.name = 'Organizational Costs'

pro_orcost.loc['Total Organizational Costs'] = pro_orcost.sum(numeric_only=True, axis=0)

gross_netorg = pro_orcost.iloc[-1] - add_tooamor

gross_netorg.name = 'Net Organizational Costs'

pro_netorg = pro_netorg.append(gross_netorg.transpose())

# Print commands
# pro_orcostamor.style.format('${:,.2f}') # detail monthly organizational costs
# add_tooamor
# pro_orcost.style.format('${:,.2f}') # detail of organizational costs
# pro_netorg.style.format('${:,.2f}') # organizational costs monthly balance sheet value
# print(gross_netorg)
# print(pro_calmonamor)
# print(pro_orcost.iloc[-1])
# pro_monamor.style.format('${:,.2f}') # monthly amortization expense