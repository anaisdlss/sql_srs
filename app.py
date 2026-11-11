import duckdb
import pandas as pd
import streamlit as st

st.write("hello world")

data = {"a": [1, 2, 3], "b": [4, 5, 6]}
df = pd.DataFrame(data)
st.write("df:")
st.write(df)

tab1, tab2, tab3 = st.tabs(["nom1", "nom2", "nom3"])

with tab1:
    # query SQL
    query_sql = st.text_area(label="Entrez votre input")
    st.write("Vous avez écrit la query suivante:")
    st.write(query_sql)
    results = duckdb.sql(query_sql).df()
    st.write(results)
