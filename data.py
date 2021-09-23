#%%
%matplotlib inline
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import pandas_datareader.data as pdr
import datetime

#取得するデータの開始日と最終日を設定
start = datetime.datetime(1979,1,1)
end = datetime.datetime(2019,12,31)

#取得するデータを設定

#四半期（実質）
y = pdr.DataReader('GDPC1', 'fred', start, end)
ypot = pdr.DataReader('GDPPOT', 'fred', start, end)
c = pdr.DataReader('A794RX0Q048SBEA', 'fred', start, end)
i = pdr.DataReader('GPDIC1', 'fred', start, end)
w = pdr.DataReader('LES1252881600Q', 'fred', start, end)
pi = pdr.DataReader('DPCERD3Q086SBEA', 'fred', start, end)
r  = pdr.DataReader('BOGZ1FL072052006Q', 'fred', start, end)

#月次
n = pdr.DataReader('CIVPART', 'fred', start, end)
cpi = pdr.DataReader('USACPIALLMINMEI', 'fred', start, end)
epi = pdr.DataReader('MICH', 'fred', start, end)
gpi = pdr.DataReader('CPIFABSL', 'fred', start, end)
lead = pdr.DataReader('USSLIND', 'fred', start, end)
coincidence = pdr.DataReader('USPHCI', 'fred', start, end)
m_supply = pdr.DataReader('M2SL', 'fred', start, end)
interest_rate = pdr.DataReader('INTDSRUSM193N', 'fred', start, end)
employment = pdr.DataReader('PAYEMS', 'fred', start, end)
sentiment = pdr.DataReader('UMCSENT', 'fred', start, end)

#日次
yield_ten  = pdr.DataReader('DGS10', 'fred', start, end)
yield_three  = pdr.DataReader('DGS3MO', 'fred', start, end)
SP_stock  = pdr.DataReader('SP500', 'fred', start, end)
nasdaq100  = pdr.DataReader('NASDAQ100', 'fred', start, end)
oilprice = pdr.DataReader('DCOILWTICO', 'fred', start, end)
breakeven_ten = pdr.DataReader('T10YIE', 'fred', start, end)
nikkei225  = pdr.DataReader('NIKKEI225', 'fred', start, end) #JAPAN
jpusrate =  pdr.DataReader('DEXJPUS', 'fred', start, end) 

print("データ取得が完了しました！")
# %%
#データファイルを作成
df = pd.DataFrame(index = y.index)
df['y_raw'] = y
df['ypot'] = ypot
df['y_obs'] =  (df["y_raw"]-df["ypot"])/df["ypot"]*100 #需給ギャップ
df['c_raw'] = c
df['i_raw'] = i
df['w_raw'] = w
df['pi_raw'] = pi
df['r_raw'] = r
print("データファイルを作成しました！")
# %%
#HP Filter
Ccycle, Ctrend = sm.tsa.filters.hpfilter(df.c_raw, 1600)
Wcycle, Wtrend = sm.tsa.filters.hpfilter(df.ｗ_raw, 1600)
Icycle, Itrend = sm.tsa.filters.hpfilter(df.i_raw, 1600)
print("HP Filterをかけました！")
#%%
#モデル推計用のファイル作成<df1>
df1 = pd.DataFrame(index = ypot.index)
df1['y_obs'] =  (df["y_raw"]-df["ypot"])/df["ypot"]*100 #需給ギャップ
df1["c_obs"] = Ccycle/Ctrend*100
df1["i_obs"] = Icycle/Itrend*100
df1["w_obs"] = Wcycle/Wtrend*100
df1["pi_obs"] = df["pi_raw"]/df["pi_raw"].shift(4)*100-100 #前年比
df1["r_obs"] = df["r_raw"] 
df1 = df1[4:]
df1.head()
# %%
