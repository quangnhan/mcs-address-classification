set1 = {'hello', 'world'}
set2 = {'there', 'hello', 'world'}

intersection = len(set1.intersection(set2))
union = len(set1.union(set2))
similarity = intersection / union if union != 0 else 0
print(f"Jaccard Similarity: {similarity}")
