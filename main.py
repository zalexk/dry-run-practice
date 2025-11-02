import streamlit as st
from openai import OpenAI
from src import prompts
import urllib.parse

def call_llm(prompt):
    response = client.chat.completions.create(
        model = st.secrets["MODEL"],
        messages = [
            {"role": "system", 
            "content": prompt},
            
            {
                "role": "user",
                "content": "Generate a question"
            }
        ]
    )
    return response.choices[0].message.content
    

def encode_uri_component(text):
    text = text.strip() # Remove the space
    text = text.strip("```c") 
    text = text.strip("```")
    
    return urllib.parse.quote(text)


client = OpenAI(
    api_key = st.secrets["API_KEY"],
    base_url = st.secrets["BASE_URL"]
)

try:
    response = call_llm(prompts.question_prompt).split("|||")
except:
    st.error("Error occurs. Please Try Again")

code = response[0]
ans = response[1]

question_col, ans_col = st.columns(2)
with question_col:
    st.header("Code")
    st.markdown(code)

with ans_col:
    with st.form("User_Ans"):
        st.header("Answer Sheet")
        user_ans = st.text_area("Write down all the output of the code")
        submitted = st.form_submit_button("Submit")
        
    if submitted:
        if user_ans.strip() == ans.strip():
            st.write("Correct")
        else:
            st.write(f"""
**Wrong!**

The correct answer is 
```
{ans}
```
""")
            # if st.button("Need Help?"):
            #     prompt = prompts.explanation_prompt.format(
            #         question = code,
            #         user_input = user_ans,
            #         corr_ans = ans
            #     )
                
            #     #try:
            #     response = call_llm(prompt)
            #     # except:
            #     #     st.error("Error occurs. Please Try Again")
            #     st.write(response)
                
            #     url = f"https://pythontutor.com/render.html#code={encode_uri_component(code)}&cumulative=false&curInstr=0&heapPrimitives=nevernest&mode=display&origin=opt-frontend.js&py=c_gcc9.3.0&rawInputLstJSON=%5B%5D&textReferences=false"

            #     st.link_button("Visual Debugger", url)

if st.button("Regenerate"):
    st.rerun() # Regenerate a new question
