import streamlit as st
import requests
import xml.etree.ElementTree as ET
import re

def show_details(item):
    result = ""
    useMethodQesitm = item.findtext('useMethodQesitm')
    atpnWarnQesitm = item.findtext('atpnWarnQesitm')
    intrcQesitm = item.findtext('intrcQesitm')
    seQesitm = item.findtext('seQesitm')
    depositMethodQesitm = item.findtext('depositMethodQesitm')

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

    return result

url = 'http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList'
params = {
    'ServiceKey': 'dLn8y7WaewYlKydHx9bAbXo2EuzgcswHHB+Zo6mMhRlwUdIbazkSts0steADWWHaxYcUkdk540UIahMTKtiozg==',
    'pageNo': '1',
    'numOfRows': '100',  # 수정: 최대 1000개로 변경
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

# 효능 검색어 입력 받기
efcyQesitm_search_term = st.text_input("어디가 아프신가요? \n\n 대표적인 증상 한가지를 입력해주세요.\n\n 증상을 완화시킬 수 있는 약을 검색해드릴게요.")

if st.button('조회') or efcyQesitm_search_term:
    params['efcyQesitm'] = efcyQesitm_search_term
    response = requests.get(url, params=params)
    response.encoding = 'utf-8'  # 응답 데이터의 인코딩 설정
    xml_data = response.text

    # XML 데이터 파싱하여 태그 제거
    root = ET.fromstring(xml_data)
    result = ""
    found_items = False  # Flag to check if any items were found

    items = root.findall('.//item')
    entp_names = set()  # 중복되지 않는 업체명을 저장하기 위한 set
    item_names = []  # 제품명을 저장하기 위한 리스트

    for item in items:
        itemSeq = item.findtext('itemSeq')
        entpName = item.findtext('entpName')
        itemName = item.findtext('itemName')
        efcyQesitm = item.findtext('efcyQesitm')

        # 검색어가 효능에 있는 경우에만 결과에 추가
        if efcyQesitm_search_term.lower() in efcyQesitm.lower():
            # 태그 제거
            efcyQesitm = re.sub('<.*?>', '', efcyQesitm)

            result += "---\n"
            result += f"제품명: {itemName}\n\n"
            result += f"업체명: {entpName}\n\n"
            result += f"효능: {efcyQesitm}\n\n"
            result += "<details>"
            result += "<summary>자세히 보기</summary>"
            result += show_details(item)
            result += "</details>\n\n"

            found_items = True  # At least one item was found

            entp_names.add(entpName)  # 업체명 추가
            item_names.append(itemName)  # 제품명 추가

    if not found_items:
        result = "해당 검색어에 대한 결과를 찾을 수 없습니다."

    total_entp_count = len(entp_names)
    total_item_count = len(set(item_names))
    result_summary = f"총 {total_entp_count}개 업체의 {total_item_count}개 제품이 있습니다.\n\n 현재는 100개까지만 검색결과를 제공하고 있습니다."
    # 결과 출력
    st.markdown(result_summary)
    st.markdown(result, unsafe_allow_html=True)
