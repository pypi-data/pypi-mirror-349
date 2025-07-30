from typing import Optional

import typer
from icecream import ic
from typing_extensions import Annotated

import oak_cli.utils.api.custom_requests as custom_requests
from oak_cli.services.auxiliary import (
    generate_current_services_table,
    generate_service_inspection_table,
)
from oak_cli.services.common import get_all_services, get_single_service, undeploy_instance
from oak_cli.utils.api.common import get_system_manager_url
from oak_cli.utils.api.custom_http import HttpMethod
from oak_cli.utils.exceptions.types import OakCLIExceptionTypes
from oak_cli.utils.logging import logger
from oak_cli.utils.styling import display_table
from oak_cli.utils.typer_augmentations import AliasGroup
from oak_cli.utils.types import (
    LIVE_VIEW_FLAG_TYPE,
    VERBOSITY_FLAG_TYPE,
    ApplicationId,
    Id,
    ServiceId,
    Verbosity,
)

ic.configureOutput(prefix="")
app = typer.Typer(cls=AliasGroup)


@app.command("inspect, i", help="Inspect a specific service")
def inspect_service(
    service_id: ServiceId,
    live: LIVE_VIEW_FLAG_TYPE = False,
) -> None:
    display_table(
        live,
        table_generator=lambda: generate_service_inspection_table(live=live, service_id=service_id),
    )


@app.command("show, s", help="Show current services")
def show_current_services(
    app_id: Annotated[
        Optional[ApplicationId],
        typer.Argument(help="ID of the parent application which services to show"),
    ] = None,
    live: LIVE_VIEW_FLAG_TYPE = False,
    verbosity: VERBOSITY_FLAG_TYPE = Verbosity.SIMPLE.value,  # type: ignore
) -> None:
    current_services = get_all_services(app_id)

    if not live and not current_services:
        logger.info("No services exist yet")
        return

    if verbosity == Verbosity.EXHAUSTIVE:
        for i, service in enumerate(current_services):
            # NOTE: Hide information that is too verbose.
            HIDDEN_TEXT = "(hidden by CLI)"
            for instance in service["instance_list"]:
                instance["cpu_history"] = HIDDEN_TEXT
                instance["memory_history"] = HIDDEN_TEXT
                instance["logs"] = HIDDEN_TEXT
            ic(i, service)
            continue
        return

    display_table(
        live,
        table_generator=lambda: generate_current_services_table(app_id, Verbosity(verbosity), live),
    )


@app.command("deploy, d", help="Deploy a new service instance")
def deploy_new_instance(service_id: ServiceId) -> None:
    custom_requests.CustomRequest(
        custom_requests.RequestCore(
            http_method=HttpMethod.POST,
            base_url=get_system_manager_url(),
            api_endpoint=f"/api/service/{service_id}/instance",
        ),
        custom_requests.RequestAuxiliaries(
            what_should_happen=f"Deploy a new instance for the service '{service_id}'.",
            show_msg_on_success=True,
            oak_cli_exception_type=OakCLIExceptionTypes.SERVICE_DEPLOYMENT,
        ),
    ).execute()


@app.command(
    "undeploy, u",
    help="""
        Undeploy all services or only the specified ones
        (Without any optional flags undeploy all services)
        """,
)
def undeploy_instances(
    service_id: Annotated[
        Optional[ServiceId],
        typer.Option(help="If provided will only undeploy all instances of that service"),
    ] = None,
    instance_id: Annotated[
        Optional[Id],
        typer.Option(
            help="""
                Undeploy only the single instance of the specified service
                (Requires the 'service_id' to be provided)
                """
        ),
    ] = None,
) -> None:
    def undeploy_service_instances(service: dict) -> None:
        for instance in service["instance_list"]:
            undeploy_instance(
                service_id=service["microserviceID"],
                instance_id=instance["instance_number"],
            )

    if service_id:
        service = get_single_service(service_id)
        if instance_id:
            undeploy_instance(service_id=service_id, instance_id=instance_id)
            return
        undeploy_service_instances(service)
        return

    for service in get_all_services():
        undeploy_service_instances(service=service)
