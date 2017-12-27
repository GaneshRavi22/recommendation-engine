# Modules used by this code are: numpy, scipy, pandas, sklearn
import pandas as pd
import sklearn.preprocessing as pp
import scipy as scipy

# Loading the shopping_cart.csv into a data frame
cart_header = ['USER_ID', 'ITEMS_PURCHASED']
df = pd.read_csv('shopping_cart.csv', sep=',', names=cart_header, skiprows=1, dtype={'USER_ID': str})

# Ungrouping shopping_cart data frame to convert onne row containng multiple items -> multiple rows each containing one item
def ungroup_delim(col, delim=','):
    return col.str.split(delim, expand=True).stack()

df = df.apply(ungroup_delim).ffill()
df = df.reset_index(drop=True)

# Printing some stats like total unique users and unique items loaded
n_users = df.USER_ID.unique().shape[0]
n_items = df.ITEMS_PURCHASED.unique().shape[0]
print 'Number of users = ' + str(n_users) + ' | Number of items = ' + str(n_items)

# Loading the items.csv into a data frame to show item names during final recommendation step
items_header = ['ITEM_ID', 'ITEM_NAME']
item_df = pd.read_csv('items.csv', sep=',', names=items_header, skiprows=1, dtype={'ITEM_ID': str})

# Creating the sparse matrix and setting the non-zero elements of it
train_data_matrix = scipy.sparse.lil_matrix((n_users, n_items))
for line in df.itertuples():
    train_data_matrix[int(line[1])-1, int(line[2])-1] = 1

print 'One-hot coded User-Item matrix: \n', train_data_matrix.todense()

# Defining the function to calculate cosine similarity
def cosine_similarities(mat):
    col_normed_mat = pp.normalize(mat.tocsc(), axis=0)
    print 'Normalized User-Item matrix: \n', col_normed_mat.todense()
    return col_normed_mat * col_normed_mat.T

# Computing the User-USer cosine similarity
user_similarity = cosine_similarities(train_data_matrix)
print 'User-User similarity matrix: \n', user_similarity.todense()

# Adding the item_id as an index, so that we can look up item_name using item_id
item_df_indexed = item_df.set_index("ITEM_ID")

# Defining the function wnich uses the User-User similarity matrix to find items bought by a similar user to the given user
def predictItemsForUser(user_id, top_n):
    lst = []
    highest_sim_score = 0
    most_sim_user = -1
    for a in range(0, n_users):
        if a + 1 != user_id:
            if user_similarity[user_id - 1, a] > highest_sim_score:
                highest_sim_score = user_similarity[user_id - 1, a]
                most_sim_user = a

    top_lst_names = []
    if most_sim_user != -1:
        for a in range(0, n_items):
            if (train_data_matrix[most_sim_user, a] > 0.0 and train_data_matrix[user_id - 1, a] < 1.0):
                lst.append(a + 1)
        top_lst = lst[:top_n]
        print 'Recommendations for user id ', user_id, ' are:'
        for top in top_lst:
            top_lst_names.append(item_df_indexed.loc[str(top), :].ITEM_NAME)
            print '\titem_id: ', top, ' item_name: ', item_df_indexed.loc[str(top), :].ITEM_NAME
    return top_lst_names

# Using the previously defined function to find 3 items bought by the most similar user to user with ID = 4
predictItemsForUser(4, 3)