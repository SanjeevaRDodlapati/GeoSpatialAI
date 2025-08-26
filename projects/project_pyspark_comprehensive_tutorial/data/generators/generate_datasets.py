"""
PySpark Tutorial - Data Generation Script
Generates realistic datasets for the comprehensive PySpark tutorial.
"""

import os
import json
import csv
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from faker import Faker
import argparse

# Set seeds for reproducibility
random.seed(42)
np.random.seed(42)
fake = Faker()
Faker.seed(42)

class DatasetGenerator:
    """Generates various datasets for PySpark tutorial."""
    
    def __init__(self, output_dir="../raw"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def generate_ecommerce_data(self, num_customers=10000, num_orders=50000, num_products=1000):
        """Generate e-commerce transaction data."""
        print(f"Generating e-commerce data: {num_customers} customers, {num_orders} orders, {num_products} products...")
        
        # Generate products
        categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Beauty", "Toys"]
        products = []
        for i in range(num_products):
            product = {
                "product_id": i + 1,
                "name": fake.catch_phrase(),
                "category": random.choice(categories),
                "price": round(random.uniform(10, 500), 2),
                "brand": fake.company(),
                "rating": round(random.uniform(1, 5), 1),
                "in_stock": random.choice([True, False])
            }
            products.append(product)
        
        # Generate customers
        customers = []
        for i in range(num_customers):
            customer = {
                "customer_id": i + 1,
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "email": fake.email(),
                "phone": fake.phone_number(),
                "address": fake.address().replace('\n', ', '),
                "city": fake.city(),
                "state": fake.state(),
                "zip_code": fake.zipcode(),
                "country": "USA",
                "registration_date": fake.date_between(start_date="-2y", end_date="today").isoformat(),
                "age": random.randint(18, 70),
                "gender": random.choice(["M", "F", "Other"])
            }
            customers.append(customer)
        
        # Generate orders
        orders = []
        order_items = []
        for i in range(num_orders):
            customer = random.choice(customers)
            order_date = fake.date_between(start_date="-1y", end_date="today")
            
            order = {
                "order_id": i + 1,
                "customer_id": customer["customer_id"],
                "order_date": order_date.isoformat(),
                "status": random.choice(["completed", "pending", "cancelled", "shipped"]),
                "payment_method": random.choice(["credit_card", "debit_card", "paypal", "apple_pay"]),
                "shipping_cost": round(random.uniform(0, 25), 2),
                "total_amount": 0  # Will be calculated
            }
            
            # Generate order items
            num_items = random.randint(1, 5)
            total_amount = 0
            for j in range(num_items):
                product = random.choice(products)
                quantity = random.randint(1, 3)
                item_total = product["price"] * quantity
                total_amount += item_total
                
                order_item = {
                    "order_id": order["order_id"],
                    "product_id": product["product_id"],
                    "quantity": quantity,
                    "unit_price": product["price"],
                    "total_price": item_total
                }
                order_items.append(order_item)
            
            order["total_amount"] = round(total_amount + order["shipping_cost"], 2)
            orders.append(order)
        
        # Save datasets
        self._save_json(products, "ecommerce_products.json")
        self._save_json(customers, "ecommerce_customers.json")
        self._save_json(orders, "ecommerce_orders.json")
        self._save_json(order_items, "ecommerce_order_items.json")
        
        # Also save as CSV
        pd.DataFrame(products).to_csv(f"{self.output_dir}/ecommerce_products.csv", index=False)
        pd.DataFrame(customers).to_csv(f"{self.output_dir}/ecommerce_customers.csv", index=False)
        pd.DataFrame(orders).to_csv(f"{self.output_dir}/ecommerce_orders.csv", index=False)
        pd.DataFrame(order_items).to_csv(f"{self.output_dir}/ecommerce_order_items.csv", index=False)
        
        print(f"✅ E-commerce data generated: {len(products)} products, {len(customers)} customers, {len(orders)} orders")
    
    def generate_iot_sensor_data(self, num_sensors=100, num_readings=100000):
        """Generate IoT sensor data for time series analysis."""
        print(f"Generating IoT sensor data: {num_sensors} sensors, {num_readings} readings...")
        
        # Generate sensor metadata
        sensor_types = ["temperature", "humidity", "pressure", "light", "motion"]
        locations = ["factory_floor", "warehouse", "office", "outdoor", "server_room"]
        
        sensors = []
        for i in range(num_sensors):
            sensor = {
                "sensor_id": f"SENSOR_{i+1:03d}",
                "sensor_type": random.choice(sensor_types),
                "location": random.choice(locations),
                "latitude": round(random.uniform(40.0, 41.0), 6),  # NYC area
                "longitude": round(random.uniform(-74.5, -73.5), 6),
                "installation_date": fake.date_between(start_date="-1y", end_date="-6m").isoformat(),
                "manufacturer": fake.company(),
                "model": f"Model_{random.randint(100, 999)}"
            }
            sensors.append(sensor)
        
        # Generate sensor readings
        readings = []
        base_time = datetime.now() - timedelta(days=30)
        
        for i in range(num_readings):
            sensor = random.choice(sensors)
            timestamp = base_time + timedelta(minutes=random.randint(0, 30*24*60))  # 30 days of data
            
            # Generate realistic values based on sensor type
            if sensor["sensor_type"] == "temperature":
                value = round(random.normalvariate(22, 5), 2)  # Normal room temp
                unit = "celsius"
            elif sensor["sensor_type"] == "humidity":
                value = round(random.uniform(30, 80), 1)
                unit = "percent"
            elif sensor["sensor_type"] == "pressure":
                value = round(random.normalvariate(1013.25, 10), 2)  # Sea level pressure
                unit = "hPa"
            elif sensor["sensor_type"] == "light":
                value = round(random.uniform(0, 1000), 1)
                unit = "lux"
            else:  # motion
                value = random.choice([0, 1])  # Binary
                unit = "boolean"
            
            reading = {
                "reading_id": i + 1,
                "sensor_id": sensor["sensor_id"],
                "timestamp": timestamp.isoformat(),
                "value": value,
                "unit": unit,
                "quality": random.choice(["good", "fair", "poor"]),
                "battery_level": round(random.uniform(10, 100), 1)
            }
            readings.append(reading)
        
        # Save datasets
        self._save_json(sensors, "iot_sensors.json")
        self._save_json(readings, "iot_readings.json")
        
        # Save as CSV and Parquet
        sensors_df = pd.DataFrame(sensors)
        readings_df = pd.DataFrame(readings)
        
        sensors_df.to_csv(f"{self.output_dir}/iot_sensors.csv", index=False)
        readings_df.to_csv(f"{self.output_dir}/iot_readings.csv", index=False)
        
        # Convert timestamp for Parquet
        readings_df['timestamp'] = pd.to_datetime(readings_df['timestamp'])
        sensors_df.to_parquet(f"{self.output_dir}/iot_sensors.parquet")
        readings_df.to_parquet(f"{self.output_dir}/iot_readings.parquet")
        
        print(f"✅ IoT data generated: {len(sensors)} sensors, {len(readings)} readings")
    
    def generate_financial_data(self, num_stocks=50, num_days=365):
        """Generate stock market data for time series analysis."""
        print(f"Generating financial data: {num_stocks} stocks, {num_days} days...")
        
        # Generate stock metadata
        sectors = ["Technology", "Healthcare", "Finance", "Energy", "Consumer", "Industrial"]
        exchanges = ["NYSE", "NASDAQ", "AMEX"]
        
        stocks = []
        for i in range(num_stocks):
            stock = {
                "symbol": f"{fake.company()[:3].upper()}{random.randint(10, 99)}",
                "company_name": fake.company(),
                "sector": random.choice(sectors),
                "exchange": random.choice(exchanges),
                "market_cap": random.randint(1000000, 50000000000),
                "ipo_date": fake.date_between(start_date="-10y", end_date="-1y").isoformat()
            }
            stocks.append(stock)
        
        # Generate price data
        prices = []
        base_date = datetime.now() - timedelta(days=num_days)
        
        for stock in stocks:
            current_price = random.uniform(20, 200)
            
            for day in range(num_days):
                date = base_date + timedelta(days=day)
                
                # Skip weekends
                if date.weekday() >= 5:
                    continue
                
                # Simulate price movement
                daily_change = random.normalvariate(0, 0.02)  # 2% daily volatility
                current_price *= (1 + daily_change)
                
                # Ensure positive price
                current_price = max(current_price, 1.0)
                
                volume = random.randint(100000, 10000000)
                
                # Calculate OHLC
                open_price = current_price
                high_price = open_price * (1 + abs(random.normalvariate(0, 0.01)))
                low_price = open_price * (1 - abs(random.normalvariate(0, 0.01)))
                close_price = random.uniform(low_price, high_price)
                
                price_record = {
                    "symbol": stock["symbol"],
                    "date": date.strftime("%Y-%m-%d"),
                    "open": round(open_price, 2),
                    "high": round(high_price, 2),
                    "low": round(low_price, 2),
                    "close": round(close_price, 2),
                    "volume": volume,
                    "adj_close": round(close_price, 2)
                }
                prices.append(price_record)
                
                current_price = close_price
        
        # Save datasets
        self._save_json(stocks, "financial_stocks.json")
        self._save_json(prices, "financial_prices.json")
        
        pd.DataFrame(stocks).to_csv(f"{self.output_dir}/financial_stocks.csv", index=False)
        pd.DataFrame(prices).to_csv(f"{self.output_dir}/financial_prices.csv", index=False)
        
        print(f"✅ Financial data generated: {len(stocks)} stocks, {len(prices)} price records")
    
    def generate_social_media_data(self, num_users=5000, num_posts=20000):
        """Generate social media data for graph analysis."""
        print(f"Generating social media data: {num_users} users, {num_posts} posts...")
        
        # Generate users
        users = []
        for i in range(num_users):
            user = {
                "user_id": i + 1,
                "username": fake.user_name(),
                "email": fake.email(),
                "full_name": fake.name(),
                "bio": fake.text(max_nb_chars=200),
                "location": fake.city(),
                "join_date": fake.date_between(start_date="-3y", end_date="today").isoformat(),
                "followers_count": random.randint(0, 10000),
                "following_count": random.randint(0, 2000),
                "verified": random.choice([True, False]),
                "profile_image_url": fake.image_url()
            }
            users.append(user)
        
        # Generate follow relationships
        follows = []
        num_follows = num_users * 10  # Average 10 follows per user
        
        for i in range(num_follows):
            follower = random.choice(users)
            following = random.choice(users)
            
            if follower["user_id"] != following["user_id"]:
                follow = {
                    "follower_id": follower["user_id"],
                    "following_id": following["user_id"],
                    "follow_date": fake.date_between(start_date="-1y", end_date="today").isoformat()
                }
                follows.append(follow)
        
        # Generate posts
        posts = []
        for i in range(num_posts):
            user = random.choice(users)
            post = {
                "post_id": i + 1,
                "user_id": user["user_id"],
                "content": fake.text(max_nb_chars=280),
                "timestamp": fake.date_time_between(start_date="-1y", end_date="now").isoformat(),
                "likes_count": random.randint(0, 1000),
                "retweets_count": random.randint(0, 100),
                "replies_count": random.randint(0, 50),
                "hashtags": [f"#{fake.word()}" for _ in range(random.randint(0, 3))],
                "mentions": random.sample([u["username"] for u in users], random.randint(0, 2))
            }
            posts.append(post)
        
        # Generate interactions (likes, retweets)
        interactions = []
        num_interactions = num_posts * 5  # Average 5 interactions per post
        
        for i in range(num_interactions):
            user = random.choice(users)
            post = random.choice(posts)
            
            if user["user_id"] != post["user_id"]:  # Can't interact with own posts
                interaction = {
                    "interaction_id": i + 1,
                    "user_id": user["user_id"],
                    "post_id": post["post_id"],
                    "interaction_type": random.choice(["like", "retweet", "reply"]),
                    "timestamp": fake.date_time_between(start_date="-1y", end_date="now").isoformat()
                }
                interactions.append(interaction)
        
        # Save datasets
        self._save_json(users, "social_media_users.json")
        self._save_json(follows, "social_media_follows.json")
        self._save_json(posts, "social_media_posts.json")
        self._save_json(interactions, "social_media_interactions.json")
        
        # Save as CSV
        pd.DataFrame(users).to_csv(f"{self.output_dir}/social_media_users.csv", index=False)
        pd.DataFrame(follows).to_csv(f"{self.output_dir}/social_media_follows.csv", index=False)
        pd.DataFrame(posts).to_csv(f"{self.output_dir}/social_media_posts.csv", index=False)
        pd.DataFrame(interactions).to_csv(f"{self.output_dir}/social_media_interactions.csv", index=False)
        
        print(f"✅ Social media data generated: {len(users)} users, {len(posts)} posts, {len(interactions)} interactions")
    
    def generate_log_data(self, num_logs=50000):
        """Generate web server log data for analysis."""
        print(f"Generating log data: {num_logs} log entries...")
        
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        ]
        
        methods = ["GET", "POST", "PUT", "DELETE", "HEAD"]
        status_codes = [200, 301, 302, 400, 401, 403, 404, 500, 502, 503]
        endpoints = ["/", "/api/users", "/api/products", "/login", "/logout", "/search", "/cart", "/checkout"]
        
        logs = []
        base_time = datetime.now() - timedelta(days=7)
        
        for i in range(num_logs):
            timestamp = base_time + timedelta(seconds=random.randint(0, 7*24*3600))
            
            log_entry = {
                "timestamp": timestamp.isoformat(),
                "ip_address": fake.ipv4(),
                "method": random.choice(methods),
                "endpoint": random.choice(endpoints),
                "status_code": random.choice(status_codes),
                "response_size": random.randint(100, 50000),
                "user_agent": random.choice(user_agents),
                "referer": fake.url() if random.random() > 0.3 else "-",
                "session_id": fake.uuid4(),
                "user_id": random.randint(1, 1000) if random.random() > 0.2 else None
            }
            logs.append(log_entry)
        
        # Save as JSON and CSV
        self._save_json(logs, "web_server_logs.json")
        pd.DataFrame(logs).to_csv(f"{self.output_dir}/web_server_logs.csv", index=False)
        
        print(f"✅ Log data generated: {len(logs)} log entries")
    
    def _save_json(self, data, filename):
        """Save data as JSON file."""
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        print(f"  Saved: {filepath}")

def main():
    parser = argparse.ArgumentParser(description="Generate datasets for PySpark tutorial")
    parser.add_argument("--all", action="store_true", help="Generate all datasets")
    parser.add_argument("--ecommerce", action="store_true", help="Generate e-commerce data")
    parser.add_argument("--iot", action="store_true", help="Generate IoT sensor data")
    parser.add_argument("--financial", action="store_true", help="Generate financial data")
    parser.add_argument("--social", action="store_true", help="Generate social media data")
    parser.add_argument("--logs", action="store_true", help="Generate log data")
    parser.add_argument("--output", default="../raw", help="Output directory")
    
    args = parser.parse_args()
    
    generator = DatasetGenerator(args.output)
    
    if args.all or args.ecommerce:
        generator.generate_ecommerce_data()
    
    if args.all or args.iot:
        generator.generate_iot_sensor_data()
    
    if args.all or args.financial:
        generator.generate_financial_data()
    
    if args.all or args.social:
        generator.generate_social_media_data()
    
    if args.all or args.logs:
        generator.generate_log_data()
    
    print("\n🎉 Data generation completed successfully!")
    print(f"📁 All datasets saved to: {os.path.abspath(args.output)}")
    print("\n📋 Available datasets:")
    print("  - E-commerce: products, customers, orders, order_items")
    print("  - IoT: sensors, readings")
    print("  - Financial: stocks, prices")
    print("  - Social Media: users, follows, posts, interactions")
    print("  - Logs: web_server_logs")

if __name__ == "__main__":
    main()
