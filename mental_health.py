from flask import Flask, request, jsonify, render_template
import openai
from bs4 import BeautifulSoup
import requests

# Flask 애플리케이션 생성
app = Flask(__name__)

# OpenAI API 키 설정 (키 만료 새로 받아야함)
#openai.api_key = ''

# 최대 메시지 수 설정
msg_cnt = 50

# 웹 페이지에서 HTML 데이터를 가져와 BeautifulSoup 객체로 변환
def fetch_html(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')

# 다양한 자료를 가져오는 URL 리스트
urls = [
    "https://www.psychiatricnews.net/news/articleView.html?idxno=9111",
    "https://blog.naver.com/hyeonse77/222273872237",
    "https://asana.com/ko/resources/overworked-signs", #직장
    "https://www.bokjiro.go.kr/ssis-tbu/cms/pc/news/news/5629228.html", #직장
    "https://brunch.co.kr/@jagyegam/4", #대인관계
    "https://redoasisone.com/entry/%ED%95%99%EC%97%85-%EC%8A%A4%ED%8A%B8%EB%A0%88%EC%8A%A4%EC%9D%98-%EC%98%81%ED%96%A5%EA%B3%BC-%EA%B4%80%EB%A6%AC-%EB%B0%A9%EB%B2%95", #학업
    "https://ideanomads.tistory.com/entry/%EC%9D%B8%EA%B0%84%EA%B4%80%EA%B3%84-%EC%8A%A4%ED%8A%B8%EB%A0%88%EC%8A%A4-%EA%B4%80%EB%A6%AC%ED%95%98%EA%B8%B0", # 대인관계
    "https://ooooooo.tistory.com/entry/%EA%B0%80%EC%A1%B1-%EA%B0%84-%EC%8A%A4%ED%8A%B8%EB%A0%88%EC%8A%A4%EA%B0%80-%EC%8C%93%EC%9D%B4%EB%8A%94-%EC%9D%B4%EC%9C%A0%EC%99%80-%ED%95%B4%EA%B2%B0-%EB%B0%A9%EC%95%88", #가족관계
    "https://blog.naver.com/koshablog/220864781364", #가족관계
    "https://www.mykpcc.com/103/?q=YToyOntzOjEyOiJrZXl3b3JkX3R5cGUiO3M6MzoiYWxsIjtzOjQ6InBhZ2UiO2k6ODt9&bmode=view&idx=11781005&t=board", #가족관계
    "https://www.maum-sopoong.or.kr/family-conflict?gcl_keyword=%EA%B0%80%EC%A1%B1%20%EA%B0%88%EB%93%B1&gcl_network=g&gad_source=1&gclid=EAIaIQobChMI477_suXViAMV4g97Bx2U6SV7EAMYASAAEgLan_D_BwE",
    "https://ko.wix.com/blog/post/how-to-deal-with-stress-at-work", #건강
    "https://www.ncmh.go.kr/ncmh/board/boardView.do;jsessionid=NInEmo7q0nKElVTo9taGIYqUhXvabP9Q3kY5KwDXHdWxGMuEneaKnS9RaukQQwUu.mohwwas2_servlet_engine1?no=137&fno=41&bn=newsView&menu_cd=02_06_02_01&bno=&pageIndex=1&search_item=&search_content=",
    "https://www.betterlifenews.co.kr/news/articleView.html?idxno=1206",
    "https://blog.naver.com/jobkoreaman/140208015774",
    "https://datascience.re.kr/1064",
    "https://metabiz101.tistory.com/6990554",
    "https://www.jobkorea.co.kr/goodjob/tip/view?News_No=16683"
    "https://www.segye.com/newsView/20090201001873"

]

# 모든 URL의 HTML 데이터를 BeautifulSoup 객체로 변환
html_contents = [fetch_html(url) for url in urls]

# 메시지 히스토리 초기화
msg_history = [
    {"role": "system", "content": "당신은 사람들의 고민거리 중 대인관계, 직장, 학업, 가족, 건강, 진로에 대한 스트레스 수치를 판단해주는 AI입니다. 따뜻한 말투와 함께 사용자와의 일상적인 대화를 통해 대인관계, 직장, 학업, 가족, 건강, 진로에 대한 각각의 스트레스 수치를 알려주세요."},
    {"role": "user", "content": [
        {"type": "text", "text": f"이 문서는 우리 서비스 내용에 관한 문서입니다.: {html_contents[0].text}"},
        {"type": "text", "text": f"이 문서들은 위로를 해주는 방법 및 말투에 관한 참고 문서입니다. : {html_contents[1].text}, {html_contents[2].text}"},
        {"type": "text", "text": f"이 문서들은 직장 스트레스에 관한 참고 문서입니다. : {html_contents[3].text}, {html_contents[4].text}, {html_contents[5].text}, {html_contents[6].text}, {html_contents[7].text}"},
        {"type": "text", "text": f"이 문서들은 대인관계 스트레스에 관한 참고 문서입니다. : {html_contents[8].text}, {html_contents[9].text}, {html_contents[10].text}, {html_contents[11].text}, {html_contents[12].text}"},
        {"type": "text", "text": f"이 문서들은 학업 스트레스에 관한 참고 문서입니다. : {html_contents[13].text}, {html_contents[14].text}, {html_contents[15].text}, {html_contents[16].text}, {html_contents[17].text}"},
        {"type": "text", "text": f"이 문서들은 가족 스트레스에 관한 참고 문서입니다. : {html_contents[18].text}, {html_contents[19].text}, {html_contents[20].text}, {html_contents[21].text}, {html_contents[22].text}"},
        {"type": "text", "text": f"이 문서들은 건강 스트레스에 관한 참고 문서입니다. : {html_contents[23].text}, {html_contents[24].text}, {html_contents[25].text}"},
        {"type": "text", "text": f"이 문서들은 가족 스트레스에 관한 참고 문서입니다. : {html_contents[26].text}, {html_contents[27].text}, {html_contents[28].text}, {html_contents[29].text}, {html_contents[30].text}"},

    ]}  
]

# OpenAI GPT-4 API 호출 함수
def generate_response(prompt):
    msg_history.append({"role": "user", "content": prompt})
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=msg_history,
            max_tokens=500,
            temperature=0.7
        )
        # 메시지 히스토리가 설정된 최대 개수를 초과하지 않도록 유지
        if len(msg_history) > msg_cnt:
            msg_history.pop(1)
        answer = response.choices[0].message['content'].strip()
        msg_history.append({"role": "assistant", "content": answer})
        return answer
    except openai.error.Timeout:
        return "응답 시간이 초과되었습니다. 다시 시도해 주세요."
    except openai.error.APIError as e:
        return f"API 오류가 발생했습니다: {str(e)}"
    except Exception as e:
        return f"오류가 발생했습니다: {str(e)}"

# 기본 라우트
@app.route('/')
def index():
    return render_template('mental_health.html')

# 채팅 라우트
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({"error": "메시지가 필요합니다."}), 400
    response = generate_response(user_input)
    return jsonify({"response": response})

# 서버 실행
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9800)