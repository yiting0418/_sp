"""vm.py — 台文虛擬機 TaiVM（堆疊機架構）"""
from compiler import Op, Instruction, CompiledFunction
from typing import List, Any

class VMError(Exception): pass

class TaiVM:
    def __init__(self, bytecode):
        self.main_code = bytecode['code']
        self.constants  = bytecode['constants']
        self.func_defs  = bytecode['functions']
        self.stack: List[Any] = []

    def push(self,v): self.stack.append(v)
    def pop(self):    return self.stack.pop()
    def peek(self):   return self.stack[-1]

    def _s(self,v):
        if v is True:  return "si\u030dt-tsāi"
        if v is False: return "bô-si\u030dt"
        if v is None:  return "bô"
        if isinstance(v,list): return "["+", ".join(self._s(x) for x in v)+"]"
        if isinstance(v,float) and v==int(v): return str(int(v))
        return str(v)

    def _t(self,v):
        if v is None or v is False or v==0 or v=='' or v==[]: return False
        return True

    def run(self):
        # 每個框架: {'code':..., 'ip':..., 'envs':[dict,...]}
        global_env = {}
        frames = [{'code': self.main_code, 'ip': 0, 'envs': [global_env]}]

        def envs():    return frames[-1]['envs']
        def cur_env(): return frames[-1]['envs'][-1]

        def lookup(name):
            for e in reversed(envs()):
                if name in e: return e[name]
            # 函式呼叫時也要能查到全域變數
            if name in global_env: return global_env[name]
            raise VMError(f"變數 '{name}' 無定義")

        def store(name, val):
            for e in reversed(envs()):
                if name in e: e[name]=val; return
            cur_env()[name]=val

        while frames:
            frame = frames[-1]
            code  = frame['code']
            if frame['ip'] >= len(code):
                frames.pop()
                self.push(None)
                continue
            instr = code[frame['ip']]; frame['ip']+=1
            op=instr.op; arg=instr.arg

            if   op==Op.PUSH_INT:   self.push(arg)
            elif op==Op.PUSH_FLOAT: self.push(arg)
            elif op==Op.PUSH_STR:   self.push(self.constants[arg])
            elif op==Op.PUSH_TRUE:  self.push(True)
            elif op==Op.PUSH_FALSE: self.push(False)
            elif op==Op.PUSH_NULL:  self.push(None)
            elif op==Op.POP:        self.pop()
            elif op==Op.DUP:        self.push(self.peek())
            elif op==Op.LOAD:       self.push(lookup(self.constants[arg]))
            elif op==Op.STORE:      store(self.constants[arg], self.pop())
            elif op==Op.DEFINE:     cur_env()[self.constants[arg]]=self.pop()
            elif op==Op.ADD:
                r,l=self.pop(),self.pop()
                self.push(self._s(l)+self._s(r) if isinstance(l,str) or isinstance(r,str) else l+r)
            elif op==Op.SUB:  r,l=self.pop(),self.pop(); self.push(l-r)
            elif op==Op.MUL:  r,l=self.pop(),self.pop(); self.push(l*r)
            elif op==Op.DIV:
                r,l=self.pop(),self.pop()
                if r==0: raise VMError("除以零！")
                self.push(l/r)
            elif op==Op.MOD:  r,l=self.pop(),self.pop(); self.push(l%r)
            elif op==Op.NEG:  self.push(-self.pop())
            elif op==Op.EQ:   r,l=self.pop(),self.pop(); self.push(l==r)
            elif op==Op.NEQ:  r,l=self.pop(),self.pop(); self.push(l!=r)
            elif op==Op.LT:   r,l=self.pop(),self.pop(); self.push(l<r)
            elif op==Op.GT:   r,l=self.pop(),self.pop(); self.push(l>r)
            elif op==Op.LE:   r,l=self.pop(),self.pop(); self.push(l<=r)
            elif op==Op.GE:   r,l=self.pop(),self.pop(); self.push(l>=r)
            elif op==Op.NOT:  self.push(not self._t(self.pop()))
            elif op==Op.AND:  r,l=self.pop(),self.pop(); self.push(self._t(l) and self._t(r))
            elif op==Op.OR:   r,l=self.pop(),self.pop(); self.push(l if self._t(l) else r)
            elif op==Op.BUILD_ARRAY:
                elems=[self.pop() for _ in range(arg)]; self.push(list(reversed(elems)))
            elif op==Op.INDEX: idx,obj=self.pop(),self.pop(); self.push(obj[int(idx)])
            elif op==Op.JUMP:          frame['ip']=arg
            elif op==Op.JUMP_IF_FALSE:
                v=self.pop()
                if not self._t(v): frame['ip']=arg
            elif op==Op.JUMP_IF_TRUE:
                v=self.peek()
                if self._t(v): frame['ip']=arg
            elif op==Op.MAKE_FUNC: self.push(self.func_defs[arg])
            elif op==Op.CALL:
                n_args=arg
                al=[self.pop() for _ in range(n_args)]; al.reverse()
                func=self.pop()
                if not isinstance(func,CompiledFunction):
                    raise VMError(f"無法呼叫：{func!r}")
                if len(al)!=len(func.params):
                    raise VMError(f"函式 '{func.name}' 參數數量不符")
                new_env={p:a for p,a in zip(func.params,al)}
                frames.append({'code':func.code,'ip':0,'envs':[new_env]})
            elif op==Op.RETURN:
                ret=self.pop(); frames.pop(); self.push(ret)
            elif op==Op.RETURN_NONE:
                frames.pop(); self.push(None)
            elif op==Op.PRINT: print(self._s(self.pop()))
            elif op==Op.INPUT:
                raw=input()
                try: self.push(int(raw))
                except:
                    try: self.push(float(raw))
                    except: self.push(raw)
            elif op==Op.HALT: break

    def disassemble(self):
        print("=== TaiVM 位元組碼 ===")
        for i,ins in enumerate(self.main_code):
            a=""
            if ins.arg is not None:
                if ins.op in (Op.PUSH_STR,Op.LOAD,Op.STORE,Op.DEFINE):
                    try: a=f"{ins.arg} ({self.constants[ins.arg]!r})"
                    except: a=str(ins.arg)
                else: a=str(ins.arg)
            print(f"  {i:4d}  {ins.op.name:20s} {a}")
        print()
        for fn in self.func_defs:
            print(f"=== 函式: {fn.name}（參數：{fn.params}）===")
            for i,ins in enumerate(fn.code):
                print(f"  {i:4d}  {ins.op.name:20s} {ins.arg if ins.arg is not None else ''}")
            print()
