# -*- coding: utf-8 -*-
import requests
import json


class ClovaSummary:
    # Clova Speech invoke URL

    url = 'https://naveropenapi.apigw.ntruss.com/text-summary/v1/summarize'
    client_id = "pficodqpxs"
    client_secret = "aFVah3wAvD8xvbM8Mp4iOUEl9a5h23XlAaDr4gMk"

    def req(self, content):
        request_body = {
            "document": {
                "content": content
            },
            "option": {
                "language": 'ko', #이걸 다 선택하도록 하는게 좋을듯!!!
                "model": "general",  # Model used for summaries (general, news) * general: 일반 문서 요약, news: 뉴스 요약
                "summaryCount": 3,   # This is the number of sentences for the summarized document. 기본값은 3
                "tone": 3  # Converts the tone of the summarized result. (0, 1, 2, 3)
                ## 0: 원문의 어투를 유지,1: 해요체로 변환, ex) 조사한다 -> 조사해요, 2: 정중체로 변환, ex)조사한다 -> 조사합니다, 3: 명사형 종결체로 변환, ex) 조사한다 -> 조사함
            }
        }
        headers = {
            'Accept': 'application/json;UTF-8',
            'Content-Type': 'application/json;UTF-8',
            'X-NCP-APIGW-API-KEY-ID': self.client_id,
            'X-NCP-APIGW-API-KEY': self.client_secret
        }
        return requests.post(headers=headers,
                             url=self.url,
                             data=json.dumps(request_body).encode('UTF-8'))


if __name__ == '__main__':
    contents = "간편송금 이용금액이 하루 평균 2000억원을 넘어섰다. 한국은행이 17일 발표한 '2019년 상반기중 전자지급서비스 이용 현황'에 따르면 올해 상반기 간편송금서비스 이용금액(일평균)은 지난해 하반기 대비 60.7% 증가한 2005억원으로 집계됐다. 같은 기간 이용건수(일평균)는 34.8% 늘어난 218만건이었다. 간편 송금 시장에는 선불전자지급서비스를 제공하는 전자금융업자와 금융기관 등이 참여하고 있다. 이용금액은 전자금융업자가 하루평균 1879억원, 금융기관이 126억원이었다. 한은은 카카오페이, 토스 등 간편송금 서비스를 제공하는 업체 간 경쟁이 심화되면서 이용규모가 크게 확대됐다고 분석했다. 국회 정무위원회 소속 바른미래당 유의동 의원에 따르면 카카오페이, 토스 등 선불전자지급서비스 제공업체는 지난해 마케팅 비용으로 1000억원 이상을 지출했다. 마케팅 비용 지출규모는 카카오페이가 491억원, 비바리퍼블리카(토스)가 134억원 등 순으로 많았다."
    WORDS = 1999
    summary = ""

    for i in range((len(contents) // WORDS) + 1):
        print(i, "번째***********")
        res = ClovaSummary().req(contents[WORDS * i:WORDS * (i + 1)])
        rescode = res.status_code
        if (rescode == 200):
            print(res.text)
            summary += json.loads(res.text)["summary"]
        else:
            print("Error : " + res.text)
    if (len(contents) // WORDS) > 0:
        res = ClovaSummary().req(summary)
        rescode = res.status_code
        if (rescode == 200):
            summary = json.loads(res.text)["summary"]
        else:
            print("Error : " + res.text)

    print("\n최종 summary")
    print(summary)
