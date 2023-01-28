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

proann_incstmt.style.format('${:,.2f}')