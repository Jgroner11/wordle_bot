from gettext import find
import importlib
from operator import index
from sre_parse import State
sampleBot = importlib.import_module("sample-bot")

import time

start = time.time()

state = '-----:00000'
print(sampleBot.play(state))
# i = 0
# while i <  100000:
#     print(i)
#     i += 1
end = time.time()
elapsed = end - start
print(elapsed)

def ch2Ind(ch):
    return ord(ch) - 97
def ind2Ch(i):
    return chr(i + 97)


answer = ['0'] * 5
badLetters = [0] * 26
alphabet = '[ '
for i in range(26):
    alphabet += ind2Ch(i) + ', '

# goodLetters = dict()

# state = "-----:00000,adieu:11221,socks:11211,crime:21213"
# for pair in state.split(','):
#     guess, feedback = pair.split(':')
#     for i, ch in enumerate(guess):
#         if(feedback[i] == '3'):
#             answer[i] = ch
#         elif(feedback[i] == '2'):
#             if(ch in goodLetters):
#                 goodLetters[ch][i] = 1
#             else:
#                 value = [0] * 5
#                 value[i] = 1
#                 goodLetters[ch] = value
#         elif(feedback[i] == '1'):
#             badLetters[ch2Ind(ch)] = 1

# print(answer)
# print(goodLetters)
# print(badLetters)
# print(alphabet)

