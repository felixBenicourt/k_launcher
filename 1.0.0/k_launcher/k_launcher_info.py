
import logging


logging.basicConfig(level=logging.INFO)


def print_k_launcher_documentation():
    """
    Prints the documentation for k_launcher in a single log statement.
    """
    documentation = """
    This is the documentation for the k_launcher.

    Usage:
        rez env k_launcher -- wrapper args*

    Arguments (args*):
        -config : name of the config you're working on.

    Additional Arguments:
        -pa : package you are working on.
        -launch : launch the DCC using his name.
        -add : add packages.
        -grab : grab the package in PROD to LOCAL.
        -save : save the context.
        -load : load the context.
        -info : listing of the options

    Example Launch Commands:
        rez env k_launcher -- run -config <config_name>
        rez env k_launcher -- run -config <config_name> -pa <package_name> -add <additional_package> -save
        rez env k_launcher -- run -config <config_name> -load <saved_context>
        rez env k_launcher -- run -config <config_name> -launch <dcc_software>

    Config Structure:
        config : package : context/path/file.rxt
    """
    logging.info(documentation)


