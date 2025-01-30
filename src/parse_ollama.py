from ollama import chat
from ollama import ChatResponse
import pandas as pd
import re


class MyOllamaChat:
    def __init__(self, model: str = 'llama3.2'):
        self.model = model
        self.prompt = """
        act and role play as senior data engineer

        skills:
        - your skills are python, sql, spark, etl, Airflow, DBT, docker 
        - your experience is 7 years

        context:
        - you should check the given job title based on your experience and skills and in outcome estimate how much is this job title related to your skills and experience, output should be just a numeric value
        - Jobs with english description should get higher percentage
        - jobs with title as data engineer should get higher percentage
        - if there is irrelevant job title, you should give 0 percentage 

        Expected Output: one percentage number
        """
        self.prompt2 = """
        No, just write a number in output
        """

    def ask_question(self, question: str) -> str:
        response: ChatResponse = chat(model=self.model, messages=[
            {
                'role': 'user',
                'content': question,
            },
        ])
        print(response['message']['content'])
        return response.message.content

    def get_related_percentage(self, job_title: str) -> int:
        try:
            response: ChatResponse = chat(model=self.model, messages=[
                {
                    'role': 'system',
                    'content': self.prompt,
                },
                {
                    'role': 'system',
                    'content': self.prompt2,
                },
                {
                    'role': 'user',
                    'content': job_title,
                },
            ])
            related_percentage = response.message.content
            match = re.search(r'\d+', related_percentage)
            if match:
                related_percentage = int(match.group())
            else:
                related_percentage = 0

            return related_percentage
        except Exception as e:
            print(e)
            return 0

    def add_related_percentage(self, df: pd.DataFrame, custom_prompt: str = None) -> pd.DataFrame:
        # set custom prompt if provided
        if custom_prompt:
            self.prompt = custom_prompt
            print(f'custom prompt: {self.prompt}')

        df['percentage'] = df['title'].apply(
            lambda x: self.get_related_percentage(x) if pd.notna(x) else 0)
        return df
