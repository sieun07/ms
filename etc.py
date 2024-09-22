from flask import Flask, request, jsonify, render_template
import openai

# Flask 애플리케이션 생성
app = Flask(__name__)

# OpenAI API 키 설정
openai.api_key = ''

# 최대 메시지 수 설정
msg_cnt = 50

# 메시지 히스토리 초기화
msg_history = [
    {"role": "system", "content": "당신은 사람들의 고민거리 중 대인관계, 직장, 학업, 가족, 건강, 진로에 대한 스트레스 수치를 판단해주는 AI입니다. 따뜻한 말투와 함께 사용자와의 일상적인 대화를 통해 대인관계, 직장, 학업, 가족, 건강, 진로에 대한 스트레스 수치를 판단해주어 각각의 스트레스 수치를 알려주세요."}
]

# OpenAI GPT-4 API 호출 함수
def generate_response(prompt):
    msg_history.append({"role": "user", "content": prompt})
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=msg_history,
            max_tokens=100,
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
    return render_template('index.html')

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
    app.run()