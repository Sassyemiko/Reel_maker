from llama_cpp import Llama
import json
import os

class SentimentAnalyzer:
    def __init__(self, model_path='models/Meta-Llama-3-8B-Instruct-Q4_K_M.gguf'):
        self.model_path = model_path
        self.llm = None
        self._load_model()
    
    def _load_model(self):
        """Load the LLM model into memory"""
        print("Loading LLM model (this may take 1-2 minutes)...")
        try:
            self.llm = Llama(
                model_path=self.model_path,
                n_ctx=2048,
                n_threads=4,
                n_gpu_layers=0,  # Set to 35 if you have NVIDIA GPU with 6GB+ VRAM
                verbose=False
            )
            print("✅ Model loaded successfully!")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            print(f"Looking for model at: {os.path.abspath(self.model_path)}")
            raise
    
    def analyze_thread(self, title, comments):
        """Analyze Reddit thread for engagement potential"""
        prompt = f"""You are analyzing Reddit threads for short-form video content (TikTok/Reels/Shorts).

REDDIT THREAD:
Title: {title}

Content: {comments[:800]}

TASK:
1. Rate engagement potential (1-10)
2. Determine sentiment (positive/negative/neutral/controversial)
3. Extract the most engaging segment for video
4. Explain why this would make good content

Respond in JSON format ONLY:
{{
    "score": <integer 1-10>,
    "sentiment": "<positive/negative/neutral/controversial>",
    "best_segment": "<the most engaging 2-3 sentences>",
    "reason": "<brief explanation>",
    "hook_potential": "<high/medium/low>"
}}"""
        
        try:
            response = self.llm(
                prompt,
                max_tokens=400,
                temperature=0.3,
                stop=['\n\n', '```']
            )
            
            return self._parse_response(response['choices'][0]['text'])
        except Exception as e:
            print(f"LLM Analysis Error: {e}")
            return {
                'score': 6,
                'sentiment': 'neutral',
                'best_segment': title + " " + comments[:200],
                'reason': 'Fallback due to parsing error',
                'hook_potential': 'medium'
            }
    
    def _parse_response(self, text):
        """Parse the LLM response into JSON"""
        try:
            # Clean up the response
            text = text.strip()
            
            # Remove markdown code blocks if present
            if text.startswith('```'):
                text = text.split('```')[1]
                if text.startswith('json'):
                    text = text[4:]
            
            # Find JSON object
            start = text.find('{')
            end = text.rfind('}') + 1
            
            if start == -1 or end == 0:
                raise ValueError("No JSON found in response")
            
            json_str = text[start:end]
            result = json.loads(json_str)
            
            # Validate required fields
            required = ['score', 'sentiment', 'best_segment', 'reason']
            for field in required:
                if field not in result:
                    result[field] = 'N/A' if field in ['sentiment', 'reason'] else 5
            
            return result
            
        except Exception as e:
            print(f"JSON Parse Error: {e}")
            print(f"Raw response: {text[:200]}")
            return {
                'score': 5,
                'sentiment': 'neutral',
                'best_segment': text[:300],
                'reason': 'Parse error - using fallback',
                'hook_potential': 'medium'
            }