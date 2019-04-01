import operator
import sys
import twitter

import pandas
import pattern.en
from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

out_folder = ""

reload(sys)
sys.setdefaultencoding("utf-8")

myApi = twitter.Api(consumer_key='suZnico4RTdKDp00KyabU8reE', \
                    consumer_secret='v9H5i9MjcRQvHGpo019qo7LEv6WKsVVxiuxgSDiW9436I4sY8h', \
                    access_token_key='2957047400-B0OeYDcCTbmj5cKAGOnMwF30Z0jYFxULmVUIHbL', \
                    access_token_secret='9dayuCykfvAimkptXdyrvsjQbJ3Cn4qu9KdzdKIpoQsF5')


def print_info(tweet):
    print '***************************'
    print 'Tweet ID: ', tweet[-1]['id']
    print 'Post Time: ', tweet[-1]['created_at']
    print 'User Name: ', tweet[-1]['user']['screen_name']
    try:
        print 'Tweet Text: ', tweet[-1]['text']
    except:
        pass


# def fetch_historical(user):
#     data = {}
#     max_id = None
#     total = 0
#     while True:
#         statuses = myApi.GetUserTimeline(screen_name=user, count=10)
#         newCount = ignCount = 0
#         for s in statuses:
#             if s.id in data:
#                 ignCount += 1
#             else:
#                 data[s.id] = s
#                 newCount += 1
#         total += newCount
#         print >>sys.stderr, "Fetched %d/%d/%d new/old/total." % (
#             newCount, ignCount, total)
#         if newCount == 0:
#             break
#         max_id = min([s.id for s in statuses])-1
#     return data.values()

#
# def rest_query_ex3():
#     filename = "relevanttweets.txt"
#     query = 'python'
#     geo = (34.048927, -111.093735, '1000mi')  # illinois
#     MAX_ID = None
#     for it in range(10):  # Retrieve up to 200 tweets
#         tweets = [json.loads(str(raw_tweet)) for raw_tweet
#                   in myApi.GetSearch(term=query, geocode=geo, count=100, max_id=MAX_ID, result_type='recent')]
#         print tweets
#         if tweets:
#             fname = os.path.join(out_folder, filename)
#             f = open(fname, 'a+')
#             for tweet in tweets:
#                 f.write(json.dumps(tweet['text']) + '\n')
#             print tweets
#             MAX_ID = tweets[-1]['id']
#             userid = tweets[-1]['user']['screen_name']
#             # data = fetch_historical(userid)
#             # txtPrint(userid, data , out_folder)
#             print MAX_ID, len(tweets), userid
#             print print_info(tweets)


# def txtPrint(user, tweets, out_folder):
#     print tweets
#     for t in tweets:
#         t.pdate = parse(t.created_at)
#         print json.loads(str(t))['text']
#     key = operator.attrgetter('pdate')
#     tweets = sorted(tweets, key=key)
#     keytweets = [json.loads(str(rawtweet)) for rawtweet in tweets]
#     fname = '%s.txt'%user
#     fname = os.path.join(out_folder, fname)
#     f = open(fname,'a+')
#     for tweet in keytweets:
#         f.write(json.dumps(tweet['text']) + '\n')
#     f.close()
#
# def CalculateSentimentScoreOfAFile(filename):
#     colnames = ['Location', 'Technology', 'Tweettext', 'SentimentScore']
#     data = pandas.read_excel(filename, names=colnames)
#     tweetText = data.Tweettext.tolist()
#     score = data.Sentiment_Score.tolist()
#     for i in range(len(tweetText)):
#         if pattern.en.positive(tweetText[i], threashold=0.1) == True:
#             print "1"
#         else:
#             print "0"

def calculate_sentimentscore():
    colnames = ['Location', 'Technology', 'Tweet', 'Sentiment_Score']
    data = pandas.read_excel("Final_NY_AIML.xlsx", names=colnames)
    tweetText = data.Tweet.tolist()
    score = data.Sentiment_Score.tolist()
    pscore = []
    for i in range(len(tweetText)):
        if pattern.en.positive(tweetText[i], threashold=0.1) == True:
            print "True"
            pscore.append("1")
        else:
            print "False"
            pscore.append("0")

    data['Sentiment_Score'] = pscore
    data.to_excel("Final_NY_AIML.xlsx")


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
        current_location = guidetails[1]
        technology1 = guidetails[2]
        current_succes = calculate_success(current_location, technology1)
        if current_succes < 20:
            print "Success Rate will be low as entered technology is still emerging at desired location"
            QtCore.QCoreApplication.instance().quit()

            recommendation(current_location, current_succes, technology)
        else:
            print "Predicted Success Rate"
            print current_succes


    button1.clicked.connect(button1_clicked)

    w.show()
    sys.exit(app.exec_())




def calulateRMSEAndAccuracy(filename, technology):
    file = pandas.read_csv(filename)
    sum = 0
    total = 0
    squaredError = 0
    lines = file.loc[file['Technology'] == technology]
    sentimentscores = lines.Sentiment_Score.tolist()
    for i in range(len(sentimentscores)):
        if sentimentscores[i] == 1:
            sum = sum + 1
        total = total + 1

    mean = float(sum) / float(total)

    for i in range(len(sentimentscores)):
        squaredError = squaredError + ((mean - sentimentscores[i]) * (mean - sentimentscores[i]))

    rmse = squaredError / total
    print squaredError
    print rmse

    return rmse


def recommendation(current_location, current_succes, technology):
    # distances lists
    success_pref = float(raw_input("Enter Success Weight"))

    location_pref = 1-success_pref
    AR = [734, 2148, 1561, 2576, 2348, 826]
    CA = [734, 2702, 2082, 3094, 2920, 1405]
    FL = [2148, 2702, 1184, 1342, 1142, 1397]
    IL = [1561, 2082, 1184, 1098, 912, 994]
    MA = [2576, 3094, 1342, 1098, 207, 1973]
    NY = [2348, 2920, 1142, 912, 207, 1764]
    TX = [826, 1405, 1397, 994, 1973, 1764]

    # print "in reccommendation function"
    states = ("AR", "CA", "FL", "IL", "MA", "NY", "TX")
    computed_states = []
    percentages = []
    for i in range(len(states)):
        if states[i] != current_location:
            sum = 0
            total = 0
            file = pandas.read_excel("Final_" + states[i] + ".xlsx")
            lines = file.loc[file['Technology'] == technology]
            sentimentscores = lines.Sentiment_Score.tolist()
            for j in range(len(sentimentscores)):
                if sentimentscores[j] == 1:
                    sum = sum + 1
                total = total + 1

            if total < 50:
                percentage = 0
                percentages.insert(i, percentage)
                computed_states.insert(i, states[i])
                window2()
            else:
                # totals.insert(i, total)
                percentage = 100 * float(sum) / float(total)
                percentages.insert(i, percentage)
                computed_states.insert(i, states[i])
                # elif states[i] == current_location:
                #     percentages.insert(i,current_succes)

    # print computed_states
    # print percentages

    if current_location == "AR":
        distances = AR
    elif current_location == "CA":
        distances = CA
    elif current_location == "FL":
        distances = FL
    elif current_location == "IL":
        distances = IL
    elif current_location == "MA":
        distances = MA
    elif current_location == "NY":
        distances = NY
    elif current_location == "TX":
        distances = TX

    # pref_results = []
    # ask preference

    # location_pref = 0.3
    # success_pref = 0.7
    pref_results1 = dict()
    for i in range(len(computed_states)):
        pref_result = ((location_pref * distances[i]) + (success_pref * (100 - percentages[i])))
        # pref_results.insert(i, pref_result)
        pref_results1[computed_states[i]] = pref_result

    # print "final results"
    # print pref_results
    # print "pref result dictionary"
    # for key, value in pref_results1.items():
    #     print ("{key}:{value}".format(key=key, value=value))

    # loc_success = dict((v, k) for k, v in pref_results1.iteritems())
    # print loc_success

    # print pref_results1
    print "Recommendations based on entered weights:"
    sorted_loc_success = sorted(pref_results1.items(), key=operator.itemgetter(1))
    print sorted_loc_success
    # print "sorted dict"
    # print sorted_loc_success
    #
    # parallel_coordinates(sorted_loc_success, 'Monetary')
    # plt.show()


def calculate_success(location, technology):

    print location,
    print technology

    if location == "AR":
        file = pandas.read_excel("Final_AR.xlsx")
    elif location == "CA":
        file = pandas.read_excel("Final_CA.xlsx")
    elif location == "FL":
        file = pandas.read_excel("Final_FL.xlsx")
    elif location == "IL":
        file = pandas.read_excel("Final_IL.xlsx")
    elif location == "MA":
        file = pandas.read_excel("Final_MA.xlsx")
    elif location == "NY":
        file = pandas.read_excel("Final_NY.xlsx")
    elif location == "TX":
        file = pandas.read_excel("Final_TX.xlsx")

    sum = 0
    total = 0
    lines = file.loc[file['Technology'] == technology]
    sentimentscores = lines.Sentiment_Score.tolist()
    for i in range(len(sentimentscores)):
        if sentimentscores[i] == 1:
            sum = sum + 1
        total = total + 1

    percentage = 100 * float(sum) / float(total)
    # print "actual percentage"
    # print percentage
    # print "total tweets at entered location"
    # print total
    if total < 50:
        return 0
    return percentage


def main():
    print "\n\n\n************ rest_query_ex1() ****************\n"
    # rest_query_ex3()
    current_location = "IL"
    # technology = guidetails[2]
    window()
    print weight
    # # current_succes = calculate_success(current_location, technology)
    # if current_succes < 30:
    #     print "Success Rate will be low as entered technology is still emerging at desired location"
    #     # recommendation(current_location, current_succes, technology)
    # else:
    #     print "Predicted Success Rate"
    #     print current_succes
    # # calculate_sentimentscore()
    # # CalculateSentimentScoreOfAFile(filename)
    # # calulateRMSEAndAccuracy("Final_TX")
    # pass


if __name__ == '__main__':
    main()
"1000"
