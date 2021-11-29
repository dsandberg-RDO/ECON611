import pandas as pd
import numpy as np
import pandas_datareader.data as web
import datetime
import json
import pandas_datareader as web

def total(list_obj):
    total = 0
    n = len(list_obj)
    for i in range(n):
        total += list_obj[i]
    return total

def mean(list_obj, rounding_digit = 1):
    n = len(list_obj)
    mean_ = round(total(list_obj) / n, rounding_digit)
    return mean_

def median(list_obj):
    n = len(list_obj)
    list_obj = sorted(list_obj)
    #lists of even length divided by 2 have reminder 0
    if n % 2 != 0:
        #list length is odd
        middle_index = int((n - 1) / 2)
        median_ = list_obj[middle_index]
    else:
        upper_middle_index = int(n / 2)
        lower_middle_index = upper_middle_index - 1
        # pass slice with two middle values to mean()
        median_ = mean(list_obj[lower_middle_index : upper_middle_index + 1])
        
    return median_

def mode(list_obj):
    # use to record value(s) that appear most times
    max_count = 0
    # use to count occurrences of each value in list
    counter_dict = {}
    for value in list_obj:
        # count for each value should start at 0
        counter_dict[value] = 0
    for value in list_obj:
        # add on to the count of the value for each occurrence in list_obj
        counter_dict[value] += 1
    # make a list of the value (not keys) from the dictionary
    count_list = list(counter_dict.values())
    # and find the max value
    max_count = max(count_list)
    # use a generator to make a list of the values (keys) whose number of 
    # occurences in the list match max_count
    mode_ = [key for key in counter_dict if counter_dict[key] == max_count]
    
    return mode_

def variance(list_obj, rounding_digit = 1, sample = False):
    # popvar(list) = sum((xi - list_mean)**2) / n for all xi in list
    # save mean value of list
    list_mean = mean(list_obj)
    # use n to calculate average of sum squared diffs
    n = len(list_obj)
    # create value we can add squared diffs to
    sum_sq_diff = 0
    for val in list_obj:
        # adds each squared diff to sum_sq_diff
        sum_sq_diff += (val - list_mean) ** 2
    if sample == False:
        # normalize result by dividing by n
        variance_ = round(sum_sq_diff / n, rounding_digit)
    else:
        # for samples, normalize by dividing by (n-1)
        variance_ = round(sum_sq_diff / (n - 1), rounding_digit)
    
    return variance_

def SD(list_obj, rounding_digit = 1, sample = False):
    # Standard deviation is the square root of variance
    SD_ = variance(list_obj, rounding_digit, sample) ** (1/2)
    
    return round(SD_, rounding_digit)

def covariance(list_obj1, list_obj2, rounding_digit = 3, sample = False):
    # determine the mean of each list
    mean1 = mean(list_obj1)
    mean2 = mean(list_obj2)
    # instantiate a variable holding the value of 0; this will be used to 
    # sum the values generated in the for loop below
    cov = 0
    n1 = len(list_obj1)
    n2 = len(list_obj2)
    # check list lengths are equal
    if n1 == n2:
        n = n1
        # sum the product of the differences
        for i in range(n1):
            cov += (list_obj1[i] - mean1) * (list_obj2[i] - mean2)
        if sample == False:
            cov = cov / n
        # account for sample by dividing by one less than number of elements in list
        else:
            cov = cov / (n - 1)
        # return covariance
        return round(cov,rounding_digit)
    else:
        print("List lengths are not equal")
        print("List1:", n1)
        print("List2:", n2)
    

def correlation(list_obj1, list_obj2):
    # corr(x,y) = cov(x, y) / (SD(x) * SD(y))
    cov = covariance(list_obj1, list_obj2)
    SD1 = SD(list_obj1)
    SD2 = SD(list_obj2)
    corr = cov / (SD1 * SD2)
    return corr

def skewness(list_obj, rounding_digit = 1, sample = False):
    mean_ = mean(list_obj)
    SD_ = SD(list_obj, sample)
    skew = 0
    n = len(list_obj)
    for val in list_obj:
        skew += (val - mean_) ** 3
    if n == 0 or SD_ == 0:
        skew == 0
    else:
        skew = skew / (n * SD_ **3) if not sample else n * skew / ((n - 1)*(n - 2) * SD_ ** 3)
    skew = round(skew,rounding_digit)   
    return skew

def kurtosis(list_obj, rounding_digit = 1, sample = False):
    mean_ = mean(list_obj)
    kurt = 0
    SD_ = SD(list_obj, sample)
    n = len(list_obj)
    for val in list_obj:
        kurt += (val - mean_) ** 4
    if n == 0 or SD_ == 0:
        kurt == 0
    else:
        kurt = kurt / (n * SD_ ** 4) if sample == False else  n * (n + 1) * kurt / \
        ( (n - 1) * (n - 2) *(n - 3) * (SD_ ** 4)) - (3 *(n - 1) ** 2) / ((n - 2) * (n - 3))
    kurt = round(kurt,rounding_digit)
    return kurt

def drew_rando(mu, sigma, length =10, rounding_digit=1):
    samples = np.random.normal(mu, sigma, length).tolist()
    for i in range(len(samples)):
        samples[i] = round(samples[i],rounding_digit)
    
    return samples

def gather_statistics(df, sample = False):
    dct = {key:{} for key in df}
    for key, val in df.items():
        # drop any missing observations from dataframe
        val = val.dropna(axis=0)
        dct[key]["Mean"]     = mean(val,3)
        dct[key]["Median"]   = round(median(val),3)
        dct[key]["Variance"] = variance(val, 3, sample)
        dct[key]["SD"]       = SD(val, 2, sample) 
        dct[key]["Skewness"] = skewness(val, 2, sample)
        dct[key]["Kurtosis"] = kurtosis(val, 2, sample)
    stats_df = pd.DataFrame(dct)
    return stats_df

def yahoo_stock_pull(year, dict_, filename):
    start = datetime.datetime(year, 1, 1)
    end = datetime.datetime.today()
    keys = dict_.keys()
    new_dict={}
    for key in keys:
        new_dict[key] = web.DataReader(key, 'yahoo', start, end)
    df = pd.concat([df['Close'] for df in new_dict.values()], axis=1, keys=new_dict.keys())
    df.to_csv(filename)
    return

def fed_data_pull(year, dict_, filename):
    start = datetime.datetime(year, 1, 1)
    end = datetime.datetime.today()
    keys = dict_.keys()
    df = web.DataReader(keys,'fred', start, end)
    df.columns = df.columns.map(dict_)
    df.to_csv(filename)
    return