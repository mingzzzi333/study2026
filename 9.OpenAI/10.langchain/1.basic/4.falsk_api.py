from langchain_openai import ChatOpenAI  # Q&A 용으로 사용 (Chat Model = gpt-3.5-turbo)
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from flask import Flask,request,jsonify
import os
from dotenv import load_dotenv

from langchain_openai import OpenAI

load_dotenv()
openai_api_key=os.environ.get('OPEN_API_KEY')

app=Flask(__name__)
llm = ChatOpenAI(model='gpt-4o-mini')

@app.run('/api/name',methods=['POST'])
def name():
    prompt = [
    SystemMessage(content="너는 작명소를 5년간 운영한 사람이야."),
    HumanMessage(content="이번에 식당 하나 차릴건데, 이름 추천해줘.")
]                            
    result = llm.invoke(prompt)

    return jsonify({"result":"success","chatbot":result.content})

@app.run('/api/name',methods=['POST'])
def name2():
    data = request.get_json()
    product=data.get("product")
    user_prompt=f"너는 {product}를 만드었다"
    print(user_prompt)
    
    prompt = [
    SystemMessage(content="너는 작명소를 5년간 운영한 사람이야."),
    HumanMessage(content="이번에 식당 하나 차릴건데, 이름 추천해줘.")
]                            
    result = llm.invoke(prompt)
    return jsonify({"result":"success","chatbot":result.content})


@app.route('/api/dinner')
def dinner():
    prompt = [
    SystemMessage(content="당신은 경력 30년차 호텔 쉐프."),
    HumanMessage(content="이번주에 요리 하나 할건데 추천해줘.")
]                            
    result = llm.invoke(prompt)
    return jsonify({"result":"success","chatbot":result.content})

if __name__=="__main__":
    app.run(debug=True)


# print(result.prompt)