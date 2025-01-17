import streamlit as st
from src.scrape import WebScraper
from src.persist import DataFramePersist
import time
from src.parse_ollama import MyOllamaChat

crawl_enbaled = False
scrape = WebScraper()
df_persist = DataFramePersist(directory='data')
ollama_chat = MyOllamaChat(model='llama3.2')


def main():

    st.title('related jobs')
    prompt = st.text_area("add a custom prompt", height=100)

    # radio button
    websites = st.radio(
        "select websites",
        ["all", "indeed", "linkedin", "stepstone"],
        index=1

    )

    # Step 1: Scrape the Website
    if st.button("Scrape Website"):
        st.write("Scraping the website...")
        # Scrape the website
        if crawl_enbaled:
            scrape.fetch_page()

        if websites == "all":
            # load data
            df = df_persist.load_dataframes('all')
        elif websites == "indeed":
            df = df_persist.load_dataframes('indeed.csv')
        elif websites == "linkedin":
            df = df_persist.load_dataframes('linkedin.csv')
        elif websites == "stepstone":
            df = df_persist.load_dataframes('stepstone.csv')
        else:
            st.write('not selected!')

        st.write(df['provider'].value_counts())
        # pass to ollama
        df = ollama_chat.add_related_percentage(df=df, custom_prompt=prompt)
        #
        for index, row in df.sort_values('percentage', ascending=False).iterrows():
            st.text_area(f'job id: {index} provider: {
                row['provider']} Ollama related estimate based on prompt: {row['percentage']}', row['title'], height=150)
        # st.dataframe(items)


if __name__ == "__main__":
    main()

    # Debugging:
    # scrape.fetch_page()
    # df = df_persist.load_dataframes('indeed.csv')
    # print(df['provider'].value_counts())
    # print(df.info())
    # # for index, row in df.iterrows():
    # #     print(row)
    # ollama_chat = MyOllamaChat(model='llama3.2')
    # ollama_chat.add_related_percentage(df=df)
    # df_persist_p = DataFramePersist(directory='data_estimated')
    # df_persist_p.save_dataframe(df, 'indeed_withP.csv')
