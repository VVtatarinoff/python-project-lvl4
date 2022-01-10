STATUSES_TEST = [
    {
        "name": "first status name"
    },
    {
        "name": "second status name"
    },
    {
        "name": "third status name"
    }
]

LABELS_TEST = [
    {
        "name": "first label name"
    },
    {
        "name": "second label name"
    },
    {
        "name": "third label name"
    }
]
USERS_TEST = [
    {
        "first_name": "Elbert",
        "last_name": "Abshire",
        "username": "elbert-abshire",
        "password": "HQN7mD9mbM",
    },
    {
        "first_name": "Lawrence",
        "last_name": "Kulas",
        "username": "lawrence-kulas",
        "password": "T3LFhdQf6Y",
    },
    {
        "first_name": "Nona",
        "last_name": "Murray",
        "username": "nona-murray",
        "password": "ZqEryw3Yw4",
    }
]
TASKS_TEST = [
    {
        "name": "first task name",
        "description": "first task description",
        "status": 1,
        "executor": 1,
        'author': 1,
        "labels": [1, 3]
    },
    {
        "name": "second task name",
        "description": "second task description",
        "status": 2,
        "executor": 2,
        'author': 1,
        "labels": [1, 2]

    },
    {
        "name": "third task name",
        "description": "third task description",
        "status": 2,
        "executor": 3,
        'author': 1
    }
]

TEST_DATA = {
    "users": {
        "new": {
            "first_name": "Malika",
            "last_name": "Hodkiewicz",
            "full_name": "Malika Hodkiewicz",
            "username": "malika-hodkiewicz",
            "password1": "8RvGr5wWTu",
            "password2": "8RvGr5wWTu"

        },
        "existing": {
            "first_name": "Lawrence",
            "last_name": "Kulas",
            "full_name": "Lawrence Kulas",
            "username": "lawrence-kulas",
            "password": "T3LFhdQf6Y"
        }
    },
    "task_statuses": {
        "new": {
            "name": "new status name"
        },
        "existing": {
            "name": "second status name"
        }
    },
    "labels": {
        "new": {
            "name": "new label name"
        },
        "existing": {
            "name": "second label name"
        }
    },
    "tasks": {
        "first": {
            "name": "first task name",
            "description": "first task description",
            "status": "first status name",
            "executor": "Elbert Abshire",
            "labels": {
                "first": "first label name",
                "third": "third label name"
            }
        },
        "second": {
            "name": "second task name",
            "description": "second task description",
            "status": "second status name",
            "executor": "Lawrence Kulas",
            "labels": {
                "first": "first label name",
                "second": "second label name"
            }
        },
        "third": {
            "name": "third task name",
            "description": "third task description",
            "status": "second status name",
            "executor": "Nona Murray"
        }
    }
}
