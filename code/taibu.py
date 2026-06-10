#!/usr/bin/env python3
"""
taibu.py — 台文程式語言主程式 Tâi-bûn-lang v1.0

  python taibu.py run    <file.taibu>        # 直譯模式
  python taibu.py compile <file.taibu> [-o f] # 編譯
  python taibu.py exec   <file.tbc>          # 執行位元組碼
  python taibu.py repl                       # 互動模式
  python taibu.py dis    <file.taibu>        # 反組譯
"""
import sys, os, pickle

from lexer import Lexer, LexError
from parser import Parser, ParseError
from interpreter import Interpreter, TaiBunError
from compiler import Compiler, CompileError
from vm import TaiVM, VMError

BANNER = """
╔══════════════════════════════════════════════════╗
║   台文程式語言  Tâi-bûn-lang  v1.0              ║
║   台灣閩南語羅馬字程式語言                        ║
║   輸入 .離開 或 lī-khui 結束                     ║
╚══════════════════════════════════════════════════╝
"""

def load(path):
    try:
        with open(path,encoding='utf-8') as f: return f.read()
    except FileNotFoundError:
        print(f"錯誤：找不到 '{path}'"); sys.exit(1)

def parse(src, fname="<input>"):
    try:
        return Parser(Lexer(src).tokenize()).parse()
    except LexError as e: print(f"[{fname}] {e}"); sys.exit(1)
    except ParseError as e: print(f"[{fname}] {e}"); sys.exit(1)

def cmd_run(path):
    ast=parse(load(path),path)
    interp=Interpreter()
    try: interp.execute(ast)
    except TaiBunError as e: print(f"[執行錯誤] {e}"); sys.exit(1)

def cmd_compile(path, out=None):
    ast=parse(load(path),path)
    c=Compiler()
    try: c.compile(ast)
    except CompileError as e: print(f"[編譯錯誤] {e}"); sys.exit(1)
    bc=c.get_bytecode()
    if out is None: out=os.path.splitext(path)[0]+".tbc"
    with open(out,'wb') as f: pickle.dump(bc,f)
    print(f"✓ 編譯完成：{out}")
    print(f"  指令：{len(bc['code'])}  函式：{len(bc['functions'])}  常數：{len(bc['constants'])}")

def cmd_exec(path):
    try:
        with open(path,'rb') as f: bc=pickle.load(f)
    except FileNotFoundError:
        print(f"錯誤：找不到 '{path}'"); sys.exit(1)
    vm=TaiVM(bc)
    try: vm.run()
    except VMError as e: print(f"[VM 錯誤] {e}"); sys.exit(1)

def cmd_dis(path):
    ast=parse(load(path),path)
    c=Compiler()
    try: c.compile(ast)
    except CompileError as e: print(f"[編譯錯誤] {e}"); sys.exit(1)
    TaiVM(c.get_bytecode()).disassemble()

def cmd_repl():
    print(BANNER)
    interp=Interpreter(); buf=[]
    while True:
        try:
            line=input("台文> " if not buf else "  ... ")
        except EOFError: print("\nkái-sàn!"); break
        if line.strip() in (".離開","lī-khui",".exit","quit()"): print("kái-sàn!"); break
        buf.append(line); src="\n".join(buf)
        try:
            ast=Parser(Lexer(src).tokenize()).parse()
        except: continue
        buf=[]
        try:
            r=interp.execute(ast)
            if r is not None: print(f"  => {interp._tai_str(r)}")
        except TaiBunError as e: print(f"[執行錯誤] {e}")
        except KeyboardInterrupt: print(); buf=[]

def main():
    args=sys.argv[1:]
    if not args: print(__doc__); sys.exit(0)
    cmd=args[0]
    if cmd=="run" and len(args)>=2: cmd_run(args[1])
    elif cmd=="compile" and len(args)>=2:
        out=args[args.index("-o")+1] if "-o" in args else None
        cmd_compile(args[1],out)
    elif cmd=="exec" and len(args)>=2: cmd_exec(args[1])
    elif cmd=="repl": cmd_repl()
    elif cmd=="dis" and len(args)>=2: cmd_dis(args[1])
    else: print(__doc__); sys.exit(1)

if __name__=="__main__": main()
