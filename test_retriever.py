from retriever import retrieve

queries = [
    "What do students say about Prof. Alfaro's exams in ICS 31?",
    "What is the prerequisite for ICS 45C?",
    "What topics does ICS 46 cover that ICS 45C does not?"
]

for q in queries:
    print("\n" + "="*80)
    print(f"QUERY: {q}")
    print("="*80)
    results = retrieve(q, top_k=3)
    for r in results:
        print(f"\n[Distance: {r['distance']:.4f}] -> Source: {r['source']}")
        print(f"Text snippet: {r['text']}")