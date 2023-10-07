import matplotlib.pyplot as plt
import json

dictionary = json.load(open('jsonRandomMethodCalls.json', 'r'))['RandomMethodCalls']
new_dictionary = {}

for k, v in dictionary.items():
	new_dictionary[float(k)]=float(v)

plt.grid(True)
plt.plot(*zip(*sorted(new_dictionary.items())))
plt.plot(color='maroon', marker='o')
plt.xlabel('Number of Clients')
plt.ylabel('Average latency per request when random requests are sent (ms)')


plt.show()