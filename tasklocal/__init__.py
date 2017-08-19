import asyncio

MONKEYPATCHED_TASK_FIELD = '_monkeypatched_tasklocal'


def get_or_create_task_dict():
    task = asyncio.Task.current_task()
    if not hasattr(task, MONKEYPATCHED_TASK_FIELD):
        setattr(task, MONKEYPATCHED_TASK_FIELD, {})

    return getattr(task, MONKEYPATCHED_TASK_FIELD)


class local():
    """
    Not thread-safe.
    """
    def __getattribute__(self, key):
        d = get_or_create_task_dict()
        if key not in d:
            return super().__getattribute__(key)

        return d[key]

    def __setattr__(self, key, value):
        get_or_create_task_dict()[key] = value

    def clear(self):
        """
        Remove tasklocal data.
        """
        t = asyncio.Task.current_task()
        if hasattr(t, MONKEYPATCHED_TASK_FIELD):
            setattr(t, MONKEYPATCHED_TASK_FIELD, {})
