from agno.agent import Agent
from agno.models.openai import OpenAIChat
from config import KNOWLEDGE_BASE
import json
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
from pydantic import BaseModel, Field
from typing import Dict, List, Union, Optional

class MongoQuery(BaseModel):
    collection: str = Field(..., description="The MongoDB collection to query.")
    operation: str = Field(..., description="Allowed operations: 'find', 'aggregate', 'count'.")
    query: Union[Dict, List[Dict]] = Field({}, description="The MongoDB query object.")
    projection: Optional[Dict] = Field(None, description="Optional projection fields to include/exclude in results.")



class MongoQueryGenerator(Agent):
    def __init__(self):
        super().__init__(

            model=OpenAIChat(id="gpt-4o-mini"),
            #model=Ollama(id=MODEL_ID),
            instructions=[
                "You are a MongoDB query generator. Based on the provided knowledge base, "
                "generate a valid MongoDB query for a given natural language request.",
                f"Knowledge base: {json.dumps(KNOWLEDGE_BASE, indent=2)}",
                "Output a JSON object with `query` and `collection` fields. if operation is count then show json count only",
                "If required only fields like if required only usernames for a query then db.users.find({query},{name:1,_id:0})"
            ],
            response_model=MongoQuery,
        )
