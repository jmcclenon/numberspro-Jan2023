# This code calculates projected Other Assets values for the balance sheet.

pro_othass = pd.DataFrame()

multipliers = range(0, 55, 1)
for i in multipliers:
    if i < 1:
        pro_othass[f'ProForma'] = deppd_assum['Amount']

    else:
        pro_othass[f'per_{i}'] = deppd_assum['Amount']

pro_othass.index.name = 'Other Assets'
pro_othass.loc['Total Other Assets'] = pro_othass.sum(numeric_only=True, axis=0)

chg_othass = pro_othass.loc['Total Other Assets'].diff()
chg_othass.name = 'Chg Oth. Assets'
pro_othass = pro_othass.append(-chg_othass.transpose())
pro_othass.index.name = 'Other Assets Chg'

# pro_othass.style.format('${:,.2f}')