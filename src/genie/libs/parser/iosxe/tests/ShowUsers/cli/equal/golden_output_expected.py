expected_output = {
    "line": {
        "2 vty 0": {
            "active": False,
            "host": "idle",
            "idle": "00:35:32",
            "location": "10.0.0.1",
            "user": "nos",
            "tty": "2",
        },
        "3 vty 1": {
            "active": False,
            "host": "idle",
            "idle": "00:41:43",
            "location": "10.0.0.2",
            "user": "testuser",
            "tty": "3",
        },
        "4 vty 2": {
            "active": True,
            "host": "idle",
            "idle": "00:00:07",
            "location": "10.0.0.3",
            "user": "testuser",
            "tty": "4",
        },
        "5 vty 3": {
            "active": False,
            "host": "idle",
            "idle": "04:20:29",
            "location": "10.0.0.4",
            "user": "testuser",
            "tty": "5",
        },
        "6 vty 4": {
            "active": False,
            "host": "idle",
            "idle": "00:00:44",
            "location": "10.0.0.5",
            "user": "user",
            "tty": "6",
        },
    }
}
