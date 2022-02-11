from os import stat
from fastapi import Body, FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, constr

import pickle
from sklearn import svm
from sklearn import datasets
import joblib
# coding=utf-8
import os
import json
import pickle
import pandas as pd
import numpy as np
import sklearn.model_selection
import sklearn.datasets
import sklearn.metrics
from sklearn.metrics import confusion_matrix, recall_score, classification_report, precision_score
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

import autosklearn.regression



# data={
#       '臺北市': {'中正': '100', '大同': '103', '中山': '104', '松山': '105', '大安': '106', '萬華': '108', '信義': '110', '士林': '111', '北投': '112', '內湖': '114', '南港': '115', '文山': '116'}, 
#       '基隆市': {'仁愛': '200', '信義': '201', '中正': '202', '中山': '203', '安樂': '204', '暖暖': '205', '七堵': '206'}, 
#       '新北市': {'萬里': '207', '金山': '208', '板橋': '220', '汐止': '221', '深坑': '222', '石碇': '223', '瑞芳': '224', '平溪': '226', '雙溪': '227', '貢寮': '228', '新店': '231', '坪林': '232', '烏來': '233', '永和': '234', '中和': '235', '土城': '236', '三峽': '237', '樹林': '238', '鶯歌': '239', '三重': '241', '新莊': '242', '泰山': '243', '林口': '244', '蘆洲': '247', '五股': '248', '八里': '249', '淡水': '251', '三芝': '252', '石門': '253'}, 
#       '宜蘭縣': {'宜蘭': '260', '頭城': '261', '礁溪': '262', '壯圍': '263', '員山': '264', '羅東': '265', '三星': '266', '大同': '267', '五結': '268', '冬山': '269', '蘇澳': '270', '南澳': '272'}, 
#       '連江縣': {'南竿': '209', '北竿': '210', '莒光': '211', '東引': '212'}, 
#       '新竹市': {'香山': '300', '新竹': '300'}, 
#       '新竹縣': {'竹北': '302', '湖口': '303', '新豐': '304', '新埔': '305', '關西': '306', '芎林': '307', '寶山': '308', '竹東': '310', '五峰': '311', '橫山': '312', '尖石': '313', '北埔': '314', '峨眉': '315'}, 
#       '桃園市': {'中壢': '320', '平鎮': '324', '龍潭': '325', '楊梅': '326', '新屋': '327', '觀音': '328', '桃園': '330', '龜山': '333', '八德': '334', '大溪': '335', '復興': '336', '大園': '337', '蘆竹': '338'}, 
#       '苗栗縣': {'竹南': '350', '頭份': '351', '三灣': '352', '南庄': '353', '獅潭': '354', '後龍': '356', '通霄': '357', '苑裡': '358', '苗栗': '360', '造橋': '361', '頭屋': '362', '公館': '363', '大湖': '364', '泰安': '365', '銅鑼': '366', '三義': '367', '西湖': '368', '卓蘭': '369'}, 
#       '臺中市': {'中區': '400', '東區': '401', '南區': '402', '西區': '403', '北區': '404', '北屯': '406', '西屯': '407', '南屯': '408', '太平': '411', '大里': '412', '霧峰': '413', '烏日': '414', '豐原': '420', '后里': '421', '石岡': '422', '東勢': '423', '和平': '424', '新社': '426', '潭子': '427', '大雅': '428', '神岡': '429', '大肚': '432', '沙鹿': '433', '龍井': '434', '梧棲': '435', '清水': '436', '大甲': '437', '外埔': '438', '大安': '439'}, 
#       '彰化縣': {'彰化': '500', '芬園': '502', '花壇': '503', '秀水': '504', '鹿港': '505', '福興': '506', '線西': '507', '和美': '508', '伸港': '509', '員林': '510', '社頭': '511', '永靖': '512', '埔心': '513', '溪湖': '514', '大村': '515', '埔鹽': '516', '田中': '520', '北斗': '521', '田尾': '522', '埤頭': '523', '溪州': '524', '竹塘': '525', '二林': '526', '大城': '527', '芳苑': '528', '二水': '529'}, 
#       '南投縣': {'南投': '540', '中寮': '541', '草屯': '542', '國姓': '544', '埔里': '545', '仁愛': '546', '名間': '551', '集集': '552', '水里': '553', '魚池': '555', '信義': '556', '竹山': '557', '鹿谷': '558'}, 
#       '嘉義市': {'西區': '600', '嘉義': '600'}, 
#       '嘉義縣': {'番路': '602', '梅山': '603', '竹崎': '604', '阿里山': '605', '中埔': '606', '大埔': '607', '水上': '608', '鹿草': '611', '太保': '612', '朴子': '613', '東石': '614', '六腳': '615', '新港': '616', '民雄': '621', '大林': '622', '溪口': '623', '義竹': '624', '布袋': '625'}, 
#       '雲林縣': {'斗南': '630', '大埤': '631', '虎尾': '632', '土庫': '633', '褒忠': '634', '東勢': '635', '臺西': '636', '崙背': '637', '麥寮': '638', '斗六': '640', '林內': '643', '古坑': '646', '莿桐': '647', '西螺': '648', '二崙': '649', '北港': '651', '水林': '652', '四湖': '653', '元長': '654'}, 
#       '臺南市': {'中西': '700', '東區': '701', '南區': '702', '北區': '704', '安平': '708', '安南': '709', '永康': '710', '歸仁': '711', '新化': '712', '左鎮': '713', '玉井': '714', '楠西': '715', '南化': '716', '仁德': '717', '關廟': '718', '龍崎': '719', '官田': '720', '麻豆': '721', '佳里': '722', '西港': '723', '七股': '724', '將軍': '725', '學甲': '726', '北門': '727', '新營': '730', '後壁': '731', '白河': '732', '東山': '733', '六甲': '734', '下營': '735', '柳營': '736', '鹽水': '737', '善化': '741', '大內': '742', '山上': '743', '新市': '744', '安定': '745'}, 
#       '高雄市': {'新興': '800', '前金': '801', '苓雅': '802', '鹽埕': '803', '鼓山': '804', '旗津': '805', '前鎮': '806', '三民': '807', '楠梓': '811', '小港': '812', '左營': '813', '仁武': '814', '大社': '815', '岡山': '820', '路竹': '821', '阿蓮': '822', '田寮': '823', '燕巢': '824', '橋頭': '825', '梓官': '826', '彌陀': '827', '永安': '828', '湖內': '829', '鳳山': '830', '大寮': '831', '林園': '832', '鳥松': '833', '大樹': '840', '旗山': '842', '美濃': '843', '六龜': '844', '內門': '845', '杉林': '846', '甲仙': '847', '桃源': '848', '那瑪夏': '849', '茂林': '851', '茄萣': '852'}, 
#       '澎湖縣': {'馬公': '880', '西嶼': '881', '望安': '882', '七美': '883', '白沙': '884', '湖西': '885'}, 
#       '金門縣': {'金沙': '890', '金湖': '891', '金寧': '892', '金城': '893', '烈嶼': '894', '烏坵': '896'}, 
#       '屏東縣': {'屏東': '900', '竹田': '911', '三地門': '901', '霧臺': '902', '瑪家': '903', '九如': '904', '里港': '905', '高樹': '906', '鹽埔': '907', '長治': '908', '麟洛': '909', '內埔': '912', '萬丹': '913', '潮州': '920', '泰武': '921', '來義': '922', '萬巒': '923', '崁頂': '924', '新埤': '925', '南州': '926', '林邊': '927', '東港': '928', '珫球': '929', '佳冬': '931', '新園': '932', '枋寮': '940', '枋山': '941', '春日': '942', '獅子': '943', '車城': '944', '牡丹': '945', '恆春': '946', '滿州': '947'}, 
#       '臺東縣': {'臺東': '950', '台東': '950', '綠島': '951', '蘭嶼': '952', '延平': '953', '卑南': '954', '鹿野': '955', '關山': '956', '海端': '957', '池上': '958', '東河': '959', '成功': '961', '長濱': '962', '太麻里': '963', '金峰': '964', '大武': '965', '達仁': '966'}, 
#       '花蓮縣': {'花蓮': '970', '新城': '971', '秀林': '972', '吉安': '973', '壽豐': '974', '鳳林': '975', '光復': '976', '豐演': '977', '瑞穗': '978', '萬榮': '979', '玉里': '981', '卓溪': '982', '富里': '983'}
#     }


class TESTRequest(BaseModel):

    #市名
    city:str
    
    #地區
    area:str

    #坪數
    total_area:str

    #建物類型
    building_type:str

    #總樓層數
    total_floor:str

    #建物型態
    state:str

    #主要用途
    usage:str

    #主要建材
    material:str

    #屋齡
    building_age:str

    #房間數量
    building_room_num:str

    #大廳數量
    building_hall_num:str

    #衛浴數量
    building_bathroom_num:str

    #管理員
    residential_guard:str

    #車位
    berth:str

    #電梯
    elevator:str




class TESTITEM(BaseModel):
    #市名
    city:str
    
    #地區
    area:str

    #坪數
    total_area:str

    #建物類型
    building_type:str

    #總樓層數
    total_floor:str

    #建物型態
    state:str

    #主要用途
    usage:str

    #主要建材
    material:str

    #屋齡
    building_age:str

    #房間數量
    building_room_num:str

    #大廳數量
    building_hall_num:str

    #衛浴數量
    building_bathroom_num:str

    #管理員
    residential_guard:str

    #車位
    berth:str

    #電梯
    elevator:str

app = FastAPI(
    title="{{ cookiecutter.project_name }}",
    description="{{ cookiecutter.project_short_description }}",
    version="{{ cookiecutter.version }}",
)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")



@app.get("/")
async def root():
    return RedirectResponse("docs")


@app.get("/page/{page_name}", response_class=HTMLResponse)
async def page(request: Request, page_name: str):
    return templates.TemplateResponse(f"{page_name}.html", {"request": request})



@app.post("/test")
async def test(
    test_request: TESTRequest = Body(
        None,
    )
):
    print(test_request)
    columns = ['postal_code', 'building_shifting_total_area', 'type', 'total_floor',
       'building_state', 'main_use', 'building_materials', 'building_age',
       'building_room_num', 'building_hall_num', 'building_bathroom_num',
       'residential_guard', 'berth', 'elevator']
    
    value1 = int(test_request.area)
    value2 = float(test_request.area)
    value3 = int(test_request.building_type)
    value4 = int(test_request.total_floor)
    value5 = int(test_request.state)
    value6 = int(test_request.usage)
    value7 = int(test_request.material)
    value8 = int(test_request.building_age)
    value9 = int(test_request.building_room_num)
    value10 = int(test_request.building_hall_num)
    value11 = int(test_request.building_bathroom_num)
    value12 = int(test_request.residential_guard)
    value13 = int(test_request.berth)
    value14 = int(test_request.elevator)

    lst = [value1,value2,value3,value4,value5,value6,
        value7,value8,value9,value10,value11,value12,
        value13,value14]
    with open('my_model1.pkl', 'rb') as f:
        clf2 = pickle.load(f)

    df = pd.DataFrame([lst], columns =columns)

    predictions = clf2.predict(df)
    result = '總價為'+ str(int(predictions)) + '元'
    print(result)

    
    return result