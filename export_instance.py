import json

scenario = "instances/sample_scenario.json"

def from_node_id(route_path, route_section, index_in_path):
    if "route_alternative_marker_at_entry" in route_section.keys() and \
                    route_section["route_alternative_marker_at_entry"] is not None and \
                    len(route_section["route_alternative_marker_at_entry"]) > 0:
        return "" + str(route_section["route_alternative_marker_at_entry"][0]) + ""
    else:
        if index_in_path == 0:  # can only get here if this node is a very beginning of a route
            return "" + str(route_section["sequence_number"]) + "_beginning"
        else:
            return "" + (str(route_path["route_sections"][index_in_path - 1]["sequence_number"]) + "->" +
                          str(route_section["sequence_number"])) + ""

def to_node_id(route_path, route_section, index_in_path):
    if "route_alternative_marker_at_exit" in route_section.keys() and \
                    route_section["route_alternative_marker_at_exit"] is not None and \
                    len(route_section["route_alternative_marker_at_exit"]) > 0:

        return "" + str(route_section["route_alternative_marker_at_exit"][0]) + ""
    else:
        if index_in_path == (len(route_path["route_sections"]) - 1): # meaning this node is a very end of a route
            return "" + str(route_section["sequence_number"]) + "_end" + ""
        else:
            return "" + (str(route_section["sequence_number"]) + "->" +
                          str(route_path["route_sections"][index_in_path + 1]["sequence_number"])) + ""

def id_to_color(id):
    return '#'+"{0:06x}".format(abs(hash(str(id*10000))))[:6]

with open(scenario) as fp:
    scenario = json.load(fp)

nodes = []
edges = []

for route in scenario["routes"]:
    for path in route["route_paths"]:
        for (i, route_section) in enumerate(path["route_sections"]):
            section_markers = route_section['section_marker'] if 'section_marker' in route_section else {}

            """
            for section_marker in section_markers:
                nodes.append({'id': section_marker+'_sm', 'color': 'red', 'shape': 'box', 'label': section_marker})
                edges.append({'from': section_marker+'_sm', 'to': str(route["id"]) + to_node_id(path, route_section, i), 'dashes': 'true'})
            """

            for resource_occupations in route_section['resource_occupations']:
                resource = resource_occupations['resource']
                nodes.append({'id': resource+'_ro', 'color': 'blue', 'shape': 'circle', 'label': resource})
                edges.append({'from': resource+'_ro', 'to': str(route["id"])+to_node_id(path, route_section, i), 'dashes': 'true'})


            edges.append({'label': str(route_section['sequence_number']), 'from': str(route["id"])+from_node_id(path, route_section, i), 'to': str(route["id"])+to_node_id(path, route_section, i), 'arrows': {'to': {'enabled': True, 'scaleFactor': 3}}, 'width': 5})
            nodes.append({'id': str(route["id"])+from_node_id(path, route_section, i), 'label': from_node_id(path, route_section, i), 'color': id_to_color(route["id"]), 'shape': 'ellipsis'})
            nodes.append({'id': str(route["id"])+to_node_id(path, route_section, i), 'label': to_node_id(path, route_section, i), 'color': id_to_color(route["id"]), 'shape': 'ellipsis'})



# removes duplicate nodes
nodes = list({v['id']: v for v in nodes}.values())

network = {'nodes': nodes, 'edges': edges}
print(json.dumps(network, indent=4, separators=(',', ': ')))