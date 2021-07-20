import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd
import time
#正規表現モジュールreをインポートする
import re
#画像を表示
from PIL import Image

st.title('川口市立図書館の蔵書検索システムをPythonスクレイピングで改良')
st.title('予約数から人気の本を可視化する')

"""
### 情報収集元：川口市立図書館蔵書検索システム
### https://www.kawaguchi-lib.jp/opw1/OPW/OPWSRCH1.CSP
"""

"""
# 作ろうとしたもの
## 誰でも好きな検索ワードで検索可能なWebアプリ
### 検索結果が予約件数順にリストアップされて、人気の本がひと目で分かる！



## 課題1
### SQLデータベースに関する勉強不足

"""
img5 = Image.open('./image/sql.png')
st.image(img5,caption="SQLite3とStreamlitとの連携でつまずく")

"""
## 課題2：Streamlit(Webアプリ)上でSeleniumを動作させることができない
### 蔵書検索システムJavaScriptベースで構築されているため、Seleniumでしかスクレイピングできない
### しかしSeleniumが動作可能なのはローカル環境のみ。
"""
#画像を表示

img2 = Image.open('./image/kousou_tosyokan.png')
st.image(img2,caption='ローカル環境でSeleniumが行う処理')





"""
# 実際にできたこと
## Streamlitで.pyファイルをWebアプリ化
### （このページはpythonコードで構築されています。）
## あらかじめローカル環境で作成したcsvファイルの表示

"""
st.markdown('**_python_での検索結果を予約件数順にソートしたもの 2021年7月9日取得**')
df1 = pd.read_csv('./data/kensaku_python.csv',index_col=0)
st.write(df1)
# #expander
expander=st.beta_expander('お金での検索結果 2021年7月8日取得')
df2 = pd.read_csv('./data/kensaku_お金.csv',index_col=0)
expander.write(df2)

expander=st.beta_expander('人生での検索結果 2021年7月8日取得')
df3 = pd.read_csv('./data/kensaku_人生.csv',index_col=0)
expander.write(df3)

"""
# なぜこのテーマを選択したのか
## 既存のシステムでも、スクレイピングと組み合わせれば、もっと活用の幅が広がるのではないか
### 私は川口市立図書館をしばしば利用しています。
### しかしウェブ上の蔵書検索システムは、昔から変わらず、今となっては古さを感じるUIのまま。
### 特に私が注目するのは、数ある蔵書の中でどれが人気なのかを知りたいということです。

## 利用者のメリット：新しい本との出会い
### 人気の本が瞬時にわかることで、今まで視野になかった本に出会うきっかけになります。
### 人気の本を知るためには予約数が一つの指標になると思います。
### しかし、現状では予約数を知るためには、毎回検索結果から本のタイトルをクリック、本の詳細ページに遷移する必要があります。
"""
img1 = Image.open('./image/100kai.png')
st.image(img1,caption='1冊ごとに詳細ページに遷移しないと予約数がわからない')

"""
## 図書館職員のメリット：工数削減
### 図書館の職員が利用者と同じシステム・UIを使っているかはわかりません
### もし利用者のものとほぼ同じだった場合
### 予約数を一括で取得することは、利用者よりも遥かに重要となるでしょう。
### なぜなら、蔵書冊数を管理する上で、予約数の多い本を知ることは必須だからです。
### 予約数を一括で取得するスクレイピング技術は職員の工数削減という面でも大きく役に立つと思います。

# 困難だったポイント
## for文を用いて各本の予約待ち件数を取得するプロセス
### 一言で予約数と言っても
### 「予約確保」
### 「予約待ち：～件」
### 「予約があるものの、予約数の表記なし」
### などさまざまな表記パターンが存在し、そのたびにif文やtry:except構文で場合分けをしながら処理を行いました。
### この部分でエラーの出ないコードを書くために、2日程度を要しました。
"""

img3 = Image.open('./image/yoyaku.png')
st.image(img3,caption="予約数に関しての表記")

img5 = Image.open('./image/yoyakumati.png')
st.image(img5,caption="予約待ち周辺の数字が一括して取得されてしまう中から、予約待ち件数だけを抜き出す")


'予約待ちの件数表記がない場合もあるので、if文やtry:except構文で場合分けして、splitメソッドで予約待ち件数だけを抽出しました'
img4 = Image.open('./image/baaiwake.png')
st.image(img4,caption="forループで本の詳細ページに1件ずつアクセスして予約待ち件数を取得している")

"""
# 手動で検索した場合との時間効率の違い
## ・手動で検索して1件ずつ予約件数を調べた場合
### ⇨**本1冊につき8秒程度**かかりました。
## ・スクレイピングによって検索結果100冊分一括で予約件数を取得した場合
### ⇨結果を予約件数順に並べ替えてcsv形式で出力するまで約100秒かかりました。
### ⇨**本1冊ごとにかかる時間は1秒**となり、手動で予約待ち件数を取得するよりも
### **7秒間/冊数の節約**になります
"""
components.html(
    """
    <iframe width="560" height="315" src="https://www.youtube.com/embed/MwJ7kZH7ryw" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    """,height = 600
)


"""
## 参考文献：諸外国の公共図書館に関する調査報告書 日本の公共図書館
### https://www.mext.go.jp/a_menu/shougai/tosho/houkoku/06082211/013.pdf

"""
# kensaku_text= st.text_input('デモンストレーション：検索ワードを入力してください(現在は機能しませんが、将来的にはデータベースから検索可能になる予定)')
# if kensaku_text:
#     kensaku_text,"で検索します"
#     kensaku_text,"で検索した結果をここに表示する予定でした"

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
#        
#      print('{}番目の本は在架ありです'.format(i+1))
#             yoyakus.append(0)
#         print("yoyakusリストには{}個の要素が格納されています".format(len(yoyakus)))
#     df['予約件数']=yoyakus
#     df2 = df.sort_values('予約件数', ascending=False).drop(columns='href').reset_index()
#     df2




# #マジックコマンド
# """
# # 章    以下、Streamlitでできる機能のデモンストレーション
# ## 節   文字の大きさ調節
# ### 項目    文字の大きさ・小
# ```
# コメントアウトの方法
# df= pd.DataFrame({
#     '1列目':[1,2,3,4],
#     '2列目':[10,20,30,40]
# })
# ```
# """
# st.write('DataFrame表示テスト')

# #df= pd.DataFrame({
# #    '1列目':[1,2,3,4],
# #    '2列目':[10,20,30,40]
# #})
# df= pd.DataFrame(
#     np.random.rand(20,3),
#     columns=['a','b','c'])

# df2= pd.DataFrame(
#     np.random.rand(100,2)/[50,50]+[35.69,139.70],
#     columns=['lat','lon'])

# #st.writeだとwidthなどの引数を使えない
# st.write(df)
# st.dataframe(df.style.highlight_max(axis=0),width=200,height=200)
# #tableはstaticなテーブルを作りたいときに使用する
# st.table(df.style.highlight_max(axis=0))
# #折れ線グラフを書く
# st.line_chart(df)
# st.area_chart(df)
# st.bar_chart(df)

# #マップをプロット
# st.map(df2)

# #画像を表示
# from PIL import Image
# if st.checkbox('ShowImage'):
#     st.write('Display Image')
#     img = Image.open('hiyoko.png')
#     st.image(img,caption='キャプション',use_column_width=True)
#     #なぜかファイルが存在しないって言われる
# "インタラクティブなウィジェットたち"
# option = st.selectbox(
#     "好きな数字は？",
#     list(range(1,11))
# )

# "あなたの好きな数字は",option,"です"

# text= st.text_input('あなたの趣味を教えて下さい')
# "あなたの趣味は",text,"です"

# condition = st.slider('あなたの今の調子は？',0,100,50)
# "コンディション：",condition

# #レイアウトを整える
# st.write('サイドバーに追加したいならは.sidebarを追加するだけ！')
# #左右カラム分け
# left_column,right_column=st.beta_columns(2)
# button=left_column.button('右カラムに文字を表示')
# if button:
#     right_column.write('ここは右カラムです')

# #expander
# expander=st.beta_expander('問い合わせ')
# expander.write('問い合わせ内容を書く')

# #プログレスバー
# import time
# st.write('プログレスバーの表示')
# "Start!"
# latest_iteration=st.empty()
# bar = st.progress(0)
# for i in range(100):
#     time.sleep(0.1)
#     latest_iteration.text(f'Iteration{i+1}')
#     bar.progress(i+1)
   
# "完了！"