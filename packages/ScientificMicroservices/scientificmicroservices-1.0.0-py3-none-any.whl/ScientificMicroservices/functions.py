__all__ = ["ABSynthesis", "MissingRowsCols", "MissingBias", "DetectOutliers"]


def ABSynthesis(key, data_dict):
    '''
    Run a meta-analysis on a set of experiments to determine the summary uplift and p-value.
    Takes a list of dicts containing at least four keys:
        successes_base: The number of events of interest (e.g. clicks) in the base condition, 1 element for each experiment.
        trials_base: The full number of people (e.g. visitors) who saw the base condition.
        successes_variant: The number of events of interest (e.g. clicks) in the variant condition, 1 element for each experiment.
        trials_variant: The full number of people (e.g. visitors) who saw the variant condition.
    '''
    Headers = {'x-rapidapi-host':'absynthesis.p.rapidapi.com', 'x-rapidapi-key':key, 'content_type':"application/json" }
    Body  = json.dumps(data_dict)
    return requests.post(url = "https://absynthesis.p.rapidapi.com/ABSynthesis", data = Body, headers=Headers).json()

def MissingRowsCols(key, data_dict):
    '''
    Return a report of the missing values in a dataset
    Takes a list of dicts or a pandas table.
    '''
    Headers = {'x-rapidapi-host':'missingrowscols.p.rapidapi.com', 'x-rapidapi-key':key, 'content_type':"application/json" }
    Body  = json.dumps(data_dict)
    return requests.post(url = "https://missingrowscols.p.rapidapi.com/MissingRowsCols", data = Body, headers=Headers).json()

def MissingBias(key, array_pair_dict):
    '''
    Determine whether missing data in one column of a table is more likely depending on a second column.
    Takes a two column pandas table, or a list of dicts containing two key-value pairs each.
    '''
    Headers = {'x-rapidapi-host':'missingbias.p.rapidapi.com', 'x-rapidapi-key':key, 'content_type':"application/json" }
    Body  = json.dumps(array_pair_dict)
    return requests.post(url = "https://missingbias.p.rapidapi.com/MissingBias", data = Body, headers=Headers).json()

def DetectOutliers(key, array_dict):
    '''
    Detect unusual values in a list based on three common statistical tests.
    Takes a list of values that can be strings or numbers.
    '''
    Headers = {'x-rapidapi-host':'detectoutliers.p.rapidapi.com', 'x-rapidapi-key':key, 'content_type':"application/json" }
    Body  = json.dumps(array_dict)
    return requests.post(url = "https://detectoutliers.p.rapidapi.com/DetectOutliers", data = Body, headers=Headers).json()
