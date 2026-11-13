# Reinstalling DSM and checks

## Choosing the version to install (important)

> **For the first installation, install the version that Synology Assistant displays for the NAS.**
>
> In junior mode, Synology Assistant shows a version in the "Version" column (here **6.2.4-25556**). The NAS expects this version: it matches the initial filesystem already present in the flash. So I downloaded the `.pat` file of **that same version** for this model (`DSM_DS218_25556.pat`), and the installation went all the way through.

Details, so as not to overstate this rule:

- It is an **observed practice**: with the version shown by Synology Assistant, the installation succeeded. I did **not test** any other version, so I cannot claim another version fails.
- The initial blockage was **not** caused by a wrong version: it was the blank partition table ([root cause](06-root-cause.md)). Choosing the right version is not enough on its own.
- The file must match the exact **model** (DS218 here, not DS218+ nor DS218j).
- After the installation, the NAS may offer updates (same branch, then DSM 7). They are done **after** the first installation, not during it.

**Procedure:**

1. In PuTTY, run `tail -f /var/log/messages` before the installation and leave it running.
2. In Synology Assistant, double-click the NAS and choose **Reinstall** (not "Migration").
3. Select `DSM_DS218_25556.pat` and let the installation run to the end without touching anything.

## What the log shows

- The `updater` successively opens `FIS directory`, `zImage` and `rd.gz`, writes them, then the NAS reboots. The `find mtd partition [RedBoot] by name fail` error is gone.
- After the reboot, the kernel is the right one:

```text
Linux version 4.4.59+ ... #25556 SMP Tue May  2 17:14:51 CST 2023
5 RedBoot partitions found on MTD device RtkSFC
```

- No more `version magic` errors, no more `init not health` messages. The USB, network and `synobios` modules load.
- The console reaches the DSM login prompt about 50 seconds after power-on.

## Identity check

Synology Assistant now shows the original serial number and MAC address (`<SN>` and `<MAC>`), identical to the label on the NAS. They were previously empty or random. This confirms that the `vendor` partition is now readable and that the factory identity was never lost.

[INSERT PHOTO: Synology Assistant after the repair, with the serial number and MAC displayed (to be hidden before publishing)]
[INSERT PHOTO: NAS label (to be fully hidden before publishing)]
[INSERT PHOTO: DSM setup page, first screen]

## The installation page: the final goal

This is where this repository's path ends: reaching the DSM setup wizard, then finishing it. Here is what each screen looks like and what to check.

### 1. In Synology Assistant

Before the repair, the NAS appears with the status **"Migratable"** but the installation fails. After repairing the FIS table:

1. The NAS still appears as **"Migratable"** (this is normal: a system is detected but is not complete). Double-click it.
2. The web wizard offers **Migration** or **Reinstall**. Choose **Reinstall** (the disks are empty or do not matter).
3. Point to the `.pat` file of the right version (see above).
4. The installation writes the system, then the NAS reboots. Allow a few minutes.

[INSERT PHOTO: Synology Assistant, NAS "Migratable" (hide IP, MAC, serial number)]
[INSERT PHOTO: "Reinstall" choice in the web wizard]
[INSERT PHOTO: installation progress bar]

### 2. The DSM setup wizard

After the reboot, Synology Assistant shows the NAS as **"Ready"** or **"Not configured"**. Double-click it: the setup wizard asks for:

| Screen | What to enter |
|---|---|
| Server name | A name of your choice (do not publish it) |
| Administrator account | A user name and a **strong** password that only you know |
| DSM updates | "Install important updates automatically" or notification only. Your call |
| QuickConnect | Optional, you can skip it |
| Analytics / statistics | Optional |

Finish, and you land on the **DSM desktop**. The NAS is repaired.

[INSERT PHOTO: "Welcome" screen of the DSM setup wizard]
[INSERT PHOTO: DSM desktop (hide the server name and the address)]

### 3. Success criteria

Tick each of these points:

- [ ] No more `find mtd partition [RedBoot] by name fail` error in `/var/log/messages` during the installation.
- [ ] After the reboot, `Linux version 4.4.59+ ... #25556` (or the installed version) and `5 RedBoot partitions found`.
- [ ] The console reaches `login:`.
- [ ] Synology Assistant shows the serial number and the MAC address.
- [ ] The DSM setup wizard opens in the browser.
- [ ] A cold reboot (full shutdown, unplug for a few seconds, power on) works **several times in a row**.

If a point fails: [troubleshooting](14-troubleshooting-faq.md).
