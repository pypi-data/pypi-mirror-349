from ddtrace import patch_all, tracer

patch_all()

from azure.functions import AppExtensionBase, Context
import typing
from logging import Logger

class TracerExtension(AppExtensionBase):
    """A Python worker extension to start Datadog tracer and insturment Azure Functions"""

    @classmethod
    def init(cls):
        pass

    @classmethod
    def pre_invocation_app_level(cls, _logger: Logger, context: Context, _func_args: typing.Dict[str, object] = {}, *args, **kwargs) -> None:
        route_function_name = context.function_name
        t = tracer.trace("azure_functions.invoke")
        span = tracer.current_span()
        span.set_tag('aas.function.name', route_function_name)
        tracer.current_span().resource = route_function_name
        cls.t = t

    @classmethod
    def post_invocation_app_level(cls, _logger: Logger, _context: Context, _func_args: typing.Dict[str, object] = {}, _func_ret: typing.Optional[object] = None, *args, **kwargs) -> None:
        cls.t.finish()
