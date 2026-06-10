"""parser.py — 台文程式語言語法分析器（遞迴下降）"""
from typing import List, Optional
from lexer import Token, TT
from ast_nodes import *

class ParseError(Exception):
    def __init__(self, msg, tok):
        super().__init__(f"[語法錯誤 L{tok.line}:C{tok.col}] {msg}（得著：{tok.type.name} {tok.value!r}）")

class Parser:
    def __init__(self, tokens):
        self.tokens=tokens; self.pos=0
    def current(self): return self.tokens[self.pos]
    def peek(self, o=1): p=self.pos+o; return self.tokens[p] if p<len(self.tokens) else self.tokens[-1]
    def error(self, msg): raise ParseError(msg, self.current())
    def expect(self, tt):
        tok=self.current()
        if tok.type!=tt: self.error(f"期待 {tt.name}")
        self.pos+=1; return tok
    def check(self, *types): return self.current().type in types
    def match(self, *types):
        if self.check(*types): tok=self.current(); self.pos+=1; return tok
        return None
    def parse(self):
        body=[]
        while not self.check(TT.EOF): body.append(self.statement())
        return Program(body)
    def block(self):
        self.expect(TT.LBRACE); stmts=[]
        while not self.check(TT.RBRACE, TT.EOF): stmts.append(self.statement())
        self.expect(TT.RBRACE); return Block(stmts)
    def statement(self):
        t=self.current().type
        if t==TT.TONG_TSO: return self.var_decl()
        if t==TT.NA_SI:    return self.if_stmt()
        if t==TT.TNG:      return self.while_stmt()
        if t==TT.SEH_LIN_LONG: return self.for_stmt()
        if t==TT.HAM_SO:   return self.func_decl()
        if t==TT.TO_TNG:   return self.return_stmt()
        if t==TT.TNG_KHI:  self.pos+=1; self.match(TT.SEMICOLON); return BreakStmt()
        if t==TT.KE_SIOK:  self.pos+=1; self.match(TT.SEMICOLON); return ContinueStmt()
        if t==TT.KONG:     return self.print_stmt()
        if t==TT.MNG:      return self.input_stmt()
        if t==TT.LBRACE:   return self.block()
        return self.assign_or_expr()
    def var_decl(self):
        self.expect(TT.TONG_TSO); name=self.expect(TT.IDENT).value
        self.expect(TT.EQ); value=self.expression(); self.match(TT.SEMICOLON)
        return VarDecl(name, value)
    def assign_or_expr(self):
        if self.check(TT.IDENT) and self.peek().type==TT.EQ:
            name=self.expect(TT.IDENT).value; self.expect(TT.EQ)
            value=self.expression(); self.match(TT.SEMICOLON)
            return Assign(name, value)
        expr=self.expression(); self.match(TT.SEMICOLON); return expr
    def if_stmt(self):
        self.expect(TT.NA_SI); cond=self.expression(); then=self.block()
        else_c=None
        if self.match(TT.NA_BO):
            else_c=self.if_stmt() if self.check(TT.NA_SI) else self.block()
        return IfStmt(cond, then, else_c)
    def while_stmt(self):
        self.expect(TT.TNG); cond=self.expression(); body=self.block()
        return WhileStmt(cond, body)
    def for_stmt(self):
        self.expect(TT.SEH_LIN_LONG); var=self.expect(TT.IDENT).value
        self.expect(TT.EQ); start=self.expression(); self.expect(TT.KAU)
        end=self.expression(); step=None
        if self.match(TT.KE): step=self.expression()
        body=self.block(); return ForStmt(var, start, end, step, body)
    def func_decl(self):
        self.expect(TT.HAM_SO); name=self.expect(TT.IDENT).value
        self.expect(TT.LPAREN); params=[]
        if not self.check(TT.RPAREN):
            params.append(self.expect(TT.IDENT).value)
            while self.match(TT.COMMA): params.append(self.expect(TT.IDENT).value)
        self.expect(TT.RPAREN); body=self.block()
        return FuncDecl(name, params, body)
    def return_stmt(self):
        self.expect(TT.TO_TNG)
        value=None
        if not self.check(TT.SEMICOLON, TT.RBRACE, TT.EOF): value=self.expression()
        self.match(TT.SEMICOLON); return ReturnStmt(value)
    def print_stmt(self):
        self.expect(TT.KONG); value=self.expression(); self.match(TT.SEMICOLON)
        return PrintStmt(value)
    def input_stmt(self):
        self.expect(TT.MNG); var=self.expect(TT.IDENT).value; self.match(TT.SEMICOLON)
        return InputStmt(var)
    def expression(self): return self.logic_or()
    def logic_or(self):
        left=self.logic_and()
        while self.check(TT.IAH_SI):
            self.pos+=1; right=self.logic_and(); left=LogicalOp(left,"ia\u030dh-sī",right)
        return left
    def logic_and(self):
        left=self.logic_not()
        while self.check(TT.KAH):
            self.pos+=1; right=self.logic_not(); left=LogicalOp(left,"kah",right)
        return left
    def logic_not(self):
        if self.check(TT.M_SI): self.pos+=1; return NotOp(self.logic_not())
        return self.comparison()
    COPS={TT.PÊNN_PÊNN:"pênn-pênn",TT.BÔ_PÊNN:"bô-pênn",
          TT.KHAH_SÈ:"khah-sè",TT.KHAH_TUĀ:"khah-tuā",
          TT.BÔ_KHAH_TUĀ:"bô-khah-tuā",TT.BÔ_KHAH_SÈ:"bô-khah-sè"}
    def comparison(self):
        left=self.addition()
        while self.current().type in self.COPS:
            op=self.COPS[self.current().type]; self.pos+=1
            right=self.addition(); left=CompareOp(left,op,right)
        return left
    def addition(self):
        left=self.multiplication()
        while self.check(TT.PLUS,TT.MINUS):
            op=self.current().value; self.pos+=1
            right=self.multiplication(); left=BinaryOp(left,op,right)
        return left
    def multiplication(self):
        left=self.unary()
        while self.check(TT.STAR,TT.SLASH,TT.PERCENT):
            op=self.current().value; self.pos+=1
            right=self.unary(); left=BinaryOp(left,op,right)
        return left
    def unary(self):
        if self.check(TT.MINUS): self.pos+=1; return UnaryOp("-",self.unary())
        if self.check(TT.M_SI):  self.pos+=1; return NotOp(self.unary())
        return self.postfix()
    def postfix(self):
        node=self.primary()
        while True:
            if self.match(TT.LBRACKET):
                idx=self.expression(); self.expect(TT.RBRACKET); node=Index(node,idx)
            elif self.match(TT.LPAREN):
                args=[]
                if not self.check(TT.RPAREN):
                    args.append(self.expression())
                    while self.match(TT.COMMA): args.append(self.expression())
                self.expect(TT.RPAREN); node=FuncCall(node,args)
            else: break
        return node
    def primary(self):
        tok=self.current()
        if tok.type==TT.INTEGER:   self.pos+=1; return NumberLiteral(tok.value,True)
        if tok.type==TT.FLOAT:     self.pos+=1; return NumberLiteral(tok.value,False)
        if tok.type==TT.STRING:    self.pos+=1; return StringLiteral(tok.value)
        if tok.type==TT.BOOL_TRUE: self.pos+=1; return BoolLiteral(True)
        if tok.type==TT.BOOL_FALSE:self.pos+=1; return BoolLiteral(False)
        if tok.type==TT.IDENT:     self.pos+=1; return Identifier(tok.value)
        if tok.type==TT.LBRACKET:
            self.pos+=1; elems=[]
            if not self.check(TT.RBRACKET):
                elems.append(self.expression())
                while self.match(TT.COMMA): elems.append(self.expression())
            self.expect(TT.RBRACKET); return ArrayLiteral(elems)
        if tok.type==TT.LPAREN:
            self.pos+=1; expr=self.expression(); self.expect(TT.RPAREN); return expr
        self.error(f"無法解析的表達式：{tok.value!r}")
