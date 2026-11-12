import duckdb
import streamlit as st

con = duckdb.connect("data/exercices_sql_tables.duckdb")


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
# if query:
#     result = duckdb.sql(query).df()
#     st.dataframe(result)

#     try:
#         result = result[solution_df.columns]
#         st.dataframe(result.compare(solution_df))
#     except KeyError:
#         st.write("Some columns are missing")
#     except ValueError:
#         n_lines_differences = result.shape[0] - solution_df.shape[0]
#         st.write(f"Result has {n_lines_differences} lines with the solution")


# # tabes solution_dfs
# tab2, tab3 = st.tabs(["Table", "solution_df"])

# with tab2:
#     st.write("table: beverages")
#     st.dataframe(beverages)
#     st.write("table: food_items")
#     st.dataframe(food_items)
#     st.write("expected:")
#     st.dataframe(solution_df)

# with tab3:
#     st.write(ANSWER_STR)
