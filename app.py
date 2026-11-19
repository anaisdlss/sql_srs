import logging
import os

import duckdb
import streamlit as st

logger = logging.getLogger(__name__)

if "data" not in os.listdir():
    logger.info("Contenu du dossier : %s", os.listdir())
    logger.info("Création du dossier data")
    os.mkdir("data")


con = duckdb.connect("data/exercices_sql_tables.duckdb", read_only=True)


st.write("""
SQL SRS
Spaced Repetition System with SQL
""")


try:

    with st.sidebar:
        theme = st.selectbox(
            "What would you like to review?",
            ("cross_joins", "GroupBy", "window_functions"),
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

    exercice_name = exercice.loc[0, "exercise_name"]
    solution_fichier = f"answers/{exercice_name}.sql"
    with open(solution_fichier, "r") as f:
        solution = f.read()

    solution_df = con.execute(solution).df()

    # query sql
    st.header("Entrez votre code :")
    query = st.text_area(label="Votre code SQL ici", key="user_input")
    if query:
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

    # tabes solution_dfs
    tab2, tab3 = st.tabs(["Table", "solution_df"])

    with tab2:
        tables_exercice = exercice.loc[0, "tables"]
        for table in tables_exercice:
            st.write(f"table: {table}")
            table_df = con.execute(f"SELECT * FROM {table}").df()
            st.dataframe(table_df)

    with tab3:
        st.write(solution)

except KeyError:
    st.write("Veuillez sélectionner un thème")
