#!/usr/bin/env python3
"""SSA form — convert variable assignments to SSA."""
class SSAConverter:
    def __init__(self):self.counters={};self.stacks={};self.result=[]
    def _fresh(self,var):
        self.counters.setdefault(var,0);self.counters[var]+=1
        name=f"{var}_{self.counters[var]}"
        self.stacks.setdefault(var,[]).append(name);return name
    def _current(self,var):
        if var not in self.stacks or not self.stacks[var]:return var
        return self.stacks[var][-1]
    def convert(self,stmts):
        self.result=[]
        for stmt in stmts:
            if stmt[0]=="assign":
                var,expr=stmt[1],stmt[2]
                new_expr=self._rename_expr(expr)
                new_var=self._fresh(var)
                self.result.append(("assign",new_var,new_expr))
            elif stmt[0]=="use":
                self.result.append(("use",self._rename_expr(stmt[1])))
        return self.result
    def _rename_expr(self,expr):
        if isinstance(expr,str):return self._current(expr)
        if isinstance(expr,tuple):
            return tuple(self._rename_expr(e) if isinstance(e,str) else e for e in expr)
        return expr
def main():
    stmts=[("assign","x",1),("assign","y",("add","x",2)),("assign","x",("add","x","y")),("use","x")]
    ssa=SSAConverter();result=ssa.convert(stmts)
    for s in result:print(s)
if __name__=="__main__":main()
