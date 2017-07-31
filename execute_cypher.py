from neo4j.v1 import GraphDatabase
import json
#driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "19960407"))


def add_friends(tx, name, friend_name):
    tx.run("MERGE (a:Person {name: $name}) "
           "MERGE (a)-[:KNOWS]->(friend:Person {name: $friend_name})",
           name=name, friend_name=friend_name)


def print_friends(tx, name):
    for record in tx.run("MATCH (a:Person)-[:works_in]->() WHERE a.name = $name "
                         "RETURN friend.name ORDER BY friend.name", name=name):
        print(record["friend.name"])


def per_employee_member_of(tx, person, company):
    tx.run("MERGE (c:Company{name:$company})"
           "MERGE (p:Person{name:$person})"
           "MERGE (p)-[:work_in]-(c)",
           company=company, person=person)


def founded_by(tx, company, person):
    tx.run("MERGE (c:Company{name:$company})"
           "MERGE (p:Person{name:$person})"
           "MERGE (c)-[:founded_by]-(p)",
           company=company, person=person)


def acquired_by(tx, com1, com2):
    tx.run("MERGE (c1:Company{name:$c1})"
           "MERGE (c2:Company{name:$c2})"
           "MERGE (c1)-[:acquired_by]-(c2)",
           c1=com1, c2=com2)


def collaborate_with(tx, com1, com2):
    tx.run("MERGE (c1:Company{name:$c1})"
           "MERGE (c2:Company{name:$c2})"
           "MERGE (c1)-[:collaborate_with]-(c2)",
           c1=com1, c2=com2)


def provide_to(tx, com1, com2):
    tx.run("MERGE (c1:Company{name:$c1})"
           "MERGE (c2:Company{name:$c2})"
           "MERGE (c1)-[:provide_to]-(c2)",
           c1=com1, c2=com2)


def parent_of(tx, p1, p2):
    tx.run("MERGE (p1:Person{name:$p1})"
           "MERGE (p2:Person{name:$p2})"
           "MERGE (p1)-[:parent_of]-(p2)",
           p1=p1, p2=p2)


def sibling_of(tx, p1, p2):
    tx.run("MERGE (p1:Person{name:$p1})"
           "MERGE (p2:Person{name:$p2})"
           "MERGE (p1)-[:sibling_of]-(p2)",
           p1=p1, p2=p2)


def spouse_of(tx, p1, p2):
    tx.run("MERGE (p1:Person{name:$p1})"
           "MERGE (p2:Person{name:$p2})"
           "MERGE (p1)-[:spouse_of]-(p2)",
           p1=p1, p2=p2)


def other_family_of(tx, p1, p2):
    tx.run("MERGE (p1:Person{name:$p1})"
           "MERGE (p2:Person{name:$p2})"
           "MERGE (p1)-[:other_family_of]-(p2)",
           p1=p1, p2=p2)


def edu_at(tx, person, school):
    tx.run("MERGE (p:Person{name:$person})"
           "MERGE (s:School{name:$school})"
           "MERGE (p)-[:edu_at]-(s)",
           person=person, school=school)


def run_on_file(driver,path):
    print "Building relationships into graph...Pleas make sure your Neo4j is open"
    print path
    with driver.session() as session:
        with open(path,'r+') as json_file:
            json_data = json.load(json_file)
            relationships = json_data['relationships']
            count = 0
            for relation in relationships:
                count = count + 1
                print relation['predicateId']
                if (relation['predicateId'] == "PER-EMPLOYEE-MEMBER-OF"):
                    session.write_transaction(per_employee_member_of, relation["arg1"], relation["arg2"])
                elif (relation['predicateId'] == "ORG-FOUNDED"):
                    session.write_transaction(founded_by, relation["arg1"], relation["arg2"])
                elif (relation['predicateId'] == "ORG-COLLABORATORS"):
                    session.write_transaction(collaborate_with, relation["arg1"], relation["arg2"])
                elif (relation['predicateId'] == "ORG-ACQUIRED-BY"):
                    session.write_transaction(acquired_by, relation["arg1"], relation["arg2"])
                elif (relation['predicateId'] == "ORG-PROVIDER-TO"):
                    session.write_transaction(provide_to, relation["arg1"], relation["arg2"])
                elif (relation['predicateId'] == "PER-PARENTS"):
                    session.write_transaction(parent_of, relation["arg1"], relation["arg2"])
                elif (relation['predicateId'] == "PER-SIBLINGS"):
                    session.write_transaction(sibling_of, relation["arg1"], relation["arg2"])
                elif (relation['predicateId'] == "PER-SPOUSE"):
                    session.write_transaction(spouse_of, relation["arg1"], relation["arg2"])
                elif (relation['predicateId'] == "PER-OTHER-FAMILY"):
                    session.write_transaction(other_family_of, relation["arg1"], relation["arg2"])
                elif (relation['predicateId'] == "EDU_AT(e1,e2)"):
                    session.write_transaction(edu_at, relation["arg1"], relation["arg2"])
                else:
                    continue

#run_on_file(driver,r"C:\Users\dengy1\EDO-Intern-Project\Yuxi\sec-crawler\SEC-relations\F_17_relations.json")
