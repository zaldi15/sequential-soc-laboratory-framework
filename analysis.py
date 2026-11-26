from pathlib import Path
import numpy as np,pandas as pd,sys
from sklearn.ensemble import RandomForestRegressor,ExtraTreesRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score
import matplotlib.pyplot as plt
out=Path(__file__).resolve().parent / 'results'
out.mkdir(exist_ok=True)
source=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent / 'data/ev_log.csv'
df=pd.read_csv(source)
df.columns=['time','speed','acceleration','voltage','current','power'];df=df.apply(pd.to_numeric).sort_values('time').reset_index(drop=True)
assert len(df)==7323 and not df.isna().any().any() and np.all(np.diff(df.time)==1)
dt=np.r_[0,np.diff(df.time)]; y=-100*df.current.to_numpy()*dt/(3600*2.5);soc=100+np.cumsum(y)
f=df[['speed','acceleration','voltage']];X=pd.concat([f,f.shift().fillna(f),f.rolling(5,min_periods=1).mean()],axis=1).to_numpy()
models={'Mean discharge rate':None,'Linear regression':LinearRegression(),'Random forest':RandomForestRegressor(n_estimators=200,min_samples_leaf=3,max_features=.8,random_state=42,n_jobs=2),'Extra trees':ExtraTreesRegressor(n_estimators=200,min_samples_leaf=3,max_features=.8,random_state=42,n_jobs=2),'KNN':make_pipeline(StandardScaler(),KNeighborsRegressor(n_neighbors=25,weights='distance'))}
cols=['Model','MAE (pp)','RMSE (pp)','R2','Final error (pp)','Increment MAE (pp)']
def run(a,b):
 rows=[];pred={}
 for name,m in models.items():
  yp=np.full(b-a,y[:a].mean()) if m is None else m.fit(X[:a],y[:a]).predict(X[a:b]);p=soc[a-1]+np.cumsum(yp);r=soc[a:b];pred[name]=p
  rows.append([name,mean_absolute_error(r,p),np.sqrt(mean_squared_error(r,p)),r2_score(r,p),p[-1]-r[-1],mean_absolute_error(y[a:b],yp)])
 return pd.DataFrame(rows,columns=cols),pred
s=int(len(df)*.8);m,p=run(s,len(df));m.to_csv(out/'holdout_metrics.csv',index=False);print('holdout',s,len(df)-s,soc[s-1],soc[-1]);print(m.to_string(index=False));print(df.describe());print('unique',df.voltage.nunique(),df.current.nunique(),'Ah',sum(df.current*dt)/3600,'Wh',sum(df.power*dt)/3600,'distance',sum(df.speed*dt)/3600)
folds=[]
for a,b in [(2929,3905),(3905,4881),(4881,5858)]:
 z,_=run(a,b);z.insert(0,'Train samples',a);z.insert(1,'Test samples',b-a);folds.append(z)
cv=pd.concat(folds);cv.to_csv(out/'rolling_origin_metrics.csv',index=False);summ=cv.groupby('Model',sort=False)[cols[1:]].agg(['mean','std']);summ.to_csv(out/'rolling_origin_summary.csv');print(summ.to_string())
absrows=[]
for name in ['Random forest','Extra trees','KNN']:
 model=models[name];q=model.fit(X[:s],soc[:s]).predict(X[s:]);absrows.append([name,mean_absolute_error(soc[s:],q),np.sqrt(mean_squared_error(soc[s:],q)),r2_score(soc[s:],q),q.min(),q.max()])
a=pd.DataFrame(absrows,columns=['Model','MAE (pp)','RMSE (pp)','R2','Min SOC','Max SOC']);a.to_csv(out/'absolute_soc_metrics.csv',index=False);print(a.to_string(index=False))
t=df.time.iloc[s:].to_numpy();pred=pd.DataFrame({'Time (s)':t,'SOC_CC (%)':soc[s:]})
for name,q in p.items():pred[name]=q;pred[name+' error (pp)']=q-soc[s:]
pred.to_csv(out/'holdout_predictions.csv',index=False)
for error,name in [(False,'Figure_4_SOC_reconstruction.png'),(True,'Figure_5_cumulative_error.png')]:
 fig,ax=plt.subplots(figsize=(7,4.1),layout='constrained')
 if not error:ax.plot(t,soc[s:],color='black',lw=2.2,label='Coulomb-counted pseudo-reference')
 else:ax.axhline(0,color='black',lw=.7)
 for (label,q),style,c in zip(p.items(),['--', '-', '-.', ':', (0, (5, 2, 1, 2))],['#D55E00', '#0072B2', '#009E73', '#CC79A7', '#8A6B00']):ax.plot(t,q-soc[s:] if error else q,label=label,ls=style,color=c,lw=1.6)
 ax.set(xlabel='Time (s)',ylabel='Cumulative SOC error (pp)' if error else 'SOC (%)');ax.grid(alpha=.18);ax.legend(fontsize=8,frameon=False);fig.savefig(out/name,dpi=300);plt.close(fig)
