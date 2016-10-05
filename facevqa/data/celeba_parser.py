from rdflib import Graph, URIRef, RDF, Namespace, BNode
from rdflib.parser import Parser
from rdflib.plugin import register

from .celeba_fields import *

register("celeba", Parser, "facevqa.data.celeba_parser", "CelebAParser")


celeba_ns = Namespace("http://mmlab.ie.cuhk.edu.hk/projects/")
schema_ns = Namespace("http://schema.org/")



def _create_gender(annotations):
    return schema_ns["Male"] if annotations[Male] else schema_ns["Female"]

def is_x(annotations, x):
    return schema_ns["True"] if annotations[x] else schema_ns["False"]


def _create_head(annotations): return BNode()
def _create_eyes(annotations): return BNode()
def _create_eyebrows(annotations): return BNode()
def _create_face_skin(annotations): return BNode()
def _create_face_hair(annotations): return BNode()
def _create_nose(annotations): return BNode()
def _create_mouth(annotations): return BNode()
def _create_neck(annotations): return BNode()
def _create_ear(annotations): return BNode()


class CelebAParser(Parser):

    def parse(self, source, sink):
        """
        Pass in a file or file-like object containing CelebA attributes
        """
        sink.bind("schema", schema_ns)
        sink.bind("celeba", celeba_ns)
        lines = source.getByteStream()
        count = int(lines.readline())
        headings = lines.readline().strip().split(" ")
        lines = [x for x in lines][:10]
        for x in lines:
            parts = [x for x in filter(None, x.strip().split(" "))]
            jpeg = parts[0]
            raw_anns = parts[1:]
            annotations = dict([
               (headings[i],int(raw_anns[i]) == 1) for i in range(len(headings))
            ])
            self._add_person(sink, jpeg, annotations)

        print(len([x for x in lines]) == count)

    def _add_person(self, sink, jpeg, annotations):
        person = URIRef(celeba_ns[jpeg])
        sink.add((person, RDF.type, URIRef(schema_ns["Person"])))
        sink.add((person, schema_ns["gender"], _create_gender(annotations)))
        sink.add((person, schema_ns["isAttractive"], is_x(annotations, Attractive)))
        sink.add((person, schema_ns["isChubby"], is_x(annotations, Chubby)))
        sink.add((person, schema_ns["hasHead"], _create_head(annotations)))
        sink.add((person, schema_ns["hasEyes"], _create_eyes(annotations)))
        sink.add((person, schema_ns["hasEyebrows"], _create_eyebrows(annotations)))
        sink.add((person, schema_ns["hasFaceSkin"], _create_face_skin(annotations)))
        sink.add((person, schema_ns["hasFaceHair"], _create_face_hair(annotations)))
        sink.add((person, schema_ns["hasNose"], _create_nose(annotations)))
        sink.add((person, schema_ns["hasMouth"], _create_mouth(annotations)))
        sink.add((person, schema_ns["hasNeck"], _create_neck(annotations)))
        sink.add((person, schema_ns["hasEar"], _create_ear(annotations)))




if __name__ == '__main__':
    g = Graph()
    text_io_wrapper = open("/Users/ss/Data/celeba/list_attr_celeba.txt", "r")
    g.parse(text_io_wrapper, format="celeba")
    print(str(g.serialize(),"utf-8"))

