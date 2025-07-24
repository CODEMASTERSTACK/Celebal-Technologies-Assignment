import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, split, element_at, rand, row_number
from pyspark.sql.window import Window

def run_mnist_pipeline(spark, data_folder, delta_table_name):
    """
    This function does all the main work.
    It reads the pictures, does the random picking, and saves everything.
    """
    print("\nThe function is started!")
    print("------------------------------------")

    print(f"Now look for all the .png files inside: {data_folder}")
    
    all_images_df = (spark.read.format("binaryFile")
                     .option("pathGlobFilter", "*.png")
                     .option("recursiveFileLookup", "true")
                     .load(data_folder))

    print("\nNow Spark read the files. Here's what the schema looks like:")
    all_images_df.printSchema()
    
    # Caching this so Spark doesn't have to re-read it later.
    all_images_df.cache()
    
    print(f"\nFound {all_images_df.count()} total images. Nice!")

    images_with_labels = all_images_df.withColumn(
        "label",
        element_at(split(col("path"), "/"), -2).cast("integer")
    )
    print("\nJust added the 'label' column. Let's check a few rows:")
    images_with_labels.select("path", "label").show(5, truncate=False)

    print("Time to do the random sampling. Picking 5 images for each number...")
    
    # This sets up the 'groups' for the window function.
    window_for_sampling = Window.partitionBy("label").orderBy(rand())
    
    final_sample_df = (images_with_labels.withColumn("row_num", row_number().over(window_for_sampling))
                       .filter(col("row_num") <= 5)
                       .drop("row_num")) 

    print(f"\nDone with sampling! We have 50 rows now (10 numbers * 5 images).")
    print(f"Total rows in our final DataFrame: {final_sample_df.count()}")
    
    print("\nHere's the count for each label to make sure it's even:")
    final_sample_df.groupBy("label").count().orderBy("label").show()

    # The assignment says NO compression, so I have to set this config.
    print(f"\nSaving the results to a managed Delta table called '{delta_table_name}'.")
    print("Setting compression to 'uncompressed' as requested.")
    spark.conf.set("spark.sql.parquet.compression.codec", "uncompressed")

    # 'overwrite' mode will just replace the table if I run this script again.
    (final_sample_df.write
     .format("delta")
     .mode("overwrite")
     .saveAsTable(delta_table_name))

    print(f"\nSuccess! The table '{delta_table_name}' should is ready.")

    # Get rid of the cached data to free up memory.
    all_images_df.unpersist()

    # Step 5: Final check to prove it worked.
    print("\n--- Final Verification ---")
    print(f"Let's read from the table '{delta_table_name}' to see what's inside:")
    spark.read.table(delta_table_name).show(10)

    print(f"\nAnd now check the table details to make sure it's 'MANAGED':")
    spark.sql(f"DESCRIBE DETAIL {delta_table_name}").show(truncate=False)
    print("\nLooks good! Project complete.")


if __name__ == "__main__":
    
    # Getting the Spark session ready. Need the Delta Lake extension for this to work.
    spark_session = (SparkSession.builder
                     .appName("Celebal_Final_Assignment")
                     .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
                     .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
                     .getOrCreate())

    # This should be the path to the folder that has the '0', '1', '2', etc. folders inside it.
    my_data_path = "abfss://celebal_dataset@azuredlproject001.dfs.core.windows.net/flat_files/mnist_png/"
    my_table_name = "first_mnist_delta_table"
    run_mnist_pipeline(spark_session, my_data_path, my_table_name)

    #Stop the Spark session.
    spark_session.stop()
