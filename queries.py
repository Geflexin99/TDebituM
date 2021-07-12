from py2neo import Graph

SCHEME = "bolt"
HOST = "localhost"
USERNAME = 'neo4j'
PASSWORD = '112211'

graph = Graph(scheme=SCHEME, host=HOST, auth=(USERNAME, PASSWORD))
def getallMeasureSoll():
    query = "MATCH (n:MeasureSoll) RETURN n.name AS MeasureSoll"

    data_MeasureSoll = graph.run(query).data()

    MeasureSolls = [MS["MeasureSoll"] for MS in data_MeasureSoll]

    return MeasureSolls


def getallMeasureIst():
    query = "MATCH (n:MeasureIst) RETURN n.name AS MeasureIst"

    data_MeasureIst = graph.run(query).data()

    MeasureIsts = [MI["MeasureIst"] for MI in data_MeasureIst]

    return MeasureIsts

def getallCurrentstate():
    query = "MATCH (n:CurrentState) RETURN n.name AS CurrentState"

    data_CurrentState = graph.run(query).data()

    CurrentStates = [currentState["CurrentState"] for currentState in data_CurrentState]

    return CurrentStates

def getallCause():
    query = "MATCH (n:Cause) RETURN n.name AS Cause"

    data_Cause = graph.run(query).data()

    Causes = [cause["Cause"] for cause in data_Cause]

    return Causes

def getallTDIncident():
    query = "MATCH (n:TDIncident) RETURN n.name AS TDIncident"

    data_incident = graph.run(query).data() #REVIEW: chech other way of extracting directly dict() values
    TDIncidents = [incident["TDIncident"] for incident in data_incident]

    return TDIncidents

def getallTDType():
    query = "MATCH (n:TDType) RETURN n.name AS TDType"

    data_types = graph.run(query).data() #REVIEW: chech other way of extracting directly dict() values
    TDTypes = [type["TDType"] for type in data_types]

    return TDTypes
print(getallTDType())

def getallTDSubtype():
    query = "MATCH (n:TDSubtype) RETURN n.name AS TDSubtyp"

    data_tdSubtyp = graph.run(query).data()

    TDSubtypes = [party["TDSubtyp"] for party in data_tdSubtyp]

    return TDSubtypes

def getallParty():
    query = "MATCH (n:Party) RETURN n.name AS Party"

    data_parties = graph.run(query).data()

    Parties = [party["Party"] for party in data_parties]

    return Parties


def causes_initiated_by_party(party):
    if party=='All':
        query = """
                MATCH (p:Party)-[:INITIATES]->(c:Cause)
                RETURN p.name AS Party, c.name AS Cause
                """
    else:
        query = """
                MATCH (p:Party)-[:INITIATES]->(c:Cause)
                WHERE p.name=$party
                RETURN p.name AS Party, c.name AS Cause
                """
    result = graph.run(query, party=party)
    data = result.data()

    parties = []
    causes = []
    info = []
    
    index_input = []
    index_output = []

    dict_parties_causes = {"input": [], "output": [], "info": [], 
                            "index_input": [], "index_output": []}

    for data_pair in data:
        party = data_pair['Party']
        cause = data_pair['Cause']

        if party not in parties:
            parties.append(party)
            if len(index_input) != 0:
                index_input.append(index_input[-1]+1)
            else:
                index_input.append(0)
        else:
            index_input.append(index_input[-1])
        

        if cause not in causes:
            causes.append(cause)
            if len(index_output) != 0:
                index_output.append(max(index_output)+1)
            else:
                index_output.append(1)
        else:
            index = causes.index(cause)
            index_output.append(index)

        query="""
            MATCH (p:Party)-[:INITIATES]->(c:Cause)-->(td:TDSubtype)
            WHERE p.name=$party AND c.name=$cause
            RETURN td.name AS TD
        """
        info_pair_raw = graph.run(query, party=party,cause=cause).data()
        info_pair = list()
        
        for td in info_pair_raw:
            info_pair.append(td['TD'])
        info.append(info_pair)
        
    index_output = [index_input[-1] + index for index in index_output]

    return parties, causes, info, index_input, index_output
    # return dict_parties_causes




def affected_party_from_td(parties, relationship):

    td_types = getallTDType()

    td_groups = []
    for party in parties:
        for td_type in td_types:
            query = """
                    MATCH (tdt:TDType)--(tds:TDSubtype)--(c:Cause)--(tdi:TDIncident)-[rel]-(p:Party)
                    WHERE tdt.name=$td_type AND p.name = $party AND type(rel)=$relationship
                    RETURN tds.name AS TDSubtype, tdi.name AS TDIncident, c.name AS Cause
                    """
            result = graph.run(query, relationship=relationship, td_type=td_type, party=party)
            data = result.data()
            info = "Causes of TD: <br>"
            amount_td_type = len(data)*10
            for e in data:
                info = info + "  - " + str(e["Cause"]) + ", <br>"
            info = info[:-6]
            td_groups.append([party, td_type, amount_td_type, info])

    #TODO: make a dictionary out of it
    output_td_types, output_parties, output_amount, output_info, output_color = [], [], [], [], []

    for group in td_groups:
        output_parties.append(group[0])
        output_td_types.append(group[1])
        output_amount.append(group[2])
        output_info.append(group[3])

        if relationship=="INITIATES":
            output_color.append('rgb(93, 164, 214)')
        else:
            output_color.append('rgb(255, 144, 14)')
        
    return output_parties, output_td_types, output_amount, output_info, output_color

def sunburst():
    query = "MATCH (n:TDType) RETURN n.name AS TDType"


    # REVIEW: chech other way of extracting directly dict() values
    types = graph.run(query).data()
    td_types = [type["TDType"] for type in types]
    print(td_types)

    query = """
            MATCH(tdt: TDType)--(tds: TDSubtype)--(c: Cause)--(tdi: TDIncident)
            RETURN tdt.name AS TD, tds.name AS TDS, c.name, tdi.name
            """

    data = graph.run(query).data()

    td_types = dict()

    for pair in data:
        td = pair['TD']
        td_subtype = pair['TDS']

        if td not in td_types.keys():
            td_types[td] = {td_subtype: 1}

        else:
            if td_subtype in td_types[td]:
                td_types[td][td_subtype] += 1
            else:
                td_types[td][td_subtype] = 1

    labels = []
    parents = []
    values = []

    for td_type in td_types.keys():
        labels += [td_type] + [td for td in td_types[td_type]]
        parents += [""] + [td_type]*len(td_types[td_type])
        values_subtypes = [td_value for td_value in td_types[td_type].values()]
        values += [0] + values_subtypes

    return labels, parents, values

def dropdown_options(parties):
    options = []
    for party in parties:
        options.append(dict(label=party, value=party))

    options.append(dict(label="All", value="All"))
    return options