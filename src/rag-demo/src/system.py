import logging
from datetime import datetime
import pandas as pd
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from langchain_ollama import ChatOllama



from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]



# bge-base embedding model
import traceback

from typing import cast
import json

from config import Config

from typing import Dict, List, Optional
from typing import Any


class BeverageInventorySystem:
    def __init__(self, llm_index,model):
        self.logger = logging.getLogger(__name__)
        self.llm_index = llm_index
        if len(model)>  0:
            self.setup_llm(model)
        else:
            self.load_data()
            self.setup_knowledge_base()
    def setup_llm(self,model):
        """Setup LangChain agents"""
        tools = [self.check_inventory,self.analyze_sales]
        llm = ChatOllama(
            model =  model,
            verbose=True,
            disable_streaming="tool_calling",
            temperature = 0,
        )
        llm.bind_tools(tools)
        graph_builder = StateGraph(State)
        # Define the function that calls the model
        def chatbot(state: State):
            return {"messages": [llm.invoke(state["messages"])]}

        graph_builder.add_node("chatbot", chatbot)
        graph_builder.add_edge(START, "chatbot")
        graph_builder.add_edge(START, "chatbot")
        graph = graph_builder.compile()
        self.app = graph
        system_message = """You are an inventory management assistant.
                Your role is to help manage inventory levels and stock information.

                Available commands:
                - check_inventory: Check current stock levels
                - analyze_sales: Analyze sales data
                Respond in a clear, concise manner focusing on inventory-related information."""
        self.app.stream({"messages": [("system", system_message)]});

    def load_data(self) -> None:
        """Load all required datasets"""
        try:
            self.products_df = pd.read_csv(Config.DATA_DIR / "products.csv")
            self.stores_df = pd.read_csv(Config.DATA_DIR / "stores.csv")
            self.inventory_df = pd.read_csv(Config.DATA_DIR / "inventory.csv")
            self.terminals_df = pd.read_csv(Config.DATA_DIR / "pos_terminals.csv")
            self.sales_df = pd.read_csv(Config.DATA_DIR / "sales_history.csv")
            self.sales_df['timestamp'] = pd.to_datetime(self.sales_df['timestamp'])
        except Exception as e:
            self.logger.error(f"Error loading data: {e}")
            raise
    def process_batch_orders(self) -> List[Dict]:
        print("process batch orders")
        return []

    def setup_knowledge_base(self) -> None:
        # Here are indexing documents from the docs directory,
        # we can enhance it further to read structed data  from the docs directory
        """Setup RAG knowledge base"""
        try:
            documents = SimpleDirectoryReader(Config.DOCS_DIR).load_data()
            Settings.llm = self.llm_index.llm
            Settings.embed_model = self.llm_index.embed_model

            self.kb_index = VectorStoreIndex.from_documents(
                documents
            )
            self.query_engine = self.kb_index.as_query_engine()
        except Exception as e:
            self.logger.error(f"Error setting up knowledge base: {e}")
            raise



    def check_inventory(self, store_id: str, product_id: Optional[str] = None) -> Any:
        """Check inventory levels

        Args:
            store_id (str): store id
            product_id (Optional[str], optional): product id. Defaults to None
        """
        print(f"checking inventory ****** {store_id} {product_id}")
        try:
            # assume query as pd.DataFrame
            query = cast(pd.DataFrame, self.inventory_df[self.inventory_df.store_id == store_id])

            if product_id:
                query = cast(pd.DataFrame,query[query.product_id == product_id])

            return query.to_dict(orient="records")
        except Exception as e:
            self.logger.error(f"Error checking inventory: {e}")
            return {}


    def query(self, query: str) :
        """Query the knowledge base"""
        try:
            response = self.query_engine.query(query)
            if response.source_nodes:
                        for idx, source in enumerate(response.source_nodes, 1):
                            print(f"\nSource {idx}:\n")

                            print(
                                f"Text: {source.node.text[:200]}...\n")
                            print(
                                f"Score: {source.score if hasattr(source, 'score') else 'N/A'}\n")
                            print(
                                f"Metadata: {json.dumps(source.node.metadata, indent=2)}",
                            )
        except Exception as e:
            self.logger.error(f"Error querying knowledge base: {e}")

    def chat(self, msg: str) :

       try:
           for event in self.app.stream({"messages": [("user", msg)]}):
               for value in event.values():
                    print("Assistant:", value["messages"][-1].content)

       except Exception as e:
           self.logger.error(f"Error querying knowledge base: {e}")
           return {}

    def analyze_sales(self, store_id: str, start_date: datetime, end_date: datetime) -> Dict:
        """Analyze sales

        Args:
            store_id (str): store id
            start_date (datetime): start date
            end_date (datetime): end date
        """
        print(f"analyzing sales ****** {store_id} {start_date} {end_date}")
        try:
            store_sales = cast(pd.DataFrame, self.sales_df[
                (self.sales_df['store_id'] == store_id) &
                (self.sales_df['timestamp'].between(start_date, end_date))
            ]).to_dict(orient="records")
            print(store_sales)

            product_quantities = {}
            payment_methods = {}
            hourly_pattern = {}

            for record in store_sales:
                # Update product quantities
                prod_id = str(record['product_id'])
                product_quantities[prod_id] = product_quantities.get(prod_id, 0) + record['quantity']

                # Update payment methods
                pay_method = record['payment_method']
                payment_methods[pay_method] = payment_methods.get(pay_method, 0) + 1

                # Update hourly pattern
                hour = record['timestamp'].hour
                hourly_pattern[hour] = hourly_pattern.get(hour, 0) + 1

            return {
                'total_sales': sum(record['total_amount'] for record in store_sales),
                'transaction_count': len(store_sales),
                'top_products': dict(sorted(product_quantities.items(),
                                        key=lambda x: x[1],
                                        reverse=True)[:5]),
                'payment_methods': payment_methods,
                'hourly_pattern': hourly_pattern
            }

        except Exception as e:
            traceback.print_exc()
            self.logger.error(f"Error analyzing sales: {e}")
            return {}

    def update_inventory(self, store_id: str, product_id: str,
                        quantity_change: int) -> bool:
        """Update inventory levels"""
        try:
            mask = (
                (self.inventory_df['store_id'] == store_id) &
                (self.inventory_df['product_id'] == product_id)
            )

            if not mask.any():
                raise ValueError(f"No inventory record found for store {store_id} and product {product_id}")

            current_stock = self.inventory_df.loc[mask, 'stock_level'].iloc[0]
            new_stock = current_stock + quantity_change

            if new_stock < 0:
                raise ValueError(f"Insufficient stock: {current_stock} available, {abs(quantity_change)} requested")

            self.inventory_df.loc[mask, 'stock_level'] = new_stock
            return True

        except Exception as e:
            self.logger.error(f"Error updating inventory: {e}")
            return False
