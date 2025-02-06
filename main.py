import pandas as pd
import streamlit as st
import json
from query_workflow import MongoDBQueryWorkflow 

def flatten_json(nested_json, parent_key='', sep='_'):
    """Recursively flatten nested JSON objects."""
    flattened = {}
    for key, value in nested_json.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key

        if isinstance(value, dict):  # If value is a dict, recursively flatten it
            flattened.update(flatten_json(value, new_key, sep))
        elif isinstance(value, list):  # If value is a list, keep it as a string
            flattened[new_key] = json.dumps(value)  # Convert lists to JSON strings
        else:
            flattened[new_key] = value
    return flattened

st.title("MongoTalk")
user_request = st.text_area("Enter your natural language query:")

if st.button("Run Query"):
    workflow = MongoDBQueryWorkflow(session_id="mongo-query-workflow")
    result = workflow.run(request=user_request, database="test_db")

    query_metadata = None
    query_results = None

    for _resp_chunk in result:
        if _resp_chunk.content:
            response_data = _resp_chunk.content
            try:
                parsed_data = json.loads(response_data)

                if "query_generated" in parsed_data and "operation" in parsed_data:
                    query_metadata = parsed_data
                elif "documents" in parsed_data:
                    query_results = parsed_data["documents"]

            except json.JSONDecodeError:
                st.error(f"Error parsing JSON. Received: {response_data}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔍 Query Details")
        if query_metadata:
            st.json(query_metadata)
        else:
            st.warning("No query details available.")

    with col2:
        st.subheader("📊 Query Results")
        if query_results:
            # Flatten each document in the results
            flattened_results = [flatten_json(doc) for doc in query_results]
            df = pd.DataFrame(flattened_results)

            # Convert '_id' to string
            if "_id" in df.columns:
                df["_id"] = df["_id"].astype(str)

            st.dataframe(df)
        else:
            st.warning("No query results found.")
