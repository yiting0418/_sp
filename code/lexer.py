"""lexer.py — 台文程式語言詞法分析器"""
import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional

class TT(Enum):
    INTEGER=auto(); FLOAT=auto(); STRING=auto()
    BOOL_TRUE=auto(); BOOL_FALSE=auto(); IDENT=auto()
    TONG_TSO=auto(); NA_SI=auto(); NA_BO=auto(); TNG=auto()
    SEH_LIN_LONG=auto(); KE_SIOK=auto(); TNG_KHI=auto()
    HAM_SO=auto(); TO_TNG=auto(); KONG=auto(); MNG=auto()
    KAH=auto(); IAH_SI=auto(); M_SI=auto(); KAU=auto(); KE=auto()
    PÊNN_PÊNN=auto(); BÔ_PÊNN=auto(); KHAH_SÈ=auto()
    KHAH_TUĀ=auto(); BÔ_KHAH_TUĀ=auto(); BÔ_KHAH_SÈ=auto()
    PLUS=auto(); MINUS=auto(); STAR=auto(); SLASH=auto(); PERCENT=auto()
    EQ=auto(); LPAREN=auto(); RPAREN=auto(); LBRACE=auto(); RBRACE=auto()
    LBRACKET=auto(); RBRACKET=auto(); COMMA=auto(); DOT=auto()
    SEMICOLON=auto(); EOF=auto()

KEYWORDS = {
    "tòng-tsò": TT.TONG_TSO, "nā-sī": TT.NA_SI, "nā-bô": TT.NA_BO,
    "tng": TT.TNG, "se\u030dh-lin-long": TT.SEH_LIN_LONG,
    "kè-sio\u030dk": TT.KE_SIOK, "tn\u0304g-khì": TT.TNG_KHI,
    "hàm-sò": TT.HAM_SO, "tò-tńg": TT.TO_TNG,
    "kóng": TT.KONG, "mn\u0304g": TT.MNG,
    "kah": TT.KAH, "ia\u030dh-sī": TT.IAH_SI, "m\u0304-sī": TT.M_SI,
    "kàu": TT.KAU, "kè": TT.KE,
    "pênn-pênn": TT.PÊNN_PÊNN, "bô-pênn": TT.BÔ_PÊNN,
    "khah-sè": TT.KHAH_SÈ, "khah-tuā": TT.KHAH_TUĀ,
    "bô-khah-tuā": TT.BÔ_KHAH_TUĀ, "bô-khah-sè": TT.BÔ_KHAH_SÈ,
    "si\u030dt-tsāi": TT.BOOL_TRUE, "bô-si\u030dt": TT.BOOL_FALSE,
}
SORTED_KEYWORDS = sorted(KEYWORDS.keys(), key=len, reverse=True)

@dataclass
class Token:
    type: TT; value: object; line: int; col: int
    def __repr__(self): return f"Token({self.type.name},{self.value!r},L{self.line})"

class LexError(Exception):
    def __init__(self, msg, line, col):
        super().__init__(f"[詞法錯誤 L{line}:C{col}] {msg}")

class Lexer:
    def __init__(self, source):
        self.src=source; self.pos=0; self.line=1; self.col=1; self.tokens=[]

    def error(self, msg): raise LexError(msg, self.line, self.col)
    def peek(self, o=0):
        p=self.pos+o; return self.src[p] if p<len(self.src) else None
    def advance(self):
        ch=self.src[self.pos]; self.pos+=1
        if ch=='\n': self.line+=1; self.col=1
        else: self.col+=1
        return ch
    def skip_ws(self):
        while self.pos < len(self.src):
            ch=self.peek()
            if ch in (' ','\t','\r','\n'): self.advance()
            elif ch=='/' and self.peek(1)=='/':
                while self.pos<len(self.src) and self.peek()!='\n': self.advance()
            elif ch=='/' and self.peek(1)=='*':
                self.advance(); self.advance()
                while self.pos<len(self.src):
                    if self.peek()=='*' and self.peek(1)=='/': self.advance(); self.advance(); break
                    self.advance()
            else: break
    def read_string(self):
        line,col=self.line,self.col; self.advance(); buf=[]
        while self.pos<len(self.src):
            ch=self.peek()
            if ch=='"': self.advance(); return Token(TT.STRING,''.join(buf),line,col)
            elif ch=='\\': self.advance(); esc=self.advance(); buf.append({'n':'\n','t':'\t','"':'"','\\':'\\'}.get(esc,esc))
            else: buf.append(self.advance())
        self.error("字串未關閉")
    def read_number(self):
        line,col=self.line,self.col; buf=[]; is_float=False
        while self.pos<len(self.src):
            ch=self.peek()
            if ch and ch.isdigit(): buf.append(self.advance())
            elif ch=='.' and not is_float and self.peek(1) and self.peek(1).isdigit():
                is_float=True; buf.append(self.advance())
            else: break
        s=''.join(buf)
        return Token(TT.FLOAT,float(s),line,col) if is_float else Token(TT.INTEGER,int(s),line,col)
    def try_keyword(self):
        line,col=self.line,self.col
        for kw in SORTED_KEYWORDS:
            if self.src[self.pos:self.pos+len(kw)]==kw:
                end=self.pos+len(kw)
                if end<len(self.src):
                    nch=self.src[end]
                    if nch.isalnum() or nch=='_': continue
                for _ in kw: self.advance()
                return Token(KEYWORDS[kw],kw,line,col)
        return None
    def read_ident(self):
        line,col=self.line,self.col; buf=[]
        while self.pos<len(self.src):
            ch=self.peek()
            if ch and (ch.isalpha() or ch.isdigit() or ch in('_','-') or ord(ch)>127): buf.append(self.advance())
            else: break
        return Token(TT.IDENT,''.join(buf),line,col)
    def tokenize(self):
        simple={'+':TT.PLUS,'-':TT.MINUS,'*':TT.STAR,'/':TT.SLASH,'%':TT.PERCENT,
                '=':TT.EQ,'(':TT.LPAREN,')':TT.RPAREN,'{':TT.LBRACE,'}':TT.RBRACE,
                '[':TT.LBRACKET,']':TT.RBRACKET,',':TT.COMMA,'.':TT.DOT,';':TT.SEMICOLON}
        while True:
            self.skip_ws()
            if self.pos>=len(self.src):
                self.tokens.append(Token(TT.EOF,None,self.line,self.col)); break
            line,col=self.line,self.col; ch=self.peek()
            if ch=='"': self.tokens.append(self.read_string())
            elif ch and ch.isdigit(): self.tokens.append(self.read_number())
            elif ch in simple: self.advance(); self.tokens.append(Token(simple[ch],ch,line,col))
            else:
                tok=self.try_keyword()
                if tok: self.tokens.append(tok)
                elif ch and (ch.isalpha() or ch=='_' or ord(ch)>127): self.tokens.append(self.read_ident())
                else: self.error(f"無法識別：{ch!r}")
        return self.tokens
