
class POS_tag:

    def __init__(self, corpus=None):
        self.corpus = corpus

        self.initp = dict()
        self.trans = dict()
        self.emiss = dict()

        if self.corpus != None:
            self.calc_statistics()

    def calc_statistics(self):
        cp = self.corpus.get_corpus_pos()
        word_list = self.corpus.word_list
        pos_list = self.corpus.pos_list

        # initial probability
        for pos in pos_list:
            self.initp[pos] = 0

        for sentence in cp:
            self.initp[sentence[0][1]] += 1

        n = len(cp)
        for pos in self.initp:
            self.initp[pos] /= n

        # transition probability
        for pos1 in pos_list:
            self.trans[pos1] = dict()
            self.trans[pos1]["count"] = 0
            for pos2 in pos_list:
                self.trans[pos1][pos2] = 0

        for sentence in cp:
            n = len(sentence)
            for i in range(n - 1):
                curr_pos = sentence[i][1]
                next_pos = sentence[i + 1][1]
                self.trans[curr_pos][next_pos] += 1
                self.trans[curr_pos]["count"] += 1

        for pos1 in self.trans:
            for pos2 in self.trans[pos1]:
                if pos2 != "count":
                    self.trans[pos1][pos2] /= self.trans[pos1]["count"]

        # emission probability
        pos_count = dict()
        for pos in pos_list:
            pos_count[pos] = 0

        for word in word_list:
            self.emiss[word] = dict()
            for pos in pos_list:
                self.emiss[word][pos] = 0

        for sentence in cp:
            for word in sentence:
                pos_count[word[1]] += 1
                self.emiss[word[0]][word[1]] += 1

        for word in word_list:
            for pos in pos_list:
                self.emiss[word][pos] /= pos_count[pos]

    def read_special_characters(self, words):
        special = {
            ' ': '<space>',
            '-': '<minus>',
            '(': '<left_parenthesis>',
            ')': '<right_parenthesis>',
            '*': '<asterisk>',
            '.': '<full_stop>',
            '"': '<quotation>',
            '/': '<slash>',
            ':': '<colon>',
            '=': '<equal>',
            ',': '<comma>',
            ';': '<semi_colon>',
            '<': '<less_than>',
            '>': '<greater_than>',
            '&': '<ampersand>',
            '{': '<left_curly_bracket>',
            '}': '<right_curly_bracket>',
            "'": '<apostrophe>',
            '+': '<plus>',
            '?': '<question_mark>',
            '!': '<exclamation>',
            '$': '<dollar>',
            '%': '<percent>'
        }

        word_count = len(words)
        for i in range(word_count):
            if words[i] in special:
                words[i] = special[words[i]]

    def test_print(self):
        f = open("test/init_prob", "w")
        f.write(str(self.initp))
        f.close()

        f = open("test/trans_prob", "w")
        f.write(str(self.trans))
        f.close()

        f = open("test/emiss_prob", "w")
        f.write(str(self.emiss))
        f.close()
