from flask import Flask, send_from_directory, jsonify, request
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
app = Flask(__name__, static_folder="public")

reviews = []

# ------------------
# API 라우팅
# ------------------
@app.route('/api/reviews', methods=['POST'])
def add_review():
    data = request.get_json()
    rating = data.get('rating')
    comment = data.get('comment')
    reviews.append({'rating': rating, 'comment': comment})
    return jsonify({'message': '저장 완료'})

@app.route('/api/reviews', methods=['GET'])
def get_review():
    return jsonify(reviews)

@app.route('/api/ai-summary', methods=['GET'])
def get_ai_summary():
    if not reviews:
        return jsonify({'summary': '아직 리뷰가 없습니다.', 'average_rating': None})

    average_rating = sum(r['rating'] for r in reviews) / len(reviews)

    reviews_text = "\n".join(
        [f"- 평점 {r['rating']}점: {r['comment']}" for r in reviews]
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "너는 쇼핑몰 리뷰 분석가야. 아래 리뷰들을 읽고 전체적인 고객 반응을 2~3문장으로 한국어로 요약해줘."
            },
            {
                "role": "user",
                "content": f"다음은 고객 리뷰 목록이야:\n{reviews_text}"
            }
        ]
    )

    summary = response.choices[0].message.content
    return jsonify({'summary': summary, 'average_rating': round(average_rating, 1)})


# ------------------
# 웹 서비스 라우팅
# ------------------
@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)