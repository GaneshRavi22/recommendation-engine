# Recommendation Engine

This project contains code supporting the blog at url => https://humansandai.wordpress.com/2017/12/26/recommendation-engine-overview-for-dummies/

## Source files
* item_item_sim_recommender.py => This stand-alone python file contains the code to a recoomendation engine
built using the Item-Item similarity technique
* user_user_sim_recommender.py => This stand-alone python file contains the code to a recoomendation engine
built using the User-User similarity technique

## Resource files
* items.csv => This is a training data file which contains the unique item_id and the item_name of all
items in the inventory.
* shopping_cart.csv => This is a training data file which contains the user_id and the list of items
purchased by that user in a single transaction.

## Running the example
### Running from PyCharm
* Import the cloned project into PyCharm. PyCharm will automatically install the required dependencies
from the _requirements.txt_ file
* Right and click on 'Run' option on the _item_item_sim_recommender.py_ file from the project window.

### Running from the Terminal
* Python 2.x and pip should already be installed on the machine.
* Install the requirements from the _requirements.txt_ file, suing the command
```
pip install -r requirements.txt
```
You might have to use sudo, if the user does not have enough permissions to install packages.
* Execute the python file using the command
```
python item_item_sim_recommender.py
```