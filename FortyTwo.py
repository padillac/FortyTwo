## This Magic-8 Ball style chatbot responds to your questions 
## with knowledge gleaned from reading every text file in the "stories" directory 
## and building associations of words most likely to appear in succession.
#
## Written by Chris Padilla, 12/2020

import os
import random

stories = os.listdir('stories/')
paths = {}
skipwords = [
    'what',
    'where',
    'when',
    'who',
    'why',
    'is',
    'are',
    'the',
    'a',
    'of',
    'and',
    'do',
    'I',
    'you',
    'will'
]

def prob(p):
    return p > random.random()

for s in stories:
    print("Processing {}... {}/{}".format(s, stories.index(s)+1, len(stories)))
    with open('stories/' + s, 'r') as f:
        raw = f.read().split()
        for i in range(len(raw)-1):
            cur = raw[i].strip().strip(':;.,?\\/[]\{\}\"\'-_=+!').replace('\\r', ' ').replace('\\n', ' ').replace('.', '').replace(',', '').replace('\\', '')
            nex = raw[i+1].strip().strip(';.,?\\/[]\{\}"\'-_=+!').replace('\\r', ' ').replace('\\n', ' ').replace('.', '').replace(',', '').replace('\\', '')
            if cur in paths:
                if nex in paths[cur]:
                    paths[cur][nex] += 1
                else:
                    paths[cur][nex] = 1
            else:
                paths[cur] = {nex: 1}


print()
while True:
    q = input("Ask me a question: ").split()
    for w in skipwords:
        if w in q:
            q = [x for x in q if x != w]
    q2 = q.copy()
    
    query = None
    while query not in paths and q:
        query = random.choice(q)
        q.remove(query)
    
    if not q and query not in paths:
        print("There is such thing as a dumb question\n")
        continue
            

    alength = random.choice(range(6,17))
    answer = [random.choice(list(paths[query].keys()))]
    for i in range(1, alength):
        done = False
        pop = list(paths[answer[i-1]].keys())
        for w in pop:
            if w in q2 and prob(.25):
                answer.append(w)
                done = True
        if done:
            continue
        weights = [paths[answer[i-1]][key] for key in pop]
        new = random.choices(pop, weights)[0]
        answer.append(new)
    
    print('\n~ ' + ' '.join(answer) + ' ~\n')

