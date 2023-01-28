# this code calculates projected operating account values.
pro_sales = pd.DataFrame()
gross_profit = pd.DataFrame()
pro_gross = pd.DataFrame()
pro_wages = pd.DataFrame()
pro_fringes = pd.DataFrame()
pro_operexp = pd.DataFrame()
pro_merbkfees = pd.DataFrame()
pro_othinc = pd.DataFrame()
proop_exp = pd.DataFrame()
totop_exp = pd.DataFrame()
cash_exp = pd.DataFrame()
pro_cashexp = pd.DataFrame()
ebit = pd.DataFrame()

multipliers = range(0, 55, 1)
for i in multipliers:
    if i < 1:
        pro_sales[f'ProForma'] = sales_assum['ProForma']
        pro_wages[f'ProForma'] = wage_assum['ProForma']

    else:
        pro_sales[f'per_{i}'] = sales_assum['Max_Mon_Sls'] * (1 - np.exp(-i * sales_assum['Grow_Con']))
        pro_wages[f'per_{i}'] = np.where(i < wage_assum['Per_hired'], 0, np.where((i < wage_assum['Per_fulltime']) & \
                                                                                  (wage_assum['Pay_base'] == 'A'),
                                                                                  (wage_assum['Sal_Amt'] / 12) * .5, \
                                                                                  np.where((i < wage_assum[
                                                                                      'Per_fulltime']) & (wage_assum[
                                                                                                              'Pay_base'] == 'H'), \
                                                                                           wage_assum[
                                                                                               'Sal_Amt'] * 40 * 4.33 * .5,
                                                                                           np.where((i >= wage_assum[
                                                                                               'Per_fulltime']) & \
                                                                                                    (wage_assum[
                                                                                                         'Pay_base'] == 'A'),
                                                                                                    (wage_assum[
                                                                                                         'Sal_Amt'] / 12), \
                                                                                                    np.where((i >=
                                                                                                              wage_assum[
                                                                                                                  'Per_fulltime']) & (
                                                                                                                         wage_assum[
                                                                                                                             'Pay_base'] == 'H'), \
                                                                                                             wage_assum[
                                                                                                                 'Sal_Amt'] * 40 * 4.33,
                                                                                                             1)))))

#    pro_fringes[f'period_{i}'] =

multipliers = range(0, 55, 1)
for i in multipliers:
    if i < 1:
        pro_operexp[f'ProForma'] = operexp_assum['ProForma']

    elif ((i > 0) and (i <= 12)):
        pro_operexp[f'per_{i}'] = operexp_assum['Exp_Amt']

    else:
        pro_operexp[f'per_{i}'] = pro_operexp.iloc[:, i - 13] * (1 + operexp_assum['Inf_Rate'])

multipliers = range(0, 55, 1)
for i in multipliers:
    if i < 1:
        pro_othinc[f'ProForma'] = deppd_assum['ProForma']

    else:
        pro_othinc[f'per_{i}'] = deppd_assum['Amount'] * (-deppd_assum['Rate_Earned'] / 12)

# This code creates the sales projections from the sales assumptions.
pro_sales.index.name = 'Projected Sales'
pro_sales.loc['Tot_Sales'] = pro_sales.sum()

# This code creates the COGS projections from the COGS assumptions.
cogs = sales_assum.iloc[:, 2]
pro_cogs = pro_sales.iloc[0:len(pro_sales.index) - 1].mul(cogs, axis=0)
# pro_cogs = pro_sales.iloc[0:2].mul(cogs, axis = 0)
pro_cogs.index.name = 'Projected COGS'
pro_cogs.loc['Total COGS'] = pro_cogs.sum(numeric_only=True, axis=0)

# This code creates the gross profit projections based on the sales and COGS schedules created above.
gross_profit = pro_sales.loc['Tot_Sales'] - pro_cogs.loc['Total COGS']
# gross_profit = pro_sales.iloc[-1] - pro_cogs.iloc[-1]
gross_profit.name = 'Gross Profit'
pro_gross = pro_gross.append(gross_profit.transpose())

# This code creates the wage projections based on the wage assumptions.
pro_wages.index = wage_assum.index
pro_wages.index.name = 'Projected Salaries & Wages'
pro_wages.loc['Total Wages'] = pro_wages.sum(numeric_only=True, axis=0)

fringe_rate = wage_assum.loc['Owner', 'Fringe_Rate']
fringes = pro_wages.loc['Total Wages'] * fringe_rate
fringes.name = 'Fringe Benefits'
pro_fringes = pro_fringes.append(fringes.transpose())

# This code creates the operating costs projections based on the operating costs assumptions.
pro_operexp.index.name = 'Projected Operating Costs'

# This code creates the merchant banking fees projections based on the wage assumptions.
# ccshr_sales = workcap_assum.iloc[0, 3]
# merbk_fees = workcap_assum.iloc[0, 4]
merbkfees = pro_sales.iloc[-1] * workcap_assum.iloc[0, 3] * workcap_assum.iloc[0, 4]
merbkfees.name = "Mer Bank Fees"
pro_merbkfees = pro_merbkfees.append(merbkfees.transpose())

# This code creates the Other Income projections based on the deposit assumptions.
pro_othinc.index.name = 'Projected Other Income'
pro_othinc.loc['Total Other Inc'] = pro_othinc.sum(numeric_only=True, axis=0)

# This code creates the total operating expense projections based on the operating schedules created above.
proop_exp = proop_exp.append(pro_wages.iloc[-1])
proop_exp = proop_exp.append(pro_fringes)
proop_exp = proop_exp.append(pro_operexp)
proop_exp = proop_exp.append(pro_merbkfees)
proop_exp = proop_exp.append(pro_othinc.iloc[-1])
proop_exp = proop_exp.append(pro_prepaidexp)
proop_exp = proop_exp.append(pro_deprebalto)
proop_exp = proop_exp.append(pro_monamor)
totop_exp = proop_exp.sum()
totop_exp.name = 'Tot Operating Expenses'
proop_exp = proop_exp.append(totop_exp.transpose())
proop_exp.index.name = 'Operating Expenses'

cash_exp = proop_exp.loc['Total Wages': 'Insurance'].sum()
cash_exp.name = 'Cash Expense'
pro_cashexp = pro_cashexp.append(cash_exp.transpose())

# ebit
# totop_exp
# gross_profit
# fringes
# print commands
# pro_sales.style.format('${:,.2f}')
# pro_cogs.style.format('${:,.2f}')
# pro_gross.style.format('${:,.2f}')
# pro_wages.style.format('${:,.2f}')
# pro_fringes.style.format('${:,.2f}')
# pro_operexp.style.format('${:,.2f}')
# pro_merbkfees.style.format('${:,.2f}')
# pro_othinc.style.format('${:,.2f}')
# proop_exp.style.format('${:,.2f}')
# pro_cashexp.style.format('${:,.2f}')