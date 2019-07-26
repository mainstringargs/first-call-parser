from tika import parser
import requests
import os, sys

#import urllib.request
#urllib.request.urlretrieve ("https://research.ameritrade.com/grid/wwws/common/reports/report.asp?reportName=markets.firstcallrecommended&c_name=invest_VENDOR",'firstCallRecommended.pdf')

#write a for-loop to open many files -- leave a comment if you'd #like to learn how
filename = 'file.pdf'

raw = parser.from_file(filename)

count = 0;

print('parsing pdf...');

tickerSet = set();

for line in raw['content'].split('\n'):
    if ': NASDAQ' in line or ': NYSE' in line or ': NA' in line:

        for word in line.split(' '):
            if ':' in word:
                ticker = (word.replace(':',''));
                #print(ticker)
                r = requests.get('https://k1search.greymanindustries.com/api_k1s.php?symbol='+ticker)
                jsonResponse = r.json()
                resCount = (jsonResponse['count'])
                if int(resCount) > 0:
                    #print("resCount is gt 0 for "+ticker)
                    found = False;
                    for result in jsonResponse['results']:
                        if result['symbol'] == ticker:
                            found = True;
                    if not found:
                        tickerSet.add(ticker)
                        count += 1;
                    else:
                        print("Ignoring K1 stock "+ticker);
                else:
                    tickerSet.add(ticker)
                    count += 1;



print("found "+str(count) + " stocks")
prevTickerSet = set()


try:
    os.rename("currStocks.txt","prevStocks.txt")
except Exception as e:
    print(e)

try:
    prevTickerSet = set(line.strip() for line in open('prevStocks.txt'))
    os.remove("prevStocks.txt")
except Exception as e:
    print(e)



with open('currStocks.txt', 'w') as f:
    for item in sorted(tickerSet):
        f.write("%s\n" % item)

print('tickerSet '+str(sorted(tickerSet)))
print('prevTickerSet '+str(sorted(prevTickerSet)))

added = tickerSet.difference(prevTickerSet)
removed = prevTickerSet.difference(tickerSet)

print("added "+str(sorted(added)));
print("removed "+str(sorted(removed)))

try:
    os.remove("addedStocks.txt")
except Exception as e:
    print(e)

try:
    os.remove("removedStocks.txt")
except Exception as e:
    print(e)

with open("addedStocks.txt", 'w') as f:
    for item in sorted(added):
        f.write("%s\n" % item)

with open("removedStocks.txt", 'w') as f:
    for item in sorted(removed):
        f.write("%s\n" % item)

try:
    os.remove("firstCallRecommended-old.pdf")
except Exception as e:
    print(e)

try:
    os.rename(filename,"firstCallRecommended-old.pdf")
except Exception as e:
    print(e)
