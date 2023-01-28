# This module calculates values for fixed assets variables required for projections.

import numpy as np
import pandas as pd
import numpy_financial as npf


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


# pro_equip.style.format('${:,.2f}') # this is total equipment value
pro_furfix.style.format('${:,.2f}') # this is total furniture & fixture value
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