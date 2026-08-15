import asyncio
from core.orchestrator import AIOSOrchestrator

async def main():
    orch = AIOSOrchestrator(config={})
    result = await orch.run_pipeline("create_episode", {
        "topic": "How AI is Changing Kerala's Job Market",
        "language": "Malayalam",
        "niche": "Technology",
        "length_minutes": 15,
    })
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())
