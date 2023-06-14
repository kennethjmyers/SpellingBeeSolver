import dill
import pandas as pd


def searchTree(node, puzzle, foundWords=[], mandatoryLetter=None):
  if node.terminatingWord:
    wordToHere = node.wordToHere
    if mandatoryLetter is not None:
      if mandatoryLetter in wordToHere:
        # print(node.wordToHere)
        foundWords.append(node.wordToHere)
    else:
      foundWords.append(node.wordToHere)
  for l in puzzle:
    child = node.__getattribute__(l)
    if child is not None:
      foundWords = searchTree(child, puzzle, foundWords, mandatoryLetter)
  return foundWords


def solvePuzzle(puzzle):
  assert len(puzzle) == 7
  assert puzzle.isalpha()
  mandatoryLetter = puzzle[0]

  allFoundWords = dict()
  for letter in puzzle:
    with open(f'./Data/LetterTrees/{letter}.tree', 'rb') as treeFile:
      thisRoot = dill.load(treeFile)
    foundWords = searchTree(node=thisRoot, puzzle=puzzle, foundWords=[], mandatoryLetter=mandatoryLetter)
    allFoundWords[letter] = foundWords

  return allFoundWords


def convertToDF(allFoundWords):
  # first pass to find max array length
  maxArrLen = 0
  for k in allFoundWords.keys():
    thisLen = len(allFoundWords[k])
    if thisLen > maxArrLen:
      maxArrLen = thisLen

  # second pass to correct lengths
  for k in allFoundWords.keys():
    thisLen = len(allFoundWords[k])
    allFoundWords[k] = allFoundWords[k] + ['' for _ in range(maxArrLen - thisLen)]

  df = pd.DataFrame(allFoundWords)
  return df


def flattenSolution(allFoundWords):
  flattened = []
  for k in allFoundWords.keys():
    flattened += allFoundWords[k]
  return flattened


def findPangrams(puzzleValue, allFoundWords):
  pangrams = []
  for word in flattenSolution(allFoundWords):
    if set(word) == set(puzzleValue):
      pangrams.append(word)
  return pangrams
