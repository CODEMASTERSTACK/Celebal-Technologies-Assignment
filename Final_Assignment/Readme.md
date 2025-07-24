# Reading binary file format from ADLS Gen2 using Python

## 1. Overview

This document provides a detailed explanation of the Python script `Reading_binary.py`. The script is designed to perform the following tasks:

1.  **Initialize a SparkSession** with the necessary configurations to work with Delta Lake.
2.  **Recursively scan a directory** to find and read all PNG image files.
3.  **Process the file paths** to extract a "label" for each image (e.g., the digit '0', '1', '2').
4.  **Perform random sampling** to select 5 images for each distinct label.
5.  **Save the sampled data** into a managed Delta Lake table without compression.
6.  **Verify the process** by reading the data back from the Delta table and describing its properties.

---

## 2. How to Run the Script

### Prerequisites

* An environment with Apache Spark installed.
* The Delta Lake library for Spark must be available.
* Access to the data source specified in `my_data_path`.

### Execution

1.  Update the `my_data_path` variable in `Reading_binary.py` to point to the root directory of your MNIST dataset.
2.  Run the script from your terminal using `spark-submit`:

    ```bash
    spark-submit \
      --packages io.delta:delta-spark_2.12:3.2.0 \
      Reading_binary.py
    ```
    *Note: The `--packages` argument ensures that the Delta Lake library is downloaded and included in your Spark application's classpath.*

---

## 3. Detailed Code Explanation

### 3.1. Imports

These lines import the necessary classes and functions from the PySpark and standard Python libraries.

```python
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, split, element_at, rand, row_number
from pyspark.sql.window import Window
```

* `os`: Not actively used in the final script, but often useful for interacting with the operating system.
* `SparkSession`: The main entry point for any Spark functionality.
* `col`, `split`, `element_at`, `rand`, `row_number`: These are built-in Spark functions used for DataFrame transformations.
* `Window`: Used to define a "window" or partition of data for functions like `row_number`.

### 3.2. The `run_mnist_pipeline` Function

This is the core function where all the data processing logic resides.

```python
def run_mnist_pipeline(spark, data_folder, delta_table_name):
```

* **`spark`**: An active `SparkSession` object.
* **`data_folder`**: The string path to the directory containing the image data.
* **`delta_table_name`**: The name for the new Delta table that will be created.

#### Reading Binary Files

```python
all_images_df = (spark.read.format("binaryFile")
                 .option("pathGlobFilter", "*.png")
                 .option("recursiveFileLookup", "true")
                 .load(data_folder))
```

* `spark.read.format("binaryFile")`: This tells Spark to use the specialized data source for reading binary files (like images, PDFs, etc.). Each file is read as a single record.
* `.option("pathGlobFilter", "*.png")`: This is a filter to ensure that only files ending with the `.png` extension are read.
* `.option("recursiveFileLookup", "true")`: This crucial option tells Spark to look for files in all subdirectories of the `data_folder`.
* `.load(data_folder)`: Starts the loading process from the specified path.

The resulting DataFrame `all_images_df` has columns like `path`, `modificationTime`, `length`, and `content`.

#### Caching the DataFrame

```python
all_images_df.cache()
```

* `.cache()`: This is an optimization. It tells Spark to store the `all_images_df` DataFrame in memory after it's first computed. Since we use this DataFrame multiple times (for counting and transformations), caching prevents Spark from having to re-read all the image files from the source, which is a slow operation.

#### Extracting Image Labels

```python
images_with_labels = all_images_df.withColumn(
    "label",
    element_at(split(col("path"), "/"), -2).cast("integer")
)
```

This is a key transformation step.
* `withColumn("label", ...)`: Creates a new column named "label".
* `split(col("path"), "/")`: Takes the `path` column (e.g., `.../mnist_png/training/7/1234.png`) and splits it into an array of strings using `/` as the delimiter. `['...', 'mnist_png', 'training', '7', '1234.png']`.
* `element_at(..., -2)`: Selects the second-to-last element from that array, which is the folder name (`'7'`). This folder name represents the digit and is our label.
* `.cast("integer")`: Converts the label from a string (`'7'`) to a number (`7`).

#### Random Sampling with a Window Function

This is the most complex part of the script. The goal is to pick exactly 5 random images for each label (0 through 9).

```python
window_for_sampling = Window.partitionBy("label").orderBy(rand())
```

* `Window.partitionBy("label")`: This creates partitions or groups. All rows with the same `label` (e.g., all the '7's) are grouped together.
* `.orderBy(rand())`: Within each group, the rows are ordered randomly. `rand()` generates a random number for each row, and ordering by it effectively shuffles the data within each partition.

```python
final_sample_df = (images_with_labels.withColumn("row_num", row_number().over(window_for_sampling))
                   .filter(col("row_num") <= 5)
                   .drop("row_num"))
```

* `.withColumn("row_num", row_number().over(window_for_sampling))`: We add a new column `row_num`. The `row_number()` function assigns a sequential number (1, 2, 3, ...) to each row *within its partition*. Because we ordered by `rand()`, this numbering is applied to the randomly shuffled rows.
* `.filter(col("row_num") <= 5)`: We keep only the rows where the `row_num` is 5 or less. This gives us the top 5 random rows from each label's partition.
* `.drop("row_num")`: The `row_num` column was just a temporary helper, so we remove it to clean up the final DataFrame.

#### Saving to a Delta Table

```python
spark.conf.set("spark.sql.parquet.compression.codec", "uncompressed")

(final_sample_df.write
 .format("delta")
 .mode("overwrite")
 .saveAsTable(delta_table_name))
```

* `spark.conf.set(...)`: This line changes a Spark configuration for this session. We are telling Spark not to use any compression (like `snappy` or `gzip`) when writing the underlying Parquet files for the Delta table.
* `.write.format("delta")`: Specifies that we want to write the data in the Delta Lake format.
* `.mode("overwrite")`: If a table with the same name already exists, it will be completely replaced. Other options are `append`, `ignore`, and `errorifexists`.
* `.saveAsTable(delta_table_name)`: Saves the DataFrame as a **managed table** in the Spark catalog. This means Spark manages both the data and the metadata.

#### Cleanup and Verification

```python
all_images_df.unpersist()
```

* `.unpersist()`: It's good practice to manually remove a DataFrame from the cache when you are done with it to free up memory for other operations.

The final lines of the function simply read the newly created table and show its details to prove that the entire pipeline was successful.

### 3.3. The Main Execution Block

This block of code only runs when the script is executed directly.

```python
if __name__ == "__main__":
```

#### Creating the SparkSession

```python
spark_session = (SparkSession.builder
                 .appName("Celebal_Final_Assignment")
                 .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
                 .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
                 .getOrCreate())
```

* `.builder`: The standard way to start creating a `SparkSession`.
* `.appName(...)`: Gives your Spark application a name, which is useful for identifying it in the Spark UI.
* `.config(...)`: These two configurations are **required** to enable Delta Lake features in your Spark session.
* `.getOrCreate()`: This either gets an existing `SparkSession` or creates a new one if none exists.

#### Setting Paths and Running the Pipeline

```python
my_data_path = "abfss://celebal_dataset@azuredlproject001.dfs.core.windows.net/flat_files/mnist_png/"
my_table_name = "first_mnist_delta_table"
run_mnist_pipeline(spark_session, my_data_path, my_table_name)
```

* This section defines the variables for the input data path and the output table name and then calls the main function to execute the pipeline.

#### Stopping the SparkSession

```python
spark_session.stop()
```

* This releases the resources used by Spark. It's a best practice to explicitly stop the session at the end of your script.
