from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.custom_hooks import handle_event_notification, schedule_task

router = APIRouter()

class EventNotification(BaseModel):
    event_type: str
    payload: dict

class ScheduleTask(BaseModel):
    task_name: str
    schedule: str
    args: dict = {}

@router.post("/hooks/event/", description="Handle incoming event notifications and process them based on their type.")
async def receive_event(notification: EventNotification):
    try:
        result = handle_event_notification(notification.event_type, notification.payload)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/tasks/schedule/", description="Schedule a background task with the specified name, schedule, and arguments.")
async def schedule_background_task(task: ScheduleTask):
    try:
        result = schedule_task(task.task_name, task.schedule, task.args)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))