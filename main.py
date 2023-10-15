
def load_file(filepath):
    with open(filepath, 'r') as f:
        return f.read().split('\n')

def to_per(num):
    return round(num * 100, 2)

alpha = "abcdefghijklmnopqrstuvwxyz"
def freqs(db):
    freqs = {}
    for word in db:
        for i in range(0,5):
            letter = word[i]
            if i not in freqs:
                freqs[i] = {}

            if letter in alpha:
                if letter in freqs[i]:
                    freqs[i][letter] += 1
                else:
                    freqs[i][letter] = 1

    for i in freqs:
        print(f'In the {i}th position:')

        freq_list = [(k, v) for k, v in freqs[i].items()]
        freq_list.sort(key=lambda x: x[1], reverse=True)
        total = sum([x[1] for x in freq_list])
        for letter, times in freq_list:
            print(f'{letter}: {times}', end=" | ")
            # print(f'{letter}: {times} ({to_per(times/total)})', end=" | ")
        print("")
    return freqs

def hunt_word(db, inword='', notinword='', inSpecific=[]):
    count = 0
    for word in db:
        ins = [True if char in word else False for char in inword]
        nots = [True if char not in word else False for char in notinword]
        insSpecific = [True if word[pos] == char else False for pos, char in inSpecific]
        if all(ins) and all(nots) and all(insSpecific):
            print(word)
            count += 1
    print(f'\nFound {count} words')

def best_words(better_db):
    letterFreqsRaw = freqs(db)
    letterFreqs = []
    for i in range(0,5):
        freq_list = [(k, v) for k, v in letterFreqsRaw[i].items()]
        freq_list.sort(key=lambda x: x[1], reverse=True)
        letterFreqs.append(freq_list)

    for i in range(0,5):
        for j in range(0,5):
            for k in range(0,5):
                for l in range(0,5):
                    for m in range(0,5):
                        inSpecific = [
                            (0, letterFreqs[0][i]),
                            (1, letterFreqs[1][j]),
                            (2, letterFreqs[2][k]),
                            (3, letterFreqs[3][l]),
                            (4, letterFreqs[4][m]),
                        ]
                        filter(better_db, inSpecific)

def filter(better_db, inSpecific):
    """ inSpecific is a list of tuples where (pos, char)"""
    set1 = better_db[0][inSpecific[0][1][0]]
    set2 = better_db[1][inSpecific[1][1][0]]
    set3 = better_db[2][inSpecific[2][1][0]]
    set4 = better_db[3][inSpecific[3][1][0]]
    set5 = better_db[4][inSpecific[4][1][0]]

    result = set1.intersection(set2, set3, set4, set5)
    if len(result) > 0:
        print(result)





if __name__ == '__main__':
    db = load_file('db.txt')

    better_db = []
    for i in range(0,5):
        better_db.append({})
    for word in db:
        for i in range(0,5):
            if word[i] not in better_db[i]:
                better_db[i][word[i]] = set()
            better_db[i][word[i]].add(word)
    
    # best_words(better_db)

    hunt_word(db, inword='ny', notinword='saiterd', inSpecific=[])

    

