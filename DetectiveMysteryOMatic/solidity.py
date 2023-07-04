from string import Template
from datetime import timedelta
from solidity_parser import parser

class SolidityTemplate(Template):
	delimiter = '//$'

def read_sol_template(filename):
	with open(filename, 'r') as f:
		template = SolidityTemplate(f.read())
		return template

def save_solidity(prefix, source):
	filename = prefix + "/model.sol"
	with open(filename, 'w') as f:
		f.write(source)

	return filename

def read_solidity(filename):
	# read solidity source code
	source_unit = parser.parse_file(filename, loc=False)
	return parser.objectify(source_unit)

def get_enum(source, contract_name, typ):
	enums_map = source.contracts[contract_name].enums
	enum_map = enums_map[typ.capitalize()]["members"]
	return list(map(lambda x: "$" + x.name, enum_map))

def decode_enum(enums_map, typ, index):
	typ = ''.join(i for i in typ if not i.isdigit())
	enum_map = enums_map[typ.capitalize()]["members"]
	return "$" + enum_map[index]["name"]

def get_event(source, contract_name, event):
	abi = source.contracts[contract_name].events
	enums_map = source.contracts[contract_name].enums
	event = event.split(" from:")[0]
	event_name, args = event.split("(")
	args = args.split(")")[0]
	event_name.strip()
	event_call = [event_name]
	for (argument, typ) in zip(args.split(","), abi[event_name].arguments):
		argument = argument.strip()
		typ = ''.join(i for i in typ if not i.isdigit())
		if (argument == "true" or argument == "false"):
			event_call.append(argument == "true")
			continue

		index = int(argument)
		if typ == "time":
			clock = timedelta(seconds = 9 * 3600 + index)
			h, m, s = str(clock).split(":")
			event_call.append(h + ":" + m)
		else:
			# TODO: make sure this is properly adjusted for every type
			index = index % 4
			event_call.append(decode_enum(enums_map, typ, index))

	return event_call

def get_tx(source, contract_name, tx):
	abi = source.contracts[contract_name].functions
	enums_map = source.contracts[contract_name].enums

	function_name = tx["function"]
	function_call = [function_name]
	for (argument, typ) in zip(tx["arguments"], abi[function_name].arguments):
		index = int(argument)
		index = index % 4
		function_call.append(decode_enum(enums_map, typ, index))

	return function_call

