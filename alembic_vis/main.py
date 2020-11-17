import os
import re
import sys
import select
import time
from collections import namedtuple
from typing import List

from graphviz import Digraph


class AlembicHistoryAnalyzer:
    regexp = re.compile(r'(?P<from_node>.+) -> (?P<to_node>[\w\d]+)( |, )(\(.*\), )?(?P<comment>.*)')
    
    HistoryEntry = namedtuple('HistoryEntry', ('from_node', 'to_node', 'comment'))
    Node = namedtuple('Node', ('name', 'comment'))
    Edge = namedtuple('Edge', ('from_node', 'to_node'))

    @classmethod
    def make_nodes(cls, history: List[HistoryEntry]):
        nodes = set()
        for entry in history:
            for from_node in entry.from_node.split(','):
                node_name = from_node.strip()
                nodes.add(cls.Node(from_node.strip(), f'{node_name} ({entry.comment})'))
            node_name = entry.to_node.strip()
            nodes.add(cls.Node(entry.to_node.strip(), f'{node_name} ({entry.comment})'))
        
        return nodes

    @classmethod
    def make_edges(cls, history: List[HistoryEntry]):
        edges = []
        for entry in history:
            edges.extend(
                [cls.Edge(from_node.strip(), entry.to_node.strip()) for from_node in entry.from_node.split(',')])
        
        return edges

    @classmethod
    def show_graph(cls, alembic_history):
        history = []
        for match in cls.regexp.finditer(alembic_history):
            groups = match.groupdict()
            history.append(cls.HistoryEntry(groups['from_node'], groups['to_node'], groups['comment']))
        
        nodes = cls.make_nodes(history)
        edges = cls.make_edges(history)
        if not nodes:
            print('Nodes not found')
            return
        
        dot = Digraph(comment='Alembic migrations')
        for node in nodes:
            dot.node(node.name, node.comment)
        
        dot.edges([(edge.from_node, edge.to_node) for edge in edges])
        rendered_path = dot.render('migrations', view=True, cleanup=True, format='pdf')
        try:
            # TODO: improve this method
            time.sleep(2)
            os.remove(rendered_path)
        except OSError:
            print('Can not remove tmp file')


def run():
    i, o, e = select.select([sys.stdin], [], [], 1)
    if i:
        alembic_history = sys.stdin.read()
        AlembicHistoryAnalyzer.show_graph(alembic_history)
    else:
        print('No input')
        exit(1)


if __name__ == '__main__':
    run()
