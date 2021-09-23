#%%
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
df_dynare = pd.read_excel('C:\dataPJ\DB_q.xlsx')
df_dynare = df_dynare.set_index('DATE') #indexを設定
#最終何期を落とすか決める
df_dynare = df_dynare[:-2]
#df_dynare = df_dynare[:-7]

# Dynare用データの成形
#前年比をとる
df_dynare["pi_obs"] = df_dynare["pi_obs"]/df_dynare["pi_obs"].shift(4)*100-100
df_dynare["cpi_obs"] = df_dynare["cpi_obs"]/df_dynare["cpi_obs"].shift(4)*100-100

#冒頭１年を落とす（前年比をとったため）
df_dynare = df_dynare[4:]

#HP Filter
Ccycle, Ctrend = sm.tsa.filters.hpfilter(df_dynare["c_obs"], 1600)
Icycle, Itrend = sm.tsa.filters.hpfilter(df_dynare["i_obs"], 1600)
Wcycle, Wtrend = sm.tsa.filters.hpfilter(df_dynare["w_obs"], 1600)
Ncycle, Ntrend = sm.tsa.filters.hpfilter(df_dynare["n_obs"], 1600)
Bcycle, Btrend = sm.tsa.filters.hpfilter(df_dynare["b_obs"], 1600)
Gcycle, Gtrend = sm.tsa.filters.hpfilter(df_dynare["g_obs"], 1600)

#HP CycleのTrendからの乖離率を算出
df_dynare["c_obs"] = Ccycle/Ctrend*100
df_dynare["i_obs"] = Icycle/Itrend*100
df_dynare["w_obs"] = Wcycle/Wtrend*100
df_dynare["n_obs"] = Ncycle/Ntrend*100
df_dynare["b_obs"] = Bcycle/Btrend*100
df_dynare["g_obs"] = Gcycle/Gtrend*100

#データの書き出し（dynareが読み込むようindexは削除）
df_dynare.to_excel('C:\dataPJ\dynare_sim\DB_dynare.xlsx', index=False, float_format='%.2f')
print("Dynare_DBの書き出しが完了しました！")

#############################################
print("描画を行います！")
#############################################
# %%  GDP vs Consumtion
fig = plt.figure()
plt.plot(df_dynare["y_obs"],label="GDP",color ="deepskyblue")
plt.plot(df_dynare["c_obs"],label="Consumption",color ="darkorange")
plt.axhline(y=0,color ="black", lw=0.5)
plt.legend(loc = 'lower left')
plt.show()
fig.savefig('graph\YvsC.png', dpi = 1000)
# %%  GDP vs Investment
fig = plt.figure()
plt.plot(df_dynare["y_obs"],label="GDP",color ="deepskyblue")
plt.plot(df_dynare["i_obs"],label="Investment",color ="darkorange")
plt.axhline(y=0,color ="black", lw=0.5)
plt.legend(loc = 'lower right')
plt.show()
fig.savefig('graph\YvsI.png', dpi = 1000)
# %%  Wage vs Labor
fig = plt.figure()
plt.plot(df_dynare["w_obs"],label="Wage",color ="deepskyblue")
plt.plot(df_dynare["n_obs"],label="Labor",color ="darkorange")
plt.axhline(y=0,color ="black", lw=0.5)
plt.legend(loc = 'lower left')
plt.show()
fig.savefig('graph\WvsN.png', dpi = 1000)
# %% Taylor rule
fig = plt.figure()
df_dynare['MODEL'] = 0.5*df_dynare["y_obs"] + 1.5 * df_dynare["pi_obs"]
plt.plot(df_dynare["MODEL"],label="Taylor Rule",color ="deepskyblue")
plt.plot(df_dynare["r_obs"],label="FF RATE",color ="darkorange")
plt.axhline(y=0,color ="black", lw=0.5)
plt.legend(loc = 'lower left')
plt.show()
fig.savefig('graph\TaylorRule.png', dpi = 1000)
# %%
