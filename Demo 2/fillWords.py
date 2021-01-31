def fillWords(results_array, sample_array2, list_sample, notfound_array, word_size):
    index = [-1, -1]
    for i in range(0, len(sample_array2)):
        try:
            index[1] = sample_array2[i].index(list_sample[0])
            #print("test", i)
            #print(sample_array2[i].index(list_sample[0]))
            index[0] = i
            #print(index[0])
        except:
            pass

    #print(index[0],index[1])

    if(list_sample[1] == "across"):
        word_index = -1
        for i in range(index[1], word_size + index[1]):
            word_index += 1
            if notfound_array[index[0]][i] != '*':
                temp_result = []
                for x in range(len(results_array)):
                    #print(results_array[x][word_index], notfound_array[index[0]][i], word_index)
                    if results_array[x][word_index] == notfound_array[index[0]][i]:
                        temp_result.append(results_array[x])
                results_array = temp_result

    else:
        word_index = -1
        #down the table, R X C
        for i in range(index[0], word_size + index[0]):
            word_index += 1
            if notfound_array[i][index[1]] != '*':
                temp_result = []
                for x in range(len(results_array)):
                    #print(results_array[x][word_index], notfound_array[i][index[1]], word_index)
                    if results_array[x][word_index] == notfound_array[i][index[1]]:
                        temp_result.append(results_array[x])
                results_array = temp_result

    return results_array

def fillSolution(result, sample_array2, list_sample, notfound_array, word_size):
    index = [-1, -1]
    for i in range(0, len(sample_array2)):
        try:
            index[1] = sample_array2[i].index(list_sample[0])
            index[0] = i
        except:
            pass

    if(list_sample[1] == "across"):
        word_index = -1
        for i in range(index[1], word_size + index[1]):
            word_index += 1
            if notfound_array[index[0]][i] == '*':
                notfound_array[index[0]][i] = result[0][word_index]

    else:
        word_index = -1
        #down the table, R X C
        for i in range(index[0], word_size + index[0]):
            word_index += 1
            #print(notfound_array[i][index[1]], result[0][word_index], word_index)
            if notfound_array[i][index[1]] == '*':
                notfound_array[i][index[1]] = result[0][word_index]

    return notfound_array

# word_size = 3

# sample_array = [['*','*','*','*','*'],
#                 ['*','*','*','*','*'],
#                 ['*','*','*','*','*'],
#                 ['*','*','*','*','*'],
#                 ['*','*','*','*','*']]

#positioning
# sample_array2 = [[1, 2, 3, 4, 5],
#                  [6, 0, 0, 0, 0],
#                  [7, 0, 0, 0, 0],
#                  [8, 0, 0, 0, 0],
#                  [9, 0, 0, 0, -1]]

#                  #map_array

# list_sample = [6, "across"]

# sample_array = [['P','A','R','I','S'],
#                 ['O','*','*','*','*'],
#                 ['O','*','*','*','*'],
#                 ['C','*','*','*','*'],
#                 ['H','*','*','*','!']]

# notfound_array = [['!', '*', '*', 'U', 'B'],
#                 ['!', 'L', 'A', 'N', 'E'],
#                 ['M', 'A', 'Y', 'B', 'E'],
#                 ['O', 'R', 'E', 'O', '!'],
#                 ['*', '*', '*', 'X', '!']]
#                 #if result array size = 1, put into designated place and check with answer if its correct or not


# result = (fillWords(results_array, sample_array2, list_sample, notfound_array, word_size))

# print(result)

# result2 = fillSolution(result, sample_array2, list_sample, notfound_array, word_size)

# print (result2)
# results_array = ['POOCH','X+Y', 'X/Y', 'LOS', 'RNA', 'BIG', 'ROB', 'TWO', 'GUY', 'MEN', 'CBS']
#results_array = ['POOCH']
