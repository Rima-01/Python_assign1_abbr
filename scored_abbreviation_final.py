
# Retrieves all the values from values.txt file for the score calculation.
def retrieve_letter_values(filename="values.txt"):
    values = {}
    with open(filename, 'r') as file:
        for line in file:
            letter, value = line.strip().split()
            values[letter] = int(value)
 #           print("values file content:", value)
    return values

#****************************************************************************#

# Converts to upper case & removes all non-letter characters
import re
def parse_name(name):
    name = name.upper()  # Converting the name to uppercase.
    name = re.sub(r"[^A-Z\s-]", "", name)  # Removing the non-letter characters except spaces and hyphens.
    name = re.sub(r"-", " ", name)  # Replacing the hyphens with spaces.
    return name

#****************************************************************************#

# Gets the indices of the 1st letter of each word. Used for comparing against the indices of the abbreviation
def get_first_letter_indices(sentence):
    # Initialising lists to store the first letters and their indices, while keeping track of indices
    indices = []
    letters = []
    for i, char in enumerate(sentence):
        # Checking if it's the start of a word
        if (i == 0 or sentence[i-1] == ' ') and char.isalpha():
            indices.append(i)
            letters.append(sentence[i])

     # Handling the case for single-word names, like 'Alder'. This manupulation is done for easier comparison of indices, later on for score calculation
    if len(indices) == 1:
        indices = [indices[0], indices[0], indices[0]]
        letters = [letters[0], letters[0], letters[0]]
    
    # Handling the case for two-word names, like 'Crab Apple'. This manupulation is done for easier comparison of indices, later on for score calculation
    elif len(indices) == 2:
        indices = [indices[0], indices[1], indices[1]]
        letters = [letters[0], letters[1], letters[1]]
        
    return indices, letters

#****************************************************************************#

# Gets the indices of the 1st letter of each word. Used for comparing against the indices of the abbreviation
def get_last_letter_indices(sentence):
    # Initialising lists to store the last letters and their indices, while keeping track of indices
    indices = []
    letters = []

    # Iterate through the sentence
    for i, char in enumerate(sentence):
        # Check if it's the last letter of a word
        if char.isalpha() and (i == len(sentence) - 1 or sentence[i + 1] == ' '):
            indices.append(i)
            letters.append(char)

     # Handling the case for single-word names, like 'Alder'. This manupulation is done for easier comparison of indices, later on for score calculation
    if len(indices) == 1:
        indices = [0, indices[0], indices[0]]
        letters = [0, letters[0], letters[0]]
        
    # Handling the case for two-word names, like 'Crab Apple'. This manupulation is done for easier comparison of indices, later on for score calculation
    elif len(indices) == 2:
        indices = [0, indices[0], indices[1]]
        letters = [0, letters[0], letters[1]]
        
    return indices, letters

#****************************************************************************#

from itertools import combinations
def get_three_letter_words_index(sentence):
    # Input string
    name = sentence

    # Get the first letter and last letter indices for the particular name
    first_letter_indices, _ = get_first_letter_indices(name)
    last_letter_indices, _ = get_last_letter_indices(name)

    # Inncluding only the first index (0) and combining it with combinations of the rest. 
    #This is to ensure that the order is not broken in the abbreviations
    indices_combinations = combinations(range(1, len(name)), 2)

    # Forming 3-letter words with the first letter fixed at index 0
    three_letter_words = []

    for combo in indices_combinations:
        indices = (0, *combo)  # Always include 0
    
        # Check if any of the indices point to a space
        if all(name[i] != ' ' for i in indices):  # Include only if no spaces
            word = ''.join(name[i] for i in indices)
            
            #Forming a large list with all relevant details for the particular name          
            three_letter_words.append((first_letter_indices, last_letter_indices, word, indices))


    return three_letter_words

#****************************************************************************#

def calc_sorted_score_abbr(three_letter_words):
    letter_values = retrieve_letter_values()

# Initializing the list to store the results of the scores
    abbr_score = []

    # Logic to correctly calculate the scores, based on position and weights of individual letters as per the values.txt file
    for k in range(len(three_letter_words)):
        total_score = 0
        for i in range(1, len(three_letter_words[k][0])):
            # Checking to see if any of the letters are 1st letters of a word, by matching the indices
            if three_letter_words[k][3][i] == three_letter_words[k][0][i]: 
                total_score = total_score + 0
             # Checking to see if any of the letters are the last letters of a word, by matching the indices   
            elif three_letter_words[k][3][i] == three_letter_words[k][1][i]:
                if three_letter_words[k][2][i] == 'E':
                   total_score = total_score + 20
                else:
                    total_score = total_score + 5    
            # Condition when the letter is neither 1st nor the the last letter. 
            #So finding out relative position and assigning scores for it's position and weights as per values.txt file
            else:
                if three_letter_words[k][3][i] < three_letter_words[k][0][i]:
                    total_score = total_score + three_letter_words[k][3][i]
                else:
                    total_score = total_score + min(3, three_letter_words[k][3][i] - three_letter_words[k][0][i]) 
                # Adding the weights as per the values.txt file
                total_score = total_score + letter_values.get(three_letter_words[k][2][i])
    
        # Appending the word(abbreviation) and its score to the list
        abbr_score.append([three_letter_words[k][2], total_score])

    # Sorting the list by the total_score (second element in each tuple). Done for easier manupulation later on
    abbr_score_sorted = sorted(abbr_score, key=lambda x: x[1])

    # Output the sorted result list
    return abbr_score_sorted


#****************************************************************************#

#****** The main function *****************#

def main():
    import re
    from itertools import combinations

    letter_values = retrieve_letter_values()

    file_inp = input("Please enter the input file name: ") 
    surname = input("Please enter your surname to create the output file: ")
    file_out = surname + "_" + file_inp.replace('.txt', '_abbrevs.txt')

    with open(file_inp,'r') as file:     # Read names from the input file.
        names = [line.strip() for line in file]
        #print(names)

    names_abbr_scores = {}

    # For each name, now calling all the functions defined above one-by-one to get the abbreviated names and scores
    for name in names:     # Process each name.
        sentence = parse_name(name)
        #print(sentence)
        three_letter_words = get_three_letter_words_index(sentence)
        #print(three_letter_words)
        names_abbr_scores[f"list_{name}"] = calc_sorted_score_abbr(three_letter_words)
    
    #print(names_abbr_scores)

#**********************************************#
    # Done to check for duplications of abbreviations across the names
    all_list = []
    for name in names:
        all_list.append(names_abbr_scores[f"list_{name}"])

#**********************************************#
    # Removing duplicates and updating with unique values only
    
    # Collecting all the first column values from all lists
    first_col_values_all = [set(row[0] for row in lst) for lst in all_list]

    # Identifying the common values in the first column across all lists, to remove all duplications
    common_values = set.intersection(*first_col_values_all)

    # Removing duplicate values
    filtered_lists = [[row for row in lst if row[0] not in common_values] for lst in all_list]
    
    #    print(f"Filtered List {i}:", filtered_list)
    # Storing only the rows with the least value(s) in the 2nd column for each list
    least_in_column_lists = []
    for filtered_list in filtered_lists:
        if filtered_list:
            # Finding the minimum values in the second column
            min_value = min(row[1] for row in filtered_list)
            # Collect all rows with the minimum value in the second column
            min_rows = [row[0] for row in filtered_list if row[1] == min_value]
            least_in_column_lists.append(min_rows)
        else:
            least_in_column_lists.append([])  # To handle when the list is empty

    # Writing the results to the output file.
    with open(file_out, 'w') as file1:
        for name, result in zip(names, least_in_column_lists):
            file1.write(f"{name}\n{' '.join(result)}\n\n")

    print(f"Results written to {file_out}")    

# Run the main function when the script is executed.
if __name__ == "__main__":
    main()




