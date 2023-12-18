import numpy as np

def head_tail_breaks(array, break_per=0.4):
    """
    Applies the head/tail breaks algorithm to classify data in an array.

    Parameters:
    array (numpy.ndarray): Input array to be classified.
    break_per (float): Break percentage to control the classification.

    Returns:
    tuple: Returns the head/tail index and the list of cut values.
    """
    if array.size == 0:
        raise ValueError("Input array is empty")

    # Flatten the array and remove invalid values
    valid_array = array[array != -1].flatten()

    if valid_array.size == 0:
        raise ValueError("No valid data in the array")

    rats, cuts = [], [0]
    rat_in_head = 0
    ht_index = 1

    while rat_in_head <= break_per and valid_array.size > 1:
        mean = np.mean(valid_array)
        cuts.append(mean)

        head_mean = valid_array[valid_array > mean]
        rat = len(head_mean) / len(valid_array)
        rats.append(rat)

        rat_in_head = np.mean(rats) if rats else rat

        if rat_in_head < break_per:
            ht_index += 1

        valid_array = head_mean

    return ht_index, cuts
