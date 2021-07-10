from py2neo import Graph

#TODO: create a new database that is empty. This notebook will override the database

SCHEME = "bolt"
HOST = "localhost"
USERNAME = 'neo4j'
PASSWORD = '112211'                     

graph = Graph(scheme=SCHEME, host=HOST, auth=(USERNAME, PASSWORD))

graph.run("""
CREATE p = (andy:Person {name:'Andy'})
-[:REPORTED]->
(incident1:TDIncident {name:"Produkt führt zu Datenlöschung - Entwicklungsaufwand der Tests"})
-[:INDICATES]->
(Tnm:TDSubtype {name:"Tests are not maintained"})
<-[:REQUIRES]-
(tcm: Measure {name:"Test case maintenance"})
-[:SOLVES]->
(fpmi:Cause {name:"Functionality of product more important"})
-[:CAUSES]->(Tnm)-[:BELONGS_TO]->(mtd:TDType {name:"Maintenance TD"})
RETURN p

""")