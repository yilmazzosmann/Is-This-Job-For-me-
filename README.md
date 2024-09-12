# Is This Job For Me?

A while ago my friend mentioned that job descriptions are long and some important details are written inside the text. There are different important factors for each person when checking these long descriptions. So, I designed a quick chatbot GUI to be with you, checking important details for you while you are concentrating on the job description and your responsibilities.

What can be these conditions:
- It can be location, language, work permit, or any other condition.
- It can be related to visa issues you can't comply.
- It can be travel requirements you don't want.
- It can be a specific skill you don't have that is mentioned a lot.
            
There are 2 versions of the app, one works on your own local PC, is totally secure, and no information about your conditions is shared with any 3rd party. But for this to work, you need a GPU in your machine. The second option works with Google's Gemini 1.5 Flash, totally on the cloud and your chat will be included in Google's datasets in the future. If the conditions you mention are important for you, and if you have a GPU, run locally, otherwise, you can use the cloud.

**Basically, you check if your skills match the job, language model will check whether your conditions are met or not!**

## Let's first see the app in action
https://github.com/user-attachments/assets/52b08ba1-98e9-4b4b-b392-f23010ee83d9

https://github.com/user-attachments/assets/6d0aee3a-8fab-49a0-90ad-31a8d4d6fc37

## How to run?

### Local Version
Download and run [ollama](https://ollama.com/download)

Check http://localhost:11434 shows "Ollama is running"

Download a model from [ollama model options](https://ollama.com/library). To do that, open the command prompt, and write *ollama pull model_name* I have found gemma2:2b model was working okay for me, but if you have better GPU, you can try better models like llama3.1 8B

Clone the project to your working directory, or download it from Github. Download Python if you do not have it (I used Python 3.9) and go to the working directory of the project. Run **```pip install -r requirements.txt```** from the command prompt. And then run **```python local_gui.py```**

### Cloud Gemini version
Clone the project to your working directory, or download it from Github. Download Python if you do not have it (I used Python 3.9) and go to the working directory of the project. Run **```pip install -r requirements.txt```** from the command prompt and **```pip install -U -q "google-generativeai>=0.7.2```**. And then run **```python cloud_gui.py```**

## Change Conditions
Please, go to whichever version you use of the app, local or cloud, go to the code, and find *self.chat_base* around line 55 or 60. Add your own conditions, specific to you, that you want the language model to check against the job description. You are the user, and you list your conditions, once you run the app with your conditions, **you will just copy paste the job description, and the app will add that as a continuity to the user prompt**. After that, you can discuss other details about the job description or make the LLM write a cover letter for you. **Once you want to discuss a new job description, just push restart chat and paste the new job description**

```
self.chat_base = [{"role": "system", "content": """
            You are an AI assistant that checks if a job searcher's conditions align with a job description. 
            Focus only on given conditions and the job description. Do not check technical compatibility or 
            infer additional information. Analyze each provided condition against the job description. Provide a clear, concise 
            "Yes" or "No" response with a brief explanation. Do not offer additional advice or elaborations."""},

            {"role": "user", "content": """
            Hello, I am looking for a job. Can you help me check if a job is suitable for me? Here are my conditions:
            - Please write here important conditions that you want to check against the job description.
            - It can be location, language, work permit, or any other condition.
            - It can be related to visa issues you can't comply.
            - It can be travel requirements you don't want.
            - It can be a specific skill you don't have that is mentioned a lot.
             
            Check these conditions against the following job description. Respond with "Yes" or "No" and a brief explanation in 1-2 sentences.
            If "No", cite the conflicting text from the job description.

            Job description:
            """}]
```
