from transformers import pipeline


class SentimentAnalysis:
    def calc_sentiment(self, texts):
        sentiment_pipeline = pipeline("sentiment-analysis")
        total_score = 0
        for text in texts:
            result = sentiment_pipeline(text)[0]
            sentiment_score = result['score']
            total_score += sentiment_score

        average_score = total_score / len(texts)
        overall_sentiment = 'positive' if average_score > 0.5 else 'neutral' if average_score == 0.5 else 'negative'
        return (overall_sentiment, average_score)