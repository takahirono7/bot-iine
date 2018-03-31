# coding: utf-8

from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ
import sys
import os
import requests
######作成したスクリプトの読み込み########
from slackbot_settings import *
from plugins.scripts.reply_iine_number import ReturnAmountOfIine

# 関数内で使う変数を定義
script_dir = os.path.abspath(os.path.dirname(__file__))

# @respond_to('string')     bot宛のメッセージ
#                           stringは正規表現が可能 「r'string'」
# @listen_to('string')      チャンネル内のbot宛以外の投稿
#                           @botname: では反応しないことに注意
#                           他の人へのメンションでは反応する
#                           正規表現可能
# @default_reply()          DEFAULT_REPLY と同じ働き
#                           正規表現を指定すると、他のデコーダにヒットせず、
#                           正規表現にマッチするときに反応
# message.reply('string')   @発言者名: string でメッセージを送信
# message.send('string')    string を送信
# message.react('icon_emoji')  発言者のメッセージにリアクション(スタンプ)する
#                               文字列中に':'はいらない

@respond_to('メンション')
def mention_func(message):
    message.reply('私にメンションと言ってどうするのだ') # メンション

# いいねの数を増やして、合計イイね数を返信する
@listen_to('iine')
def add_iine(message):
    iine = ReturnAmountOfIine(message, script_dir)
# イイねされたことがある人かどうかを調べる
    check_result = iine.check_csv_file()
    if check_result == "exist":
        iine.add_iine_to_csv_file()
    else:
        iine.add_people_to_csv_file()
# イイねの数を調べる
    number_of_iine = iine.count_iine()

# message.sendではuser idなどがslack上でそのままでてしまうため、postを使う
    post_message = "に1いいねプレゼントぽめ。合計いいね数は『{}』ぽめ".format(number_of_iine)
    requests.post(URL, data = iine.return_post_message(post_message))

# いいねの数を減らして、合計イイね数を返信する
@listen_to('yokunaine')
def remove_iine(message):
    iine = ReturnAmountOfIine(message, script_dir)
# イイねされたことがある人かどうかを調べる
    check_result = iine.check_csv_file()
    if check_result == "exist":
        iine.remove_iine_to_csv_file()
# イイねの数を調べる
        number_of_iine = iine.count_iine()
# message.sendではuser idなどがslack上でそのままでてしまうため、postを使う
        post_message = "のいいねをとりあげちゃうぽめ。合計いいね数は『{}』ぽめ".format(number_of_iine)
        requests.post(URL, data = iine.return_post_message(post_message))
    else:
        message.send('その人は一回もいいねされてないぽめ')

