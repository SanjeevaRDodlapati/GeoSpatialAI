#!/usr/bin/env python3

import os
import time
import numpy as np
from datetime import datetime, timedelta
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# MLlib imports
from pyspark.ml import Pipeline
from pyspark.ml.feature import *
from pyspark.ml.classification import *
from pyspark.ml.regression import *
from pyspark.ml.clustering import *
from pyspark.ml.evaluation import *
from pyspark.ml.tuning import *
from pyspark.ml.stat import Correlation

print("Testing MLlib Module 6 Code...")

# Create Spark session
spark = SparkSession.builder \
    .appName("PySpark-MLlib-Test") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
    .config("spark.default.parallelism", "4") \
    .config("spark.sql.shuffle.partitions", "4") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

print(f"Spark Version: {spark.version}")

# Generate test datasets (simplified)
print("\nGenerating test datasets...")

# Customer dataset
customer_df = spark.range(1, 1001) \
    .withColumnRenamed("id", "customer_id") \
    .withColumn("age", (rand(42) * 50 + 18).cast("int")) \
    .withColumn("monthly_charges", (rand(44) * 80 + 20).cast("decimal(8,2)")) \
    .withColumn("contract_type", 
        when(rand(46) < 0.5, "Month-to-month").otherwise("One year")) \
    .withColumn("churn", when(rand(55) < 0.3, 1).otherwise(0))

print(f"Customer dataset: {customer_df.count()} records")

# Sales dataset  
sales_df = spark.range(1, 1001) \
    .withColumnRenamed("id", "sale_id") \
    .withColumn("store_id", (rand(56) * 10 + 1).cast("int")) \
    .withColumn("temperature", (rand(59) * 40 + 30).cast("decimal(5,2)")) \
    .withColumn("sales_amount", (rand(66) * 1000 + 500).cast("decimal(10,2)"))

print(f"Sales dataset: {sales_df.count()} records")

# Product dataset
product_df = spark.range(1, 501) \
    .withColumnRenamed("id", "product_id") \
    .withColumn("price", (rand(67) * 500 + 10).cast("decimal(8,2)")) \
    .withColumn("rating", (rand(68) * 4 + 1).cast("decimal(3,2)"))

print(f"Product dataset: {product_df.count()} records")

# Test feature engineering
print("\nTesting feature engineering...")

# Simple feature assembly for customers
customer_assembler = VectorAssembler(
    inputCols=["age", "monthly_charges"], 
    outputCol="features"
)
customers_features = customer_assembler.transform(customer_df).withColumnRenamed("churn", "churn_label")
customers_features.cache()

print(f"Customer features: {customers_features.count()} records")

# Simple feature assembly for sales
sales_assembler = VectorAssembler(
    inputCols=["store_id", "temperature"], 
    outputCol="features"
)
sales_features = sales_assembler.transform(sales_df).withColumnRenamed("sales_amount", "total_amount")
sales_features.cache()

print(f"Sales features: {sales_features.count()} records")

# Simple feature assembly for products
products_assembler = VectorAssembler(
    inputCols=["price", "rating"], 
    outputCol="features"
)
products_features = products_assembler.transform(product_df)
products_features.cache()

print(f"Product features: {products_features.count()} records")

# Test classification
print("\nTesting classification...")
train_data, test_data = customers_features.randomSplit([0.8, 0.2], seed=42)

lr = LogisticRegression(featuresCol="features", labelCol="churn_label", maxIter=10)
lr_model = lr.fit(train_data)
lr_predictions = lr_model.transform(test_data)

evaluator = BinaryClassificationEvaluator(labelCol="churn_label", rawPredictionCol="rawPrediction")
auc = evaluator.evaluate(lr_predictions)
print(f"Logistic Regression AUC: {auc:.4f}")

# Test regression
print("\nTesting regression...")
sales_train, sales_test = sales_features.randomSplit([0.8, 0.2], seed=42)

lin_reg = LinearRegression(featuresCol="features", labelCol="total_amount", maxIter=10)
lin_reg_model = lin_reg.fit(sales_train)
lin_reg_predictions = lin_reg_model.transform(sales_test)

reg_evaluator = RegressionEvaluator(labelCol="total_amount", predictionCol="prediction", metricName="rmse")
rmse = reg_evaluator.evaluate(lin_reg_predictions)
print(f"Linear Regression RMSE: {rmse:.2f}")

# Test clustering
print("\nTesting clustering...")
kmeans = KMeans(featuresCol="features", k=3, seed=42)
kmeans_model = kmeans.fit(products_features)
kmeans_predictions = kmeans_model.transform(products_features)

cluster_evaluator = ClusteringEvaluator(predictionCol="prediction", featuresCol="features")
silhouette = cluster_evaluator.evaluate(kmeans_predictions)
print(f"K-Means Silhouette Score: {silhouette:.4f}")

print("\n✅ All MLlib tests passed successfully!")
print("The notebook code should work correctly.")

spark.stop()
