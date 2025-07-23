import pandas as pd
import os

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# file_path = os.path.join(BASE_DIR, 'downloads', 'unv_chem.xlsx')
# file_path_csv = os.path.join(BASE_DIR, 'downloads', 'merged_shift_chem_2025-07-17.xlsx')

def process_data_fwt(df):
    df['SHIFT'] = 'A'
    df['HEAT_JUDGMENT_DT'] = pd.to_datetime(df['HEAT_JUDGMENT_DT'].astype(str), format='%Y%m%d').dt.strftime('%d/%m/%Y')
    df['HEAT_NO'] = df['HEAT_NO'].str[1:]
    df['MILL'] = df['MILL'].str.strip()
    desired_order = ['TEST_NAME','HEAT_JUDGMENT_DT', 'SHIFT', 'HEAT_NO', 'LOT_NO', 'SMS', 'MILL', 'RAIL_GRADE','SECTION','STRAND_NO','DEFLECTION_MM','REMARKS','HEAT_STATUS']
    df = df[desired_order]
    df_rsm = df[df['MILL'] == 'RSM'].reset_index(drop=True)
    df_urm = df[df['MILL'] == 'URM'].reset_index(drop=True)
    return df_rsm, df_urm


def process_data_macro(df):
    df['SHIFT'] = 'A'
    df['HEAT_JUDGMENT_DT'] = pd.to_datetime(df['HEAT_JUDGMENT_DT'].astype(str), format='%Y%m%d').dt.strftime('%d/%m/%Y')
    df['HEAT_NO'] = df['HEAT_NO'].str[1:]
    df['MILL'] = df['MILL'].str.strip()
    desired_order = ['TEST_NAME','HEAT_JUDGMENT_DT', 'SHIFT', 'HEAT_NO', 'LOT_NO', 'SMS', 'MILL', 'RAIL_GRADE','SECTION','STRAND_NO','LIMIT_PRINT',  'SULPHUR_PRINT', 'VISUAL_EXAM','HEAT_STATUS']
    df = df[desired_order]
    df_rsm = df[df['MILL'] == 'RSM'].reset_index(drop=True)
    df_urm = df[df['MILL'] == 'URM'].reset_index(drop=True)
    return df_rsm, df_urm

def process_data_tensile(df):
    df['SHIFT'] = 'A'
    df['HEAT_JUDGMENT_DT'] = pd.to_datetime(df['HEAT_JUDGMENT_DT'].astype(str), format='%Y%m%d').dt.strftime('%d/%m/%Y')
    df['HEAT_NO'] = df['HEAT_NO'].str[1:]
    df['MILL'] = df['MILL'].str.strip()
    desired_order = ['TEST_NAME','HEAT_JUDGMENT_DT', 'SHIFT', 'HEAT_NO', 'LOT_NO', 'SMS', 'MILL', 'RAIL_GRADE','SECTION','STRAND_NO','YS_MPA_MIN550',  'UTS_MPA_MIN880', 'ELONGATION_MIN10','HARDNESS_BHN_260_300','REMARKS','HEAT_STATUS']
    df = df[desired_order]
    df_rsm = df[df['MILL'] == 'RSM'].reset_index(drop=True)
    df_urm = df[df['MILL'] == 'URM'].reset_index(drop=True)
    return df_rsm, df_urm


def process_data_chem(df):

    df_chem = df.copy()
    rearranged_group = [
        'C_RESULT', 'MN_RESULT', 'P_RESULT', 'S_RESULT', 'SI_RESULT', 'AL_RESULT', 'CR_RESULT', 'V_RESULT',
        'N_RESULT', 'H_RESULT', 'O_RESULT', 'CU_RESULT', 'NI_RESULT', 'MO_RESULT', 'NB_RESULT',
        'TI_RESULT', 'SB_RESULT', 'SN_RESULT', 'CT_RESULT', 'CMN_RESULT'
    ]
    cols = df_chem.columns.tolist()
    start, end = cols.index('C_RESULT'), cols.index('CMN_RESULT')
    df_chem = df_chem[
        cols[:start] + rearranged_group + cols[end+1:]
    ]
    df_chem ['HEAT_NO'] = df_chem['HEAT_NO'].str[1:]
    df_chem['P_key'] = df_chem['SMS'] + df_chem['MILL'] + df_chem['HEAT_NO'] 
    key_column = 'P_key'
    ladle_df = df_chem[df_chem['ANALYSIS'] == 'Ladle'].copy()
    ladle_df = ladle_df.set_index(key_column)
    ladle_df = ladle_df.add_suffix('_Ladle')
    columns_to_drop = [
        'ORD_Ladle', 'ANALYSIS_Ladle', 'RETEST_STEP_Ladle', 
        'TYPE_Ladle', 'LOT_NO_Ladle', 'STRAND_NO_Ladle', 
        'HEAT_NO_Ladle', 'MILL_Ladle', 'SMS_Ladle'
    ]
    ladle_df.insert(0, 'Test Name', 'Chemical')
    ladle_df.insert(1,'Heat_No.',ladle_df['HEAT_NO_Ladle'].values)
    ladle_df.insert(2,'SMS',ladle_df['SMS_Ladle'].values)
    ladle_df.insert(3,'Mill',ladle_df['MILL_Ladle'].values)
    ladle_df = ladle_df.drop(columns=columns_to_drop, errors='ignore')

    prod1_df = df_chem[(df_chem['ANALYSIS'] == 'Product') & (df_chem['LOT_NO'] == 1)].copy()
    prod1_df = prod1_df.set_index(key_column)
    prod1_df = prod1_df.add_suffix('_Prod1')
    columns_to_drop = [
        'ORD_Prod1', 'ANALYSIS_Prod1', 'RETEST_STEP_Ladle', 'H_RESULT_Prod1',	'O_RESULT_Prod1',
        'TYPE_Prod1', 'LOT_NO_Prod1', 'HEAT_NO_Prod1', 'MILL_Prod1', 'SMS_Prod1', 'REMARKS_Prod1', 'RETEST_STEP_Prod1'
    ]
    prod1_df = prod1_df.drop(columns=columns_to_drop,errors ='ignore')
    prod1_df = prod1_df[[prod1_df.columns[-1]] + prod1_df.columns[:-1].tolist()]

    prod2_df = df_chem[(df_chem['ANALYSIS'] == 'Product') & (df_chem['LOT_NO'] == 2)].copy()
    prod2_df = prod2_df.set_index(key_column)
    prod2_df = prod2_df.add_suffix('_Prod2')
    columns_to_drop = [
        'ORD_Prod2', 'ANALYSIS_Prod2', 'RETEST_STEP_Ladle', 'H_RESULT_Prod2',	'O_RESULT_Prod2',
        'TYPE_Prod2', 'LOT_NO_Prod2', 'HEAT_NO_Prod2', 'MILL_Prod2', 'SMS_Prod2', 'REMARKS_Prod2', 'RETEST_STEP_Prod2'
    ]
    prod2_df = prod2_df.drop(columns=columns_to_drop,errors ='ignore')
    prod2_df = prod2_df[[prod2_df.columns[-1]] + prod2_df.columns[:-1].tolist()]

    chem_df = ladle_df.join(prod1_df, how='left', rsuffix='_Prod1').join(prod2_df, how='left', rsuffix='_Prod2')
    chem_df = chem_df.reset_index()
    chem_df = chem_df[chem_df.columns[1:]]
    

    df_rsm = chem_df[chem_df['Mill'] == 'RSM'].reset_index(drop=True)
    df_urm = chem_df[chem_df['Mill'] == 'URM'].reset_index(drop=True)
    return df_rsm, df_urm



# df_chem = pd.read_excel(file_path)
# df_rsm, df_urm = process_data_chem(df_chem)
# df_urm.to_excel(file_path_csv)


# print(df_rsm)
# print(df_urm)

