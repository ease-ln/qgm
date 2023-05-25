# Metrics Recommender
This is the system to recommend metrics based on the GQM model

### To run this code:

1. Set up the virtual environment (instructions for Linux)
    ```bash
    #/path
    python3 -m venv venv
    source venv/bin/activate
    ```
2. Clone this repository at */path/venv*
3. Start the backend part
    ```bash
    # /path/venv/MetricsRecommender
    python -m pip install -U pip      
    pip install -r requirements.txt
    python3 manage.py runserver
    ```
4. Start the frontend part
   ```bash
    # /path/venv/MetricsRecommender/gqm_interface
    npm install
    npm start
   ```
5. Turn off the virtual environment
    ```bash
    # /path
    deactivate
   ``` 
   
### How to use
1) Login into the system. If you do not have an account - register.
2) Enter your progect goal
3) Click on the goal and enter questions
4) Click on question and choose an action: generate automatically, use the pre-cooked set or choose appropriate metrics by yourself

### Admin account

login: admin

password: admin

- You can find the dataset on MetricsRecommender/gqm_api/questions.csv
- Run the statistics collection on the dataset you can by running MetricsRecommender/gqm_api/statistics_collection.py
