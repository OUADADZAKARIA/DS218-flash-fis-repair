# Stability tests

| Test | Result |
|---|---|
| Soft reboot from DSM ("Restart") | Passed. Back at the login prompt, services started |
| Cold boot (DSM shutdown, power unplugged for about 10 s) | **3 successes out of 3**, login prompt at about 50 s, no critical error |
| Messages to ignore in the logs | `read_env from factory failed`, `hub doesn't have any ports`, `iscsi_pluginserverd` restart (with no iSCSI target configured) |
| Absence of faults | No `ROM fail`, `panic`, `oops`, disk or memory error in the cold-boot logs |
| Load | Creation of a 3.49 TB Btrfs volume, background check running, CPU about 10 %, RAM about 13 % |
| Test disk (WD 4 TB) | "Healthy" status, 0 bad sectors, about 35 °C, quick S.M.A.R.T. test "Healthy" |
| Extended S.M.A.R.T. test | Started, then interrupted (no result recorded). To be run again |

> The extended stability test (several hours) was not finished at the time of writing. See [open questions](12-open-questions.md).

[INSERT PHOTO: cold-boot log with the login prompt (hide the server name)]
[INSERT PHOTO: Storage Manager with the created volume and the check running]
[INSERT PHOTO: disk health information (hide the disk serial number)]
