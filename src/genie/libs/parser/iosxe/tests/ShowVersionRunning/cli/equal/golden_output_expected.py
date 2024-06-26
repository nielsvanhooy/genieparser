expected_output = {
    "version_running": {
        1: {
            "built": "n/a",
            "by": "n/a",
            "file": "consolidated:packages.conf",
            "file_sha_checksum": "5320a1aa65add90d5c7cfb0ccf4d5a68f6a4fe39",
            "on": "RP0",
            "package": "Provisioning File",
            "role": "provisioning file",
            "status": "active",
            "version": "n/a",
        },
        2: {
            "built": "2021-11-08_11.20",
            "by": "mcpre",
            "file": "consolidated:cat9k-rpbase.BLD_POLARIS_DEV_LATEST_20211108_175756.SSA.pkg",
            "file_sha_checksum": "ac93b8faa50c0c5b3d1e3f044e914ad3df34ccc5",
            "on": "RP0",
            "package": "rpbase",
            "role": "rp_base",
            "status": "active",
            "version": "BLD_POLARIS_DEV_LATEST_20211108_175756",
        },
        3: {
            "built": "2021-11-08_11.20",
            "by": "mcpre",
            "file": "consolidated:cat9k-rpboot.BLD_POLARIS_DEV_LATEST_20211108_175756.SSA.pkg",
            "file_sha_checksum": "n/a",
            "on": "RP0",
            "package": "rpboot",
            "role": "rp_boot",
            "status": "active",
            "version": "BLD_POLARIS_DEV_LATEST_20211108_175756",
        },
        4: {
            "built": "2021-11-08_11.20",
            "by": "mcpre",
            "file": "consolidated:cat9k-guestshell.BLD_POLARIS_DEV_LATEST_20211108_175756.SSA.pkg",
            "file_sha_checksum": "c42ea329f864e9eb830cf5a7e99864e488496558",
            "on": "RP0/0",
            "package": "guestshell",
            "role": "guestshell",
            "status": "active",
            "version": "BLD_POLARIS_DEV_LATEST_20211108_175756",
        },
        5: {
            "built": "2021-11-08_11.20",
            "by": "mcpre",
            "file": "consolidated:cat9k-rpbase.BLD_POLARIS_DEV_LATEST_20211108_175756.SSA.pkg",
            "file_sha_checksum": "ac93b8faa50c0c5b3d1e3f044e914ad3df34ccc5",
            "on": "RP0/0",
            "package": "rpbase",
            "role": "rp_daemons",
            "status": "active",
            "version": "BLD_POLARIS_DEV_LATEST_20211108_175756",
        },
        6: {
            "built": "2021-11-08_11.20",
            "by": "mcpre",
            "file": "consolidated:cat9k-rpbase.BLD_POLARIS_DEV_LATEST_20211108_175756.SSA.pkg",
            "file_sha_checksum": "ac93b8faa50c0c5b3d1e3f044e914ad3df34ccc5",
            "on": "RP0/0",
            "package": "rpbase",
            "role": "rp_iosd",
            "status": "active",
            "version": "BLD_POLARIS_DEV_LATEST_20211108_175756",
        },
        7: {
            "built": "2021-11-08_11.20",
            "by": "mcpre",
            "file": "consolidated:cat9k-rpbase.BLD_POLARIS_DEV_LATEST_20211108_175756.SSA.pkg",
            "file_sha_checksum": "ac93b8faa50c0c5b3d1e3f044e914ad3df34ccc5",
            "on": "RP0/0",
            "package": "rpbase",
            "role": "rp_security",
            "status": "active",
            "version": "BLD_POLARIS_DEV_LATEST_20211108_175756",
        },
        8: {
            "built": "2021-11-08_11.20",
            "by": "mcpre",
            "file": "consolidated:cat9k-webui.BLD_POLARIS_DEV_LATEST_20211108_175756.SSA.pkg",
            "file_sha_checksum": "836bc1e3e0b6fa3c4ef24239a76ef7f9896456c7",
            "on": "RP0/0",
            "package": "webui",
            "role": "rp_webui",
            "status": "active",
            "version": "BLD_POLARIS_DEV_LATEST_20211108_175756",
        },
        9: {
            "built": "2021-11-08_11.20",
            "by": "mcpre",
            "file": "consolidated:cat9k-srdriver.BLD_POLARIS_DEV_LATEST_20211108_175756.SSA.pkg",
            "file_sha_checksum": "f0a09b32013bcdde0f9ed18583dd60d290cf02ab",
            "on": "RP0/0",
            "package": "srdriver",
            "role": "srdriver",
            "status": "active",
            "version": "BLD_POLARIS_DEV_LATEST_20211108_175756",
        },
        10: {
            "built": "2021-11-08_11.20",
            "by": "mcpre",
            "file": "consolidated:cat9k-rpbase.BLD_POLARIS_DEV_LATEST_20211108_175756.SSA.pkg",
            "file_sha_checksum": "ac93b8faa50c0c5b3d1e3f044e914ad3df34ccc5",
            "on": "RP1",
            "package": "rpbase",
            "role": "rp_base",
            "status": "n/a",
            "version": "BLD_POLARIS_DEV_LATEST_20211108_175756",
        },
        11: {
            "built": "2021-11-08_11.20",
            "by": "mcpre",
            "file": "consolidated:cat9k-rpboot.BLD_POLARIS_DEV_LATEST_20211108_175756.SSA.pkg",
            "file_sha_checksum": "n/a",
            "on": "RP1",
            "package": "rpboot",
            "role": "rp_boot",
            "status": "n/a",
            "version": "BLD_POLARIS_DEV_LATEST_20211108_175756",
        },
        12: {
            "built": "2021-11-08_11.20",
            "by": "mcpre",
            "file": "consolidated:cat9k-wlc.BLD_POLARIS_DEV_LATEST_20211108_175756.SSA.pkg",
            "file_sha_checksum": "76aa35c084aacb3f7944e9b52d873d4405c4145c",
            "on": "RP1",
            "package": "wlc",
            "role": "rp_wlc",
            "status": "n/a",
            "version": "BLD_POLARIS_DEV_LATEST_20211108_175756",
        },
        13: {
            "built": "2021-11-08_11.20",
            "by": "mcpre",
            "file": "consolidated:cat9k-guestshell.BLD_POLARIS_DEV_LATEST_20211108_175756.SSA.pkg",
            "file_sha_checksum": "c42ea329f864e9eb830cf5a7e99864e488496558",
            "on": "RP1/0",
            "package": "guestshell",
            "role": "guestshell",
            "status": "n/a",
            "version": "BLD_POLARIS_DEV_LATEST_20211108_175756",
        },
        14: {
            "built": "2021-11-08_11.20",
            "by": "mcpre",
            "file": "consolidated:cat9k-rpbase.BLD_POLARIS_DEV_LATEST_20211108_175756.SSA.pkg",
            "file_sha_checksum": "ac93b8faa50c0c5b3d1e3f044e914ad3df34ccc5",
            "on": "RP1/0",
            "package": "rpbase",
            "role": "rp_daemons",
            "status": "n/a",
            "version": "BLD_POLARIS_DEV_LATEST_20211108_175756",
        },
        15: {
            "built": "2021-11-08_11.20",
            "by": "mcpre",
            "file": "consolidated:cat9k-rpbase.BLD_POLARIS_DEV_LATEST_20211108_175756.SSA.pkg",
            "file_sha_checksum": "ac93b8faa50c0c5b3d1e3f044e914ad3df34ccc5",
            "on": "RP1/0",
            "package": "rpbase",
            "role": "rp_iosd",
            "status": "n/a",
            "version": "BLD_POLARIS_DEV_LATEST_20211108_175756",
        },
        16: {
            "built": "2021-11-08_11.20",
            "by": "mcpre",
            "file": "consolidated:cat9k-rpbase.BLD_POLARIS_DEV_LATEST_20211108_175756.SSA.pkg",
            "file_sha_checksum": "ac93b8faa50c0c5b3d1e3f044e914ad3df34ccc5",
            "on": "RP1/0",
            "package": "rpbase",
            "role": "rp_security",
            "status": "n/a",
            "version": "BLD_POLARIS_DEV_LATEST_20211108_175756",
        },
        17: {
            "built": "2021-11-08_11.20",
            "by": "mcpre",
            "file": "consolidated:cat9k-webui.BLD_POLARIS_DEV_LATEST_20211108_175756.SSA.pkg",
            "file_sha_checksum": "836bc1e3e0b6fa3c4ef24239a76ef7f9896456c7",
            "on": "RP1/0",
            "package": "webui",
            "role": "rp_webui",
            "status": "n/a",
            "version": "BLD_POLARIS_DEV_LATEST_20211108_175756",
        },
        18: {
            "built": "2021-11-08_11.20",
            "by": "mcpre",
            "file": "/tmp/sw/isos/cat9k-srdriver.BLD_POLARIS_DEV_LATEST_20211108_175756.SSA.pkg",
            "file_sha_checksum": "f0a09b32013bcdde0f9ed18583dd60d290cf02ab",
            "on": "RP1/0",
            "package": "srdriver",
            "role": "srdriver",
            "status": "n/a",
            "version": "BLD_POLARIS_DEV_LATEST_20211108_175756",
        },
        19: {
            "built": "2021-11-08_11.20",
            "by": "mcpre",
            "file": "consolidated:cat9k-cc_srdriver.BLD_POLARIS_DEV_LATEST_20211108_175756.SSA.pkg",
            "file_sha_checksum": "685a30ff7ddb5383b30b72abbd1468980882987f",
            "on": "SLOT1",
            "package": "cc_srdriver",
            "role": "cc_srdriver",
            "status": "active",
            "version": "BLD_POLARIS_DEV_LATEST_20211108_175756",
        },
        20: {
            "built": "2021-11-08_11.20",
            "by": "mcpre",
            "file": "consolidated:cat9k-cc_srdriver.BLD_POLARIS_DEV_LATEST_20211108_175756.SSA.pkg",
            "file_sha_checksum": "685a30ff7ddb5383b30b72abbd1468980882987f",
            "on": "SLOT2",
            "package": "cc_srdriver",
            "role": "cc_srdriver",
            "status": "active",
            "version": "BLD_POLARIS_DEV_LATEST_20211108_175756",
        },
        21: {
            "built": "2021-11-08_11.20",
            "by": "mcpre",
            "file": "consolidated:cat9k-cc_srdriver.BLD_POLARIS_DEV_LATEST_20211108_175756.SSA.pkg",
            "file_sha_checksum": "685a30ff7ddb5383b30b72abbd1468980882987f",
            "on": "SLOT3",
            "package": "cc_srdriver",
            "role": "cc_srdriver",
            "status": "active",
            "version": "BLD_POLARIS_DEV_LATEST_20211108_175756",
        },
        22: {
            "built": "2021-11-08_11.20",
            "by": "mcpre",
            "file": "consolidated:cat9k-cc_srdriver.BLD_POLARIS_DEV_LATEST_20211108_175756.SSA.pkg",
            "file_sha_checksum": "685a30ff7ddb5383b30b72abbd1468980882987f",
            "on": "SLOT4",
            "package": "cc_srdriver",
            "role": "cc_srdriver",
            "status": "active",
            "version": "BLD_POLARIS_DEV_LATEST_20211108_175756",
        },
        23: {
            "built": "2021-11-08_11.20",
            "by": "mcpre",
            "file": "consolidated:cat9k-cc_srdriver.BLD_POLARIS_DEV_LATEST_20211108_175756.SSA.pkg",
            "file_sha_checksum": "685a30ff7ddb5383b30b72abbd1468980882987f",
            "on": "SLOT5",
            "package": "cc_srdriver",
            "role": "cc_srdriver",
            "status": "active",
            "version": "BLD_POLARIS_DEV_LATEST_20211108_175756",
        },
        24: {
            "built": "2021-11-08_11.20",
            "by": "mcpre",
            "file": "consolidated:cat9k-cc_srdriver.BLD_POLARIS_DEV_LATEST_20211108_175756.SSA.pkg",
            "file_sha_checksum": "685a30ff7ddb5383b30b72abbd1468980882987f",
            "on": "SLOT6",
            "package": "cc_srdriver",
            "role": "cc_srdriver",
            "status": "active",
            "version": "BLD_POLARIS_DEV_LATEST_20211108_175756",
        },
        25: {
            "built": "2021-11-08_11.20",
            "by": "mcpre",
            "file": "consolidated:cat9k-cc_srdriver.BLD_POLARIS_DEV_LATEST_20211108_175756.SSA.pkg",
            "file_sha_checksum": "685a30ff7ddb5383b30b72abbd1468980882987f",
            "on": "SLOT7",
            "package": "cc_srdriver",
            "role": "cc_srdriver",
            "status": "active",
            "version": "BLD_POLARIS_DEV_LATEST_20211108_175756",
        },
    }
}
