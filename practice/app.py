from flask import Flask

# Flask 애플리케이션을 생성합니다.
app = Flask(__name__)

# 라우트를 정의합니다.
@app.route('/')
def index():
    return 'Hello, World!'

# 애플리케이션을 실행합니다.
if __name__ == '__main__':
    app.run(debug=True)
