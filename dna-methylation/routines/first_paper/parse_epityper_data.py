import pandas as pd

data_file_path = 'D:/Aaron/Bio/epityper/'
data_file_name = 'PRR4.txt'

df = pd.read_csv(data_file_path + data_file_name, sep='\t')
col_names = df.columns.values
col_names[0] = 'ID_REF'
df.columns = col_names
sample_ids = list(df.ID_REF)
for item in sample_ids:
    indexes = [i for i,d in enumerate(list(df.ID_REF)) if d==item]
    if len(indexes) > 1:
        count = 1
        for index in indexes:
            df['ID_REF'][index] += '_' + str(count)
            count += 1

df = df[df['ID_REF'].notnull()]
df = df[df['Age'].notnull()]
df = df[df['Sex'].notnull()]

df_control = df[df['Group'] == 'Control']
obs_control = pd.DataFrame(
    {'sample_id': list(df_control.ID_REF),
     'Sex': list(df_control.Sex),
     'Age': list(df_control.Age)
    })
df_control = df_control.T
df_control.drop(df_control.tail(4).index,inplace=True)

df_centenarian = df[df['Group'] == 'Centenarian']
obs_centenarian = pd.DataFrame(
    {'sample_id': list(df_centenarian.ID_REF),
     'Sex': list(df_centenarian.Sex),
     'Age': list(df_centenarian.Age)
    })
df_centenarian = df_centenarian.T
df_centenarian.drop(df_centenarian.tail(4).index,inplace=True)

df_down = df[df['Group'] == 'Down']
obs_down = pd.DataFrame(
    {'sample_id': list(df_down.ID_REF),
     'Sex': list(df_down.Sex),
     'Age': list(df_down.Age)
    })
df_down = df_down.T
df_down.drop(df_down.tail(4).index,inplace=True)

df_offspring = df[df['Group'] == 'Offspring']
obs_offspring = pd.DataFrame(
    {'sample_id': list(df_offspring.ID_REF),
     'Sex': list(df_offspring.Sex),
     'Age': list(df_offspring.Age)
    })
df_offspring = df_offspring.T
df_offspring.drop(df_offspring.tail(4).index,inplace=True)

df_control.to_csv(data_file_path + data_file_name[:-4] + '_data_control.txt', header=None, index=True, sep='\t', na_rep="NA")
df_centenarian.to_csv(data_file_path + data_file_name[:-4] + '_data_centenarian.txt', header=None, index=True, sep='\t', na_rep="NA")
df_down.to_csv(data_file_path + data_file_name[:-4] + '_data_down.txt', header=None, index=True, sep='\t', na_rep="NA")
df_offspring.to_csv(data_file_path + data_file_name[:-4] + '_data_offspring.txt', header=None, index=True, sep='\t', na_rep="NA")

obs_control.to_csv(data_file_path + data_file_name[:-4] + '_obs_control.txt', header=True, index=None, sep='\t', na_rep="NA")
obs_centenarian.to_csv(data_file_path + data_file_name[:-4] + '_obs_centenarian.txt', header=True, index=None, sep='\t', na_rep="NA")
obs_down.to_csv(data_file_path + data_file_name[:-4] + '_obs_down.txt', header=True, index=None, sep='\t', na_rep="NA")
obs_offspring.to_csv(data_file_path + data_file_name[:-4] + '_obs_offspring.txt', header=True, index=None, sep='\t', na_rep="NA")