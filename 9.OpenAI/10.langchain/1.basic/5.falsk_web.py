from langchain_openai import ChatOpenAI  # Q&A 용으로 사용 (Chat Model = gpt-3.5-turbo)
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from flask import Flask,request,jsonify,render_template
import os
from dotenv import load_dotenv

from langchain_openai import OpenAI

load_dotenv()

app=Flask(__name__)
llm = ChatOpenAI(model='gpt-4o-mini')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/name', methods=['POST'])
def name():
    prompt = [
    SystemMessage(content="너는 작명소를 5년간 운영한 사람이야."),
    HumanMessage(content="이번에 식당 하나 차릴건데, 이름 추천해줘.")
]                            
    result = llm.invoke(prompt)

    return jsonify({"result":"success","chatbot":result.content})


if __name__=="__main__":
    app.run(debug=True)


# print(result.prompt)