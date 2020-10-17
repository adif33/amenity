# Code Project For Amenity
## How does it work
To accomplish fast search, first we need to preprocess the data. For each word found in an article we will create a file containing all the articles that contains that word.
When a search is performed, for each keyword we will read the appropriate file containing the articles names into a set, then depending on the operator we will intersect or union the sets and return the resulting articles.
To do the preprocessing in fast and scalable manner, Docker is used to do the different services needed for such operation:
An Assigner that insert each article into a Redis queue
Readers that accept articles from the queue to process. For each word in the article the article name is inserted into a queue that represents the word
Writers that takes the articles names from each word’s queue and adds them to right file according to the word
That method is used to handle the large size of the data and to enable the scaling of Readers and Writers.

## How to run it
Docker and Redis are required.

There is a test script:
>/test/main_test.py

It will make the setup and preprocessing on some sample articles and then run some different test scenarios queries, as described in /test/expected_results.py.

For normal use: 
>/setup.py

It will make all the installations and run the server and the preprocessors in the background (it’s possible for the Assigner to add files while running)
