import xmltodict
import json


def get_xml_data(xml_file_path):
    file = open(xml_file_path)
    xml_att = xmltodict.parse(file.read())
    print(xml_file_path)

    # with open("d.json", 'w') as d:
    #     d.write(json.dumps(xml_att))
    body_control = []
    tire_pressure = []
    readiness = []

    for data in xml_att['VDoc']['VDocSection']['DataItems']:
        if data['@attributeName'] == "ActionSelection":
            vehicle_info = data['Item']
            vehicle_info.append({'@name': 'VIN', '@value': xml_att['VDoc']['@VehicleIdentificationNumber']})
            vehicle_info.append({'@name': 'ODOMETER', '@value': xml_att['VDoc']['@Odometer']})
            vehicle_info.append({'@name': 'LICENSE PLATE', '@value': xml_att['VDoc']['@LicensePlateNumber']})
            vehicle_info.append({'@name': 'DateCreated', '@value': xml_att['VDoc']['@DateCreated']})
            # print(vehicle_info)
        if "CodeScanSystems" in data:
            # print(data)
            CodeScanSystems = data['CodeScanSystems']
            # print(CodeScanSystems)
            for system in CodeScanSystems['System']:
                if system['@name'] == 'Body Control Module':
                    try:
                        body_control = system['Item']
                        if isinstance(body_control, dict):
                            body_control = [system['Item']]
                    except Exception as e:
                        body_control = []

                    # print(body_control)
                if system['@name'] == 'Tire Pressure Monitor':
                    try:
                        tire_pressure = system['Item']
                        if isinstance(tire_pressure, dict):
                            tire_pressure = [system['Item']]
                    except Exception as e:
                        tire_pressure = []
                    # print(tire_pressure)

        # readiness
        if "ReadinessMonitorsTestsComplete" in data:
            # print(data['ReadinessMonitorsTestsComplete'])
            readiness = data['ReadinessMonitorsTestsComplete']['Item']
            if isinstance(readiness, dict):
                readiness = [data['ReadinessMonitorsTestsComplete']]
        if "CodeScanType" in data:
            code_scan_type = data['CodeScanType']['@value']

    top_information = {}
    for vehicle in vehicle_info:
        if vehicle["@name"] == 'YEAR':
            top_information['year'] = vehicle
        if vehicle["@name"] == 'MAKE':
            top_information['make'] = vehicle
        if vehicle["@name"] == 'MODEL':
            top_information['model'] = vehicle
        if vehicle["@name"] == 'ENGINE':
            top_information['engine'] = vehicle

    file.close()
    return vehicle_info, CodeScanSystems, body_control, tire_pressure, readiness, code_scan_type, top_information
