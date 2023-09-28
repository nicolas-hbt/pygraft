import numpy as np


def generate_weight_vector(size, spread):
    """
    Generates a weight vector of size `size` with random values between 0 and 1.

    Args:
        size (int): The size of the weight vector.
        spread (float): The spread of the weight vector.

    Returns:
        A weight vector of size `size` with random values between 0 and 1.
    """
    if not 0 <= spread <= 1:
        raise ValueError("Spread parameter must be between 0 and 1.")

    weights = [np.random.rand() for _ in range(size)]
    total_weight = sum(weights)
    weights = [weight / total_weight for weight in weights]
    balanced_weights = [weight * (1 - spread) + (spread / size) for weight in weights]

    return balanced_weights


def generate_random_numbers(mean, std_dev, size):
    """
    Generates random numbers from a normal distribution with mean `mean` and standard deviation `std_dev`.

    Args:
        mean (float): The mean of the normal distribution.
        std_dev (float): The standard deviation of the normal distribution.
        size (int): The size of the output array.
    
    Returns:
        An array of random numbers from a normal distribution with mean `mean` and standard deviation `std_dev`.
    """
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
    """
    Makes the KG generation process faster by lowering the diversity in entities' profiles.
    
    Args:
        num_entities (int): The number of entities.
        
    Returns:
        The fast ratio for the given number of entities.
    """
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
    Infers new triples to be added using transitive inference.

    Args:
        triples (set): The set of triples.
        original_triples (set): The set of original triples.

    Returns:
        set: The set of inferred triples.
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
    """
    Infers new triples to be added using inverse inference.

    Args:
        kg (set): The set of triples.
        inv_rel (str): The inverse relation.

    Returns:
        set: The set of inferred triples.
    """
    return set((triple[2], inv_rel, triple[0]) for triple in kg)


def symmetric_inference(kg):
    """
    Infers new triples to be added using symmetric inference.
    
    Args:
        kg (set): The set of triples.
        
    Returns:
        set: The set of inferred triples.
    """
    return set((triple[2], triple[1], triple[0]) for triple in kg)


def reflexive_inference(kg):
    """
    Infers new triples to be added using reflexive inference.

    Args:
        kg (set): The set of triples.

    Returns:
        set: The set of inferred triples.
    """
    return set((triple[0], triple[1], triple[0]) for triple in kg) | set(
        (triple[2], triple[1], triple[2]) for triple in kg
    )


def subproperty_inference(kg, super_rel):
    """
    Infers new triples to be added using subproperty inference.

    Args:
        kg (set): The set of triples.
        super_rel (str): The superproperty relation.

    Returns:
        set: The set of inferred triples.
    """
    return set((triple[0], super_rel, triple[2]) for triple in kg)


def filter_symmetric(arr):
    """
    Filters out symmetric triples from an array.

    Args:
        arr (np.ndarray): The array of triples.

    Returns:
        np.ndarray: The filtered array of triples.
    """
    result = []
    for row in arr:
        if row.tolist() not in result and row[::-1].tolist() not in result:
            result.append(row.tolist())
    return np.array(result)
