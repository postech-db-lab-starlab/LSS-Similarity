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

   Set up all the parameters in ```xgb_params.json``` file or ```neural_params.json``` file.

   You can train the model and test the code by running the code below:
   ```
   python nl_sql_dist.py --parameters xgb_params.json
   ```

   With provided sample features, you would get results as follows:
   ```
   Accuracy: 92.78%
   True Positive: 42
   False Positive: 4
   False Negative: 3
   True Negative: 48
   -----------------------------
   Precision: 0.91
   Recall: 0.93
   =============================
   ```

   To train the neural network model, use the following code:
   ```
   python nl_sql_dist.py --parameters neural_params.json
   ```

   With proided sample features, you would get results as follows:
   ```
   Accuracy: 94.85%
   True Positive: 43
   False Positive: 3
   False Negative: 2
   True Negative: 49
   -----------------------------
   Precision: 0.93
   Recall: 0.96
   =============================
   ```

### Test

   Firstly, you should update the ```xgb_params.json``` file or ```neural_params.json``` to direct pretrained model file.

   You can load the existing model by running the following code:
   ```
   python nl_sql_dist.py --parameters xgb_params.json
   ```
   We provide the pre-trained model for test, named ```XGB_TEST1.dat```.

   If you use the pre-trained model, the program will use all the data in ```feature_answer_all.txt``` as test data.
