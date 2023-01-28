# This module calculates the monthly prepaid expense. this shit works.

pro_prepaidexp = pd.DataFrame()
pro_prepaidadd = pd.DataFrame()
pro_prepaidbal = pd.DataFrame()

multipliers = range(0, 55, 1)
for i in multipliers:
    if i == 0:
        pro_prepaidadd[f'ProForma'] = prepaid_assum['Costs']

    else:
        pro_prepaidadd[f'per_{i}'] = np.where((i / 12 <= 1) & (i % 12 == 0),
                                              prepaid_assum['Costs'] * (1 + prepaid_assum['Inf_Rate']), \
                                              np.where((i / 12 <= 2) & (i % 12 == 0),
                                                       prepaid_assum['Costs'] * ((1 + prepaid_assum['Inf_Rate']) ** 2), \
                                                       np.where((i / 12 <= 3) & (i % 12 == 0),
                                                                prepaid_assum['Costs'] * (
                                                                            (1 + prepaid_assum['Inf_Rate']) ** 3), \
                                                                np.where((i / 12 <= 4) & (i % 12 == 0),
                                                                         prepaid_assum['Costs'] * ((1 + prepaid_assum[
                                                                             'Inf_Rate']) ** 4), \
                                                                         np.where((i / 12 <= 5) & (i % 12 == 0),
                                                                                  prepaid_assum['Costs'] * ((1 +
                                                                                                             prepaid_assum[
                                                                                                                 'Inf_Rate']) ** 5), \
                                                                                  0)))))

    if i == 0:
        pro_prepaidexp[f'ProForma'] = prepaid_assum['Adjuster']



    elif i <= 12:
        pro_prepaidexp[f'per_{i}'] = prepaid_assum['Costs'] / 12

    else:
        pro_prepaidexp[f'per_{i}'] = pro_prepaidexp.iloc[:, i - 12] * (1 + prepaid_assum['Inf_Rate'])

pro_prepaidexp.index.name = 'PrePaid Balance'
pro_prepaidexp.style.format('${:,.2f}')

pro_prepaidadd.index = prepaid_assum.index

pro_prepaidadd.index.name = 'PrePaid Payments'

pro_prepaidbal = pro_prepaidadd.cumsum(axis=1) - pro_prepaidexp.cumsum(axis=1)

pro_prepaidbal.index.name = 'PrePaid Balance'

# Print commands
# pro_prepaidexp.style.format('${:,.2f}') # monthly prepaid expenses
pro_prepaidadd.style.format('${:,.2f}') # annual additions to prepaid
# pro_prepaidbal.style.format('${:,.2f}') # monthly prepaid balance sheet balance