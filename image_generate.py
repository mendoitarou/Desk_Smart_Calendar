#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys, os, time, json, datetime

import requests
from PIL import Image,ImageDraw,ImageFont
import feedparser

# ===== CONFIG =====
area_code = 390000
is_news_show = True # True/False
news_source_name = "nhk"#"itmedia", "virtual_life_magazine", "piyolog"
# ===== CONFIG =====

conv_weatherCodes = {# 2023/04/21更新
    100 : '晴',
    101 : '晴時々曇',
    102 : '晴一時雨',
    103 : '晴時々雨',
    104 : '晴一時雪',
    105 : '晴時々雪',
    106 : '晴一時雨か雪',
    107 : '晴時々雨か雪',
    108 : '晴一時雨か雷雨',
    110 : '晴後時々曇',
    111 : '晴後曇り',
    112 : '晴後一時雨',
    113 : '晴後時々雨',
    114 : '晴後雨',
    115 : '晴後一時雨',
    116 : '晴後時々雪',
    117 : '晴後雪',
    118 : '晴後雨か雪',
    119 : '晴後雨か雷雨',
    120 : '晴朝夕一時雨',
    121 : '晴朝の内一時雨',
    122 : '晴夕方一時雨',
    123 : '晴山沿い雷雨',
    124 : '晴山沿い雪',
    125 : '晴午後は雷雨',
    126 : '晴昼頃から雨',
    127 : '晴夕方あら雨',
    128 : '晴夜は雨',
    130 : '朝の内霧後晴',
    131 : '晴明け方霧',
    132 : '晴朝夕雲',
    140 : '晴時々雨で雷を伴う',
    160 : '晴一時雪か雨',
    170 : '晴時々雪か雨',
    181 : '晴後雪か雨',
    200 : '曇',
    201 : '曇時々晴',
    202 : '曇一時雨',
    203 : '曇時々雨',
    204 : '曇一時雪',
    205 : '曇時々雪',
    206 : '曇一時雨か雪',
    207 : '曇時々雨か雪',
    208 : '曇一時雨か雷雨',
    209 : '霧',
    210 : '曇後時々晴',
    211 : '曇後晴',
    212 : '曇後一時雨',
    213 : '曇後時々雨',
    214 : '曇後雨',
    215 : '曇後一時雪',
    216 : '曇後時々雪',
    217 : '曇後雪',
    218 : '曇後雨か雪',
    219 : '曇後雨か雷雨',
    220 : '曇朝夕一時雨',
    221 : '曇朝の内一時雨',
    222 : '曇夕方一時雨',
    223 : '曇日中時々晴',
    224 : '曇昼頃から雨',
    225 : '曇夕方から雨',
    226 : '曇夜は雨',
    228 : '曇昼頃から雪',
    229 : '雲夕方から雪',
    230 : '雲夜は雪',
    231 : '曇海上海岸は霧か霧雨',
    240 : '曇時々雨で雷を伴う',
    250 : '曇時々雪で雷を伴う',
    260 : '雲一時雪か雨',
    270 : '雲時々雪か雨',
    281 : '曇後雪か雨',
    300 : '雨',
    301 : '雨時々晴',
    302 : '雨時々止む',
    303 : '雨時々雪',
    304 : '雨か雪',
    306 : '大雨',
    308 : '雨で暴風を伴う',
    309 : '雨一時雪',
    311 : '雨後晴',
    313 : '雨後曇',
    314 : '雨後時々雪',
    315 : '雨後雪',
    316 : '雨か雪後晴',
    317 : '雨か雪後曇',
    320 : '朝の内雨後晴',
    321 : '朝の内雨後曇',
    322 : '雨朝晩一時雪',
    323 : '雨昼頃から晴',
    324 : '雨夕方から晴',
    325 : '雨夜は晴',
    326 : '雨夕方から雪',
    327 : '雨夜は雪',
    328 : '雨一時強く降る',
    329 : '雨一時みぞれ',
    340 : '雪か雨',
    350 : '雨で雷を伴う',
    361 : '雪か雨後晴',
    371 : '雪か雨後曇',
    400 : '雪',
    401 : '雪時々晴',
    402 : '雪時々止む',
    403 : '雪時々雨',
    405 : '大雪',
    406 : '風雪強く',
    407 : '暴風雪',
    409 : '雪一時雨',
    411 : '雪後晴',
    413 : '雪後曇',
    414 : '雪後雨',
    420 : '朝の内雪後晴',
    421 : '朝の内雪後曇',
    422 : '雪昼頃から雨',
    423 : '雪夕方から雨',
    425 : '雪一時強く降る',
    426 : '雪後みぞれ',
    427 : '雪一時みぞれ',
    450 : '雪で雷を伴う',
}

# weatherCodesからアイコン画像のIDに変更
conv_weatherCodes_Image = {# 2023/04/21更新
    100 : 100,
    101 : 101,
    102 : 102,
    103 : 102,
    104 : 104,
    105 : 104,
    106 : 102,
    107 : 102,
    108 : 102,
    110 : 110,
    111 : 110,
    112 : 112,
    113 : 112,
    114 : 112,
    115 : 115,
    116 : 115,
    117 : 115,
    118 : 112,
    119 : 112,
    120 : 102,
    121 : 102,
    122 : 112,
    123 : 100,
    124 : 100,
    125 : 112,
    126 : 112,
    127 : 112,
    128 : 112,
    130 : 100,
    131 : 100,
    132 : 101,
    140 : 102,
    160 : 104,
    170 : 104,
    181 : 115,
    200 : 200,
    201 : 201,
    202 : 202,
    203 : 202,
    204 : 204,
    205 : 204,
    206 : 202,
    207 : 202,
    208 : 202,
    209 : 200,
    210 : 210,
    211 : 210,
    212 : 212,
    213 : 212,
    214 : 212,
    215 : 215,
    216 : 215,
    217 : 215,
    218 : 212,
    219 : 212,
    220 : 202,
    221 : 202,
    222 : 212,
    223 : 201,
    224 : 212,
    225 : 212,
    226 : 212,
    228 : 215,
    229 : 215,
    230 : 215,
    231 : 200,
    240 : 202,
    250 : 204,
    260 : 204,
    270 : 204,
    281 : 215,
    300 : 300,
    301 : 301,
    302 : 302,
    303 : 303,
    304 : 300,
    306 : 300,
    308 : 308,
    309 : 303,
    311 : 311,
    313 : 313,
    314 : 314,
    315 : 314,
    316 : 311,
    317 : 313,
    320 : 311,
    321 : 313,
    322 : 303,
    323 : 311,
    324 : 311,
    325 : 311,
    326 : 314,
    327 : 314,
    328 : 300,
    329 : 300,
    340 : 400,
    350 : 300,
    361 : 411,
    371 : 413,
    400 : 400,
    401 : 401,
    402 : 402,
    403 : 403,
    405 : 400,
    406 : 406,
    407 : 406,
    409 : 403,
    411 : 411,
    413 : 413,
    414 : 414,
    420 : 411,
    421 : 413,
    422 : 414,
    423 : 414,
    425 : 400,
    426 : 400,
    427 : 400,
    450 : 400,
}

# カレントディレクトリのフルパスを取得
path = os.getcwd()

def get_weather_api(area_code = 390000, debug = False):
    if(debug):
        # デバッグ用のJSONを読み取る
        r_parse = json.load(open("debug_weather.json", "r", encoding="utf-8"))
    else:
        # 気象庁から天気予報を取ってくる
        url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"
        res = requests.get(url)
        r_parse = res.json()
    today_weather_code = int(r_parse[0]["timeSeries"][0]["areas"][0]["weatherCodes"][0])# 天気コード
    min_temp = round(float(r_parse[1]["tempAverage"]["areas"][0]["min"]))# 四捨五入する
    max_temp = round(float(r_parse[1]["tempAverage"]["areas"][0]["max"]))# 四捨五入する
    weather_data = {}# 返り値用
    weather_data["min_temp"] = min_temp
    weather_data["max_temp"] = max_temp
    weather_data["weather_code"] = today_weather_code
    print(f"MIN_TEMP: {min_temp}, MAX_TEMP: {max_temp}, WEATHER_CODE: {today_weather_code}")# デバッグ用に出力
    return weather_data

def get_latest_news(source = "nhk"):
    # ニュースの取得場所を変更
    if(source == "nhk"):
        url = "https://www.nhk.or.jp/rss/news/cat0.xml"
    if(source == "itmedia"):
        url = "https://rss.itmedia.co.jp/rss/2.0/itmedia_all.xml"
    if(source == "virtual_life_magazine"):
        url = "https://vr-lifemagazine.com/feed/"
    if(source == "piyolog"):
        url = "https://piyolog.hatenadiary.jp/rss"
    f = feedparser.parse(url) # 取得
    news_data = {}# 返り値用
    count = 0# 取得するニュースの個数制限用
    # タイトル抽出
    for article in f['entries']:
        if(count < 3):# 3つ取得する
            news_data[count] = article['title']
        count = count + 1
    return news_data

def generate_image(debug = False):
    # 背景(真っ白)読み込み
    im = Image.open(path+"/assets/base.png")
    im = im.convert('RGB')

    # テキストを書き込む準備
    draw = ImageDraw.Draw(im)

    # 表示
    sign_font = ImageFont.truetype(path+'/assets/ipag.ttc', 10, index=0)# Sign
    draw.text((50, 240), 'Tarou Software', fill='black', font=sign_font)# sign multiline_text
    
    # 日付(曜日)取得
    now_date = datetime.datetime.now()
    print("NOW_DATA: "+now_date.strftime('%Y-%m-%d_%H-%M-%S'))
    now_date_Year = now_date.year
    now_date_Month = now_date.month
    now_date_Day = now_date.day
    now_date_Weekday_ENG = now_date.strftime('%a')
    # 日付用フォント読み込み
    date_Main_font = ImageFont.truetype(path+'/assets/ipag.ttc', 48, index=0)# Main
    date_Sub_font = ImageFont.truetype(path+'/assets/ipag.ttc', 12, index=0)# Sub
    # 日付の書き込み
    draw.text((25, 10), f'{now_date_Month}', fill='black', font=date_Main_font)# Month #30,10
    draw.text((50, 50), f'{now_date_Day}', fill='black', font=date_Main_font)# Day # 45,50
    # 右上 90,15 90,25 (マシ？)
    # 右真ん中 90,45 95,55 (かなり微妙)
    # 右下 95,70 95,80 (かなり微妙)
    # 左真ん中 10,45 10,55
    # 左下 15,70 15,80 (一番マシ？)
    draw.text((15, 70), f'{now_date_Year}', fill='black', font=date_Sub_font)# Year
    draw.text((15, 80), f'{now_date_Weekday_ENG}', fill='black', font=date_Sub_font)# Month(Ex: Wed)

    # 天気予報
    weather_data = get_weather_api(area_code, debug)# データの取得
    # 天気アイコン貼り付け
    im_weatherImage = Image.open(f'weatherCodes_Image/{weather_data["weather_code"]}.png')# 天気アイコン画像読み込み
    im_weatherImage = im_weatherImage.resize((60, 40), Image.LANCZOS)# 大きさ変更
    im.paste(im_weatherImage, (10, 110))
    # 気温書き込み
    weather_title_font = ImageFont.truetype(path+'/assets/ipag.ttc', 10, index=0)# タイトル用フォント読み込み
    weather_temp_font = ImageFont.truetype(path+'/assets/ipag.ttc', 16, index=0)# 気温用フォント読み込み
    draw.text((5, 100), 'Weather: ', fill='black', font=weather_title_font)# Title
    draw.text((10, 150), f'⇩ {weather_data["min_temp"]}', fill='black', font=weather_temp_font)# Min
    draw.text((50, 150), f'⇧ {weather_data["max_temp"]}', fill='black', font=weather_temp_font)# Max
    draw.text((90, 155), f'(℃)', fill='black', font=weather_title_font)# Celsius

    # ニュースを表示(表示文字数が少なすぎて使い勝手悪い)
    if(is_news_show):
        news_data = get_latest_news(news_source_name)
        news_title_font = ImageFont.truetype(path+'/assets/ipag.ttc', 10, index=0)# タイトル用フォント読み込み
        news_article_font = ImageFont.truetype(path+'/assets/ipag.ttc', 11, index=0)# ニュース用フォント読み込み
        draw.text((5, 170), 'News: ', fill='black', font=news_title_font)# Title
        draw.text((5, 185), f'・{news_data[0]}', fill='black', font=news_article_font)# Article
        draw.text((5, 205), f'・{news_data[1]}', fill='black', font=news_article_font)# Article
        draw.text((5, 225), f'・{news_data[2]}', fill='black', font=news_article_font)# Article
    
    # 画像保存
    #im.save(path + '/latest.bmp', quality=100)

    # 実行ログ保存
    text = "\n[LOG][RUN]\n"+"NOW_DATA: "+now_date.strftime('%Y-%m-%d_%H-%M-%S')+"\n"+"MIN_TEMP: "+str(weather_data['min_temp'])+", MAX_TEMP: "+str(weather_data['max_temp'])+", WEATHER_CODE: "+str(weather_data['weather_code'])+"\n"
    log_path = path+"/log.txt"
    with open(log_path, mode='a') as f:
        f.write(text)

    #デバッグ
    if(debug):
        # デバッグ用画像表示
        im.show()
        # デバッグ用画像保存
        #im.save(path + '/temp.png', quality=100)

    # 返り値として画像を返す
    return im

#weather_data = get_weather_api(39000)
#print(f"Weather_Icon_Image_Path: ./weatherCodes_Image/{weather_data["weather_code"]}.svg")

#get_latest_news(news_source_name)

#generate_image(True)
