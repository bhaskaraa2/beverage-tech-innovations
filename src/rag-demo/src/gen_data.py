import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import logging
from config import Config

class TestDataGenerator:
    def __init__(self, output_path: Path ):
        self.output_path = output_path
        self.output_path.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)
        np.random.seed(42)

    def generate_stores(self) -> pd.DataFrame:
        """Generate store data"""
        stores_data = {
            'store_id': [f'STORE{str(i).zfill(3)}' for i in range(1, 11)],
            'name': [
                'Downtown Store', 'Mall Center', 'Gas Station', 'Beach Shop',
                'Airport Store', 'Plaza Store', 'Highway Stop', 'Central Market',
                'Station Store', 'Port Shop'
            ],
            'location': [
                'Downtown', 'Shopping Mall', 'Highway 101', 'Beach Road',
                'Terminal 2', 'City Plaza', 'Highway 202', 'Central District',
                'Train Station', 'Port Area'
            ],
            'type': [
                'Retail', 'Retail', 'Gas Station', 'Convenience', 'Airport',
                'Retail', 'Gas Station', 'Retail', 'Transit', 'Transit'
            ],
            'capacity': np.random.randint(300, 1200, 10),
            'opening_hours': [
                '24/7', '9AM-10PM', '24/7', '8AM-8PM', '6AM-11PM',
                '9AM-9PM', '24/7', '8AM-10PM', '7AM-11PM', '8AM-8PM'
            ],
            'region': ['North', 'Central', 'South', 'East', 'West'] * 2
        }
        df = pd.DataFrame(stores_data)
        df.to_csv(self.output_path / 'stores.csv', index=False)
        return df

    def generate_products(self) -> pd.DataFrame:
        """Generate product data"""
        products_data = {
            'product_id': [f'PROD{str(i).zfill(3)}' for i in range(1, 31)],
            'name': [
                'Cola Classic', 'Lemon Soda', 'Orange Fizz', 'Energy Boost',
                'Sparkling Water', 'Green Tea', 'Sports Drink', 'Fruit Punch',
                'Ginger Ale', 'Mineral Water', 'Black Tea', 'Coffee Cold Brew',
                'Mango Juice', 'Apple Cider', 'Coconut Water', 'Tonic Water',
                'Root Beer', 'Grape Soda', 'Berry Blast', 'Lime Fizz',
                'Peach Tea', 'Lemonade', 'Cherry Cola', 'Protein Shake',
                'Aloe Vera', 'Iced Coffee', 'Orange Juice', 'Cranberry Juice',
                'Diet Cola', 'Vitamin Water'
            ],
            'category': [
                'Soda', 'Soda', 'Soda', 'Energy', 'Water', 'Tea', 'Sports',
                'Juice', 'Soda', 'Water', 'Tea', 'Coffee', 'Juice', 'Cider',
                'Water', 'Mixer', 'Soda', 'Soda', 'Energy', 'Soda', 'Tea',
                'Juice', 'Soda', 'Protein', 'Health', 'Coffee', 'Juice',
                'Juice', 'Soda', 'Water'
            ],
            'unit_price': np.random.uniform(1.5, 5.0, 30).round(2),
            'pack_size': np.random.choice([6, 12, 24], 30),
            'storage_temp': np.random.choice(['Cold', 'Room Temperature'], 30),
            'supplier_id': [f'SUP{str(i).zfill(3)}' for i in range(1, 6)] * 6
        }
        df = pd.DataFrame(products_data)
        df.to_csv(self.output_path / 'products.csv', index=False)
        return df

    def generate_inventory(self, stores_df: pd.DataFrame,
                         products_df: pd.DataFrame) -> pd.DataFrame:
        """Generate inventory data"""
        inventory_data = []
        for _, store in stores_df.iterrows():
            for _, product in products_df.iterrows():
                inventory_data.append({
                    'store_id': store['store_id'],
                    'product_id': product['product_id'],
                    'stock_level': np.random.randint(50, 500),
                    'reorder_point': np.random.randint(50, 100),
                    'max_capacity': np.random.randint(500, 1000),
                    'last_restock': (datetime.now() -
                                   timedelta(days=np.random.randint(1, 30)))
                                   .strftime('%Y-%m-%d %H:%M:%S'),
                    'temperature': round(np.random.uniform(2.0, 8.0), 2)
                })
        df = pd.DataFrame(inventory_data)
        df.to_csv(self.output_path / 'inventory.csv', index=False)
        return df

    def generate_pos_terminals(self, stores_df: pd.DataFrame) -> pd.DataFrame:
        """Generate POS terminal data"""
        terminals_data = []
        terminal_types = ['Standard', 'Express', 'Self-Service', 'Mobile', 'Kiosk']
        locations = ['Front', 'Back', 'Drive-through', 'Outdoor', 'Express Lane']

        for _, store in stores_df.iterrows():
            num_terminals = np.random.randint(2, 6)
            for i in range(num_terminals):
                terminals_data.append({
                    'terminal_id': f"POS{len(terminals_data)+1:03d}",
                    'store_id': store['store_id'],
                    'type': np.random.choice(terminal_types),
                    'location': np.random.choice(locations),
                    'status': np.random.choice(
                        ['Active', 'Inactive', 'Maintenance'],
                        p=[0.8, 0.1, 0.1]
                    ),
                    'last_maintenance': (datetime.now() -
                                       timedelta(days=np.random.randint(1, 90)))
                                       .strftime('%Y-%m-%d')
                })
        df = pd.DataFrame(terminals_data)
        df.to_csv(self.output_path / 'pos_terminals.csv', index=False)
        return df

    def generate_sales_history(self, stores_df: pd.DataFrame,
                             products_df: pd.DataFrame,
                             pos_terminals_df: pd.DataFrame) -> pd.DataFrame:
        """Generate sales history data"""
        sales_data = []
        start_date = datetime(2024, 12, 25)
        end_date = datetime(2024, 12, 31)
        dates = pd.date_range(start=start_date, end=end_date, freq='h')
        payment_methods = ['Cash', 'Credit Card', 'Debit Card',
                         'Mobile Payment', 'Gift Card']
        cashier_ids = [f'CASH{str(i).zfill(3)}' for i in range(1, 11)]

        for date in dates:
            for _, store in stores_df.iterrows():
                # Get store's terminals
                store_terminals = pos_terminals_df[
                    (pos_terminals_df['store_id'] == store['store_id']) &
                    (pos_terminals_df['status'] == 'Active')
                ]

                if len(store_terminals) == 0:
                    continue

                # More sales during business hours
                if 8 <= date.hour <= 20:
                    num_transactions = np.random.randint(3, 10)
                else:
                    num_transactions = np.random.randint(0, 4)

                for _ in range(num_transactions):
                    terminal = store_terminals.sample().iloc[0]
                    transaction_id = f"TRX{len(sales_data)+1:06d}"
                    payment_method = np.random.choice(payment_methods)
                    cashier_id = (np.random.choice(cashier_ids)
                                if terminal['type'] != 'Self-Service'
                                else None)

                    # Generate multiple items per transaction
                    num_items = np.random.randint(1, 5)
                    for _ in range(num_items):
                        product = products_df.sample().iloc[0]
                        quantity = np.random.randint(1, 5)
                        sales_data.append({
                            'transaction_id': transaction_id,
                            'store_id': store['store_id'],
                            'terminal_id': terminal['terminal_id'],
                            'terminal_type': terminal['type'],
                            'product_id': product['product_id'],
                            'quantity': quantity,
                            'unit_price': product['unit_price'],
                            'total_amount': quantity * product['unit_price'],
                            'payment_method': payment_method,
                            'cashier_id': cashier_id,
                            'timestamp': date.strftime('%Y-%m-%d %H:%M:%S'),
                            'status': np.random.choice(
                                ['Completed', 'Voided', 'Refunded'],
                                p=[0.97, 0.02, 0.01]
                            )
                        })

        df = pd.DataFrame(sales_data)
        df.to_csv(self.output_path / 'sales_history.csv', index=False)
        return df

    def generate_batch_templates(self, products_df: pd.DataFrame) -> pd.DataFrame:
        """Generate batch order templates"""
        templates_data = {
            'template_id': [f'TEMP{str(i).zfill(3)}' for i in range(1, 6)],
            'name': ['Morning Restock', 'Weekend Supply', 'Holiday Pack',
                    'Emergency Stock', 'Regular Refill'],
            'priority': ['High', 'Medium', 'High', 'Critical', 'Low'],
            'products': [
                products_df.sample(n=5)['product_id'].tolist()
                for _ in range(5)
            ],
            'quantities': [
                [np.random.randint(50, 200) for _ in range(5)]
                for _ in range(5)
            ]
        }
        df = pd.DataFrame(templates_data)
        df.to_csv(self.output_path / 'batch_templates.csv', index=False)
        return df

    def generate_suppliers(self) -> pd.DataFrame:
        """Generate supplier data"""
        suppliers_data = {
            'supplier_id': [f'SUP{str(i).zfill(3)}' for i in range(1, 6)],
            'name': ['Beverage Co', 'Drinks Inc', 'Fresh Beverages',
                    'Global Drinks', 'Local Suppliers'],
            'contact': [f'contact{i}@supplier.com' for i in range(1, 6)],
            'lead_time_days': np.random.randint(1, 7, 5),
            'reliability_score': np.random.uniform(0.8, 1.0, 5).round(2)
        }
        df = pd.DataFrame(suppliers_data)
        df.to_csv(self.output_path / 'suppliers.csv', index=False)
        return df

    def generate_all(self):
        """Generate all test datasets"""
        try:
            self.logger.info("Starting test data generation...")

            # Generate base data
            stores_df = self.generate_stores()
            products_df = self.generate_products()
            suppliers_df = self.generate_suppliers()

            # Generate dependent data
            inventory_df = self.generate_inventory(stores_df, products_df)
            pos_terminals_df = self.generate_pos_terminals(stores_df)
            sales_df = self.generate_sales_history(
                stores_df, products_df, pos_terminals_df
            )
            batch_templates_df = self.generate_batch_templates(products_df)

            self.logger.info("Test data generation completed successfully!")

            # Return all generated dataframes
            return {
                'stores': stores_df,
                'products': products_df,
                'inventory': inventory_df,
                'pos_terminals': pos_terminals_df,
                'sales': sales_df,
                'batch_templates': batch_templates_df,
                'suppliers': suppliers_df
            }

        except Exception as e:
            self.logger.error(f"Error generating test data: {e}")
            raise

if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    c = Config()
    # Generate test data
    generator = TestDataGenerator(Config.DATA_DIR)
    data = generator.generate_all()

    # Print summary
    for name, df in data.items():
        print(f"\n{name.capitalize()} dataset:")
        print(f"Shape: {df.shape}")
        print("Sample:")
        print(df.head(2))
