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
# pro_curltdebt.style.format('${:,.2f}')
# pro_ltdebt.style.format('${:,.2f}')
# curpor_debt.style.format('${:,.2f}')
# ltpor_debt.style.format('${:,.2f}')
