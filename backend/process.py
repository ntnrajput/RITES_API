import pandas as pd

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
