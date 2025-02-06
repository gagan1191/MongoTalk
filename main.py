
from query_workflow import MongoDBQueryWorkflow
import streamlit as st
import pandas as pd
import json

st.title("MongoTalk")
user_request = st.text_area("Enter your natural language query:")


if st.button("Run Query"):
    workflow = MongoDBQueryWorkflow(session_id="mongo-query-workflow")
    result = workflow.run(request=user_request, database="test_db")

    query_metadata = None  # To store query details
    query_results = None   # To store actual query output

    for _resp_chunk in result:
        if _resp_chunk.content:  # Ensure content exists
            response_data = _resp_chunk.content

            try:
                parsed_data = json.loads(response_data)  # Safely parse JSON

                # If the response has 'query_generated', it's query metadata
                if "query_generated" in parsed_data and "operation" in parsed_data:
                    query_metadata = parsed_data
                # Otherwise, treat it as query results
                elif "documents" in parsed_data:
                    query_results = parsed_data["documents"]

            except json.JSONDecodeError:
                st.error(f"Error parsing JSON. Received: {response_data}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")

    # Create two columns for side-by-side display
    col1, col2 = st.columns(2)

    # Display query metadata in the left column
    with col1:
        st.subheader("🔍 Query Details")
        if query_metadata:
            st.json(query_metadata)  # Display JSON metadata
        else:
            st.warning("No query details available.")

    # Display query results in the right column
    with col2:
        st.subheader("📊 Query Results")
        if query_results:
            df = pd.DataFrame(query_results)

            # Convert '_id' to string (for readability)
            if "_id" in df.columns:
                df["_id"] = df["_id"].astype(str)

            st.dataframe(df)  # Display results as a table
        else:
            st.warning("No query results found.")
