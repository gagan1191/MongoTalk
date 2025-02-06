from pymongo import MongoClient
from config import MONGO_URI, DATABASE_NAME
from query_generator import MongoQueryGenerator
from typing import Iterator
from agno.workflow import Workflow, RunResponse, RunEvent
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from bson import ObjectId
import json
from pydantic import BaseModel, Field
# Load environment variables


class QueryResult(BaseModel):
    documents: list[dict] = Field(..., description="The documents returned by the query.")



class MongoDBQueryWorkflow(Workflow):
    query_generator: MongoQueryGenerator = MongoQueryGenerator()  # Default value
    mongo_client: MongoClient = MongoClient("mongodb://localhost:27017/")  # Default value

    def __init__(self, connection_string: str = "mongodb://localhost:27017/", **kwargs):
        super().__init__(**kwargs)
        # Update mongo_client if a different connection string is provided
        if connection_string:
            self.mongo_client = MongoClient(connection_string)


    def convert_object_ids(self, document):
        """Recursively convert ObjectId to string in the given document."""
        if isinstance(document, list):
            return [self.convert_object_ids(doc) for doc in document]
        elif isinstance(document, dict):
            return {
                key: (str(value) if isinstance(value, ObjectId) else self.convert_object_ids(value))
                for key, value in document.items()
            }
        else:
            return document

    def run(self, request: str, database: str) -> Iterator[RunResponse]:
        """Run the MongoDB query workflow."""
        # Step 1: Indicate that the workflow has started
        #yield RunResponse(event=RunEvent.run_started, content="Starting the MongoDB query workflow...")

        # Step 2: Generate the MongoDB query
        #yield RunResponse(event=RunEvent.run_started, content="Generating MongoDB query...")
        query_response = self.query_generator.run(request)
        #print(query_response)
        if not query_response or not query_response.content:
            yield RunResponse(event=RunEvent.run_failed, content="Failed to generate a query.")
            return



        #yield RunResponse(
        #    event=RunEvent.run_completed,
        #    content=f"Query generated: {json.dumps(query_response.content.query)} for collection: {query_response.content.collection}\n",
        #)

        # Step 3: Execute the MongoDB query
        #yield RunResponse(event=RunEvent.run_started, content="Executing MongoDB query...")
        try:
            db = self.mongo_client["test_db"]
            collection = db[query_response.content.collection]

            # **Allow only read operations**
            if query_response.content.operation == "find":
                result = list(collection.find(
                    query_response.content.query,
                    query_response.content.projection or {}  # Apply projection if provided
                ))

            elif query_response.content.operation == "aggregate":
                result = list(collection.aggregate(query_response.content.query))

            elif query_response.content.operation == "count":
                result = collection.count_documents(query_response.content.query)

            else:
                result = {"error": "Unauthorized operation. Read-only mode enabled."}

            # Convert ObjectId values to strings (if needed)
            result = self.convert_object_ids(result)
            yield RunResponse(
                event=RunEvent.run_completed,
                content=QueryResult(documents=result).model_dump_json(indent=2),
            )
        except Exception as e:
            yield RunResponse(event=RunEvent.run_failed, content=f"Query execution failed: {str(e)}")
            return

        # Step 4: Workflow Completed
        #yield RunResponse(event=RunEvent.workflow_completed, content="Workflow completed successfully.")
    query_generator: MongoQueryGenerator = MongoQueryGenerator()  # Default value
    mongo_client: MongoClient = MongoClient("mongodb://localhost:27017/")  # Default value

    def __init__(self, connection_string: str = "mongodb://localhost:27017/", **kwargs):
        super().__init__(**kwargs)
        # Update mongo_client if a different connection string is provided
        if connection_string:
            self.mongo_client = MongoClient(connection_string)


    def convert_object_ids(self, document):
        """Recursively convert ObjectId to string in the given document."""
        if isinstance(document, list):
            return [self.convert_object_ids(doc) for doc in document]
        elif isinstance(document, dict):
            return {
                key: (str(value) if isinstance(value, ObjectId) else self.convert_object_ids(value))
                for key, value in document.items()
            }
        else:
            return document

    def run(self, request: str, database: str) -> Iterator[RunResponse]:
        """Run the MongoDB query workflow."""
        # Step 1: Indicate that the workflow has started
        #yield RunResponse(event=RunEvent.run_started, content="Starting the MongoDB query workflow...")

        # Step 2: Generate the MongoDB query
        #yield RunResponse(event=RunEvent.run_started, content="Generating MongoDB query...")
        query_response = self.query_generator.run(request)
        #print(query_response)
        if not query_response or not query_response.content:
            yield RunResponse(event=RunEvent.run_failed, content="Failed to generate a query.")
            return



        yield RunResponse(
            event=RunEvent.run_completed,
            content=f"Query generated: {json.dumps(query_response.content.query)} {json.dumps(query_response.content.operation)} for collection: {query_response.content.collection}\n",
        )

        # Step 3: Execute the MongoDB query
        yield RunResponse(event=RunEvent.run_started, content="Executing MongoDB query...")
        try:
            db = self.mongo_client["test_db"]
            collection = db[query_response.content.collection]

            # **Allow only read operations**
            if query_response.content.operation == "find":
                result = list(collection.find(
                    query_response.content.query,
                    query_response.content.projection or {}  # Apply projection if provided
                ))

            elif query_response.content.operation == "aggregate":
                result = list(collection.aggregate(query_response.content.query))

            elif query_response.content.operation == "count":
                result = collection.count_documents(query_response.content.query)
                result = [{"count":result}]

            else:
                result = {"error": "Unauthorized operation. Read-only mode enabled."}

            # Convert ObjectId values to strings (if needed)
            
            result = self.convert_object_ids(result)
            #print(result)
            yield RunResponse(
                event=RunEvent.run_completed,
                content=QueryResult(documents=result).model_dump_json(indent=2),
            )
        except Exception as e:
            yield RunResponse(event=RunEvent.run_failed, content=f"Query execution failed: {str(e)}")
            return

        # Step 4: Workflow Completed
        yield RunResponse(event=RunEvent.workflow_completed, content="Workflow completed successfully.")