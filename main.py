import os
import streamlit as st
from src.scrape import WebScraper
from src.persist import DataFramePersist
from src.parse_ollama import MyOllamaChat
from dotenv import load_dotenv


# Load environment variables
load_dotenv()
llm_model: str = os.getenv("llm_model")
scraped_files_path: str = os.getenv("scraped_files_path")
analyzed_files_path: str = os.getenv("analyzed_files_path")

# Initialize
scrape = WebScraper()
df_persist_data = DataFramePersist(directory=scraped_files_path)
df_persist_estimated = DataFramePersist(directory=analyzed_files_path)
ollama_chat = MyOllamaChat(model=llm_model)


def main():
    st.title('look at job market')
    prompt = st.text_area("add a custom prompt",
                          "I am a Data Engineer with 6 years of experience in the data field. "
                          "Find the most relevant jobs related to my skills and experience ",
                          )

    # radio button
    websites = st.radio(
        "select websites",
        ["all", "indeed", "linkedin", "stepstone", "xing"],
        index=1
    )

    # use cached data
    if st.checkbox("Use cached data", value=True):
        crawl_enbaled = False
    else:
        crawl_enbaled = True

    # use cached given score
    if st.checkbox("Use cached given score", value=True):
        given_score = False
    else:
        given_score = True
    #
    if st.button("Scrape Websites"):
        st.write("Scraping the website...")
        # Scrape the website
        if crawl_enbaled:
            scrape.fetch_page()

        if websites == "all":
            # load data
            df = df_persist_data.load_dataframes('all')
        elif websites == "indeed":
            df = df_persist_data.load_dataframes('indeed.csv')
        elif websites == "linkedin":
            df = df_persist_data.load_dataframes('linkedin.csv')
        elif websites == "stepstone":
            df = df_persist_data.load_dataframes('stepstone.csv')
        else:
            st.write('not selected!')

        st.write(df['provider'].value_counts())
        # pass to ollama
        if given_score:
            df = ollama_chat.add_related_percentage(
                df=df, custom_prompt=prompt)
            # persist
            df_persist_estimated.save_dataframe(df, 'indeed_withP.csv')
        else:
            df = df_persist_estimated.load_dataframes('indeed_withP.csv')

        # sort jobs based on related percentage
        for index, row in df.sort_values('percentage', ascending=False).iterrows():
            st.text_area(f'job id: {index} provider: {
                row['provider']} Ollama related estimate based on prompt: {row['percentage']}', row['title'], height=150)


if __name__ == "__main__":
    main()
