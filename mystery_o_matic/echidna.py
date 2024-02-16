from os import mkdir
from subprocess import Popen


def create_outdir(prefix):
    """
    Create an output directory with the given prefix.

    Args:
        prefix (str): The prefix for the output directory.

    Returns:
        None
    """
    try:
        mkdir(prefix)
    except OSError:
        pass


def create_echidna_process(prefix, path, seed, workers):
    """
    Creates and starts an Echidna process.

    Args:
        prefix (str): The prefix for the output files.
        path (str): The path to the Echidna executable.
        seed (int): The seed value for random number generation (optional).
        workers (int): The number of worker processes to use.

    Returns:
        tuple: A tuple containing the following:
            - subprocess.Popen: The Echidna process.
            - file object: The output JSON file.
            - file object: The error output file.
    """
    call = ["echidna"]
    call.extend([path])
    call.extend(["--config", "config/echidna.yaml", "--workers", str(workers)])
    if seed is not None:
        call.extend(["--seed", str(seed)])
    outjson = open(prefix + "/result.json", "w")
    outerr = open(prefix + "/out.err", "w")
    return (
        Popen(call, stdout=outjson, stderr=outerr),
        outjson,
        outerr,
    )
