from os import mkdir
from subprocess import Popen

def create_outdir(prefix):
	try:
		mkdir(prefix)
	except OSError:
		pass

def create_echidna_process(prefix, path):
	call = ["echidna"]
	call.extend([path])
	call.extend(["--config", "config/echidna.yaml", "--workers", "6"])
	outjson = open(prefix + "/result.json", "w")
	outerr = open(prefix + "/out.err", "w")
	return (
		Popen(call, stdout=outjson, stderr=outerr),
		outjson,
		outerr,
	)
