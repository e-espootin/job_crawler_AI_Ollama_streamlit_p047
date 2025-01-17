import streamlit as st
from src.scrape import WebScraper
from src.persist import DataFramePersist
import time
from src.parse_ollama import MyOllamaChat

crawl_enbaled = False
scrape = WebScraper()
df_persist = DataFramePersist(directory='data')


def main():

    st.title('related jobs')
    url = st.text_input("add prompt")

    col1 = st.columns(1)

    # radio button
    websites = st.radio(
        "select websites",
        ["all", "indeed", "linkedin", "stepstone"],
        index=0

    )

    # Step 1: Scrape the Website
    if st.button("Scrape Website"):
        if websites == "all":
            st.write("Scraping the website...")

            # Scrape the website
            if crawl_enbaled:
                scrape.fetch_page()

            # load data
            df = df_persist.load_dataframes('all')
            st.write(df['provider'].value_counts())
            #
            for index, row in df.iterrows():
                st.text_area(f'job {index} provider {
                             row['provider']}', row['title'], height=150)
            # st.dataframe(items)

        else:
            st.write('not selected!')


if __name__ == "__main__":
    # main()
    # scrape.fetch_page()
    df = df_persist.load_dataframes('indeed.csv')
    print(df['provider'].value_counts())
    print(df.info())
    # for index, row in df.iterrows():
    #     print(row)
    ollama_chat = MyOllamaChat(model='llama3.2')
    ollama_chat.add_related_percentage(df=df)
    df_persist_p = DataFramePersist(directory='data_estimated')
    df_persist_p.save_dataframe(df, 'indeed_withP.csv')
