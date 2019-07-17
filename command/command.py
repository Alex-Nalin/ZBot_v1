import os
import codecs
import json
import requests
import logging
from time import sleep
import http
import re
import ast
from googleapiclient.discovery import build

_configPath = os.path.abspath('../command/config.json')
with codecs.open(_configPath, 'r', 'utf-8-sig') as json_file:
    _config = json.load(json_file)


def remove_emoji(emoji):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\u200d"
                               u"\u2640-\u2642"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', emoji.decode("utf-8"))

class Help:

    def __init__(self, bot_client):
        self.bot_client = bot_client

    def help(self):

        #"<h2>Bot Help</h2> \

        displayHelp = "<card accent='tempo-bg-color--blue' iconSrc=''> \
                            <header><h2>Bot Commands</h2></header> \
                            <body> \
                              <table> \
                                <thead> \
                                  <tr> \
                                    <td>Command</td> \
                                    <td>Usage</td> \
                                    <td>Description</td> \
                                    <td>Permission</td> \
                                  </tr> \
                                </thead> \
                                <tbody> \
                                  <tr> \
                                    <td>/weather</td> \
                                    <td>/weather location days[0-7]</td> \
                                    <td>Gives weather forecast up to 7 days, if citi is more than one string, use _</td> \
                                    <td>All</td> \
                                  </tr> \
                                  <tr> \
                                    <td>/gif</td> \
                                    <td>/gif string</td> \
                                    <td>Search Giphy for gif randomly or specific if string is provided</td> \
                                    <td>All</td> \
                                  </tr> \
                                  <tr> \
                                    <td>/quoteoftheday</td> \
                                    <td>/quoteoftheday or /qod</td> \
                                    <td>Give the Quote of the Day to ponder on</td> \
                                    <td>All</td> \
                                  </tr> \
                                  <tr> \
                                    <td>/bot joke</td> \
                                    <td>/bot joke</td> \
                                    <td>Punch line joke call</td> \
                                    <td>All</td> \
                                  </tr> \
                                  <tr> \
                                    <td>/jokes</td> \
                                    <td>/jokes</td> \
                                    <td>Gives another API call to a different Joke endpoint</td> \
                                    <td>All</td> \
                                  </tr> \
                                  <tr> \
                                    <td>/funQuote</td> \
                                    <td>/funQuote</td> \
                                    <td>Finds Movie and Famous people's Quote</td> \
                                    <td>All</td> \
                                  </tr> \
                                </tbody> \
                                </table> \
                            </body> \
                        </card>"

        #return dict(message='<messageML><div class="wysiwyg">' + displayHelp + '</div></messageML>')
        return dict(message='<messageML>' + displayHelp + '</messageML>')

class punchJoke:

    def __init__(self, bot_client):
        self.bot_client = bot_client

    def get_random_joke(self):
        logging.debug('Getting a random joke..')
        url = 'https://official-joke-api.appspot.com/jokes/random'

        try:
            response = requests.get(url)
            response_body = json.loads(response.text)
            question = response_body['setup']
            punchline = response_body['punchline']
            return question, punchline
        except requests.exception.HTTPError as e:
            return "", ""

    def send_joke(self, stream_id):
        question, punchline = self.get_random_joke()
        for line in question, punchline:
            msg_to_send = dict(
                message='<messageML><div class="wysiwyg">' +
                        '<p>' +
                        line +
                        '</p></div>'
                        '</messageML>')
            self.bot_client.get_message_client().send_msg(stream_id, msg_to_send)
            sleep(3)
        # self.bot_client.get_message_client().send_msg_with_attachment(
        #     stream_id,
        #     '<messageML>Attachment POC</messageML>',
        #     'nameoftheImage.png',
        #     '../data/image.png')

class Jokes:

    def __init__(self, bot_client):
        self.bot_client = bot_client

    def getJokes(self):
        try:

            try:
                conn = http.client.HTTPSConnection(_config['Jokes']['URL'])

                headers = {
                    'accept': "application/json",
                    'user-agent': _config['Jokes']['user-agent'],
                    'cache-control': "no-cache"
                }

                conn.request("GET", "/", headers=headers)

                res = conn.getresponse()
                data = res.read().decode("utf-8")

                render = data.split("\":")

                jokeData = render[2][:-8].replace("\u2019", "'").replace("\n", "")
                #print(jokeData)

            except:
                return dict(message="<messageML>Please try Joke later.</messageML>")
            return dict(message="<messageML>Here's a joke for you <b> " + jokeData + "</b></messageML>")
        except:
            return dict(message="<messageML>Joke did not work</messageML>")

class FunQuote:

    def __init__(self, bot_client):
        self.bot_client = bot_client


    def funQuote(self):
        try:
            try:
                conn = http.client.HTTPSConnection(_config['x-mashape']['URL'])

                headers = {
                    'x-mashape-key': _config['x-mashape']['API_Key'],
                    'cache-control': "no-cache"
                }

                conn.request("GET", "/", headers=headers)

                res = conn.getresponse()
                data = res.read().decode("utf-8")
                #print("data: " + data)

                fundata = str(data)
                quotedata = fundata.split(":")
                quote = quotedata[1][:-9]
                author = quotedata[2][1:][:-12]
                category = quotedata[3][:-2].replace("\"", "")
            except:
                return dict(message="<messageML>Please try FunQuote later.</messageML>")

            return dict(message="<messageML>" + category + " quote from <b>" + author + "</b>: <b>" + quote + "</b></messageML>")
        except:
            return dict(message="<messageML>FunQuote did not work</messageML>")


class GetGiphyImage:

    def __init__(self, bot_client):
        self.bot_client = bot_client

    def GetGiphy(self, giphyText):

        try:
            giphyAPIKey = _config['giphy']['apikey']

            paramList = giphyText.split()
            gifLen = len(paramList[0]) + 1
            isRandom = len(paramList) == 1 or paramList[1] == 'random'

            if isRandom:
                ep = "http://api.giphy.com/v1/gifs/random"
                payload = {"apikey": giphyAPIKey}
            else:
                giphyText = giphyText[int(gifLen):]
                print(giphyText)
                ep = "http://api.giphy.com/v1/gifs/translate"
                payload = {"apikey": giphyAPIKey, "s": giphyText}

            response = requests.get(ep, params=payload).json()

            if isRandom:
                #print("Random")
                gifimagelink = (response['data']['image_original_url'])
                msgtoui = "<card iconSrc=\"\" accent=\"tempo-bg-color--blue\"><header>(Click to view the GIF)</header><body><img src=\"" + gifimagelink + "\"/><br/><a href=\"" + gifimagelink + "\"/></body></card>"

            else:
                #print("Specific")
                gifimagelink = (response['data']['images']['original']['url'])
                # header = ' '.join(paramList)
                header = giphyText
                msgtoui = "<card iconSrc=\"\" accent=\"tempo-bg-color--blue\"><header> You searched Giphy for: \"<b>"+ header +"</b>\" (click to view GIF)</header><body><img src=\"" + gifimagelink + "\"/><br/><a href=\"" + gifimagelink + "\"/></body></card>"

        except Exception as ex:
            errorStr = "Symphony REST Exception (system): {}".format(ex)
            logging.debug('error', errorStr)
            msgtoui = "Sorry, I could not return a GIF right now."

        return dict(message="<messageML>" + str(msgtoui) + "</messageML>")

    ## Not used as the sending is handled in the listener
    # def send_giphy(self, stream_id):
    #
    #     messagetosend = self.GetGiphy()
    #
    #     ## This send the card with a space in front, like an image is missing
    #     # msg_to_send = dict(
    #     #     message='<messageML><div class="wysiwyg">' +
    #     #             '<p>' +
    #     #             str(messagetosend) +
    #     #             '</p></div>'
    #     #             '</messageML>')
    #
    #     msg_to_send = dict(message="<messageML>" + str(messagetosend) + "</messageML>")
    #
    #     #print("msg_to_send: " + str(msg_to_send))
    #     self.bot_client.get_message_client().send_msg(stream_id, msg_to_send)


class WikiSearch:

    def __init__(self, bot_client):
        self.bot_client = bot_client

    def wiki(self, wikiText):

        request = str(wikiText).split()
        wikiLen = len(request[0]) + 1

        my_api_key = _config['Wiki']['API_Key']
        my_cse_id = _config['Wiki']['token']

        try:
            wikiText = wikiText[int(wikiLen):]
            print(wikiText)
            service = build("customsearch", "v1", developerKey=my_api_key)
            res = service.cse().list(q=wikiText, cx=my_cse_id, num=3).execute()
            print(res)
            results = res['items']
            #print(str(results))
        except:
            return dict(message="<messageML>Please use a valid search</messageML>")


        table_body = ""
        table_header = "<table style='max-width:95%'><thead><tr style='background-color:#4D94FF;color:#ffffff;font-size:1rem' class=\"tempo-text-color--white tempo-bg-color--black\">" \
                       "<td style='max-width:10%'>Link</td>" \
                       "<td>Information</td>" \
                       "</tr></thead><tbody>"

        for result in results:
            link_raw = result["link"]
            link = str(link_raw).replace(_config['Wiki']['replace'], "")

            table_body += "<tr>" \
                          "<td><a href =\"" + link_raw + "\">" + link + "</a></td>" \
                          "<td>" + str(result["snippet"]).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;") + "</td>" \
                          "</tr>"

        table_body += "</tbody></table>"

        reply = table_header + table_body
        return dict(message="<messageML>" + str(reply) + "</messageML>")


class QuoteOftheDay:

    def __init__(self, bot_client):
        self.bot_client = bot_client

    def QoD(self):

        try:

            conn = http.client.HTTPConnection("quotes.rest")
            headers = {
                'cache-control': "no-cache",
            }
            conn.request("GET", "/qod", headers=headers)
            res = conn.getresponse()
            data = res.read()
            parsed = json.loads(data)
            parsedData = (json.dumps(parsed, indent=4))
            #print("parsedData: " + parsedData)
            qodraw = (data.decode("utf-8")).replace("\n", "")

            qodrawsplit = qodraw.split("\":")
            checklen = len(qodrawsplit)

            if checklen == 4:
                replyToChat = "Quote of the Day will be live again tomorrow :)"
                return dict(message="<messageML>" + str(replyToChat) + "</messageML>")
            else:

                qodrawsplitdata = str(qodrawsplit[5][2:][:-23])
                qodrawsplitdata = qodrawsplitdata.replace("\",", "")
                qodrawsplitAuhor = str(qodrawsplit[7][2:][:-21])
                qodrawsplitAuhor = qodrawsplitAuhor.replace("\",", "")

                qod_msg = "<card accent=\"tempo-bg-color--blue\"><header>Quote of the Day by " + str(qodrawsplitAuhor) + "</header><body>" + str(qodrawsplitdata).replace("\\r\\n"," ").replace("\\r\\"," ") + "</body></card>"
                return dict(message="<messageML>" + str(qod_msg) + "</messageML>")

        except:
            return dict(message="<messageML>Quote of the Day did not work</messageML>")


class Weather:

    def __init__(self, bot_client):
        self.bot_client = bot_client

    def weather(self, weatherText):

        # try:
        #
        #     commandCallerUID = messageDetail.FromUserId
        #
        #     connComp.request("GET", "/pod/v3/users?uid=" + commandCallerUID, headers=headersCompany)
        #
        #     resComp = connComp.getresponse()
        #     dataComp = resComp.read()
        #     data_raw = str(dataComp.decode('utf-8'))
        #     data_dict = ast.literal_eval(data_raw)
        #
        #     dataRender = json.dumps(data_dict, indent=2)
        #     d_org = json.loads(dataRender)
        #
        #     for index_org in range(len(d_org["users"])):
        #         firstName = d_org["users"][index_org]["firstName"]
        #         lastName = d_org["users"][index_org]["lastName"]
        #         displayName = d_org["users"][index_org]["displayName"]
        #         #companyName = d_org["users"][index_org]["company"]
        #         companyNameTemp = d_org["users"][index_org]["company"]
        #         companyTemp = str(companyNameTemp).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;")
        #         companyName = str(companyTemp)
        #         userID = str(d_org["users"][index_org]["id"])
        #
        #     botlog.LogSymphonyInfo(firstName + " " + lastName + " (" + displayName + ") from Company/Pod name: " + str(companyName) + " with UID: " + str(userID))
        #     callerCheck = (firstName + " " + lastName + " - " + displayName + " - " + companyName + " - " + str(userID))
        #
        # except:
        #     botlog.LogSymphonyInfo("Inside second user check")
        #     commandCallerUID = messageDetail.FromUserId
        #
        #     connComp.request("GET", "/pod/v3/users?uid=" + commandCallerUID, headers=headersCompany)
        #
        #     resComp = connComp.getresponse()
        #     dataComp = resComp.read()
        #     data_raw = str(dataComp.decode('utf-8'))
        #     data_dict = ast.literal_eval(data_raw)
        #
        #     dataRender = json.dumps(data_dict, indent=2)
        #     d_org = json.loads(dataRender)
        #
        #     for index_org in range(len(d_org["users"])):
        #         firstName = d_org["users"][index_org]["firstName"]
        #         lastName = d_org["users"][index_org]["lastName"]
        #         displayName = d_org["users"][index_org]["displayName"]
        #         #companyName = d_org["users"][index_org]["company"]
        #         companyNameTemp = d_org["users"][index_org]["company"]
        #         companyTemp = str(companyNameTemp).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;")
        #         companyName = str(companyTemp)
        #         userID = str(d_org["users"][index_org]["id"])
        #
        #     botlog.LogSymphonyInfo(firstName + " " + lastName + " (" + displayName + ") from Company/Pod name: " + str(companyName) + " with UID: " + str(userID))
        #     callerCheck = (firstName + " " + lastName + " - " + displayName + " - " + companyName + " - " + str(userID))
        #
        # try:
        #     if callerCheck in AccessFile:
        #
        #         botlog.LogSymphonyInfo("Bot Call: Weather")
        #
        #         # try:
        #
        message = weatherText
        #stream_id = streamId
        weatherCatcher = message.split()
        location = ""
        days = ""
        rawtwo = 2
        two = str(rawtwo)
        rawthree = 3
        three = str(rawthree)
        rawfour = 4
        four = str(rawfour)
        rawfive = 5
        five = str(rawfive)
        rawsix = 6
        six = str(rawsix)
        rawseven = 7
        seven = str(rawseven)

        catchLength = len(weatherCatcher)
        print("Lenght is: " + (str(catchLength)))

        try:
            emptyLocation = catchLength == 0 or weatherCatcher[0] == ""
            if emptyLocation:
                replyToChat = "Please enter a location, if it is more than one word, e.g New York, please use underscore as in New_York"
                return dict(message="<messageML>" + str(replyToChat) + "</messageML>")
            else:
                location = weatherCatcher[1]
                print("Location: " + location)
        except:
            print("Loading the weather forecast")
            # replyToChat = "Loading the weather forecast"
            # return dict(message="<messageML>" + str(replyToChat) + "</messageML>")

        try:
            emptyDays = weatherCatcher[2] == ""
            if emptyDays:
                days = 0
            else:
                days = weatherCatcher[2]
                # replyToChat = "Forecasting weather for <b>" + str(days) + "</b> days in <b>" + str(location) + "</b>"
                # return dict(message="<messageML>" + str(replyToChat) + "</messageML>")

                print("Forecasting weather for <b>" + str(days) + "</b> days in <b>" + str(location) + "</b>")
                # replyToChat = "Forecasting weather for <b>" + str(days) + "</b> days in <b>" + str(location) + "</b>"
                # return dict(message="<messageML>" + str(replyToChat) + "</messageML>")

                print("Days: " + days)
        except:
            print("Forecasting weather for today in <b>" + str(location) + "</b>")
            # replyToChat = "Forecasting weather for today in <b>" + str(location) + "</b>"
            # return dict(message="<messageML>" + str(replyToChat) + "</messageML>")


        conn = http.client.HTTPSConnection("api.apixu.com")
        headers = {
            'cache-control': "no-cache",
        }
        conn.request("GET", "/v1/forecast.json?key=" + _config['weather']['API_Key'] + "&q=" + location + "&days=" + days + "", headers=headers)
        res = conn.getresponse()
        data = res.read()
        d_raw = remove_emoji(data)
        data_new = d_raw.replace("","").replace("Å","ō")
        # print(data_new)
        # request_raw = data.decode('utf-8')
        data = json.dumps(data_new, indent=2)
        # data = json.dumps(request_raw, indent=2)
        data_dict = ast.literal_eval(data)
        d = json.loads(data_dict)
        # d = data
        # print(str(d))

        # Checking for location validation
        notmatchingLocation = "{'error': {'code': 1006, 'message': 'No matching location found.'}}"
        #tempWeather = str(data.decode("utf-8")).replace("\"", "")
        tempWeather = str(d).replace("\'", "")
        #print("tempWeather: " + str(tempWeather))

        if str(d).startswith(notmatchingLocation):
            replyToChat = "The location entered is not valid, please try again."
            return dict(message="<messageML>" + str(replyToChat) + "</messageML>")
        else:

            # try:
            # # Main weather info - to display regardless of days selected
            weatherRaw = tempWeather.split(":")
            LocationName = str(d["location"]["name"])
            Region = str(d["location"]["region"])
            Country = str(d["location"]["country"])
            LastUpdated = str(d["current"]["last_updated"])
            TempC = str(d["current"]["temp_c"])
            TempF = str(d["current"]["temp_f"])
            Condition = str(d["current"]["condition"]["text"])
            CurrentURL = str(d["current"]["condition"]["icon"])

            day1date = str(d["forecast"]["forecastday"][0]["date"])
            day1maxtemp = str(d["forecast"]["forecastday"][0]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][0]["day"]["maxtemp_f"]) + " F"
            day1mintemp = str(d["forecast"]["forecastday"][0]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][0]["day"]["mintemp_f"]) + " F"
            day1avgtemp = str(d["forecast"]["forecastday"][0]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][0]["day"]["avgtemp_f"]) + " F"
            day1maxwind = str(d["forecast"]["forecastday"][0]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][0]["day"]["maxwind_kph"]) + " kph"
            day1totalprecip = str(d["forecast"]["forecastday"][0]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][0]["day"]["totalprecip_in"]) + "in"
            day1avghumidity = str(d["forecast"]["forecastday"][0]["day"]["avghumidity"])
            day1condition = str(d["forecast"]["forecastday"][0]["day"]["condition"]["text"])
            day1icon = str(d["forecast"]["forecastday"][0]["day"]["condition"]["icon"])
            day1sunrise = str(d["forecast"]["forecastday"][0]["astro"]["sunrise"])
            day1sunset = str(d["forecast"]["forecastday"][0]["astro"]["sunset"])
            day1moonrise = str(d["forecast"]["forecastday"][0]["astro"]["moonrise"])
            day1moonset = str(d["forecast"]["forecastday"][0]["astro"]["moonset"])
            # except:
            #     return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")

            table_body = "<table style='table-layout:auto;width:100%'>" \
                         "<thead>" \
                         "<tr class=\"tempo-text-color--white tempo-bg-color--black\">" \
                         "<td>Date</td>" \
                         "<td>Max Temp</td>" \
                         "<td>Min Temp</td>" \
                         "<td>Avg Temp</td>" \
                         "<td>Max Wind</td>" \
                         "<td>Tot Precipitation</td>" \
                         "<td>Avg Humidity</td>" \
                         "<td>Condition</td>" \
                         "<td></td>" \
                         "<td>Sunrise</td>" \
                         "<td>Sunset</td>" \
                         "<td>Moonrise</td>" \
                         "<td>Moonset</td>" \
                         "</tr>" \
                         "</thead><tbody>"

            table_body += "<tr>" \
                          "<td>" + day1date + "</td>" \
                          "<td>" + day1maxtemp + "</td>" \
                          "<td>" + day1mintemp + "</td>" \
                          "<td>" + day1avgtemp + "</td>" \
                          "<td>" + day1maxwind + "</td>" \
                          "<td>" + day1totalprecip + "</td>" \
                          "<td>" + day1avghumidity + "</td>" \
                          "<td>" + day1condition + "</td>" \
                          "<td><img src=\"" + day1icon + "\"/></td>" \
                          "<td>" + day1sunrise + "</td>" \
                          "<td>" + day1sunset + "</td>" \
                          "<td>" + day1moonrise + "</td>" \
                          "<td>" + day1moonset + "</td>" \
                          "</tr>"

            if days == two:

                try:
                    #print("2 days")
                    day2date = str(d["forecast"]["forecastday"][1]["date"])
                    day2maxtemp = str(d["forecast"]["forecastday"][1]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["maxtemp_f"]) + " F"
                    day2mintemp = str(d["forecast"]["forecastday"][1]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["mintemp_f"]) + " F"
                    day2avgtemp = str(d["forecast"]["forecastday"][1]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["avgtemp_f"]) + " F"
                    day2maxwind = str(d["forecast"]["forecastday"][1]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][1]["day"]["maxwind_kph"]) + " kph"
                    day2totalprecip = str(d["forecast"]["forecastday"][1]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][1]["day"]["totalprecip_in"]) + "in"
                    day2avghumidity = str(d["forecast"]["forecastday"][1]["day"]["avghumidity"])
                    day2condition = str(d["forecast"]["forecastday"][1]["day"]["condition"]["text"])
                    day2icon = str(d["forecast"]["forecastday"][1]["day"]["condition"]["icon"])
                    day2sunrise = str(d["forecast"]["forecastday"][1]["astro"]["sunrise"])
                    day2sunset = str(d["forecast"]["forecastday"][1]["astro"]["sunset"])
                    day2moonrise = str(d["forecast"]["forecastday"][1]["astro"]["moonrise"])
                    day2moonset = str(d["forecast"]["forecastday"][1]["astro"]["moonset"])
                except:
                    replyToChat = "Sorry, I am not able to get the weather, please try again later"
                    return dict(message="<messageML>" + str(replyToChat) + "</messageML>")

                table_body += "<tr><td>" + day2date + "</td><td>" + day2maxtemp + "</td><td>" + day2mintemp + "</td><td>" + day2avgtemp + "</td><td>" + day2maxwind + "</td><td>" + day2totalprecip + "</td><td>" + day2avghumidity + "</td><td>" + day2condition + "</td><td><img src=\"" + day2icon + "\"/></td><td>" + day2sunrise + "</td><td>" + day2sunset + "</td><td>" + day2moonrise + "</td><td>" + day2moonset + "</td></tr>"

            if days == three:

                try:
                    #print("2 days")
                    day2date = str(d["forecast"]["forecastday"][1]["date"])
                    day2maxtemp = str(d["forecast"]["forecastday"][1]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["maxtemp_f"]) + " F"
                    day2mintemp = str(d["forecast"]["forecastday"][1]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["mintemp_f"]) + " F"
                    day2avgtemp = str(d["forecast"]["forecastday"][1]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["avgtemp_f"]) + " F"
                    day2maxwind = str(d["forecast"]["forecastday"][1]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][1]["day"]["maxwind_kph"]) + " kph"
                    day2totalprecip = str(d["forecast"]["forecastday"][1]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][1]["day"]["totalprecip_in"]) + "in"
                    day2avghumidity = str(d["forecast"]["forecastday"][1]["day"]["avghumidity"])
                    day2condition = str(d["forecast"]["forecastday"][1]["day"]["condition"]["text"])
                    day2icon = str(d["forecast"]["forecastday"][1]["day"]["condition"]["icon"])
                    day2sunrise = str(d["forecast"]["forecastday"][1]["astro"]["sunrise"])
                    day2sunset = str(d["forecast"]["forecastday"][1]["astro"]["sunset"])
                    day2moonrise = str(d["forecast"]["forecastday"][1]["astro"]["moonrise"])
                    day2moonset = str(d["forecast"]["forecastday"][1]["astro"]["moonset"])
                except:
                    replyToChat = "Sorry, I am not able to get the weather, please try again later"
                    return dict(message="<messageML>" + str(replyToChat) + "</messageML>")

                table_body += "<tr><td>" + day2date + "</td><td>" + day2maxtemp + "</td><td>" + day2mintemp + "</td><td>" + day2avgtemp + "</td><td>" + day2maxwind + "</td><td>" + day2totalprecip + "</td><td>" + day2avghumidity + "</td><td>" + day2condition + "</td><td><img src=\"" + day2icon + "\"/></td><td>" + day2sunrise + "</td><td>" + day2sunset + "</td><td>" + day2moonrise + "</td><td>" + day2moonset + "</td></tr>"

                try:
                    #print("3 days")
                    day3date = str(d["forecast"]["forecastday"][2]["date"])
                    day3maxtemp = str(d["forecast"]["forecastday"][2]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["maxtemp_f"]) + " F"
                    day3mintemp = str(d["forecast"]["forecastday"][2]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["mintemp_f"]) + " F"
                    day3avgtemp = str(d["forecast"]["forecastday"][2]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["avgtemp_f"]) + " F"
                    day3maxwind = str(d["forecast"]["forecastday"][2]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][2]["day"]["maxwind_kph"]) + " kph"
                    day3totalprecip = str(d["forecast"]["forecastday"][2]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][2]["day"]["totalprecip_in"]) + "in"
                    day3avghumidity = str(d["forecast"]["forecastday"][2]["day"]["avghumidity"])
                    day3condition = str(d["forecast"]["forecastday"][2]["day"]["condition"]["text"])
                    day3icon = str(d["forecast"]["forecastday"][2]["day"]["condition"]["icon"])
                    day3sunrise = str(d["forecast"]["forecastday"][2]["astro"]["sunrise"])
                    day3sunset = str(d["forecast"]["forecastday"][2]["astro"]["sunset"])
                    day3moonrise = str(d["forecast"]["forecastday"][2]["astro"]["moonrise"])
                    day3moonset = str(d["forecast"]["forecastday"][2]["astro"]["moonset"])
                except:
                    replyToChat = "Sorry, I am not able to get the weather, please try again later"
                    return dict(message="<messageML>" + str(replyToChat) + "</messageML>")

                table_body += "<tr><td>" + day3date + "</td><td>" + day3maxtemp + "</td><td>" + day3mintemp + "</td><td>" + day3avgtemp + "</td><td>" + day3maxwind + "</td><td>" + day3totalprecip + "</td><td>" + day3avghumidity + "</td><td>" + day3condition + "</td><td><img src=\"" + day3icon + "\"/></td><td>" + day3sunrise + "</td><td>" + day3sunset + "</td><td>" + day3moonrise + "</td><td>" + day3moonset + "</td></tr>"


            if days == four:

                try:
                    #print("2 days")
                    day2date = str(d["forecast"]["forecastday"][1]["date"])
                    day2maxtemp = str(d["forecast"]["forecastday"][1]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["maxtemp_f"]) + " F"
                    day2mintemp = str(d["forecast"]["forecastday"][1]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["mintemp_f"]) + " F"
                    day2avgtemp = str(d["forecast"]["forecastday"][1]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["avgtemp_f"]) + " F"
                    day2maxwind = str(d["forecast"]["forecastday"][1]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][1]["day"]["maxwind_kph"]) + " kph"
                    day2totalprecip = str(d["forecast"]["forecastday"][1]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][1]["day"]["totalprecip_in"]) + "in"
                    day2avghumidity = str(d["forecast"]["forecastday"][1]["day"]["avghumidity"])
                    day2condition = str(d["forecast"]["forecastday"][1]["day"]["condition"]["text"])
                    day2icon = str(d["forecast"]["forecastday"][1]["day"]["condition"]["icon"])
                    day2sunrise = str(d["forecast"]["forecastday"][1]["astro"]["sunrise"])
                    day2sunset = str(d["forecast"]["forecastday"][1]["astro"]["sunset"])
                    day2moonrise = str(d["forecast"]["forecastday"][1]["astro"]["moonrise"])
                    day2moonset = str(d["forecast"]["forecastday"][1]["astro"]["moonset"])
                except:
                    replyToChat = "Sorry, I am not able to get the weather, please try again later"
                    return dict(message="<messageML>" + str(replyToChat) + "</messageML>")

                table_body += "<tr><td>" + day2date + "</td><td>" + day2maxtemp + "</td><td>" + day2mintemp + "</td><td>" + day2avgtemp + "</td><td>" + day2maxwind + "</td><td>" + day2totalprecip + "</td><td>" + day2avghumidity + "</td><td>" + day2condition + "</td><td><img src=\"" + day2icon + "\"/></td><td>" + day2sunrise + "</td><td>" + day2sunset + "</td><td>" + day2moonrise + "</td><td>" + day2moonset + "</td></tr>"

                try:
                    #print("3 days")
                    day3date = str(d["forecast"]["forecastday"][2]["date"])
                    day3maxtemp = str(d["forecast"]["forecastday"][2]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["maxtemp_f"]) + " F"
                    day3mintemp = str(d["forecast"]["forecastday"][2]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["mintemp_f"]) + " F"
                    day3avgtemp = str(d["forecast"]["forecastday"][2]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["avgtemp_f"]) + " F"
                    day3maxwind = str(d["forecast"]["forecastday"][2]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][2]["day"]["maxwind_kph"]) + " kph"
                    day3totalprecip = str(d["forecast"]["forecastday"][2]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][2]["day"]["totalprecip_in"]) + "in"
                    day3avghumidity = str(d["forecast"]["forecastday"][2]["day"]["avghumidity"])
                    day3condition = str(d["forecast"]["forecastday"][2]["day"]["condition"]["text"])
                    day3icon = str(d["forecast"]["forecastday"][2]["day"]["condition"]["icon"])
                    day3sunrise = str(d["forecast"]["forecastday"][2]["astro"]["sunrise"])
                    day3sunset = str(d["forecast"]["forecastday"][2]["astro"]["sunset"])
                    day3moonrise = str(d["forecast"]["forecastday"][2]["astro"]["moonrise"])
                    day3moonset = str(d["forecast"]["forecastday"][2]["astro"]["moonset"])
                except:
                    replyToChat = "Sorry, I am not able to get the weather, please try again later"
                    return dict(message="<messageML>" + str(replyToChat) + "</messageML>")

                table_body += "<tr><td>" + day3date + "</td><td>" + day3maxtemp + "</td><td>" + day3mintemp + "</td><td>" + day3avgtemp + "</td><td>" + day3maxwind + "</td><td>" + day3totalprecip + "</td><td>" + day3avghumidity + "</td><td>" + day3condition + "</td><td><img src=\"" + day3icon + "\"/></td><td>" + day3sunrise + "</td><td>" + day3sunset + "</td><td>" + day3moonrise + "</td><td>" + day3moonset + "</td></tr>"

                try:
                    #print("4 days")
                    day4date = str(d["forecast"]["forecastday"][3]["date"])
                    day4maxtemp = str(d["forecast"]["forecastday"][3]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][3]["day"]["maxtemp_f"]) + " F"
                    day4mintemp = str(d["forecast"]["forecastday"][3]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][3]["day"]["mintemp_f"]) + " F"
                    day4avgtemp = str(d["forecast"]["forecastday"][3]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][3]["day"]["avgtemp_f"]) + " F"
                    day4maxwind = str(d["forecast"]["forecastday"][3]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][3]["day"]["maxwind_kph"]) + " kph"
                    day4totalprecip = str(d["forecast"]["forecastday"][3]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][3]["day"]["totalprecip_in"]) + "in"
                    day4avghumidity = str(d["forecast"]["forecastday"][3]["day"]["avghumidity"])
                    day4condition = str(d["forecast"]["forecastday"][3]["day"]["condition"]["text"])
                    day4icon = str(d["forecast"]["forecastday"][3]["day"]["condition"]["icon"])
                    day4sunrise = str(d["forecast"]["forecastday"][3]["astro"]["sunrise"])
                    day4sunset = str(d["forecast"]["forecastday"][3]["astro"]["sunset"])
                    day4moonrise = str(d["forecast"]["forecastday"][3]["astro"]["moonrise"])
                    day4moonset = str(d["forecast"]["forecastday"][3]["astro"]["moonset"])
                except:
                    replyToChat = "Sorry, I am not able to get the weather, please try again later"
                    return dict(message="<messageML>" + str(replyToChat) + "</messageML>")

                table_body += "<tr><td>" + day4date + "</td><td>" + day4maxtemp + "</td><td>" + day4mintemp + "</td><td>" + day4avgtemp + "</td><td>" + day4maxwind + "</td><td>" + day4totalprecip + "</td><td>" + day4avghumidity + "</td><td>" + day4condition + "</td><td><img src=\"" + day4icon + "\"/></td><td>" + day4sunrise + "</td><td>" + day4sunset + "</td><td>" + day4moonrise + "</td><td>" + day4moonset + "</td></tr>"

            if days == five:
                try:
                    #print("2 days")
                    day2date = str(d["forecast"]["forecastday"][1]["date"])
                    day2maxtemp = str(d["forecast"]["forecastday"][1]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["maxtemp_f"]) + " F"
                    day2mintemp = str(d["forecast"]["forecastday"][1]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["mintemp_f"]) + " F"
                    day2avgtemp = str(d["forecast"]["forecastday"][1]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["avgtemp_f"]) + " F"
                    day2maxwind = str(d["forecast"]["forecastday"][1]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][1]["day"]["maxwind_kph"]) + " kph"
                    day2totalprecip = str(d["forecast"]["forecastday"][1]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][1]["day"]["totalprecip_in"]) + "in"
                    day2avghumidity = str(d["forecast"]["forecastday"][1]["day"]["avghumidity"])
                    day2condition = str(d["forecast"]["forecastday"][1]["day"]["condition"]["text"])
                    day2icon = str(d["forecast"]["forecastday"][1]["day"]["condition"]["icon"])
                    day2sunrise = str(d["forecast"]["forecastday"][1]["astro"]["sunrise"])
                    day2sunset = str(d["forecast"]["forecastday"][1]["astro"]["sunset"])
                    day2moonrise = str(d["forecast"]["forecastday"][1]["astro"]["moonrise"])
                    day2moonset = str(d["forecast"]["forecastday"][1]["astro"]["moonset"])
                except:
                    replyToChat = "Sorry, I am not able to get the weather, please try again later"
                    return dict(message="<messageML>" + str(replyToChat) + "</messageML>")

                table_body += "<tr><td>" + day2date + "</td><td>" + day2maxtemp + "</td><td>" + day2mintemp + "</td><td>" + day2avgtemp + "</td><td>" + day2maxwind + "</td><td>" + day2totalprecip + "</td><td>" + day2avghumidity + "</td><td>" + day2condition + "</td><td><img src=\"" + day2icon + "\"/></td><td>" + day2sunrise + "</td><td>" + day2sunset + "</td><td>" + day2moonrise + "</td><td>" + day2moonset + "</td></tr>"

                try:
                    #print("3 days")
                    day3date = str(d["forecast"]["forecastday"][2]["date"])
                    day3maxtemp = str(d["forecast"]["forecastday"][2]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["maxtemp_f"]) + " F"
                    day3mintemp = str(d["forecast"]["forecastday"][2]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["mintemp_f"]) + " F"
                    day3avgtemp = str(d["forecast"]["forecastday"][2]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["avgtemp_f"]) + " F"
                    day3maxwind = str(d["forecast"]["forecastday"][2]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][2]["day"]["maxwind_kph"]) + " kph"
                    day3totalprecip = str(d["forecast"]["forecastday"][2]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][2]["day"]["totalprecip_in"]) + "in"
                    day3avghumidity = str(d["forecast"]["forecastday"][2]["day"]["avghumidity"])
                    day3condition = str(d["forecast"]["forecastday"][2]["day"]["condition"]["text"])
                    day3icon = str(d["forecast"]["forecastday"][2]["day"]["condition"]["icon"])
                    day3sunrise = str(d["forecast"]["forecastday"][2]["astro"]["sunrise"])
                    day3sunset = str(d["forecast"]["forecastday"][2]["astro"]["sunset"])
                    day3moonrise = str(d["forecast"]["forecastday"][2]["astro"]["moonrise"])
                    day3moonset = str(d["forecast"]["forecastday"][2]["astro"]["moonset"])
                except:
                    replyToChat = "Sorry, I am not able to get the weather, please try again later"
                    return dict(message="<messageML>" + str(replyToChat) + "</messageML>")

                table_body += "<tr><td>" + day3date + "</td><td>" + day3maxtemp + "</td><td>" + day3mintemp + "</td><td>" + day3avgtemp + "</td><td>" + day3maxwind + "</td><td>" + day3totalprecip + "</td><td>" + day3avghumidity + "</td><td>" + day3condition + "</td><td><img src=\"" + day3icon + "\"/></td><td>" + day3sunrise + "</td><td>" + day3sunset + "</td><td>" + day3moonrise + "</td><td>" + day3moonset + "</td></tr>"

                try:
                    #print("4 days")
                    day4date = str(d["forecast"]["forecastday"][3]["date"])
                    day4maxtemp = str(d["forecast"]["forecastday"][3]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][3]["day"]["maxtemp_f"]) + " F"
                    day4mintemp = str(d["forecast"]["forecastday"][3]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][3]["day"]["mintemp_f"]) + " F"
                    day4avgtemp = str(d["forecast"]["forecastday"][3]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][3]["day"]["avgtemp_f"]) + " F"
                    day4maxwind = str(d["forecast"]["forecastday"][3]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][3]["day"]["maxwind_kph"]) + " kph"
                    day4totalprecip = str(d["forecast"]["forecastday"][3]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][3]["day"]["totalprecip_in"]) + "in"
                    day4avghumidity = str(d["forecast"]["forecastday"][3]["day"]["avghumidity"])
                    day4condition = str(d["forecast"]["forecastday"][3]["day"]["condition"]["text"])
                    day4icon = str(d["forecast"]["forecastday"][3]["day"]["condition"]["icon"])
                    day4sunrise = str(d["forecast"]["forecastday"][3]["astro"]["sunrise"])
                    day4sunset = str(d["forecast"]["forecastday"][3]["astro"]["sunset"])
                    day4moonrise = str(d["forecast"]["forecastday"][3]["astro"]["moonrise"])
                    day4moonset = str(d["forecast"]["forecastday"][3]["astro"]["moonset"])
                except:
                    replyToChat = "Sorry, I am not able to get the weather, please try again later"
                    return dict(message="<messageML>" + str(replyToChat) + "</messageML>")

                table_body += "<tr><td>" + day4date + "</td><td>" + day4maxtemp + "</td><td>" + day4mintemp + "</td><td>" + day4avgtemp + "</td><td>" + day4maxwind + "</td><td>" + day4totalprecip + "</td><td>" + day4avghumidity + "</td><td>" + day4condition + "</td><td><img src=\"" + day4icon + "\"/></td><td>" + day4sunrise + "</td><td>" + day4sunset + "</td><td>" + day4moonrise + "</td><td>" + day4moonset + "</td></tr>"

                try:
                    #print("5 days")
                    day5date = str(d["forecast"]["forecastday"][4]["date"])
                    day5maxtemp = str(d["forecast"]["forecastday"][4]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][4]["day"]["maxtemp_f"]) + " F"
                    day5mintemp = str(d["forecast"]["forecastday"][4]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][4]["day"]["mintemp_f"]) + " F"
                    day5avgtemp = str(d["forecast"]["forecastday"][4]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][4]["day"]["avgtemp_f"]) + " F"
                    day5maxwind = str(d["forecast"]["forecastday"][4]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][4]["day"]["maxwind_kph"]) + " kph"
                    day5totalprecip = str(d["forecast"]["forecastday"][4]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][4]["day"]["totalprecip_in"]) + "in"
                    day5avghumidity = str(d["forecast"]["forecastday"][4]["day"]["avghumidity"])
                    day5condition = str(d["forecast"]["forecastday"][4]["day"]["condition"]["text"])
                    day5icon = str(d["forecast"]["forecastday"][4]["day"]["condition"]["icon"])
                    day5sunrise = str(d["forecast"]["forecastday"][4]["astro"]["sunrise"])
                    day5sunset = str(d["forecast"]["forecastday"][4]["astro"]["sunset"])
                    day5moonrise = str(d["forecast"]["forecastday"][4]["astro"]["moonrise"])
                    day5moonset = str(d["forecast"]["forecastday"][4]["astro"]["moonset"])
                except:
                    replyToChat = "Sorry, I am not able to get the weather, please try again later"
                    return dict(message="<messageML>" + str(replyToChat) + "</messageML>")

                table_body += "<tr><td>" + day5date + "</td><td>" + day5maxtemp + "</td><td>" + day5mintemp + "</td><td>" + day5avgtemp + "</td><td>" + day5maxwind + "</td><td>" + day5totalprecip + "</td><td>" + day5avghumidity + "</td><td>" + day5condition + "</td><td><img src=\"" + day5icon + "\"/></td><td>" + day5sunrise + "</td><td>" + day5sunset + "</td><td>" + day5moonrise + "</td><td>" + day5moonset + "</td></tr>"

            if days == six:

                try:
                    #print("2 days")
                    day2date = str(d["forecast"]["forecastday"][1]["date"])
                    day2maxtemp = str(d["forecast"]["forecastday"][1]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["maxtemp_f"]) + " F"
                    day2mintemp = str(d["forecast"]["forecastday"][1]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["mintemp_f"]) + " F"
                    day2avgtemp = str(d["forecast"]["forecastday"][1]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["avgtemp_f"]) + " F"
                    day2maxwind = str(d["forecast"]["forecastday"][1]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][1]["day"]["maxwind_kph"]) + " kph"
                    day2totalprecip = str(d["forecast"]["forecastday"][1]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][1]["day"]["totalprecip_in"]) + "in"
                    day2avghumidity = str(d["forecast"]["forecastday"][1]["day"]["avghumidity"])
                    day2condition = str(d["forecast"]["forecastday"][1]["day"]["condition"]["text"])
                    day2icon = str(d["forecast"]["forecastday"][1]["day"]["condition"]["icon"])
                    day2sunrise = str(d["forecast"]["forecastday"][1]["astro"]["sunrise"])
                    day2sunset = str(d["forecast"]["forecastday"][1]["astro"]["sunset"])
                    day2moonrise = str(d["forecast"]["forecastday"][1]["astro"]["moonrise"])
                    day2moonset = str(d["forecast"]["forecastday"][1]["astro"]["moonset"])
                except:
                    replyToChat = "Sorry, I am not able to get the weather, please try again later"
                    return dict(message="<messageML>" + str(replyToChat) + "</messageML>")

                table_body += "<tr><td>" + day2date + "</td><td>" + day2maxtemp + "</td><td>" + day2mintemp + "</td><td>" + day2avgtemp + "</td><td>" + day2maxwind + "</td><td>" + day2totalprecip + "</td><td>" + day2avghumidity + "</td><td>" + day2condition + "</td><td><img src=\"" + day2icon + "\"/></td><td>" + day2sunrise + "</td><td>" + day2sunset + "</td><td>" + day2moonrise + "</td><td>" + day2moonset + "</td></tr>"

                try:
                    #print("3 days")
                    day3date = str(d["forecast"]["forecastday"][2]["date"])
                    day3maxtemp = str(d["forecast"]["forecastday"][2]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["maxtemp_f"]) + " F"
                    day3mintemp = str(d["forecast"]["forecastday"][2]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["mintemp_f"]) + " F"
                    day3avgtemp = str(d["forecast"]["forecastday"][2]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["avgtemp_f"]) + " F"
                    day3maxwind = str(d["forecast"]["forecastday"][2]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][2]["day"]["maxwind_kph"]) + " kph"
                    day3totalprecip = str(d["forecast"]["forecastday"][2]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][2]["day"]["totalprecip_in"]) + "in"
                    day3avghumidity = str(d["forecast"]["forecastday"][2]["day"]["avghumidity"])
                    day3condition = str(d["forecast"]["forecastday"][2]["day"]["condition"]["text"])
                    day3icon = str(d["forecast"]["forecastday"][2]["day"]["condition"]["icon"])
                    day3sunrise = str(d["forecast"]["forecastday"][2]["astro"]["sunrise"])
                    day3sunset = str(d["forecast"]["forecastday"][2]["astro"]["sunset"])
                    day3moonrise = str(d["forecast"]["forecastday"][2]["astro"]["moonrise"])
                    day3moonset = str(d["forecast"]["forecastday"][2]["astro"]["moonset"])
                except:
                    replyToChat = "Sorry, I am not able to get the weather, please try again later"
                    return dict(message="<messageML>" + str(replyToChat) + "</messageML>")

                table_body += "<tr><td>" + day3date + "</td><td>" + day3maxtemp + "</td><td>" + day3mintemp + "</td><td>" + day3avgtemp + "</td><td>" + day3maxwind + "</td><td>" + day3totalprecip + "</td><td>" + day3avghumidity + "</td><td>" + day3condition + "</td><td><img src=\"" + day3icon + "\"/></td><td>" + day3sunrise + "</td><td>" + day3sunset + "</td><td>" + day3moonrise + "</td><td>" + day3moonset + "</td></tr>"

                try:
                    #print("4 days")
                    day4date = str(d["forecast"]["forecastday"][3]["date"])
                    day4maxtemp = str(d["forecast"]["forecastday"][3]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][3]["day"]["maxtemp_f"]) + " F"
                    day4mintemp = str(d["forecast"]["forecastday"][3]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][3]["day"]["mintemp_f"]) + " F"
                    day4avgtemp = str(d["forecast"]["forecastday"][3]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][3]["day"]["avgtemp_f"]) + " F"
                    day4maxwind = str(d["forecast"]["forecastday"][3]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][3]["day"]["maxwind_kph"]) + " kph"
                    day4totalprecip = str(d["forecast"]["forecastday"][3]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][3]["day"]["totalprecip_in"]) + "in"
                    day4avghumidity = str(d["forecast"]["forecastday"][3]["day"]["avghumidity"])
                    day4condition = str(d["forecast"]["forecastday"][3]["day"]["condition"]["text"])
                    day4icon = str(d["forecast"]["forecastday"][3]["day"]["condition"]["icon"])
                    day4sunrise = str(d["forecast"]["forecastday"][3]["astro"]["sunrise"])
                    day4sunset = str(d["forecast"]["forecastday"][3]["astro"]["sunset"])
                    day4moonrise = str(d["forecast"]["forecastday"][3]["astro"]["moonrise"])
                    day4moonset = str(d["forecast"]["forecastday"][3]["astro"]["moonset"])
                except:
                    replyToChat = "Sorry, I am not able to get the weather, please try again later"
                    return dict(message="<messageML>" + str(replyToChat) + "</messageML>")

                table_body += "<tr><td>" + day4date + "</td><td>" + day4maxtemp + "</td><td>" + day4mintemp + "</td><td>" + day4avgtemp + "</td><td>" + day4maxwind + "</td><td>" + day4totalprecip + "</td><td>" + day4avghumidity + "</td><td>" + day4condition + "</td><td><img src=\"" + day4icon + "\"/></td><td>" + day4sunrise + "</td><td>" + day4sunset + "</td><td>" + day4moonrise + "</td><td>" + day4moonset + "</td></tr>"

                try:
                    #print("5 days")
                    day5date = str(d["forecast"]["forecastday"][4]["date"])
                    day5maxtemp = str(d["forecast"]["forecastday"][4]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][4]["day"]["maxtemp_f"]) + " F"
                    day5mintemp = str(d["forecast"]["forecastday"][4]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][4]["day"]["mintemp_f"]) + " F"
                    day5avgtemp = str(d["forecast"]["forecastday"][4]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][4]["day"]["avgtemp_f"]) + " F"
                    day5maxwind = str(d["forecast"]["forecastday"][4]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][4]["day"]["maxwind_kph"]) + " kph"
                    day5totalprecip = str(d["forecast"]["forecastday"][4]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][4]["day"]["totalprecip_in"]) + "in"
                    day5avghumidity = str(d["forecast"]["forecastday"][4]["day"]["avghumidity"])
                    day5condition = str(d["forecast"]["forecastday"][4]["day"]["condition"]["text"])
                    day5icon = str(d["forecast"]["forecastday"][4]["day"]["condition"]["icon"])
                    day5sunrise = str(d["forecast"]["forecastday"][4]["astro"]["sunrise"])
                    day5sunset = str(d["forecast"]["forecastday"][4]["astro"]["sunset"])
                    day5moonrise = str(d["forecast"]["forecastday"][4]["astro"]["moonrise"])
                    day5moonset = str(d["forecast"]["forecastday"][4]["astro"]["moonset"])
                except:
                    replyToChat = "Sorry, I am not able to get the weather, please try again later"
                    return dict(message="<messageML>" + str(replyToChat) + "</messageML>")

                table_body += "<tr><td>" + day5date + "</td><td>" + day5maxtemp + "</td><td>" + day5mintemp + "</td><td>" + day5avgtemp + "</td><td>" + day5maxwind + "</td><td>" + day5totalprecip + "</td><td>" + day5avghumidity + "</td><td>" + day5condition + "</td><td><img src=\"" + day5icon + "\"/></td><td>" + day5sunrise + "</td><td>" + day5sunset + "</td><td>" + day5moonrise + "</td><td>" + day5moonset + "</td></tr>"

                try:
                    #print("6 days")
                    day6date = str(d["forecast"]["forecastday"][5]["date"])
                    day6maxtemp = str(d["forecast"]["forecastday"][5]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][5]["day"]["maxtemp_f"]) + " F"
                    day6mintemp = str(d["forecast"]["forecastday"][5]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][5]["day"]["mintemp_f"]) + " F"
                    day6avgtemp = str(d["forecast"]["forecastday"][5]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][5]["day"]["avgtemp_f"]) + " F"
                    day6maxwind = str(d["forecast"]["forecastday"][5]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][5]["day"]["maxwind_kph"]) + " kph"
                    day6totalprecip = str(d["forecast"]["forecastday"][5]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][5]["day"]["totalprecip_in"]) + "in"
                    day6avghumidity = str(d["forecast"]["forecastday"][5]["day"]["avghumidity"])
                    day6condition = str(d["forecast"]["forecastday"][5]["day"]["condition"]["text"])
                    day6icon = str(d["forecast"]["forecastday"][5]["day"]["condition"]["icon"])
                    day6sunrise = str(d["forecast"]["forecastday"][5]["astro"]["sunrise"])
                    day6sunset = str(d["forecast"]["forecastday"][5]["astro"]["sunset"])
                    day6moonrise = str(d["forecast"]["forecastday"][5]["astro"]["moonrise"])
                    day6moonset = str(d["forecast"]["forecastday"][5]["astro"]["moonset"])
                except:
                    replyToChat = "Sorry, I am not able to get the weather, please try again later"
                    return dict(message="<messageML>" + str(replyToChat) + "</messageML>")

                table_body += "<tr><td>" + day6date + "</td><td>" + day6maxtemp + "</td><td>" + day6mintemp + "</td><td>" + day6avgtemp + "</td><td>" + day6maxwind + "</td><td>" + day6totalprecip + "</td><td>" + day6avghumidity + "</td><td>" + day6condition + "</td><td><img src=\"" + day6icon + "\"/></td><td>" + day6sunrise + "</td><td>" + day6sunset + "</td><td>" + day6moonrise + "</td><td>" + day6moonset + "</td></tr>"


            if days == seven:

                try:
                    #print("2 days")
                    day2date = str(d["forecast"]["forecastday"][1]["date"])
                    day2maxtemp = str(d["forecast"]["forecastday"][1]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["maxtemp_f"]) + " F"
                    day2mintemp = str(d["forecast"]["forecastday"][1]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["mintemp_f"]) + " F"
                    day2avgtemp = str(d["forecast"]["forecastday"][1]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["avgtemp_f"]) + " F"
                    day2maxwind = str(d["forecast"]["forecastday"][1]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][1]["day"]["maxwind_kph"]) + " kph"
                    day2totalprecip = str(d["forecast"]["forecastday"][1]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][1]["day"]["totalprecip_in"]) + "in"
                    day2avghumidity = str(d["forecast"]["forecastday"][1]["day"]["avghumidity"])
                    day2condition = str(d["forecast"]["forecastday"][1]["day"]["condition"]["text"])
                    day2icon = str(d["forecast"]["forecastday"][1]["day"]["condition"]["icon"])
                    day2sunrise = str(d["forecast"]["forecastday"][1]["astro"]["sunrise"])
                    day2sunset = str(d["forecast"]["forecastday"][1]["astro"]["sunset"])
                    day2moonrise = str(d["forecast"]["forecastday"][1]["astro"]["moonrise"])
                    day2moonset = str(d["forecast"]["forecastday"][1]["astro"]["moonset"])
                except:
                    replyToChat = "Sorry, I am not able to get the weather, please try again later"
                    return dict(message="<messageML>" + str(replyToChat) + "</messageML>")

                table_body += "<tr><td>" + day2date + "</td><td>" + day2maxtemp + "</td><td>" + day2mintemp + "</td><td>" + day2avgtemp + "</td><td>" + day2maxwind + "</td><td>" + day2totalprecip + "</td><td>" + day2avghumidity + "</td><td>" + day2condition + "</td><td><img src=\"" + day2icon + "\"/></td><td>" + day2sunrise + "</td><td>" + day2sunset + "</td><td>" + day2moonrise + "</td><td>" + day2moonset + "</td></tr>"

                try:
                    #print("3 days")
                    day3date = str(d["forecast"]["forecastday"][2]["date"])
                    day3maxtemp = str(d["forecast"]["forecastday"][2]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["maxtemp_f"]) + " F"
                    day3mintemp = str(d["forecast"]["forecastday"][2]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["mintemp_f"]) + " F"
                    day3avgtemp = str(d["forecast"]["forecastday"][2]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["avgtemp_f"]) + " F"
                    day3maxwind = str(d["forecast"]["forecastday"][2]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][2]["day"]["maxwind_kph"]) + " kph"
                    day3totalprecip = str(d["forecast"]["forecastday"][2]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][2]["day"]["totalprecip_in"]) + "in"
                    day3avghumidity = str(d["forecast"]["forecastday"][2]["day"]["avghumidity"])
                    day3condition = str(d["forecast"]["forecastday"][2]["day"]["condition"]["text"])
                    day3icon = str(d["forecast"]["forecastday"][2]["day"]["condition"]["icon"])
                    day3sunrise = str(d["forecast"]["forecastday"][2]["astro"]["sunrise"])
                    day3sunset = str(d["forecast"]["forecastday"][2]["astro"]["sunset"])
                    day3moonrise = str(d["forecast"]["forecastday"][2]["astro"]["moonrise"])
                    day3moonset = str(d["forecast"]["forecastday"][2]["astro"]["moonset"])
                except:
                    replyToChat = "Sorry, I am not able to get the weather, please try again later"
                    return dict(message="<messageML>" + str(replyToChat) + "</messageML>")

                table_body += "<tr><td>" + day3date + "</td><td>" + day3maxtemp + "</td><td>" + day3mintemp + "</td><td>" + day3avgtemp + "</td><td>" + day3maxwind + "</td><td>" + day3totalprecip + "</td><td>" + day3avghumidity + "</td><td>" + day3condition + "</td><td><img src=\"" + day3icon + "\"/></td><td>" + day3sunrise + "</td><td>" + day3sunset + "</td><td>" + day3moonrise + "</td><td>" + day3moonset + "</td></tr>"

                try:
                    #print("4 days")
                    day4date = str(d["forecast"]["forecastday"][3]["date"])
                    day4maxtemp = str(d["forecast"]["forecastday"][3]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][3]["day"]["maxtemp_f"]) + " F"
                    day4mintemp = str(d["forecast"]["forecastday"][3]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][3]["day"]["mintemp_f"]) + " F"
                    day4avgtemp = str(d["forecast"]["forecastday"][3]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][3]["day"]["avgtemp_f"]) + " F"
                    day4maxwind = str(d["forecast"]["forecastday"][3]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][3]["day"]["maxwind_kph"]) + " kph"
                    day4totalprecip = str(d["forecast"]["forecastday"][3]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][3]["day"]["totalprecip_in"]) + "in"
                    day4avghumidity = str(d["forecast"]["forecastday"][3]["day"]["avghumidity"])
                    day4condition = str(d["forecast"]["forecastday"][3]["day"]["condition"]["text"])
                    day4icon = str(d["forecast"]["forecastday"][3]["day"]["condition"]["icon"])
                    day4sunrise = str(d["forecast"]["forecastday"][3]["astro"]["sunrise"])
                    day4sunset = str(d["forecast"]["forecastday"][3]["astro"]["sunset"])
                    day4moonrise = str(d["forecast"]["forecastday"][3]["astro"]["moonrise"])
                    day4moonset = str(d["forecast"]["forecastday"][3]["astro"]["moonset"])
                except:
                    replyToChat = "Sorry, I am not able to get the weather, please try again later"
                    return dict(message="<messageML>" + str(replyToChat) + "</messageML>")

                table_body += "<tr><td>" + day4date + "</td><td>" + day4maxtemp + "</td><td>" + day4mintemp + "</td><td>" + day4avgtemp + "</td><td>" + day4maxwind + "</td><td>" + day4totalprecip + "</td><td>" + day4avghumidity + "</td><td>" + day4condition + "</td><td><img src=\"" + day4icon + "\"/></td><td>" + day4sunrise + "</td><td>" + day4sunset + "</td><td>" + day4moonrise + "</td><td>" + day4moonset + "</td></tr>"

                try:
                    #print("5 days")
                    day5date = str(d["forecast"]["forecastday"][4]["date"])
                    day5maxtemp = str(d["forecast"]["forecastday"][4]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][4]["day"]["maxtemp_f"]) + " F"
                    day5mintemp = str(d["forecast"]["forecastday"][4]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][4]["day"]["mintemp_f"]) + " F"
                    day5avgtemp = str(d["forecast"]["forecastday"][4]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][4]["day"]["avgtemp_f"]) + " F"
                    day5maxwind = str(d["forecast"]["forecastday"][4]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][4]["day"]["maxwind_kph"]) + " kph"
                    day5totalprecip = str(d["forecast"]["forecastday"][4]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][4]["day"]["totalprecip_in"]) + "in"
                    day5avghumidity = str(d["forecast"]["forecastday"][4]["day"]["avghumidity"])
                    day5condition = str(d["forecast"]["forecastday"][4]["day"]["condition"]["text"])
                    day5icon = str(d["forecast"]["forecastday"][4]["day"]["condition"]["icon"])
                    day5sunrise = str(d["forecast"]["forecastday"][4]["astro"]["sunrise"])
                    day5sunset = str(d["forecast"]["forecastday"][4]["astro"]["sunset"])
                    day5moonrise = str(d["forecast"]["forecastday"][4]["astro"]["moonrise"])
                    day5moonset = str(d["forecast"]["forecastday"][4]["astro"]["moonset"])
                except:
                    replyToChat = "Sorry, I am not able to get the weather, please try again later"
                    return dict(message="<messageML>" + str(replyToChat) + "</messageML>")

                table_body += "<tr><td>" + day5date + "</td><td>" + day5maxtemp + "</td><td>" + day5mintemp + "</td><td>" + day5avgtemp + "</td><td>" + day5maxwind + "</td><td>" + day5totalprecip + "</td><td>" + day5avghumidity + "</td><td>" + day5condition + "</td><td><img src=\"" + day5icon + "\"/></td><td>" + day5sunrise + "</td><td>" + day5sunset + "</td><td>" + day5moonrise + "</td><td>" + day5moonset + "</td></tr>"

                try:
                    #print("6 days")
                    day6date = str(d["forecast"]["forecastday"][5]["date"])
                    day6maxtemp = str(d["forecast"]["forecastday"][5]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][5]["day"]["maxtemp_f"]) + " F"
                    day6mintemp = str(d["forecast"]["forecastday"][5]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][5]["day"]["mintemp_f"]) + " F"
                    day6avgtemp = str(d["forecast"]["forecastday"][5]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][5]["day"]["avgtemp_f"]) + " F"
                    day6maxwind = str(d["forecast"]["forecastday"][5]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][5]["day"]["maxwind_kph"]) + " kph"
                    day6totalprecip = str(d["forecast"]["forecastday"][5]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][5]["day"]["totalprecip_in"]) + "in"
                    day6avghumidity = str(d["forecast"]["forecastday"][5]["day"]["avghumidity"])
                    day6condition = str(d["forecast"]["forecastday"][5]["day"]["condition"]["text"])
                    day6icon = str(d["forecast"]["forecastday"][5]["day"]["condition"]["icon"])
                    day6sunrise = str(d["forecast"]["forecastday"][5]["astro"]["sunrise"])
                    day6sunset = str(d["forecast"]["forecastday"][5]["astro"]["sunset"])
                    day6moonrise = str(d["forecast"]["forecastday"][5]["astro"]["moonrise"])
                    day6moonset = str(d["forecast"]["forecastday"][5]["astro"]["moonset"])
                except:
                    replyToChat = "Sorry, I am not able to get the weather, please try again later"
                    return dict(message="<messageML>" + str(replyToChat) + "</messageML>")

                table_body += "<tr><td>" + day6date + "</td><td>" + day6maxtemp + "</td><td>" + day6mintemp + "</td><td>" + day6avgtemp + "</td><td>" + day6maxwind + "</td><td>" + day6totalprecip + "</td><td>" + day6avghumidity + "</td><td>" + day6condition + "</td><td><img src=\"" + day6icon + "\"/></td><td>" + day6sunrise + "</td><td>" + day6sunset + "</td><td>" + day6moonrise + "</td><td>" + day6moonset + "</td></tr>"

                try:
                    #print("7 days")
                    day7date = str(d["forecast"]["forecastday"][6]["date"])
                    day7maxtemp = str(d["forecast"]["forecastday"][6]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][6]["day"]["maxtemp_f"]) + " F"
                    day7mintemp = str(d["forecast"]["forecastday"][6]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][6]["day"]["mintemp_f"]) + " F"
                    day7avgtemp = str(d["forecast"]["forecastday"][6]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][6]["day"]["avgtemp_f"]) + " F"
                    day7maxwind = str(d["forecast"]["forecastday"][6]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][6]["day"]["maxwind_kph"]) + " kph"
                    day7totalprecip = str(d["forecast"]["forecastday"][6]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][6]["day"]["totalprecip_in"]) + "in"
                    day7avghumidity = str(d["forecast"]["forecastday"][6]["day"]["avghumidity"])
                    day7condition = str(d["forecast"]["forecastday"][6]["day"]["condition"]["text"])
                    day7icon = str(d["forecast"]["forecastday"][6]["day"]["condition"]["icon"])
                    day7sunrise = str(d["forecast"]["forecastday"][6]["astro"]["sunrise"])
                    day7sunset = str(d["forecast"]["forecastday"][6]["astro"]["sunset"])
                    day7moonrise = str(d["forecast"]["forecastday"][6]["astro"]["moonrise"])
                    day7moonset = str(d["forecast"]["forecastday"][6]["astro"]["moonset"])
                except:
                    replyToChat = "Sorry, I am not able to get the weather, please try again later"
                    return dict(message="<messageML>" + str(replyToChat) + "</messageML>")

                table_body += "<tr><td>" + day7date + "</td><td>" + day7maxtemp + "</td><td>" + day7mintemp + "</td><td>" + day7avgtemp + "</td><td>" + day7maxwind + "</td><td>" + day7totalprecip + "</td><td>" + day7avghumidity + "</td><td>" + day7condition + "</td><td><img src=\"" + day7icon + "\"/></td><td>" + day7sunrise + "</td><td>" + day7sunset + "</td><td>" + day7moonrise + "</td><td>" + day7moonset + "</td></tr>"

            table_body += "</tbody></table>"

            #return messageDetail.ReplyToChatV2_noBotLog("<card iconSrc=\"https://thumb.ibb.co/csXBgU/Symphony2018_App_Icon_Mobile.png\" accent=\"tempo-bg-color--blue\"><header>The current condition in " + LocationName + ", " + Region + ", " + Country + " as of " + LastUpdated + " is " + Condition + ", <img src=\"" + CurrentURL + "\"/> (" + TempC + " C / " + TempF + " F)<br/></header><body>" + table_body + "</body></card>")
            replyToChat = "<card iconSrc=\"\" accent=\"tempo-bg-color--blue\"><header>The current condition in " + LocationName + ", " + Region + ", " + Country + " as of " + LastUpdated + " is " + Condition + ", <img src=\"" + CurrentURL + "\"/> (" + TempC + " C / " + TempF + " F)<br/></header><body>" + table_body + "</body></card>"
            return dict(message="<messageML>" + str(replyToChat) + "</messageML>")