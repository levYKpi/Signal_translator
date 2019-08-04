class Generator:
    def __init__(self):
        self.wrong_idents = []
        # self.proc_relation = []
        self.constants = []
        self.variables = []
        self.signals = []
        self.links = {}
        self.ins = []
        self.outs = []
        self.same_mem = []
        self.text = ''
        self.errors = ''
        pass

    def e_print(self, tmp):
        self.errors += str(tmp) + '\n'

    def prog(self, node):
        return ";;PROGRAM " + node.leaves[1].leaves[0].leaves[0].node[0] + '\n'

    def ranges(self, lst):
        s = 1
        if lst:
            for r in lst[0]:
                if r.node == '<range>':
                    b = r.leaves[0].leaves[0].node[0]
                    e = r.leaves[2].leaves[0].node[0]
                    if b < e:
                        s *= (e - b + 1)
                    else:
                        self.e_print("wrong range, in:")
                        self.e_print(r.leaves[0].leaves[0].node[0])
                        self.e_print(r.leaves[2].leaves[0].node[0])
                        # exit(0)
        return s

    def declaration_check(self, node, flag):
        text = ''
        for leaf in node.leaves:
            _n = 0
            _type = ''
            _var = []    # leaf.leaves[0].leaves[0].leaves[0].node[0]
            _v_dup = []
            _atts = []
            _range = []
            for att in leaf.leaves:
                if att.node == '<attribute>':
                    if att.leaves[0].node[0] != '[':
                        _atts.append(att.leaves[0].node[0])
                    else:
                        _range.append(att.leaves)
                elif att.node == '<variable-identifier>':
                    _var.append(att.leaves[0].leaves[0].node[0])
                    _v_dup.append(att.leaves[0].leaves[0].node)
            if "EXT" in _atts and "EXT" not in self.same_mem:
                for _ in _var:
                    self.same_mem.append(_)
            i = -1
            for _ in _var:
                i += 1
                if _ in self.wrong_idents:
                    self.e_print("var duplicates in:")
                    self.e_print(_v_dup[i])
                    # exit(0)
                else:
                    if flag:
                        self.wrong_idents.append(_)
            if "SIGNAL" in _atts:
                if flag:
                    for _ in _var:
                        self.signals.append(_)
            if "INTEGER" in _atts and "FLOAT" not in _atts and "BLOCKFLOAT" not in _atts:
                _n = self.ranges(_range)
                _type = 'dw'
            elif "FLOAT" in _atts and "INTEGER" not in _atts and "BLOCKFLOAT" not in _atts:
                _n = self.ranges(_range)
                _type = 'dq'
            elif "BLOCKFLOAT" in _atts and "FLOAT" not in _atts and "INTEGER" not in _atts:
                if len(_range) == 1:
                    _type = 'dd'
                    _n = 1 + self.ranges(_range)
                else:
                    self.e_print("many/less ranges in:")
                    self.e_print(leaf.leaves[-2].leaves[-2].leaves[2].node)
                    # exit(0)
            else:
                self.e_print("wrong attrebutes")
                self.e_print(leaf.leaves[-1].node)
            if "COMPLEX" in _atts and "SIGNAL" not in _atts:
                _n *= 2
            if flag:
                for _ in _var:
                    text += "    " + _ + " " + _type + " "
                    if _n == 1:
                        text += '?\n'
                    else:
                        text += str(_n)
                        text += " dup(?)\n"
        return text

    def proc(self, node):
        _ident = node.leaves[1].leaves[0].leaves[0].node[0]
        if _ident in self.wrong_idents:
            self.e_print(_ident + " = wrong identify")
            self.e_print(node.leaves[1].leaves[0].leaves[0].node)
            # exit(0)
        text = _ident + " PROC\n"
        self.wrong_idents.append(_ident)
        text += "    PUSHAD\n    mov EBP, ESP\n    POPAD\n    RET\n"
        text += _ident + " ENDP\n"
        self.declaration_check(node.leaves[2].leaves[1], 0)
        return text

    def deffunc(self, node):
        beg = node.leaves[3].leaves[3].leaves[0].node[0]
        end = node.leaves[3].leaves[1].leaves[0].node[0]
        num = node.leaves[2].leaves[0].node[0]
        _ident = node.leaves[0].leaves[0].leaves[0].node[0]
        if _ident in self.wrong_idents:
            self.e_print(_ident + " = wrong identify")
            self.e_print(node.leaves[0].leaves[0].leaves[0].node)
            # exit(0)
        self.wrong_idents.append(_ident)
        text = ''
        if beg < end:
            siz = end - beg + 1
            text = "    " + _ident + " dw " + str(siz) + " dup(" + str(num) + ")\n"
            # beg (?)
            # siz (num)
        else:
            self.e_print("wrong range in:")
            self.e_print(node.leaves[3].leaves[1].leaves[0].node[0])
            # exit(0)
        return text

    def vars(self):
        pass

    def consts(self, node):
        _ident = node.leaves[0].leaves[0].leaves[0].node[0]
        if _ident in self.wrong_idents:
            self.e_print(_ident + " = wrong identify")
            self.e_print(node.leaves[0].leaves[0].leaves[0].node[0])
            # exit(0)
        text = "    " + _ident + " dq "
        if len(node.leaves[2].leaves) == 2:
            text += "-" + str(node.leaves[2].leaves[1].leaves[0].leaves[0].node[0])
        elif '<unsigned-constant>' == node.leaves[2].leaves[0].node:
            text += str(node.leaves[2].leaves[0].leaves[0].leaves[0].node[0])
        else:
            text += str(node.leaves[2].leaves[0].leaves[0].leaves[0].leaves[0].node[0])
            text += ", "
            text += str(node.leaves[2].leaves[0].leaves[0].leaves[1].leaves[0].node[0])
        text += '\n'
        return text

    def statement(self, node):
        text = ''
        if node.leaves[0].node[0] == 'LINK':
            _var = node.leaves[1].leaves[0].leaves[0].node[0]
            _code = node.leaves[3].leaves[0].node[0]
            if _var in self.signals:
                self.links[_code] = _var
            else:
                self.e_print("var for this link dose not exist in:")
                self.e_print(node.leaves[1].leaves[0].leaves[0].node)
                # exit(0)
        elif node.leaves[0].node[0] == 'OUT':
            _code = node.leaves[1].leaves[0].node[0]
            self.outs.append(_code)
            if _code in self.links and (_code not in self.ins):
                text += "    OUT EBX," + str(_code) + "\n"
                text += "    mov " + self.links[_code] + ", EBX\n"
            else:
                self.e_print("unlinked or same var in:")
                self.e_print(node.leaves[1].leaves[0].node)
                # exit(0)
        elif node.leaves[0].node[0] == 'IN':
            _code = node.leaves[1].leaves[0].node[0]
            self.ins.append(_code)
            if _code in self.links and (_code not in self.outs):
                text += "    mov EAX, " + self.links[_code] + "\n"
                text += "    IN EAX," + str(_code) + "\n"
            else:
                self.e_print("unlinked or same var in:")
                self.e_print(node.leaves[1].leaves[0].node)
                # exit(0)
        return text

    def compile(self, node):
        if node.node[0] == 'PROGRAM':
            self.text += self.prog(node.parent)
        if node.node[0] == 'PROCEDURE':
            self.text += self.proc(node.parent)
            self.text += '\n'
        if node.node == '<declarations>':
            self.text += "DATA segment\n"
        if node.node == '<constant-declaration>':
            self.text += self.consts(node)
        if node.node == '<function>':
            self.text += self.deffunc(node)
        if node.node == '<variable-declarations>':
            if node.leaves:
                self.text += self.declaration_check(node.leaves[1], 1)
        if node.node == '<procedure-declarations>':
            self.text += 'DATA ENDS\n\n'
        if node.node[0] == 'BEGIN':
            self.text += 'CODE SEGMENT\n'
            self.text += '        assume ds:data, cs:code\n'
            self.text += 'begin:\n'
        if node.node == '<statement-list>':
            if node.leaves:
                for _ in node.leaves:
                    self.text += self.statement(_)
            else:
                self.text += '    nop\n'
        if node.node[0] == 'END':
            self.text += "    mov ax, 4c00h\n"
            self.text += "    int 21h\n"
            self.text += "CODE ENDS\n"
            self.text += "    end begin\n"
        for _ in node.leaves:
            self.compile(_)
