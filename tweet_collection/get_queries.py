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
    assert num_candidate > 0, "num_candidate should be positive"

    try :
        # Open txt file
        with open("{0}{1}_candidate_{2}.txt".format(file_path, keyword_type, num_candidate),'r',encoding = 'utf-8') as f:
            # Retrieve words
            keywords = f.read().split(',')
            # Remove empty keywords
            keywords = [w.strip() for w in keywords if w.strip()]
            # Remove duplicate and sort list
            keywords = sorted(set(keywords), key=str.lower)
            return keywords
    
    except IOError as err:
        raise err