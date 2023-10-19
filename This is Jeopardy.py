'''
    AUTHOR: Jacob L. Miller
    DATE: Saturday, October 14, 2023
    PROJECT: This is Jeopardy (Data Filtering and Analysis)
'''

import pandas as pd
pd.set_option('display.max_colwidth', None)
jeopardy = pd.read_csv('jeopardy.csv')
for col in jeopardy.columns:
    jeopardy = jeopardy.rename(columns={col:col.strip()})

'''
  Name:         contains_filter_toStr
  Type:         void
  Description:  Prints the result of the contains_filter function
  Parameters:   words  => list of words the dataset is filtered by
                          in the contains_filter function
                numStr => Number of questions in the jeopardy dataset
                          that contain the words in the 'words' list
                data   => Dataset that is filtered by the 'words' list
                          in the contains_filter function
  Returns:      None
'''
def contains_filter_toStr(words, numStr, data):
    str_o = ''
    for i in range(len(words)):
        if (i == len(words) - 2):
            str_o += '\'{}\' and '.format(words[i])
        elif (i == len(words) - 1):
            str_o += '\'{}\''.format(words[i])
        else:
            str_o += '\'{}\', '.format(words[i])
    print('Number of Questions that contain the word(s) {}: {}\n'.format(str_o, numStr))
    print('Examples: \n--------\n')
    for index, row in data.head().iterrows():
        print('\t{}\n'.format(row['Question']))
    print('\n')

'''
  Name:         contains_filter
  Type:         Pandas Dataframe
  Description:  Searches through the jeopardy dataset's 
                'Questions' column and returns the entries
                in the dataset where the Question contains
                the words in the given 'words' list.
  Parameters:   data  => dataset in which to filter by the
                         given 'words' list
                words => list of words to filter the given
                         dataset by
  Returns:      Returns the rows in the jeopardy dataset 
                where the question in the 'Questions' column
                contain the words in the given 'words' list.
'''
def contains_filter(data, words):
    filter = lambda x: all(word.lower() in x.lower() for word in words)
    filtered_data = data[data.Question.apply(filter)]
    contains_filter_toStr(words, filtered_data.shape[0], filtered_data)
    return filtered_data

words = ['King', 'England']
filtered_data = contains_filter(jeopardy, words)



'''
  Name:         consists
  Type:         bool
  Description:  Used to determine if the phrase consists of
                  the target word(s)
  Parameters:   phrase => string to check for target word(s)
                target => list of target words
  Returns:      returns TRUE if phrase contains target word(s)
                  or FALSE if phrase does not contain the 
                  target word(s)
'''
def consists(phrase, target):
    consists_of = True
    phrase = ' {} '.format(phrase)
    for word in target:
        if (not any(phrase.lower().__contains__(variation.lower())
                    for variation in target[word])):
            consists_of = False
    return consists_of

'''
  Name:         gen_variation
  Type:         string
  Description:  Used to apply specific grammar (or punctuation) 
                to a word or input. Thereby generating a 'variation' 
                of that word or input.
  Parameters:   word    => word or input to apply grammar to and 
                           generate variation of.
                grammar => specific grammar (or punctuation) to apply 
                           to word or input
  Returns:      Returns 'variation' of word or input with a specific
                grammar (or punctuation) applied to it.
'''
def gen_variation(word, grammar):
    if (len(grammar) == 2):
        if (grammar[1] == ' '):
            return grammar[0] + word
        else:
            return grammar[0] + word + grammar[1]
    elif (len(grammar) == 1):
        return word + grammar
    else:
        return word

'''
  Name:        gen_allVariations
  Type:        Dictionary
  Description: Used to generate all the variations of a list of words 
               or inputs by applying all possible combinations of grammar
               (or punctuation) to each word or input in the list.
  Parameters:  words => list of words to generate all variations of
  Returns:     Returns a dictionary, where the keys represent the 
               words we would like to generate all variations of 
               and the values are all the possible variations of
               its respective word or input key.
'''
def gen_allVariations(words):
    word_dict = {}
    grammar_dict = { # grammar dictionary used to represent 
                     # all the possible punctuation marks
         0: '',      1: '\' ',    2: '\'',
         3: '"',     4: '" ',     5: ',',      
         6: '.',     7: '!',      8: '?',      
         9: '""',   10: "''",    11: '( ',    
        12: ')',    13: '()',    14: 's'
    }
    for word in words: # for loop to iterate through all the words in the
                       # 'words' list
        word_dict[word] = [' {} '.format(word)]
        for key1 in grammar_dict: # nested for loop to iterate through all the
                                  # possible punctuation marks and generate all
                                  # the possible variations for each word or 
                                  # input
            for key2 in grammar_dict:
                if ((grammar_dict[key1] == '') and (grammar_dict[key2] == '')):
                    continue
                elif ((grammar_dict[key1] == 's') and (grammar_dict[key2] == 's')):
                    continue
                else:   
                    newWord = gen_variation(word, grammar_dict[key1])
                    newWord = gen_variation(newWord, grammar_dict[key2])
                    word_dict[word].append(' {} '.format(newWord))
    return word_dict

'''
  Name:         contains_filter_improved
  Type:         Pandas DataFrame
  Description:  Modified version of the contains_filter function
                which finds all the questions that contain all the
                words, or any variation of them, in the given
                'words' list. Each variation applies a different
                punctuation to it's respective word or input.
                Filtered data does not include entries where the
                words in the 'words' list are only featured as
                substrings of other words (e.g. King vs Viking).
  Parameters:   data  => dataframe to search through
                words => list of words for which to filter the
                         data by
  Returns:      Returns filtered dataframe, where each value in
                the 'Question' column contains all the words,
                or any variation of them, in the given 'words'
                list.
'''
def contains_filter_improved(data, words):
    words_dict = gen_allVariations(words)
    filter = lambda x: all(word.lower() in x.lower() for word in words) # Runs a pre-filter on the data to
                                                                # shorten the runtime of the more complex
                                                                # 'consists' filter by shortening the amount
                                                                # of entries the 'consists' filter has to
                                                                # scan through while including all the 
                                                                # variations of the given words in the
                                                                # 'words' list.
    filtered_data = data[data.Question.apply(filter)]
    filtered_data = filtered_data[filtered_data.Question.apply(lambda x: consists(x, words_dict))]
    contains_filter_toStr(words, filtered_data.shape[0], filtered_data)
    return filtered_data

filtered_data = contains_filter_improved(jeopardy, words)
words = ['Norse', 'God']
filtered_data = contains_filter_improved(jeopardy, words)



'''
  Name:         toFloat
  Type:         float
  Description:  Used to convert the datatype of the
                'Values' column in the jeopardy dataframe
                from string to float
  Parameters:   val => value in 'Values' column to convert to
                       datatype 'float'
  Returns:      value converted to datatype 'float'
'''
def toFloat(val):
    newVal = val
    if (not isinstance(val, float)):
        if (isinstance(val, str)):
            newVal = newVal.strip('$').replace(',', '')
            newVal = float(newVal)
        else:
            newVal = float(newVal)
    return newVal

jeopardy.Value = jeopardy.Value.apply(lambda x: toFloat(x))
king_avg = round(contains_filter_improved(jeopardy, ['King']).Value.mean()*100)/100
print('Average value for questions containing the word \'King\': {}'.format(king_avg))



'''
  Name:         unique_count
  Type:         Pandas Series
  Description:  Sorts the given dataset by its 'answer' column and
                returns the number of questions each unique answer
                applies to.
  Parameters:   dataset       => dataset to sort
                questions_col => name of the dataset's 'questions' column
                answers_col   => name of the dataset's 'answers' column
  Returns:      Returns a Series object that represents the unique answers
                in the given dataset's 'answers' column and the number of 
                questions each answer applies to.
'''
def unique_count(dataset, questions_col, answers_col):
    count = dataset.groupby(answers_col)[questions_col].count()
    return count

king_data = contains_filter(jeopardy, ['King'])
king_count = unique_count(king_data, 'Question', 'Answer')['Henry VIII']
print('Number of questions where \'Henry VIII\' was the answer: {}'.format(king_count))