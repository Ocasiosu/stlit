import streamlit as st
import numpy as np
import pandas as pd
import time



from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome('chromedriver',options=options)

st.title('川口市立図書館の蔵書を予約数順にソート')
st.title('問題点：Streamlit上でSeleniumを動作させることができない')
"もともとの考えでは、Webアプリとして公開。"
"誰でも好きな検索ワードで検索できて"
"予約件数順にリストアップされて便利！ってのを実現したかった"

"ローカル上でSeleniumを使用して取得したcsvをもとに"
"SQLデータベースを作成して。。。"

kensaku_text= st.text_input('検索ワードを入力してください')
"検索ワードは",kensaku_text,"です"


if st.checkbox('検索してみる'):
    #st.write('検索結果')
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
    st.write(title.text,"← 「検索結果一覧」 と表示されればページが取得できています")
    elems_tr = driver.find_elements_by_tag_name('tr')
    st.write(elems_tr[12].text)
    #タイトルを収集する
    titles = []
    for i in range(100):
        title = elems_tr[i+12].find_element_by_tag_name('a')
        titles.append(title.text)
    #tdタグから出版社リストを取得する。[4]番目が出版社
    publishers = []
    for i in range(100):
        elems_td = elems_tr[i+12].find_elements_by_tag_name('td')
        publish = elems_td[4].text
        publishers.append(publish)
        #tdタグの[5]番目が出版日を表している
    release_dates = []
    for i in range(100):
        elems_td = elems_tr[i+12].find_elements_by_tag_name('td')
        release_date = elems_td[5].text
        release_dates.append(release_date)
        #tdタグの[6]番目がざいかを表している
    availables = []
    for i in range(100):
        elems_td = elems_tr[i+12].find_elements_by_tag_name('td')
        available = elems_td[6].text
        availables.append(available)
        #titleからget_attributeでhrefの中身を取り出して、hrefリストを作る
    urls = []
    for i in range(100):
        title = elems_tr[i+12].find_element_by_tag_name('a')
        url_title = title.get_attribute('href')
        urls.append(url_title)
    df = pd.DataFrame()
    df['タイトル'] = titles
    df['出版社'] = publishers
    df['出版日'] = release_dates
    df['在架'] = availables
    df['href'] = urls
    df





"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"


st.write('DataFrame表示テスト')

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