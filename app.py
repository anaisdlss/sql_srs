import ast

import duckdb
import streamlit as st

con = duckdb.connect("data/exercices_sql_tables.duckdb", read_only=True)


st.write("""
SQL SRS
Spaced Repetition System with SQL
""")

# données

# ANSWER_STR = """
# SELECT * FROM beverages
# CROSS JOIN food_items
# """

# solution_df = duckdb.sql(ANSWER_STR).df()


with st.sidebar:
    theme = st.selectbox(
        "What would you like to review?",
        ("cross_joins", "GroupBy", "window_functions"),
        index=None,
        placeholder="Select a theme",
    )
    st.write("You selected:", theme)

    exercice = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'").df()
    st.write(exercice)


# query sql
st.header("Entrez votre code :")
query = st.text_area(label="Votre code SQL ici", key="user_input")
if query:
    result_query = con.execute(query).df()
    st.dataframe(result_query)

#     try:
#         result = result[solution_df.columns]
#         st.dataframe(result.compare(solution_df))
#     except KeyError:
#         st.write("Some columns are missing")
#     except ValueError:
#         n_lines_differences = result.shape[0] - solution_df.shape[0]
#         st.write(f"Result has {n_lines_differences} lines with the solution")


# tabes solution_dfs
tab2, tab3 = st.tabs(["Table", "solution_df"])

with tab2:
    tables_exercice = ast.literal_eval(exercice.loc[0, "tables"])
    for table in tables_exercice:
        st.write(f"table: {table}")
        table_df = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(table_df)

with tab3:
    exercice_name = exercice.loc[0, "exercise_name"]
    solution_fichier = f"answers/{exercice_name}.sql"
    with open(solution_fichier, "r") as f:
        solution = f.read()
    st.write(solution)
