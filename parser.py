from tree import Tree


class Parser:
    def __init__(self, first_table, keys, consts, idents, compl):
        self.__lexemes = first_table
        self.__table = [x[0] for x in first_table]
        self.__length_lex = len(self.__table)
        # self.__keys = keys
        self.__keys = dict([(value, key) for key, value in keys.items()])
        self.__consts = consts
        self.__complex = compl
        # self.__idents = idents
        self.__idents = dict([(value, key) for key, value in idents.items()])
        self.__idx = 0
        self.__tree = Tree('<signal-program>', None)

    def error(self, tmp):
        self.__idx = self.__idx
        self.__tree.append_node([tmp, self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
        self.__tree.print_tree()
        print('error ' + tmp)
        print("code %d line %d colume %d" %
              (self.__lexemes[self.__idx][0], self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]))
        exit()

    def idx_error(self):
        self.__idx += 1
        if self.__idx >= self.__length_lex:
            self.__tree.append_node('EOF')
            self.__tree.print_tree()
            print('error EOF')
            exit()

    def unsigned_integer(self):
        self.__tree.append_node('<unsigned_integer>')
        t_idx = self.__table[self.__idx]
        t_el = self.__consts[t_idx - 1000001]
        if (t_idx > 1000000)\
                and (t_idx < 20000000)\
                and isinstance(t_el, int):
            self.__tree.append_node([t_el, self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
            self.idx_error()
            self.__tree.set_parent()
        else:
            self.error('no_unsigned_integer')
        self.__tree.set_parent()

    def fractional_part(self):
        self.__tree.append_node('<fractional-part>')
        if self.__table[self.__idx] == 35:
            self.__tree.append_node('#')
            self.idx_error()
            self.__tree.set_parent()
            if self.__table[self.__idx] in [43, 45]:
                self.__tree.append_node('sign')
                self.__tree.append_node(chr(self.__table[self.__idx]))
                self.idx_error()
                self.__tree.set_parent()
                self.__tree.set_parent()
            self.unsigned_integer()
        self.__tree.set_parent()

    def integer_part(self):
        self.__tree.append_node('<integer-part>')
        self.unsigned_integer()
        self.__tree.set_parent()

    def unsigned_number(self):
        # self.__tree.append_node('<unsigned_number>')
        # self.integer_part()
        # self.fractional_part()
        # self.__tree.set_parent()
        self.__tree.append_node('<unsigned_number>')
        t_idx = self.__table[self.__idx]
        t_el = self.__consts[self.__table[self.__idx] - 1000001]
        if (t_idx > 1000000) \
                and (t_idx < 20000000):
            self.__tree.append_node([t_el, self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
            self.idx_error()
            self.__tree.set_parent()
        else:
            self.error('no_unsigned_number')
        self.__tree.set_parent()

    def identifier(self):
        self.__tree.append_node('<identifier>')
        tmp = self.__table[self.__idx]
        if (tmp < 1000000) and (tmp > 1000):
            self.__tree.append_node([self.__idents[tmp], self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
            self.idx_error()
            self.__tree.set_parent()
        else:
            self.error('no_identifier')
        self.__tree.set_parent()

    def function_identifier(self):
        self.__tree.append_node('<function-identifier>')
        self.identifier()
        self.__tree.set_parent()

    def procedure_identifier(self):
        self.__tree.append_node('<procedure-identifier>')
        self.identifier()
        self.__tree.set_parent()

    def variable_identifier(self):
        self.__tree.append_node('<variable-identifier>')
        self.identifier()
        self.__tree.set_parent()

    def constant_identifier(self):
        self.__tree.append_node('<constant-identifier>')
        self.identifier()
        self.__tree.set_parent()

    def right_part(self):
        self.__tree.append_node('<right-pat>')
        if self.__table[self.__idx] == 44:
            self.__tree.append_node([',', self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
            self.idx_error()
            self.__tree.set_parent()
            self.unsigned_integer()
        elif self.__table[self.__idx] == 417:
            self.__tree.append_node('$EXP')
            self.idx_error()
            self.__tree.set_parent()
            if self.__table[self.__idx] == 40:
                self.__tree.append_node('(')
                self.idx_error()
                self.__tree.set_parent()
            else:
                self.error("no '('")
            self.unsigned_integer()
            if self.__table[self.__idx] == 41:
                self.__tree.append_node(')')
                self.idx_error()
                self.__tree.set_parent()
            else:
                self.error("no ')'")
        self.__tree.set_parent()

    def left_part(self):
        self.__tree.append_node('<left-part>')
        self.__tree.append_node('<unsigned_integer>')
        if (self.__table[self.__idx] > 1000000) and (self.__table[self.__idx] < 1000000):
            self.__tree.append_node([self.__consts[self.__table[self.__idx] - 1000001],
                                     self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
            self.idx_error()
            self.__tree.set_parent()
        self.__tree.set_parent()
        self.__tree.set_parent()

    # def complex_number(self):
    #     self.__tree.append_node('<complex-number>')
    #     self.left_part()
    #     self.right_part()
    #     self.__tree.set_parent()

    def unsigned_constant(self):
        self.__tree.append_node('<unsigned-constant>')
        self.unsigned_number()
        self.__tree.set_parent()

    def complex_constant(self):
        self.__tree.append_node('<complex-constant>')
        self.__tree.append_node('<complex-number>')
        # if self.__table[self.__idx] == 39:
        #     self.__tree.append_node('\'')
        #     self.__tree.set_parent()
        #     self.idx_error()
        # else:
        #     self.error('no "\'"')
        # self.complex_number()
        # if self.__table[self.__idx] == 39:
        #     self.__tree.append_node('\'')
        #     self.__tree.set_parent()
        #     self.idx_error()
        # else:
        #     self.error('no "\'"')
        self.__tree.append_node('left-part')
        self.__tree.append_node([self.__complex[self.__table[self.__idx] - 20000001][0],
                                 self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
        self.__tree.set_parent()
        self.__tree.set_parent()
        self.__tree.append_node('right-part')
        self.__tree.append_node([self.__complex[self.__table[self.__idx] - 20000001][1],
                                 self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
        self.__tree.set_parent()
        self.__tree.set_parent()
        self.idx_error()
        self.__tree.set_parent()
        self.__tree.set_parent()

    def statement(self):
        self.__tree.append_node('<statement>')
        if self.__table[self.__idx] == 414:
            self.__tree.append_node(['LINK', self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
            self.__tree.set_parent()
            self.idx_error()
            self.variable_identifier()
            if self.__table[self.__idx] == 44:
                self.__tree.append_node([',', self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
                self.__tree.set_parent()
                self.idx_error()
            else:
                self.error("no ','")
            self.unsigned_integer()
        elif self.__table[self.__idx] == 415:
            self.__tree.append_node(['IN', self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
            self.__tree.set_parent()
            self.idx_error()
            self.unsigned_integer()
        elif self.__table[self.__idx] == 416:
            self.__tree.append_node(['OUT', self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
            self.__tree.set_parent()
            self.idx_error()
            self.unsigned_integer()
        # else:
        #     self.error('no_statement')
        if self.__table[self.__idx] == 59:
            self.__tree.append_node([';', self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
            self.__tree.set_parent()
            self.idx_error()
        else:
            self.error("no ';'")
        self.__tree.set_parent()

    def statement_list(self):
        self.__tree.append_node('<statement-list>')
        while self.__table[self.__idx] in [414, 415, 416]:
            self.statement()
        self.__tree.set_parent()

    def identifier_list(self):
        # self.__tree.append_node('identifier-list')
        while self.__table[self.__idx] == 44:
            self.__tree.append_node([',', self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
            self.__tree.set_parent()
            self.idx_error()
            self.variable_identifier()
        # self.__tree.set_parent()

    def range_(self):
        self.__tree.append_node('<range>')
        self.unsigned_integer()
        if self.__table[self.__idx] == 301:
            self.__tree.append_node(['..', self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
            self.__tree.set_parent()
            self.idx_error()
        self.unsigned_integer()
        self.__tree.set_parent()

    def range_list(self):
        while self.__table[self.__idx] == 44:
            self.__tree.append_node([',', self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
            self.__tree.set_parent()
            self.idx_error()
            self.range_()

    def attribute(self):
        self.__tree.append_node('<attribute>')
        if self.__table[self.__idx] in range(407, 413):
            self.__tree.append_node([self.__keys[self.__table[self.__idx]],
                                     self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
            self.__tree.set_parent()
            self.idx_error()
        elif self.__table[self.__idx] == 91:
            self.__tree.append_node(['[', self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
            self.__tree.set_parent()
            self.idx_error()
            self.range_()
            self.range_list()
            if self.__table[self.__idx] == 93:
                self.__tree.append_node([']', self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
                self.__tree.set_parent()
                self.idx_error()
            else:
                self.error('no "]"')
        else:
            self.error('no_attribute')
        self.__tree.set_parent()

    def attribute_list(self):
        while self.__table[self.__idx] in list(range(407, 412)) + [91]:
            self.attribute()

    def declaration(self):
        self.__tree.append_node('<declaration>')
        self.variable_identifier()
        self.identifier_list()
        if self.__table[self.__idx] == 58:
            self.__tree.append_node([':', self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
            self.__tree.set_parent()
            self.idx_error()
        else:
            self.error('no ":"')
        self.attribute()
        self.attribute_list()
        if self.__table[self.__idx] == 59:
            self.__tree.append_node([';', self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
            self.__tree.set_parent()
            self.idx_error()
        else:
            self.error('no ";"')
        self.__tree.set_parent()

    def declaration_list(self):
        self.__tree.append_node('<declaration-list>')
        while (self.__table[self.__idx] > 1000) and (self.__table[self.__idx] < 1000000):
            self.declaration()
        self.__tree.set_parent()

    def parameters_list(self):
        self.__tree.append_node('<parameters-list>')
        if self.__table[self.__idx] == 40:
            self.__tree.append_node(['(', self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
            self.__tree.set_parent()
            self.idx_error()
        else:
            self.error('no "("')
        self.declaration_list()
        if self.__table[self.__idx] == 41:
            self.__tree.append_node([')', self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
            self.__tree.set_parent()
            self.idx_error()
        else:
            self.error('no ")"')
        self.__tree.set_parent()

    def procedure(self):
        self.__tree.append_node('<procedure>')
        if self.__table[self.__idx] == 402:
            self.__tree.append_node(['PROCEDURE', self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
            self.__tree.set_parent()
            self.idx_error()
        else:
            self.error('no_PROCEDURE')
        self.procedure_identifier()
        self.parameters_list()
        if self.__table[self.__idx] == 59:
            self.__tree.append_node([';', self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
            self.__tree.set_parent()
            self.idx_error()
        else:
            self.error('no ";"')
        self.__tree.set_parent()

    def procedure_declarations(self):
        self.__tree.append_node('<procedure-declarations>')
        while self.__table[self.__idx] == 402:
            self.procedure()
        self.__tree.set_parent()

    def function_characteristic(self):
        self.__tree.append_node('<function_characteristic>')
        if self.__table[self.__idx] == 92:
            self.__tree.append_node(['\\', self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
            self.__tree.set_parent()
            self.idx_error()
        else:
            self.error('no "\\"')
        self.unsigned_integer()
        if self.__table[self.__idx] == 44:
            self.__tree.append_node([',', self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
            self.__tree.set_parent()
            self.idx_error()
        else:
            self.error('no ","')
        self.unsigned_integer()
        self.__tree.set_parent()

    def function(self):
        self.__tree.append_node('<function>')
        self.function_identifier()
        if self.__table[self.__idx] == 61:
            self.__tree.append_node(['=', self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
            self.__tree.set_parent()
            self.idx_error()
        else:
            self.error('no "="')
        self.unsigned_integer()
        self.function_characteristic()
        if self.__table[self.__idx] == 59:
            self.__tree.append_node([';', self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
            self.__tree.set_parent()
            self.idx_error()
        else:
            self.error('no ";"')
        self.__tree.set_parent()

    def function_list(self):
        self.__tree.append_node('<function-list>')
        while (self.__table[self.__idx] > 1000) and (self.__table[self.__idx] < 100000):
            self.function()
        self.__tree.set_parent()

    def math_function_declarations(self):
        self.__tree.append_node('<math-function-declarations>')
        if self.__table[self.__idx] == 413:
            self.__tree.append_node(['DEFFUNC', self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
            self.__tree.set_parent()
            self.idx_error()
            self.function_list()
        self.__tree.set_parent()

    def variable_declarations(self):
        self.__tree.append_node('<variable-declarations>')
        if self.__table[self.__idx] == 406:
            self.__tree.append_node(['VAR', self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
            self.__tree.set_parent()
            self.idx_error()
            self.declaration_list()
        self.__tree.set_parent()

    def constant(self):
        self.__tree.append_node('<constant>')
        if self.__table[self.__idx] > 20000000:
            self.complex_constant()
        elif self.__table[self.__idx] == 45:
            self.__tree.append_node(['-', self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
            self.__tree.set_parent()
            self.idx_error()
            self.unsigned_constant()
        else:
            self.unsigned_constant()
        self.__tree.set_parent()

    def constant_declaration(self):
        self.__tree.append_node('<constant-declaration>')
        self.constant_identifier()
        if self.__table[self.__idx] == 61:
            self.__tree.append_node(['=', self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
            self.__tree.set_parent()
            self.idx_error()
        else:
            self.error('no "="')
        self.constant()
        if self.__table[self.__idx] == 59:
            self.__tree.append_node([';', self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
            self.__tree.set_parent()
            self.idx_error()
        else:
            self.error('no ";"')
        self.__tree.set_parent()

    def constant_declaration_list(self):
        self.__tree.append_node('<constant_declaration_list>')
        while (self.__table[self.__idx] > 1000) and (self.__table[self.__idx] < 1000000):
            self.constant_declaration()
        self.__tree.set_parent()

    def constant_declarations(self):
        self.__tree.append_node('<constant_declarations>')
        if self.__table[self.__idx] == 405:
            self.__tree.append_node(['CONST', self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
            self.__tree.set_parent()
            self.idx_error()
            self.constant_declaration_list()
        self.__tree.set_parent()

    def declarations(self):
        self.__tree.append_node('<declarations>')
        self.constant_declarations()
        self.variable_declarations()
        self.math_function_declarations()
        self.procedure_declarations()
        self.__tree.set_parent()

    def block(self):
        self.__tree.append_node('<block>')
        self.declarations()
        if self.__table[self.__idx] == 403:
            self.__tree.append_node(['BEGIN', self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
            self.__tree.set_parent()
            self.idx_error()
        else:
            self.error('no_BEGIN')
        self.statement_list()
        if self.__table[self.__idx] == 404:
            self.__tree.append_node(['END', self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
            self.__tree.set_parent()
            self.idx_error()
        else:
            self.error('no_END')
        self.__tree.set_parent()

    def program(self):
        self.__tree.append_node('<program>')
        if self.__table[self.__idx] == 401:
            self.__tree.append_node(['PROGRAM', self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
            self.__tree.set_parent()
            self.idx_error()
            self.procedure_identifier()
            if self.__table[self.__idx] == 59:
                self.__tree.append_node([';', self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
                self.__tree.set_parent()
                self.idx_error()
            else:
                self.error('no ";"')
            self.block()
            if self.__table[self.__idx] == 46:
                self.__tree.append_node(['.', self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
                self.__tree.set_parent()
                # self.idx_error()
            else:
                self.error('no "."')
        elif self.__table[self.__idx] == 402:
            self.__tree.append_node(['PROCEDURE', self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
            self.__tree.set_parent()
            self.idx_error()
            self.procedure_identifier()
            self.parameters_list()
            if self.__table[self.__idx] == 59:
                self.__tree.append_node([';', self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
                self.__tree.set_parent()
                self.idx_error()
            else:
                self.error('no ";"')
            self.block()
            if self.__table[self.__idx] == 59:
                self.__tree.append_node([';', self.__lexemes[self.__idx][1], self.__lexemes[self.__idx][2]])
                self.__tree.set_parent()
                # self.idx_error()
            else:
                self.error('no ";"')
        else:
            self.error('no_program')
        self.__tree.set_parent()

    def parsing(self):
        self.program()
        self.__tree.print_tree()

    def get_tree(self):
        return self.__tree
