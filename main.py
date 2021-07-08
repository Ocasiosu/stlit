import streamlit as st
import numpy as np
import pandas as pd
from selenium import webdriver
import time


#川口市立図書館のログインページを開く


st.title('川口市立図書館の蔵書を予約数順にソート')
st.title('Streamlit上でSeleniumを動作させることができない\n⇨ローカル上でSeleniumを使用して取得したランキングを掲載することしかできない')

kensaku_text= st.text_input('検索ワードを入力してください')
"検索ワードは",kensaku_text,"です"


if st.checkbox('検索してみる'):
    st.write('検索結果')
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get('https://www.kawaguchi-lib.jp/opw1/OPW/OPWSRCH1.CSP')
    search_box = driver.find_element_by_xpath('/html/body/div[2]/form/div/div[2]/div[3]/div[1]/div[3]/input')
    search_box.send_keys(kensaku_text)
    elem_kensaku_btn = driver.find_element_by_name('srchbtn2')
    elem_kensaku_btn.click()
    
    #表示件数を100件にするために、urlの後ろにクエリをつけたアドレスに移動する
    time.sleep(1)
    driver.get("https://www.kawaguchi-lib.jp/opw1/OPW/OPWSRCHLIST.CSP?DB=LIB&MODE=1&PID2=OPWSRCH1&FLG=LIST&SORT=-3&HOLD=NOHOLD&WRTCOUNT=100&HOLDSEL=2&PAGE=1")
    #&SRCID=6 この数字がずれると何も表示されなくなるが、この部分を消してしまえば問題なく表示される
    title = driver.find_element_by_tag_name('h1')
    st.write(title.text)
    elems_tr = driver.find_elements_by_tag_name('tr')
    st.write(elems_tr[12].text)







st.write('DataFrame')

#df= pd.DataFrame({
#    '1列目':[1,2,3,4],
#    '2列目':[10,20,30,40]
#})
df= pd.DataFrame(
    np.random.rand(20,3),
    columns=['a','b','c'])

df2= pd.DataFrame(
    np.random.rand(100,2)/[50,50]+[35.69,139.70],
    columns=['lat','lon'])

#st.whiteだとwidthなどの引数を使えない
st.write(df)
st.dataframe(df.style.highlight_max(axis=0),width=200,height=200)
#tableはstaticなテーブルを作りたいときに使用する
st.table(df.style.highlight_max(axis=0))

#マジックコマンド
"""
# 章
## 節
### 項目
```
df= pd.DataFrame({
    '1列目':[1,2,3,4],
    '2列目':[10,20,30,40]
})
```
"""

#折れ線グラフを書く
st.line_chart(df)
st.area_chart(df)
st.bar_chart(df)

#マップをプロット
st.map(df2)

#画像を表示
from PIL import Image
if st.checkbox('ShowImage'):
    st.write('Display Image')
    img = Image.open('hiyoko.png')
    st.image(img,caption='キャプション',use_column_width=True)
    #なぜかファイルが存在しないって言われる
"インタラクティブなウィジェットたち"
option = st.sidebar.selectbox(
    "好きな数字は？",
    list(range(1,11))
)

"あなたの好きな数字は",option,"です"

text= st.sidebar.text_input('あなたの趣味を教えて下さい')
"あなたの趣味は",text,"です"

condition = st.sidebar.slider('あなたの今の調子は？',0,100,50)
"コンディション：",condition

#レイアウトを整える
st.sidebar.write('サイドバーに書きたいときは.sidebarを追加するだけ！')
#左右カラム分け
left_column,right_column=st.beta_columns(2)
button=left_column.button('右カラムに文字を表示')
if button:
    right_column.write('ここは右カラムです')

#expander
expander=st.beta_expander('問い合わせ')
expander.write('問い合わせ内容を書く')

#プログレスバー
import time
st.write('プログレスバーの表示')
"Start!"
latest_iteration=st.empty()
bar = st.progress(0)
for i in range(100):
    time.sleep(0.1)
    latest_iteration.text(f'Iteration{i+1}')
    bar.progress(i+1)
   
"完了！"