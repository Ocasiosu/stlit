import streamlit as st
import numpy as np
import pandas as pd
import time
#正規表現モジュールreをインポートする
import re
# 例外処理用のlibraryをインポートする
from selenium.common.exceptions import NoSuchElementException


st.title('課題：川口市立図書館の蔵書検索システムから予約数をスクレイピングして、人気の本を可視化する')
st.title('問題点：Streamlit上でSeleniumを動作させることができない')
"""
### SeleniumはJavaScriptベースで構築された蔵書検索システムをスクレイピングできる唯一の方法
### しかし動作可能なのはローカル上のみ
## もともとの考え
### Webアプリとして公開⇨誰でも好きな検索ワードで検索可能
### 検索結果が予約件数順にリストアップされて人気の本がひと目で分かる！

どうすれば実現できる？
ローカル上でSeleniumを使用して取得したxlsxをもとに
データベースを作成して。。。
"""

kensaku_text= st.text_input('デモンストレーション：検索ワードを入力してください')

if kensaku_text:
    kensaku_text,"で検索します"
    kensaku_text,"で検索した結果をここに表示する予定でした"

'ローカルでの検索結果を表示する'
#expander
expander=st.beta_expander('Pythonでの検索結果')
df1 = pd.read_excel('./data/kensaku_python.xlsx',index_col=0)
expander.write(df1)

expander=st.beta_expander('お金での検索結果')
df2 = pd.read_excel('./data/kensaku_お金.xlsx',index_col=0)
expander.write(df2)

# if st.checkbox('検索してみる'):
#     #st.write('検索結果')
#     driver = webdriver.Chrome('chromedriver.exe')
#     driver.get('https://www.kawaguchi-lib.jp/opw1/OPW/OPWSRCH1.CSP')
#     search_box = driver.find_element_by_xpath('/html/body/div[2]/form/div/div[2]/div[3]/div[1]/div[3]/input')
#     search_box.send_keys(kensaku_text)
#     elem_kensaku_btn = driver.find_element_by_name('srchbtn2')
#     elem_kensaku_btn.click()
    
#     #表示件数を100件にするために、urlの後ろにクエリをつけたアドレスに移動する
#     time.sleep(1)
#     driver.get("https://www.kawaguchi-lib.jp/opw1/OPW/OPWSRCHLIST.CSP?DB=LIB&MODE=1&PID2=OPWSRCH1&FLG=LIST&SORT=-3&HOLD=NOHOLD&WRTCOUNT=100&HOLDSEL=2&PAGE=1")
#     #&SRCID=6 この数字がずれると何も表示されなくなるが、この部分を消してしまえば問題なく表示される
#     title = driver.find_element_by_tag_name('h1')
#     st.write(title.text,"← 「検索結果一覧」 と表示されればページが取得できています")
#     elems_tr = driver.find_elements_by_tag_name('tr')
#     st.write(elems_tr[12].text)
#     #タイトルを収集する
#     titles = []
#     for i in range(100):
#         title = elems_tr[i+12].find_element_by_tag_name('a')
#         titles.append(title.text)
#     #tdタグから出版社リストを取得する。[4]番目が出版社
#     publishers = []
#     for i in range(100):
#         elems_td = elems_tr[i+12].find_elements_by_tag_name('td')
#         publish = elems_td[4].text
#         publishers.append(publish)
#         #tdタグの[5]番目が出版日を表している
#     release_dates = []
#     for i in range(100):
#         elems_td = elems_tr[i+12].find_elements_by_tag_name('td')
#         release_date = elems_td[5].text
#         release_dates.append(release_date)
#         #tdタグの[6]番目がざいかを表している
#     availables = []
#     for i in range(100):
#         elems_td = elems_tr[i+12].find_elements_by_tag_name('td')
#         available = elems_td[6].text
#         availables.append(available)
#         #titleからget_attributeでhrefの中身を取り出して、hrefリストを作る
#     urls = []
#     for i in range(100):
#         title = elems_tr[i+12].find_element_by_tag_name('a')
#         url_title = title.get_attribute('href')
#         urls.append(url_title)
#     df = pd.DataFrame()
#     df['タイトル'] = titles
#     df['出版社'] = publishers
#     df['出版日'] = release_dates
#     df['在架'] = availables
#     df['href'] = urls
#     df

# if st.checkbox('上でDataFieldが生成されてからクリックしてください'):
#     #予約件数リストyoyakusを定義する
#     yoyakus = []
#     for i in range(100):
#         if df.iloc[i]['在架'] =='× 在架なし':
#             time.sleep(0.5)
#             st.write('{}冊目は在架なしなので、予約数を調べます'.format(i+1))
#             #driver.get(preurl+"{}".format(i+1))
#             #df中のi行目,['href']列にアクセスする
#             driver.get(df.iloc[i]['href'])
#             #現在urlが本の詳細ページのときの処理
#             #print(driver.current_url+"を読み込んでいます")
#             try:#実行したい処理
#                 elems_yoyaku = driver.find_elements_by_class_name('col-xs-3')
#                 elem_yoyaku = elems_yoyaku[2].text.split('予約待ち')#elems_yoyakuでサーチしたdivタグの3番目を"予約待ち"という文字列で分断
#                 if len(elem_yoyaku) < 2:
#                     st.write('予約確保のみで予約待ちの文字列なしです')
#                     yoyakus.append(0)
#                 else:#len(elem_yoyaku)が2以上ならば elem_yoyaku[1]を指定したときにエラーが出ない
#                     num_yoyaku = int(re.sub(r"\D", "", elem_yoyaku[1]))#elem_yoyakuの2番めは予約確保の有無に関わらず、予約待ち件数になる
#                     st.write(num_yoyaku)#予約確保があったとしても、予約待ち件数だけを表示できた！
#                     yoyakus.append(num_yoyaku)

#             except NoSuchElementException:#上記が実行できなかった場合の処理
#                 st.write('予約数が取得できません')
#                 yoyakus.append(0)

#         else:
#             print('{}番目の本は在架ありです'.format(i+1))
#             yoyakus.append(0)
#         print("yoyakusリストには{}個の要素が格納されています".format(len(yoyakus)))
#     df['予約件数']=yoyakus
#     df2 = df.sort_values('予約件数', ascending=False).drop(columns='href').reset_index()
#     df2

"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"




#マジックコマンド
"""
# 章    以下、Streamlitの文法練習
## 節   文字の大きさ調節
### 項目    文字の大きさ・小
```
コメントアウトの方法
df= pd.DataFrame({
    '1列目':[1,2,3,4],
    '2列目':[10,20,30,40]
})
```
"""
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

#st.writeだとwidthなどの引数を使えない
st.write(df)
st.dataframe(df.style.highlight_max(axis=0),width=200,height=200)
#tableはstaticなテーブルを作りたいときに使用する
st.table(df.style.highlight_max(axis=0))
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
option = st.selectbox(
    "好きな数字は？",
    list(range(1,11))
)

"あなたの好きな数字は",option,"です"

text= st.text_input('あなたの趣味を教えて下さい')
"あなたの趣味は",text,"です"

condition = st.slider('あなたの今の調子は？',0,100,50)
"コンディション：",condition

#レイアウトを整える
st.write('サイドバーに追加したいならは.sidebarを追加するだけ！')
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