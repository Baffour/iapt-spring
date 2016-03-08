#
#  Copyright (C) 2009 Thadeus Burgess
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>
#


import re
import bz2

# Stop Words courtesy of http://www.dcs.gla.ac.uk/idom/ir_resources/linguistic_utils/stop_words
STOP_WORDS = r"""\b(a|about|above|across|after|afterwards|again|against|all|almost|alone|along|already|also|
although|always|am|among|amongst|amoungst|amount|an|and|another|any|anyhow|anyone|anything|anyway|anywhere|are|
around|as|at|back|be|became|because|become|becomes|becoming|been|before|beforehand|behind|being|below|beside|
besides|between|beyond|bill|both|bottom|but|by|call|can|cannot|cant|co|computer|con|could|couldnt|cry|de|describe|
detail|do|done|down|due|during|each|eg|eight|either|eleven|else|elsewhere|empty|enough|etc|even|ever|every|everyone|
everything|everywhere|except|few|fifteen|fify|fill|find|fire|first|five|for|former|formerly|forty|found|four|from|
front|full|further|get|give|go|had|has|hasnt|have|he|hence|her|here|hereafter|hereby|herein|hereupon|hers|herself|
him|himself|his|how|however|hundred|i|ie|if|in|inc|indeed|interest|into|is|it|its|itself|keep|last|latter|latterly|
least|less|ltd|made|many|may|me|meanwhile|might|mill|mine|more|moreover|most|mostly|move|much|must|my|myself|name|
namely|neither|never|nevertheless|next|nine|no|nobody|none|noone|nor|not|nothing|now|nowhere|of|off|often|on|once|
one|only|onto|or|other|others|otherwise|our|ours|ourselves|out|over|own|part|per|perhaps|please|put|rather|re|same|
see|seem|seemed|seeming|seems|serious|several|she|should|show|side|since|sincere|six|sixty|so|some|somehow|someone|
something|sometime|sometimes|somewhere|still|such|system|take|ten|than|that|the|their|them|themselves|then|thence|
there|thereafter|thereby|therefore|therein|thereupon|these|they|thick|thin|third|this|those|though|three|through|
throughout|thru|thus|to|together|too|top|toward|towards|twelve|twenty|two|un|under|until|up|upon|us|very|via|was|
we|well|were|what|whatever|when|whence|whenever|where|whereafter|whereas|whereby|wherein|whereupon|wherever|whether|
which|while|whither|who|whoever|whole|whom|whose|why|will|with|within|without|would|yet|you|your|yours|yourself|
yourselves)\b"""

stop_words_list = re.compile(STOP_WORDS, re.IGNORECASE)


# Leveshtein.
#
# Copyright (C) 2009 Thadeus Burgess
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

class Levenshtein():
    def __init__(self):
        pass

    @staticmethod
    def length(a,b):
        """
        Calculates the Levenshtein distance between a and b.
        """
        n, m = len(a), len(b)
        if n > m:
            # Make sure n <= m, to use O(min(n,m)) space
            a,b = b,a
            n,m = m,n

        current = range(n+1)
        for i in range(1,m+1):
            previous, current = current, [i]+[0]*n
            for j in range(1,n+1):
                add, delete = previous[j]+1, current[j-1]+1
                change = previous[j-1]
                if a[j-1] != b[i-1]:
                    change = change + 1
                current[j] = min(add, delete, change)

        return current[n]

    @staticmethod
    def suggestion(original, searchable, number_of_matches = 3):
        """
        Compares a string to a list a strings and returns
        list of the closes matches.
        """
        distances = []

        for txt in searchable:
            set = (Levenshtein.length(original, txt), txt)
            distances.append(set)

        distances.sort()
        return distances[0:number_of_matches]

# NCD
#
# Author: Francisco Ribeiro <francisco.gtr@gmail.com>
#

def ncd(key1, key2):
    """
    Performs an NCD (Normalized Compression Distance) comparison between two keys.

    You can read some documentation on the algorithm here: http://www.sophos.com/blogs/sophoslabs/?p=188

    These can either be the contents of a file or search terms.

    This will be a float value between 0.0 and 1.1, where the lower the value the
    closer in similarity.

    :key1: First value to compare, must be compressable
    :key2: Second value to compare, must be compressable.

    >>> key1 = "h3ll0"
    >>> key2 = "hello"
    >>> key3 = "lehlo"
    >>> key4 = "aeiou"

    >>> ncd(key1, key2)
    0.071428571428571425
    >>> ncd(key2, key3)
    0.024390243902439025
    >>> ncd(key3, key4)
    0.11904761904761904
    >>> ncd(key1, key3)
    0.095238095238095233
    >>> ncd(key1, key4)
    0.16666666666666666
    >>> ncd(key2, key4)
    0.095238095238095233
    """

    key3 = key1 + key2
    
    ck1 = bz2.compress(key1)
    ck2 = bz2.compress(key2)
    ck3 = bz2.compress(key3)
    
    n = float((len(ck3) - min(len(ck1), len(ck2)))) / float(max(len(ck1), len(ck2)))

    return n

#######################################################################
#######################################################################
################                                     ##################
################            NGRAM                    ##################
################                                     ##################
################     Trigram String Compare.         ##################
################     By Michel Albert                ##################
################                                     ##################
#######################################################################
#######################################################################

# This is part of "ngram". A Python module to compute the similarity between
# strings
# Copyright (C) 2005   Michel Albert
#
# This library is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#

import pprint
from types import BooleanType
from types import FloatType
from types import IntType
from types import ListType
from types import StringType

class Ngram():
    """ Used to compute similarities between strings. Can easily be used to
    compare one string to a whole batch of strings or pick the best string out
    of a list

    This code was *largely* inspired by String::Trigram by Tarek Ahmed. Actually
    I just translated it to python ;)

    You can find the original Perl-Module at
    http://search.cpan.org/dist/String-Trigram/
   """

    def __init__(self, haystack, **kwargs):
        """
        Constructor

        PARAMETERS::

            haystack - String or list of strings. This is where we will look for
                       matches

        OPTIONAL PARAMETERS::

            min_sim     - minimum similarity score for a string to be considered
                          worthy. Default = 0.0
            warp        - If warp > 1 short strings are getting away better, if
                          warp < 1 they are getting away worse. Default = 1.0
            ic          - Ignore case? Default = False
            only_alnum  - Only consider alphanumeric characters? Default = False
            ngram_len   - n-gram size. Default = 3 (trigram)
            padding     - padding size. Default = ngram_len - 1
            noise       - noise characters that should be ignored when comparing

      """

        self.__min_sim    = 0.0
        self.__warp       = 1.0
        self.__ic         = False     # ignore case
        self.__only_alnum = False
        self.__noise      = ''
        self.__debug      = False
        self.__ngram_len  = 3
        self.__padding    = self.__ngram_len - 1

        if kwargs.has_key('min_sim'):    self.min_sim(kwargs['min_sim'])
        if kwargs.has_key('warp'):       self.warp(kwargs['warp'])
        if kwargs.has_key('ic'):         self.ic(kwargs['ic'])
        if kwargs.has_key('only_alnum'): self.only_alnum(kwargs['only_alnum'])
        if kwargs.has_key('ngram_len'):  self.ngram_len(kwargs['ngram_len'])
        if kwargs.has_key('padding'):    self.padding(kwargs['padding'])
        if kwargs.has_key('noise'):      self.noise(kwargs['noise'])

        if type(haystack) is ListType:
            self.__ngram_index = self.ngramify(haystack)
        else:
            raise TypeError, "Comparison base must be a list of strings"

    def ngramify(self, haystack, ic = None, only_alnum = None, padding = None, noise = None):
        """
        Takes list of strings and puts them into an index of ngrams. KEY is a
        ngram, VALUE a list of strings containing that ngram. VALUE has two KEYS:
           grams: count of ngram occurring in string
           len:   length of string with padding (if ignoring non alphanumerics,
                this gets determined after those characters have been removed)

        PARAMETERS:
           haystack    - List of strings to be indexed
           ic          - Ignore Case?
           only_alnum  - Only alphanumeric charactes?
           padding     - Size of the padding
           noise       - Noise characters that should be removed

        RETURNS:
           N-Gram index

            Structure:
           {
              'abc': 'string1':{'grams':0, 'len':11},
              'bcd': 'string2':{'grams':0, 'len':11},
              'ing': 'string3':{'grams':1, 'len':11},
              ...
           }
         
        """
        if ic is None:          ic = self.__ic
        if only_alnum is None:  only_alnum = self.__only_alnum
        if padding is None:     padding = 'X' * self.__padding
        if noise is None:       noise   = self.__noise

        seen  = {}
        grams = {}

        for string in haystack:
            tmpstr = string
            if only_alnum: raise NotImplementedError
            if ic:         tmpstr = tmpstr.lower()
            for char in noise:
                tmpstr = tmpstr.replace(char, '')
            if seen.has_key(tmpstr): continue
            seen[tmpstr] = 1

            tmpstr = padding + tmpstr + padding
            length = len(tmpstr)
            for i in xrange(length - self.__ngram_len + 1):
                ngram = tmpstr[i:i + self.__ngram_len]

                if not grams.has_key(ngram):
                    grams[ngram] = {string: {'grams':0, 'len': 0}}
                if not grams[ngram].has_key(string):
                    grams[ngram][string] = {'grams':0, 'len': 0}
                grams[ngram][string]['grams'] += 1
                grams[ngram][string]['len']   += length

        return grams

    def reInit(self, base):
        """
      Reinitialises the search space.

      PARAMETERS:
         base - The new search space
      """
        if type(base) is not ListType:
            raise NotImplementedError, "Only lists are supported as comparison base!"
        self.__ngram_index = self.ngramify(base)
    re_init = reInit

    def getSimilarStrings(self, string):
        """
      Retrieves all strings that have a similarity higher than min_sim with
      "string"

      PARAMETERS:
         - string:   The string to compare with the search space

      RETURNS:
         Dictionary of scoring strings.
         Example output:

         {'askfjwehiuasdfji': 1.0, 'asdfawe': 0.17391304347826086}
      """
        ngram_buf = {}

        # KEY = potentially similar string, VALUE = number of identical ngrams
        siminfo     = {}

        if self.__only_alnum: raise NotImplementedError
        if self.__ic:         string = string.lower()
        for char in self.__noise:
            string = string.replace(char, '')
        string = 'X' * self.__padding + string + 'X' * self.__padding

        numgram = len(string) - self.__ngram_len + 1

        for i in xrange(numgram):
            ngram = string[i:i + self.__ngram_len]
            if not self.__ngram_index.has_key(ngram): continue
            matches = self.__ngram_index[ngram]

            for match in matches:
                actName = match
                actMatch = matches[match]
                ngram_count = actMatch['grams']
                if not ngram_buf.has_key(ngram): ngram_buf[ngram] = {}
                if not ngram_buf[ngram].has_key(actName):
                    ngram_buf[ngram][actName] = ngram_count
                if ngram_buf[ngram][actName] > 0:
                    ngram_buf[ngram][actName] -= 1
                    if not siminfo.has_key(actName): siminfo[actName] = {'name': 0, 'len':0}
                    siminfo[actName]['name'] += 1
                    siminfo[actName]['len'] = actMatch['len']

        return self.computeSimilarity(string, siminfo)
    get_similar_strings = getSimilarStrings

    def computeSimilarity(self, string, siminfo):
        """
      Calculates the similarity of the given some information about n-grams.
      PARAMETERS:
         string   - This is what we want to get the score of
         siminfo  - A dictionary containing info about n-gram distribution.
                    (see getSimilarStrings)
      RETURNS:
         the score as float
      """
        result = {}
        strCount = 0
        allgrams = 0
        samegrams = 0
        actSim = 0
        length = len(string)
        for key in siminfo:
            samegrams = siminfo[key]['name']
            allgrams = length + siminfo[key]['len'] - 2 * self.__ngram_len - samegrams + 2;
            actSim = self.computeActSimOld(samegrams, allgrams)

            if actSim > self.__min_sim:
                result[key] = actSim

        return result
    compute_similarity = computeSimilarity

    def computeActSimOld(self, samegrams, allgrams, warp = None):
        """
      Computes the similarity score between two sets of n-grams according to
      the following formula:

      (a = all trigrams, d = different trigrams, e = warp)

      (a**e - d**e)/a**e

      PARAMETERS:
         samegrams   - n-grams that were found in the string
         allgrams    - All n-grams in the search space
         warp        - the warp factor. See __init__ for explanation

      RETURNS:
         Similarity score as float

      """
        diffgrams   = -1
        actSim      = -1

        if warp is None: warp = self.__warp

        if warp == 1:
            actSim = float(samegrams) / allgrams
        else:
            diffgrams = allgrams - samegrams
            actSim = ((allgrams ** warp) - (diffgrams ** warp)) / (allgrams ** warp)
        return actSim
    compute_act_sim_old = computeActSimOld

    def getBestMatch(self, needle, count = 1):
        """
      Returns the best match for the given string

      PARAMETERS:
         needle:  The string to search for
         count:     How many results to return

      RETURNS:
         String that best matched the supplied parameter and the score with
         which it matched.
      """

        if type(needle) is not StringType: raise TypeError, "needle must be of type string!"
        if type(count)  is not IntType: raise TypeError, "count must be of type int!"

        # convert the dictionary into a list of tuples
        temp = self.getSimilarStrings(needle).items()

        # sort the resulting list by the second field
        temp.sort(cmp = lambda x, y: cmp(y[1], x[1]))

        # return the top <count> items from the list
        return temp[:count]
    get_best_match = getBestMatch

    def min_sim(self, * args):

        if len(args) == 0: return self.__min_sim

        if type(args[0]) is not FloatType:
            raise TypeError, "min_sim must be a float"
        if args[0] < 0 or args[0] > 1:
            raise ValueError, "min_sim must range between 0 and 1"
        self.__min_sim = args[0]

    def warp(self, * args):

        if len(args) == 0: return self.__warp

        if type(args[0]) is not FloatType:
            raise TypeError, "warp must be a float"
        if args[0] < 0:
            raise ValueError, "warp must be bigger than 1"
        self.__warp = args[0]

    def ic(self, * args):

        if len(args) == 0: return self.__ic

        if type(args[0]) is not BooleanType:
            raise TypeError, "ic must be a boolean"
        self.__ic = args[0]

    def only_alnum(self, * args):

        if len(args) == 0: return self.__only_alnum

        if type(args[0]) is not BooleanType:
            raise TypeError, "only_alnum must be a boolean"
        self.__only_alnum = args[0]

    def noise(self, * args):

        if len(args) == 0: return self.__noise

        if type(args[0]) is not StringType:
            raise TypeError, "noise must be a string"
        self.__noise = args[0]

    def ngram_len(self, * args):

        if len(args) == 0: return self.__ngram_len

        if type(args[0]) is not IntType:
            raise TypeError, "ngram_len must be an integer "
        if args[0] < 0:
            raise ValueError, "ngram_len must be bigger than 1"
        self.__ngram_len = args[0]

    def padding(self, * args):

        if len(args) == 0: return self.__padding

        if type(args[0]) is not IntType:
            raise TypeError, "padding must be an integer "
        if args[0] < 0:
            raise ValueError, "padding must be bigger than 1"
        self.__ngram_len = args[0]

    def compare(self, s1, s2):
        """
      Simply compares two strings and returns the similarity score.

      This is a class method. It can be called without instantiating
      the ngram class first. Example:

      >> ngram = Ngram()
      >> ngram.compare('sfewefsf', 'sdfafwgah')
      >> 0.050000000000000003

      PARAMETERS:
         s1 -  First string
         s2 -  Last string

      """
        if s1 is None or s2 is None:
            if s1 == s2: return 1.0
            else: return 0.0

        result = ngram([s1]).getSimilarStrings(s2)
        if result == {}: return 0.0
        else: return result[s1]
    compare = classmethod(compare)

if __name__ == "__main__":


    # A simple example
    #base = ['sdafaf', 'asfwef', 'asdfawe', 'adfwe', 'askfjwehiuasdfji']
    #tg = ngram(base, min_sim = 0.0)

    #pprint.pprint(tg.getSimilarStrings('askfjwehiuasdfji'))
    #print
    #pprint.pprint(ngram.compare('sdfeff', 'sdfeff'))
    #print
    #pprint.pprint(tg.getBestMatch('afadfwe', 2))

    import doctest
    doctest.testmod()
