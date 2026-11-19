import os
import subprocess
import sys
from datetime import date, timedelta

import duckdb
import pandas as pd
import streamlit as st

# créer la base seulement si elle n'existe pas encore
# (sinon elle serait recréée à chaque interaction Streamlit)
if not os.path.exists("data/exercices_sql_tables.duckdb"):
    subprocess.run([sys.executable, "init_db.py"], check=True)

con = duckdb.connect("data/exercices_sql_tables.duckdb", read_only=False)


def check_query_solution(solution_df: pd.DataFrame, query: str) -> None:
    """
    Run the user's SQL query and compare its result with the expected solution.

    Steps:
        1. Execute the query on the database and display the result.
        2. Reorder the result's columns like the solution's
           (a KeyError means some columns are missing).
        3. Sort the rows of both DataFrames so row order does not matter,
           then compare them cell by cell and display the differences.
        4. Warn if the number of rows differs from the solution.

    Args:
        solution_df (pd.DataFrame): expected result of the exercise.
        query (str): SQL query written by the user.

    Returns:
        None: feedback is displayed directly in the Streamlit app.
    """
    result = con.execute(query).df()
    st.dataframe(result)

    try:
        result = result[solution_df.columns]  # dans meme ordre
        cols = list(solution_df.columns)
        result_sorted = result.sort_values(cols).reset_index(drop=True)
        solution_sorted = solution_df.sort_values(cols).reset_index(drop=True)
        differences = result_sorted.compare(solution_sorted)
        if differences.empty:
            st.success("Bonne réponse !")
        else:
            st.dataframe(differences)
    except KeyError:
        st.warning("Some columns are missing")

    n_lines_differences = result.shape[0] - solution_df.shape[0]
    if n_lines_differences != 0:
        st.write(f"Result has {n_lines_differences} lines with the solution")


def select_theme_and_exercices() -> pd.DataFrame:
    """
    Let the user pick a theme and return the matching exercises.

    Steps:
        1. Fetch the available themes from the memory_state table.
        2. Display a selectbox so the user can choose a theme.
        3. Fetch the exercises of that theme, sorted from the least
           recently reviewed to the most recent, and display them.

    Returns:
        pd.DataFrame: exercises of the selected theme, sorted by
        last_reviewed, with an index reset from 0 (row 0 is the
        exercise to review first). Empty if no theme is selected.
    """
    available_theme = (
        con.execute("SELECT DISTINCT theme FROM memory_state").df()["theme"].unique()
    )
    theme = st.selectbox(
        "What would you like to review?",
        available_theme,
        index=None,
        placeholder="Select a theme",
    )

    exercice = (
        con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'")
        .df()
        .sort_values("last_reviewed")
        .reset_index(drop=True)
    )
    st.dataframe(exercice)
    return exercice


st.header("""
SQL SRS
Spaced Repetition System with SQL
""")

try:

    with st.sidebar:
        exercices = select_theme_and_exercices()

    exercice_name = exercices.loc[0, "exercise_name"]
    solution_fichier = f"answers/{exercice_name}.sql"

    with open(solution_fichier, "r") as f:
        solution = f.read()

    solution_df = con.execute(solution).df()

    st.subheader("Entrez votre code :")
    query = st.text_area(label="Votre code SQL ici", key="user_input")

    if query:
        check_query_solution(solution_df, query)

    for n_jours in [2, 7, 21]:
        if st.button(f"Revoir dans {n_jours} jours"):
            next_date = date.today() + timedelta(days=n_jours)
            con.execute(
                f"UPDATE memory_state SET last_reviewed = '{next_date}' WHERE exercise_name = '{exercice_name}'"
            )
            st.rerun()

    if st.button("Reset"):
        con.execute("UPDATE memory_state SET last_reviewed = '1970-01-01'")
        st.rerun()

    tab2, tab3 = st.tabs(["Table", "Solution query"])

    with tab2:
        tables_exercice = exercices.loc[0, "tables"]
        for table in tables_exercice:
            st.write(f"table: {table}")
            table_df = con.execute(f"SELECT * FROM {table}").df()
            st.dataframe(table_df)

    with tab3:
        st.write(solution)

except KeyError:
    st.write("Veuillez sélectionner un thème")
