import streamlit as st
import requests


API_URL = "http://localhost:8000"


st.set_page_config(
    page_title="Supplier Risk Graph",
    page_icon="🔎",
    layout="wide",
)


st.title("🔎 Supplier Risk Graph")

st.caption(
    "Investigate supplier entities, corporate relationships, "
    "and synthetic risk exposure using GraphRAG."
)


st.sidebar.header("Investigation")

supplier_id = st.sidebar.text_input(
    "Supplier ID",
    value="SUP-0001"
)


if st.sidebar.button("Investigate Supplier"):

    with st.spinner("Investigating supplier..."):

        response = requests.get(
            f"{API_URL}/supplier/{supplier_id}/investigate"
        )

    if response.status_code != 200:

        st.error(
            f"API request failed: {response.text}"
        )

    else:

        data = response.json()

        if data["risk_found"]:
            st.warning(
                f"Potential risk paths found: "
                f"{data['risk_path_count']}"
            )
        else:
            st.success(
                "No risk paths found in the demonstration dataset."
            )

        st.subheader("Risk Paths")

        for path in data["risk_paths"]:

            with st.expander(
                path.get("risk_type", "Risk")
            ):

                st.json(path)


st.divider()

st.subheader("Ask the Supplier Risk Graph")

question = st.text_input(
    "Ask a question",
    placeholder=(
        "Which suppliers have indirect risk exposure?"
    )
)


if st.button("Ask"):

    if not question.strip():

        st.warning("Enter a question.")

    else:

        with st.spinner("Searching graph and generating answer..."):

            response = requests.post(
                f"{API_URL}/ask",
                json={
                    "question": question
                }
            )

        if response.status_code != 200:

            st.error(
                f"API request failed: {response.text}"
            )

        else:

            result = response.json()

            st.subheader("Answer")

            st.write(
                result.get("answer", "")
            )

            st.subheader("Evidence")

            sources = result.get("sources", [])

            if sources:

                for source in sources:
                    st.write(source)

            graph_evidence = result.get(
                "graph_evidence",
                []
            )

            if graph_evidence:

                st.subheader(
                    "Graph Evidence"
                )

                st.json(graph_evidence)