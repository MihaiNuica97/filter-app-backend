from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import nltk
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
import time
from django.shortcuts import render

nltk.data.path.append("/home/nltk_data")
tweet_tokenizer = TweetTokenizer()
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))


def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

def hello(request):
    print("Handling request to home page.")
    return HttpResponse("Hello, Azure!")


@csrf_exempt
def filter_this(request):
    t0 = time.time()
    if request.method == 'POST':
        json_data = json.loads(request.body)
        json_data['match'] = False
        tokens = tweet_tokenizer.tokenize(json_data['content'])
        print(json_data['content'])
        filtered_tokens = [w for w in tokens if not w in stop_words]
        tags = nltk.pos_tag(filtered_tokens)
        pruned_sentence = []
        # print("Pruning sentence: ", tags)
        for i in tags:
            try:
                pruned_sentence.append(lemmatizer.lemmatize(i[0], get_wordnet_pos(i[1])))
            except:
                print(i, "Could not be pruned!")
                print()
        heuristic = 0.3
        lemmas = ['dog.n.01', 'cat.n.01', 'play.n.01', 'animal.n.01', 'play.v.01', 'game.n.01',"jewel.n.01","sport.n.01","food.n.01"]
        filters = [wordnet.synset(w) for w in lemmas]
        for f in filters:
            for word in pruned_sentence:
                # print("Similarity for word: ", word)
                try:
                    synonyms = wordnet.synsets(word)[:2]
                except:
                    continue
                for syn in synonyms:
                    # print(syn)
                    try:
                        similarity = syn.path_similarity(f)
                    except:
                        continue
                    if similarity >= heuristic:
                        # print("Found match!\nWord in post: ", word, "\nSimilarity score: ", similarity, ".\nFilter: ",
                        #       f,
                        #       "\nSyn: ", syn, "\nSyn definition: ", syn.definition())
                        # print()
                        json_data['match'] = True

        t1 = time.time() - t0
        print(t1)
        return JsonResponse(json_data, safe=False)
    else:
        return HttpResponse("You tried a GET instead of a POST")
