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
            print(cash_flow.at[j, i])

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
            print(cash_gen)
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