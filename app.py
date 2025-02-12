import streamlit as st
from datetime import datetime
import chdb

def query_clickhouse(date):
    query = f"""
    SELECT *
    FROM s3('s3://clickhouse-alerts/*.json')
    WHERE generated = '{date}'
    ORDER BY generated ASC
    """
    result = chdb.query(query, "DataFrame")
    return result

def main():
    st.title('ClickHouse Google Alerts')
    selected_date = st.date_input("Choose a date", datetime.today())
    if st.button('Show alerts'):
        with st.spinner("Finding alerts...", show_time=True):
            data = query_clickhouse(selected_date.strftime('%Y-%m-%d'))
        if data.shape[0] > 0:
            for row in data.iterrows():
                attrs = row[1].to_dict()
                link_text = attrs['link'][:90] + "..." if len(attrs['link']) >= 90 else attrs['link']
                st.markdown(f"""
                #### {attrs['title']}  
                {attrs['summary']}  
                ➡️ [{link_text}]({attrs['link']})
                """, unsafe_allow_html=True)
        else:
            st.write("No data found for selected date.")

if __name__ == "__main__":
    main()

