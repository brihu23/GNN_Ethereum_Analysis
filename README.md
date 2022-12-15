# Readme

# Installation

1. To get started create a virtual environment and install dependencies

```bash
python3 -m venv env
#activating virtual env
source env/bin/activate
pip3 install -r requirements.txt
```

1. Download the pkl file from [https://www.kaggle.com/datasets/xblock/ethereum-phishing-transaction-network?resource=download](https://www.kaggle.com/datasets/xblock/ethereum-phishing-transaction-network?resource=download) into your filesystem and set ****************************maingraph_path**************************** to the file location

# Creating a subgraph

1. To create your own subgraph
    1. Set the **is_subgraph** variable to FALSE at the top of the file
    2. Set the ****************************subgraph_save_path**************************** to your desired path output
    3. Set the **nodes** variable to the desired number of randomly sampled fraud and normal nodes to sample from the main graph
    4. Run the below snippet
    
    ```bash
    python3.10 main.py
    ```
    
2. To amplify your subgraph with usd_values
    1. Set the ****************************subgraph_path**************************** to the path output of the ****************************subgraph_save_path**************************** from the previous step
    2. Set the **is_subgraph** variable to TRUE at the top of the file
    3. Run the below snippet (this will take around 5-6 hours) and you will need to set your own transpose api key in *get_tx_hash_v2.py*
    
    ```bash
    python3.10 main.py
    ```
    

# Loading our subgraph

1. Download the subgraph here —> [https://drive.google.com/file/d/1wGclh1IlXdQ8_6Zz3bp6RurOkuxPj6c_/view?usp=sharing](https://drive.google.com/file/d/1wGclh1IlXdQ8_6Zz3bp6RurOkuxPj6c_/view?usp=sharing)
    1. This subgraph was created from 200 fraudulent and 200 normal nodes and amplified with usd_values
2. Set the ****************************subgraph_path**************************** to the file location of the unzipped pkl file from above
3. Set the **is_subgraph** variable to TRUE at the top of the file
4. Set the ******************************preload_path****************************** to the file above
5. Run the below snippet

```bash
python3.10 main.py
```

# Running RGCN Model on Subgraph