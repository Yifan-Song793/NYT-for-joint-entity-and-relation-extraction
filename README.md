# NYT-for-joint-entity-and-relation-extraction
A script to preprocess NYT dataset for joint entity and relation extraction.

The lack of reproducibility is an issue in science, particularly in machine learning. Recently, I am interested in joint entity and relation extraction and I have read nearly all the papers in the last 5 years about this topic. However, what confused me is that most of the models cannot be reproduced. The main reason is that they don't provide the full version of their datasets. In detail, while nearly all the models claim that they can address the multi-token entities problem, the datasets they released only have the annotation of the entity tail.

For nobody provides data preprocessing script for their joint entity and relation extraction models, I wrote this script.

The origin NYT dataset for JERE I used is from [CopyRE](https://github.com/xiangrongzeng/copy_re). I aligned it to the raw NYT distant supervised learning dataset released by [USC-DS-RelationExtraction](https://github.com/INK-USC/USC-DS-RelationExtraction). Note that all the sentences in the origin dataset can be found in the raw NYT dataset. Therefore, no third-party annotation tool is needed.

## How to Use

1. **Download the datasets**
    Download the origin NYT dataset from [here](https://drive.google.com/file/d/10f24s9gM7NdyO3z5OqQxJgYud4NnCJg3/view) and decompress it under `nyt/`
    Download the raw NYT distant supervised learning dataset from [here](https://drive.google.com/drive/folders/0B--ZKWD8ahE4UktManVsY1REOUk?usp=sharing) and decompress it under `nyt/`

2. **Run the script**

    ```python
    python data_align.py
    ```

    The aligned data with full annotation will be under `nyt/`

    ```json
    {"sent": ["Massachusetts", "ASTON", "MAGNA", "Great", "Barrington", ";", "also", "at", "Bard", "College", ",", "Annandale-on-Hudson", ",", "N.Y.", ",", "July", "1-Aug", "."], "rels": [{"e1s": 11, "e1e": 11, "e2s": 8, "e2e": 9, "r": 22}]}
    ```

    e1s: entity 1 start position
    e1e: entity 1 end position
    e2s: entity 2 start position
    e2e: entity 2 end position
    r: relationship between entity 1 and entity 2



## Statistics

| Train | 56195 |
| ----- | ----- |
| Valid | 4999  |
| Test  | 5000  |



We call for a unified evaluation settings to prevent mistakes. At least, we must use the same dataset. Hope my script helps.