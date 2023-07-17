from django.shortcuts import render, redirect
from dashboard_app.twitterUtils import TwitterHandle
from dashboard_app.load_tweets import load_tweets_from_csv_zip
from django.contrib import messages
from .forms import UserRegistrationForm


def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, f'Your account has been created. You can log in now!')    
            return redirect('login')
    else:
        form = UserRegistrationForm()

    context = {'form': form}
    return render(request, 'register.html', context)

def login(request):
    return render(request, 'login.html')

def show(request):
    search_query = request.GET.get('search')
    tutils = TwitterHandle()
    tweets = tutils.get_tweets(search_query)
    positive_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    negative_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    neutral_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']
    total_tweets = len(tweets)
    positive_sentiment = int((len(positive_tweets) / total_tweets) * 100)
    negative_sentiment = int((len(negative_tweets) / total_tweets) * 100)
    neutral_sentiment = int(100 - (positive_sentiment + negative_sentiment))

    context = {}
    context['sentiment'] = {
        'positive_sentiment': 0.75,
        'negative_sentiment': 0.5,
        'neutral_sentiment': 0.20
    }
    context['positive_tweets'] = positive_tweets[:5]
    context['negative_tweets'] = negative_tweets[:5]
    context['neutral_tweets'] = neutral_tweets[:5]

    return render(request, 'chart.html', context)


def data_load(request):
    try:
        load_tweets_from_csv_zip()
        messages.success(request, "data load successfull!!!")

    except Exception as e:
        print(e)
        messages.error(request, f"Data load failed!!!\n{e}")
    return redirect('home')


def prediction(request):
    arr_pred = []
    arr_pos_txt = []
    arr_neg_txt = []
    if request.method == 'POST':
        api = TwitterHandle()
        t = request.POST['tweeterid']
        tweets = api.get_tweets(query=t, count=100)

        pos_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
        pos = "Positive tweets percentage: {} %".format(100 * len(pos_tweets) / len(tweets))

        neg_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
        neg = "Negative tweets percentage: {}%".format(100 * len(neg_tweets) / len(tweets))
        # adding the percentages to the prediction array to be shown in the html page.
        arr_pred.append(pos)
        arr_pred.append(neg)

        # storing first 5 positive tweets
        arr_pos_txt.append("Positive tweets:")
        for tweet in pos_tweets[:5]:
            arr_pos_txt.append(tweet['text'])

        # storing first 5 negative tweets
        arr_neg_txt.append("Negative tweets:")
        for tweet in neg_tweets[:5]:
            arr_neg_txt.append(tweet['text'])

        return render(request, 'prediction.html', {'arr_pred': arr_pred
            , 'arr_pos_txt': arr_pos_txt, 'arr_neg_txt': arr_neg_txt})
