# Comprehensive MLlib Demo - All Major Components
import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.ml.feature import VectorAssembler, StringIndexer, OneHotEncoder
from pyspark.ml.classification import LogisticRegression, RandomForestClassifier
from pyspark.ml.regression import LinearRegression, RandomForestRegressor
from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import BinaryClassificationEvaluator, RegressionEvaluator, ClusteringEvaluator
from pyspark.ml import Pipeline

print('🔥 COMPREHENSIVE PYSPARK MLLIB DEMO 🔥')
print('=' * 60)

# Create Spark session
spark = SparkSession.builder.appName('Comprehensive-MLlib-Demo').config('spark.sql.adaptive.enabled', 'true').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

print(f'✅ Spark {spark.version} initialized')

# 1. CLASSIFICATION DEMO
print('\n📊 1. CLASSIFICATION ALGORITHMS')
print('-' * 40)

# Create customer churn dataset
customers = spark.range(1, 2001).withColumnRenamed('id', 'customer_id') \
    .withColumn('age', (rand(42) * 50 + 18).cast('int')) \
    .withColumn('monthly_charges', (rand(44) * 80 + 20)) \
    .withColumn('contract_type', when(rand(46) < 0.5, 'Month-to-month').otherwise('One year')) \
    .withColumn('churn', when((col('monthly_charges') > 70) & (col('contract_type') == 'Month-to-month'), 1).when(rand(55) < 0.2, 1).otherwise(0))

# Feature engineering
indexer = StringIndexer(inputCol='contract_type', outputCol='contract_indexed')
encoder = OneHotEncoder(inputCol='contract_indexed', outputCol='contract_encoded')
assembler = VectorAssembler(inputCols=['age', 'monthly_charges', 'contract_encoded'], outputCol='features')

# Create pipeline
pipeline = Pipeline(stages=[indexer, encoder, assembler])
features_df = pipeline.fit(customers).transform(customers)

train_df, test_df = features_df.randomSplit([0.8, 0.2], seed=42)

print(f'📋 Dataset: {customers.count()} customers')
print(f'📋 Churn rate: {customers.filter(col("churn") == 1).count() / customers.count() * 100:.1f}%')

# Test multiple classifiers
classifiers = {
    'Logistic Regression': LogisticRegression(featuresCol='features', labelCol='churn', maxIter=10),
    'Random Forest': RandomForestClassifier(featuresCol='features', labelCol='churn', numTrees=10)
}

evaluator = BinaryClassificationEvaluator(labelCol='churn', rawPredictionCol='rawPrediction')

for name, classifier in classifiers.items():
    start_time = time.time()
    model = classifier.fit(train_df)
    predictions = model.transform(test_df)
    auc = evaluator.evaluate(predictions)
    duration = time.time() - start_time
    print(f'  🎯 {name}: AUC = {auc:.4f} (trained in {duration:.2f}s)')

# 2. REGRESSION DEMO
print('\n📈 2. REGRESSION ALGORITHMS')
print('-' * 40)

# Create sales dataset
sales = spark.range(1, 2001).withColumnRenamed('id', 'sale_id') \
    .withColumn('store_size', when(rand(60) < 0.3, 'Small').when(rand(61) < 0.7, 'Medium').otherwise('Large')) \
    .withColumn('temperature', (rand(62) * 30 + 40)) \
    .withColumn('promotion', when(rand(63) < 0.3, 1).otherwise(0)) \
    .withColumn('sales_amount', 1000 + col('temperature') * 20 + when(col('promotion') == 1, 500).otherwise(0) + when(col('store_size') == 'Large', 800).when(col('store_size') == 'Medium', 400).otherwise(0) + (rand(64) * 500 - 250))

# Feature engineering for regression
size_indexer = StringIndexer(inputCol='store_size', outputCol='size_indexed')
size_encoder = OneHotEncoder(inputCol='size_indexed', outputCol='size_encoded')
reg_assembler = VectorAssembler(inputCols=['temperature', 'promotion', 'size_encoded'], outputCol='features')

reg_pipeline = Pipeline(stages=[size_indexer, size_encoder, reg_assembler])
sales_features = reg_pipeline.fit(sales).transform(sales)

sales_train, sales_test = sales_features.randomSplit([0.8, 0.2], seed=42)

print(f'📋 Dataset: {sales.count()} sales records')
print(f'📋 Avg sales: ${sales.agg(avg("sales_amount")).collect()[0][0]:.2f}')

# Test regressors
regressors = {
    'Linear Regression': LinearRegression(featuresCol='features', labelCol='sales_amount', maxIter=10),
    'Random Forest': RandomForestRegressor(featuresCol='features', labelCol='sales_amount', numTrees=10)
}

reg_evaluator = RegressionEvaluator(labelCol='sales_amount', predictionCol='prediction', metricName='rmse')

for name, regressor in regressors.items():
    start_time = time.time()
    model = regressor.fit(sales_train)
    predictions = model.transform(sales_test)
    rmse = reg_evaluator.evaluate(predictions)
    duration = time.time() - start_time
    print(f'  📈 {name}: RMSE = {rmse:.2f} (trained in {duration:.2f}s)')

# 3. CLUSTERING DEMO
print('\n🎲 3. CLUSTERING ALGORITHMS')
print('-' * 40)

# Create product dataset
products = spark.range(1, 1001).withColumnRenamed('id', 'product_id') \
    .withColumn('price', (rand(65) * 500 + 10)) \
    .withColumn('rating', (rand(66) * 4 + 1)) \
    .withColumn('reviews', (rand(67) * 1000 + 10).cast('int'))

prod_assembler = VectorAssembler(inputCols=['price', 'rating', 'reviews'], outputCol='features')
product_features = prod_assembler.transform(products)

print(f'📋 Dataset: {products.count()} products')

# Test clustering
kmeans = KMeans(featuresCol='features', k=4, seed=42)
model = kmeans.fit(product_features)
predictions = model.transform(product_features)

cluster_evaluator = ClusteringEvaluator(predictionCol='prediction', featuresCol='features')
silhouette = cluster_evaluator.evaluate(predictions)

print(f'  🎲 K-Means (k=4): Silhouette Score = {silhouette:.4f}')

# Show cluster distribution
cluster_counts = predictions.groupBy('prediction').count().orderBy('prediction').collect()
for row in cluster_counts:
    print(f'    Cluster {row.prediction}: {row.count} products')

print('\n✅ DEMO COMPLETE!')
print('🎉 All PySpark MLlib components working perfectly!')
print('📊 Classification: ✅  📈 Regression: ✅  🎲 Clustering: ✅  🔗 Pipelines: ✅')

spark.stop()
