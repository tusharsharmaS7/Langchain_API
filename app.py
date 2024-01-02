import flask
from flask import request, jsonify, session
import psycopg2 
from langchain.llms import OpenAI
from langchain.chains import TextGenerationChain 
import os  

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = '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'  
# Database connection 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@host:port/database_name'
db = psycopg2.connect(**app.config['SQLALCHEMY_DATABASE_URI'])

@app.route('/your_api_endpoint', methods=['POST'])
def create_session():
    user_id = request.json['user_id']
    prompt = request.json['prompt']
    
    chain = get_chain_from_session(user_id)
    if chain is None:
       
        llm = OpenAI(
            openai_api_key=os.environ.get("OPENAI_API_KEY"), 
            temperature=0.6,
            model_name=...,  
        )
        chain = TextGenerationChain(llm=llm)
        store_chain_in_session(user_id, chain)

    response = chain.run(prompt)
    

    return jsonify({'response': response.text, 'history': get_session_history(user_id)}) 

def get_chain_from_session(user_id):
    chain=session.get(user_id)
    return chain
    
    

def store_chain_in_session(user_id, chain):
    session[user_id]=chain
   
    

def get_session_history(user_id):
    cursor=db.cursor()
    cursor.execute("SELECT response FROM get_session_history WHERE user_id=%s",(user_id,))
    history=[row[0] for row in cursor.fetchall()]
    return history
    


if __name__ == '__main__':
    app.run(debug=True)

