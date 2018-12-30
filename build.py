# -*- coding: utf-8 -*-
# 根据python代码，构建ast树
import ast

leaf_list = ['Load', 'Store', 'Del', 'AugLoad', 'AugStore', 'Param', 
             'Add', 'Sub', 'Mult', 'MatMult' 'Div', 'Mod', 'Pow', 'LShift', 'RShift', 'BitOr', 'BitXor', 'BitAnd', 'FloorDiv',
             'Invert', 'Not', 'UAdd', 'USub',
             'Eq', 'NotEq', 'Lt', 'LtE', 'Gt', 'GtE', 'Is', 'IsNot', 'In', 'NotIn']

class CodeVisitor(ast.NodeVisitor):
    def __init__(self):
        super(CodeVisitor, self).__init__()
        self.ast = ""

    def generic_visit(self, node):
        name = node.__class__.__name__
        if name in leaf_list:
            return name
        else:
            self.ast += name + " "
            ast.NodeVisitor.generic_visit(self, node)
            return None
 
    def visit_FunctionDef(self, node):

        self.ast += (type(node).__name__) + " "
        self.ast += node.name + " "
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Attribute(self, node):

        self.ast += (type(node).__name__) + " "
        ast.NodeVisitor.visit(self, node.value)
        atype = ast.NodeVisitor.visit(self, node.ctx)

        self.ast += node.attr + " "
        self.ast += atype + " "
   
    def visit_ImportFrom(self, node):
        
        self.ast += (type(node).__name__) + " "
        self.ast += str(node.module) + " "
        ast.NodeVisitor.generic_visit(self, node)

    def visit_alias(self, node):

        self.ast += (node.name) + " "
        self.ast += (str(node.asname)) + " "

    def visit_Compare(self, node):
        op = ast.NodeVisitor.visit(self, node.ops[0])
        
        self.ast += (type(node).__name__)+ " "
        self.ast += (op) + " "
        ast.NodeVisitor.generic_visit(self, node)
          
    def visit_Name(self, node):
        ntype = ast.NodeVisitor.visit(self, node.ctx)
        self.ast += (node.id) + " "
        self.ast += (ntype) + " "

def read_file(code):
    f = open(code, 'r',encoding='UTF-8')
    file = f.read()
    try:
        ast_text = ast.parse(file, mode='exec')
    except:
        return "Module"
    # get AST str
    #tree = ast.dump(ast_text)
    #print (tree)
    # visit AST node
    visitor = CodeVisitor()
    visitor.visit(ast_text)
    return visitor.ast

def get_asts(file_list):
    ast_strs = []
    for file in file_list:
        ast_strs.append(read_file(file))
    return ast_strs

if __name__ == '__main__':
    file_name = "code_test.py"
    
    ast_str = read_file(file_name)
    print(ast_str)
