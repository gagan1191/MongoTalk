
from query_workflow import MongoDBQueryWorkflow
from agno.utils.pprint import pprint_run_response
import streamlit as st

st.title("MongoDB Query Workflow")
user_request = st.text_area("Enter your natural language query:")

if st.button("Run Query"):
    workflow = MongoDBQueryWorkflow(session_id="mongo-query-workflow")
    result = workflow.run(request=user_request, database="test_db")
##    pprint_run_response(result)
#    st.text_area("Query Result", result, height=300)
    for _resp_chunk in result:
        # Display tool calls if available
        st.write(str(_resp_chunk.content))
