import importlib
from . import watch as inner_watch, plugin as inner_plugin

__all__ = ("call_watch", "call_plugin")


def load_plugin(package, name):
    """
    definition of plugin is a module with callable main, which is recommended in form of class __call__

    plugin is divided into built-in and custom parts. Logically, built-in function will be found first, so you need to avoid the same name.
    """
    plug = importlib.import_module(package + f".{name}")
    return getattr(plug, "main")
    # return __import__(folder+f".{name}.main")


def call_watch(name):
    try:
        ret = getattr(inner_watch, name).main()
    except AttributeError:
        ret = load_plugin("watch", name)()
    return ret


def call_plugin(name, query, exp):
    try:
        ret = getattr(inner_plugin, name).main(query, exp)
    except AttributeError:
        ret = load_plugin("plugin", name)(query, exp)
    return ret
