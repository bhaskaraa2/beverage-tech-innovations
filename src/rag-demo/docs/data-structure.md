
1. **Stores Data Structure**

Purpose: Track retail locations and their operational characteristics

| Column | Type | Description | Example | Purpose |
|--------|------|-------------|----------|----------|
| store_id | string | Unique store identifier | STORE001 | Primary key for store identification |
| name | string | Store name | Downtown Store | Human-readable store reference |
| location | string | Physical location | Shopping Mall | Geographic tracking |
| type | string | Store category | Retail, Gas Station | Business model classification |
| capacity | integer | Store capacity | 1000 | Inventory planning |
| opening_hours | string | Operating hours | 24/7, 9AM-10PM | Operations scheduling |
| region | string | Geographic region | North, Central | Regional management |

2. **Products Data Structure**

Purpose: Maintain beverage product catalog and supplier relationships

| Column | Type | Description | Example | Purpose |
|--------|------|-------------|----------|----------|
| product_id | string | Unique product identifier | PROD001 | Primary key for product tracking |
| name | string | Product name | Cola Classic | Consumer-facing identification |
| category | string | Product category | Soda, Water, Tea | Product classification |
| unit_price | float | Price per unit | 2.50 | Pricing management |
| pack_size | integer | Units per pack | 6, 12, 24 | Inventory unit definition |
| storage_temp | string | Storage temperature | Cold, Room Temperature | Storage requirements |
| supplier_id | string | Supplier reference | SUP001 | Supplier relationship |

3. **Inventory Data Structure**
Purpose: Track real-time inventory levels and storage conditions

| Column | Type | Description | Example | Purpose |
|--------|------|-------------|----------|----------|
| store_id | string | Store reference | STORE001 | Location tracking |
| product_id | string | Product reference | PROD001 | Product identification |
| stock_level | integer | Current stock | 250 | Inventory monitoring |
| reorder_point | integer | Reorder threshold | 75 | Automated reordering |
| max_capacity | integer | Maximum capacity | 750 | Storage limitation |
| last_restock | datetime | Last restock date | 2024-01-01 10:30:00 | Restock tracking |
| temperature | float | Current temperature | 4.5 | Quality control |

4. **POS Terminals Data Structure**

Purpose: Manage point-of-sale devices and their operational status

| Column | Type | Description | Example | Purpose |
|--------|------|-------------|----------|----------|
| terminal_id | string | Unique terminal ID | POS001 | Terminal identification |
| store_id | string | Store reference | STORE001 | Location association |
| type | string | Terminal type | Standard, Self-Service | Terminal classification |
| location | string | Terminal location | Front, Back | In-store positioning |
| status | string | Operational status | Active, Maintenance | Availability tracking |
| last_maintenance | date | Last service date | 2024-01-01 | Maintenance scheduling |

5. **Sales History Data Structure**
Purpose: Record all sales transactions and analyze business performance

| Column | Type | Description | Example | Purpose |
|--------|------|-------------|----------|----------|
| transaction_id | string | Unique transaction ID | TRX000001 | Transaction tracking |
| store_id | string | Store reference | STORE001 | Sales location |
| terminal_id | string | Terminal reference | POS001 | Sales point |
| terminal_type | string | Type of terminal | Standard | Service type tracking |
| product_id | string | Product reference | PROD001 | Product sold |
| quantity | integer | Units sold | 3 | Sales volume |
| unit_price | float | Price per unit | 2.50 | Price tracking |
| total_amount | float | Transaction total | 7.50 | Revenue tracking |
| payment_method | string | Payment type | Credit Card | Payment analytics |
| cashier_id | string | Cashier reference | CASH001 | Staff tracking |
| timestamp | datetime | Transaction time | 2024-01-01 14:30:00 | Time analysis |
| status | string | Transaction status | Completed | Transaction validation |

6. **Batch Templates Data Structure**

Purpose: Define standard reorder patterns for efficient inventory management

| Column | Type | Description | Example | Purpose |
|--------|------|-------------|----------|----------|
| template_id | string | Template identifier | TEMP001 | Template reference |
| name | string | Template name | Morning Restock | Template identification |
| priority | string | Priority level | High, Medium, Low | Order prioritization |
| products | list | Product IDs | [PROD001, PROD002] | Product grouping |
| quantities | list | Order quantities | [100, 150] | Standard order sizes |

7. **Suppliers Data Structure**

Purpose: Manage supplier relationships and performance tracking |

| Column | Type | Description | Example | Purpose |
|--------|------|-------------|----------|----------|
| supplier_id | string | Unique supplier ID | SUP001 | Supplier identification |
| name | string | Supplier name | Beverage Co | Business reference |
| contact | string | Contact email | contact1@supplier.com | Communication |
| lead_time_days | integer | Delivery lead time | 3 | Order planning |
| reliability_score | float | Reliability rating | 0.95 | Supplier evaluation |
