import streamlit as st
import requests
import xml.etree.ElementTree as ET
import re

url = 'http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList'
params = {
    'ServiceKey': 'dLn8y7WaewYlKydHx9bAbXo2EuzgcswHHB+Zo6mMhRlwUdIbazkSts0steADWWHaxYcUkdk540UIahMTKtiozg==',
    'pageNo': '1',
    'numOfRows': '3',
    'entpName': '',
    'itemName': '',
    'itemSeq': '',
    'efcyQesitm': '',
    'useMethodQesitm': '',
    'atpnWarnQesitm': '',
    'atpnQesitm': '',
    'intrcQesitm': '',
    'seQesitm': '',
    'depositMethodQesitm': '',
    'openDe': '',
    'updateDe': '',
    'type': 'xml'
}

# 의약품 제품 이름 입력 받기
item_name = st.text_input("검색할 의약품 이름을 입력하고 Enter를 누르거나 조회 버튼을 눌러주세요:")
params['itemName'] = item_name

if st.button('조회') or item_name:
    response = requests.get(url, params=params)
    response.encoding = 'utf-8'  # 응답 데이터의 인코딩 설정
    xml_data = response.text

    # XML 데이터 파싱하여 태그 제거
    root = ET.fromstring(xml_data)
    result = ""

    found_items = False  # Flag to check if any items were found

    for item in root.iter('item'):
        itemSeq = item.findtext('itemSeq')
        entpName = item.findtext('entpName')
        itemName = item.findtext('itemName')
        efcyQesitm = item.findtext('efcyQesitm')
        useMethodQesitm = item.findtext('useMethodQesitm')
        atpnWarnQesitm = item.findtext('atpnWarnQesitm')
        atpnQesitm = item.findtext('atpnQesitm')
        intrcQesitm = item.findtext('intrcQesitm')
        seQesitm = item.findtext('seQesitm')
        depositMethodQesitm = item.findtext('depositMethodQesitm')

        # 태그 제거
        efcyQesitm = re.sub('<.*?>', '', efcyQesitm)
        useMethodQesitm = re.sub('<.*?>', '', useMethodQesitm)
        atpnWarnQesitm = re.sub('<.*?>', '', atpnWarnQesitm)
        atpnQesitm = re.sub('<.*?>', '', atpnQesitm)
        intrcQesitm = re.sub('<.*?>', '', intrcQesitm)
        seQesitm = re.sub('<.*?>', '', seQesitm)
        depositMethodQesitm = re.sub('<.*?>', '', depositMethodQesitm)

        result += "---\n"
        result += f"제품명: {itemName}\n\n"
        result += f"업체명: {entpName}\n\n"
        result += f"제품 번호: {itemSeq}\n\n"

        if efcyQesitm:
            result += f"효능: {efcyQesitm}\n\n"
        if useMethodQesitm:
            result += f"사용 방법: {useMethodQesitm}\n\n"
        if atpnWarnQesitm:
            result += f"주의 사항: {atpnWarnQesitm}\n\n"
        if intrcQesitm:
            result += f"상호 작용: {intrcQesitm}\n\n"
        if seQesitm:
            result += f"부작용: {seQesitm}\n\n"
        if depositMethodQesitm:
            result += f"보관 방법: {depositMethodQesitm}\n\n"

        found_items = True  # At least one item was found

    if not found_items:
        result = "해당 제품에 대한 정보를 찾을 수 없습니다. 다시 입력해주세요."

    # 결과 출력
    st.write(result)
