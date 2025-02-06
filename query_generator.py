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
            instructions=[
                "You are a MongoDB query generator. Based on the provided knowledge base, "
                "generate **optimized** MongoDB queries for any given natural language request.",
                f"Knowledge base: {json.dumps(KNOWLEDGE_BASE, indent=2)}",
                
                "### 🔍 Query Generation Guidelines:",
                "1️⃣ Identify the relevant collection(s) based on the query request.",
                "2️⃣ If the request involves **filtering**, include appropriate `$match` conditions.",
                "3️⃣ If the request requires **counting**, return a JSON object with `count` only.",
                "4️⃣ If the request involves **aggregations** (e.g., total order amount per user), use the `$group` stage.",
                "5️⃣ If the request involves **joins** (e.g., user order details), use `$lookup` to combine `users` and `orders` collections.",
                "6️⃣ If a projection is needed (e.g., only usernames), return only required fields using `{ field_name: 1, _id: 0 }`.",
                "7️⃣ Always return queries in **valid JSON format**.",
                
                "### 🔹 Handling Relations:",
                "- The `orders.user_id` field references `users._id`.",
                "- When retrieving orders, **always join with users** if user details are required.",
                
                "### 🔹 Examples:",
                "- _Find all active users_: `db.users.find({ status: 'active' })`",
                "- _Get total sales per user_: Use `$group` to sum `total` by `user_id`.",
                "- _List users who placed orders_: Use `$lookup` to join `users` and `orders`.",
                
                "### ⚠️ Constraints:",
                "- **Read-only queries** (no inserts, updates, or deletes).",
                "- Always ensure valid MongoDB syntax."
            ],
            response_model=MongoQuery,
        )

