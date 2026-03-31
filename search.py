import requests
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# from groq import Groq  # DISABLED - Using local LLM instead

def vader(scraped_text):
    try:
        nltk.data.find('vader_lexicon.zip')
    except LookupError:
        nltk.download('vader_lexicon')
    
    def analyze_sentiment(text):
        """Analyzes the sentiment of a given text using VADER."""
        try:
            analyzer = SentimentIntensityAnalyzer()
            scores = analyzer.polarity_scores(text)
            return scores
        except Exception as e:
            print(f"Error during sentiment analysis: {e}")
            return None
    
    texts = scraped_text
    final = texts
    for i, text in enumerate(scraped_text):
        title, desc = text
        sentiment = analyze_sentiment(desc)
        if sentiment:
            print(f"Text: \"{title}\"")
            print(f"Scores: {sentiment}")
            print("-" * 20)
            final[i].append(sentiment['compound'])
        else:
            print(f"Could not analyze: {text}")
    
    return final


def groq(final, api_key=None, threshold=-0.3, model="llama-3.3-70b-versatile",
         temperature=1, max_tokens=1024):
    """
    DISABLED FOR OFFLINE OPERATION
    This function previously used Groq API.
    Now it returns the highest-scoring thread based on VADER sentiment.
    """
    print("⚠️  Groq API is disabled for offline mode")
    print("📊 Using VADER sentiment scoring instead...")
    
    final_filtered = []
    ranking = []
    
    for item in final:
        if len(item) >= 3 and item[2] < threshold: 
            final_filtered.append([item[0], item[1]])
            ranking.append([item[0], item[2]])
    
    print("FINALISED FILTERED TEXT")
    print("Printing out rankings...")
    print("--------------------")
    for rank in ranking: 
        print(rank)
    print("--------------------")
    
    # Select the thread with the most negative sentiment (most dramatic)
    if ranking:
        best_thread = max(ranking, key=lambda x: abs(x[1]))
        best_title = best_thread[0]
        
        # Find the full thread data
        for text in final_filtered:
            if text[0] == best_title:
                print(f"✅ Selected: {best_title}")
                return {
                    'title': text[0],
                    'desc': text[1],
                    'score': best_thread[1]
                }
    
    # Fallback: return first thread
    if final_filtered:
        return {
            'title': final_filtered[0][0],
            'desc': final_filtered[0][1],
            'score': 0
        }
    
    print("❌ Error: No threads available!")
    return None