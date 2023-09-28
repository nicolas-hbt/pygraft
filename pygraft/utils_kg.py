import numpy as np


def generate_weight_vector(size, spread):
    if not 0 <= spread <= 1:
        raise ValueError("Spread parameter must be between 0 and 1.")

    weights = [np.random.rand() for _ in range(size)]
    total_weight = sum(weights)
    weights = [weight / total_weight for weight in weights]
    balanced_weights = [weight * (1 - spread) + (spread / size) for weight in weights]

    return balanced_weights


def generate_random_numbers(mean, std_dev, size):
    # Generate random numbers from a normal distribution
    numbers = np.random.normal(mean, std_dev, size)
    # Normalize the numbers so their sum is equal to 1
    normalized_numbers = numbers / np.sum(numbers)
    # Clip the numbers between a small positive value and 1
    clipped_numbers = np.clip(normalized_numbers, np.finfo(float).eps, 1)
    # Normalize again to ensure the sum is exactly 1
    clipped_numbers = clipped_numbers / np.sum(clipped_numbers)

    return clipped_numbers


def get_fast_ratio(num_entities):
    if num_entities >= 1000000:
        return 15
    if num_entities >= 500000:
        return 10
    elif num_entities >= 50000:
        return 5
    elif num_entities >= 30000:
        return 3
    else:
        return 1


def transitive_inference(triples, original_triples):
    """
    with multi-hop reasoning
    """
    inferred_triples = set()
    print(list(triples))
    rel = list(triples)[0][1]
    for triple1 in original_triples:
        for triple2 in triples:
            if triple1[2] == triple2[0]:
                inferred_triple = (triple1[0], rel, triple2[2])

                if inferred_triple not in triples:
                    inferred_triples.add(inferred_triple)

    if inferred_triples:
        triples.update(inferred_triples)  # for next run
        inferred_triples.update(transitive_inference(triples, original_triples))

    return inferred_triples


def inverse_inference(kg, inv_rel):
    return set((triple[2], inv_rel, triple[0]) for triple in kg)


def symmetric_inference(kg):
    return set((triple[2], triple[1], triple[0]) for triple in kg)


def reflexive_inference(kg):
    return set((triple[0], triple[1], triple[0]) for triple in kg) | set(
        (triple[2], triple[1], triple[2]) for triple in kg
    )


def subproperty_inference(kg, super_rel):
    return set((triple[0], super_rel, triple[2]) for triple in kg)


def filter_symmetric(arr):
    result = []
    for row in arr:
        if row.tolist() not in result and row[::-1].tolist() not in result:
            result.append(row.tolist())
    return np.array(result)
