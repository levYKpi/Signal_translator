from math import sin, cos


def ord_(tmp):
    if tmp:
        return ord(tmp)
    else:
        return -1


class Scanning:
    __atts = [6 for _ in range(256)] + [-1]
    ###############################
    __keyWords = {'PROGRAM': 401, 'PROCEDURE': 402, 'BEGIN': 403, 'END': 404, 'CONST': 405, 'VAR': 406,
                  'SIGNAL': 407, 'COMPLEX': 408, 'INTEGER': 409, 'FLOAT': 410, 'BLOCKFLOAT': 411,
                  'EXT': 412, 'DEFFUNC': 413, 'LINK': 414, 'IN': 415, 'OUT': 416, '$EXP': 417, '..': 301}
    ################
    # delimiters = []
    ################
    __identify = {}
    __intConsts = []
    __cmplConsts = []
    # __intcConsts = []
    ################
    __errors = []
    ################
    __lexemes = []

    def __init__(self):
        for i in [32] + list(range(8, 14)):
            self.__atts[i] = 0
        for i in range(48, 58):
            self.__atts[i] = 1
        for i in [36] + list(range(65, 91)):
            self.__atts[i] = 2
        for i in [35, 41, 45, 44, 91, 58, 59, 61, 92, 93]:
            self.__atts[i] = 3
        self.__atts[46] = 4
        self.__atts[40] = 5
        self.__atts[39] = 52

    def scan(self, filename):
        with open(str(filename), 'r') as fn:
            tmp_char = fn.read(1)
            idn_count = 1000
            consts_count = 1000000
            cmpl_count = 20000000
            # idnCompl
            buff = ''
            ln = 1
            cn = 0
            while tmp_char:
                # whitespaces
                while self.__atts[ord_(tmp_char)] == 0:
                    if tmp_char == '\n':
                        ln += 1
                        cn = 0
                    tmp_char = fn.read(1)
                    cn += 1
                    continue
                # error
                if self.__atts[ord_(tmp_char)] == 6:
                    self.__errors.append([tmp_char, ln, cn, "недопустимий символ або початок з недозволеного"])
                    tmp_char = fn.read(1)
                    cn += 1
                    continue
                # delimiters
                if self.__atts[ord_(tmp_char)] == 3:
                    self.__lexemes.append([ord_(tmp_char), ln, cn])
                    tmp_char = fn.read(1)
                    cn += 1
                    continue
                # identify
                if self.__atts[ord_(tmp_char)] == 2:
                    _cn = cn
                    buff += tmp_char
                    tmp_char = fn.read(1)
                    cn += 1
                    while self.__atts[ord_(tmp_char)] == 2 or tmp_char.isdigit():
                        buff += tmp_char
                        tmp_char = fn.read(1)
                        cn += 1
                    if buff in self.__keyWords:
                        self.__lexemes.append([self.__keyWords[buff], ln, _cn])
                    elif buff in self.__identify:
                        self.__lexemes.append([self.__identify[buff], ln, _cn])
                    else:
                        idn_count += 1
                        self.__identify.update({buff: idn_count})
                        self.__lexemes.append([idn_count, ln, _cn])
                    buff = ''
                    continue
                # intconsts
                # if self.__atts[ord_(tmp_char)] == 1:
                #     _cn = cn
                #     buff += tmp_char
                #     tmp_char = fn.read(1)
                #     cn += 1
                #     while self.__atts[ord_(tmp_char)] == 1:
                #         buff += tmp_char
                #         tmp_char = fn.read(1)
                #         cn += 1
                #         if not tmp_char:
                #             break
                #     consts_count += 1
                #     # self.__intcConsts.append(consts_count)
                #     self.__lexemes.append([consts_count, ln, _cn])
                #     self.__intConsts.append(buff)
                #     buff = ''
                #     continue
                if self.__atts[ord(tmp_char)] == 1:
                    _cn = cn
                    buff += tmp_char
                    tmp_char = fn.read(1)
                    cn += 1
                    while self.__atts[ord(tmp_char)] == 1:
                        buff += tmp_char
                        tmp_char = fn.read(1)
                        cn += 1
                    left_p = buff
                    buff = ''
                    if tmp_char == '#':
                        tmp_char = fn.read(1)
                        cn += 1
                        if tmp_char == '+' or tmp_char == '-':
                            buff += tmp_char
                            tmp_char = fn.read(1)
                            cn += 1
                            while self.__atts[ord(tmp_char)] == 1:
                                buff += tmp_char
                                tmp_char = fn.read(1)
                                cn += 1
                            right_p = buff
                            buff = ''
                            consts_count += 1
                            # self.ucConsts.append(consts_count)
                            self.__lexemes.append([consts_count, ln, _cn])
                            self.__intConsts.append(float(left_p + 'e' + right_p))
                            continue
                        else:
                            self.errors.append([tmp_char, ln, cn, "пропуск <sign>"])
                            continue
                    else:
                        consts_count += 1
                        self.__lexemes.append([consts_count, ln, _cn])
                        self.__intConsts.append(int(left_p))
                        continue
                # coments
                if tmp_char == '(':
                    tmp_char = fn.read(1)
                    cn += 1
                    if tmp_char == '*':
                        tmp_char = fn.read(1)
                        cn += 1
                        while tmp_char:
                            if tmp_char == '\n':
                                ln += 1
                                cn = 0
                            elif tmp_char == '*':
                                tmp_char = fn.read(1)
                                cn += 1
                                if tmp_char == ')':
                                    tmp_char = fn.read(1)
                                    cn += 1
                                    break
                                elif not tmp_char:
                                    self.__errors.append([tmp_char, ln, cn, "незакритий коментар"])
                                    break
                                elif tmp_char == '\n':
                                    ln += 1
                                    cn = 0
                                else:
                                    continue
                            elif not tmp_char:
                                self.__errors.append([tmp_char, ln, cn, "незакритий коментар"])
                                break
                            tmp_char = fn.read(1)
                            cn += 1
                        if not tmp_char:
                            self.__errors.append([tmp_char, ln, cn, "незакритий коментар"])
                            break
                    else:
                        self.__lexemes.append([40, ln, cn])
                        continue
                # range
                if self.__atts[ord_(tmp_char)] == 4:
                    tmp_char = fn.read(1)
                    cn += 1
                    if tmp_char == '.':
                        tmp_char = fn.read(1)
                        cn += 1
                        self.__lexemes.append([self.__keyWords['..'], ln, cn-1])
                        continue
                    else:
                        self.__lexemes.append([ord_('.'), ln, cn])
                        continue

                if tmp_char == "'":
                    cmpl = []
                    left_p = ''
                    right_p = ''
                    _cn = cn
                    tmp_char = fn.read(1)
                    cn += 1
                    if tmp_char.isdigit():
                        left_p += tmp_char
                        tmp_char = fn.read(1)
                        cn += 1
                        while tmp_char.isdigit():
                            left_p += tmp_char
                            tmp_char = fn.read(1)
                            cn += 1
                        cmpl.append(int(left_p))
                    else:
                        cmpl.append(0)
                    if tmp_char == ',':
                        tmp_char = fn.read(1)
                        cn += 1
                        if tmp_char.isdigit():
                            right_p += tmp_char
                            tmp_char = fn.read(1)
                            cn += 1
                            while tmp_char.isdigit():
                                right_p += tmp_char
                                tmp_char = fn.read(1)
                                cn += 1
                            cmpl.append(int(right_p))
                        else:
                            self.errors.append([tmp_char, ln, cn, "не число"])
                    elif tmp_char == '$':
                        tmp_char = fn.read(1)
                        cn += 1
                        if tmp_char == 'E':
                            tmp_char = fn.read(1)
                            cn += 1
                            if tmp_char == 'X':
                                tmp_char = fn.read(1)
                                cn += 1
                                if tmp_char == 'P':
                                    tmp_char = fn.read(1)
                                    cn += 1
                                    if tmp_char == '(':
                                        tmp_char = fn.read(1)
                                        cn += 1
                                        if tmp_char.isdigit():
                                            right_p += tmp_char
                                            tmp_char = fn.read(1)
                                            cn += 1
                                            while tmp_char.isdigit():
                                                right_p += tmp_char
                                                tmp_char = fn.read(1)
                                                cn += 1
                                            if cmpl[0] == 0:
                                                cmpl.append(sin(int(right_p)))
                                            else:
                                                cmpl.append(cmpl[0] * sin(int(right_p)))
                                                cmpl[0] *= cos(int(right_p))
                                        else:
                                            self.errors.append([tmp_char, ln, cn, "не число"])
                                        if tmp_char == ')':
                                            tmp_char = fn.read(1)
                                            cn += 1
                                        else:
                                            self.errors.append([tmp_char, ln, cn, "не дужка )"])
                                    else:
                                        self.errors.append([tmp_char, ln, cn, "не дужка ("])
                                else:
                                    self.errors.append([tmp_char, ln, cn, "не exp"])
                            else:
                                self.errors.append([tmp_char, ln, cn, "не exp"])
                        else:
                            self.errors.append([tmp_char, ln, cn, "не exp"])
                    else:
                        cmpl.append(0)
                    if tmp_char == "'":
                        tmp_char = fn.read(1)
                        cn += 1
                        cmpl_count += 1
                        self.__cmplConsts.append(cmpl)
                        self.__lexemes.append([cmpl_count, ln, _cn])
                    else:
                        self.__errors.append([tmp_char, ln, cn, "не закрито комплексну константу"])
                        continue
                        # break

    def print_lexemes(self):
        print("╔═════════ Lexemes ════════════════════════╗")
        print("╠══════════════code════════line═════colume═╣")
        i = -1
        for instance in self.__lexemes:
            i += 1
            print("╠══════════════════════════════════════════╣")
            print("║%19d| %9d| %9d ║ %d" % (instance[0], instance[1], instance[2], i))
        print("╚══════════════════════════════════════════╝")

    def print_key_words(self):
        print("╔═════════ Key Words ══════════════════════╗")
        print("╠════════════════key═══════════════════val═╣")
        for key, val in self.__keyWords.items():
            print("╠══════════════════════════════════════════╣")
            print("║%20s |%19d ║" % (key, val))
        print("╚══════════════════════════════════════════╝")

    def print_consts(self):
        print("╔═════════ CONSTANTS ══════════════════════╗")
        print("╠═══════════════code═══════════════════cns═╣")
        i = 1000000
        for x in self.__intConsts:
            i += 1
            print("╠══════════════════════════════════════════╣")
            print("║%20s |%19s ║" % (i, x))
        i = 20000000
        for x in self.__cmplConsts:
            i += 1
            print("╠══════════════════════════════════════════╣")
            print("║%20s |%8f %+8fi ║" % (i, x[0], x[1]))
        print("╚══════════════════════════════════════════╝")

    def print_idents(self):
        print("╔═════════ IDENTIFIERS ════════════════════╗")
        print("╠════════════════code══════════════════idn═╣")
        for key, val in self.__identify.items():
            print("╠══════════════════════════════════════════╣")
            print("║%20d |%19s ║" % (val, key))
        print("╚══════════════════════════════════════════╝")

    def print_errors(self):
        print("╔═════════════ ERROR TABLE ═════════════════")
        if self.__errors:
            for e in self.__errors:
                print("║%10s%10s%10s      %s" % (e[0], e[1], e[2], e[3]))
        else:
            print("║ no lex-errors")
        print("╚═══════════════════════════════════════════")

    def get_lexemes(self):
        return self.__lexemes

    def get_key_words(self):
        return self.__keyWords

    def get_consts(self):
        return self.__intConsts

    def get_complex(self):
        return self.__cmplConsts

    def get_idents(self):
        return self.__identify
