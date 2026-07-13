def shortest_word(license_plate, words):
    # 1. Sort the words by length.
    # Python's sort is "stable", meaning ties stay in their original order.
    words.sort(key=len)

    # 2. Create a list of the required letters from the license plate
    # We ignore numbers/spaces and make everything lowercase.
    required_chars = [] 
    for char in license_plate:
        if char.isalpha():
            required_chars.append(char.lower())

    # 3. Check each word
    for word in words:
        # Create a temporary copy of the word as a list
        # We do this so we can "cross off" (remove) letters as we find them
        temp_word = list(word)

        for letter in required_chars:
            if letter in temp_word:
                # If the letter exists, remove it (cross it off)
                # so we can handle duplicates (like two 's's)
                temp_word.remove(letter)
            else:
                break
        else:
            return word
        

result_1 = shortest_word("1s3 PSt", ["step","stepsss", "steps", "stripe","stepple"])
print(result_1)
