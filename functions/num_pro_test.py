# This is module 1

from pathlib import Path, PureWindowsPath
import numpy as np
import pandas as pd
import numpy_financial as npf

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
wage_assum['Tot_Mon_Wage'] = np.where(wage_assum['Pay_base'] == 'A', wage_assum['Sal_Amt']/12 * (1 + wage_assum['Fringe_Rate']),\
                                      wage_assum['Sal_Amt'] * 40 * 4.33 * (1 + wage_assum['Fringe_Rate']))
debt_assum['Tot_Mon_DebtSer'] = -npf.pmt(debt_assum.Int_Rate/12, debt_assum.Term * 12, debt_assum.Loan_Amt)

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

beg_cash = cash_proForma
mincash_bal = workcap_assum.loc['Cash', 'Min_Cash_Bal']
print(beg_cash)
print(mincash_bal)

#runfile('num_pro_test_1.py')
#exec(open("num_pro_test_1.py").read())




#workcap_assum
#prepaid_assum
#equipur_assum
#offpur_assum
#furpur_assum
#conlea_assum
#orgcost_assum
#deppd_assum
#debt_assum
#equity_assum
#sales_assum
#operexp_assum
#wage_assum

#tot_wage
#tot_operexp
#tot_debtser
#tot_work_cap
#start_inv
#tot_prepaid
#tot_equipur
#tot_offpur
#tot_furpur
#tot_conlea
#tot_softcosts
#tot_deppd
#tot_debt
#implied_equity
#tot_uses
#equity_proForma
#cash_proForma

#print(f'{cashflow_stmt:.2f}')

