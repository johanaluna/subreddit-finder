import pymongo
from decouple import config
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd



def transform_get(text, loadcv, loaddf):
    """Function written by Matthew/Johana"""
    transform = loadcv.transform([text])
    inputdata = transform.todense()
    dist_matrix = cosine_similarity(loaddf, inputdata)
    results = pd.DataFrame(dist_matrix)

    return results[0].sort_values(ascending=False)[:3].index.tolist()

def get_subreddit_info(array):
    """
    Function written by Matthew/Johana that gets
    subreddit information based on ID numbers
    """
    print(array)
    client = pymongo.MongoClient(config('SECRET_CODE'))
    db = client.sfw_db.sfw_table
    data = [db.find_one({'sub_id': int(num)}) for num in array]
    return(data)

def jsonConversion(json_obj):
    """Return: string combination of title and text."""
    title = json_obj["title"]
    text = json_obj["text"]
    # if json_obj["link"] is False:
    #     string = " ".join([title, text])
    # else:
    string = " ".join([title, text])
    return string

def list_subreddits(prediction):
    """Uses the previous function to get the information the FE needs"""
    subreddits = get_subreddit_info(prediction)
    output = []
    for subreddit in subreddits:
        sub_dict = {}
        sub_dict['name'] = subreddit['name']
        sub_dict['url'] = 'https://www.reddit.com' + subreddit['url']
        sub_dict['subscribers'] = subreddit['subscribers']
        sub_dict['active_accounts'] = subreddit['active_accounts']
        sub_dict['score'] = subreddit['score']
        if type(subreddit['description']) is float:
            sub_dict['description'] = 'None'
        else:
            sub_dict['description'] = subreddit['description']
        output.append(sub_dict)
    return output