import json
from functools import reduce
import numpy as np
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

load_dotenv()

FILE_PATH = os.getenv('MESSAGE_FILE_PATH')


def reducerPhotos(collector, item):
    if item['sender_name'] in collector:
        collector[item['sender_name']] = collector[item['sender_name']] + len(item['photos'])
    else:
        collector[item['sender_name']] = len(item['photos'])
    return collector


def reducerReactions(collector, item):
    if 'reactions' in item:
        if item['sender_name'] in collector:
            collector[item['sender_name']] = collector[item['sender_name']] + len(item['reactions'])
        else:
            collector[item['sender_name']] = len(item['reactions'])
    return collector


def reducerWithoutReactions(collector, item):
    if 'reactions' not in item:
        if item['sender_name'] in collector:
            collector[item['sender_name']] = collector[item['sender_name']] + 1
        else:
            collector[item['sender_name']] = 1
    return collector

def mostReactionReducer(collector, item):
    if 'reactions' in item:
        for reaction in item['reactions']:
            if reaction['actor'] in collector:
                collector[reaction['actor']] = collector[reaction['actor']] + 1
            else:
                collector[reaction['actor']] = 1
    return collector


def generatePlotForData(amount, title, output):
    sortedAmount = {k: v for k, v in reversed(sorted(amount.items(), key=lambda item: item[1]))}

    x = list(sortedAmount.keys()) + list(filter(lambda key: key not in sortedAmount.keys(), members))
    values = list(map(lambda key: key in sortedAmount and sortedAmount[key], x))

    plt.bar(x, height=values)
    for i, v in enumerate(values):
        plt.text(i - 0.25, v + 1, str(v or 0), color='blue', fontweight='bold')
    plt.title(title)

    outputDir = os.getenv('OUTPUT_DIR')

    plt.xticks(x, x, rotation=75)
    plt.tight_layout()
    plt.savefig(outputDir + '/' + output, dpi=200, bbox_inches='tight')
    plt.close()


with open(FILE_PATH) as file:
    # preload
    jsonData = json.load(file)
    messages = jsonData['messages']
    members = list(map(lambda member: member['name'], jsonData['participants']))
    messageWithPhotos = list(filter(lambda x: 'photos' in x, messages))

    # photos
    amountPhotos = reduce(reducerPhotos, messageWithPhotos, {})
    generatePlotForData(amountPhotos, "Répartition des memes sur skate fast eat ass",
                        'plot-output-photos.png')

    # reaction
    amountReaction = reduce(reducerReactions, messageWithPhotos, {})
    generatePlotForData(amountReaction, "reactions des memes sur skate fast eat ass",
                        'plot-output-reactions.png')

    #meme sans réaction
    amountWithoutReaction = reduce(reducerWithoutReactions, messageWithPhotos, {})
    generatePlotForData(amountWithoutReaction, "Memes sans réactions dans skate fast eat ass",
                        'plot-output-without-reactions.png')

    #personne qui réagit le plus
    mostReactionAmount = reduce(mostReactionReducer, messageWithPhotos, {})
    generatePlotForData(mostReactionAmount, "Personne qui réagit le plus dans skate fast eat ass",
                        'plot-output-most-reaction.png')
