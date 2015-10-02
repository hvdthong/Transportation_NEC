__author__ = 'vdthoang'
# this file find the features for each token

# make the default is 'utf-8'
import sys, re
reload(sys)
sys.setdefaultencoding('utf8')


def token_matchDict(token, dictionary):
    if token in dictionary:
        return True
    else:
        return False


def token_isCapitalized(token):
    if token[0].isupper() is True:
        return True
    else:
        return False


def token_isAllDigit(token):
    if token.isdigit() is True:
        return True
    else:
        return False


def token_isAllCharacter(token):
    if token.isalpha() is True:
        return True
    else:
        return False


def token_isBusPlate(token):
    pattern = r'[A-z]{3}[0-9]+[A-z]{1}'
    if re.match(pattern, token):
        return True
    else:
        return False
