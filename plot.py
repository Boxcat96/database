#%%
import pandas as pd
import matplotlib.pyplot as plt
df_q = pd.read_excel('C:\dataPJ\DB_q.xlsx')
df_q = df_q.set_index('DATE') #indexを設定
# %%  GDP vs Consumtion
fig = plt.figure()
plt.plot(df_q["y_obs"],label="GDP",color ="darkorange")
plt.axhline(y=0,color ="black", lw=0.5)
#plt.legend(loc = 'lower left')
plt.show()
fig.savefig('graph\GDP.png')
# %%
