import json
import os
import sys

import pandas
import pattern.en
import twitter
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

reload(sys)
sys.setdefaultencoding('utf-8')

myApi = twitter.Api(consumer_key='Fayly1okkvsf9bX8HioXD7RJd',
                    consumer_secret='5fO4De1uJ9zWkWSHzhniC7bAuLzXtfR0JNsHC2PiM3Win4HdaP',
                    access_token_key='121365445-1WLpzT6owWu9awLVYD0GU5yF4t8GPSPtjSejdFVo',
                    access_token_secret='J7Vp5D9GQoWgN6HePugSpdm8M15u9MK5CdoSHuTo6hAMG')

outfolder = "iot/arizona"
googleGeoAPI = "AIzaSyCPL1iGsOybfLTmLSM_TC26a8skvFFCfHo"

guidetails = []
weight = []


def window():
    # Create an PyQT4 application object.
    app = QApplication(sys.argv)

    # The QWidget widget is the base class of all user interface objects in PyQt4.
    w = QWidget()

    # Set window size.
    w.resize(3200, 2400)

    label_input1 = QLabel('Enter the name of your event', w)
    label_input1.move(520, 110)
    label_input1.resize(280, 40)
    label_input1.show()

    textbox_eventName = QLineEdit(w)
    textbox_eventName.move(520, 140)
    textbox_eventName.resize(280, 40)

    label_input2 = QLabel('Enter the Technology', w)
    label_input2.move(520, 190)
    label_input2.resize(280, 40)
    label_input2.show()

    textbox_Technology = QLineEdit(w)
    textbox_Technology.move(520, 220)
    textbox_Technology.resize(280, 40)

    label_input3 = QLabel('Enter the Location', w)
    label_input3.move(520, 270)
    label_input3.resize(280, 40)
    label_input3.show()

    textbox_Location = QLineEdit(w)
    textbox_Location.move(520, 300)
    textbox_Location.resize(280, 40)

    label_eventname = QLabel(w)
    label_eventname.move(820, 140)
    label_eventname.resize(280, 40)
    label_eventname.show()

    label_technology = QLabel(w)
    label_technology.move(820, 220)
    label_technology.resize(280, 40)
    label_technology.show()

    label_location = QLabel(w)
    label_location.move(820, 300)
    label_location.resize(280, 40)
    label_location.show()

    button1 = QPushButton('get event success', w)
    button1.move(520, 350)

    button_setweight = QPushButton('set weight', w)
    button_setweight.move(520, 440)
    button_setweight.hide()

    combo_weight = QComboBox(w)
    for i in range(1, 11):
        combo_weight.addItem(str(i))

    combo_weight.move(520, 410)
    combo_weight.hide()

    label_setweight_technology = QLabel('set the weight of Success Rate', w)
    label_setweight_technology.move(520, 380)
    label_setweight_technology.resize(280, 40)
    label_setweight_technology.hide()

    label_weightresultlabel = QLabel('the weight of location is', w)
    label_weightresultlabel.move(520, 460)
    label_weightresultlabel.resize(280, 40)
    label_weightresultlabel.hide()

    label_weightresult = QLabel(w)
    label_weightresult.move(670, 460)
    label_weightresult.resize(280, 40)
    label_weightresult.show()

    w.setWindowTitle("Event Success Rate prediction")

    @pyqtSlot()
    def button1_clicked():
        eventname = QLineEdit.text(textbox_eventName)
        location = QLineEdit.text(textbox_Location)
        technology = QLineEdit.text(textbox_Technology)
        label_eventname.setText(eventname)
        label_location.setText(location)
        label_technology.setText(technology)
        ab = [eventname, location, technology]

        for v in ab:
            guidetails.append(str(v))

        combo_weight.show()
        button_setweight.show()
        label_setweight_technology.show()

    @pyqtSlot()
    def button_setweight_clicked():
        val_of_weight = combo_weight.currentText()
        result = str(10 - int(val_of_weight))
        label_weightresult.setText(result)
        weight.append(result)
        label_weightresultlabel.show()
        display()

    button_setweight.clicked.connect(button_setweight_clicked)
    button1.clicked.connect(button1_clicked)

    w.show()
    sys.exit(app.exec_())


def display():
    print guidetails
    print weight


# print "Your query is: ", queryToGet
# location = raw_input("Enter Location")
# diameter = raw_input("Enter the Radius that you want to cover") + "mi"
# url = 'https://maps.googleapis.com/maps/api/geocode/json'
# params = {'sensor': 'false', 'address': location}
# r = requests.get(url, params=params)
# responeDict = r.json()
# lat = 0
# lon = 0
# if responeDict['status'] == 'OK':
# lat = responeDict['results'][0]['geometry']['location']['lat']
# lon = responeDict['results'][0]['geometry']['location']['lng']

# query = "io18 OR Google I/O 2018 OR googleIO2018 OR googleio2018 OR googleio"
# query = "#googleIO OR #googleio OR #googleio2018 OR #io18"
# filename = "googleIO.xltx"
# 36.7783 119.4179 california
# 31.9686, 99.9018 texas
# 27.6648, 81.5158 florida
# 42.4072, 71.3824 mass
# 40.7128, 74.0060 new york
# 40.6331, 89.3985 illinois
# 34.0489, 111.0937 arizona

def collect_data():
    filename = "iot.csv"
    query_newyork = ["robotics OR #Robotics", "BigData OR #BigData", "Data Analytics OR #DataAnalytics",
                     "Blockchain OR #Blockchain",
                     "Smart City OR #smartcity", "Datascience OR #DataScience OR Data Science",
                     "Cryptocurrency OR #Cryptocurrency", "cybersecurity OR CyberSecurity OR #CyberSecurity",
                     "UX OR ux OR #UX",
                     "AWS cloud OR #awscloud OR #aws OR cloudcomputing OR #cloudcomputing"]

    query_california = ["Blockchain OR #Blockchain", "Robotics OR #Robotics", "Security OR #security",
                        "BigData OR #BigData", "Datascience OR #DataScience OR Data Science",
                        "AWS cloud OR #awscloud OR #aws", "Cloudcomputing OR #cloudcomputing",
                        "Virtual Reality OR #VirtualReality OR #VR", "Augmented Reality OR #AugmentedReality OR #AR",
                        "Wifi OR #Wifi OR Wireless Fidelity OR #WirelessFidelity"]

    query_mass = ["Datascience OR #DataScience OR Data Science", "Robotics OR #Robotics", "Blockchain OR Blockchain",
                  "Smart City OR #smartcity", "OnlineSecurity OR #OnlineSsecurity",
                  "CyberAttacks OR #CyberAttacks OR Cyber Attacks", "ChatBots OR ChatBots OR Chatbots",
                  "EmbededDesign OR #EmbededDesign OR Embeded Design",
                  "Cloudcomputing OR #cloudcomputing", "Hacking OR #hacking", "EmbededSoftware OR #EmbededSoftware",
                  "IOS OR #ios",
                  "DigitalMarketing OR #DigitalMarketing"]

    query_texas = ["Robotics OR #Robotics", "BigData OR #BigData", "Datascience OR #DataScience OR Data Science",
                   "Wifi OR #Wifi OR Wireless Fidelity OR #WirelessFidelity", "BigData OR #BigData",
                   "Electric IoTWorld", "Electric Vehicles"]

    query_illinois = ["Blockchain OR #Blockchain", "Robotics OR #Robotics", "OnlineSecurity OR #onlinesecurity",
                      "BigData OR #BigData", "Datascience OR #DataScience OR Data Science",
                      "Cloudcomputing OR #cloudcomputing", "CyberAttacks OR #CyberAttacks", "IOS OR #ios",
                      "EmbededAvisor OR #EmbededAdvisor", "Smart City OR #smartcity",
                      "ChatBots OR #ChatBots OR Chatbots",
                      "Virtual Reality OR #VirtualReality OR #VR", "Augmented Reality OR #AugmentedReality OR #AR",
                      "Wifi OR #Wifi OR Wireless Fidelity OR #WirelessFidelity"]

    query_florida = ["Datascience OR #DataScience OR Data Science", "DigitalMarketing OR #DigitalMarketing",
                     "IOS OR #ios", "BigData OR #BigData", "cybersecurity OR CyberSecurity OR #CyberSecurity",
                     "Robotics OR #Robotics"]

    query_ariona = ["DataAnalytics OR #DAtaAnalytics OR Data Analytics", "Smart City OR #smartcity",
                    "UX OR #UX OR #UX/UI", "Malware OR #Malware", "Blockchain OR #Blockchain", "Robotics OR #Robotics",
                    "DigitalMarketing OR #DigitalMarketing", "BigData OR #BigData",
                    "cybersecurity OR CyberSecurity OR #CyberSecurity", "Cloudservices OR #cloudservices"]

    for i in query_ariona:
        geo = (34.0489, -111.0937, "1000mi")
        MAX_ID = None
        for it in range(5):  # Retrieve up to 100 tweets
            tweets = [json.loads(str(raw_tweet)) for raw_tweet
                      in myApi.GetSearch(term=i, geocode=geo, count=100, max_id=MAX_ID, result_type='recent')]
            if tweets:
                fname = os.path.join(outfolder, filename)
                f = open(fname, 'a+')
                for tweet in tweets:
                    f.write("AR," + i.split(" OR")[0] + "," + json.dumps(tweet['text']) + '\n')
                    print tweet['text']  # data = fetch_historical("@GoogleIO2018")


# txtPrint("@GoogleIO2018", data, out_folder)
#                 MAX_ID = tweets[-1]['id']
#                 MAX_ID, len(tweets)
# #
# def fetch_historical(user):
#     data = {}
#     max_id = None
#     total = 0
#     # print user
#     while True:
#         statuses = myApi.GetUserTimeline(screen_name=user, count=200, max_id=max_id)
#         newCount = ignCount = 0
#         for s in statuses:
#             if (newCount + ignCount) < 100:
#                 if s.id in data:
#                     ignCount += 1
#                 else:
#                     data[s.id] = s
#                     newCount += 1
#         total += newCount
#         print >> sys.stderr, "Fetched %d/%d/%d new/old/total." % (
#             newCount, ignCount, total)
#         if newCount == 0:
#             break
#         max_id = min([s.id for s in statuses]) - 1
#     return data.values()
#
# def txtPrint(user, tweets, out_folder):
#     for t in tweets:
#         t.pdate = parse(t.created_at)
#         print json.loads(str(t))['text']
#     key = operator.attrgetter('pdate')
#     tweets = sorted(tweets, key=key)
#     keytweets = [json.loads(str(rawtweet)) for rawtweet in tweets]
#     fname = '%s.xls' % user
#     fname = os.path.join(out_folder, fname)
#     f = open(fname, 'a+')
#     for tweet in keytweets:
#         f.write(json.dumps(tweet['text']) + '\n')
#     f.close()

# vectorizer = TfidfVectorizer(stop_words='english')
# X = vectorizer.fit_transform()
#
# true_k = 2
# model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
# model.fit(X)
#
# print("Top terms per cluster:")
# order_centroids = model.cluster_centers_.argsort()[:, ::-1]
# terms = vectorizer.get_feature_names()
# for i in range(true_k):
#     print("Cluster %d:" % i),
#     for ind in order_centroids[i, :10]:
#         print(' %s' % terms[ind]),
#     print
#
# print("\n")
# print("Prediction")
#
# Y = vectorizer.transform(["Ninja is climbing and Google is the best."])
# prediction = model.predict(Y)
# print(prediction)
#
# Y = vectorizer.transform(["My cat is hungry."])
# prediction = model.predict(Y)
# print(prediction)


# with open("googleIO/newyork/googleIO.xltx", "r") as f:
#     cali_tweets = f.readlines()
#     print type(cali_tweets)
#     f = open("consolidated.xltx", "a+")
#     for tweets in cali_tweets:
#         f.write("googleIO" + "NY" + json.dumps(tweets))
# colnames = ['Event_Name','Location','Text']

def generate_clusters(state):
    colnames = ['Text']
    data = pandas.read_csv('iot/' + state + '/iot.csv', names=colnames)

    documents = data.Text.tolist()
    print type(documents)

    stopwords = ['U2026', '@MikeQuindazzi', 'RT', 'mikequindazzi', 'u2026', 'rt', 'u201d', 'iot', 'i_robertjones',
                 'djs2kiebs8', 'u201csmart', '0vcyqv8h6d', "a", "about", "above", "above", "across", "after",
                 "afterwards", "again", "against", "all", "almost",
                 "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "amoungst",
                 "amount",
                 "an", "and", "another", "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are", "around",
                 "as",
                 "at", "back", "be", "became", "because", "become", "becomes", "becoming", "been", "before",
                 "beforehand",
                 "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom", "but",
                 "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe",
                 "detail",
                 "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else", "elsewhere",
                 "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except",
                 "few",
                 "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty",
                 "found",
                 "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he",
                 "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him",
                 "himself",
                 "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it",
                 "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may",
                 "me",
                 "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must",
                 "my",
                 "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none",
                 "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only",
                 "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own", "part",
                 "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems",
                 "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so",
                 "some",
                 "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system",
                 "take",
                 "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter",
                 "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this",
                 "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top",
                 "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very",
                 "via",
                 "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter",
                 "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither",
                 "who",
                 "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you",
                 "your", "yours", "yourself", "yourselves", "the", '0,"rt', '1,"rt', "&amp;", "twitter", "@taywurr:",
                 "@imangelapowers:", "today", "17t04", "fisher85m", "9ewuv1zbqu", "gp_pulipaka", "ys2p7obpby", "u00a0"]

    vectorizer = TfidfVectorizer(stop_words=stopwords)
    X = vectorizer.fit_transform(documents)

    true_k = 10
    model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
    model.fit(X)

    print("Top terms per cluster:")
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    for i in range(true_k):
        print("Cluster %d:" % i),
        for ind in order_centroids[i, :10]:
            print(' %s' % terms[ind]),
        print

    print("\n")
    print("Prediction")

    Y = vectorizer.transform(["iot"])
    prediction = model.predict(Y)
    print(prediction)


def calculate_sentimentscore():
    colnames = ['Location', 'Technology', 'Tweet']
    data = pandas.read_csv("iot/texas/iot.csv", names=colnames)
    tweetText = data.Tweet.tolist()
    pscore = []
    for i in range(len(tweetText)):
        if pattern.en.positive(tweetText[i], threashold=0.1) == True:
            pscore.append("1")
        else:
            pscore.append("0")

    data['Sentiment_Score'] = pscore
    data.to_csv("iot/texas/iot.csv")


def main():
    print "\n\n\n************ Collecting data ****************\n"
    # collect_data()
    # states = ["arizona","california","newyork","florida","illinois","texas","mass"]

    # for i in states:
    #     # generate_clusters(i)
    #
    # pass

    files = ["iot/arizona/iot.csv", "iot/california/iot.csv", "iot/newyork/iot.csv", "iot/illinois/iot.csv",
             "iot/mass/iot.csv", "iot/florida/iot.csv", "iot/texas/iot.csv"]

    colnames = ['Location', 'Technology', 'Tweet']

    # tt = open("trainingtable.csv", "a")
    # for i in files:
    #     f = open(i)
    #     f.next()
    #     for l in f:
    #         tt.write(l)
    #
    #     f.close()
    #
    # tt.close()

    # alldata = pandas.read_csv(i, names=colnames)
    # print alldata

    # calculate_sentimentscore()


if __name__ == '__main__':
    main()
    window()
