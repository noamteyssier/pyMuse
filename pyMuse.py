#!/usr/bin/env python

import requests, argparse, json, sys


def build_query(args, nopeList):
    """reads through args and assembles the query string"""
    query = []
    for a in vars(args):

        # skip over the numSyllables and wordType args
        if a in nopeList:
            continue

        # add to query string if value is found
        if vars(args)[a]:
            qString = '='.join([a, vars(args)[a]])
            query.append(qString)

    # always append the number of syllables & parts of speech
    query.append('md=sp')

    return '&'.join(query)
def print_out(results, numSyllables=None, wordType=None):
    """perform numSyllables/wordType comparisons and print out if passing"""
    for j in results:

        # match numSyllables if arg
        if numSyllables:
            if j['numSyllables'] != int(numSyllables):
                continue

        # match wordType if arg
        if wordType:
            if wordType not in j['tags']:
                continue

        # convert printable items to list
        try:
            items = [j['word'], j['numSyllables'], '+'.join([str(p) for p in j['tags']])]
        except KeyError:
            # in case where tags are not found
            items = [j['word'], j['numSyllables']]

        # print tab delim
        print '\t'.join([str(s) for s in items])


def main():
    p = argparse.ArgumentParser()
    p.add_argument('-rhy', '--rel_rhy', help='search for exact rhymes')
    p.add_argument('-close', '--rel_nry', help='search for approximate rhymes')
    p.add_argument('-syn', '--rel_syn', help='search for synonyms')
    p.add_argument('-ant', '--rel_ant', help='search for antonyms')
    p.add_argument('-ml', '--ml', help='find words with related meaning')
    p.add_argument('-sl', '--sl', help='words pronounced similarly')
    p.add_argument('-sp', '--sp', help='words spelled similarly')
    p.add_argument('-n', '--numSyllables', help='number of syllables to return')
    p.add_argument('-p', '--wordType', help='Part of Speech to Search for [(n)oun, (v)erb, (adj)ective]')
    args = p.parse_args()

    url_base = 'https://api.datamuse.com/words?'


    nopeList = ['numSyllables', 'wordType']
    qString = build_query(args, nopeList)
    query = url_base + qString

    results = requests.get(query).json()
    print_out(results, args.numSyllables, args.wordType)



if __name__ == '__main__':
    main()
