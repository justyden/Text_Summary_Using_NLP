from nrclex import NRCLex
import re

from SentimentAnalysis import SentimentAnalysis
from TextSummary import TextSummary


class Helper:

    def __init__(self):
        self.textSummarizer = TextSummary()
        self.sentimentAnalyzer = SentimentAnalysis()
        self.num_of_top_emotions = 3

    def find_top_emotion(self, sentences, alt=False):
        emotion_count = {
            'fear': 0,
            'anger': 0,
            'anticip': 0,
            'trust': 0,
            'surprise': 0,
            'positive': 0,
            'negative': 0,
            'sadness': 0,
            'disgust': 0,
            'joy': 0,
            'anticipation': 0
        }
        emotion_dict = {
            'fear': [],
            'anger': [],
            'trust': [],
            'surprise': [],
            'positive': [],
            'negative': [],
            'sadness': [],
            'disgust': [],
            'joy': [],
            'anticipation': []
        }

        if alt:
            for count, sentence in enumerate(sentences):
                emotion_detect = NRCLex(sentence.lower())
                affect_dict = emotion_detect.affect_dict
                for word in list(affect_dict):
                    for emotion in affect_dict[word]:
                        emotion_dict[emotion].append((word, count))

            return emotion_dict
        else:
            for sentence in sentences:
                emotion_detect = NRCLex(sentence.lower())
                raw_scores = emotion_detect.raw_emotion_scores
                for emotion in list(raw_scores.keys()):
                    emotion_count[emotion] = emotion_count[emotion] + raw_scores[emotion]

            return max(emotion_count, key=emotion_count.get)


    def has_chars(self,text):

        for index in text:
            if text != ' ':
                return True
        return False

    def filter_tweets(self, tweets):
        clean_tweets = []
        for tweet in tweets:
            clean_tweet = ""
            remove = False
            for letter in tweet:
                if remove:
                    if letter == " ":
                        remove = False
                elif letter == "@" or letter == "#":
                    remove = True
                elif not remove:
                    clean_tweet = clean_tweet + letter

            # remove urls
            # str_parts = clean_tweet.split("http:/")
            str_parts = re.split(r'http:/|https:/', clean_tweet)

            new_str = ""
            for x in str_parts:
                if len(x) > 0:
                    to_add = x
                    if x[0] == "/":
                        start = x.find(' ')
                        if start == -1:
                            to_add = ''
                        else:
                            to_add = x[start + 1:]
                    new_str = new_str + to_add

            if len(clean_tweet) > 5 and self.has_chars(clean_tweet):
                clean_tweets.append(new_str)

        return clean_tweets

    def prioritize_sentences(self, sentences_dict, priority_emotion):
        priority_sentences = []
        for s in sentences_dict:
            emotion_detect = NRCLex(s.lower())
            top_emotions = [x[0] for x in emotion_detect.top_emotions]
            if priority_emotion in top_emotions[:3]:
                priority_sentences.append(s)
        coherent_text = " ".join(priority_sentences)
        return coherent_text

    def top_emotions_dict(self, texts, num_emotions):
        affect_dict = self.find_top_emotion(texts, True)
        top_dict = {}
        for x in range(num_emotions):
            emotion = max(affect_dict, key=lambda k: len(affect_dict[k]))
            top_dict[emotion] = affect_dict[emotion]
            affect_dict.pop(emotion)
        return top_dict

    def summarize_texts(self, text):
        top_emotion = self.find_top_emotion(text)
        coherent_text = self.prioritize_sentences(text)
        summary = self.textSummarizer.summarize_text_bart(coherent_text, top_emotion)

        return "Here is a rough summary of the texts: " + summary

    def find_sentiment(self, text):
        sentiment, score = self.sentimentAnalyzer.calc_sentiment(text)
        string = "The overall sentiment detected is " + sentiment + " with a score of " + str(score) + "."
        return string

    def get_emotions_detected(self, text):
        emotion_dict = self.top_emotions_dict(text, self.num_of_top_emotions)
        string = "The most significant emotions were: "
        for emotion in list(emotion_dict.keys()):
            string = string + ", "
        string = string[:-2]
        string = string + "\n"
        for emotion in list(emotion_dict.keys()):
            string = string + "Words like: "
            for count, word in enumerate(emotion_dict[emotion]):
                if count+1 != len(emotion_dict[emotion]):
                    string = string + word + ", "
                else:
                    string = string + "and " + word + ", "
            string = string + "convey " + emotion + ". \n"
        string = string[:-1]

        return string

if __name__ == "__main__":
    text1 = ["As I walked into the surprise party, the room erupted with cheers and joy."]
    text2 = "Yes"
    print(text1)
    analysis = Helper()
    #emotions1 = analysis.get_emotions_detected(text1)
    #sentiment1 = analysis.find_sentiment(text1)
    emotions2 = analysis.get_emotions_detected(text2)
    sentiment2 = analysis.find_sentiment(text2)
    #summarize = analysis.summarize_texts(text)
    #print(summarize)
    print(sentiment2)
    print(emotions2)