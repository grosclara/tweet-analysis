# Test reading json
# Test remove empty words
# Test remove duplicates

def get_candidate_queries(num_candidate, file_path, keyword_type):
    """
    Generate and return a list of string queries for the search Twitter API from the file file_path_num_candidate.txt
    :param num_candidate: the number of the candidate
    :param file_path: the path to the keyword and hashtag 
    files
    :param type: type of the keyword, either "keywords" or "hashtags"
    :return: (list) a list of string queries that can be done to the search API independently
    """

    # Validation of parameters
    assert keyword_type == 'hashtags' or keyword_type == 'keywords', "Invalid keyword_type parameter: either 'hashtags' or 'keywords'"
    assert type(num_candidate) == int, "num_candidate should be a int"

    # Open txt file
    try:
        with open("{0}{1}_candidate_{2}.txt".format(file_path, keyword_type, num_candidate),'r',encoding = 'utf-8') as f:
            keywords = f.read().split(',')
            return clean_query(keywords)
    except IOError:
            print("Not able to read the following file: {0}{1}_candidate_{2}.txt".format(file_path, keyword_type, num_candidate))


def clean_query(keywords):
    """
    Return a list of keywords without any duplicates nor empty words.
    :param keywords: the list of keywords to clean
    :return: (list) a list of keywords
    """
    # Remove duplicate
    keywords = list(set(keywords)) 
    # Remove empty keywords
    keywords = [w.strip() for w in keywords if w.strip()]
    return keywords

