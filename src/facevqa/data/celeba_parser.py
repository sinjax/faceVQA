from rdflib import Graph, URIRef, RDF, Namespace, BNode, RDFS, XSD, Literal
from rdflib.parser import Parser
from rdflib.plugin import register

from facevqa.data.celeba_fields import *

register("celeba", Parser, "facevqa.data.celeba_parser", "CelebAParser")


celeba_ns = Namespace("http://mmlab.ie.cuhk.edu.hk/projects/")
schema_ns = Namespace("http://schema.org/")



def _create_gender(annotations):
    return schema_ns["Male"] if annotations[Male] else schema_ns["Female"]

def is_x(annotations, x):
    return schema_ns["True"] if annotations[x] else schema_ns["False"]


def _hair_colour(annotations):
    if annotations[Black_Hair]: return string_literal("Black")
    if annotations[Gray_Hair]: return string_literal("Gray")
    if annotations[Blond_Hair]: return string_literal("Blond")
    if annotations[Brown_Hair]: return string_literal("Brown")
    return None


def _hair_style(annotations):
    if annotations[Receding_Hairline]: return string_literal("receding hairline")
    if annotations[Bald]: return string_literal("bald")
    if annotations[Bangs]: return string_literal("bangs")
    return None


def _hair_shape(annotations):
    if annotations[Straight_Hair]: return string_literal("Straight_Hair")
    if annotations[Wavy_Hair]: return string_literal("Wavy_Hair")


def _create_head(annotations, sink):
    head = BNode()
    sink.add((head, RDF.type, schema_ns.Head))
    colour = _hair_colour(annotations)
    style = _hair_style(annotations)
    shape = _hair_shape(annotations)
    if colour: sink.add((head, schema_ns.hairColour, colour))
    if style: sink.add((head, schema_ns.hairStyle, style))
    if shape: sink.add((head, schema_ns.hairShape, shape))
    return head

def _add_wearing(person, annotations, sink):
    if annotations[Wearing_Earrings]: sink.add((person, schema_ns.wearing, string_literal("earrings")))
    if annotations[Wearing_Hat]: sink.add((person, schema_ns.wearing, string_literal("hat")))
    if annotations[Wearing_Lipstick]: sink.add((person, schema_ns.wearing, string_literal("lipstick")))
    if annotations[Wearing_Necklace]: sink.add((person, schema_ns.wearing, string_literal("necklace")))
    if annotations[Wearing_Necktie]: sink.add((person, schema_ns.wearing, string_literal("necktie")))

def _create_eyes(annotations, sink):
    eyes = BNode()
    sink.add((eyes, RDF.type, schema_ns.Eyes))
    sink.add((eyes,schema_ns.isWearingGlasses,is_x(annotations,Eyeglasses)))
    sink.add((eyes,schema_ns.areThin,is_x(annotations,Narrow_Eyes)))
    sink.add((eyes,schema_ns.haveBags,is_x(annotations,Bags_Under_Eyes)))
    return eyes

def _create_eyebrows(annotations, sink):
    eyebrows = BNode()
    sink.add((eyebrows, RDF.type, schema_ns.Eyebrows))
    sink.add((eyebrows, schema_ns.hairy, is_x(annotations,Bushy_Eyebrows)))
    sink.add((eyebrows, schema_ns.arched, is_x(annotations,Arched_Eyebrows)))
    return eyebrows


def _create_cheeks(annotations, sink):
    cheeks = BNode()
    sink.add((cheeks, RDF.type, schema_ns.Cheeks))
    sink.add((cheeks, schema_ns.highCheekBones, is_x(annotations, High_Cheekbones)))
    sink.add((cheeks, schema_ns.roseCheeks, is_x(annotations, Rosy_Cheeks)))
    return cheeks


def _create_face(annotations, sink):
    face = BNode()
    sink.add((face, RDF.type, schema_ns.Face))
    if annotations[Oval_Face]: sink.add((face, schema_ns.faceShape, string_literal("oval")))
    sink.add((face, schema_ns.complextion, is_x(annotations,Pale_Skin)))
    sink.add((face, schema_ns.doubleChin, is_x(annotations, Double_Chin)))
    sink.add((face, schema_ns.cheeks, _create_cheeks(annotations, sink)))
    return face


def string_literal(s):
    return Literal(s, datatype=XSD.string)


def _create_face_hair(annotations, sink):
    facialHair = BNode()
    sink.add((facialHair, RDF.type, schema_ns.FacialHair))
    if annotations[Five_o_Clock_Shadow]: sink.add((facialHair, schema_ns.facialHairStyle, string_literal("stubble")))
    if annotations[Goatee]: sink.add((facialHair, schema_ns.facialHairStyle,string_literal("goatee")))
    if annotations[Sideburns]: sink.add((facialHair, schema_ns.facialHairStyle,string_literal("sideburns")))
    if annotations[No_Beard]: sink.add((facialHair, schema_ns.facialHairStyle,string_literal("clean shaven")))
    if annotations[Mustache]: sink.add((facialHair, schema_ns.facialHairStyle,string_literal("mustache")))

    return facialHair

def _create_nose(annotations, sink):
    nose = BNode()
    sink.add((nose, RDF.type, schema_ns.Nose))
    if annotations[Pointy_Nose]: sink.add((nose, schema_ns.noseShape, string_literal("pointy")))
    if annotations[Big_Nose]: sink.add((nose, schema_ns.noseStyle, string_literal("big")))
    return nose
def _create_mouth(annotations, sink):
    mouth = BNode()
    sink.add((mouth, RDF.type, schema_ns.Mouth))
    if annotations[Mouth_Slightly_Open]: sink.add((mouth, schema_ns.mouthConfiguration, string_literal("slightly open")))
    if annotations[Smiling]: sink.add((mouth, schema_ns.mouthConfiguration, string_literal("smiling")))
    if annotations[Big_Lips]: sink.add((mouth, schema_ns.mouthShape, string_literal("big lips")))
    return mouth


def _prepare_ontology(sink):


    # Male

    # Wearing_Earrings Wearing_Hat Wearing_Lipstick Wearing_Necklace Wearing_Necktie
    sink.add((schema_ns.wearing, RDFS.domain, schema_ns.Person))
    sink.add((schema_ns.wearing, RDFS.range, XSD.string))

    # Heavy_Makeup
    sink.add((schema_ns.heavyMakeup, RDFS.domain, schema_ns.Person))
    sink.add((schema_ns.heavyMakeup, RDFS.range, schema_ns.Boolean))

    # Blurry
    sink.add((schema_ns.blurry, RDFS.domain, schema_ns.Person))
    sink.add((schema_ns.blurry, RDFS.range, schema_ns.Boolean))

    # Attractive
    sink.add((schema_ns.attractive, RDFS.domain, schema_ns.Person))
    sink.add((schema_ns.attractive, RDFS.range, schema_ns.Boolean))

    # Chubby
    sink.add((schema_ns.chubby, RDFS.domain, schema_ns.Person))
    sink.add((schema_ns.chubby, RDFS.range, schema_ns.Boolean))

    # Young
    sink.add((schema_ns.age, RDFS.domain, schema_ns.Person))
    sink.add((schema_ns.age, RDFS.range, XSD.string))

    sink.add((schema_ns.hasHead,RDFS.domain,schema_ns.Person))
    sink.add((schema_ns.hasHead,RDFS.range,schema_ns.Head))

    sink.add((schema_ns.hasEyes,RDFS.domain,schema_ns.Person))
    sink.add((schema_ns.hasEyes,RDFS.range,schema_ns.Eyes))

    sink.add((schema_ns.hasEyebrows,RDFS.domain,schema_ns.Person))
    sink.add((schema_ns.hasEyebrows,RDFS.range,schema_ns.Eyebrows))

    sink.add((schema_ns.hasFace,RDFS.domain,schema_ns.Person))
    sink.add((schema_ns.hasFace,RDFS.range,schema_ns.Face))

    sink.add((schema_ns.hasFacialHair,RDFS.domain,schema_ns.Person))
    sink.add((schema_ns.hasFacialHair,RDFS.range,schema_ns.FacialHair))

    sink.add((schema_ns.hasNose,RDFS.domain,schema_ns.Person))
    sink.add((schema_ns.hasNose,RDFS.range,schema_ns.Nose))

    sink.add((schema_ns.hasMouth,RDFS.domain,schema_ns.Person))
    sink.add((schema_ns.hasMouth,RDFS.range,schema_ns.Mouth))

    # Black_Hair Blond_Hair Brown_Hair Gray_Hair
    sink.add((schema_ns.hairColor, RDFS.subPropertyOf, schema_ns.color))
    sink.add((schema_ns.hairColor, RDFS.domain, schema_ns.Head))
    sink.add((schema_ns.hairColor, RDFS.range, XSD.string))

    # Receding_Hairline Bald Bangs
    sink.add((schema_ns.hairStyle, RDFS.subPropertyOf, schema_ns.style))
    sink.add((schema_ns.hairStyle, RDFS.domain, schema_ns.Head))
    sink.add((schema_ns.hairStyle, RDFS.range, XSD.string))

    # Straight_Hair Wavy_Hair
    sink.add((schema_ns.hairShape, RDFS.subPropertyOf, schema_ns.shape))
    sink.add((schema_ns.hairShape, RDFS.domain, schema_ns.Head))
    sink.add((schema_ns.hairShape, RDFS.range, XSD.string))

    # Eyeglasses
    sink.add((schema_ns.isWearingGlasses, RDFS.domain, schema_ns.Eyes))
    sink.add((schema_ns.isWearingGlasses, RDFS.range, schema_ns.Boolean))

    # Narrow_Eyes
    sink.add((schema_ns.areThin, RDFS.domain, schema_ns.Eyes))
    sink.add((schema_ns.areThin, RDFS.range, schema_ns.Boolean))

    # Bags_Under_Eyes
    sink.add((schema_ns.haveBags, RDFS.domain, schema_ns.Eyes))
    sink.add((schema_ns.haveBags, RDFS.range, schema_ns.Boolean))

    # Bushy_Eyebrows
    sink.add((schema_ns.hairy, RDFS.domain, schema_ns.Eyebrows))
    sink.add((schema_ns.hairy, RDFS.range, schema_ns.Boolean))

    # Arched_Eyebrows
    sink.add((schema_ns.arched, RDFS.domain, schema_ns.Eyebrows))
    sink.add((schema_ns.arched, RDFS.range, schema_ns.Boolean))

    # Pale_Skin
    sink.add((schema_ns.complextion, RDFS.domain, schema_ns.Face))
    sink.add((schema_ns.complextion, RDFS.range, schema_ns.Boolean))

    # Oval_Face
    sink.add((schema_ns.faceShape, RDFS.subPropertyOf, schema_ns.shape))
    sink.add((schema_ns.faceShape, RDFS.domain, schema_ns.Face))
    sink.add((schema_ns.faceShape, RDFS.range, XSD.string))


    sink.add((schema_ns.cheeks, RDFS.domain, schema_ns.Face))
    sink.add((schema_ns.cheeks, RDFS.range, schema_ns.Cheeks))

    # Double_Chin
    sink.add((schema_ns.doubleChin, RDFS.domain, schema_ns.Face))
    sink.add((schema_ns.doubleChin, RDFS.range, schema_ns.Boolean))

    # High_Cheekbones
    sink.add((schema_ns.highCheekBones, RDFS.domain, schema_ns.Cheeks))
    sink.add((schema_ns.highCheekBones, RDFS.range, schema_ns.Boolean))

    # Rosy_Cheeks
    sink.add((schema_ns.roseyCheeks, RDFS.domain, schema_ns.Cheeks))
    sink.add((schema_ns.roseyCheeks, RDFS.range, schema_ns.Boolean))

    # 5_o_Clock_Shadow Goatee Sideburns No_Beard Mustache
    sink.add((schema_ns.facialHairStyle, RDFS.domain, schema_ns.FacialHair))
    sink.add((schema_ns.facialHairStyle, RDFS.range, XSD.string))
    sink.add((schema_ns.facialHairStyle, RDFS.subPropertyOf, schema_ns.style))

    # Pointy_Nose
    sink.add((schema_ns.noseShape, RDFS.domain, schema_ns.Nose))
    sink.add((schema_ns.noseShape, RDFS.range, XSD.string))
    sink.add((schema_ns.noseShape, RDFS.subPropertyOf, schema_ns.style))

    # Big_Nose
    sink.add((schema_ns.noseStyle, RDFS.domain, schema_ns.Nose))
    sink.add((schema_ns.noseStyle, RDFS.range, XSD.string))
    sink.add((schema_ns.noseStyle, RDFS.subPropertyOf, schema_ns.style))

    # Mouth_Slightly_Open Smiling
    sink.add((schema_ns.mouthConfiguration, RDFS.domain, schema_ns.Mouth))
    sink.add((schema_ns.mouthConfiguration, RDFS.range, XSD.string))
    sink.add((schema_ns.mouthConfiguration, RDFS.subPropertyOf, schema_ns.style))

    # Big_Lips
    sink.add((schema_ns.mouthShape, RDFS.domain, schema_ns.Mouth))
    sink.add((schema_ns.mouthShape, RDFS.range, XSD.string))
    sink.add((schema_ns.mouthShape, RDFS.subPropertyOf, schema_ns.style))

class CelebAParser(Parser):

    def parse(self, source, sink):
        """
        Pass in a file or file-like object containing CelebA attributes
        """
        sink.bind("schema", schema_ns)
        sink.bind("celeba", celeba_ns)
        sink.bind("rdfs", RDFS)

        _prepare_ontology(sink)
        lines = source.getByteStream()
        count = int(lines.readline())
        headings = lines.readline().strip().split(" ")
        lines = [x for x in lines][:1000]
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
        sink.add((person, schema_ns.gender, _create_gender(annotations)))
        sink.add((person, schema_ns.attractive, is_x(annotations, Attractive)))
        sink.add((person, schema_ns.blurry, is_x(annotations, Blurry)))
        sink.add((person, schema_ns.chubby, is_x(annotations, Chubby)))
        sink.add((person, schema_ns.heavyMakeup, is_x(annotations, Heavy_Makeup)))
        _add_wearing(person,annotations,sink)
        sink.add((person, schema_ns.hasHead, _create_head(annotations,sink)))
        sink.add((person, schema_ns.hasEyes, _create_eyes(annotations,sink)))
        sink.add((person, schema_ns.hasEyebrows, _create_eyebrows(annotations,sink)))
        sink.add((person, schema_ns.hasFace, _create_face(annotations,sink)))
        sink.add((person, schema_ns.hasFacialHair, _create_face_hair(annotations,sink)))
        sink.add((person, schema_ns.hasNose, _create_nose(annotations,sink)))
        sink.add((person, schema_ns.hasMouth, _create_mouth(annotations,sink)))




if __name__ == '__main__':
    g = Graph()
    text_io_wrapper = open("/Users/ss/Data/celeba/list_attr_celeba.txt", "r")
    g.parse(text_io_wrapper, format="celeba")
    print(str(g.serialize(),"utf-8"))

    res = g.query("""
        select ?x WHERE {
            ?x rdfs:range schema:Head
        }
    """)

