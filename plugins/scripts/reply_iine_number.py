# coding:utf-8
import os
import re
import sys
import requests
from slackbot_settings import *
import csv
import fileinput


class ReturnAmountOfIine():
	def __init__(self, message, script_dir):
# slackのuserid
		self.message = message.body['text']

#slackでiineをしたuseridを以下の正規表現でとりだす
		self.userid = re.search(r'(?<=<@).+?(?=>)', message.body['text']).group(0)
# 投稿元のchannel id
		self.channel_id = message.body['channel']
# iineの数が記載されているcsvファイルのパス
		self.csv_path = os.path.join(script_dir, "scripts", "iine.csv")

# 対象のuserがすでにcsvファイル上に記載されているかを判定する
	def check_csv_file(self):
		with open(self.csv_path, 'r') as f:
			reader = csv.DictReader(f)
			for row in reader:
				if row[u'people'] == self.userid:
					return("exist")
				else:
					return("not_exist")

# イイねの数が記載されているcsv fileを編集し、対象ユーザのイイね数を1増やす
# fileinputモジュールを用い、標準出力をcsv fileに書き込む
	def add_iine_to_csv_file(self):
		with fileinput.input(self.csv_path, inplace=True) as f:
# for文でcsvファイルを一行づつ出力し、イイねされたユーザの名前に該当したら数を一つ増やす
			for line in f:
# 行末の改行を削除する
				line = line.rstrip('\r\n')
				if line.startswith(self.userid):
					new_iine_val = (int(line.split(",")[1]) + 1)
					print(self.userid+","+str(new_iine_val))
					continue
				print(line)

	def remove_iine_to_csv_file(self):
		with fileinput.input(self.csv_path, inplace=True) as f:
# for文でcsvファイルを一行づつ出力し、イイねされたユーザの名前に該当したら数を一つ減らす
			for line in f:
				line = line.rstrip('\r\n')
				if line.startswith(self.userid):
					new_iine_val = (int(line.split(",")[1]) - 1)
					print(self.userid+","+str(new_iine_val))
					continue
				print(line)

# ユーザがcsvファイル上にいなかったら末尾に追記する
	def add_people_to_csv_file(self):
		data = [self.userid,int(1)]
		with open(self.csv_path, 'a') as f:
# 書き込み用writeオブジェクトを作成
# 書き込みの際末尾を改行する
			writer = csv.writer(f, lineterminator='\n')
			writer.writerow(data)

# iineの数を確認する
	def count_iine(self):
		with open (self.csv_path, 'r') as f:
			for line in f:
# 行末の改行を削除する
				line = line.rstrip('\r\n')
				if line.startswith(self.userid):
					return line.split(",")[1]


	def return_post_message(self, post_message):
		post_json = {
		    'token': API_TOKEN,
		    'text': "<@"+self.userid+">"+post_message,
		    'channel': self.channel_id,
		    'username': "pomeranian_bot",
		    'link_names': 1,
		    "icon_emoji": ":pomeranian_bot:"
		}		
		return post_json
