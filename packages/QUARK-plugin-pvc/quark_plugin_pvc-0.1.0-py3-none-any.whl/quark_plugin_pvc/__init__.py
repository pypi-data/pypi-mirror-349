from quark.plugin_manager import factory

from quark_plugin_pvc.pvc_graph_provider import PvcGraphProvider
from quark_plugin_pvc.pvc_qubo_mapping import PvcQuboMapping


def register() -> None:
    """
    Register all modules exposed to quark by this plugin.
    For each module, add a line of the form:
        factory.register("module_name", Module)

    The "module_name" will later be used to refer to the module in the configuration file.
    """
    factory.register("pvc_graph_provider", PvcGraphProvider)
    factory.register("pvc_qubo_mapping", PvcQuboMapping)
