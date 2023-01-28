# Authored by Sydney Wayman, copyright June 24, 2022
# The following code is used to load start-up data from files to create dataframes for variable catagories and
# intial variable values.

# New structure of model is based on calculating proforma balance sheet (sources and uses). Working capital use value
# is now based on a set number of months of cash operating expenses and debt service. Because of this, the model has to
# calculate these values first. This means the income statement variables have to be calculated first.


from pathlib import Path, PureWindowsPath
import numpy as np
import pandas as pd
import numpy_financial as npf

# This statement is setting the float format for displaying float values in pandas to display them in dollar format Z # with no decimal places. The '.format' at the end of the statement is used to specify the format of the float values. # The '${:,.0f}' part specifies that the float values should be formatted as dollar values with no decimal places.
pd.options.display.float_format = '${:,.0f}'.format
#pd.set_option('display.max_columns', None)




orgcost_assum = pd.read_csv('datafiles/orgcost_assum.csv', index_col='Organizational Costs')
equipur_assum = pd.read_csv('datafiles/equipur_assum.csv', index_col='Equipment Purchases')
furpur_assum = pd.read_csv('datafiles/furpur_assum.csv', index_col='Furniture & Fixtures')
offpur_assum = pd.read_csv('datafiles/offpur_assum.csv', index_col='Office Equipment')
conlea_assum = pd.read_csv('datafiles/conlea_assum.csv', index_col='Leasehold Improvements')
prepaid_assum = pd.read_csv('datafiles/prepaid_assum.csv', index_col='PrePaid Expenses')
deppd_assum = pd.read_csv('datafiles/deppd_assum.csv', index_col='Deposits Paid')
workcap_assum = pd.read_csv('datafiles/workcap_assum.csv', index_col='Working Capital Assumptions')
sales_assum = pd.read_csv('datafiles/sales_assum.csv', index_col='Product')
operexp_assum = pd.read_csv('datafiles/operexp_assum.csv', index_col='Operating Expenses')
wage_assum = pd.read_csv('datafiles/wage_assum.csv', index_col='Salaries & Wages')
debt_assum = pd.read_csv('datafiles/debt_assum.csv', index_col='Lenders')
equity_assum = pd.read_csv('datafiles/equity_assum.csv', index_col='Opening Equity')
cashprep_stmt = pd.read_csv('datafiles/cashprep_stmt.csv', index_col='Cash Prep Statement')
cashflow_stmt = pd.read_csv('datafiles/cashflow_stmt.csv', index_col='Cash Flow Statement')
balance_sheet = pd.read_csv('datafiles/balance_sheet.csv', index_col='Balance Sheet')
income_stmt = pd.read_csv('datafiles/income_stmt.csv', index_col='Income Statement')

# The following code adds common variables to the _assum dataframe
prepaid_assum['Prepaid_Exp'] = (prepaid_assum['Costs'] / 12)
equipur_assum['Depreciation'] = (equipur_assum['Costs'] / (equipur_assum['Use_Life'] * 12)) * equipur_assum['Qty_Pur']
equipur_assum['Tot_Costs'] = equipur_assum['Costs'] * equipur_assum['Qty_Pur']
furpur_assum['Depreciation'] = (furpur_assum['Costs'] / (furpur_assum['Use_Life'] * 12)) * furpur_assum['Qty_Pur']
furpur_assum['Tot_Costs'] = furpur_assum['Costs'] * furpur_assum['Qty_Pur']
offpur_assum['Depreciation'] = (offpur_assum['Costs'] / (offpur_assum['Use_Life'] * 12)) * offpur_assum['Qty_Pur']
offpur_assum['Tot_Costs'] = offpur_assum['Costs'] * offpur_assum['Qty_Pur']
conlea_assum['Depreciation'] = (conlea_assum['Costs'] / (conlea_assum['Use_Life'] * 12))
orgcost_assum['Amortization'] = (orgcost_assum['Costs'] / (orgcost_assum['Use_Life'] * 12))
wage_assum['Tot_Mon_Wage'] = np.where(wage_assum['Pay_base'] == 'A',
wage_assum['Sal_Amt'] / 12 * (1 + wage_assum['Fringe_Rate']), \
wage_assum['Sal_Amt'] * 40 * 4.33 * (1 + wage_assum['Fringe_Rate']))
debt_assum['Tot_Mon_DebtSer'] = -npf.pmt(debt_assum.Int_Rate / 12, debt_assum.Term * 12, debt_assum.Loan_Amt)

# This code creates Sources/Uses values
tot_wage = wage_assum.Tot_Mon_Wage.sum()
tot_operexp = operexp_assum.Exp_Amt.sum()
tot_debtser = debt_assum.Tot_Mon_DebtSer.sum()
tot_debt = debt_assum.Loan_Amt.sum()
tot_work_cap = tot_wage + tot_operexp + tot_debtser
start_inv = workcap_assum.loc['Inventory', 'Open_Bal']
tot_prepaid = prepaid_assum.Costs.sum()
tot_equipur = equipur_assum.Tot_Costs.sum()
tot_offpur = offpur_assum.Tot_Costs.sum()
tot_furpur = furpur_assum.Tot_Costs.sum()
tot_conlea = conlea_assum.Costs.sum()
tot_orgcost = orgcost_assum.Costs.sum()
tot_deppd = deppd_assum.Amount.sum()
tot_debtser = debt_assum.Tot_Mon_DebtSer.sum()
implied_equity = tot_work_cap + start_inv + tot_prepaid + tot_equipur + tot_offpur + tot_furpur + tot_conlea + tot_orgcost \
                 + tot_deppd - tot_debt
tot_uses = tot_work_cap + start_inv + tot_prepaid + tot_equipur + tot_offpur + tot_furpur + tot_conlea + tot_orgcost \
           + tot_deppd
equity_proForma = np.where(implied_equity > 0, tot_uses - tot_debt, .2 * tot_debt)
cash_proForma = np.where(implied_equity > 0, tot_work_cap, equity_proForma - tot_debt)

# workcap_assum
# prepaid_assum
# equipur_assum
# offpur_assum
# furpur_assum
# conlea_assum
# orgcost_assum
# deppd_assum
# debt_assum
# equity_assum
# sales_assum
# operexp_assum
# wage_assum

# tot_wage
# tot_operexp
# tot_debtser
# tot_work_cap
# start_inv
# tot_prepaid
# tot_equipur
# tot_offpur
# tot_furpur
# tot_conlea
# tot_softcosts
# tot_deppd
# tot_debt
# implied_equity
# tot_uses
# equity_proForma
# cash_proForma

#cashflow_stmt

# this was added to module 1 in pycharm

beg_cash = cash_proForma
mincash_bal = workcap_assum.loc['Cash', 'Min_Cash_Bal']
#print(beg_cash)
#print(mincash_bal)

# This module calculates values for fixed assets variables required for projections.

pro_equipdepre = pd.DataFrame()
pro_furfixdepre = pd.DataFrame()
pro_offequdepre = pd.DataFrame()
pro_consdepre = pd.DataFrame()

pro_equip = pd.DataFrame()
pro_furfix = pd.DataFrame()
pro_offequ = pd.DataFrame()
pro_cons = pd.DataFrame()

pro_fixass = pd.DataFrame()
fixed_assets = pd.DataFrame()
# add_toobalto = pd.DataFrame()
mon_depre = pd.DataFrame()
# add_toobal = pd.DataFrame()
accum_depre = pd.DataFrame()
pro_deprebalto = pd.DataFrame()
pro_deprebal = pd.DataFrame()
gross_netfixed = pd.DataFrame()
pro_netfixed = pd.DataFrame()

multipliers = range(0, 55, 1)
for i in multipliers:

    if i < 1:
        pro_equipdepre[f'ProForma'] = equipur_assum['Adjuster']
        pro_furfixdepre[f'ProForma'] = furpur_assum['Adjuster']
        pro_offequdepre[f'ProForma'] = offpur_assum['Adjuster']
        pro_consdepre[f'ProForma'] = conlea_assum['Adjuster']

        pro_equip[f'ProForma'] = (equipur_assum['Costs'] * equipur_assum['Qty_Pur'])
        pro_furfix[f'ProForma'] = (furpur_assum['Costs'] * furpur_assum['Qty_Pur'])
        pro_offequ[f'ProForma'] = (offpur_assum['Costs'] * offpur_assum['Qty_Pur'])
        pro_cons[f'ProForma'] = (conlea_assum['Costs'])

    else:
        pro_equipdepre[f'per_{i}'] = equipur_assum['Depreciation']
        pro_furfixdepre[f'per_{i}'] = furpur_assum['Depreciation']
        pro_offequdepre[f'per_{i}'] = offpur_assum['Depreciation']
        pro_consdepre[f'per_{i}'] = conlea_assum['Depreciation']

        pro_equip[f'per_{i}'] = (equipur_assum['Costs'] * equipur_assum['Qty_Pur'])
        pro_furfix[f'per_{i}'] = (furpur_assum['Costs'] * furpur_assum['Qty_Pur'])
        pro_offequ[f'per_{i}'] = (offpur_assum['Costs'] * offpur_assum['Qty_Pur'])
        pro_cons[f'per_{i}'] = (conlea_assum['Costs'])

# This code creates the depreciation expense projections based on the fixed asset assumptions.
pro_equipdepre.index = equipur_assum.index
pro_equipdepre.index.name = 'Projected Equip Depre Expense'
pro_equipdepre.loc['Total Equip Depre'] = pro_equipdepre.sum(numeric_only=True, axis=0)

# This code creates the depreciation expense projections based on the fixed asset assumptions.
pro_furfixdepre.index = furpur_assum.index
pro_furfixdepre.index.name = 'Projected Fur Fix Depre Expense'
pro_furfixdepre.loc['Total Fur & Fix Depre'] = pro_furfixdepre.sum(numeric_only=True, axis=0)

# This code creates the depreciation expense projections based on the fixed asset assumptions.
pro_offequdepre.index = offpur_assum.index
pro_offequdepre.index.name = 'Projected Off Equip Depre Expense'
pro_offequdepre.loc['Total Off Equip Depre'] = pro_offequdepre.sum(numeric_only=True, axis=0)

# This code creates the depreciation expense projections based on the leasehold improvement assumptions.
pro_consdepre.index = conlea_assum.index
pro_consdepre.index.name = 'Projected Leasehold Depre Expense'
pro_consdepre.loc['Total Leasehold Depre'] = pro_consdepre.sum(numeric_only=True, axis=0)

# This code calculates total equipment balance for balance sheet.
pro_equip.index = equipur_assum.index
pro_equip.index.name = 'Equipment'
pro_equip.loc['Total Equipment'] = pro_equip.sum(numeric_only=True, axis=0)

# This code calculates total furniture & fixtures balance for balance sheet.
pro_furfix.index = furpur_assum.index
pro_furfix.index.name = 'Furniture & Fixtures'
pro_furfix.loc['Total Furniture & Fixtures'] = pro_furfix.sum(numeric_only=True, axis=0)

# This calculates total office equipment balance for balance sheet.
pro_offequ.index = offpur_assum.index
pro_offequ.index.name = 'Office Equipment'
pro_offequ.loc['Total Office Equipment'] = pro_offequ.sum(numeric_only=True, axis=0)

# This code calculates total leasehold improvements balance for balance sheet.
pro_cons.index = conlea_assum.index
pro_cons.index.name = 'Leasehold Improvements'
pro_cons.loc['Total Leasehold Improvements'] = pro_cons.sum(numeric_only=True, axis=0)

# This code creates the Fixed Assets balance for the balance sheet.
fixed_assets = pro_equip.iloc[-1] + pro_furfix.iloc[-1] + pro_offequ.iloc[-1]  # + pro_cons.iloc[-1]
fixed_assets.name = 'Total Fixed Assets'
pro_fixass = pro_fixass.append(fixed_assets.transpose())

# This code calculates the accumulated Depreciation balance sheet balance.
mon_depre = pro_equipdepre.iloc[-1] + pro_furfixdepre.iloc[-1] + pro_offequdepre.iloc[-1] + pro_consdepre.iloc[-1]
mon_depre.name = 'Monthly Depre'
pro_deprebalto = pro_deprebalto.append(mon_depre.transpose())
accum_depre = pro_equipdepre.iloc[-1] + pro_furfixdepre.iloc[-1] + pro_offequdepre.iloc[-1] + pro_consdepre.iloc[-1]
accum_depre = accum_depre.cumsum()
accum_depre.name = 'Accumulated Depreciation'
pro_deprebal = pro_deprebal.append(accum_depre.transpose())

# This code calculates net fixed assets balance for balance sheet.
gross_netfixed = pro_fixass.iloc[-1] - pro_deprebal.iloc[-1]
gross_netfixed.name = 'Net Fixed Assets'
pro_netfixed = pro_netfixed.append(gross_netfixed.transpose())

# above is good!!!

# Print commands
# pro_equipdepre.style.format('${:,.2f}') # this is monthly equipment depreciation
# pro_furfixdepre.style.format('${:,.2f}') # this is monthly furniture & fixture depreciation
# pro_offequdepre.style.format('${:,.2f}') # this is monthly office equipment depreciation
# pro_consdepre.style.format('${:,.2f}') # this is monthly leasehold depreciation


pro_equip.style.format('${:,.2f}')  # this is total equipment value
# pro_furfix.style.format('${:,.2f}') # this is total furniture & fixture value
# pro_offequ.style.format('${:,.2f}') # this is total office equipment value
# pro_cons.style.format('${:,.2f}') # this is total leasehold value

# pro_fixass.style.format('${:,.2f}') # this is total fixed assets
# pro_deprebalto.style.format('${:,.2f}') # this is monthly depreciation
# pro_deprebal.style.format('${:,.2f}') # this is accumulated depreciation
# pro_netfixed.style.format('${:,.2f}') # this is total net fixed assets

# mon_depre
# pro_mondepre.style.format('${:,.2f}') # monthly total depreciation
# pro_netfixed.style.format('${:,.2f}') # total assets

# print(fixed_assets) # series of total fixed assets
# print(accum_depre) # series of monthly total depreciation
# print(gross_netfixed) # series of fixed assets value after 1 month of depre

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
# pro_prepaidadd.style.format('${:,.2f}') # annual additions to prepaid
# pro_prepaidbal.style.format('${:,.2f}') # monthly prepaid balance sheet balance

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

# this module calculates projected interest expense and principal account values.
pro_intexp = pd.DataFrame()
pro_prin = pd.DataFrame()
pro_loanbal = pd.DataFrame()
curltdebt_pro = pd.DataFrame()
pro_curltdebt = pd.DataFrame()
pro_ltdebt = pd.DataFrame()

multipliers = range(0, 55, 1)
for i in multipliers:
    if i == 0:
        pro_intexp[f'ProForma'] = debt_assum['Adjuster']
        pro_prin[f'ProForma'] = debt_assum['Adjuster']
        pro_loanbal[f'ProForma'] = debt_assum['Loan_Amt']


    else:
        pro_intexp[f'per_{i}'] = -npf.ipmt(debt_assum.Int_Rate / 12, i, debt_assum.Term * 12, debt_assum.Loan_Amt)
        pro_prin[f'per_{i}'] = -npf.ppmt(debt_assum.Int_Rate / 12, i, debt_assum.Term * 12, debt_assum.Loan_Amt)
        pro_loanbal[f'per_{i}'] = debt_assum['Loan_Amt'] * ((((1 + (debt_assum['Int_Rate'] / 12)) ** (
                    debt_assum['Term'] * 12)) - ((1 + (debt_assum['Int_Rate'] / 12)) ** i)) \
                                                            / ((1 + (debt_assum['Int_Rate'] / 12)) ** (
                            debt_assum['Term'] * 12) - 1))

# This code creates the interest expense projections based on the loan assumptions.
pro_intexp.index = ['SBA', 'Chase']
pro_intexp.index.name = 'Projected Interest Expense'
pro_intexp.loc['Total Interest Expense'] = pro_intexp.sum(numeric_only=True, axis=0)

# This code creates the principal payments projections based on the loan assumptions.
pro_prin.index = ['SBA', 'Chase']
pro_prin.index.name = 'Projected Principal Payments'
pro_prin.loc['Total Principal Payments'] = pro_prin.sum(numeric_only=True, axis=0)

# This code creates the ending loan balance projections based on the loan assumptions.
pro_loanbal.index = ['SBA', 'Chase']
pro_loanbal.index.name = 'Loan Balance'
pro_loanbal.loc['Total'] = pro_loanbal.sum(numeric_only=True, axis=0)

# This code creates the current portion ltd balance sheet projections based on the loan assumptions.
curltdebt_pro = curltdebt_pro.append(pro_prin.loc['SBA'].transpose())
curltdebt_pro = curltdebt_pro.append(pro_prin.loc['Chase'].transpose())
# print(curltdebt_pro)

multipliers = range(0, 55, 1)

for i in multipliers:
    #    pro_curltdebt[f'Period_{i}'] = curltdebt_pro.iloc[:, i+1:i+13].sum(axis=1)
    if i == 0:
        pro_curltdebt[f'ProForma'] = curltdebt_pro.iloc[:, i + 1:i + 13].sum(axis=1)

    else:
        pro_curltdebt[f'per_{i}'] = curltdebt_pro.iloc[:, i + 1:i + 13].sum(axis=1)

# pro_curltdebt.index = debt_assum.index
pro_curltdebt.index.name = 'Cur Port LTD'
pro_curltdebt.index = ['SBA', 'Chase']
pro_curltdebt.loc['Total'] = pro_curltdebt.sum(numeric_only=True, axis=0)

# This code creates the non-current portion ltd balance sheet projections based on the loan assumptions.
# pro_ltloanbal_copy = pro_loanbal.copy()
# pro_curltdebt_copy = pro_curltdebt.copy()
# pro_ltdebt.index = debt_assum.index
pro_ltdebt.index.name = 'Non-Cur Debt'
pro_ltdebt = pro_loanbal - pro_curltdebt

curpor_debt = pro_curltdebt.copy()
curpor_debt.index = ['Cur SBA', 'Cur Chase', 'Total Current']
ltpor_debt = pro_ltdebt.copy()
ltpor_debt.index = ['LT SBA', 'LT Chase', 'Total NonCurrent']

# print commands
# pro_intexp.style.format('${:,.2f}')
# pro_prin.style.format('${:,.2f}')
# pro_loanbal.style.format('${:,.2f}')
pro_curltdebt.style.format('${:,.2f}')
# pro_ltdebt.style.format('${:,.2f}')
# curpor_debt.style.format('${:,.2f}')
# ltpor_debt.style.format('${:,.2f}')

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

# this module calculates EBIT & Net Income

ebit = pd.DataFrame()
pro_ebit = pd.DataFrame()
net_inc = pd.DataFrame()
pro_netinc = pd.DataFrame()
incB4_tax = pd.DataFrame()
inc_B4tax = pd.DataFrame()
testcum = pd.DataFrame(index=['Retained Earnings'])

ebit = pro_gross.iloc[-1] - proop_exp.iloc[-1]
ebit.name = 'EBIT'
ebit.index.name = 'Ebit'
pro_ebit = pro_ebit.append(ebit.transpose())

# ebit
# pro_ebit.style.format('${:,.2f}')
# pro_netinc.style.format('${:,.2f}')
# print(incB4_tax)
# incB4_tax
# inc_B4tax.style.format('${:,.2f}')
# testcum.style.format('${:,.2f}')
# test_cum.style.format('${:,.2f}')

# This code calculates balance sheet working capital balances.
pro_cash = pd.DataFrame()
pro_acctsrec = pd.DataFrame()
pro_inven = pd.DataFrame()
pro_acctspay = pd.DataFrame()
pro_wagespay = pd.DataFrame()
pro_equity = pd.DataFrame(index=['Owners Equity'], columns=proop_exp.columns)

# This code calculates the projected cash balances.

# This code calculates the projected accounts receivable balances.
ending_arbal = (pro_sales.iloc[-1] * workcap_assum.iloc[2, 3]) / ((365 / workcap_assum.iloc[2, 5]) / 12)
ending_arbal.name = "Accts Rec. Balance"
pro_acctsrec = pro_acctsrec.append(ending_arbal.transpose())

# This code calculates the projected inventory balances.
ending_invbal = pro_cogs.iloc[-1] / ((365 / workcap_assum.iloc[3, 5]) / 12)
ending_invbal.name = "Inventory"
pro_inven = pro_inven.append(ending_invbal.transpose())
pro_inven.iat[0, 0] = workcap_assum.iloc[3, 1]

# This code calculates the projected accounts payable balances.
ending_apbal = (pro_cogs.iloc[-1] * workcap_assum.iloc[4, 3]) / ((365 / workcap_assum.iloc[4, 5]) / 12)
ending_apbal.name = "Accts Pay. Balance"
pro_acctspay = pro_acctspay.append(ending_apbal.transpose())

# This code calculates the projected wages payable balances.
ending_wagespay = (pro_wages.iloc[-1] + pro_fringes.iloc[-1]) / ((365 / workcap_assum.iloc[5, 5]) / 12)
ending_wagespay.name = "Wages Payable"
pro_wagespay = pro_wagespay.append(ending_wagespay.transpose())

# This code calculates opening equity balances
for b, col in pro_equity.iteritems():
    pro_equity.loc['Owners Equity', b] = equity_proForma

# ending_arbal
# print commands
# pro_acctsrec.style.format('${:,.2f}')
# pro_inven.style.format('${:,.2f}')
# pro_acctspay.style.format('${:,.2f}')
# pro_wagespay.style.format('${:,.2f}')
# pro_equity.style.format('${:,.2f}')
# equity_proForma
# print(addto)

# This code creates Current Assets less cash schedule for use in cash flow statement

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
# chg_currliab.at['Chg in Liab.', 'ProForma'] = 0

# totcurr_liab
# chg_curliab

# curr_ass.style.format('${:,.2f}')
# curr_liab.style.format('${:,.2f}')
# chg_currass.style.format('${:,.2f}')

add_cols = proop_exp.columns
add_rows = cashflow_stmt.index
# column_headers = pro_sales.columns.values.tolist()
# add_cols = proop_exp.columns
# add_rows = cashprep_stmt.index

# print(column_headers)
#print(add_cols)
#print(add_rows)

# This code creates holding rows for variables that may be used in the future.

mat_stdebt = pd.DataFrame(np.zeros((1, 55)))
new_stdebt = pd.DataFrame(np.zeros((1, 55)))
cap_ex = pd.DataFrame(np.zeros((1, 55)))
lt_invest = pd.DataFrame(np.zeros((1, 55)))
new_equity = pd.DataFrame(np.zeros((1, 55)))
new_ltdebt = pd.DataFrame(np.zeros((1, 55)))

mat_stdebt.index = ['Mat of ST Debt']

cap_ex.index = ['Capital Expenditures']
# cap_ex.index.name = 'CAP EX'

lt_invest.index = ['LT Investment']
# lt_invest.index.name = 'LT Investment'

new_equity.index = ['New Equity']
# new_equity.index.name = 'New Equity'

new_ltdebt.index = ['New LT Debt']
# new_ltdebt.index.name = 'New LT Debt'

# cash_bal.columns = add_cols
# cash_bal.head()

mat_stdebt.columns = add_cols
mat_stdebt.head()

new_stdebt.columns = add_cols
new_stdebt.head()

cap_ex.columns = add_cols
cap_ex.head()

lt_invest.columns = add_cols
lt_invest.head()

new_equity.columns = add_cols
new_equity.head()

new_ltdebt.columns = add_cols
new_ltdebt.head()

# cash_bal.style.format('${:,.2f}')
# mat_stdebt.style.format('${:,.2f}')
# new_stdebt
# cap_ex.style.format('${:,.2f}')
# lt_invest.style.format('${:,.2f}')
# new_equity.style.format('${:,.2f}')
# new_ltdebt.style.format('${:,.2f}')

# This code creates the cashflow statement, calculates the short term debt, and calculates cash generated.


cash_flow = pd.DataFrame(index=add_rows, columns=add_cols)

for i, col in cash_flow.iteritems():

    for j, row in cash_flow.iterrows():

        if i == 'ProForma' and j == 'CashBal':
            cash_flow.at[j, i] = cash_proForma

        elif i == 'ProForma':
            cash_flow.at[j, i] = 0

        elif j == 'Sales':
            cash_flow.at[j, i] = pro_sales.at['Tot_Sales', i]
        #            print(cash_flow.at[j, i])

        elif j == 'OperExp':
            cash_flow.at[j, i] = -pro_cogs.at['Total COGS', i] - pro_cashexp.at['Cash Expense', i]
        #            print(cash_flow.at[j, i])

        elif j == 'OperCashFlow':
            cash_flow.at[j, i] = cash_flow.loc['Sales':'OperExp', i].sum()
        #            print(cash_flow.at[j, i])

        elif j == 'ChgCurAss':
            cash_flow.at[j, i] = curr_ass.at['Chg in Assets', i]
        #            print(cash_flow.at[j, i])

        elif j == 'ChgCurLiab':
            cash_flow.at[j, i] = curr_liab.at['Chg in Liab.', i]
        #            print(cash_flow.at[j, i])

        elif j == 'NetOperCash':
            cash_flow.at[j, i] = cash_flow.loc['OperCashFlow':'ChgCurLiab', i].sum()
        #            print(cash_flow.at[j, i])

        elif j == 'IntExp':
            cash_flow.at[j, i] = -pro_intexp.at['Total Interest Expense', i] - \
                                 (cash_flow.iat[cash_flow.index.get_loc('ReqSTD'), (cash_flow.columns.get_loc(i) - 1)] * \
                                  (workcap_assum.at['STD', 'Int_Rate'] / 12))  # correct this
        #            print(cash_flow.at[j, i])

        elif j == 'CashAftFinCosts':
            cash_flow.at[j, i] = cash_flow.loc['NetOperCash':'IntExp', i].sum()
        #            print(cash_flow.at[j, i])

        elif j == 'MatLTD':
            cash_flow.at[j, i] = -pro_prin.at['Total Principal Payments', i]
        #            print(cash_flow.at[j, i])

        elif j == 'MatSTD':
            cash_flow.at[j, i] = -cash_flow.iat[
                cash_flow.index.get_loc('ReqSTD'), (cash_flow.columns.get_loc(i) - 1)]  # check this
        #            print(cash_flow.at[j, i])

        elif j == 'CashAftDebtSer':
            cash_flow.at[j, i] = cash_flow.loc['CashAftFinCosts':'MatSTD', i].sum()
        #            print(cash_flow.at[j, i])

        elif j == 'CapEx':
            cash_flow.at[j, i] = -cap_ex.at['Capital Expenditures', i]
        #            print(cash_flow.at[j, i])

        elif j == 'NewLTInv':
            cash_flow.at[j, i] = -lt_invest.at['LT Investment', i]
        #            print(cash_flow.at[j, i])

        elif j == 'ChgOthAss':
            cash_flow.at[j, i] = pro_othass.at['Chg Oth. Assets', i]
        #            print(cash_flow.at[j, i])

        elif j == 'CashSur(Def)':
            cash_flow.at[j, i] = cash_flow.loc['CashAftDebtSer':'ChgOthAss', i].sum()
        #    print(cash_flow.at[j, i])

        elif j == 'NewEquity':
            cash_flow.at[j, i] = new_equity.at['New Equity', i]
        #            print(cash_flow.at[j, i])

        elif j == 'NewLTD':  # check this
            cash_flow.at[j, i] = new_ltdebt.at['New LT Debt', i]
            cashB4_std = cash_flow.loc['CashSur(Def)':'NewLTD', i].sum()
        #            print(cash_flow.at[j, i])
        #            print(cashB4_std)

        elif j == 'ReqSTD':  # check this
            cash_flow.at[j, i] = np.where(cash_flow.iat[cash_flow.index.get_loc('CashBal'), (
                        cash_flow.columns.get_loc(i) - 1)] + cashB4_std - mincash_bal >= 0, \
                                          0, abs(cash_flow.iat[cash_flow.index.get_loc('CashBal'), (
                            cash_flow.columns.get_loc(i) - 1)] + cashB4_std - mincash_bal))

        elif j == 'TotExtFin':
            cash_flow.at[j, i] = cash_flow.loc['NewEquity':'ReqSTD', i].sum()
        #            print(cash_flow.at[j, i])

        elif j == 'NetCashGen':
            cash_gen = cash_flow.loc['CashSur(Def)', i] + cash_flow.loc['TotExtFin', i]
        #    print(cash_gen)
            cash_flow.at[j, i] = cash_gen
        #            print(beg_cash)

        #            cash_flow.at[j, i] = cash_flow.loc['NewEquity':'ReqSTD', m].sum()
        #            print(cash_flow.at[j, i])

        elif j == 'CashBal':  # need to check this
            cash_flow.at[j, i] = cash_flow.iat[
                                     cash_flow.index.get_loc('CashBal'), (cash_flow.columns.get_loc(i) - 1)] + cash_gen
#            print(cash_flow.at[j, i])


# .style.format('${:,.2f}')
# cashpro1
# cash_bal.style.format('${:,.2f}')
# cap_ex
cash_flow.style.format('${:,.2f}')
# print(cash_workshe)
# print(cashpro1)

# This code calculates income before taxes and retained earnings

net_inc = pd.DataFrame()
pro_netinc = pd.DataFrame()
incB4_tax = pd.DataFrame()
inc_B4tax = pd.DataFrame()
testcum = pd.DataFrame(index=['Retained Earnings'])

net_inc = pro_ebit.iloc[-1] + cash_flow.loc['IntExp']
net_inc.name = 'Income before Tax'
pro_netinc = pro_netinc.append(net_inc.transpose())
incB4_tax = pro_netinc.iloc[-1]
incB4_tax.cumsum()
inc_B4tax = inc_B4tax.append(incB4_tax.transpose())

testcum = inc_B4tax.cumsum(axis=1)
test_cum = testcum.copy()
test_cum.index = ['Retained Earnings']

# pro_ebit.style.format('${:,.2f}')
# pro_netinc.style.format('${:,.2f}')
# print(incB4_tax)
# incB4_tax
# inc_B4tax.style.format('${:,.2f}')
# testcum.style.format('${:,.2f}')
# test_cum.style.format('${:,.2f}')

# This module creates the projected income statement based on the schedules created above.

proinc_stmt = pd.DataFrame()

proinc_stmt = proinc_stmt.append(pro_sales)
proinc_stmt = proinc_stmt.append(pro_cogs)
proinc_stmt = proinc_stmt.append(pro_gross)
proinc_stmt = proinc_stmt.append(proop_exp)
proinc_stmt = proinc_stmt.append(pro_ebit)

# incomestmt = proinc_stmt.copy()
proinc_stmt = proinc_stmt.append(cash_flow.loc['IntExp'])

proinc_stmt = proinc_stmt.append(pro_netinc.iloc[-1])

proinc_stmt.index.name = 'Projected Income Statement'

proinc_stmt.style.format('${:,.2f}')

# incomestmt.style.format('${:,.2f}')
# proinc_stmt.index.name = 'Projected Income STMT'
#proinc_stmt.style.format('${:,.2f}')
print(proinc_stmt)
# proinc_stmt = proinc_stmt.append(pro_gross.iloc[-1])
# proinc_stmt

# This code calculates annual projected income statements

proann_incstmt = pd.DataFrame()

multipliers = range(1, 5, 1)

for i in multipliers:
    if i == 1:
        proann_incstmt[f'Year_{i}'] = proinc_stmt.iloc[:, 1:13].sum(axis=1)

    elif i == 2:
        proann_incstmt[f'Year_{i}'] = proinc_stmt.iloc[:, 13:25].sum(axis=1)

    elif i == 3:
        proann_incstmt[f'Year_{i}'] = proinc_stmt.iloc[:, 25:37].sum(axis=1)

    elif i == 4:
        proann_incstmt[f'Year_{i}'] = proinc_stmt.iloc[:, 38:49].sum(axis=1)

#proann_incstmt.style.format('${:,.2f}')
print(proann_incstmt)

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

# bal_sheet = proinc_stmt.append(pro_cogs)
# bal_sheet = proinc_stmt.append(pro_cogs)
# bal_sheet = proinc_stmt.append(pro_cogs)

#pd.set_option('expand_frame_repr', False)
print(bal_sheet)
#print(f'{bal_sheet:.2f}')
#bal_sheet.format("${:,.2f}")
#print(bal_sheet.style.format('${:,.2f}'))