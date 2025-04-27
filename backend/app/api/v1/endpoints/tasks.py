from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Task not found"}},
)


@router.get(
    "/",
    response_model=List[TaskRead],
    summary="List all tasks",
    description="Retrieve a list of all tasks in the system.",
    response_description="A list of tasks with their details.",
)
async def get_tasks(
    db: AsyncSession = Depends(get_db),
) -> List[TaskRead]:
    """Get all tasks."""
    result = await db.execute(select(Task))
    tasks = result.scalars().all()
    return tasks


@router.post(
    "/",
    response_model=TaskRead,
    summary="Create a new task",
    description="Create a new task with the provided details.",
    response_description="The created task with its ID.",
    status_code=201,
)
async def create_task(
    task_in: TaskCreate,
    db: AsyncSession = Depends(get_db),
) -> TaskRead:
    """Create a new task."""
    task = Task(title=task_in.title, description=task_in.description)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


@router.get(
    "/{task_id}",
    response_model=TaskRead,
    summary="Get a specific task",
    description="Retrieve a specific task by its ID.",
    response_description="The task details if found.",
    responses={404: {"description": "Task not found"}},
)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
) -> TaskRead:
    """Get a specific task by ID."""
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch(
    "/{task_id}",
    response_model=TaskRead,
    summary="Update a task",
    description="Partially update a task's details. Only provided fields will be updated.",
    response_description="The updated task details.",
    responses={404: {"description": "Task not found"}},
)
async def update_task(
    task_id: int,
    task_in: TaskUpdate,
    db: AsyncSession = Depends(get_db),
) -> TaskRead:
    """Partially update a task by ID."""
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if task_in.title is not None:
        task.title = task_in.title
    if task_in.description is not None:
        task.description = task_in.description
    await db.commit()
    await db.refresh(task)
    return task


@router.delete(
    "/{task_id}",
    response_model=dict,
    summary="Delete a task",
    description="Delete a task by its ID.",
    response_description="Confirmation of deletion.",
    responses={404: {"description": "Task not found"}},
)
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Delete a task by ID."""
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    await db.delete(task)
    await db.commit()
    return {"detail": "Task deleted"}
