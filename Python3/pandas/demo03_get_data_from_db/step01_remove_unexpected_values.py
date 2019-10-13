import pandas as pd

def get_exception_indexes(df):
    indexes_removed = set()
    df_age = df[df['Age'].apply(lambda x: x < 0 or str(x) in ('', 'nan'))]['Age']
    indexes_removed.update(list(df_age.index.values))
    df_duplicated_ids = df[df.duplicated(subset=['id'], keep=False)]
    df_duplicated_group = df_duplicated_ids.groupby('id')
    for id in df_duplicated_group.groups.keys():
        indexes_removed.update(df_duplicated_group.groups[id])
    return list(indexes_removed)

if __name__=='__main__':
    df_output_user = pd.read_excel('output_user.xlsx', sheet_name='Data')
    index_removed = get_exception_indexes(df_output_user)

    df_output_user_removed = df_output_user.iloc[index_removed]
    df_output_user_keeped = df_output_user.drop(index=index_removed)

    writer = pd.ExcelWriter('output_user.removed.xlsx', engine='openpyxl')
    df_output_user_keeped.to_excel(writer, sheet_name='Data', index=False)
    df_output_user_removed.to_excel(writer, sheet_name='Removed', index=False)
    writer.save()