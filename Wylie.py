# -*- coding: utf-8 -*-
# pylint: disable=too-many-function-args

from __future__ import print_function
import re
#  This Python package implements the conversion between Unicode Tibetan text, and
#  Wylie (EWTS) transliteration.
#  It is based on the equivalent Java module, found at
#  http://www.thlib.org/reference/transliteration/wyconverter.php
#  and includes numerous bugfixes for cases for which the original tool was failing
#
#  The Extended Wylie Transliteration System is documented at:
#  http://www.thlib.org/reference/transliteration/#essay=/thl/ewts/


class Wylie(object):
    #  various options for Wylie conversion
    check = bool()
    check_strict = bool()
    print_warnings = bool()
    fix_spacing = bool()

    #  constant hashes and sets to help with the conversion
    m_consonant = {}
    m_subjoined = {}
    m_vowel = {}
    m_final_uni = {}
    m_final_class = {}
    m_other = {}
    m_ambiguous_wylie = {}
    m_tib_vowel_long = {}
    m_tib_caret = {}
    m_tib_top = {}
    m_tib_subjoined = {}
    m_tib_vowel = {}
    m_tib_final_wylie = {}
    m_tib_final_class = {}
    m_tib_other = {}
    m_ambiguous_key = {}
    m_tokens_start = {}
    m_special = []
    m_suffixes = []
    m_tib_stacks = []
    m_tokens = []
    m_superscripts = {}
    m_subscripts = {}
    m_prefixes = {}
    m_suff2 = {}

    #  initialize all the hashes with the correspondences between Wylie and Unicode.
    #  this gets called from a 'static section' to initialize the hashes the moment the
    #  class gets loaded.
    @classmethod
    def initHashes(self):
        tmpSet = None
        #  *** Wylie to Unicode mappings ***
        #  list of wylie consonant => unicode
        self.m_consonant = {
            "k": u"\u0f40",
            "kh": u"\u0f41",
            "g": u"\u0f42",
            "gh": u"\u0f42\u0fb7",
            "g+h": u"\u0f42\u0fb7",
            "ng": u"\u0f44",
            "c": u"\u0f45",
            "ch": u"\u0f46",
            "j": u"\u0f47",
            "ny": u"\u0f49",
            "T": u"\u0f4a",
            "-t": u"\u0f4a",
            "Th": u"\u0f4b",
            "-th": u"\u0f4b",
            "D": u"\u0f4c",
            "-d": u"\u0f4c",
            "Dh": u"\u0f4c\u0fb7",
            "D+h": u"\u0f4c\u0fb7",
            "-dh": u"\u0f4c\u0fb7",
            "-d+h": u"\u0f4c\u0fb7",
            "N": u"\u0f4e",
            "-n": u"\u0f4e",
            "t": u"\u0f4f",
            "th": u"\u0f50",
            "d": u"\u0f51",
            "dh": u"\u0f51\u0fb7",
            "d+h": u"\u0f51\u0fb7",
            "n": u"\u0f53",
            "p": u"\u0f54",
            "ph": u"\u0f55",
            "b": u"\u0f56",
            "bh": u"\u0f56\u0fb7",
            "b+h": u"\u0f56\u0fb7",
            "m": u"\u0f58",
            "ts": u"\u0f59",
            "tsh": u"\u0f5a",
            "dz": u"\u0f5b",
            "dzh": u"\u0f5b\u0fb7",
            "dz+h": u"\u0f5b\u0fb7",
            "w": u"\u0f5d",
            "zh": u"\u0f5e",
            "z": u"\u0f5f",
            "'": u"\u0f60",
            u"\u2018": u"\u0f60",
            #  typographic quotes
            u"\u2019": u"\u0f60",
            "y": u"\u0f61",
            "r": u"\u0f62",
            "l": u"\u0f63",
            "sh": u"\u0f64",
            "Sh": u"\u0f65",
            "-sh": u"\u0f65",
            "s": u"\u0f66",
            "h": u"\u0f67",
            "W": u"\u0f5d",
            "Y": u"\u0f61",
            "R": u"\u0f6a",
            "f": u"\u0f55\u0f39",
            "v": u"\u0f56\u0f39"
        }

        #  subjoined letters
        self.m_subjoined = {
            "k": u"\u0f90",
            "kh": u"\u0f91",
            "g": u"\u0f92",
            "gh": u"\u0f92\u0fb7",
            "g+h": u"\u0f92\u0fb7",
            "ng": u"\u0f94",
            "c": u"\u0f95",
            "ch": u"\u0f96",
            "j": u"\u0f97",
            "ny": u"\u0f99",
            "T": u"\u0f9a",
            "-t": u"\u0f9a",
            "Th": u"\u0f9b",
            "-th": u"\u0f9b",
            "D": u"\u0f9c",
            "-d": u"\u0f9c",
            "Dh": u"\u0f9c\u0fb7",
            "D+h": u"\u0f9c\u0fb7",
            "-dh": u"\u0f9c\u0fb7",
            "-d+h": u"\u0f9c\u0fb7",
            "N": u"\u0f9e",
            "-n": u"\u0f9e",
            "t": u"\u0f9f",
            "th": u"\u0fa0",
            "d": u"\u0fa1",
            "dh": u"\u0fa1\u0fb7",
            "d+h": u"\u0fa1\u0fb7",
            "n": u"\u0fa3",
            "p": u"\u0fa4",
            "ph": u"\u0fa5",
            "b": u"\u0fa6",
            "bh": u"\u0fa6\u0fb7",
            "b+h": u"\u0fa6\u0fb7",
            "m": u"\u0fa8",
            "ts": u"\u0fa9",
            "tsh": u"\u0faa",
            "dz": u"\u0fab",
            "dzh": u"\u0fab\u0fb7",
            "dz+h": u"\u0fab\u0fb7",
            "w": u"\u0fad",
            "zh": u"\u0fae",
            "z": u"\u0faf",
            "'": u"\u0fb0",
            u"\u2018": u"\u0fb0",
            #  typographic quotes
            u"\u2019": u"\u0fb0",
            "y": u"\u0fb1",
            "r": u"\u0fb2",
            "l": u"\u0fb3",
            "sh": u"\u0fb4",
            "Sh": u"\u0fb5",
            "-sh": u"\u0fb5",
            "s": u"\u0fb6",
            "h": u"\u0fb7",
            "a": u"\u0fb8",
            "W": u"\u0fba",
            "Y": u"\u0fbb",
            "R": u"\u0fbc"
        }

        #  vowels
        self.m_vowel = {
            "a": u"\u0f68",
            "A": u"\u0f71",
            "i": u"\u0f72",
            "I": u"\u0f71\u0f72",
            "u": u"\u0f74",
            "U": u"\u0f71\u0f74",
            "e": u"\u0f7a",
            "ai": u"\u0f7b",
            "o": u"\u0f7c",
            "au": u"\u0f7d",
            "-i": u"\u0f80",
            "-I": u"\u0f71\u0f80"
        }

        #  final symbols to unicode
        self.m_final_uni = {
            "M": u"\u0f7e",
            "~M`": u"\u0f82",
            "~M": u"\u0f83",
            "X": u"\u0f37",
            "~X": u"\u0f35",
            "H": u"\u0f7f",
            "?": u"\u0f84",
            "^": u"\u0f39"
        }

        #  final symbols organized by class
        self.m_final_class = {
            "M": "M",
            "~M`": "M",
            "~M": "M",
            "X": "X",
            "~X": "X",
            "H": "H",
            "?": "?",
            "^": "^"
        }

        #  other stand-alone symbols
        self.m_other = {
            "0": u"\u0f20",
            "1": u"\u0f21",
            "2": u"\u0f22",
            "3": u"\u0f23",
            "4": u"\u0f24",
            "5": u"\u0f25",
            "6": u"\u0f26",
            "7": u"\u0f27",
            "8": u"\u0f28",
            "9": u"\u0f29",
            " ": u"\u0f0b",
            "*": u"\u0f0c",
            "/": u"\u0f0d",
            "//": u"\u0f0e",
            ";": u"\u0f0f",
            "|": u"\u0f11",
            "!": u"\u0f08",
            ":": u"\u0f14",
            "_": " ",
            "=": u"\u0f34",
            "<": u"\u0f3a",
            ">": u"\u0f3b",
            "(": u"\u0f3c",
            ")": u"\u0f3d",
            "@": u"\u0f04",
            "#": u"\u0f05",
            "$": u"\u0f06",
            "%": u"\u0f07"
        }
        #  special characters: flag those if they occur out of context
        self.m_special = []
        self.m_special.append(".")
        self.m_special.append("+")
        self.m_special.append("-")
        self.m_special.append("~")
        self.m_special.append("^")
        self.m_special.append("?")
        self.m_special.append("`")
        self.m_special.append("]")
        # superscripts: hashmap of superscript => set of letters or stacks
        # below
        self.m_superscripts = {"r": [], "l": [], "s": []}

        tmpSet = []
        self.m_superscripts["r"].append("k")
        self.m_superscripts["r"].append("g")
        self.m_superscripts["r"].append("ng")
        self.m_superscripts["r"].append("j")
        self.m_superscripts["r"].append("ny")
        self.m_superscripts["r"].append("t")
        self.m_superscripts["r"].append("d")
        self.m_superscripts["r"].append("n")
        self.m_superscripts["r"].append("b")
        self.m_superscripts["r"].append("m")
        self.m_superscripts["r"].append("ts")
        self.m_superscripts["r"].append("dz")
        self.m_superscripts["r"].append("k+y")
        self.m_superscripts["r"].append("g+y")
        self.m_superscripts["r"].append("m+y")
        self.m_superscripts["r"].append("b+w")
        self.m_superscripts["r"].append("ts+w")
        self.m_superscripts["r"].append("g+w")

        tmpSet = []
        self.m_superscripts["l"].append("k")
        self.m_superscripts["l"].append("g")
        self.m_superscripts["l"].append("ng")
        self.m_superscripts["l"].append("c")
        self.m_superscripts["l"].append("j")
        self.m_superscripts["l"].append("t")
        self.m_superscripts["l"].append("d")
        self.m_superscripts["l"].append("p")
        self.m_superscripts["l"].append("b")
        self.m_superscripts["l"].append("h")

        self.m_superscripts["s"].append("k")
        self.m_superscripts["s"].append("g")
        self.m_superscripts["s"].append("ng")
        self.m_superscripts["s"].append("ny")
        self.m_superscripts["s"].append("t")
        self.m_superscripts["s"].append("d")
        self.m_superscripts["s"].append("n")
        self.m_superscripts["s"].append("p")
        self.m_superscripts["s"].append("b")
        self.m_superscripts["s"].append("m")
        self.m_superscripts["s"].append("ts")
        self.m_superscripts["s"].append("k+y")
        self.m_superscripts["s"].append("g+y")
        self.m_superscripts["s"].append("p+y")
        self.m_superscripts["s"].append("b+y")
        self.m_superscripts["s"].append("m+y")
        self.m_superscripts["s"].append("k+r")
        self.m_superscripts["s"].append("g+r")
        self.m_superscripts["s"].append("p+r")
        self.m_superscripts["s"].append("b+r")
        self.m_superscripts["s"].append("m+r")
        self.m_superscripts["s"].append("n+r")

        #  subscripts => set of letters above
        self.m_subscripts = {"y": [], "r": [], "l": [], "w": []}

        self.m_subscripts["y"].append("k")
        self.m_subscripts["y"].append("kh")
        self.m_subscripts["y"].append("g")
        self.m_subscripts["y"].append("p")
        self.m_subscripts["y"].append("ph")
        self.m_subscripts["y"].append("b")
        self.m_subscripts["y"].append("m")
        self.m_subscripts["y"].append("r+k")
        self.m_subscripts["y"].append("r+g")
        self.m_subscripts["y"].append("r+m")
        self.m_subscripts["y"].append("s+k")
        self.m_subscripts["y"].append("s+g")
        self.m_subscripts["y"].append("s+p")
        self.m_subscripts["y"].append("s+b")
        self.m_subscripts["y"].append("s+m")

        self.m_subscripts["r"].append("k")
        self.m_subscripts["r"].append("kh")
        self.m_subscripts["r"].append("g")
        self.m_subscripts["r"].append("t")
        self.m_subscripts["r"].append("th")
        self.m_subscripts["r"].append("d")
        self.m_subscripts["r"].append("n")
        self.m_subscripts["r"].append("p")
        self.m_subscripts["r"].append("ph")
        self.m_subscripts["r"].append("b")
        self.m_subscripts["r"].append("m")
        self.m_subscripts["r"].append("sh")
        self.m_subscripts["r"].append("s")
        self.m_subscripts["r"].append("h")
        self.m_subscripts["r"].append("dz")
        self.m_subscripts["r"].append("s+k")
        self.m_subscripts["r"].append("s+g")
        self.m_subscripts["r"].append("s+p")
        self.m_subscripts["r"].append("s+b")
        self.m_subscripts["r"].append("s+m")
        self.m_subscripts["r"].append("s+n")

        self.m_subscripts["l"].append("k")
        self.m_subscripts["l"].append("g")
        self.m_subscripts["l"].append("b")
        self.m_subscripts["l"].append("r")
        self.m_subscripts["l"].append("s")
        self.m_subscripts["l"].append("z")

        self.m_subscripts["w"].append("k")
        self.m_subscripts["w"].append("kh")
        self.m_subscripts["w"].append("g")
        self.m_subscripts["w"].append("c")
        self.m_subscripts["w"].append("ny")
        self.m_subscripts["w"].append("t")
        self.m_subscripts["w"].append("d")
        self.m_subscripts["w"].append("ts")
        self.m_subscripts["w"].append("tsh")
        self.m_subscripts["w"].append("zh")
        self.m_subscripts["w"].append("z")
        self.m_subscripts["w"].append("r")
        self.m_subscripts["w"].append("l")
        self.m_subscripts["w"].append("sh")
        self.m_subscripts["w"].append("s")
        self.m_subscripts["w"].append("h")
        self.m_subscripts["w"].append("g+r")
        self.m_subscripts["w"].append("d+r")
        self.m_subscripts["w"].append("ph+y")
        self.m_subscripts["w"].append("r+g")
        self.m_subscripts["w"].append("r+ts")

        #  prefixes => set of consonants or stacks after
        self.m_prefixes = {"g": [], "d": [], "b": [],
                           "m": [], "'": [], u"\u2018": [], u"\u2019": []}
        tmpSet = []
        tmpSet.append("c")
        tmpSet.append("ny")
        tmpSet.append("t")
        tmpSet.append("d")
        tmpSet.append("n")
        tmpSet.append("ts")
        tmpSet.append("zh")
        tmpSet.append("z")
        tmpSet.append("y")
        tmpSet.append("sh")
        tmpSet.append("s")
        self.m_prefixes["g"] = tmpSet

        tmpSet = []
        tmpSet.append("k")
        tmpSet.append("g")
        tmpSet.append("ng")
        tmpSet.append("p")
        tmpSet.append("b")
        tmpSet.append("m")
        tmpSet.append("k+y")
        tmpSet.append("g+y")
        tmpSet.append("p+y")
        tmpSet.append("b+y")
        tmpSet.append("m+y")
        tmpSet.append("k+r")
        tmpSet.append("g+r")
        tmpSet.append("p+r")
        tmpSet.append("b+r")
        self.m_prefixes["d"] = tmpSet

        tmpSet = []
        tmpSet.append("k")
        tmpSet.append("g")
        tmpSet.append("c")
        tmpSet.append("t")
        tmpSet.append("d")
        tmpSet.append("ts")
        tmpSet.append("zh")
        tmpSet.append("z")
        tmpSet.append("sh")
        tmpSet.append("s")
        tmpSet.append("r")
        tmpSet.append("l")
        tmpSet.append("k+y")
        tmpSet.append("g+y")
        tmpSet.append("k+r")
        tmpSet.append("g+r")
        tmpSet.append("r+l")
        tmpSet.append("s+l")
        tmpSet.append("r+k")
        tmpSet.append("r+g")
        tmpSet.append("r+ng")
        tmpSet.append("r+j")
        tmpSet.append("r+ny")
        tmpSet.append("r+t")
        tmpSet.append("r+d")
        tmpSet.append("r+n")
        tmpSet.append("r+ts")
        tmpSet.append("r+dz")
        tmpSet.append("s+k")
        tmpSet.append("s+g")
        tmpSet.append("s+ng")
        tmpSet.append("s+ny")
        tmpSet.append("s+t")
        tmpSet.append("s+d")
        tmpSet.append("s+n")
        tmpSet.append("s+ts")
        tmpSet.append("r+k+y")
        tmpSet.append("r+g+y")
        tmpSet.append("s+k+y")
        tmpSet.append("s+g+y")
        tmpSet.append("s+k+r")
        tmpSet.append("s+g+r")
        tmpSet.append("l+d")
        tmpSet.append("l+t")
        tmpSet.append("k+l")
        tmpSet.append("s+r")
        tmpSet.append("z+l")
        tmpSet.append("s+w")
        self.m_prefixes["b"] = tmpSet

        tmpSet = []
        tmpSet.append("kh")
        tmpSet.append("g")
        tmpSet.append("ng")
        tmpSet.append("ch")
        tmpSet.append("j")
        tmpSet.append("ny")
        tmpSet.append("th")
        tmpSet.append("d")
        tmpSet.append("n")
        tmpSet.append("tsh")
        tmpSet.append("dz")
        tmpSet.append("kh+y")
        tmpSet.append("g+y")
        tmpSet.append("kh+r")
        tmpSet.append("g+r")
        self.m_prefixes["m"] = tmpSet

        tmpSet = []
        tmpSet.append("kh")
        tmpSet.append("g")
        tmpSet.append("ch")
        tmpSet.append("j")
        tmpSet.append("th")
        tmpSet.append("d")
        tmpSet.append("ph")
        tmpSet.append("b")
        tmpSet.append("tsh")
        tmpSet.append("dz")
        tmpSet.append("kh+y")
        tmpSet.append("g+y")
        tmpSet.append("ph+y")
        tmpSet.append("b+y")
        tmpSet.append("kh+r")
        tmpSet.append("g+r")
        tmpSet.append("d+r")
        tmpSet.append("ph+r")
        tmpSet.append("b+r")
        self.m_prefixes["'"] = tmpSet
        self.m_prefixes[u"\u2018"] = tmpSet
        self.m_prefixes[u"\u2019"] = tmpSet

        #  set of suffix letters
        # also included are some Skt letters b/c they occur often in suffix
        # position in Skt words
        self.m_suffixes = []
        self.m_suffixes.append("'")
        self.m_suffixes.append(u"\u2018")
        self.m_suffixes.append(u"\u2019")
        self.m_suffixes.append("g")
        self.m_suffixes.append("ng")
        self.m_suffixes.append("d")
        self.m_suffixes.append("n")
        self.m_suffixes.append("b")
        self.m_suffixes.append("m")
        self.m_suffixes.append("r")
        self.m_suffixes.append("l")
        self.m_suffixes.append("s")
        self.m_suffixes.append("N")
        self.m_suffixes.append("T")
        self.m_suffixes.append("-n")
        self.m_suffixes.append("-t")
        #  suffix2 => set of letters before
        self.m_suff2 = {"s": [], "d": []}

        tmpSet = []
        tmpSet.append("g")
        tmpSet.append("ng")
        tmpSet.append("b")
        tmpSet.append("m")
        self.m_suff2["s"] = tmpSet

        tmpSet = []
        tmpSet.append("n")
        tmpSet.append("r")
        tmpSet.append("l")
        self.m_suff2["d"] = tmpSet

        #  root letter index for very ambiguous three-stack syllables
        self.m_ambiguous_key = {
            "dgs": 1,
            "dms": 1,
            "'gs": 1,
            "mngs": 0,
            "bgs": 0,
            "dbs": 1
        }

        self.m_ambiguous_wylie = {
            "dgs": "dgas",
            "dms": "dmas",
            "'gs": "'gas",
            "mngs": "mangs",
            "bgs": "bags",
            "dbs": "dbas"
        }
        #  *** Unicode to Wylie mappings ***
        #  top letters
        self.m_tib_top = {
            u'\u0f40': "k",
            u'\u0f41': "kh",
            u'\u0f42': "g",
            u'\u0f43': "g+h",
            u'\u0f44': "ng",
            u'\u0f45': "c",
            u'\u0f46': "ch",
            u'\u0f47': "j",
            u'\u0f49': "ny",
            u'\u0f4a': "T",
            u'\u0f4b': "Th",
            u'\u0f4c': "D",
            u'\u0f4d': "D+h",
            u'\u0f4e': "N",
            u'\u0f4f': "t",
            u'\u0f50': "th",
            u'\u0f51': "d",
            u'\u0f52': "d+h",
            u'\u0f53': "n",
            u'\u0f54': "p",
            u'\u0f55': "ph",
            u'\u0f56': "b",
            u'\u0f57': "b+h",
            u'\u0f58': "m",
            u'\u0f59': "ts",
            u'\u0f5a': "tsh",
            u'\u0f5b': "dz",
            u'\u0f5c': "dz+h",
            u'\u0f5d': "w",
            u'\u0f5e': "zh",
            u'\u0f5f': "z",
            u'\u0f60': "'",
            u'\u0f61': "y",
            u'\u0f62': "r",
            u'\u0f63': "l",
            u'\u0f64': "sh",
            u'\u0f65': "Sh",
            u'\u0f66': "s",
            u'\u0f67': "h",
            u'\u0f68': "a",
            u'\u0f69': "k+Sh",
            u'\u0f6a': "R"
        }
        #  subjoined letters
        self.m_tib_subjoined = {
            u'\u0f90': "k",
            u'\u0f91': "kh",
            u'\u0f92': "g",
            u'\u0f93': "g+h",
            u'\u0f94': "ng",
            u'\u0f95': "c",
            u'\u0f96': "ch",
            u'\u0f97': "j",
            u'\u0f99': "ny",
            u'\u0f9a': "T",
            u'\u0f9b': "Th",
            u'\u0f9c': "D",
            u'\u0f9d': "D+h",
            u'\u0f9e': "N",
            u'\u0f9f': "t",
            u'\u0fa0': "th",
            u'\u0fa1': "d",
            u'\u0fa2': "d+h",
            u'\u0fa3': "n",
            u'\u0fa4': "p",
            u'\u0fa5': "ph",
            u'\u0fa6': "b",
            u'\u0fa7': "b+h",
            u'\u0fa8': "m",
            u'\u0fa9': "ts",
            u'\u0faa': "tsh",
            u'\u0fab': "dz",
            u'\u0fac': "dz+h",
            u'\u0fad': "w",
            u'\u0fae': "zh",
            u'\u0faf': "z",
            u'\u0fb0': "'",
            u'\u0fb1': "y",
            u'\u0fb2': "r",
            u'\u0fb3': "l",
            u'\u0fb4': "sh",
            u'\u0fb5': "Sh",
            u'\u0fb6': "s",
            u'\u0fb7': "h",
            u'\u0fb8': "a",
            u'\u0fb9': "k+Sh",
            u'\u0fba': "W",
            u'\u0fbb': "Y",
            u'\u0fbc': "R"
        }
        #  vowel signs:
        #  a-chen is not here because that's a top character, not a vowel sign.
        #  pre-composed "I" and "U" are dealt here; other pre-composed Skt vowels are more
        # easily handled by a global replace in toWylie(), b/c they turn into
        # subjoined "r"/"l".
        self.m_tib_vowel = {
            u'\u0f71': "A",
            u'\u0f72': "i",
            u'\u0f73': "I",
            u'\u0f74': "u",
            u'\u0f75': "U",
            u'\u0f7a': "e",
            u'\u0f7b': "ai",
            u'\u0f7c': "o",
            u'\u0f7d': "au",
            u'\u0f80': "-i"
        }
        #  long (Skt) vowels
        self.m_tib_vowel_long = {
            "i": "I",
            "u": "U",
            "-i": "-I"
        }

        #  final symbols => wylie
        self.m_tib_final_wylie = {
            u'\u0f7e': "M",
            u'\u0f82': "~M`",
            u'\u0f83': "~M",
            u'\u0f37': "X",
            u'\u0f35': "~X",
            u'\u0f39': "^",
            u'\u0f7f': "H",
            u'\u0f84': "?"
        }
        #  final symbols by class
        self.m_tib_final_class = {
            u'\u0f7e': "M",
            u'\u0f82': "M",
            u'\u0f83': "M",
            u'\u0f37': "X",
            u'\u0f35': "X",
            u'\u0f39': "^",
            u'\u0f7f': "H",
            u'\u0f84': "?"
        }
        #  special characters introduced by ^
        self.m_tib_caret = {
            "ph": "f",
            "b": "v",
        }
        #  other stand-alone characters
        self.m_tib_other = {
            ' ': "_",
            u'\u0f04': "@",
            u'\u0f05': "#",
            u'\u0f06': "$",
            u'\u0f07': "%",
            u'\u0f08': "!",
            u'\u0f0b': " ",
            u'\u0f0c': "*",
            u'\u0f0d': "/",
            u'\u0f0e': "//",
            u'\u0f0f': ";",
            u'\u0f11': "|",
            u'\u0f14': ":",
            u'\u0f20': "0",
            u'\u0f21': "1",
            u'\u0f22': "2",
            u'\u0f23': "3",
            u'\u0f24': "4",
            u'\u0f25': "5",
            u'\u0f26': "6",
            u'\u0f27': "7",
            u'\u0f28': "8",
            u'\u0f29': "9",
            u'\u0f34': "=",
            u'\u0f3a': "<",
            u'\u0f3b': ">",
            u'\u0f3c': "(",
            u'\u0f3d': ")",
        }
        #  all these stacked consonant combinations don't need "+"s in them
        self.m_tib_stacks = []
        self.m_tib_stacks.append("b+l")
        self.m_tib_stacks.append("b+r")
        self.m_tib_stacks.append("b+y")
        self.m_tib_stacks.append("c+w")
        self.m_tib_stacks.append("d+r")
        self.m_tib_stacks.append("d+r+w")
        self.m_tib_stacks.append("d+w")
        self.m_tib_stacks.append("dz+r")
        self.m_tib_stacks.append("g+l")
        self.m_tib_stacks.append("g+r")
        self.m_tib_stacks.append("g+r+w")
        self.m_tib_stacks.append("g+w")
        self.m_tib_stacks.append("g+y")
        self.m_tib_stacks.append("h+r")
        self.m_tib_stacks.append("h+w")
        self.m_tib_stacks.append("k+l")
        self.m_tib_stacks.append("k+r")
        self.m_tib_stacks.append("k+w")
        self.m_tib_stacks.append("k+y")
        self.m_tib_stacks.append("kh+r")
        self.m_tib_stacks.append("kh+w")
        self.m_tib_stacks.append("kh+y")
        self.m_tib_stacks.append("l+b")
        self.m_tib_stacks.append("l+c")
        self.m_tib_stacks.append("l+d")
        self.m_tib_stacks.append("l+g")
        self.m_tib_stacks.append("l+h")
        self.m_tib_stacks.append("l+j")
        self.m_tib_stacks.append("l+k")
        self.m_tib_stacks.append("l+ng")
        self.m_tib_stacks.append("l+p")
        self.m_tib_stacks.append("l+t")
        self.m_tib_stacks.append("l+w")
        self.m_tib_stacks.append("m+r")
        self.m_tib_stacks.append("m+y")
        self.m_tib_stacks.append("n+r")
        self.m_tib_stacks.append("ny+w")
        self.m_tib_stacks.append("p+r")
        self.m_tib_stacks.append("p+y")
        self.m_tib_stacks.append("ph+r")
        self.m_tib_stacks.append("ph+y")
        self.m_tib_stacks.append("ph+y+w")
        self.m_tib_stacks.append("r+b")
        self.m_tib_stacks.append("r+d")
        self.m_tib_stacks.append("r+dz")
        self.m_tib_stacks.append("r+g")
        self.m_tib_stacks.append("r+g+w")
        self.m_tib_stacks.append("r+g+y")
        self.m_tib_stacks.append("r+j")
        self.m_tib_stacks.append("r+k")
        self.m_tib_stacks.append("r+k+y")
        self.m_tib_stacks.append("r+l")
        self.m_tib_stacks.append("r+m")
        self.m_tib_stacks.append("r+m+y")
        self.m_tib_stacks.append("r+n")
        self.m_tib_stacks.append("r+ng")
        self.m_tib_stacks.append("r+ny")
        self.m_tib_stacks.append("r+t")
        self.m_tib_stacks.append("r+ts")
        self.m_tib_stacks.append("r+ts+w")
        self.m_tib_stacks.append("r+w")
        self.m_tib_stacks.append("s+b")
        self.m_tib_stacks.append("s+b+r")
        self.m_tib_stacks.append("s+b+y")
        self.m_tib_stacks.append("s+d")
        self.m_tib_stacks.append("s+g")
        self.m_tib_stacks.append("s+g+r")
        self.m_tib_stacks.append("s+g+y")
        self.m_tib_stacks.append("s+k")
        self.m_tib_stacks.append("s+k+r")
        self.m_tib_stacks.append("s+k+y")
        self.m_tib_stacks.append("s+l")
        self.m_tib_stacks.append("s+m")
        self.m_tib_stacks.append("s+m+r")
        self.m_tib_stacks.append("s+m+y")
        self.m_tib_stacks.append("s+n")
        self.m_tib_stacks.append("s+n+r")
        self.m_tib_stacks.append("s+ng")
        self.m_tib_stacks.append("s+ny")
        self.m_tib_stacks.append("s+p")
        self.m_tib_stacks.append("s+p+r")
        self.m_tib_stacks.append("s+p+y")
        self.m_tib_stacks.append("s+r")
        self.m_tib_stacks.append("s+t")
        self.m_tib_stacks.append("s+ts")
        self.m_tib_stacks.append("s+w")
        self.m_tib_stacks.append("sh+r")
        self.m_tib_stacks.append("sh+w")
        self.m_tib_stacks.append("t+r")
        self.m_tib_stacks.append("t+w")
        self.m_tib_stacks.append("th+r")
        self.m_tib_stacks.append("ts+w")
        self.m_tib_stacks.append("tsh+w")
        self.m_tib_stacks.append("z+l")
        self.m_tib_stacks.append("z+w")
        self.m_tib_stacks.append("zh+w")
        #  a map used to split the input string into tokens for fromWylie().
        #  all letters which start tokens longer than one letter are mapped to the max length of
        #  tokens starting with that letter.
        self.m_tokens_start = {
            'S': 2,
            '/': 2,
            'd': 4,
            'g': 3,
            'b': 3,
            'D': 3,
            'z': 2,
            '~': 3,
            '-': 4,
            'T': 2,
            'a': 2,
            'k': 2,
            't': 3,
            's': 2,
            'c': 2,
            'n': 2,
            'p': 2,
            '\r': 2,
        }
        #  also for tokenization - a set of tokens longer than one letter
        self.m_tokens = []
        self.m_tokens.append("-d+h")
        self.m_tokens.append("dz+h")
        self.m_tokens.append("-dh")
        self.m_tokens.append("-sh")
        self.m_tokens.append("-th")
        self.m_tokens.append("D+h")
        self.m_tokens.append("b+h")
        self.m_tokens.append("d+h")
        self.m_tokens.append("dzh")
        self.m_tokens.append("g+h")
        self.m_tokens.append("tsh")
        self.m_tokens.append("~M`")
        self.m_tokens.append("-I")
        self.m_tokens.append("-d")
        self.m_tokens.append("-i")
        self.m_tokens.append("-n")
        self.m_tokens.append("-t")
        self.m_tokens.append("//")
        self.m_tokens.append("Dh")
        self.m_tokens.append("Sh")
        self.m_tokens.append("Th")
        self.m_tokens.append("ai")
        self.m_tokens.append("au")
        self.m_tokens.append("bh")
        self.m_tokens.append("ch")
        self.m_tokens.append("dh")
        self.m_tokens.append("dz")
        self.m_tokens.append("gh")
        self.m_tokens.append("kh")
        self.m_tokens.append("ng")
        self.m_tokens.append("ny")
        self.m_tokens.append("ph")
        self.m_tokens.append("sh")
        self.m_tokens.append("th")
        self.m_tokens.append("ts")
        self.m_tokens.append("zh")
        self.m_tokens.append("~M")
        self.m_tokens.append("~X")
        self.m_tokens.append("\r\n")

    #  setup a wylie object
    def initWylie(self, check, check_strict, print_warnings, fix_spacing):

        #  check_strict requires check
        if check_strict and not check:
            raise "check_strict requires check."
        self.check = check
        self.check_strict = check_strict
        self.print_warnings = print_warnings
        self.fix_spacing = fix_spacing
        self.initHashes()

    #  constructor passing all options
    #  see the comments at the beginning of this file for more details.
    # @overloaded
    def __init__0(self, check, check_strict, print_warnings, fix_spacing):
        self.initWylie(check, check_strict, print_warnings, fix_spacing)

    #  constructor with default options
    # @__init__.register(object)
    def __init__(self):
        self.initWylie(True, True, False, True)

    #  helper functions to access the various hash tables
    def consonant(self, s):
        return self.m_consonant.get(s)

    def subjoined(self, s):
        return self.m_subjoined.get(s)

    def vowel(self, s):
        return self.m_vowel.get(s)

    def final_uni(self, s):
        return self.m_final_uni.get(s)

    def final_class(self, s):
        return self.m_final_class.get(s)

    def other(self, s):
        return self.m_other.get(s)

    def isSpecial(self, s):
        return s in self.m_special

    def isSuperscript(self, s):
        return s in self.m_superscripts

    def superscript(self, sup, below):
        tmpSet = self.m_superscripts.get(sup)
        if tmpSet is None:
            return False
        return below in tmpSet

    def isSubscript(self, s):
        return s in self.m_subscripts

    def subscript(self, sub, above):
        tmpSet = self.m_subscripts.get(sub)
        if tmpSet is None:
            return False
        return above in tmpSet

    def isPrefix(self, s):
        return s in self.m_prefixes

    def prefix(self, pref, after):
        tmpSet = self.m_prefixes.get(pref)
        if tmpSet is None:
            return False
        return after in tmpSet

    def isSuffix(self, s):
        return s in self.m_suffixes

    def isSuff2(self, s):
        return s in self.m_suff2

    def suff2(self, suff, before):
        tmpSet = self.m_suff2.get(suff)
        if tmpSet is None:
            return False
        return before in tmpSet

    def ambiguous_key(self, syll):
        return self.m_ambiguous_key.get(syll)

    def ambiguous_wylie(self, syll):
        return self.m_ambiguous_wylie.get(syll)

    def tib_top(self, c):
        return self.m_tib_top.get(c)

    def tib_subjoined(self, c):
        return self.m_tib_subjoined.get(c)

    def tib_vowel(self, c):
        return self.m_tib_vowel.get(c)

    def tib_vowel_long(self, s):
        return self.m_tib_vowel_long.get(s)

    def tib_final_wylie(self, c):
        return self.m_tib_final_wylie.get(c)

    def tib_final_class(self, c):
        return self.m_tib_final_class.get(c)

    def tib_caret(self, s):
        return self.m_tib_caret.get(s)

    def tib_other(self, c):
        return self.m_tib_other.get(c)

    def tib_stack(self, s):
        return s in self.m_tib_stacks

    #  split a string into Wylie tokens;
    # make sure there is room for at least one null element at the end of the
    # array
    def splitIntoTokens(self, str_):  # noqa: C901
        i = 0
        o = 0
        maxlen = len(str_)
        tokens = [''] * (maxlen + 2)
        while i < maxlen:
            try:
                c = str_[i]
                mlo = self.m_tokens_start.get(c, None)
                # if there are multi-char tokens starting with this char, try
                # them
                if mlo is not None:
                    length = int(mlo)
                    while length > 1:
                        if i <= maxlen - length:
                            tr = str_[i: i + length]
                            if tr in self.m_tokens:
                                tokens[o] = tr
                                o += 1
                                i += length
                                length -= 1
                                raise Exception("Continue")
                        length -= 1
                #  things starting with backslash are special
                if c == '\\' and i <= maxlen - 2:
                    if str_[i + 1] == 'u' and i <= maxlen - 6:
                        tokens[o] = str_.substring(i, i + 6)
                        o += 1
                        #  \\uxxxx
                        i += 6
                    elif str_[i + 1] == 'U' and i <= maxlen - 10:
                        tokens[o] = str_.substring(i, i + 10)
                        o += 1
                        #  \\Uxxxxxxxx
                        i += 10
                    else:
                        tokens[o] = str_.substring(i, i + 2)
                        o += 1
                        #  \\x
                        i += 2
                    raise Exception("Continue")
                #  otherwise just take one char

                tokens[o] = c
                o += 1
                i += 1
            except Exception:
                continue
        return tokens

    # Converts successive stacks of Wylie into unicode, starting at the given index
        # within the array of tokens.
        #
        # Assumes that the first available token is valid, and is either a vowel or a consonant.
        # Returns a WylieTsekbar object
    def fromWylieOneTsekbar(self, tokens, i):  # noqa: C901
        orig_i = i
        t = tokens[i]

        # variables for tracking the state within the syllable as we parse it
        stack = None
        prev_cons = None
        visarga = False

        # variables for checking the root letter, after parsing a whole tsekbar made of only single
        # consonants and one consonant with "a" vowel
        check_root = True
        consonants = []
        root_idx = -1

        out = ""
        warns = []

        # the type of token that we are expecting next in the input stream
        #   - PREFIX : expect a prefix consonant, or a main stack
        #   - MAIN   : expect only a main stack
        #   - SUFF1  : expect a 1st suffix
        #   - SUFF2  : expect a 2nd suffix
        #   - NONE   : expect nothing (after a 2nd suffix)
        #
        # the state machine is actually more lenient than this, in that a "main stack" is allowed
        # to come at any moment, even after suffixes.  this is because such syllables are sometimes
        # found in abbreviations or other places.  basically what we check is that prefixes and
        # suffixes go with what they are attached to.
        #
        # valid tsek-bars end in one of these states: SUFF1, SUFF2, NONE
        state = self.State.PREFIX

        # iterate over the stacks of a tsek-bar
        while t is not None and (self.vowel(t) is not None or self.consonant(t) is not None) and not visarga:  # STACK

            # translate a stack
            if stack is not None:
                prev_cons = stack.single_consonant

            stack = self.fromWylieOneStack(tokens, i)
            i += stack.tokens_used
            t = tokens[i]
            out += stack.uni_string
            warns.extend(stack.warns)
            visarga = stack.visarga
            if not self.check:
                continue

            # check for syllable structure consistency by iterating a simple state machine
                # - prefix consonant
            if state == self.State.PREFIX and stack.single_consonant is not None:
                consonants.append(stack.single_consonant)
                if self.isPrefix(stack.single_consonant):
                    next = t
                    if self.check_strict:
                        next = self.consonantString(tokens, i)
                    if next is not None and not self.prefix(stack.single_consonant, next):
                        next = next.replace("+", "")
                        warns.append("Prefix \"" + stack.single_consonant +
                                     "\" does not occur before \"" + next + "\".")
                else:
                    warns.append("Invalid prefix consonant: \"" +
                                 stack.single_consonant + "\".")
                state = self.State.MAIN

            # - main stack with vowel or multiple consonants
            elif stack.single_consonant is None:
                state = self.State.SUFF1

                # keep track of the root consonant if it was a single cons with
                # an "a" vowel
                if root_idx >= 0:
                    check_root = False
                elif stack.single_cons_a is not None:
                    consonants.append(stack.single_cons_a)
                    root_idx = len(consonants) - 1

            # - unexpected single consonant after prefix
            elif state == self.State.MAIN:
                warns.append("Expected vowel after \"" +
                             stack.single_consonant + "\".")

            # - 1st suffix
            elif state == self.State.SUFF1:
                consonants.append(stack.single_consonant)

                # check this one only in strict mode b/c it trips on lots of
                # Skt stuff
                if self.check_strict:
                    if not self.isSuffix(stack.single_consonant):
                        warns.append("Invalid suffix consonant: \"" +
                                     stack.single_consonant + "\".")
                state = self.State.SUFF2

            # - 2nd suffix
            elif state == self.State.SUFF2:
                consonants.append(stack.single_consonant)
                if self.isSuff2(stack.single_consonant):
                    if not self.suff2(stack.single_consonant, prev_cons):
                        warns.append("Second suffix \"" + stack.single_consonant +
                                     "\" does not occur after \"" + prev_cons + "\".")
                else:
                    warns.append("Invalid 2nd suffix consonant: \"" +
                                 stack.single_consonant + "\".")
                state = self.State.NONE

            # - more crap after a 2nd suffix
            elif state == self.State.NONE:
                warns.append("Cannot have another consonant \"" +
                             stack.single_consonant + "\" after 2nd suffix.")

        if state == self.State.MAIN and stack.single_consonant is not None and self.isPrefix(stack.single_consonant):
            warns.append("Vowel expected after \"" +
                         stack.single_consonant + "\".")

        # check root consonant placement only if there were no warnings so far, and the syllable
            # looks ambiguous.  not many checks are needed here because the previous state machine
            # already takes care of most illegal combinations.
        if self.check and len(warns) == 0 and check_root and root_idx >= 0:

            # 2 letters where each could be prefix/suffix: root is 1st
            if len(consonants) == 2 and \
                    root_idx != 0 and \
                    self.prefix(consonants[0], consonants[1]) and \
                    self.isSuffix(consonants[1]):
                warns.append("Syllable should probably be \"" +
                             consonants[0] + "a" + consonants[1] + "\".")

            # 3 letters where 1st can be prefix, 2nd can be postfix before "s" and last is "s":
                # use a lookup table as this is completely ambiguous.
            elif len(consonants) == 3 and \
                    self.isPrefix(consonants[0]) and \
                    self.suff2("s", consonants[1]) and \
                    consonants[2] == "s":
                cc = self.joinStrings(consonants, "")
                cc = cc.replace(u'\u2018', '\'')
                cc = cc.replace(u'\u2019', '\'')  # typographical quotes
                expect_key = self.ambiguous_key(cc)
                if expect_key is not None and int(expect_key) != root_idx:
                    warns.append("Syllable should probably be \"" +
                                 self.ambiguous_wylie(cc) + "\".")

        # return the stuff as a WylieTsekbar struct
        ret = Wylie.WylieTsekbar()
        ret.uni_string = out
        ret.tokens_used = i - orig_i
        ret.warns = warns
        return ret

    def unicodeEscape(self, warns, line, t):
        hex = t.substring(2)
        if hex.isEmpty():
            return None
        if not self.validHex(hex):
            self.warnl(warns, line, "\"" + t + "\": invalid hex code.")
            return ""
        return str(int(hex, base=16))
        # Character.valueOf(str(int(hex, base=16))).__str__()

    #  Converts a Wylie (EWTS) string to unicode.  If 'warns' is not the null List, puts warnings into it.
    # @fromWylie.register(object, str, List)
    def fromWylie(self, str_, warns=None):  # noqa: C901
        out = []
        line = 1
        units = 0

        #  remove initial spaces if required
        if self.fix_spacing:
            str_ = re.sub("^\\s+", "", str_, 1)

        #  split into tokens
        tokens = self.splitIntoTokens(str_)
        i = 0

        #  iterate over the tokens
        # __i_5 = i
        while tokens[i] != '':  # ITER
            try:
                t = tokens[i]
                o = None

                #  [non-tibetan text] : pass through, nesting brackets
                if t == "[":
                    nesting = 1
                    i += 1
                    while tokens[i] is not None:  # ESC
                        t = tokens[i]
                        i += 1
                        if t == "[":
                            nesting += 1
                        if t == "]":
                            nesting -= 1
                        if nesting == 0:
                            raise Exception("Continue")  # ITER

                        # handle unicode escapes and \1-char escapes within
                        # [comments]...
                        if t.startsWith("\\u") or t.startsWith("\\U"):
                            o = self.unicodeEscape(warns, line, t)
                            if o is not None:
                                out.append(o)
                                continue  # ESC
                        if t.startsWith("\\"):
                            o = t.substring(1)
                        else:
                            o = t
                        out.append(o)
                    self.warnl(warns, line, "Unfinished [non-Wylie stuff].")
                    break  # ITER

                #  punctuation, numbers, etc
                o = self.other(t)
                if o is not None:
                    out.append(o)
                    i += 1
                    units += 1
                    #  collapse multiple spaces?
                    if t == " " and self.fix_spacing:
                        while tokens[i] is not None and tokens[i] == " ":
                            pass
                    continue
                if self.vowel(t) is not None or self.consonant(t) is not None:
                    tb = self.fromWylieOneTsekbar(tokens, i)
                    word = ""
                    j = 0
                    while j < tb.tokens_used:
                        word += tokens[i + j]
                        j += 1
                    out.append(tb.uni_string)
                    i += tb.tokens_used
                    units += 1
                    for w in tb.warns:
                        self.warnl(warns, line, "\"" + word + "\": " + w)
                    continue
                if t == u"\ufeff" or t == u"\u200b":
                    i += 1
                    continue
                if t.startswith("\\u") or t.startswith("\\U"):
                    o = self.unicodeEscape(warns, line, t)
                    if o is not None:
                        i += 1
                        out.append(o)
                        continue
                if t.startswith("\\"):
                    out.append(t.substring(1))
                    i += 1
                    continue
                if t == "\r\n" or t == "\n" or t == "\r":
                    line += 1
                    out.append(t)
                    i += 1
                    if self.fix_spacing:
                        while tokens[i] is not None and tokens[i] == " ":
                            pass
                    continue
                if t == '':
                    i += 1
                    continue
                c = t[0]
                if self.isSpecial(t) or (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z'):
                    self.warnl(warns, line, "Unexpected character \"" + t + "\".")
                out.append(t)
                i += 1
            except Exception:
                continue

        if units == 0:
            self.warn(warns, "No Tibetan characters found!")
        return ''.join(out)

    def validHex(self, t):
        i = 0
        while i < len(t):
            c = t[i]
            if not ((c >= 'a' and c <= 'f') or (c >= '0' and c <= '9')):
                return False
            i += 1
        return True

    def warn(self, warns, str_):
        if warns is not None:
            warns.append(str_)
        if self.print_warnings:
            print(str_)

    def warnl(self, warns, line, str_):
        self.warn(warns, "line " + str(line) + ": " + str_)

    def debug(self, str_):
        print(str_)

    def debugvar(self, o, name):
        print(">>" + name + "<< : (" + ("NULL" if o is None else o.__str__()) + ")")

    def joinStrings(self, a, sep):
        return sep.join([x for x in a if x is not None])

    # Converts one stack's worth of Wylie into unicode, starting at the given index
        # within the array of tokens.
        # Assumes that the first available token is valid, and is either a vowel or a consonant.
        # Returns a WylieStack object.
    def fromWylieOneStack(self, tokens, i):  # noqa: C901
        orig_i = i
        t = None
        t2 = None
        # o = None
        out = ""
        warns = []
        consonants = 0  # how many consonants found
        vowel_found = None  # any vowels (including a-chen)
        # any vowel signs (that go under or above the main stack)
        vowel_sign = None
        single_consonant = None  # did we find just a single consonant?
        plus = False  # any explicit subjoining via '+'?
        caret = 0  # find any '^'?
        final_found = {}  # keep track of finals (H, M, etc) by class

        # do we have a superscript?
        t = tokens[i]
        t2 = tokens[i + 1]
        if t2 is not None and self.isSuperscript(t) and self.superscript(t, t2):
            if self.check_strict:
                next = self.consonantString(tokens, i + 1)
                if not self.superscript(t, next):
                    next = next.replace("+", "")
                    warns.append(
                        "Superscript \"" + t + "\" does not occur above combination \"" + next + "\".")
            out += self.consonant(t)
            consonants += 1
            i += 1
            while tokens[i] is not None and tokens[i] == "^":
                caret += 1
                i += 1

        # main consonant + stuff underneath.
                # this is usually executed just once, but the "+" subjoining
                # operator makes it come back here
        while True:  # MAIN
            # main consonant (or a "a" after a "+")
            t = tokens[i]
            if self.consonant(t) is not None or (len(out) > 0 and self.subjoined(t) is not None):
                if len(out) > 0:
                    out += self.subjoined(t)
                else:
                    out += self.consonant(t)
                i += 1
                if t == "a":
                    vowel_found = "a"
                else:
                    consonants += 1
                    single_consonant = t
                while tokens[i] is not None and tokens[i] == "^":
                    caret += 1
                    i += 1

                # subjoined: rata, yata, lata, wazur.  there can be up two
                # subjoined letters in a stack.
                z = 0
                while z < 2:
                    t2 = tokens[i]
                    if t2 is not None and self.isSubscript(t2):

                        # lata does not occur below multiple consonants
                        # (otherwise we mess up "brla" = "b.r+la")
                        if t2 == "l" and consonants > 1:
                            break

                        # full stack checking (disabled by "+")
                        if self.check_strict and not plus:
                            prev = self.consonantStringBackwards(
                                tokens, i - 1, orig_i)
                            if not self.subscript(t2, prev):
                                prev = prev.replace("+", "")
                                warns.append(
                                    "Subjoined \"" + t2 + "\" not expected after \"" + prev + "\".")

                        # simple check only
                        elif self.check:
                            if not self.subscript(t2, t) and not (z == 1 and t2 == "w" and t == "y"):
                                warns.append(
                                    "Subjoined \"" + t2 + "\"not expected after \"" + t + "\".")
                        out += self.subjoined(t2)
                        i += 1
                        consonants += 1
                        while tokens[i] is not None and tokens[i] == "^":
                            caret += 1
                            i += 1
                        t = t2
                    else:
                        break
                    z += 1

            # caret (^) can come anywhere in Wylie but in Unicode we generate it at the end of
                    # the stack but before vowels if it came there (seems to be what OpenOffice expects),
                    # or at the very end of the stack if that's how it was in
                    # the Wylie.
            if caret > 0:
                if caret > 1:
                    warns.append(
                        "Cannot have more than one \"^\" applied to the same stack.")
                final_found[self.final_class("^")] = "^"
                out += self.final_uni("^")
                caret = 0

            # vowel(s)
            t = tokens[i]
            if t is not None and self.vowel(t) is not None:
                if 0 == len(out):
                    out += self.vowel("a")
                if not t == "a":
                    out += self.vowel(t)
                i += 1
                vowel_found = t
                if not t == "a":
                    vowel_sign = t

            # plus sign: forces more subjoining
            t = tokens[i]
            if t is not None and t == "+":
                i += 1
                plus = True

                # sanity check: next token must be vowel or subjoinable
                # consonant.
                t = tokens[i]
                if t is None or (self.vowel(t) is None and self.subjoined(t) is None):
                    if self.check:
                        warns.append(
                            "Expected vowel or consonant after \"+\".")
                    break  # MAIN

                # consonants after vowels doesn't make much sense but process
                # it anyway
                if self.check:
                    if self.vowel(t) is None and vowel_sign is not None:
                        warns.append("Cannot subjoin consonant (" + t +
                                     ") after vowel (" + vowel_sign + ") in same stack.")
                    elif t == "a" and vowel_sign is not None:
                        warns.append(
                            "Cannot subjoin a-chen (a) after vowel (" + vowel_sign + ") in same stack.")
                continue  # MAIN
            break  # MAIN

        # final tokens
        t = tokens[i]
        while t is not None and self.final_class(t) is not None:
            uni = self.final_uni(t)
            klass = self.final_class(t)

            # check for duplicates
            if klass in final_found:
                if final_found.get(klass) == t:
                    warns.append("Cannot have two \"" + t +
                                 "\" applied to the same stack.")
                else:
                    warns.append("Cannot have \"" + t + "\" and \"" +
                                 final_found.get(klass) + "\" applied to the same stack.")
            else:
                final_found[klass] = t
                out += uni
            i += 1
            single_consonant = None
            t = tokens[i]

        # if next is a dot "." (stack separator), skip it.
        if tokens[i] is not None and tokens[i] == ".":
            i += 1

        # if we had more than a consonant and no vowel, and no explicit "+" joining, backtrack and
            # return the 1st consonant alone
        if consonants > 1 and vowel_found is None:
            if plus:
                if self.check:
                    warns.append(
                        "Stack with multiple consonants should end with vowel.")
            else:
                i = orig_i + 1
                consonants = 1
                single_consonant = tokens[orig_i]
                out = ""
                out += self.consonant(single_consonant)

        # calculate "single consonant"
        if consonants != 1 or plus:
            single_consonant = None

        # return the stuff as a WylieStack struct
        ret = Wylie.WylieStack()
        ret.uni_string = out
        ret.tokens_used = i - orig_i
        if vowel_found is not None:
            ret.single_consonant = None
        else:
            ret.single_consonant = single_consonant
        if vowel_found is not None and vowel_found == "a":
            ret.single_cons_a = single_consonant
        else:
            ret.single_cons_a = None
        ret.warns = warns
        ret.visarga = "H" in final_found
        return ret

    def consonantString(self, tokens, i):
        out = []
        while tokens[i] is not None:
            t = tokens[i]
            i += 1
            if t == "+" or t == "^":
                continue
            if self.consonant(t) is None:
                break
            out.append(t)
        return self.joinStrings(out, "+")

    def consonantStringBackwards(self, tokens, i, orig_i):
        out = []
        while i >= orig_i and tokens[i] is not None:
            t = tokens[i]
            i -= 1
            if t == "+" or t == "^":
                continue
            if self.consonant(t) is None:
                break
            out.insert(0, t)
        return self.joinStrings(out, "+")

    def handleSpaces(self, str_, i, out):
        found = 0
        # orig_i = i
        while i < len(str_) and str_[i] == ' ':
            i += 1
            found += 1
        if found == 0 or i == len(str_):
            return 0
        t = str_[i]
        if self.tib_top(t) is None and self.tib_other(t) is None:
            return 0
        while i < found:
            out.append('_')
            i += 1
        return found

    # Converts from Unicode strings to Wylie (EWTS) transliteration, without warnings,
        # including escaping of non-tibetan into [comments].
    def toWylie(self, str_):
        return self.toWylieOptions(str_, None, True)

    # Converts from Unicode strings to Wylie (EWTS) transliteration.
        #
        # Arguments are:
        #    str   : the unicode string to be converted
        #    escape: whether to escape non-tibetan characters according to Wylie encoding.
        #            if escape == false, anything that is not tibetan will be just passed through.
        #
        # Returns: the transliterated string.
        #
        # To get the warnings, call getWarnings() afterwards.
    # @toWylie.register(object, str, List, bool)
    def toWylieOptions(self, str_, warns, escape):  # noqa: C901
        out = ""
        line = 1
        units = 0

        # globally search and replace some deprecated pre-composed Sanskrit
        # vowels
        str_ = str_.replace(u"\u0f76", u"\u0fb2\u0f80")
        str_ = str_.replace(u"\u0f77", u"\u0fb2\u0f71\u0f80")
        str_ = str_.replace(u"\u0f78", u"\u0fb3\u0f80")
        str_ = str_.replace(u"\u0f79", u"\u0fb3\u0f71\u0f80")
        str_ = str_.replace(u"\u0f81", u"\u0f71\u0f80")
        str_ = str_.replace(u"\u0f00", u"\u0F68\u0F7C\u0F7E")

        i = 0
        length = len(str_)

        # iterate over the string, codepoint by codepoint
        while i < length:  # ITER
            t = str_[i]

            # found tibetan script - handle one tsekbar
            if self.tib_top(t) is not None:
                tb = self.toWylieOneTsekbar(str_, length, i)
                out += tb.wylie
                i += tb.tokens_used
                units += 1
                for w in tb.warns:
                    self.warnl(warns, line, w)
                if not escape:
                    i += self.handleSpaces(str_, i, out)
                continue  # ITER

            # punctuation and special stuff.  spaces are tricky:
                # - in non-escaping mode: spaces are not turned to '_' here (handled by handleSpaces)
                # - in escaping mode: don't do spaces if there is non-tibetan coming, so they become part
            o = self.tib_other(t)
            if o is not None and (t != ' ' or (escape and not self.followedByNonTibetan(str_, i))):
                out += o
                i += 1
                units += 1
                if not escape:
                    i += self.handleSpaces(str_, i, out)
                continue  # ITER

            # newlines, count lines.  "\r\n" together count as one newline.
            if t == '\r' or t == '\n':
                line += 1
                i += 1
                out += t
                if t == '\r' and i < length and str_[i] == '\n':
                    i += 1
                    out += '\n'
                continue  # ITER

            # ignore BOM and zero-width space
            if t == u'\ufeff' or t == u'\u200b':
                i += 1
                continue  # ITER

            # anything else - pass along?
            if not escape:
                out += t
                i += 1
                continue  # ITER

            # other characters in the tibetan plane, escape with \\u0fxx
            if t > u'\u0f00' and t <= u'\u0fff':
                # c = t.encode("utf8")
                out += t
                i += 1

                # warn for tibetan codepoints that should appear only after a
                # tib_top
                if self.tib_subjoined(t) is not None or self.tib_vowel(t) is not None or self.tib_final_wylie(t) is not None:
                    self.warnl(warns, line, "Tibetan sign " + t +
                               " needs a top symbol to attach to.")
                continue  # ITER

            # ... or escape according to Wylie:
                # put it in [comments], escaping[] sequences and closing at
                # line ends
            out += "["
            while self.tib_top(t) is None and (self.tib_other(t) is None or t == ' ') and t != '\r' and t != '\n':
                # \escape [opening and closing] brackets
                if t == '[' or t == ']':
                    out += "\\"
                    out += t

                # unicode-escape anything in the tibetan plane (i.e characters
                # not handled by Wylie)
                elif t > u'\u0f00' and t <= u'\u0fff':
                    out += self.formatHex(t)

                # and just pass through anything else!
                else:
                    out += t

                i += 1
                if i >= length:
                    break

                t = str_[i]
            out += "]"
        return out

    def formatHex(self, t):
        return u''.join(char if 32 <= ord(char) <= 126 else u'\\u%04x' % ord(char) for char in t)

    def followedByNonTibetan(self, str_, i):
        length = len(str_)
        while i < length and str_[i] == ' ':
            i += 1
        if i == length:
            return False
        t = str_[i]
        return self.tib_top(t) is None and self.tib_other(t) is None and t != '\r' and t != '\n'

    # C onvert Unicode to Wylie: one tsekbar
    def toWylieOneTsekbar(self, str_, length, i):  # noqa: C901
        orig_i = i
        warns = []
        stacks = []
        while True:  # ITER
            st = self.toWylieOneStack(str_, length, i)
            stacks.append(st)

            if st.warns:
                warns.extend(st.warns)

            i += st.tokens_used
            if st.visarga:
                break  # ITER
            if i >= length or self.tib_top(str_[i]) is None:
                break  # ITER

        # figure out if some of these stacks can be prefixes or suffixes (in which case
                # they don't need their "a" vowels)
        if len(stacks) > 1 and stacks[0].single_cons is not None:
            cs = stacks[1].cons_str.replace("+w", "")
            if self.prefix(stacks[0].single_cons, cs):
                stacks[0].prefix = True
        if len(stacks) > 1 and stacks[-1].single_cons is not None and self.isSuffix(stacks[-1].single_cons):
            stacks[-1].suffix = True
        if len(stacks) > 2 and \
                stacks[-1].single_cons is not None and \
                stacks[-2].single_cons is not None and \
                self.isSuffix(stacks[-2].single_cons) and \
                self.suff2(stacks[-1].single_cons, stacks[-2].single_cons):
            stacks[-1].suff2 = True
            stacks[-2].suffix = True
        if len(stacks) == 2 and stacks[0].prefix and stacks[1].suffix:
            stacks[0].prefix = False
        if len(stacks) == 3 and stacks[0].prefix and stacks[1].suffix and stacks[2].suff2:
            strb = ""
            for st in stacks:
                strb += st.single_cons
            ztr = strb
            root = self.ambiguous_key(ztr)
            if root is None:
                warns.append(
                    "Ambiguous syllable found: root consonant not known for \"" + ztr + "\".")
                root = 1
            stacks[root].prefix = stacks[root].suffix = False
            stacks[root + 1].suff2 = False
        if stacks[0].prefix and self.tib_stack(stacks[0].single_cons + "+" + stacks[1].cons_str):
            stacks[0].dot = True
        out = ""
        for st in stacks:
            out += self.putStackTogether(st)
        ret = self.ToWylieTsekbar()
        ret.wylie = out
        ret.tokens_used = i - orig_i
        ret.warns = warns
        return ret

    # Unicode to Wylie: one stack at a time
    def toWylieOneStack(self, str_, length, i):  # noqa: C901
        orig_i = i
        ffinal = None
        vowel = None
        klass = None

        # split the stack into a ToWylieStack object:
        #   - top symbol
        #   - stacked signs (first is the top symbol again, then subscribed main characters...)
        #   - caret (did we find a stray tsa-phru or not?)
        #   - vowel signs (including small subscribed a-chung, "-i" Skt signs, etc)
        #   - final stuff (including anusvara, visarga, halanta...)
        #   - and some more variables to keep track of what has been found
        st = self.ToWylieStack()

        # assume: tib_top(t) exists
        t = str_[i]
        i += 1
        st.top = self.tib_top(t)
        st.stack.append(self.tib_top(t))

        # grab everything else below the top sign and classify in various
        # categories
        while i < length:
            t = str_[i]
            o = self.tib_subjoined(t)
            o1 = self.tib_vowel(t)
            o2 = self.tib_final_wylie(t)
            if o is not None:
                i += 1
                st.stack.append(o)

                # check for bad ordering
                if len(st.finals) > 0:
                    st.warns.append(
                        "Subjoined sign \"" + o + "\" found after final sign \"" + str(ffinal) + "\".")
                elif len(st.vowels) > 0:
                    st.warns.append(
                        "Subjoined sign \"" + o + "\" found after vowel sign \"" + str(vowel) + "\".")
            elif (o1) is not None:
                i += 1
                st.vowels.append(o1)
                if vowel is None:
                    vowel = o1
                if len(st.finals) > 0:
                    st.warns.append(
                        "Vowel sign \"" + o1 + "\" found after final sign \"" + str(ffinal) + "\".")
            elif (o2) is not None:
                i += 1
                klass = self.tib_final_class(t)
                if o2 == "^":
                    st.caret = True
                else:
                    if o2 == "H":
                        st.visarga = True
                    st.finals.append(o2)
                    if ffinal is None:
                        ffinal = o2
                    if klass in st.finals_found:
                        st.warns.append(
                            "Final sign \"" + o2 + "\" should not combine with\
                                 found after final sign \"" + str(ffinal) + "\".")
                    else:
                        st.finals_found[klass] = o2
            else:
                break

        # now analyze the stack according to various rules
                # a - chen with vowel signs: remove the "a" and keep the vowel
                # signs
        if st.top == "a" and len(st.stack) == 1 and len(st.vowels) > 0:
            st.stack.pop(0)

        # handle long vowels: A+i becomes I, etc.
        if len(st.vowels) > 1 and st.vowels[0] == "A" and self.tib_vowel_long(st.vowels[1]) is not None:
            vowel_long = self.tib_vowel_long(st.vowels[1])
            st.vowels.pop(0)
            st.vowels.pop(0)
            st.vowels.insert(0, vowel_long)
        if st.caret and len(st.stack) == 1 and self.tib_caret(st.top) is not None:
            caret = self.tib_caret(st.top)
            st.top = vowel_long
            st.stack.pop(0)
            st.stack.insert(0, caret)
            st.caret = False
        st.cons_str = self.joinStrings(st.stack, "+")
        if len(st.stack) == 1 and not st.stack[0] == "a" and not st.caret and len(st.vowels) == 0 and len(st.finals) == 0:
            st.single_cons = st.cons_str
        st.tokens_used = i - orig_i
        return st

    def putStackTogether(self, st):
        out = ""
        if self.tib_stack(st.cons_str):
            out += self.joinStrings(st.stack, "")
        else:
            out += st.cons_str
        if st.caret:
            out += "^"
        if len(st.vowels) > 0:
            out += self.joinStrings(st.vowels, "+")
        elif not st.prefix and not st.suffix and not st.suff2 and (len(st.cons_str) == 0 or st.cons_str[-1] != 'a'):
            out += "a"
        out += self.joinStrings(st.finals, "")
        if st.dot:
            out += "."
        return out

    class State:
        PREFIX = 'PREFIX'
        MAIN = 'MAIN'
        SUFF1 = 'SUFF1'
        SUFF2 = 'SUFF2'
        NONE = 'NONE'

    class WylieStack(object):
        uni_string = None
        tokens_used = int()
        single_consonant = None
        single_cons_a = None
        warns = None
        visarga = bool()

    class WylieTsekbar(object):
        uni_string = None
        tokens_used = int()
        warns = None

    class ToWylieStack(object):
        top = None
        stack = []
        caret = bool()
        vowels = []
        finals = []
        finals_found = None
        visarga = bool()
        cons_str = None
        single_cons = None
        prefix = bool()
        suffix = bool()
        suff2 = bool()
        dot = bool()
        tokens_used = int()
        warns = None

        def __init__(self):
            self.stack = []
            self.vowels = []
            self.finals = []
            self.finals_found = {}
            self.warns = []

    class ToWylieTsekbar(object):
        wylie = None
        tokens_used = int()
        warns = None

# warn = []
# print (Wylie().fromWylie("sems can thams cad", warn))
# print ('\n'.join(warn))

# warn = []
# print (Wylie().toWylieOptions(u"ཨོཾ་ཨཿཧཱུྂ་བཛྲ་གུ་རུ་པདྨ་སིདྡྷི་ཧཱུྂ༔", warn, True))
# print ('\n'.join(warn))

# print (Wylie().fromWylie("phyugs zog gi stod nad} ", []))

warn = []
print (Wylie().toWylie(u"ཨོཾ་ཨཿཧཱུྂ་བཛྲ་གུ་རུ་པདྨ་སིདྡྷི་ཧཱུྂ༔", warn, True))
print ('\n'.join(warn))

warn = []
print (Wylie().toWylie(
    u"༄༅།	།ཞེས་བྱ་བྱ་རྣམས་ཡོད། སྤྱོད་ལྡན་གནས་སུ་སྐྱེ་བའི་རྒྱུ། །འཐབ་འཁྲོལ་གནོད་པ་ཐར་བྱེད་པའོ། །གཟུགས་ཀྱིསལྷག་མྱོས་མེ་ལོང་ཚལ། །རྒྱལ་ཆེན་མིག་མི་བཟང་གནས་སོ། །ཡུལ་འཁོར་\n"+
    u"སྐྱོང་ནི་ཤར་ཕྱོགས་ཏེ། །ལུས་ངན་བྱང་ཕྱོགས་ལྕང་ལོ་ཅན། །གཞན་ཡང་ཡུལ་པ་འཕགས་པར་སྐྱེས། །སྣ་ཚོགས་གཟུགས་དང་ལྕང་ལོ་ཅན། །ངོས་ལ་ཉིས་བརྒྱ་ལྔ་ཅུ་པ། །གཉའ་ཤིང་འཛིན་སྟེང་གནས་པ་\n"+
    u"སྟེ༑ ༑དཔག་མེད་བཀོད་པ་ལོངས་སྤྱོད་ལྡན། །དེ་འཁོར་ཀུན་ཏུརྒྱུ་བའི་ལྷ། །བྱེ་བ་ཕྲག་ནི་སུམ་ཅུ་དྲུག །དེ་རྣམས་གནས་པའི་གཞལ་ཡསཁང་། །གཟའ་སྐར་ཞེས་ཀྱང་འཇིག་རྟེན་གྲགས། །ཉི་ཟླ་གཉིས་ནི་\n"+
    u"ལྷ་གནས་ཏེ། །དཔག་ཚད་ལྔ་ཅུ་གཅིག་དང་བཅས། །གྱེན་འཐུར་འཕང་བའི་མདའ་ཡབ་དང་། །ནང་ན་སྐྱེད་ཚལ་གྲོང་ཁྱེར་དང་། །ལྟེང་ཁས་བརྒྱན་ཅིང་ལོངས་སྤྱོད་ལྡན། །འཁོར་ལོའི་རླུང་གིས་འདྲེན་པ་\n"+
    u"ཡིན༑ ༑ནམ་ཕྱེད་ཉི་མ་ནུབ་པ་དང་། །ཉི་མ་ཕྱེད་དང་འཆར་དུས་ཅིག །ཉི་མའི་འོད་དང་རང་གྲིབ་ལ། །བརྟེན་ནས་ཟླ་བ་འཕེལ་འགྲིབ་བྱེད། །འདིར་ནི་ཚུལ་ལྡན་བརྩེ་བ་ཅན། །ཁྱད་པར་སྒྲོན་མེ་བྱིན་པའི་\n"+
    u"མཐུ༑ ༑འཇིག་རྟེན་སྐྱོང་བ་བཞི་པོ་ནི། །ཚུལ་ཁྲིམས་བསོད་ནམས་གཞན་པས་ལྷག །སྣ་ཚོགས་ལོངས་སྤྱོད་བསམ་མི་ཁྱབ། །སེམས་ཀྱི་ཀུན་རྟོག་དགེ་བ་ཡིན། །གྲངས་བཞིན་ཡུལ་ཀྱང་དེ་འདྲར་སྣང་། །འདི་\n", warn, True))
print ('\n'.join(warn))
