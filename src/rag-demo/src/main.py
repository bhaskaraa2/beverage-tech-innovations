#!/usr/bin/env python3

import argparse
from datetime import datetime, timedelta
import logging
import sys
from system import BeverageInventorySystem
from generic_llm import GenericLLMIndex
from typing import Optional



class BeverageInventoryManager:
    """Main application manager for Beverage Inventory System"""

    def __init__(self,support_langchain=False):
        """Initialize the system"""
        self.logger = logging.getLogger(__name__)
        self.setup_system(support_langchain)

    def setup_system(self,support_langchain=False):
        ## refere https://docs.llamaindex.ai/en/stable/getting_started/starter_example_local/
        """Setup and initialize the system components"""
        model = ""
        if support_langchain:
            model = "llama3-groq-tool-use"
        try:
            if support_langchain:
                self.system = BeverageInventorySystem(None,model)
            else:
                index = GenericLLMIndex(llm_provider="ollama", model_name="llama3.2")
                self.system = BeverageInventorySystem(index,model)

            self.logger.info("System initialized successfully")
        except Exception as e:
            self.logger.error(f"System initialization failed: {e}")
            raise


    def run_inventory_check(self, store_id: Optional[str]):
        """Run inventory check for specified store or all stores"""
        try:
            if store_id:
                inventory = self.system.check_inventory(store_id)
                self.logger.info(f"Inventory check completed for store {store_id}")
                return inventory
            else:
                all_inventory = {}
                for store in self.system.stores_df['store_id']:
                    all_inventory[store] = self.system.check_inventory(store)
                self.logger.info("Complete inventory check finished")
                return all_inventory
        except Exception as e:
            self.logger.error(f"Inventory check failed: {e}")
            raise

    def process_batch_orders(self):
        """Process pending batch orders"""
        try:
            processed = self.system.process_batch_orders()
            self.logger.info(f"Processed {len(processed)} batch orders")
            return processed
        except Exception as e:
            self.logger.error(f"Batch order processing failed: {e}")
            raise
    def query(self, query: str) :
        """Query the knowledge base"""
        try:
            self.system.query(query)

        except Exception as e:
            self.logger.error(f"Error querying knowledge base: {e}")
            return {}

    def chat(self, query: str) :
        try:
            self.system.chat(query)
        except Exception as e:
            self.logger.error(f"Error querying knowledge base: {e}")
            return {}


    def analyze_sales(self, store_id: str, days: int = 30):
        """Analyze sales for specified store and time period"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            analysis = self.system.analyze_sales(store_id, start_date, end_date)
            self.logger.info(f"Sales analysis completed for store {store_id}")
            return analysis
        except Exception as e:
            self.logger.error(f"Sales analysis failed: {e}")
            raise

def main():
    """Main entry point for the application"""
    parser = argparse.ArgumentParser(description='Beverage Inventory System')
    parser.add_argument('--action', choices=['inventory', 'batch', 'sales','query',"chat"],
                       required=True, help='Action to perform')
    parser.add_argument('--store', help='Store ID for specific operations')
    parser.add_argument('--days', type=int, default=30,
                       help='Number of days for sales analysis')

    args = parser.parse_args()

    # Setup logging
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler(stream=sys.stdout))
    try:
        # Initialize system
        manager = BeverageInventoryManager(args.action == 'chat')

        # Execute requested action
        if args.action == 'inventory':
            result = manager.run_inventory_check(args.store)
            print("\nInventory Check Results:")
            for store_id, inventory in (result.items() if isinstance(result, dict) else {args.store: result}.items()):
                print(f"\nStore: {store_id}")
                for item in inventory:
                    print(f"Product: {item['product_id']}, Stock: {item['stock_level']}")

        elif args.action == 'batch':
            result = manager.process_batch_orders()
            print("\nBatch Processing Results:")
            for batch in result:
                print(f"Batch {batch['batch_id']}: {batch['status']}")

        elif args.action == 'sales':
            if not args.store:
                raise ValueError("Store ID required for sales analysis")
            result = manager.analyze_sales(args.store, args.days)
            print(result)
            print(f"\nSales Analysis for Store {args.store}:")
            print(f"Total Sales: ${result['total_sales']:,.2f}")
            print(f"Transactions: {result['transaction_count']}")
            print("\nTop Products:")
            for prod, qty in result['top_products'].items():
                print(f"- {prod}: {qty} units")
        elif args.action == 'query':
            # read query from stdin
            print("Query:")
            query = sys.stdin.readline()
            manager.query(query)
        elif args.action == "chat":
            # read query from stdin
            print("Query:")
            query = sys.stdin.readline()
            manager.chat(query)
        logger.info("Operation completed successfully")

    except Exception as e:
        logger.error(f"Operation failed: {e}")
        raise

if __name__ == "__main__":
    main()
