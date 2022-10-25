# dataframes train, test
from sklearn.preprocessing import OneHotEncoder
onehot_features = ['col1', 'col2', 'col3']
onehotter = OneHotEncoder(handle_unknown='infrequent_if_exist', min_frequency=0.005, drop='if_binary')
onehotter.fit(train[onehot_features])

onehot_data = onehotter.transform(train[onehot_features]).toarray()
onehot_columns = onehotter.get_feature_names_out([x for x in onehot_features])
onehot_data = pd.DataFrame(onehot_data, columns=onehot_columns)
train = train.drop(columns=onehot_features)
train = train.join(onehot_data)