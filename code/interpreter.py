"""interpreter.py — 台文程式語言直譯器（樹狀走訪）"""
from ast_nodes import *
from typing import Any, Dict, Optional

class TaiBunError(Exception): pass
class ReturnSignal(Exception):
    def __init__(self, v): self.value=v
class BreakSignal(Exception): pass
class ContinueSignal(Exception): pass

class Environment:
    def __init__(self, parent=None):
        self.vars={}; self.parent=parent
    def get(self, name):
        if name in self.vars: return self.vars[name]
        if self.parent: return self.parent.get(name)
        raise TaiBunError(f"變數 '{name}' 無定義")
    def set(self, name, value):
        if name in self.vars: self.vars[name]=value; return
        if self.parent and self.parent.has(name): self.parent.set(name,value); return
        self.vars[name]=value
    def define(self, name, value): self.vars[name]=value
    def has(self, name):
        if name in self.vars: return True
        return self.parent.has(name) if self.parent else False

class TaiBunFunction:
    def __init__(self, decl, closure): self.decl=decl; self.closure=closure
    def __repr__(self): return f"<hàm-sò {self.decl.name}>"

class Interpreter:
    def __init__(self): self.global_env=Environment()
    def execute(self, node, env=None):
        if env is None: env=self.global_env
        return self._v(node,env)
    def _v(self, node, env):
        m=f"_v_{type(node).__name__}"
        fn=getattr(self,m,None)
        if fn is None: raise TaiBunError(f"未知節點：{type(node).__name__}")
        return fn(node,env)
    def _v_Program(self,n,e):
        r=None
        for s in n.body: r=self._v(s,e)
        return r
    def _v_Block(self,n,e):
        local=Environment(e); r=None
        for s in n.body: r=self._v(s,local)
        return r
    def _v_VarDecl(self,n,e):
        v=self._v(n.value,e); e.define(n.name,v); return v
    def _v_Assign(self,n,e):
        v=self._v(n.value,e); e.set(n.name,v); return v
    def _v_NumberLiteral(self,n,e): return n.value
    def _v_StringLiteral(self,n,e): return n.value
    def _v_BoolLiteral(self,n,e): return n.value
    def _v_NullLiteral(self,n,e): return None
    def _v_ArrayLiteral(self,n,e): return [self._v(x,e) for x in n.elements]
    def _v_Identifier(self,n,e): return e.get(n.name)
    def _v_BinaryOp(self,n,e):
        l=self._v(n.left,e); r=self._v(n.right,e)
        if n.op=='+':
            if isinstance(l,str) or isinstance(r,str): return self._s(l)+self._s(r)
            return l+r
        elif n.op=='-': return l-r
        elif n.op=='*': return l*r
        elif n.op=='/':
            if r==0: raise TaiBunError("除以零！")
            return l/r
        elif n.op=='%': return l%r
    def _v_UnaryOp(self,n,e):
        v=self._v(n.operand,e)
        if n.op=='-': return -v
    def _v_CompareOp(self,n,e):
        l=self._v(n.left,e); r=self._v(n.right,e); o=n.op
        if o=="pênn-pênn":    return l==r
        if o=="bô-pênn":     return l!=r
        if o=="khah-sè":     return l<r
        if o=="khah-tuā":    return l>r
        if o=="bô-khah-tuā": return l<=r
        if o=="bô-khah-sè":  return l>=r
    def _v_LogicalOp(self,n,e):
        if n.op=="kah":     return self._t(self._v(n.left,e)) and self._t(self._v(n.right,e))
        if n.op=="ia\u030dh-sī": l=self._v(n.left,e); return l if self._t(l) else self._v(n.right,e)
    def _v_NotOp(self,n,e): return not self._t(self._v(n.operand,e))
    def _v_Index(self,n,e):
        o=self._v(n.obj,e); i=self._v(n.idx,e); return o[int(i)]
    def _v_FuncCall(self,n,e):
        callee=self._v(n.callee,e); args=[self._v(a,e) for a in n.args]
        if callable(callee): return callee(args)
        if isinstance(callee,TaiBunFunction):
            fe=Environment(callee.closure)
            if len(args)!=len(callee.decl.params):
                raise TaiBunError(f"函式 '{callee.decl.name}' 期待 {len(callee.decl.params)} 個參數，得著 {len(args)} 個")
            for p,a in zip(callee.decl.params,args): fe.define(p,a)
            try: self._v_Block(callee.decl.body,fe)
            except ReturnSignal as r: return r.value
            return None
        raise TaiBunError(f"無法呼叫：{callee!r}")
    def _v_FuncDecl(self,n,e):
        f=TaiBunFunction(n,e); e.define(n.name,f); return f
    def _v_ReturnStmt(self,n,e): raise ReturnSignal(self._v(n.value,e) if n.value else None)
    def _v_BreakStmt(self,n,e): raise BreakSignal()
    def _v_ContinueStmt(self,n,e): raise ContinueSignal()
    def _v_PrintStmt(self,n,e): v=self._v(n.value,e); print(self._s(v)); return v
    def _v_InputStmt(self,n,e):
        raw=input()
        try: val=int(raw)
        except ValueError:
            try: val=float(raw)
            except: val=raw
        e.set(n.var,val) if e.has(n.var) else e.define(n.var,val); return val
    def _v_IfStmt(self,n,e):
        if self._t(self._v(n.condition,e)): return self._v(n.then_block,e)
        elif n.else_block: return self._v(n.else_block,e)
    def _v_WhileStmt(self,n,e):
        while self._t(self._v(n.condition,e)):
            try: self._v(n.body,e)
            except BreakSignal: break
            except ContinueSignal: continue
    def _v_ForStmt(self,n,e):
        start=int(self._v(n.start,e)); end=int(self._v(n.end,e))
        step=int(self._v(n.step,e)) if n.step else 1
        le=Environment(e)
        for i in range(start,end+1,step):
            le.define(n.var,i)
            try: self._v(n.body,le)
            except BreakSignal: break
            except ContinueSignal: continue
    def _t(self,v):
        if v is None or v is False: return False
        if isinstance(v,(int,float)) and v==0: return False
        if isinstance(v,str) and v=='': return False
        if isinstance(v,list) and len(v)==0: return False
        return True
    def _s(self,v):
        if v is True:  return "si\u030dt-tsāi"
        if v is False: return "bô-si\u030dt"
        if v is None:  return "bô"
        if isinstance(v,list): return "["+", ".join(self._s(x) for x in v)+"]"
        if isinstance(v,float) and v==int(v): return str(int(v))
        return str(v)
    # Alias for external use
    def _tai_str(self, v): return self._s(v)
