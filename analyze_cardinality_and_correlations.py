for col in df.columns:
    print(f'Column {col} has cardinality {len(df[col].unique())}')
    
def print_high_correlations(df, corr_method='pearson', sample_size=500000, threshold=0.005):
    subset = df.sample(min(sample_size, len(df)))
    corrs = {}
    for i, row in subset.corr(method=corr_method).iterrows():
        row = pd.DataFrame(row)
        ans = list(row[np.abs(row[i])>=threshold].index)
        if len(ans) > 1:
            ans.remove(i)
            corrs[i] = ans
    return corrs
                       
corr_dict = print_high_correlations(df, 'spearman', 0.15)