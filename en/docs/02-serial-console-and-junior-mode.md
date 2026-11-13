# Serial console (UART) and the junior-mode shell

This chapter explains how to **see what the NAS does while it boots** and how to get a **shell** on it when DSM is not installed. The rest of this repository depends on it: without boot logs, it is impossible to tell a hardware problem from a software one.

> **Reminder:** never connect a 5 V level to the console. The board's UART connector works at **3.3 V**.

## 1. Why a serial console

- The web interface and Synology Assistant only show a summarised state ("Migratable"). The real reason for an installation failure is in the NAS logs.
- Errors from the very beginning of boot (the `verify fsbl fail` loop, a kernel crash before the network is up) appear **nowhere else** than on the serial console.
- The serial console also gives access to **U-Boot** (RAM tests) and to the **junior-mode shell** (flash backup and repair).

## 2. Required hardware

| Item | Detail |
|---|---|
| USB-serial adapter | An FT232-type chip, set to **3.3 V** (jumper or switch on the adapter) |
| Wires | 3 jumper wires: ground (**GND**), **TX** and **RX**. No power wire (VCC) |
| Software | PuTTY (Windows), or any serial terminal (`screen`, `minicom`, `picocom` on Linux) |

[INSERT PHOTO: the USB-serial adapter with the voltage selector on 3.3 V]

## 3. Connecting the adapter to the board

The DS218 (`HDR23L1` v1.1 board) has a service connector marked **J2**, which is the UART console. I did not record the pinout pin by pin here: **identify it yourself before connecting anything**.

1. **Turn the NAS off and unplug the power.**
2. Locate the **J2** connector on the board (silkscreen next to the connector).
3. Identify **ground (GND)** with a multimeter in continuity mode: it is connected to the board ground (for example the USB connector shield or a metal mounting screw).
4. Identify **TX** and **RX**: during boot, the NAS **TX** pin shows activity around 3.3 V. It connects to the adapter's **RX**. The NAS **RX** pin connects to the adapter's **TX**. The two are **crossed**.
5. Do **not** connect any power pin (VCC, 3.3 V, 5 V) of the adapter to the board: the NAS powers itself.
6. If you are unsure about a pin, **do not connect it**: the wrong wire can damage the board.

**Stop:** if you are not certain of the pinout, stop. No step in this repository justifies connecting "just to try".

[INSERT PHOTO: the J2 connector located on the board]
[INSERT PHOTO: GND, TX and RX wires connected to J2 (hide any personal information that is visible)]

## 4. Configuring PuTTY

1. Plug the USB adapter into the PC. In Windows **Device Manager**, open **Ports (COM & LPT)** and note the port number (for example `COM6`).
2. Start PuTTY, choose **Serial** (not SSH) and fill in:

| Setting | Value |
|---|---|
| Serial line | the port you noted (for example `COM6`) |
| Speed (baud) | `115200` |
| Data bits | `8` |
| Stop bits | `1` |
| Parity | `None` |
| Flow control | `None` |

3. **Save the log to a file**: in the left pane, open **Session > Logging**, tick **All session output** and set a file name such as `ds218_&Y&M&D_&T.log` (PuTTY replaces `&Y&M&D_&T` with the date and time). You get one log per session without copying anything by hand.
4. Click **Open**, then power on the NAS.

[INSERT PHOTO: PuTTY configuration window in Serial mode (115200, 8N1, no flow control)]
[INSERT PHOTO: "All session output" ticked in Session > Logging]

## 5. Reading a boot

The stages you see scroll by, in order:

| What you see | Stage |
|---|---|
| `C1:80000000`, `C2`, `C3h`, then `hwsetting_...` and `secure_fsbl_...` lines | SoC boot ROM, reading of the hwsetting and the FSBL |
| `U-Boot 2012.07 ...` then `U-Boot 2015.07 ...` | U-Boot loaders |
| `Hit Esc or Tab key to enter console mode or rescue linux` | **Window to enter the U-Boot console** (press Esc) |
| `Starting Kernel ...` | Linux kernel starts |
| `[    0.000000] Linux version ...` | Start of the kernel log |
| `DiskStation login:` | The system is up |

A healthy boot of this DS218 under DSM reaches the login prompt about **50 s** after power-on.

A few landmarks to recognise a failed boot:
- a **loop** repeating `C1:80000000` … `verify fsbl fail`: the boot does not progress;
- `Internal error: Oops`, `Kernel panic` or `FATAL: Audio ROS Unexpected interrupt error!!`: kernel crash;
- a hang with no message after `reading byte size = 0x002f0000` (reading the kernel).

The signatures and their interpretation are in the [timeline and diagnosis](05-timeline-and-diagnosis.md) chapter. The `scripts/analyze_log.py` script finds them automatically in a log.

## 6. Entering the U-Boot console

1. Turn the NAS off, open the PuTTY session, power on again.
2. As soon as the message `Hit Esc or Tab key to enter console mode or rescue linux` appears, press **Esc** several times.
3. The prompt becomes `Realtek>`. Type `help` for the list of commands.

Useful commands here (check with `help` what your U-Boot offers): `bdinfo` (memory and clock information), `mw` / `md` (write and display memory), `mtest` and `mtest2` (RAM tests, see the [hardware intervention](04-hardware-intervention.md) chapter), `reset` (reboot).

**Warning:** U-Boot is for observing. Do not use `saveenv`, `rtkspi`, `fatwrite`, `keyset` or `uart_write` unless you know exactly what you are doing. A mistake can erase the bootloader or the factory identity.

## 7. The junior-mode shell

When DSM is not (or no longer) installed, the NAS boots into **junior mode**: a mini system in RAM, enough to receive an installation. In this mode, Synology Assistant shows the status "Migratable" or "Not installed".

1. Let the boot run to `DiskStation login:`.
2. Log in as **`root`** with Synology's junior-mode password: this is a publicly documented default value (search for "Synology junior mode root password"). It is **`101-0101`** on DSM 6.2.
3. You get a BusyBox shell: `BusyBox v1.16.1 ... built-in shell (ash)`.

**Be aware of what this means:** this shell is a full administrator shell on the NAS. A mistyped command on `/dev/mtd*` or on a disk is irreversible.

### Available and missing tools

Observed on this NAS (the list is not exhaustive):

| Present (used here) | Missing (observed) |
|---|---|
| `cat`, `dd`, `printf`, `ls`, `tail`, `grep`, `ifconfig`, `httpd`, `vi` | `od`, `hexdump`, `md5sum`, `tr`, `cmp`, `sed`, `awk`, `strings` |

Always test a tool before relying on it: `which od` prints nothing if it is missing.

Practical consequence: **you cannot analyse a flash dump on the NAS**. You copy it to the PC and analyse it there (see below).

### Getting a file from the NAS to the PC

`/tmp` is in **RAM**: everything is lost at reboot, so retrieve your files before that. To download them, start a small web server:

```sh
httpd -p 8081 -h /tmp
```

Then, on the PC, open `http://<NAS_IP>:8081/<file_name>` in a browser. If the message `bind: Address already in use` appears, the server is already running.

To find the NAS address in junior mode: `ifconfig` (or Synology Assistant). A `169.254.x.x` address means no DHCP server answered: see [after the installation](10-after-installation.md).

### Reading the junior-mode logs

```sh
tail -n 60 /var/log/messages     # latest messages (installation, updater errors)
tail -f /var/log/messages        # follow live (Ctrl+C to stop)
dmesg | tail -n 80               # kernel log
cat /proc/mtd                    # flash partitions (see chapter 07)
```

If you start `tail -f` **before** an installation and no longer touch the terminal, the log stays complete. If you open another terminal during it, it may get lost.

[INSERT PHOTO: `DiskStation login:` prompt then BusyBox shell in PuTTY (hide the server name)]
[INSERT PHOTO: output of `cat /proc/mtd` in junior mode (a single `RtkSFC` partition)]
