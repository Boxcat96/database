#%%
import pandas as pd
import pandas_datareader.data as pdr
import datetime
import time
# 処理前の時刻
t1 = time.time() 
print("モジュールの読み込みが完了しました！")

#%% ファイルを開く
input_file_name = 'C:\dataPJ\datacode.xlsx' #パスを設定してください
input_book = pd.ExcelFile(input_file_name)
input_sheet_name = input_book.sheet_names
sheet_q = input_book.parse(input_sheet_name[0]) #quarterly シート
sheet_m = input_book.parse(input_sheet_name[1]) #monthly シート
sheet_d = input_book.parse(input_sheet_name[2]) #daily シート
code_q = sheet_q["code"]
code_m = sheet_m["code"]
code_d = sheet_d["code"]
print("シートの読み込みが完了しました！")
#%%
#取得するデータの開始日と最終日を設定
start = datetime.datetime(1979,1,1) #データの始期
end = datetime.date.today () 
#end = datetime.datetime(2019,12,31) #データの終期
#################################

#取得するデータを設定
#四半期
df_q = pdr.DataReader(code_q, 'fred', start, end)
df_q.columns = sheet_q["notation"]
df_q["y_obs"] = (df_q["y_raw"]-df_q["ypot"])/df_q["ypot"]*100
# 月次
df_m = pdr.DataReader(code_m, 'fred', start, end)
df_m.columns = sheet_m["notation"]

# 日次
df_d = pdr.DataReader(code_d, 'fred', start, end)
df_d.columns = sheet_d["notation"]

print("データの読み込みが完了しました！")
# %%  
#月次データを四半期化
df_q_m = df_m.resample(rule="QS").mean()

#日次データを四半期化
df_q_d = df_d.resample(rule="QS").mean()

#日次データを月次化
df_m_d = df_d.resample(rule="MS").mean()

#データの結合
df_q_merge_raw = pd.merge(df_q, df_q_m, on = 'DATE')
df_q_merge = pd.merge(df_q_merge_raw, df_q_d, on = 'DATE')
df_m_merge = pd.merge(df_m, df_m_d, on = 'DATE')

#データの書き出し
df_q_merge.to_excel('C:\dataPJ\DB_q.xlsx', sheet_name = 'quarterly')
df_m_merge.to_excel('C:\dataPJ\DB_m.xlsx', sheet_name = 'monthly')
df_d.to_excel('C:\dataPJ\DB_d.xlsx', sheet_name = 'daily')
print("DBの書き出しが完了しました！")
# %%
# 処理時間
t2 = time.time()
elapsed_time = t2-t1
print(f"経過時間：{elapsed_time}")
