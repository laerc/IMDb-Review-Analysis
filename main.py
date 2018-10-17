# How to get an API key? http://www.omdbapi.com/apikey.aspx
# Get reviews from an API? https://developers.themoviedb.org/3/reviews/get-review-details
# Dataset : http://ai.stanford.edu/%7Eamaas/data/sentiment/
# To start, just download the dataset, and extract the file in the same folder of the main.py

import nltk

from review import Review
from parser import Parser
from analyser import Analyser
from classifier import Classifier

def start():
	nltk.download('punkt')
	nltk.download('wordnet')
	nltk.download('stopwords')
	nltk.download('sentiwordnet')
	nltk.download('lin_thesaurus')
	nltk.download('vader_lexicon')
	nltk.download('averaged_perceptron_tagger')
	nltk.download('tagsets')
'''
analyser = Analyser()
analyser.get_score_from_file()

start()
'''
parser = Parser('train')

filenames = parser.get_files_name()
x_train_dataset, y_train_dataset, reviews, input_size = parser.get_data_from_file()

classifier = Classifier(x_train_dataset, y_train_dataset)
#classifier.LogisticTrain()
word1 = 'Seeing a review comparing this brilliant title to Lord of the Rings made me make an account here and post my very first review. I had very high expectations from this series and I believed that it will (like most TV series) absolutely ruin the book. And I couldnt have been more wrong! Where do I start... The cast is great, though not amazing with one exception - Sean Bean is perfect for the role of cold master of the North, Eddard Stark. The setting, the atmosphere is perfect and not boring at all! Some scenes are just amazing and are exactly as written in the book - for example the scene where they find the wolves, the nature and the dialogs are just as they should be. Now to get to the part most people are interested in: What is this? What can I expect of the series? THIS IS NOT LORD OF THE RINGS. Now that I got that out, I can continue. The very idea behind the series is a lot different. Its based around great families on different sides of the world, the stories their members have to tell and the secrets they hide. And there are many secrets, You will have a chance to witness small portion of them in the first episode. If you cannot follow the story just yet, dont worry! Its meant to be like that, you will eventually get to know all the characters and get involved in the story so much you will BEG for next episode just to see what happens. What to expect? Plots, love, action, war, hatred, quite a few surprises and much much more... All that after the first episode. I really hope they will not ruin it as the series progress. Conclusion: Do not miss this! Yes YOU complaining that the book is better. And everyone else.'
word2 = 'Had a test screening tonight in cinema I work at, and couldnt wait to watch my all-time favorite Marvel (anti) hero on big screen. Tom Hardy is great as always, that guy really can act. Cant think of anyone else who would be a better choice for the role but him. Introduction was really long, but I was not bored for a second. When Venom comes in his true form - the party starts! Wish few action scenes were less like Michael Bays style (hardly see anything) but the inner child in me was really happy for Venoms maniacal kicking and punching around. Venoms character is really well made visually - his walking, jumping and smashing are just like in the comic books - thumbs up for that! Hope they will release R rated version on BluRay so we can see more of Venoms craziness. Tom Hardy allegedly said best parts are cut out to make the movie more age appropriate, and I think thats a shame. Anyway, I will watch this movie once more in cinema, and buy it on BluRay. After all, its Venom!Go and see it on big screen - hope you wont be disappointed!Oh, and there are TWO mid-credit scenes - one we all are waiting for and another one that...just go and see it for yourself!'
word3 = 'good movie good movie very good film excelent production great film amazing film awesome film good great movie'
word4 = 'bad movie did not liked the movie very bad not good could be better bad production horrible director'
#classifier.LogisticTest([word1, word2, word3, word4], parser)

classifier.buildNeuralNetwork(input_size, 3, [word1, word2, word3, word4], parser)


