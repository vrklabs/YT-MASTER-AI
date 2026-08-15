import httpx
from typing import Any, Dict
from agents.base_agent import BaseAgent
from core.memory import Memory

class ScriptAgent(BaseAgent):
    def __init__(self, model_backend: str = "openrouter", model_name: str = "openrouter/free-llama-3.1-8b"):
        super().__init__("script")
        self.model_backend = model_backend
        self.model_name = model_name
        self.openrouter_key = None  # environment-ൽ നിന്ന് എടുക്കും

    async def run(self, params: Dict[str, Any], memory: Memory) -> Dict[str, Any]:
        import os
        self.openrouter_key = os.environ.get("OPENROUTER_API_KEY")
        topic = params.get("topic", "AI in Kerala")
        language = params.get("language", "Malayalam")
        niche = params.get("niche", "Technology")
        length_minutes = params.get("length_minutes", 15)

        research_data = memory.load("research") or {}
        keywords = research_data.get("keywords", [])

        prompt = f"""
        നിങ്ങൾ ഒരു പ്രൊഫഷണൽ ഡോക്യുമെന്ററി സ്ക്രിപ്റ്റ് റൈറ്ററാണ്.
        വിഷയം: {topic}
        ഭാഷ: {language}
        നിച്: {niche}
        ദൈർഘ്യം: {length_minutes} മിനിറ്റ്

        ആവശ്യങ്ങൾ:
        - ശക്തമായ ഹുക്ക്
        - 6-8 പ്രധാന ഭാഗങ്ങൾ
        - ഓരോ ഭാഗത്തിലും ദൃശ്യ വിവരണം
        - സ്വാഭാവിക ഭാഷ
        - CTA അവസാനം

        കീവേഡുകൾ: {', '.join(keywords)}
        """
        script_text = await self._generate(prompt)
        script_output = {
            "title": f"Episode: {topic}",
            "language": language,
            "script": script_text,
            "word_count": len(script_text.split()),
            "model": self.model_name,
        }
        memory.save("script", script_output)
        return script_output

    async def _generate(self, prompt: str) -> str:
        if self.openrouter_key:
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {"Authorization": f"Bearer {self.openrouter_key}"}
            payload = {
                "model": self.model_name,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 4000,
            }
            async with httpx.AsyncClient(timeout=120) as client:
                try:
                    response = await client.post(url, json=payload, headers=headers)
                    response.raise_for_status()
                    data = response.json()
                    return data["choices"][0]["message"]["content"]
                except Exception as e:
                    print(f"OpenRouter error: {e}")
                    return self._fallback_script()
        else:
            return self._fallback_script()

    def _fallback_script(self) -> str:
        return """
[സീൻ 1: കേരളത്തിന്റെ ഐടി കോറിഡോറുകൾ]
നറേഷൻ: ഒരു കാലത്ത് കേരളത്തിന്റെ സ്വപ്നം ഐടി ജോലിയായിരുന്നു. ഇന്ന് ആ സ്വപ്നത്തെ തന്നെ മാറ്റിമറിക്കാൻ പോകുന്ന ഒരു സാങ്കേതികവിദ്യ വന്നിരിക്കുന്നു — ആർട്ടിഫിഷ്യൽ ഇന്റലിജൻസ്.
...
"""
