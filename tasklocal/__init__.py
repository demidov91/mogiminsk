import asyncio


def get_or_create_task_dict():
    task = asyncio.Task.current_task()
    if not hasattr(task, '_monkeypatched_tasklocal'):
        task._monkeypatched_tasklocal = {}

    return task._monkeypatched_tasklocal


class local():
    def __getattribute__(self, key):
        d = get_or_create_task_dict()
        if key not in d:
            return super().__getattribute__(key)

        return d[key]

    def __setattr__(self, key, value):
        get_or_create_task_dict()[key] = value
