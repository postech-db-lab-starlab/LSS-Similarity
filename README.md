# LSS-Similarity

## Dataset Preparation

### Prepare SQL/NL Data

   Use the [Web-Crawler-for-NL2SQL](https://github.com/postech-db-lab-starlab/Web-Crawler-for-NL2SQL) to extract the web-crawled SQL and natural language data. The data will be saved to the PostgreSQL dataset

### Prepare SQL/NL Alignments

   We use [english word aligner](https://github.com/FerreroJeremy/monolingual-word-aligner) to align words in SQL and NL and extract features from the alignments.
   
   To align words in SQL and NL, first change directory to ```monolingual-word-aligner```
   ```
   cd monolingual-word-aligner
   ```

   Then, run the following codes.
   ```
   python run_all_mining.py
   python3 InputWords.py
   python run_all_align.py
   ```

   Following codes align words in SQL and NL, and save the alignment information into the database ```alignments.dls_cu```.

### Prepare Answers

   In order to train the XGBoost Model, manually marked answers are needed. The answers should be stored in PostgreSQL database as follows.
   ```
   Schema: "answers"
   Table: "sql_0_0_nl_0"
   Headers: ["sql_id", "nl_id"]
   ```
   Each row in answers.sql_0_0_nl_0 table stores answer as pair of ids ("sql_id", "nl_id").

### Word Embedding

   You can download the word embedding by following codes
   ```
   wget http://clic.cimec.unitn.it/composes/materials/EN-wform.w.5.cbow.neg10.400.subsmpl.txt.gz
   gunzip EN-wform.w.5.cbow.neg10.400.subsmpl.txt.gz
   ```

## Extract Features
   
   You can extract features from SQL, NL pair by running the following code.
   ```
   python feature_extract.py
   ```
   Features are stored in file ```features.txt``` in form ```(<sql_id> <nl_id> <feat0> <feat1> <feat2>)```

   Run the following code to re-format the file for XGBoost Model.
   ```
   python modify_feature.py
   ```

   All features and answers for each feature are stored in file ```feature_answer_all.txt``` in form ```(<sql_id> <nl_id> <feat0> <feat1> <feat2> <answer>)``` where ```<answer>``` is 1 or 0

## Run XGBoost Model

### Train

   You can train the model and test the code by running the code below
   ```
   python nl_sql_dist.py --model xgb
   ```

### Test

   You can load the existing model by running the following code
   ```
   python xgb_dist.py <PATH_TO_SAVED_MODEL>
   ```
   We provide the pre-trained model for test, named ```XGB_TEST1.dat```.

   If you use the pre-trained model, the program will use all the data in ```feature_answer_all.txt``` as test data.
