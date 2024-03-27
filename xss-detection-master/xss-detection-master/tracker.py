from __future__ import annotations
import esprima  # type: ignore
from esprima.esprima import nodes  # type: ignore
import escodegen  # type: ignore
from typing import List, TypeAlias, Tuple, Any
import re

# Expression: TypeAlias = nodes.nodes.ThisExpression | nodes.nodes.Identifier | nodes.nodes.Literal | nodes.nodes.ArrayExpression | nodes.nodes.ObjectExpression | nodes.nodes.FunctionExpression | nodes.nodes.ArrowFunctionExpression | nodes.nodes.ClassExpression | nodes.nodes.TaggedTemplateExpression | nodes.nodes.MemberExpression | nodes.nodes.Super | nodes.nodes.MetaProperty | nodes.nodes.NewExpression | nodes.nodes.CallExpression | nodes.nodes.UpdateExpression | nodes.nodes.AwaitExpression | nodes.nodes.UnaryExpression | nodes.nodes.BinaryExpression | nodes.nodes.LogicalExpression | nodes.nodes.ConditionalExpression | nodes.nodes.YieldExpression | nodes.nodes.AssignmentExpression | nodes.nodes.SequenceExpression
# Statement: TypeAlias = nodes.nodes.BlockStatement | nodes.nodes.BreakStatement | nodes.nodes.ContinueStatement | nodes.nodes.DebuggerStatement | nodes.nodes.DoWhileStatement | nodes.nodes.EmptyStatement | nodes.nodes.ExpressionStatement | nodes.nodes.ForStatement | nodes.nodes.ForInStatement | nodes.nodes.ForOfStatement | nodes.nodes.FunctionDeclaration | nodes.nodes.IfStatement | nodes.nodes.LabeledStatement | nodes.nodes.ReturnStatement | nodes.nodes.SwitchStatement | nodes.nodes.ThrowStatement | nodes.nodes.TryStatement | nodes.nodes.VariableDeclaration | nodes.nodes.WhileStatement | nodes.nodes.WithStatement
# Declaration: TypeAlias = nodes.nodes.ClassDeclaration | nodes.nodes.FunctionDeclaration | nodes.nodes.VariableDeclaration

Expression: TypeAlias = Any
Statement: TypeAlias = Any
Declaration: TypeAlias = Any


SOURCES = ['document.URL', 'document.documentURI', 'document.URLUnencoded',
           'document.baseURI', 'location.search', 'document.cookie', 'document.referrer']

SINKS = r'(?:document\.domain|innerHTML|outerHTML|insertAdjacentHTML|onevent)$'
SINK_FUNCTIONS = ['document.write', 'document.writeln']


class Controlled:
    def __init__(self, identifier: str, controllers: List[str], node: str):
        self.identifier = identifier
        self.controllers = controllers
        self.node = node


class SinkFunction:
    def __init__(self, name: str, sinked_params: List[int]):
        self.name = name
        self.sinked_params = sinked_params


controlled: dict[str, Controlled] = {}

sink_functions: dict[str, SinkFunction] = {}

for src in SOURCES:
    controlled[src] = Controlled(src, [], "default")


def is_controlled(obj) -> bool:
    if obj in controlled:
        return True
    return False


def is_sink(obj: str) -> bool:
    if re.search(SINKS, obj):
        return True
    return False


def is_sink_function(obj: str) -> bool:
    if obj in sink_functions:
        return True
    return False

# marks the obj as controlled by the sources


def mark(obj: str, controllers: List[str] | None, node: str) -> None:
    if (controllers is None) or (controllers is not None and len(controllers) != 0):
        controllers = [] if controllers is None else controllers
        controlled[obj] = Controlled(obj, controllers, node)


def unmark(obj: str) -> None:
    del controlled[obj]


def trace(obj: str) -> Tuple[str, str]:
    if obj not in controlled:
        return "",""
    if len(controlled[obj].controllers) == 0:
        return controlled[obj].node, obj
    for controller in controlled[obj].controllers:
        trace(controller)
    return "", ""


def mark_function_as_sink(node: nodes.nodes.FunctionDeclaration, sinked_objs: List[str]):
    if node.id == None:
        return
    if len(sinked_objs) == 0:
        return

    sinked_params: List[int] = []

    params = {}
    for idx, p in enumerate(node.params):
        params[gen(p)] = idx

    for sinked in sinked_objs:
        source_type, name = trace(sinked)
        if source_type == "function_param":
            sinked_params.append(params[name])

    name = gen(node.id)
    sink_functions[name] = SinkFunction(name, sinked_params)
    return None


def parse(code):
    return esprima.parse(code)


def gen(node) -> str:
    return escodegen.generate(node)

#  possible sources/controllers, sinked


def expression(expr: Expression | None) -> Tuple[List[str], List[str]]:
    sources: List[str] = []
    sinked: List[str] = []

    if expr == None:
        return sources, sinked

    elif isinstance(expr, nodes.Identifier):
        identifier = gen(expr)
        if is_controlled(identifier):
            return [identifier], []

    elif isinstance(expr, nodes.AssignmentExpression):
        left = gen(expr.left)
        controllers, _ = expression(expr.right)
        mark(left, controllers, gen(expr))
        if is_sink(left):
            for c in controllers:
                _, name = trace(c)
                print("Controlled var passed to sink")
                print(gen(expr))
                sinked.append(name)
        return [left], sinked

    elif isinstance(expr, nodes.CallExpression):
        so, si = expression(expr.callee)
        sinked.extend(si)
        sources.extend(so)
        callee = gen(expr.callee)
        if callee in SINK_FUNCTIONS:
            for arg in expr.arguments:
                so,si = expression(arg)
                for s in so:
                    print("Passing controlled var to sink function: ",s)
                    print(gen(expr))
                    sinked.extend(so)
                sources.extend(so)
                sinked.extend(si)
                if is_controlled(gen(arg)):
                    print("Passing controlled var to sink function")
                    print(gen(expr))
                    sinked.append(arg)
        elif is_sink_function(callee):
            sinked_params = sink_functions[callee].sinked_params
            for sinked_param in sinked_params:
                arg = gen(expr.arguments[sinked_param])
                if is_controlled(arg):
                    print("Passing controlled var to sink function")
                    print(gen(expr))
                    sinked.append(arg)

    elif isinstance(expr, nodes.TemplateLiteral):
        for e in expr.expressions:
            so, si = expression(e)
            sources.extend(so)
            sinked.extend(si)
        return sources, sinked

    elif isinstance(expr, nodes.StaticMemberExpression):
        string = gen(expr)
        object_sources, object_sinked = expression(expr.object)
        property_sources, property_sinked = expression(expr.property)
        sources.extend(object_sources)
        sources.extend(property_sources)
        sinked.extend(object_sinked)
        sinked.extend(property_sinked)

        if is_controlled(string):
            sources.append(string)
        return sources, sinked

    elif isinstance(expr, nodes.NewExpression):
        for arg in expr.arguments:
            so, si = expression(arg)
            sources.extend(so)
            sinked.extend(si)
        return sources, sinked

    elif isinstance(expr, nodes.UpdateExpression):
        return expression(expr.argument)

    elif isinstance(expr, nodes.AwaitExpression):
        return expression(expr.argument)

    elif isinstance(expr, nodes.UnaryExpression):
        return expression(expr.argument)

    elif isinstance(expr, nodes.BinaryExpression):
        left_sources, left_sinked = expression(expr.left)
        right_sources, right_sinked = expression(expr.right)
        return left_sources + right_sources, left_sinked + right_sinked

    elif isinstance(expr, nodes.ConditionalExpression):
        cso, csi = expression(expr.consequent)
        aso, asi = expression(expr.alternate)
        return cso+aso, csi+asi

    return sources, sinked

# returns sinked objs in the statement


def statements_and_declarations(node: Statement | Declaration) -> List[str]:

    if isinstance(node, nodes.VariableDeclaration):
        variable_declaration(node)

    elif isinstance(node, nodes.BlockStatement):
        return block_statement(node)

    elif isinstance(node, nodes.ExpressionStatement):
        _, sinked = expression(node.expression)
        return sinked

    elif isinstance(node, nodes.FunctionDeclaration):
        function_declaration(node)

    elif isinstance(node, nodes.DoWhileStatement):
        _, sinked = expression(node.test)
        sinked_body = statements_and_declarations(node.body)
        sinked.extend(sinked_body)
        return sinked

    elif isinstance(node, nodes.ExpressionStatement):
        _, sinked = expression(node.expression)
        return sinked

    elif isinstance(node, nodes.ForStatement):
        return statements_and_declarations(node.body)

    elif isinstance(node, nodes.ForInStatement):
        return statements_and_declarations(node.body)

    elif isinstance(node, nodes.ForOfStatement):
        return statements_and_declarations(node.body)

    elif isinstance(node, nodes.IfStatement):
        sinked = statements_and_declarations(node.consequent)
        if hasattr(node, "alternate"):
            sinked.extend(statements_and_declarations(node.alternate))
        return sinked

    elif isinstance(node, nodes.SwitchStatement):
        sinked = []
        for case in node.cases:
            for stmt in case.consequent:
                sinked.extend(statements_and_declarations(stmt))
        return sinked

    elif isinstance(node, nodes.TryStatement):
        sinked = block_statement(node.block)
        if node.handler != None:
            sinked.extend(block_statement(node.handler.body))
        if node.finalizer != None:
            sinked.extend(block_statement(node.finalizer))

    elif isinstance(node, nodes.WhileStatement):
        return statements_and_declarations(node.body)

    return []


def variable_declaration(node: nodes.nodes.VariableDeclaration):
    for var_declarator in node.declarations:
        sources, _ = expression(var_declarator.init)
        mark(gen(var_declarator.id), sources, gen(node))


def function_declaration(node: nodes.nodes.FunctionDeclaration):
    for param in node.params:
        mark(gen(param), None, "function_param")
    sinked = block_statement(node.body)
    mark_function_as_sink(node, sinked)

# returns sinked objs in the block


def block_statement(node: nodes.nodes.BlockStatement) -> List[str]:
    sinked: List[str] = []
    for stmt in node.body:
        sinked.extend(statements_and_declarations(stmt))
    return sinked


def walk(ast):
    for node in ast.body:
        statements_and_declarations(node)


sample2 = """
function search() {
    const query = document.getElementById('search').value
    window.location.href = window.location.href.split('?')[0] + "?q=" + query
}
document.getElementById('searchbtn').addEventListener('click', search)

const q = (new URLSearchParams(location.search)).get('q');
if (q) {
    document.getElementById("reflect").innerHTML = `Search results for ${q}`
}
"""

sample3 = """
function trackSearch(query) {
    document.write('<img src="/resources/images/tracker.gif?searchTerms=' + query + '">');
}
var query = (new URLSearchParams(window.location.search)).get('search');
if (query) {
    trackSearch(query);
}
"""
sample4 = """

var stores = ["London", "Paris", "Milan"];
var store = (new URLSearchParams(location.search)).get('storeId');
document.write('<select name="storeId">');
if (store) {
    document.write('<option selected>' + store + '</option>');
}
for (var i = 0; i < stores.length; i++) {
    if (stores[i] === store) {
        continue;
    }
    document.write('<option>' + stores[i] + '</option>');
}
document.write('</select>');
"""


ast = parse(sample4)
walk(ast)
