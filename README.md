# This is Jeopardy!
Author: Jacob L. Miller<br>
Date: October 17, 2023
## Project Description
This project employs Python and the Pandas library to filter and meticulously analyze a dataset encompassing over two decades of data from the Jeopardy game show. The overall purpose of this project is to demonstrate the author's abilities in scripting in Python and utilizing the Pandas library to accomplish various tasks. Tasks such as thoroughly analyzing data within a given dataset, performing various functions on datasets by using Pandas dataframes, and quickly filtering large datasets by using a combination of Pandas functions and string class member functions (split, strip, etc.).
## Features
   - Filtering the jeopardy dataset for questions that contain all of the words in a given list of words.
     - First done by using the Python list object's 'all' member function, which iterates through the words in the given list of words and returns true if all the words are contained in the question and false if they are not.
       - Entries where the words in the list are included but have a certain punctuation applied to them (such as a period, comma, etc.), or are included as a substring of another word (e.g. King vs Viking) are excluded.
     - Then done by using a more complex filter to include the entries where the words in the list are contained in the question, even when they have certain punctuation applied to them.
       - This more complex filter generates a dictionary of 'word variations' (each variation consisting of the word with a different punctuation applied to it) to account for every possible punctuation mark.
         - Each key in this dictionary represents a word in the given list of words, while each value represents the list of word variations for that particular word.
       - Once this dictionary is generated, it uses a combination of the more simple filter as well as a for loop to loop through each word variation and check if any of those are contained within the entries' question.
         - This is done to reduce the amount of entries the for loop needs to loop through, and therefore significantly decrease the for loops' runtime.
   - Basic data analysis conducted on the jeopardy dataset
     - Using the Python Pandas library's various member functions, such as mean and count.