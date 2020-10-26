import scipy.stats as stats
import functools
import configparser
import os
import time

config = configparser.ConfigParser()
config.read('config.ini')

odds = config['CDFINFO']['odds']
nShinies = int(config['CDFINFO']['nShinies'])

nEncountersFile = config['FILES']['nEncounters']
outputFile = config['FILES']['output']

odds = odds.split('/')
odds = float(odds[0])/float(odds[1])


@functools.lru_cache(maxsize=128)
def probShiny(nEncounters, prob=odds, nShinies=nShinies):

    return 1-stats.binom.cdf(k=nShinies-1, n=nEncounters, p=prob)


def main():
    if os.path.exists(nEncountersFile):
        with open(nEncountersFile, 'r') as file:
            nEncounters = int(file.read())
        while True :
            with open(nEncountersFile, 'r') as file:
                tmp = int(file.read())

            if tmp is not nEncounters:
                nEncounters = tmp
                p = probShiny(nEncounters)
                with open(outputFile, 'w+') as file:
                   file.write(f"{p*100:.2f}%")
            time.sleep(.1)
    else:
        print('The number of encounters file not found.')

if __name__ =='__main__':
    main()