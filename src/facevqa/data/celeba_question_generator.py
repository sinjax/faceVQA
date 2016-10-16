import json

from pymantic import sparql
from rdflib import Graph


def _from_dict(target, d):
    for k, v in d.items():
        setattr(target, k, v)
    return target

class QuestionQuery(object):
    head = None
    query = []
    tail = None


def _bind(person, var):
    return "bind (%s as %s)"%(person,var)


class Question(object):

    query = None
    question = None
    answer = None
    vars = []
    name = None

    @staticmethod
    def read(question_json):
        q = _from_dict(Question(), question_json)
        q.query = _from_dict(QuestionQuery(), q.query)
        return q

    def query_person(self, person):
        head = self.query.head
        tail = self.query.tail
        lines = [_bind(person, "?person")] + self.query.query
        joined_lines = ".".join(lines)
        return "%(head)s { %(joined_lines)s } %(tail)s"%locals()

    def query_is_valid(self):
        return len(self.query.query) > 0

    def construct_question_answer(self, query_result):
        name_question_answer = []
        for binding in query_result["results"]["bindings"]:
            question = self.question
            answer = self.answer
            for k,v in binding.items():
                k = "?%s"%k
                question = question.replace(k,v["value"])
                answer = answer.replace(k,v["value"])
            name_question_answer += [
                {
                    "name": self.name,
                    "question": question,
                    "answer": answer
                }
            ]
        return name_question_answer




class BalzeGraphConnector(object):
    def __init__(self,host="192.168.0.3:9999", namespace="kb"):
        sparql_server = "http://%(host)s/blazegraph/namespace/%(namespace)s/sparql"%locals()
        self.server = sparql.SPARQLServer(sparql_server)
        super().__init__()

    def query(self, q):
        return self.server.query(q)

class RDFLibConnector(object):
    def __init__(self, graph):
        self.graph = Graph()
        self.graph.parse("/Users/ss/Data/celeba/list_attr_celeba.rdf.xml")

    def query(self, q):
        return self.graph.query(q)



class QuestionGenerator(object):
    def __init__(self, question_config, sparql_connector):
        self.questions = {}
        self.server = sparql_connector
        with open(question_config) as question_f:
            for question_json in json.load(question_f):
                q = Question.read(question_json)
                self.questions[q.name] = q

    def list_people(self):
        return self.server.query("select ?person {?person a <http://schema.org/Person>}")

    def generate_questions(self, *person):
        for person in person:
            ret = {
                "person": person,
                "question_answers" : []
            }
            for question_name, question in self.questions.items():
                if not question.query_is_valid(): continue
                query_person = question.query_person(person)
                query_result = self.server.query(query_person)
                ret["question_answers"] += [question.construct_question_answer(query_result)]
            yield ret


def _as_uri(param):
    return "<%(value)s>"%param


if __name__ == '__main__':
    connector = BalzeGraphConnector()
    gen = QuestionGenerator("templates/questions.json", connector)
    people = gen.list_people()
    one_person = _as_uri(people["results"]["bindings"][0]["person"])
    for person in people["results"]["bindings"][:100]:
        person_uri = _as_uri(person["person"])
        for person_question_answers in gen.generate_questions(person_uri):
            print("""%(person)s"""%person_question_answers)
            for question_answers in person_question_answers["question_answers"]:
                if len(question_answers) == 0: continue
                print("""   %(name)s"""%question_answers[0])
                for question_answer in question_answers:
                    print("""      %(question)s?   %(answer)s"""%question_answer)


