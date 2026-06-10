"""compiler.py — 台文位元組碼編譯器"""
from enum import IntEnum, auto
from ast_nodes import *
from typing import List, Any, Optional

class Op(IntEnum):
    PUSH_INT=auto(); PUSH_FLOAT=auto(); PUSH_STR=auto()
    PUSH_TRUE=auto(); PUSH_FALSE=auto(); PUSH_NULL=auto()
    POP=auto(); DUP=auto()
    LOAD=auto(); STORE=auto(); DEFINE=auto()
    ADD=auto(); SUB=auto(); MUL=auto(); DIV=auto(); MOD=auto(); NEG=auto()
    EQ=auto(); NEQ=auto(); LT=auto(); GT=auto(); LE=auto(); GE=auto()
    NOT=auto(); AND=auto(); OR=auto()
    BUILD_ARRAY=auto(); INDEX=auto()
    JUMP=auto(); JUMP_IF_FALSE=auto(); JUMP_IF_TRUE=auto()
    MAKE_FUNC=auto(); CALL=auto(); RETURN=auto(); RETURN_NONE=auto()
    PRINT=auto(); INPUT=auto(); HALT=auto()

class Instruction:
    __slots__=('op','arg')
    def __init__(self,op,arg=None): self.op=op; self.arg=arg
    def __repr__(self): return f"{self.op.name:20s} {self.arg if self.arg is not None else ''}"

class CompiledFunction:
    def __init__(self,name,params,code): self.name=name; self.params=params; self.code=code
    def __repr__(self): return f"<CompiledFunction {self.name}>"

class CompileError(Exception): pass

class Compiler:
    def __init__(self):
        self.code=[]; self.constants=[]; self.functions=[]; self._loops=[]
    def emit(self,op,arg=None):
        self.code.append(Instruction(op,arg)); return len(self.code)-1
    def str_idx(self,s):
        if s not in self.constants: self.constants.append(s)
        return self.constants.index(s)
    def patch(self,i,t): self.code[i].arg=t
    def addr(self): return len(self.code)
    def compile(self,node):
        m=f"_c_{type(node).__name__}"
        fn=getattr(self,m,None)
        if fn is None: raise CompileError(f"未知節點：{type(node).__name__}")
        fn(node)
    def _c_Program(self,n):
        for s in n.body: self.compile(s)
        self.emit(Op.HALT)
    def _c_Block(self,n):
        for s in n.body: self.compile(s)
    def _c_VarDecl(self,n):
        self.compile(n.value); self.emit(Op.DEFINE,self.str_idx(n.name))
    def _c_Assign(self,n):
        self.compile(n.value); self.emit(Op.STORE,self.str_idx(n.name))
    def _c_NumberLiteral(self,n):
        self.emit(Op.PUSH_INT,int(n.value)) if n.is_int else self.emit(Op.PUSH_FLOAT,float(n.value))
    def _c_StringLiteral(self,n):
        self.emit(Op.PUSH_STR,self.str_idx(n.value))
    def _c_BoolLiteral(self,n):
        self.emit(Op.PUSH_TRUE if n.value else Op.PUSH_FALSE)
    def _c_NullLiteral(self,n): self.emit(Op.PUSH_NULL)
    def _c_ArrayLiteral(self,n):
        for e in n.elements: self.compile(e)
        self.emit(Op.BUILD_ARRAY,len(n.elements))
    def _c_Identifier(self,n): self.emit(Op.LOAD,self.str_idx(n.name))
    def _c_BinaryOp(self,n):
        self.compile(n.left); self.compile(n.right)
        self.emit({'+':Op.ADD,'-':Op.SUB,'*':Op.MUL,'/':Op.DIV,'%':Op.MOD}[n.op])
    def _c_UnaryOp(self,n):
        self.compile(n.operand)
        if n.op=='-': self.emit(Op.NEG)
    def _c_CompareOp(self,n):
        self.compile(n.left); self.compile(n.right)
        self.emit({"pênn-pênn":Op.EQ,"bô-pênn":Op.NEQ,"khah-sè":Op.LT,
                   "khah-tuā":Op.GT,"bô-khah-tuā":Op.LE,"bô-khah-sè":Op.GE}[n.op])
    def _c_LogicalOp(self,n):
        if n.op=="kah":
            self.compile(n.left); j=self.emit(Op.JUMP_IF_FALSE,None)
            self.emit(Op.POP); self.compile(n.right); self.patch(j,self.addr())
        else:
            self.compile(n.left); j=self.emit(Op.JUMP_IF_TRUE,None)
            self.emit(Op.POP); self.compile(n.right); self.patch(j,self.addr())
    def _c_NotOp(self,n): self.compile(n.operand); self.emit(Op.NOT)
    def _c_Index(self,n): self.compile(n.obj); self.compile(n.idx); self.emit(Op.INDEX)
    def _c_FuncCall(self,n):
        self.compile(n.callee)
        for a in n.args: self.compile(a)
        self.emit(Op.CALL,len(n.args))
    def _c_FuncDecl(self,n):
        sub=Compiler(); sub.constants=self.constants
        for s in n.body.body: sub.compile(s)
        sub.emit(Op.RETURN_NONE)
        # merge sub functions
        offset=len(self.functions)
        for f in sub.functions: self.functions.append(f)
        func=CompiledFunction(n.name,n.params,sub.code)
        self.functions.append(func)
        fidx=len(self.functions)-1
        self.emit(Op.MAKE_FUNC,fidx); self.emit(Op.DEFINE,self.str_idx(n.name))
    def _c_ReturnStmt(self,n):
        if n.value: self.compile(n.value); self.emit(Op.RETURN)
        else: self.emit(Op.RETURN_NONE)
    def _c_PrintStmt(self,n): self.compile(n.value); self.emit(Op.PRINT)
    def _c_InputStmt(self,n): self.emit(Op.INPUT); self.emit(Op.DEFINE,self.str_idx(n.var))
    def _c_IfStmt(self,n):
        self.compile(n.condition); jf=self.emit(Op.JUMP_IF_FALSE,None)
        self.compile(n.then_block)
        if n.else_block:
            je=self.emit(Op.JUMP,None); self.patch(jf,self.addr())
            self.compile(n.else_block); self.patch(je,self.addr())
        else: self.patch(jf,self.addr())
    def _c_WhileStmt(self,n):
        start=self.addr(); self.compile(n.condition); jend=self.emit(Op.JUMP_IF_FALSE,None)
        bps=[]; cps=[]; self._loops.append((bps,cps))
        self.compile(n.body); self.emit(Op.JUMP,start); self.patch(jend,self.addr())
        for p in bps: self.patch(p,self.addr())
        for p in cps: self.patch(p,start)
        self._loops.pop()
    def _c_ForStmt(self,n):
        vi=self.str_idx(n.var); ei=self.str_idx("__fe__"); si=self.str_idx("__fs__")
        self.compile(n.start); self.emit(Op.DEFINE,vi)
        self.compile(n.end);   self.emit(Op.DEFINE,ei)
        if n.step: self.compile(n.step)
        else: self.emit(Op.PUSH_INT,1)
        self.emit(Op.DEFINE,si)
        start=self.addr()
        self.emit(Op.LOAD,vi); self.emit(Op.LOAD,ei); self.emit(Op.LE)
        jend=self.emit(Op.JUMP_IF_FALSE,None)
        bps=[]; cps=[]; self._loops.append((bps,cps))
        self.compile(n.body)
        # step_addr: continue jumps here (step increment then re-check)
        step_addr=self.addr()
        self.emit(Op.LOAD,vi); self.emit(Op.LOAD,si); self.emit(Op.ADD); self.emit(Op.STORE,vi)
        self.emit(Op.JUMP,start); self.patch(jend,self.addr())
        for p in bps: self.patch(p,self.addr())
        for p in cps: self.patch(p,step_addr)  # continue -> increment, not start
        self._loops.pop()
    def _c_BreakStmt(self,n):
        if not self._loops: raise CompileError("tn̄g-khì 必須在迴圈內")
        self._loops[-1][0].append(self.emit(Op.JUMP,None))
    def _c_ContinueStmt(self,n):
        if not self._loops: raise CompileError("kè-sio̍k 必須在迴圈內")
        self._loops[-1][1].append(self.emit(Op.JUMP,None))
    def get_bytecode(self):
        return {'code':self.code,'constants':self.constants,'functions':self.functions}
