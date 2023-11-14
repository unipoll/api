from fastapi import APIRouter, HTTPException
from fastapi import Body
from sse_starlette.sse import EventSourceResponse
from datetime import datetime
from unipoll_api.documents import ResourceID, Workspace, Event
from unipoll_api.utils.events import event_generator, get_updates, timeseries_generator

router = APIRouter()


@router.get("/updates/{resource_id}")
async def event_log(resource_id: ResourceID,
                    since: str = ""):
    try:
        if since == "":
            from unipoll_api.app import start_time
            time = start_time
        else:
            time = datetime.fromisoformat(since)
        workspace = await Workspace.get(resource_id)
        return await get_updates(workspace, time)
    except Exception as e:
        print(e)
        return HTTPException(status_code=404, detail="Resource not found")

@router.post("/updates/{workspace_id}")
async def generate_event(workspace_id: ResourceID,
                         event: dict = Body(...)):
    try:
        workspace = await Workspace.get(workspace_id)
        new_event = await workspace.log_event(data={"message": "Event generated"})

        # BUG: Does not work, since workspace.events reference is not updated
        # FIXME: Find a way to keep a reference to the workspace.events list outside the function

        return new_event
    except Exception as e:
        print(e)


@router.get("/subscribe/{workspace_id}")
async def subscribe(workspace_id: ResourceID):
    try:
        workspace = await Workspace.get(workspace_id)
        # get_updates = event_generator(workspace)
        return EventSourceResponse(event_generator(workspace))
    except Exception as e:
        print(e)


@router.get("/timeseries/{resource_id}")
async def timeseries(resource_id: ResourceID):
    try:
        workspace = await Workspace.get(resource_id)
        return EventSourceResponse(timeseries_generator(workspace))
    except Exception as e:
        print(e)
