# -*- coding: UTF-8 -*-

import os
import requests
import flask
from urllib import request
from urllib import parse
from bs4 import BeautifulSoup
from linebot.models import Sender
#from moviehelpermodule.moviehelper import show_movieHelper, use_moviename_serch_movielist, use_moviename_serch_article, use_movieurl_get_movieinfo, use_actorURL_get_actorIntorduction, show_movieInfo_message, show_actor_intorduction, use_actorURL_search_movielist, search_movie_thisweekAndIntheaters, search_movie_comingsoon, show_chart_message, search_movie_chart, search_movie_chartNetizens, select_movie_type, search_movie_type, show_location_message, use_location_search_movietheater, use_movietheatherName_search_movie, use_movietheaterInfo_get_locationMessage, get_MovieMoment, use_movieurl_get_movieReleasedArea, use_movieurl_get_movieMoment, workTeam

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
app = flask.Flask(__name__)

line_bot_api = LineBotApi('...')
handler = WebhookHandler('...')

from urllib import request, parse
import urllib
from bs4 import BeautifulSoup
from linebot.models import *
#from moviehelpermodule.calculate import getDistance, getNowTimeEmoji, useTimeGetTimeEmoji
import time
from math import radians, atan, tan, acos, cos, sin
################################################################
def getDistance(latA, lonA, latB, lonB):  
    ra = 6378140  # radius of equator: meter  
    rb = 6356755  # radius of polar: meter   
    flatten = (ra - rb) / ra  # Partial rate of the earth  
    # change angle to radians  
    radLatA = radians(latA)  
    radLonA = radians(lonA)  
    radLatB = radians(latB)  
    radLonB = radians(lonB)  
    
    pA = atan(rb / ra * tan(radLatA))  
    pB = atan(rb / ra * tan(radLatB))  
    x = acos(sin(pA) * sin(pB) + cos(pA) * cos(pB) * cos(radLonA - radLonB))  
    c1 = (sin(x) - x) * (sin(pA) + sin(pB))**2 / cos(x / 2)**2  
    c2 = (sin(x) + x) * (sin(pA) - sin(pB))**2 / sin(x / 2)**2  
    dr = flatten / 8 * (c1 - c2)  
    distance = ra * (x + dr)
    return round(distance/1000,2)


def pagebox(soup):
    # --------------------pagebox
    if len(soup.select(".page_numbox ul")) == 0 or soup.select_one(".page_numbox ul") == None:
        pagebox_flex_message = False
    else:
        pagebox = soup.select(".page_numbox ul")[0]
        nowpage = pagebox.select(".active span")[0].text
        anotherpageURL = [i["href"] for i in pagebox.select("a")]
        anotherpage = [i.text for i in pagebox.select("a")]

        contents = []
        for index in range(len(anotherpage)):
            contents.append({
                "type": "text",
                "text": anotherpage[index],
                "align": "center",
                "action": {
                    "type": "postback",
                    "data": anotherpageURL[index]
                }
            })
        # ??????
        pagebox_flex_message = FlexSendMessage(
            alt_text='??????',
            contents={
                "type": "bubble",
                "direction": "ltr",
                "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                    "type": "text",
                    "text": "?????????"+nowpage+"???",
                    "align": "center"
                    },
                    {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "xl",
                    "contents": contents
                    }
                ]
                }
            }
        )
    return(pagebox_flex_message)


def use_moviename_serch_movielist(movieNameOrURL, page):
    # ?????????URL????????????
    if movieNameOrURL[:71] == 'https://movies.yahoo.com.tw/moviesearch_result.html?type=movie&keyword=':
        movieURL = movieNameOrURL
    else:
        urlname = parse.quote(movieNameOrURL)
        movieURL = 'https://movies.yahoo.com.tw/moviesearch_result.html?type=movie&keyword=' + \
            urlname + '&page=' + page
    # ????????????URL
    print(movieURL)
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
    req = request.Request(movieURL, headers=headers)
    resp = request.urlopen(req)
    respData = str(resp.read().decode('utf-8'))
    soup = BeautifulSoup(respData, "html.parser")
    # movieNameCN ?????????
    # movieNameEN ?????????
    # movieExpectation ?????????
    # movieSatisfactoryDegree ?????????
    # moviePoster ??????
    # movieReleaseTime ????????????
    # movieDetailUrl ??????????????????

    # --------------------movie list
    if soup.select_one(".release_movie_name > a") == None:
        movie_flex_message = FlexSendMessage(
            alt_text= "????????? "+movieNameOrURL+" ???????????????",
            contents={
                "type": "bubble",
                "direction": "ltr",
                "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                    "type": "text",
                    "text": "????????? "+movieNameOrURL+" ???????????????",
                    "align": "center"
                    }
                ]
                }
            }
        )
        page = False
        return(movie_flex_message, page)
    else:
        movieInfo = [i.text for i in soup.select(".release_info")]
        movieNameCN = [i.text for i in soup.select(".release_movie_name > a")]
        movieNameEN = []
        for i in soup.select(".en a"):
            if i.text.strip() == '':
                movieNameEN.append("-")
            else:
                movieNameEN.append(i.text.strip())
        movieExpectation = [i.text for i in soup.select("#content_l dt span")]
        # info_item = soup.find_all('div','release_info')
        # movieExpectation = []
        # for item in info_item:
        #     try:
        #         level = item.find('div','leveltext').span.text.strip()                
        #         movieExpectation.append(level)
        #     except :
        #         movieExpectation.append('0')


        movieSatisfactoryDegree = []
        for info in movieInfo:
            movieSatisfactoryDegree.append('?????????') if info.find(
                "?????????") == -1 else movieSatisfactoryDegree.append(info[info.find("?????????")+5:info.find("?????????")+8])
        moviePoster = [i["src"] for i in soup.select(".release_foto img")]
        #moviePoster = soup.find('div','foto').find("img").get("src")
        movieReleaseTime = [(i.text)[7:] for i in soup.select(".time")]
        movieDetailUrl = [i["href"]
                          for i in soup.select(".release_movie_name > a")]

        # ????????????json??????
        contents = []
        for index in range(len(movieNameCN)):
            contents.append({
                "type": "bubble",
                "direction": "ltr",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [{
                        "type": "text",
                        "text": "??????",
                        "size": "xl",
                        "align": "start",
                        "weight": "bold",
                        "color": "#000000"
                    }]
                },
                "hero": {
                    "type": "image",
                    "url": moviePoster[index],
                    "gravity": "top",
                    "size": "full",
                    "aspectRatio": "1:1.4",
                    "aspectMode": "cover",
                    "backgroundColor": "#FFFFFF"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [{
                        "type": "box",
                        "layout": "vertical",
                        "contents": [{
                            "type": "text",
                            "text": movieNameCN[index],
                            "margin": "none",
                            "size": "lg",
                            "align": "center",
                            "gravity": "top",
                            "weight": "bold"
                        },
                            {
                            "type": "text",
                            "text": movieNameEN[index],
                            "align": "center"
                        }]
                    },
                        {
                        "type": "separator",
                        "margin": "lg",
                        "color": "#FFFFFF"
                    },
                        {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [{
                            "type": "text",
                            "text": "???????????????"
                        },
                            {
                            "type": "text",
                            "text": movieReleaseTime[index]
                        }]
                    },
                        {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [{
                            "type": "text",
                            "text": "????????????",
                            "align": "start",
                            "weight": "bold",
                            "color": "#BB21CA"
                        },
                            {
                            "type": "text",
                            "text": movieExpectation[index]
                        }]
                    },
                        {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [{
                                "type": "text",
                                "text": "????????????",
                                "align": "start",
                                "weight": "bold",
                                "color": "#2133CA"
                        },
                            {
                                "type": "text",
                                "text": movieSatisfactoryDegree[index],
                                "align": "start"
                        }]
                    }
                    ]},
                "footer": {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [{
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "????????????",
                            "data": movieDetailUrl[index]
                        }
                    }]
                }
            })
        # ??????
        movie_flex_message = FlexSendMessage(
            alt_text='????????????',
            contents={
                "type": "carousel",
                "contents": contents
            }
        )

        pagebox_flex_message = pagebox(soup)

        return(movie_flex_message, pagebox_flex_message)


def use_moviename_serch_article(movieName):
    # --------------------article
    # ?????????URL????????????
    urlname = parse.quote(movieName)
    # ????????????URL
    movieURL = 'https://movies.yahoo.com.tw/tagged/'+urlname
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
    req = request.Request(movieURL, headers=headers)
    resp = request.urlopen(req)
    respData = str(resp.read().decode('utf-8'))
    soup = BeautifulSoup(respData, "html.parser")

    if soup.select_one(".fotoinner img") == None:
        article_flex_message = FlexSendMessage(
            alt_text="????????? "+movieName+" ???????????????",
            contents={
                "type": "bubble",
                "direction": "ltr",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "????????? "+movieName+" ???????????????",
                            "align": "center"
                        }
                    ]
                }
            }
        )
    else:
        articleTitle = [i.text for i in soup.select(".text_truncate_2")][:10]
        articleContent = [i.text[21:-17]
                          for i in soup.select(".jq_text_overflow_link")][:10]
        #articleImg = [i['src'] for i in soup.select(".lazy-load")][:10]
        articleImg = [i['src'] for i in soup.select("#content_l img")][:10]
        articleURL = [i['href'] for i in soup.select(".news_content a")][:10]
        articleDate = [i.text for i in soup.select(".day")][:10]

        articleContents = []
        for index in range(len(articleTitle)):
            articleContents.append({
                "type": "bubble",
                "direction": "ltr",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "????????????",
                            "size": "xl",
                            "align": "start",
                            "weight": "bold"
                        }
                    ]
                },
                "hero": {
                    "type": "image",
                    "url": articleImg[index],
                    "size": "full",
                    "aspectRatio": "3:4",
                    "aspectMode": "cover"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": articleTitle[index],
                            "align": "center",
                            "weight": "bold",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": articleContent[index],
                            "size": "sm",
                            "wrap": True
                        }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "uri",
                                "label": "????????????yahoo?????????",
                                "uri": articleURL[index]
                            }
                        }
                    ]
                }
            })

        article_flex_message = FlexSendMessage(
            alt_text='????????????',
            contents={
                "type": "carousel",
                "contents": articleContents
            }
        )
    return(article_flex_message)


def use_movieurl_get_movieinfo(url):
    try:
        headers = {}
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
        req = request.Request(url, headers=headers)
        resp = request.urlopen(req)
        respData = str(resp.read().decode('utf-8'))  # ????????????????????????
        soup = BeautifulSoup(respData,features="lxml")

        # --------------------moviePoster
        #moviePoster = soup.select_one(".movie_intro_foto img")["src"]
        moviePoster = soup.find('div','foto').find("img").get("src")

        moviePoster_image_message = ImageSendMessage(
            original_content_url=moviePoster,
            preview_image_url=moviePoster
        )
        # --------------------info
        movieNameCN = soup.select_one("h1").text
        
        for i in soup.select(".movie_intro_info_r h3"):
            if i.text.strip() == '':
                movieNameEN = "-"
            else:
                movieNameEN = i.text.strip()
        movieTag = [((i.text.split())[0])+'???'
                    for i in soup.select(".level_name .gabtn")]
        movieReleaseTime = soup.select_one(".level_name_box+ span").text[5:]
        movieRuntime = (soup.select_one("span:nth-child(6)").text)[5:]
        movieProCo = (soup.select("span:nth-child(7)")[1].text)[5:]
        movieIMDb = (soup.select_one("span:nth-child(8)").text)[7:]
        if movieIMDb == '':
            movieIMDb = '?????????'
        movieExpectation = (
            (soup.select(".evaluate_inner")[0].text).split())[-2]
        if movieExpectation == '':
            movieExpectation = '?????????'
        movieSatisfactoryDegree = (
            (soup.select(".evaluate_inner")[1].text).split())[3]
        if movieSatisfactoryDegree == '':
            movieSatisfactoryDegree = '?????????'
        if soup.select(".movie_intro_list")[0] == None:
            director="???????????????"
        else:
            director = [i.text.replace('\n', '').replace(' ', '').split(
                '???') for i in soup.select(".movie_intro_list")][0]
            director = ','.join(director)
        if len((soup.select(".movie_intro_list")[1]).text) == 3:#????????????
            print("1")
            actor="???????????????"
        else:
            print("2")
            actor = [i.text.replace('\n', '').replace(' ', '').split(
                '???') for i in soup.select(".movie_intro_list")][1]
            actor = ','.join(actor)
        # ????????????
        print(movieNameCN)
        print(movieNameEN)
        print(movieTag)
        print(movieReleaseTime)
        print(movieRuntime)
        print(movieProCo)
        print(movieIMDb)
        print(movieExpectation)
        print(movieSatisfactoryDegree)
        # print(director)
        # print(actor)
        movieTagContent = []
        for tag in movieTag:
            movieTagContent.append({
                "type": "text",
                "text": tag,
                "flex": 0,
                "weight": "bold",
                "color": "#000C3B"
            })
        info_flex_message = FlexSendMessage(
            alt_text='????????????',
            contents={
                "type": "bubble",
                "direction": "ltr",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "????????????",
                            "size": "xl",
                            "align": "start",
                            "weight": "bold"
                        },
                        {
                        "type": "separator",
                        "margin": "md",
                        "color": "#4B6174"
                        },
                        {
                            "type": "text",
                            "text": movieNameCN,
                            "margin": "md",
                            "size": "lg",
                            "align": "center",
                            "weight": "bold",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": movieNameEN,
                            "size": "md",
                            "align": "center",
                            "wrap": True
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "margin": "lg",
                            "contents": movieTagContent
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "margin": "lg",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "????????????",
                                    "weight": "bold"
                                },
                                {
                                    "type": "text",
                                    "text": movieReleaseTime.strip()
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "margin": "xs",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "??????",
                                    "weight": "bold"
                                },
                                {
                                    "type": "text",
                                    "text": movieRuntime
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "margin": "xs",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "????????????",
                                    "weight": "bold"
                                },
                                {
                                    "type": "text",
                                    "text": movieProCo
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "margin": "lg",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "IMDb??????",
                                    "weight": "bold",
                                    "color": "#EAC44E"
                                },
                                {
                                    "type": "text",
                                    "text": movieIMDb
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "margin": "xs",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "?????????",
                                            "weight": "bold",
                                            "color": "#BB21CA"
                                        },
                                        {
                                            "type": "text",
                                            "text": movieExpectation
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "?????????",
                                            "weight": "bold",
                                            "color": "#2133CA"
                                        },
                                        {
                                            "type": "text",
                                            "text": movieSatisfactoryDegree
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "lg",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "??????",
                                            "weight": "bold"
                                        },
                                        {
                                            "type": "text",
                                            "text": director,
                                            "size": "xs",
                                            "wrap": True
                                        },
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "text": "??????",
                                                    "weight": "bold"
                                                },
                                                {
                                                    "type": "text",
                                                    "text": actor,
                                                    "size": "xxs",
                                                    "wrap": True
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            }
        )
        # --------------------story
        story = soup.select_one("#story").text
        print(story)
        print(soup.find("gray_infobox_inner"))
        story_flex_message = FlexSendMessage(
            alt_text='??????',
            contents={
                "type": "bubble",
                "direction": "ltr",
                "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                    "type": "text",
                    "text": "????????????",
                    "size": "xl",
                    "align": "start",
                    "weight": "bold"
                    },
                    {
                    "type": "separator",
                    "margin": "md",
                    "color": "#4B6174"
                    },
                    {
                    "type": "text",
                    "text": story,
                    "align": "start",
                    "wrap": True
                    }
                ]
                }
        })
        # --------------------actor
        actorName = [i.text for i in soup.select(".actor_inner h2")]
        actorContents = []
        if soup.select_one(".actor_inner h2") == None:
            actorContents.append({
                "type": "bubble",
                "direction": "ltr",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "????????????????????????",
                            "align": "center"
                        }
                    ]
                }
            })
        else:
            actorNameCN = []
            actorNameEN = []
            actorDetailURL = []
            if len(actorName) > 0:
                for name in actorName:
                    name = name.split()
                    actorNameCN.append(name[0])
                    if len(name) >= 3:
                        ENname = ''
                        for index in range(len(name))[1:]:
                            ENname += ' '+name[index]
                        actorNameEN.append(ENname)
                    elif len(name) == 2:
                        actorNameEN.append(name[1])
                    else:
                        actorNameEN.append(' ')

                actorImg = []
                for img in soup.select("._slickcontent .fotoinner img"):
                    if img["data-src"] == "/build/images/noavatar.jpg":
                        actorImg.append("https://movies.yahoo.com.tw"+img["data-src"])
                    else:
                        actorImg.append(img["data-src"])
                       # actorImg[-1] =  str(actorImg[-1]).replace("http", "https")
                        print(actorImg[-1])
                print(actorImg)

                actorNameCN = actorNameCN[:10]
                actorDetailURL = [i["href"] for i in soup.select(".starlist a")]
            for index in range(len(actorNameCN)):
                actorContents.append({
                    "type": "bubble",
                    "direction": "ltr",
                    "header": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "???????????????",
                                "size": "xl",
                                "align": "start",
                                "weight": "bold"
                            }
                        ]
                    },
                    "hero": {
                        "type": "image",
                        "url": actorImg[index],
                        "size": "full",
                        "aspectRatio": "3:4",
                        "aspectMode": "cover"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": actorNameCN[index],
                                "size": "xl",
                                "weight": "bold"
                            },
                            {
                                "type": "text",
                                "text": actorNameEN[index],
                                "size": "xl"
                            }
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "postback",
                                    "label": "????????????",
                                    "data": actorDetailURL[index]
                                }
                            }
                        ]
                    }
                })

        actor_flex_message = FlexSendMessage(
            alt_text='????????????',
            contents={
                "type": "carousel",
                "contents": actorContents
            }
        )

        # --------------------movieStills
        movieStills = [i for i in soup.select(".imglist img")]
        movieStillsUrl = []
        for img in movieStills:
            movieStillsUrl.append(img["data-src"])

        print(movieStillsUrl)
        movieStillsContent = []
        cnt = 0
        for img in movieStillsUrl[:10]:
            movieStillsContent.append({
                "type": "bubble",
                "direction": "ltr",
                "hero": {
                    "type": "image",
                    "url": img,
                    "size": "full",
                    "aspectRatio": "1.85:1",
                    "aspectMode": "cover"
                }
            })

        movieStills_flex_message = FlexSendMessage(
            alt_text='????????????',
            contents={
                "type": "carousel",
                "contents": movieStillsContent
            }
        )

        return(moviePoster_image_message, info_flex_message, story_flex_message, actor_flex_message, movieStills_flex_message)

        # --------------------
    except Exception as e:
        print(str(e))

def use_actorURL_get_actorIntorduction(url):
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
    req = request.Request(url, headers=headers)
    resp = request.urlopen(req)
    respData = str(resp.read().decode('utf-8'))  # ????????????????????????
    soup = BeautifulSoup(respData)

    # --------------------info
    actorNameCN = soup.select_one(".maker_name").text
    actorNameEN = soup.select_one(".name_en").text
    if actorNameEN == "":
        actorNameEN = "?????????"
    if len(actorNameCN[:-len(actorNameEN)]) > 1:
        actorNameCN = actorNameCN[:-len(actorNameEN)]

    actorBirth = soup.select_one(".maker_birth").text[5:]
    if actorBirth == "":
        actorBirth = "?????????"
    actorImg = soup.select_one(".pic img")["src"]
    actorImgFrom = soup.select_one(".pic_txt").text
    actorTitle = [i.text.split() for i in soup.select(".maker_tips")][0]
    if actorTitle == []:
        actorTitle.append("?????????")
    actorPop = soup.select_one(".popnum").text[3:]
    print(actorNameCN)
    print(actorNameEN)
    print(actorBirth)
    print(actorImg)
    print(actorImgFrom)
    print(actorTitle)
    print(actorPop)
    titleContent=[]
    for title in actorTitle:
        titleContent.append({
            "type": "text",
            "text": title,
            "flex": 0,
            "weight": "bold",
            "color": "#000C3B"
        })

    actor_flex_message = FlexSendMessage(
        alt_text='????????????',
        contents={
            "type": "bubble",
            "direction": "ltr",
            "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "text",
                "text": "????????????",
                "size": "xl",
                "align": "start",
                "weight": "bold"
                }
            ]
            },
            "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                        "type": "image",
                        "url": actorImg,
                        "align": "start",
                        "aspectRatio": "1:2",
                        "aspectMode": "cover"
                        }
                    ]
                    },
                    {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                            "type": "text",
                            "text": actorNameCN,
                            "size": "lg",
                            "weight": "bold"
                            },
                            {
                            "type": "text",
                            "text": actorNameEN
                            }
                        ]
                        },
                        {
                        "type": "box",
                        "layout": "horizontal",
                        "flex": 0,
                        "spacing": "md",
                        "margin": "lg",
                        "contents": titleContent
                        },
                        {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "lg",
                        "contents": [
                            {
                            "type": "text",
                            "text": "?????????",
                            "flex": 0,
                            "weight": "bold"
                            },
                            {
                            "type": "text",
                            "text": actorBirth
                            }
                        ]
                        },
                        {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "lg",
                        "contents": [
                            {
                            "type": "text",
                            "text": "?????????",
                            "flex": 0,
                            "weight": "bold"
                            },
                            {
                            "type": "text",
                            "text": actorPop
                            }
                        ]
                        }
                    ]
                    }
                ]
                },
                {
                    "type": "text",
                    "text": actorImgFrom,
                    "margin": "md",
                    "size": "xxs",
                    "align": "end",
                    "color": "#6A6A6A"
                }
            ]
            }
        }
    )
    if "??????" not in actorTitle:
        directorColor = "#D6D6D6"
    else:
        directorColor = "#42659A"

    if "??????" not in actorTitle:
        actorColor = "#D6D6D6"
    else:
        actorColor = "#42659A"

    introductionlist_flex_message = FlexSendMessage(
        alt_text='????????????',
        contents={
            "type": "bubble",
            "direction": "ltr",
            "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "button",
                "action": {
                    "type": "postback",
                    "label": "????????????",
                    "data": '????????????:'+url
                }
                },
                {
                "type": "separator"
                },
                {
                "type": "button",
                "action": {
                    "type": "postback",
                    "label": "????????????",
                    "data": 'https://movies.yahoo.com.tw/name_movies/'+url[url.find('-',-10)+1:]+'?type=1'
                },
                "color": directorColor
                },
                {
                "type": "button",
                "action": {
                    "type": "postback",
                    "label": "????????????",
                    "data": 'https://movies.yahoo.com.tw/name_movies/'+url[url.find('-',-10)+1:]+'?type=2'
                },
                "color": actorColor
                },
                {
                "type": "separator"
                },
                {
                "type": "button",
                "action": {
                    "type": "postback",
                    "label": "????????????",
                    "data": 'https://movies.yahoo.com.tw/tagged/'+actorNameCN
                }
                }
            ]
            }
        }
    )

    return(actor_flex_message, introductionlist_flex_message)
def show_actor_intorduction(url):
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
    req = request.Request(url, headers=headers)
    resp = request.urlopen(req)
    respData = str(resp.read().decode('utf-8'))  # ????????????????????????
    soup = BeautifulSoup(respData)

    
    intorduction = soup.select_one(".jq_text_overflow_href_main").text
    cutFrequency = int(len(intorduction)/300)+1
    contents = []
    for frequency in range(cutFrequency):
        content = intorduction[frequency*300:(frequency+1)*300]
        print(content)
        print('*'*20)
        contents.append({
            "type": "bubble",
            "direction": "ltr",
            "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "text",
                "text": content,
                "align": "start",
                "wrap": True
                }
            ]
            }
        })
    intorduction_flex_message = FlexSendMessage(
        alt_text='????????????',
        contents={
            "type": "carousel",
            "contents": contents[:10]
        }
    )
    return(intorduction_flex_message)


def use_actorURL_search_movielist(url):
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
    req = request.Request(url, headers=headers)
    resp = request.urlopen(req)
    respData = str(resp.read().decode('utf-8'))  # ????????????????????????
    soup = BeautifulSoup(respData)

    # movieNameCN ?????????
    # movieNameEN ?????????
    # movieExpectation ?????????
    # movieSatisfactoryDegree ?????????
    # moviePoster ??????
    # movieReleaseTime ????????????
    # movieDetailUrl ??????????????????

    # --------------------movie list
    if soup.select_one(".release_info") == None:
        movie_flex_message = FlexSendMessage(
            alt_text="????????????????????????",
            contents={
                "type": "bubble",
                "direction": "ltr",
                "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                    "type": "text",
                    "text": "????????????????????????",
                    "align": "center"
                    }
                ]
                }
            }
        )
        page = False
        return(movie_flex_message, page)
    else:
        movieInfo = [i for i in soup.select(".release_info")]
        movieInfoText = [i.text for i in soup.select(".release_info")]
        movieNameCN = [i.text.strip() for i in soup.select(".release_movie_name > .gabtn")]
        movieNameEN = []
        for i in soup.select(".en .gabtn"):
            if i.text.strip() == '':
                movieNameEN.append(' ')
            else:
                movieNameEN.append(i.text.strip())
        movieExpectation = []
        for info in movieInfoText:
            movieExpectation.append('?????????') if info.find(
                "?????????") == -1 else movieExpectation.append(info[info.find("?????????")+5:info.find("?????????")+8])
        movieSatisfactoryDegree = []
        if url[-1] == '1':
            for html in movieInfo:
                try:#????????????
                    movieSatisfactoryDegree.append(
                        (html.select("span")[0])["data-num"])
                except:#????????????
                    movieSatisfactoryDegree.append(
                        (html.select("span")[1])["data-num"])
        elif url[-1] == '2':
            for html in movieInfo:
                if html.select(".count") == []:
                    movieSatisfactoryDegree.append("?????????")
                else:
                    movieSatisfactoryDegree.append(
                        (html.select(".count")[0])["data-num"])
        
        moviePoster = [i["data-src"] for i in soup.select(".lazy-load")]
        
        movieReleaseTime = [(i.text)[23:] for i in soup.select(".release_movie_time")]
        movieDetailUrl = [i["href"]
                            for i in soup.select(".release_movie_name > .gabtn")]
        print(movieNameCN)
        print(movieNameEN)
        print(movieExpectation)
        print(movieSatisfactoryDegree)
        print(moviePoster)
        print(movieReleaseTime)
        print(movieDetailUrl)
        # ????????????json??????
        contents = []
        for index in range(len(movieNameCN)):
            contents.append({
                "type": "bubble",
                "direction": "ltr",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [{
                        "type": "text",
                        "text": "??????",
                        "size": "xl",
                        "align": "start",
                        "weight": "bold",
                        "color": "#000000"
                    }]
                },
                "hero": {
                    "type": "image",
                    "url": moviePoster[index],
                    "gravity": "top",
                    "size": "full",
                    "aspectRatio": "1:1.4",
                    "aspectMode": "cover",
                    "backgroundColor": "#FFFFFF"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [{
                        "type": "box",
                        "layout": "vertical",
                        "contents": [{
                            "type": "text",
                            "text": movieNameCN[index],
                            "margin": "none",
                            "size": "lg",
                            "align": "center",
                            "gravity": "top",
                            "weight": "bold"
                        },
                            {
                            "type": "text",
                            "text": movieNameEN[index],
                            "align": "center"
                        }]
                    },
                        {
                        "type": "separator",
                        "margin": "lg",
                        "color": "#FFFFFF"
                    },
                        {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [{
                            "type": "text",
                            "text": "???????????????"
                        },
                            {
                            "type": "text",
                            "text": movieReleaseTime[index]
                        }]
                    },
                        {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [{
                            "type": "text",
                            "text": "????????????",
                            "align": "start",
                            "weight": "bold",
                            "color": "#BB21CA"
                        },
                            {
                            "type": "text",
                            "text": movieExpectation[index]
                        }]
                    },
                        {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [{
                                "type": "text",
                                "text": "????????????",
                                "align": "start",
                                "weight": "bold",
                                "color": "#2133CA"
                        },
                            {
                                "type": "text",
                                "text": movieSatisfactoryDegree[index],
                                "align": "start"
                        }]
                    }
                    ]},
                "footer": {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [{
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "????????????",
                            "data": movieDetailUrl[index]
                        },
                        "color": "#B0B0B0"
                    }]
                }
            })
        # ??????
        movie_flex_message = FlexSendMessage(
            alt_text='????????????',
            contents={
                "type": "carousel",
                "contents": contents
            }
        )

        pagebox_flex_message = pagebox(soup)

        return(movie_flex_message, pagebox_flex_message)



def search_movie_comingsoon(url):
    if url == '':
        url = 'https://movies.yahoo.com.tw/movie_comingsoon.html'
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
    req = request.Request(url, headers=headers)
    resp = request.urlopen(req)
    respData = str(resp.read().decode('utf-8'))  # ????????????????????????
    soup = BeautifulSoup(respData)

    # --------------------movieTab
    #content_l a
    movieTab = [i for i in soup.select(".comingsoon_tab li")]
    print(movieTab)
    contents = []
    monthBoxContents = []
    month = []
    for index in range(len(movieTab)):
        tab = movieTab[index]
        if tab.text[:2] == '20':  # ???
            cnt = 0
            contents.append({
                "type": "text",
                "text": tab.text,
                "size": "lg",
                "margin": "xxl",
                "align": "center",
                "weight": "bold"
            })
        else:
            cnt+=1
            if tab["class"] == ['select']:  # ??????
                thisMonth = tab["class"] == ['select']
                month.append({
                    "type": "text",
                    "text": tab.text,
                    "size": "xl",
                    "weight": "bold",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": tab.a["href"]
                    }
                })
            else:
                month.append({
                    "type": "text",
                    "text": tab.text,
                    "size": "xl",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": tab.a["href"]
                    }
                })
        if cnt == 3:
            cnt = 0
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "margin": "xxl",
                "contents": month[0:3]
            })
            month=[]
        if cnt == len(movieTab):
            cnt = 0
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "margin": "xxl",
                "contents": month[0:3]
            })
            month=[]

    contents.insert(0,{
                "type": "text",
                "text": "????????????",
                "size": "xl",
                "weight": "bold"
                })
    contents.insert(1,
                {
                "type": "separator",
                "margin": "xl",
                "color": "#4B6174"
                })
    movietab_flex_message = FlexSendMessage(
        alt_text='????????????',
        contents={
            "type": "bubble",
            "direction": "ltr",
            "body": {
            "type": "box",
            "layout": "vertical",
            "contents": contents
            }
        }
    )

    # --------------------movieInfo
    print(movietab_flex_message)
    movieInfo = [i.text for i in soup.select(".release_info")]
    if movieInfo == []:
        print("no data")
        movie_flex_message = FlexSendMessage(
            alt_text='???????????????????????????',
            contents={
                "type": "bubble",
                "direction": "ltr",
                "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                    "type": "text",
                    "text": "???????????????????????????????????????",
                    "align": "center",
                    "weight": "bold"
                    }
                ]
                }
            }
        )
        pagebox_flex_message = False
    else:
        movieNameCN = [i.text.strip()
                                    for i in soup.select(".release_movie_name > a")]
        movieNameEN = []
        for i in soup.select(".en a"):
            if i.text.strip() == '':
                movieNameEN.append("-")
            else:
                movieNameEN.append(i.text.strip())

        #movieExpectation = [i.text for i in soup.select("div.leveltext")]
        info_item = soup.find_all('div','release_info')
        movieExpectation = []
        for item in info_item:
            try:
                level = item.find('div','leveltext').span.text.strip()
                movieExpectation.append(level)
            except :
                movieExpectation.append('0')


        movieSatisfactoryDegree = []
        for info in movieInfo:
            if info.find("?????????") == -1:
                movieSatisfactoryDegree.append('?????????') 
            else: 
                movieSatisfactoryDegree.append(info[info.find("?????????")+5:info.find("?????????")+8])
        
        
        moviePoster = [i["data-src"] for i in soup.select(".lazy-load")]
        movieReleaseTime = [(i.text)[23:]
                            for i in soup.select(".release_movie_time")]
        movieDetailUrl = [i["href"]
                            for i in soup.select(".release_movie_name > a")]

        # --------------------
        contents = []
        for index in range(len(movieNameCN)):
            contents.append({
                "type": "bubble",
                "direction": "ltr",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [{
                        "type": "text",
                        "text": "??????",
                        "size": "xl",
                        "align": "start",
                        "weight": "bold",
                        "color": "#000000"
                    }]
                },
                "hero": {
                    "type": "image",
                    "url": moviePoster[index],
                    "gravity": "top",
                    "size": "full",
                    "aspectRatio": "1:1.4",
                    "aspectMode": "cover",
                    "backgroundColor": "#FFFFFF"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [{
                        "type": "box",
                        "layout": "vertical",
                        "contents": [{
                            "type": "text",
                            "text": movieNameCN[index],
                            "margin": "none",
                            "size": "lg",
                            "align": "center",
                            "gravity": "top",
                            "weight": "bold"
                        },
                            {
                            "type": "text",
                            "text": movieNameEN[index],
                            "align": "center"
                        }]
                    },
                        {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [{
                            "type": "text",
                            "text": "???????????????"
                        },
                            {
                            "type": "text",
                            "text": movieReleaseTime[index]
                        }]
                    },
                        {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [{
                            "type": "text",
                            "text": "????????????",
                            "align": "start",
                            "weight": "bold",
                            "color": "#BB21CA"
                        },
                            {
                            "type": "text",
                            "text": movieExpectation[index]
                        }]
                    },
                        {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [{
                                "type": "text",
                                "text": "????????????",
                                "align": "start",
                                "weight": "bold",
                                "color": "#2133CA"
                        },
                            {
                                "type": "text",
                                "text": movieSatisfactoryDegree[index],
                                "align": "start"
                        }]
                    }
                    ]},
                "footer": {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [{
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "????????????",
                            "data": movieDetailUrl[index]
                        }
                    }]
                }
            })
        pagebox_flex_message = pagebox(soup)

        # ??????
        movie_flex_message = FlexSendMessage(
            alt_text='????????????',
            contents={
                "type": "carousel",
                "contents": contents
            }
        )

    return(movietab_flex_message, movie_flex_message, pagebox_flex_message)


def show_chart_message():
    chartSelect_flex_message = FlexSendMessage(
        alt_text='???????????????',
        contents={
            "type": "bubble",
            "direction": "ltr",
            "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "button",
                "action": {
                    "type": "message",
                    "label": "???????????????",
                    "text": "?????????"
                }
                },
                {
                "type": "button",
                "action": {
                    "type": "message",
                    "label": "???????????????",
                    "text": "???????????????"
                }
                },
                {
                "type": "button",
                "action": {
                    "type": "message",
                    "label": "???????????????",
                    "text": "???????????????"
                }
                },
                {
                "type": "separator"
                },
                {
                "type": "button",
                "action": {
                    "type": "message",
                    "label": "???????????????",
                    "text": "???????????????"
                }
                },
                {
                "type": "button",
                "action": {
                    "type": "message",
                    "label": "???????????????",
                    "text": "???????????????"
                }
                }
            ]
            }
        }
    )
    return(chartSelect_flex_message)


def search_movie_chart(url):
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
    req = request.Request(url, headers=headers)
    resp = request.urlopen(req)
    respData = str(resp.read().decode('utf-8'))  # ????????????????????????
    soup = BeautifulSoup(respData)


    if url == "https://movies.yahoo.com.tw/chart.html":
        chartType = "???????????????"
    elif url == "https://movies.yahoo.com.tw/chart.html?cate=us":
        chartType = "???????????????"
    elif url == "https://movies.yahoo.com.tw/chart.html?cate=year":
        chartType = "???????????????"
    else:
        chartType = "?????????"

    movieRank = [i.text for i in soup.select(".tr+ .tr .td:nth-child(1)")]
    movieRankTypeDiv = [i for i in soup.select(".up , .new , .down")]
    movieRankType = []
    for div in movieRankTypeDiv:
        if div["class"][1] == "new":
            movieRankType.append("????")
        if div["class"][1] == "up":
            movieRankType.append("??????")
        if div["class"][1] == "down":
            movieRankType.append("??????")
    movieNameCN = [i.text for i in soup.select(".rank_txt , h2")]
    movieReleaseTime = [i.text for i in soup.select(".tr+ .tr .td:nth-child(5)")]
    movieSatisfactoryDegree = [i.text.strip()
                                            for i in soup.select(".starwithnum")]
    movieURLHTML = [i for i in soup.select(
        ".up~ .td:nth-child(4) , .down~ .td:nth-child(4) , .new~ .td:nth-child(4)")]
    movieURL = []
    for html in movieURLHTML:
        if html.a != None:
            movieURL.append(html.a["href"])
        else:
            movieURL.append("????????????")
    contents = []
    for index in range(int(len(movieNameCN)/5)):
        rankContents =[]
        for index2 in range(5):
            now = (index*5)+index2 # 1~max
            if movieSatisfactoryDegree[now] == '':
                movieSatisfactoryDegree[now] = '???????????????'

            if movieSatisfactoryDegree[now] == '???????????????':
                star = "????????????"
            elif int(float(movieSatisfactoryDegree[now])) == 0 :
                star = "???"
            else:
                star = int(float(movieSatisfactoryDegree[now]))*'???'

            if star[0]=="???":
                starColor = "#FF7100"
            else:
                starColor = "#000000"

            if now == 0:
                medal = "????"
            elif now == 1:
                medal = "????"
            elif now == 2:
                medal = "????"
            else:
                medal = ""

            rankContents.append({
                "type": "box",
                "layout": "vertical",
                "margin": "md",
                "action": {
                    "type": "postback",
                    "data": movieURL[now]
                },
                "contents": [
                    {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "md",
                    "contents": [
                        {
                        "type": "text",
                        "text": movieRank[now] + medal,
                        "size": "lg",
                        "weight": "bold"
                        }
                    ]
                    },
                    {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                        "type": "text",
                        "text": movieReleaseTime[now],
                        "flex": 3
                        },
                        {
                        "type": "text",
                        "text": movieSatisfactoryDegree[now],
                        "flex": 0,
                        "align": "end"
                        },
                        {
                        "type": "text",
                        "text": star,
                        "flex": 0,
                        "color": starColor,
                        "align": "start"
                        }
                    ]
                    },
                    {
                    "type": "text",
                    "text": movieNameCN[now],
                    "size": "lg",
                    "weight": "bold"
                    }
                ]
            })
            rankContents.append({
                "type": "separator",
                "margin": "md"
            })



        rankContents.insert(0,{
                    "type": "text",
                    "text": chartType,
                    "size": "xl",
                    "weight": "bold"
                    })
        rankContents.insert(1,
                    {
                    "type": "separator",
                    "margin": "xl",
                    "color": "#4B6174"
                    })

        contents.append({
            "type": "bubble",
            "direction": "ltr",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": rankContents
            }
        })
    movierank_flex_message = FlexSendMessage(
        alt_text='?????????',
        contents={
            "type": "carousel",
            "contents": contents
        }
    )

    dataImg = "https://movies.yahoo.com.tw"+soup.select_one("a.gabtn img")["src"]
    dataDate = soup.select_one(".rank_time").text[5:]
    data_flex_message = FlexSendMessage(
        alt_text='chartdata',
        contents={
            "type": "bubble",
            "direction": "ltr",
            "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "text",
                "text": "???????????????",
                "flex": 0,
                },
                {
                "type": "text",
                "text": dataDate,
                "align": "start"
                },
                {
                "type": "text",
                "text": "???????????????",
                "flex": 0,
                "margin": "md",
                "align": "start"
                },
                {
                "type": "image",
                "url": dataImg,
                "flex": 0,
                "align": "start",
                "aspectRatio": "4:1",
                "aspectMode": "fit",
                "backgroundColor": "#FFFFFF"
                }
            ]
            }
        }
    )
    return(movierank_flex_message, data_flex_message)


def search_movie_chartNetizens(url):
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
    req = request.Request(url, headers=headers)
    resp = request.urlopen(req)
    respData = str(resp.read().decode('utf-8'))  # ????????????????????????
    soup = BeautifulSoup(respData)


    if url == "https://movies.yahoo.com.tw/chart.html?cate=exp_30":
        chartType = "???????????????"
    elif url == "https://movies.yahoo.com.tw/chart.html?cate=rating":
        chartType = "???????????????"
    elif url == "https://movies.yahoo.com.tw/chart.html?cate=year":
        chartType = "???????????????"
    else:
        chartType = "?????????"

    movieRank = [i.text for i in soup.select(".tr+ .tr .td:nth-child(1)")]
    movieNameCN = [i.text for i in soup.select(".rank_txt , h2")]
    movieReleaseTime = [i.text for i in soup.select(".tr+ .tr .td:nth-child(3)")]
    movieSatisfactory = [i.text for i in soup.select("h6")]
    movieVotes = [i.text for i in soup.select("h4")]
    movieURLHTML = [i for i in soup.select(
        ".tr+ .tr .td:nth-child(2)")]
    movieURL = []
    for html in movieURLHTML:
        if html.a != None:
            movieURL.append(html.a["href"])
        else:
            movieURL.append("????????????")

    contents = []
    for index in range(int(len(movieNameCN)/5)):
        rankContents =[]
        for index2 in range(5):
            now = (index*5)+index2 # 1~max
            if movieSatisfactory[now] == '':
                movieSatisfactory[now] = '???????????????'

            if movieSatisfactory[now] == '???????????????':
                star = "????????????"
            elif int(float(movieSatisfactory[now])) == 0 :
                star = "???"
            elif int(float(movieSatisfactory[now])) > 5:
                star = "?????????"
            else:
                star = int(float(movieSatisfactory[now]))*'???'
            
            if star[0]=="???":
                starColor = "#FF7100"
            else:
                starColor = "#000000"

            if now == 0:
                medal = "????"
            elif now == 1:
                medal = "????"
            elif now == 2:
                medal = "????"
            else:
                medal = ""
            rankContents.append({
                "type": "box",
                "layout": "vertical",
                "margin": "md",
                "action": {
                    "type": "postback",
                    "data": movieURL[now]
                },
                "contents": [
                    {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "md",
                    "contents": [
                        {
                        "type": "text",
                        "text": movieRank[now] + medal,
                        "size": "lg",
                        "weight": "bold"
                        },
                        {
                        "type": "text",
                        "text": movieVotes[now],
                        "align": "end"
                        }
                    ]
                    },
                    {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                        "type": "text",
                        "text": movieReleaseTime[now],
                        "flex": 3
                        },
                        {
                        "type": "text",
                        "text": movieSatisfactory[now],
                        "flex": 0,
                        "align": "end"
                        },
                        {
                        "type": "text",
                        "text": star,
                        "flex": 0,
                        "color": starColor,
                        "align": "start"
                        }
                    ]
                    },
                    {
                    "type": "text",
                    "text": movieNameCN[now],
                    "size": "lg",
                    "weight": "bold"
                    }
                ]
            })
            rankContents.append({
                "type": "separator",
                "margin": "md"
            })


        rankContents.insert(0,{
                    "type": "text",
                    "text": chartType,
                    "size": "xl",
                    "weight": "bold"
                    })
        rankContents.insert(1,
                    {
                    "type": "separator",
                    "margin": "xl",
                    "color": "#4B6174"
                    })

        contents.append({
            "type": "bubble",
            "direction": "ltr",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": rankContents
            }
        })

    

    movierank_flex_message = FlexSendMessage(
        alt_text='?????????',
        contents={
            "type": "carousel",
            "contents": contents
        }
    )

    dataFrom = soup.select(".rank_data span")[1].text
    data_flex_message = FlexSendMessage(
        alt_text='?????????',
        contents={
            "type": "bubble",
            "direction": "ltr",
            "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [                
                {
                "type": "text",
                "text": "???????????????",
                "flex": 0,
                "margin": "md",
                "align": "start"
                },
                {
                "type": "text",
                "text": dataFrom,
                "flex": 0,
                "margin": "md",
                "align": "start",
                "wrap": True
                }
            ]
            }
        }
    )
    return(movierank_flex_message, data_flex_message)

def select_movie_type():
    '''
    1??????
    2??????
    3??????
    4??????
    5??????
    6??????
    7??????
    8????????????
    9??????
    10??????
    11????????????
    12??????
    13??????
    14????????????
    15????????????
    16?????????
    17??????
    18??????
    19??????
    '''
    movieType_flex_message = FlexSendMessage(
        alt_text='??????????????????',
        contents={
            "type": "bubble",
            "direction": "ltr",
            "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "text",
                "text": "???????????????",
                "size": "xl",
                "align": "start",
                "weight": "bold"
                },
                {
                "type": "separator",
                "margin": "md",
                "color": "#4B6174"
                },
                {
                "type": "box",
                "layout": "horizontal",
                "margin": "lg",
                "contents": [
                    {
                    "type": "text",
                    "text": "??????",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "??????"
                    }
                    },
                    {
                    "type": "text",
                    "text": "??????",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "??????"
                    }
                    },
                    {
                    "type": "text",
                    "text": "??????",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "??????"
                    }
                    }
                ]
                },
                {
                "type": "box",
                "layout": "horizontal",
                "margin": "lg",
                "contents": [
                    {
                    "type": "text",
                    "text": "??????",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "??????"
                    }
                    },
                    {
                    "type": "text",
                    "text": "??????",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "??????"
                    }
                    },
                    {
                    "type": "text",
                    "text": "??????",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "??????"
                    }
                    }
                ]
                },
                {
                "type": "box",
                "layout": "horizontal",
                "margin": "lg",
                "contents": [
                    {
                    "type": "text",
                    "text": "??????",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "??????"
                    }
                    },
                    {
                    "type": "text",
                    "text": "????????????",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "????????????"
                    }
                    },
                    {
                    "type": "text",
                    "text": "??????",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "??????"
                    }
                    }
                ]
                },
                {
                "type": "box",
                "layout": "horizontal",
                "margin": "lg",
                "contents": [
                    {
                    "type": "text",
                    "text": "??????",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "??????"
                    }
                    },
                    {
                    "type": "text",
                    "text": "????????????",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "????????????"
                    }
                    },
                    {
                    "type": "text",
                    "text": "??????",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "??????"
                    }
                    }
                ]
                },
                {
                "type": "box",
                "layout": "horizontal",
                "margin": "lg",
                "contents": [
                    {
                    "type": "text",
                    "text": "??????",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "??????"
                    }
                    },
                    {
                    "type": "text",
                    "text": "????????????",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "????????????"
                    }
                    },
                    {
                    "type": "text",
                    "text": "????????????",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "????????????"
                    }
                    }
                ]
                },
                {
                "type": "box",
                "layout": "horizontal",
                "margin": "lg",
                "contents": [
                    {
                    "type": "text",
                    "text": "?????????",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "?????????"
                    }
                    },
                    {
                    "type": "text",
                    "text": "??????",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "??????"
                    }
                    },
                    {
                    "type": "text",
                    "text": "??????",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "??????"
                    }
                    }
                ]
                },
                {
                "type": "box",
                "layout": "horizontal",
                "margin": "lg",
                "contents": [
                    {
                    "type": "text",
                    "text": "??????",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "??????"
                    }
                    }
                ]
                }
            ]
            }
        }
    )

    return(movieType_flex_message)


def search_movie_type(typeName, url):
    if typeName == '':
        movieURL = url
    else:
        movieTypeDition = {
            "1": "??????",
            "2": "??????",
            "3": "??????",
            "4": "??????",
            "5": "??????",
            "6": "??????",
            "7": "??????",
            "8": "????????????",
            "9": "??????",
            "10": "??????",
            "11": "????????????",
            "12": "??????",
            "13": "??????",
            "14": "????????????",
            "15": "????????????",
            "16": "?????????",
            "17": "??????",
            "18": "??????",
            "19": "??????"
        }
        typeNo = list(movieTypeDition.keys())[
                      list(movieTypeDition.values()).index(typeName)]
        # ????????????URL
        movieURL = 'https://movies.yahoo.com.tw/moviegenre_result.html?genre_id='+typeNo+'&page=1'

    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
    req = request.Request(movieURL, headers=headers)
    resp = request.urlopen(req)
    respData = str(resp.read().decode('utf-8'))
    soup = BeautifulSoup(respData, "html.parser")

    movieNameCN = [i.text.strip()
                                for i in soup.select(".release_movie_name > .gabtn")]
    movieNameEN = []
    for i in soup.select(".en .gabtn"):
        if i.text.strip() == '':
            movieNameEN.append("-")
        else:
            movieNameEN.append(i.text.strip())
    movieInfo = [i for i in soup.select(".release_movie_name")]
    movieExpectation = []

    
    info_item = soup.find_all('div','release_info')
    for item in info_item:
        try:
            level = item.find('div','leveltext').span.text.strip()
            movieExpectation.append(level)
        except :
            movieExpectation.append('0')

    
    movieSatisfactoryDegree = []
    for html in movieInfo:
        movieExpectation.append(html.select("span")[0].text)
        try:
            movieSatisfactoryDegree.append(
                (html.select("span")[1])["data-num"])
        except:
            movieSatisfactoryDegree.append("?????????")
    moviePoster = [i["data-src"] for i in soup.select(".lazy-load")]
    movieReleaseTime = [(i.text)[23:]
                         for i in soup.select(".release_movie_time")]
    movieDetailUrl = [i["href"]
                        for i in soup.select(".release_movie_name > .gabtn")]
    # ????????????json??????
    contents = []
    for index in range(len(movieNameCN)):
        contents.append({
            "type": "bubble",
            "direction": "ltr",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [{
                    "type": "text",
                    "text": "??????",
                    "size": "xl",
                    "align": "start",
                    "weight": "bold",
                    "color": "#000000"
                }]
            },
            "hero": {
                "type": "image",
                "url": moviePoster[index],
                "gravity": "top",
                "size": "full",
                "aspectRatio": "1:1.4",
                "aspectMode": "cover",
                "backgroundColor": "#FFFFFF"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [{
                    "type": "box",
                    "layout": "vertical",
                    "contents": [{
                        "type": "text",
                        "text": movieNameCN[index],
                        "margin": "none",
                        "size": "lg",
                        "align": "center",
                        "gravity": "top",
                        "weight": "bold"
                    },
                        {
                        "type": "text",
                        "text": movieNameEN[index],
                        "align": "center"
                    }]
                },
                    {
                    "type": "separator",
                    "margin": "lg",
                    "color": "#FFFFFF"
                },
                    {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [{
                        "type": "text",
                        "text": "???????????????"
                    },
                        {
                        "type": "text",
                        "text": movieReleaseTime[index]
                    }]
                },
                    {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [{
                        "type": "text",
                        "text": "????????????",
                        "align": "start",
                        "weight": "bold",
                        "color": "#BB21CA"
                    },
                        {
                        "type": "text",
                        "text": movieExpectation[index]
                    }]
                },
                    {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [{
                            "type": "text",
                            "text": "????????????",
                            "align": "start",
                            "weight": "bold",
                            "color": "#2133CA"
                    },
                        {
                            "type": "text",
                            "text": movieSatisfactoryDegree[index],
                            "align": "start"
                    }]
                }
                ]},
            "footer": {
                "type": "box",
                "layout": "horizontal",
                "contents": [{
                    "type": "button",
                    "action": {
                        "type": "postback",
                        "label": "????????????",
                        "data": movieDetailUrl[index]
                    }
                }]
            }
        })
    # ??????
    movie_flex_message = FlexSendMessage(
        alt_text='????????????',
        contents={
            "type": "carousel",
            "contents": contents
        }
    )

    pagebox_flex_message = pagebox(soup)

    return(movie_flex_message, pagebox_flex_message)

#ok
def show_location_message():
    location_flex_message = TemplateSendMessage(
        alt_text='?????????????????????',
        template=ButtonsTemplate(
            title='???????????????',
            text='?????????????????????????????????????????????????????????????????????',
            size='lg',
            weight='bold',
            actions=[LocationAction(label='??????????????????')]
        )
    )
    return(location_flex_message)


def use_location_search_movietheater(userAddress, userLat, userLng):
    import googlemaps

    googleAPIKey = "..."#google api  key
    gmaps = googlemaps.Client(key=googleAPIKey)
    nearbyMovietheater = googlemaps.places.places_nearby(location=(userLat,userLng), rank_by="distance", language="zh-TW", keyword="??????", client=gmaps)
    
    print("movie theater is at "+ str(nearbyMovietheater))
    movietheaterName = []
    movietheaterLat = []
    movietheaterLng = []
    movietheaterPhotos = []
    movietheaterRating = []
    movietheaterAddress = []
    movietheaterDistance = []
    for data in nearbyMovietheater["results"]:
        if data["name"].find("??????????????????") == -1:
            movietheaterName.append(data["name"])
            movietheaterLat.append(data["geometry"]["location"]["lat"])
            movietheaterLng.append(data["geometry"]["location"]["lng"])
            distance = getDistance(userLat,userLng,data["geometry"]["location"]["lat"],data["geometry"]["location"]["lng"])
            movietheaterDistance.append(distance)
            if distance < 2:
                movietheaterPhotos.append("https://i.imgur.com/5HQbSSD.png")
            elif distance < 6:
                movietheaterPhotos.append("https://i.imgur.com/Xfu8rQU.png")
            elif distance < 10:
                movietheaterPhotos.append("https://i.imgur.com/3s4OfPN.png")
            elif distance <30:
                movietheaterPhotos.append("https://i.imgur.com/HW88JUy.png")
            else:
                movietheaterPhotos.append("https://i.imgur.com/GfGsFuy.png")
            movietheaterRating.append(data["rating"])
            movietheaterAddress.append(data["vicinity"])
    contents = []
    if len(movietheaterName)==0:
        movietheater_flex_message = FlexSendMessage(
            alt_text='?????????????????????',
            contents={
                "type": "bubble",
                "direction": "ltr",
                "body": {"type": "box", "layout": "vertical",
                "contents": [{"type": "text", "text": "????????????????????????", "align": "center"}]}
            }
        )
    else:
        #output 10 theater
        for index in range(len(movietheaterName[:10])):
            contents.append({
                "type": "bubble",
                "direction": "ltr",
                "header": {"type": "box", "layout": "vertical",
                "contents": 
                [{
                    "type": "text",
                    "text": movietheaterName[index],
                    "size": "xl", "align": "start", "weight": "bold"}]
                    },
                "hero": {
                "type": "image",
                "url": movietheaterPhotos[index],
                "size": "xxl",
                "aspectRatio": "1.91:1",
                "aspectMode": "fit"
                },
                "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                    "type": "text",
                    "text": movietheaterName[index],
                    "align": "start"
                    },
                    {
                    "type": "text",
                    "text": movietheaterAddress[index]
                    },
                    {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                        "type": "text",
                        "text": "??????",
                        "flex": 0,
                        "gravity": "bottom"
                        },
                        {
                        "type": "text",
                        "text": str(movietheaterRating[index]),
                        "size": "xl"
                        }
                    ]
                    },
                    {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                        "type": "text",
                        "text": "??????",
                        "flex": 0,
                        "gravity": "bottom"
                        },
                        {
                        "type": "text",
                        "text": str(movietheaterDistance[index]),
                        "flex": 0,
                        "size": "xl"
                        },
                        {
                        "type": "text",
                        "text": "??????",
                        "align": "start",
                        "gravity": "bottom"
                        }
                    ]
                    }
                ]},

                "footer": {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                    "type": "button",
                    "action": {
                        "type": "postback",
                        "label": "????????????",
                        "data": "???????????????"+movietheaterName[index]+":1"
                    }
                    },
                    {
                    "type": "button",
                    "action": {
                        "type": "postback",
                        "label": "????????????",
                        "data": "?????????????????????"+"name"+movietheaterName[index]+"address"+movietheaterAddress[index]+"lat"+str(movietheaterLat[index])+"lng"+str(movietheaterLng[index])
                    }
                    }
                ]
                }
            })

        movietheater_flex_message = FlexSendMessage(
            alt_text='???????????????',
            contents={
                "type": "carousel",
                "contents": contents
            }
        )
    return(movietheater_flex_message)

def use_movietheatherName_search_movie(movietheaterName, page):

    #??????google????????????????????????(google???????????????????????????????????????????????????)
    movietheaterNameQuote = parse.quote(movietheaterName)
    googleSearchURL = "https://www.google.com/search?ei=cn&q="+movietheaterNameQuote+"+site%3Ahttp%3A%2F%2Fwww.atmovies.com.tw%2F"
    #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
    req = request.Request(googleSearchURL, headers=headers)
    resp = request.urlopen(req)
    respData = str(resp.read().decode('utf-8'))  # ????????????????????????
    soup = BeautifulSoup(respData)

   # movietheaterURL = soup.select_one("#res .r a")["href"]
    movietheaterURL = soup.select_one("div .yuRUbf a")["href"]

    #???????????????
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
    req = request.Request(movietheaterURL, headers=headers)
    resp = request.urlopen(req)
    respData = str(resp.read().decode('utf-8'))  # ????????????????????????
    soup = BeautifulSoup(respData)

    # movieList = [i for i in soup.findAll('ul',{'id':'theaterShowtimeTable'})]
    # for movieInfo in movieList[(int(page)-1)*10:int(page)*10]:
    #     print("movieName"+movieInfo.select_one("a").text)
    #     for ul in movieInfo.select("ul ul li")[:-1]:
    #         print("***")
    #         print(ul)
    movietheaterContents = []
    movieList = [i for i in soup.findAll('ul',{'id':'theaterShowtimeTable'})]
    movieContents = []
    for movieInfo in movieList[(int(page)-1)*10:int(page)*10]:
        movieName = movieInfo.select_one("a").text
        timeContents = []
        cnt=0
        
        for movietime in movieInfo.select("ul + ul li")[:-1]:
            try:
                href = movietime.select_one("a")["href"]
            except:
                href = None

            print("*"*5)
            print(movietime.text)
            if len(movietime.text) >10:
                print("NO")
            elif movietime.text.strip() == movieName:
                print("NO")
            elif movietime.text.strip()[:2] == "??????":
                print("NO")
            elif movietime.text.strip() == "":
                print("NO")
            elif href != None and (movietime.text[-1] == "0" or movietime.text[-1] == "5"):
                timeContents.append({
                    "type": "box",
                    "layout": "vertical",
                    "margin": "md",
                    "contents": [                        
                        {
                        "type": "button",
                        "action": {
                            "type": "uri",
                            "label": movietime.text ,#+ useTimeGetTimeEmoji(int(movietime.text[:2]), int(movietime.text[3:5])),
                            "uri": 'http://www.atmovies.com.tw'+href
                        },
                        "color": "#000000"
                        },
                        {
                        "type": "separator",
                        "margin": "md"
                        }
                    ]
                })
            elif movietime.text.replace("???",":") > time.strftime("%H:%M", time.localtime(time.time())) and (movietime.text[-1] == "0" or movietime.text[-1] == "5"):
                timeContents.append({
                    "type": "box",
                    "layout": "vertical",
                    "margin": "md",
                    "contents": [
                        {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": movietime.text ,#+ useTimeGetTimeEmoji(int(movietime.text[:2]), int(movietime.text[3:5])),
                            "data": "????????????????????????"
                        },
                        "color": "#000000"
                        },
                        {
                        "type": "separator",
                        "margin": "md"
                        }
                    ]
                })
            elif movietime.text[-1] == "0" or movietime.text[-1] == "5":
                timeContents.append({
                    "type": "box",
                    "layout": "vertical",
                    "margin": "md",
                    "contents": [
                        {
                        "type": "text",
                        "text": movietime.text,
                        "size": "sm",
                        "align": "center",
                        "color": "#C1C1C1"
                        },
                        {
                        "type": "separator",
                        "margin": "sm"
                        }
                    ]
                })
            else:
                timeContents.append({
                    "type": "box",
                    "layout": "vertical",
                    "margin": "md",
                    "contents": [
                        {
                        "type": "text",
                        "text": movietime.text,
                        "size": "lg",
                        "align": "center",
                        "weight": "bold"
                        },
                        {
                        "type": "separator",
                        "margin": "md"
                        }
                    ]
                })
        movieContents.append({
            "type": "bubble",
            "direction": "ltr",
            "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "text",
                "text": movieName,
                "size": "xl",
                "align": "start",
                "weight": "bold",
                "wrap": True,
                "action": {
                    "type": "message",
                    "text": movieName
                }
                }
            ]
            },
            "body": {
            "type": "box",
            "layout": "vertical",
            "contents": timeContents
            }
        })

    movie_flex_message = FlexSendMessage(
        alt_text='????????????',
        contents={
            "type": "carousel",
            "contents": movieContents
        }
    )

    totalPage = int(len(soup.select(".filmTitle a"))/10)
    print(totalPage)
    if totalPage>1 :
        nowPage = int(page)
        print(nowPage)
        contents = []
        for index in range(totalPage):
            if index+1 != nowPage:
                contents.append({
                    "type": "text",
                    "text": str(index+1),
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "???????????????"+movietheaterName+":"+str(index+1)
                    }
                })
        # ??????
        pagebox_flex_message = FlexSendMessage(
            alt_text='??????',
            contents={
                "type": "bubble",
                "direction": "ltr",
                "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                    "type": "text",
                    "text": "?????????"+str(nowPage)+"???",
                    "align": "center"
                    },
                    {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "xl",
                    "contents": contents
                    }
                ]
                }
            }
        )
    else:
        pagebox_flex_message = False
    movietheaterName_flex_message = FlexSendMessage(
        alt_text=movietheaterName,
        contents={
            "type": "bubble",
            "direction": "ltr",
            "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "text",
                "text": movietheaterName,
                "align": "center"
                }
            ]
            }
        }
    )
    return(movietheaterName_flex_message, movie_flex_message, pagebox_flex_message)
    #---------------------------------------------------------------------
#ok
def use_movietheaterInfo_get_locationMessage(movietheaterName, movietheaterAddress, movietheaterLat, movietheaterLng):
    location_message = LocationSendMessage(
        title=movietheaterName,
        address=movietheaterAddress,
        latitude=float(movietheaterLat),
        longitude=float(movietheaterLng)
    )
    return(location_message)

def get_MovieMoment():
    url = 'http://www.atmovies.com.tw/movie/new/'
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
    req = request.Request(url, headers=headers)
    resp = request.urlopen(req)
    respData = str(resp.read().decode('utf-8'))  # ????????????????????????
    #respData = str(resp.read().decode('utf-8'))  # ????????????????????????

    soup = BeautifulSoup(respData)
    movieOption = [i for i in soup.select("form:nth-child(3) select option")][1:]
    movieName = []
    movieURL = []
    movieID = []
    movieSelectContents = []
    for option in movieOption:
        if option.text[0] == "???":
            movieName.append("????"+option.text[1:])
        else:
            movieName.append(option.text)
        movieURL.append(option["value"])
        movieID.append(option["value"][33:-1])

    print(len(movieName))
    for page in range(int(len(movieName)/10)):
        movieNameContents = []
        for index in range(int(page)*10,int(page+1)*10):
            movieNameContents.append({
                "type": "box",
                "layout": "vertical",
                "margin": "lg",
                "action": {
                    "type": "postback",
                    "data": "??????????????????"+movieURL[index]+"|"+movieID[index]+"@"+movieName[index]
                },
                "contents": [
                    {
                    "type": "text",
                    "text": movieName[index],
                    "size": "lg"
                    },
                    {
                    "type": "separator",
                    "margin": "lg"
                    }
                ]
            })

        movieNameContents.insert(0,{
                    "type": "text",
                    "text": "????????????",
                    "size": "xl",
                    "weight": "bold"
                    })
        movieNameContents.insert(1,
                    {
                    "type": "separator",
                    "margin": "xl",
                    "color": "#4B6174"
                    })
        movieSelectContents.append({
            "type": "bubble",
            "direction": "ltr",
            "body": {
            "type": "box",
            "layout": "vertical",
            "contents": movieNameContents
            }
        })
    
    movieSelect_flex_message = FlexSendMessage(
        alt_text='?????????????????????',
        contents={
            "type": "carousel",
            "contents": movieSelectContents
        }
    )
    return(movieSelect_flex_message)

def use_movieurl_get_movieReleasedArea(movieURL, movieID, movieName):
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
    req = request.Request(movieURL, headers=headers)
    resp = request.urlopen(req)
    respData = str(resp.read().decode('utf-8'))  # ????????????????????????
    soup = BeautifulSoup(respData)
    
    if movieName[0] == "????":
        movieName = movieName[1:]
    name_flex_message = FlexSendMessage(
        alt_text='?????????',
        contents={
            "type": "bubble",
            "direction": "ltr",
            "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "text",
                "text": movieName,
                "align": "center",
                "weight": "bold"
                }
            ]
            }
        }
    )
    try:
        areaOption = [i for i in soup.select(".movie_theater select option")][1:]
        areaContent = []
        areaCnt = 0
        areaDict = {}
        for area in areaOption:
            areaCnt+=1
            areaName = area.text.strip()
            areaID = area["value"][-5:]
            areaDict[areaID] = areaName
            areaContent.append({
            "type": "button",
            "action": {
                "type": "postback",
                "label": areaName,
                "data": "????????????"+movieID+areaID+",1"
            }
            })
        print(areaName)
        print(areaID)
        print(areaDict)
        areaMessageContents = []
        for contentIndex in range(int(areaCnt/4)+1):
            contentsAreaContent = []
            for areaIndex in range(4):
                try:
                    contentsAreaContent.append(areaContent[contentIndex*4+areaIndex])
                except:
                    contentsAreaContent.append({"type": "filler"})
            areaMessageContents.append({
                "type": "bubble",
                "direction": "ltr",
                "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                    "type": "text",
                    "text": "????????????????????????",
                    "size": "lg",
                    "align": "center"
                    },
                    {
                    "type": "separator",
                    "margin": "lg",
                    "color": "#4B6174"
                    },
                    {
                    "type": "box",
                    "layout": "vertical",
                    "contents": contentsAreaContent
                    }
                ]
                }
            })
        area_flex_message = FlexSendMessage(
            alt_text='????????????',
            contents={
                "type": "carousel",
                "contents": areaMessageContents
            }
        )
    except:
        area_flex_message = FlexSendMessage(
            alt_text='?????????????????????????????????????????????',
            contents={
                "type": "bubble",
                "direction": "ltr",
                "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                    "type": "text",
                    "text": "?????????????????????????????????????????????",
                    "align": "center",
                    "weight": "bold",
                    "wrap": True
                    }
                ]
                }
            }
        )
    
    return(name_flex_message, area_flex_message)

def use_movieurl_get_movieMoment(movieID, inAreaID, page):
    url = 'http://www.atmovies.com.tw/showtime/'+movieID+inAreaID
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
    req = request.Request(url, headers=headers)
    resp = request.urlopen(req)
    respData = str(resp.read().decode('utf-8'))  # ????????????????????????
    soup = BeautifulSoup(respData)

    
    movietheaterContents = []
    movietheaterData = [i for i in soup.select("#filmShowtimeBlock ul")]
    for content in movietheaterData[(int(page)-1)*10:int(page)*10]:
        movietheaterName = content.find("li").text
        timeContents = []
        cnt=0
        if content.select_one(".filmVersion") != None:
            cnt+=1
            if cnt>1 : break
            timeContents.append({
                "type": "box",
                "layout": "vertical",
                "margin": "md",
                "contents": [
                    {
                    "type": "text",
                    "text": (content.select("li")[1]).text.split('\n')[0],
                    "size": "lg",
                    "align": "center",
                    "weight": "bold"
                    },
                    {
                    "type": "separator",
                    "margin": "md"
                    }
                ]
            })
        for movietime in [i for i in content.select("li")][2:]:
            #now=time.strftime("%H:%M", time.localtime(time.time()+28800))
            print(movietime.text.replace("???",":") > time.strftime("%H:%M", time.localtime()))
            print(movietime.text.replace("???",":")+"<-movie "+" now->"+time.strftime("%H:%M", time.localtime()))
            if len(movietime.text)>9:#????????????????????? ????????????????????????
                print("no")
            elif movietime.find("a") != None:#???????????????(?????????????????????)
                print('http://www.atmovies.com.tw'+movietime.find("a")["href"])
                timeContents.append({
                    "type": "box",
                    "layout": "vertical",
                    "margin": "md",
                    "contents": [                        
                        {
                        "type": "button",
                        "action": {
                            "type": "uri",
                            "label": movietime.text ,#+ useTimeGetTimeEmoji(int(movietime.text[:2]), int(movietime.text[3:5])),
                            "uri": 'http://www.atmovies.com.tw'+movietime.find("a")["href"]
                        },
                        "color": "#000000"
                        },
                        {
                        "type": "separator",
                        "margin": "md"
                        }
                    ]
                })
            elif movietime.text.replace("\n","").replace("\r","").replace("???",":") > time.strftime("%H:%M", time.localtime()):#?????????????????? ??????????????????
                timeContents.append({
                    "type": "box",
                    "layout": "vertical",
                    "margin": "md",
                    "contents": [                        
                        {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": movietime.text ,#+ useTimeGetTimeEmoji(int(movietime.text[:2]), int(movietime.text[3:5])),
                            "data": "????????????????????????"
                        },
                        "color": "#000000"
                        },
                        {
                        "type": "separator",
                        "margin": "md"
                        }
                    ]
                })
            else:#??????????????????
                timeContents.append({
                    "type": "box",
                    "layout": "vertical",
                    "margin": "md",
                    "contents": [
                        {
                        "type": "text",
                        "text": movietime.text,
                        "size": "sm",
                        "align": "center",
                        "color": "#C1C1C1"
                        },
                        {
                        "type": "separator",
                        "margin": "sm"
                        }
                    ]
                })
        movietheaterContents.append({
            "type": "bubble",
            "direction": "ltr",
            "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "text",
                "text": movietheaterName,
                "size": "xl",
                "align": "start",
                "weight": "bold",
                "wrap": True,
                "action": {
                    "type": "text",
                    "text": "?????????"+movietheaterName
                }
                },
                {
                "type": "separator",
                "margin": "xl",
                "color": "#4B6174"
                }
            ]
            },
            "body": {
            "type": "box",
            "layout": "vertical",
            "contents": timeContents
            }
        })

    movietheater_flex_message = FlexSendMessage(
        alt_text='???????????????',
        contents={
            "type": "carousel",
            "contents": movietheaterContents
        }
    )

    totalPage = int(len(movietheaterData)/10)
    print(totalPage)
    if totalPage>1 :
        nowPage = int(page)
        print(nowPage)
        contents = []
        for index in range(totalPage):
            if index+1 != nowPage:
                contents.append({
                    "type": "text",
                    "text": str(index+1),
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "????????????"+movieID+inAreaID+","+str(index+1)
                    }
                })
        # ??????
        pagebox_flex_message = FlexSendMessage(
            alt_text='??????',
            contents={
                "type": "bubble",
                "direction": "ltr",
                "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                    "type": "text",
                    "text": "?????????"+str(nowPage)+"???",
                    "align": "center"
                    },
                    {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "xl",
                    "contents": contents
                    }
                ]
                }
            }
        )
    else:
        pagebox_flex_message = False

    movieName = soup.select_one("h2 a").text
    movieNameCN = movieName[:movieName.find(" ")]
    movieNameEN = movieName[movieName.find(" ")+1:]
    movieDetail = soup.select_one(".runtimeText").text
    movieRuntime = movieDetail[movieDetail.find("?????????")+3:movieDetail.find("???")+1]
    movieReleaseTime = movieDetail[movieDetail.find("???????????????")+5:movieDetail.find("??????")+-1]
    movieInfo_flex_message = FlexSendMessage(
        alt_text='??????',
        contents={
            "type": "bubble",
            "direction": "ltr",
            "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "text",
                "text": movieNameCN,
                "size": "md",
                "align": "center",
                "weight": "bold",
                "wrap": True
                },
                {
                "type": "text",
                "text": movieNameEN,
                "size": "sm",
                "align": "center",
                "wrap": True
                },
                {
                "type": "box",
                "layout": "horizontal",
                "margin": "lg",
                "contents": [
                    {
                    "type": "text",
                    "text": "?????????",
                    "align": "end"
                    },
                    {
                    "type": "text",
                    "text": movieRuntime
                    }
                ]
                },
                {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                    "type": "text",
                    "text": "???????????????",
                    "align": "end"
                    },
                    {
                    "type": "text",
                    "text": movieReleaseTime
                    }
                ]
                },
                {
                "type": "separator",
                "margin": "xl"
                }
            ]
            },
            "footer": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                "type": "button",
                "action": {
                    "type": "message",
                    "label": "????????????",
                    "text": movieNameCN
                }
                },                
                {
                "type": "button",
                "action": {
                    "type": "message",
                    "label": "????????????",
                    "text": '??????'+movieNameCN
                }
                }
            ]
            }
        }        
    )
    areaDict = {"/a01/":"??????","/a02/":"??????","/a03/":"??????","/a35/":"??????","/a37/":"??????","/a04/":"??????","/a47/":"??????","/a45/":"??????","/a49/":"??????","/a05/":"??????","/a06/":"??????","/a07/":"??????","/a39/":"??????","/a38/":"??????","/a89/":"??????","/a87/":"??????","/a69/":"??????","/a68/":"??????"}
    nowTime_flex_message = FlexSendMessage(
        alt_text='????????????',
        contents={
            "type": "bubble",
            "direction": "ltr",
            "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "text",
                "text": "???????????????",
                "align": "start",
                "weight": "bold"
                },
                {
                "type": "text",
                "text": areaDict.get(inAreaID,"??????"),
                "align": "center"
                },
                {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                        "type": "filler"
                        },
                        {
                        "type": "text",
                        "text": "???????????????",
                        "align": "start",
                        "weight": "bold"
                        },
                        {
                        "type": "text",
                        "text": time.strftime("%Y-%m-%d %H:%M", time.localtime()),
                        "align": "center"
                        },
                        {
                        "type": "filler"
                        }
                    ]
                    },
                    # {
                    # "type": "text",
                    # "text": getNowTimeEmoji(),
                    # "flex": 0,
                    # "size": "4xl"
                    # }
                ]
                }
            ]
            }
        }
    )
    return(movieInfo_flex_message, nowTime_flex_message, movietheater_flex_message, pagebox_flex_message)

def show_movieHelper():
    moviehelper_flex_message = FlexSendMessage(
        alt_text='???????????????',
        contents={
            "type": "bubble",
            "direction": "ltr",
            "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "text",
                "text": "????????????",
                "size": "xl",
                "align": "start",
                "weight": "bold"
                }
            ]
            },
            "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "lg",
            "contents": [
                {
                "type": "box",
                "layout": "horizontal",
                "flex": 0,
                "margin": "md",
                "contents": [
                    {
                    "type": "text",
                    "text": "????????????",
                    "flex": 1,
                    "align": "end"
                    },
                    {
                    "type": "text",
                    "text": "????????????????????????????????????????????????",
                    "wrap": True
                    }
                ]
                },
                {
                "type": "box",
                "layout": "horizontal",
                "flex": 0,
                "margin": "md",
                "contents": [
                    {
                    "type": "text",
                    "text": "????????????",
                    "flex": 1,
                    "align": "end"
                    },
                    {
                    "type": "text",
                    "text": "?????????????????????????????????????????????????????????????????????????????????e.g., ????????????????????????",
                    "wrap": True
                    }
                ]
                },
                {
                "type": "box",
                "layout": "horizontal",
                "flex": 0,
                "margin": "md",
                "contents": [
                    {
                    "type": "text",
                    "text": "??????????????????",
                    "flex": 1,
                    "align": "end"
                    },
                    {
                    "type": "text",
                    "text": "???????????????????????????????????????????????????????????????????????????(e.g., ???????????????)",
                    "wrap": True
                    }
                ]
                },
                {
                "type": "box",
                "layout": "horizontal",
                "flex": 0,
                "margin": "md",
                "contents": [
                    {
                    "type": "text",
                    "text": "???????????????",
                    "flex": 1,
                    "align": "end"
                    },
                    {
                    "type": "text",
                    "text": "??????'????????????'",
                    "wrap": True
                    }
                ]
                },
                {
                "type": "text",
                "text": "???????????????",
                "size": "lg"
                },
                {
                "type": "box",
                "layout": "horizontal",
                "flex": 0,
                "margin": "xl",
                "contents": [
                    {
                    "type": "text",
                    "text": "???????????????",
                    "flex": 1,
                    "align": "end"
                    },
                    {
                    "type": "text",
                    "text": "??????????????????????????????????????????",
                    "wrap": True
                    }
                ]
                },
                {
                "type": "box",
                "layout": "horizontal",
                "margin": "md",
                "contents": [
                    {
                    "type": "text",
                    "text": "???????????????",
                    "flex": 1,
                    "align": "end"
                    },
                    {
                    "type": "text",
                    "text": "????????????????????????????????????????????????",
                    "wrap": True
                    }
                ]
                },
                {
                "type": "box",
                "layout": "horizontal",
                "margin": "md",
                "contents": [
                    {
                    "type": "text",
                    "text": "???????????????",
                    "flex": 1,
                    "align": "end"
                    },
                    {
                    "type": "text",
                    "text": "???????????????????????????????????????????????????????????????",
                    "wrap": True
                    }
                ]
                },
                {
                "type": "box",
                "layout": "horizontal",
                "margin": "md",
                "contents": [
                    {
                    "type": "text",
                    "text": "????????????",
                    "flex": 1,
                    "align": "end"
                    },
                    {
                    "type": "text",
                    "text": "?????????????????????????????????Yahoo?????????",
                    "wrap": True
                    }
                ]
                },
                {
                "type": "box",
                "layout": "horizontal",
                "margin": "md",
                "contents": [
                    {
                    "type": "text",
                    "text": "???????????????",
                    "flex": 1,
                    "align": "end"
                    },
                    {
                    "type": "text",
                    "text": "????????????????????????????????????",
                    "wrap": True
                    }
                ]
                }
                ,
                {
                "type": "box",
                "layout": "horizontal",
                "margin": "md",
                "contents": [
                    {
                    "type": "text",
                    "text": "??????????????????",
                    "flex": 1,
                    "align": "end"
                    },
                    {
                    "type": "text",
                    "text": "??????????????????????????????",
                    "align": "start",
                    "wrap": True
                    }
                ]
                }
            ]
        }}
    )
    return(moviehelper_flex_message)

#ok    
def workTeam():
    workTeam_flex_message = FlexSendMessage(
        alt_text='????????????',
        contents={
            "type": "bubble",
            "direction": "ltr",
            "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "text",
                "text": "????????????",
                "size": "xl",
                "align": "center",
                "weight": "bold"
                },
                {
                "type": "box",
                "layout": "horizontal",
                "margin": "xl",
                "contents": [
                    {
                    "type": "text",
                    "text": "1081507?????????",
                    "align": "center"
                    }]
                },
                {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                    "type": "text",
                    "text": "1081508?????????",
                    "align": "center"
                    }]
                },
                {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                    "type": "text",
                    "text": "1081213?????????",
                    "align": "center"
                    }]
                },
                {
                "type": "box",
                "layout": "horizontal",
                "margin": "xl",
                "contents": [
                    {
                    "type": "text",
                    "text": "???????????????",
                    "align": "end"
                    },
                    {
                    "type": "text",
                    "text": "Yahoo??????",
                    "align": "start",
                    "action": {
                        "type": "uri",
                        "uri": "https://movies.yahoo.com.tw/"
                        }
                    }]
                },
                {
                "type": "box",
                "layout": "horizontal",
                "margin": "none",
                "contents": [
                    {
                    "type": "filler"
                    },
                    {
                    "type": "text",
                    "text": "???????????????",
                    "align": "start",
                    "action": {
                        "type": "uri",
                        "uri": "http://www.atmovies.com.tw/home/"
                    }
                    }
                ]
                }
            ]
            }
        }
    )
    return(workTeam_flex_message)

#ok
def show_movieInfo_message():
    movie_flex_message = FlexSendMessage(
        alt_text='??????????????????????????????',
        contents={
            "type": "carousel",
            "contents": [
                {
                "type": "bubble",
                "direction": "ltr",
                "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                    "type": "text",
                    "text": "????????????????????????????????????",
                    "size": "lg",
                    "wrap": True
                    },
                    {
                    "type": "separator",
                    "margin": "lg"
                    },
                    {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": "??????????????????",
                        "text": "????????????"
                    }
                    }
                ]}
                },
                {
                    "type": "bubble",
                    "direction": "ltr",
                    "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                        "type": "text",
                        "text": "????????????????????????????????????",
                        "size": "lg",
                        "wrap": True
                        },
                        {
                        "type": "separator",
                        "margin": "lg"
                        },
                        {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "????????????????????????",
                            "text": "?????????"
                        }
                        }
                    ]
                    }
                },
                {
                    "type": "bubble",
                    "direction": "ltr",
                    "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                        "type": "text",
                        "text": "???????????????????????????????????????",
                        "size": "lg",
                        "wrap": True
                        },
                        {
                        "type": "separator",
                        "margin": "lg"
                        },
                        {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "???????????????????????????",
                            "text": "????????????"
                        }
                        }
                    ]
                    }
                }
            ]
        }
    )
    return(movie_flex_message)


def search_movie_thisweekAndIntheaters(url):
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
    req = request.Request(url, headers=headers)
    resp = request.urlopen(req)
    respData = str(resp.read().decode('utf-8'))  # ????????????????????????
    soup = BeautifulSoup(respData)

    # --------------------info
    movieInfo = [i for i in soup.select(".release_info")]
    movieInfoText = [i.text for i in soup.select(".release_info")]
    movieNameCN = [i.text.strip() for i in soup.select(".release_movie_name > .gabtn")]
    movieNameEN = []
    for i in soup.select(".en .gabtn"):
        if i.text.strip() == '':
            movieNameEN.append("-")
        else:
            movieNameEN.append(i.text.strip())
    movieExpectation = []
    for info in movieInfoText:
        movieExpectation.append('?????????') if info.find(
            "?????????") == None else movieExpectation.append(info[info.find("?????????")+5:info.find("?????????")+8])
    movieSatisfactoryDegree = []
    for html in movieInfo:
        try:
            movieSatisfactoryDegree.append(
                (html.select("span")[1])["data-num"])
        except:
            movieSatisfactoryDegree.append("0%")
    moviePoster = [i["data-src"] for i in soup.select(".lazy-load")]

    movieReleaseTime = [(i.text)[23:] for i in soup.select(".release_movie_time")]
    movieDetailUrl = [i["href"]
                        for i in soup.select(".release_movie_name > .gabtn")]
    
    # --------------------
    contents = []
    for index in range(len(movieNameCN)):
        contents.append({
            "type": "bubble",
            "direction": "ltr",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [{
                    "type": "text",
                    "text": "??????",
                    "size": "xl",
                    "align": "start",
                    "weight": "bold",
                    "color": "#000000"
                }]
            },
            "hero": {
                "type": "image",
                "url": moviePoster[index],
                "gravity": "top",
                "size": "full",
                "aspectRatio": "1:1.4",
                "aspectMode": "cover",
                "backgroundColor": "#FFFFFF"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [{
                    "type": "box",
                    "layout": "vertical",
                    "contents": [{
                        "type": "text",
                        "text": movieNameCN[index],
                        "margin": "none",
                        "size": "lg",
                        "align": "center",
                        "gravity": "top",
                        "weight": "bold"
                    },
                        {
                        "type": "text",
                        "text": movieNameEN[index],
                        "align": "center"
                    }]
                },
                    {
                    "type": "separator",
                    "margin": "lg",
                    "color": "#FFFFFF"
                },
                    {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [{
                        "type": "text",
                        "text": "???????????????"
                    },
                        {
                        "type": "text",
                        "text": movieReleaseTime[index]
                    }]
                },
                    {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [{
                        "type": "text",
                        "text": "????????????",
                        "align": "start",
                        "weight": "bold",
                        "color": "#BB21CA"
                    },
                        {
                        "type": "text",
                        "text": movieExpectation[index]
                    }]
                },
                    {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [{
                            "type": "text",
                            "text": "????????????",
                            "align": "start",
                            "weight": "bold",
                            "color": "#2133CA"
                    },
                        {
                            "type": "text",
                            "text": movieSatisfactoryDegree[index],
                            "align": "start"
                    }]
                }
                ]},
            "footer": {
                "type": "box",
                "layout": "horizontal",
                "contents": [{
                    "type": "button",
                    "action": {
                        "type": "postback",
                        "label": "????????????",
                        "data": movieDetailUrl[index]
                    }
                }]
            }
        })
    # ??????
    movie_flex_message = FlexSendMessage(
        alt_text='????????????',
        contents={
            "type": "carousel",
            "contents": contents
        }
    )

    pagebox_flex_message = pagebox(soup)

    return(movie_flex_message, pagebox_flex_message)


# ?????????????????? /callback ??? Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = flask.request.headers['X-Line-Signature']
    # get request body as text
    body = flask.request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        flask.abort(400)
    return 'OK'

def get(city):
    token = 'CWB-96756676-7BE5-4607-A23A-34386D3D2C27'
    url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=' + token + '&format=JSON&locationName=' + str(city)
    Data = requests.get(url)
    Data = (json.loads(Data.text))['records']['location'][0]['weatherElement']
    res = [[] , [] , []]
    for j in range(3):
        for i in Data:
            res[j].append(i['time'][j])
    return res 

def weather_location_message():
    location_flex_message = TemplateSendMessage(
        alt_text='?????????????????????',
        template=ButtonsTemplate(
            title='??????????????????',
            text='???????????????????????????????????????????????????????????????EX:?????? ?????????',
            size='lg',
            weight='bold',
            actions=[
                LocationAction(
                    label=' '
                )
            ]
        )
    )
    return(location_flex_message)


# ---------------------------------------------------------------
# ????????????
@handler.add(PostbackEvent)
def handle_postback(event):
    userpostback = event.postback.data
    print(userpostback)
    
    #????????????
    if userpostback[:71] == 'https://movies.yahoo.com.tw/moviesearch_result.html?type=movie&keyword=':
        movielist, pagebox = use_moviename_serch_movielist(userpostback, '')
        print(pagebox)
        line_bot_api.reply_message(event.reply_token, [movielist, pagebox])
    #??????????????????
    if userpostback[:43] == 'https://movies.yahoo.com.tw/movieinfo_main/':
        moviePosterContant, infoContant, storyContant, actorContant, stillsContant = use_movieurl_get_movieinfo(
            userpostback)
        line_bot_api.reply_message(
            event.reply_token, [moviePosterContant, infoContant, storyContant, actorContant, stillsContant])


    #??????????????????
    if userpostback[:38] == 'https://movies.yahoo.com.tw/name_main/':
        actor, button = use_actorURL_get_actorIntorduction(userpostback)
        line_bot_api.reply_message(event.reply_token, [actor, button])
    #??????????????????
    if userpostback[:40] == 'https://movies.yahoo.com.tw/name_movies/':
        movielist, pagebox = use_actorURL_search_movielist(userpostback)
        line_bot_api.reply_message(event.reply_token, [movielist, pagebox])
    #????????????
    if userpostback[:5] == '????????????:':
        line_bot_api.reply_message(event.reply_token, show_actor_intorduction(userpostback[5:]))
    #????????????
    if userpostback[:35] == 'https://movies.yahoo.com.tw/tagged/':
        line_bot_api.reply_message(event.reply_token, use_moviename_serch_article(userpostback[35:]))
    #????????????
    if userpostback[:48] == 'http://movies.yahoo.com.tw/movie_comingsoon.html':
        movietab, movielist, pagebox = search_movie_comingsoon(userpostback)
        if pagebox != False:
            line_bot_api.reply_message(event.reply_token, [movietab, movielist, pagebox])
        else:
            line_bot_api.reply_message(event.reply_token, [movietab, movielist])
    #???????????? ?????????
    if userpostback[:47] == 'https://movies.yahoo.com.tw/movie_thisweek.html' or userpostback[:48] == 'http://movies.yahoo.com.tw/movie_intheaters.html':
        movielist, pagebox = search_movie_thisweekAndIntheaters(userpostback)
        line_bot_api.reply_message(event.reply_token, [movielist, pagebox])
    #???????????????
    movieType = ['??????','??????','??????','??????','??????','??????','??????','????????????','??????','??????','????????????','??????','??????','????????????','????????????','?????????','??????','??????','??????']
    if userpostback in movieType:
        line_bot_api.reply_message(event.reply_token, search_movie_type(userpostback, ''))
    if userpostback[:59] == 'http://movies.yahoo.com.tw/moviegenre_result.html?genre_id=':
        line_bot_api.reply_message(event.reply_token, search_movie_type('', userpostback))
    #?????????
    if userpostback[:3] == '?????????':
        line_bot_api.reply_message(event.reply_token, get_MovieMoment(userpostback[3:]))
    #??????????????????
    if userpostback[:6] == '??????????????????':
        movieURL = userpostback[6:userpostback.find("|")]
        movieID = userpostback[userpostback.find("|")+1:userpostback.find("@")]
        movieName = userpostback[userpostback.find("@")+1:]
        nameMessage, areaMessage = use_movieurl_get_movieReleasedArea(movieURL, movieID, movieName)
        line_bot_api.reply_message(event.reply_token, [nameMessage, areaMessage])
    #???????????????
    if userpostback[:4] == '????????????':
        movieID = userpostback[4:userpostback.find("/")]
        area = userpostback[userpostback.find("/"):userpostback.find(",")]
        page = userpostback[userpostback.find(",")+1:]
        movieInfo, nowtime, movieMoment, pagebox = use_movieurl_get_movieMoment(movieID, area, page)
        line_bot_api.reply_message(event.reply_token, [movieInfo, nowtime, movieMoment, pagebox])
    #?????????????????????#ok
    if userpostback[:7] == '?????????????????????':
        movietheaterName = userpostback[userpostback.find("name")+4:userpostback.find("address")]
        movietheaterAddress = userpostback[userpostback.find("address")+7:userpostback.find("lat")]
        movietheaterLat = userpostback[userpostback.find("lat")+3:userpostback.find("lng")]
        movietheaterLng = userpostback[userpostback.find("lng")+3:]
        line_bot_api.reply_message(event.reply_token, use_movietheaterInfo_get_locationMessage(movietheaterName, movietheaterAddress, movietheaterLat, movietheaterLng))
    #?????????????????????
    if userpostback[:5] == '???????????????':
        movietheaterName = userpostback[5:userpostback.find(":")]
        page = userpostback[userpostback.find(":")+1:]
        theaterName, movielist, page = use_movietheatherName_search_movie(movietheaterName, page)
        #line_bot_api.reply_message(event.reply_token, [theaterName, movielist, page])
        line_bot_api.reply_message(event.reply_token, [theaterName, movielist])

    if userpostback == '????????????????????????':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="????????????????????????"))
# ---------------------------------------------------------------
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    userMessage = event.message.text
    print(event)
    
    if userMessage == 'Jarvis, u there?':#ok
        line_bot_api.reply_message(event.reply_token,    
        TextSendMessage( text="At your service, madame." ))
       # ,sender=Sender(
       #     name="<J.a.r.v.i.s>",
       #     icon_url="<https://nurdspace.nl/images/3/34/Jarvis.jpg>"))
       
    # elif userMessage == '????????????':
    #     line_bot_api.reply_message(event.reply_token,weather_location_message())
    elif userMessage == '????????????':
        line_bot_api.reply_message(event.reply_token,weather_location_message())
    elif(userMessage[:2] == '??????'):
            city = userMessage[3:]
            city = city.replace('???','???')
            if(not (city in cities)):
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="???????????????:?????? ??????"))
            else:
                res = get(city)
                print(res)
                line_bot_api.reply_message(event.reply_token,TemplateSendMessage(
                alt_text = city + '?????? 36 ??????????????????',
                template = CarouselTemplate(
                    columns = [
                        CarouselColumn(
                            thumbnail_image_url = 'https://i.imgur.com/Ex3Opfo.png',
                            title = '{} ~ {}'.format(data[0]['startTime'][5:-3],data[0]['endTime'][5:-3]),
                            text = '???????????? {}\n?????? {} ~ {} ??C\n???????????? {}'.format(data[0]['parameter']['parameterName'],data[2]['parameter']['parameterName'],data[4]['parameter']['parameterName'],data[1]['parameter']['parameterName']),
                            actions = [
                                URIAction(
                                    label = '????????????',
                                    uri = 'https://www.cwb.gov.tw/V8/C/W/County/index.html'
                                )
                            ]
                         )for data in res
                    ]
                    )
            ))
    elif userMessage == '????????????':#ok
        line_bot_api.reply_message(event.reply_token,show_movieInfo_message())
    elif userMessage == '???????????????':
        line_bot_api.reply_message(event.reply_token,show_movieHelper())
    elif userMessage == '????????????':
        movietab, movielist, pagebox = search_movie_comingsoon('')
        if pagebox != False: 
            print("true")
            line_bot_api.reply_message(event.reply_token, [movietab, movielist, pagebox])
        else:
            print("false")
            line_bot_api.reply_message(event.reply_token, [movietab, movielist])
    elif userMessage == '????????????':
        movielist, pagebox = search_movie_thisweekAndIntheaters('https://movies.yahoo.com.tw/movie_thisweek.html?page=1')
        if pagebox == False:
            line_bot_api.reply_message(event.reply_token, movielist)
        else:
            line_bot_api.reply_message(event.reply_token, [movielist, pagebox])
    elif userMessage == '?????????':
        movielist, pagebox = search_movie_thisweekAndIntheaters('https://movies.yahoo.com.tw/movie_intheaters.html?page=1')
        line_bot_api.reply_message(event.reply_token, [movielist, pagebox])
    elif userMessage == '?????????':
        movierank, data = search_movie_chart('https://movies.yahoo.com.tw/chart.html')
        line_bot_api.reply_message(event.reply_token, [show_chart_message(), movierank])
    elif userMessage == '???????????????':
        movierank, data = search_movie_chart('https://movies.yahoo.com.tw/chart.html?cate=us')
        line_bot_api.reply_message(event.reply_token, [movierank])
    elif userMessage == '???????????????':
        movierank, data = search_movie_chart('https://movies.yahoo.com.tw/chart.html?cate=year')
        line_bot_api.reply_message(event.reply_token, [movierank])
    elif userMessage == '???????????????':
        movierank, data = search_movie_chartNetizens('https://movies.yahoo.com.tw/chart.html?cate=exp_30')
        line_bot_api.reply_message(event.reply_token, [movierank])
    elif userMessage == '???????????????':
        movierank, data = search_movie_chartNetizens('https://movies.yahoo.com.tw/chart.html?cate=rating')
        line_bot_api.reply_message(event.reply_token, [movierank])
    elif userMessage == '????????????':
        line_bot_api.reply_message(event.reply_token, select_movie_type())
    elif userMessage == '???????????????':
        line_bot_api.reply_message(event.reply_token, show_location_message())
    elif userMessage[:3] == '?????????':
        theatername, movie, page = use_movietheatherName_search_movie(userMessage[3:], "1")
        if page == False:
            line_bot_api.reply_message(event.reply_token, [theatername, movie])
        else:
            line_bot_api.reply_message(event.reply_token, [theatername, movie, page])
    elif userMessage == '????????????':
        movielist = get_MovieMoment()
        line_bot_api.reply_message(event.reply_token, movielist)
    elif userMessage[:2] == '??????':
        line_bot_api.reply_message(event.reply_token, use_moviename_serch_article(userMessage[2:]))
    else:
        movielist, pagebox = use_moviename_serch_movielist(userMessage, '1')
        if not pagebox:
            line_bot_api.reply_message(event.reply_token, movielist)
        else:
            line_bot_api.reply_message(event.reply_token, [movielist, pagebox])


@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(event.reply_token,show_movieHelper())



@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    print(event.message.address)
    print(event.message.latitude)
    print(event.message.longitude)
    radar = use_location_search_movietheater(event.message.address,event.message.latitude,event.message.longitude)    
    line_bot_api.reply_message(event.reply_token, radar)
    


if __name__ == "__main__":
    app.run(port = 5001)