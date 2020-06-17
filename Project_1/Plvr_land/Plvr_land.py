import pandas as pd
import cn2an


def data(self):
    output = []
    res = list(df_all['總樓層數'])
    for i in res:
        if not i == 0:
            i = i.strip('層')
            output += [cn2an.transform(i)]
        elif i == 0:
            output += [0]
    return output


def a():
    df_filter_a = pd.read_csv('df_all.csv', header=[0, 1])
    filter_a = df_filter_a[(df_filter_a['主要用途']['main use'] == '住家用')
                           & (df_filter_a['建物型態']['building state'].str.contains('住宅大樓'))
                           & (df_filter_a['總樓層數']['total floor number'] >= 13)]
    filter_a.to_csv('filter_a.csv', index=False, encoding='utf_8_sig')


def b():
    df_filter_b = pd.read_csv('df_all.csv', header=[0, 1])
    total = [df_filter_b.shape[0]]
    df_filter_b['車位數量'] = df_filter_b['交易筆棟數']['transaction pen number'].str.split('車位').str.get(1)
    park = df_filter_b['車位數量'].astype(int).sum()
    total_price = df_filter_b['總價元']['total price NTD'].mean()
    park_price = df_filter_b['車位總價元']['the berth total price NTD'].sum() / park
    filter_b = pd.DataFrame({'總件數': total,
                             '總車位數': park,
                             '平均總價元': total_price,
                             '平均車位總價元': park_price})
    filter_b.to_csv('filter_b.csv', index=False, encoding='utf_8_sig')


if __name__ == '__main__':
    df_a = pd.read_csv('a_lvr_land_a.csv')
    df_b = pd.read_csv('b_lvr_land_a.csv', skiprows=[1])
    df_e = pd.read_csv('e_lvr_land_a.csv', skiprows=[1])
    df_f = pd.read_csv('f_lvr_land_a.csv', skiprows=[1])
    df_h = pd.read_csv('h_lvr_land_a.csv', skiprows=[1])
    df_all = pd.concat([df_a, df_b, df_e, df_f, df_h], axis=0)
    df_all['總樓層數'].fillna(value=0, inplace=True)
    df_all['總樓層數'] = df_all.apply(data, axis=0)
    df_all.to_csv('df_all.csv', index=False, encoding='utf_8_sig')
    a()
    b()
