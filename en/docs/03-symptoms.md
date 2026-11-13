# Observed symptoms

## Software symptoms (the cause of the blockage)

- Synology Assistant shows the NAS with the status **"Migratable"** (French UI: « Pouvant être migré »), even after several reinstallations and even after wiping the disks.
- The web wizard only offers "Migration" or "Reinstall". The outcome is identical in both cases.
- After the `.pat` file is uploaded, the installation seems to run, then the NAS reboots into the same state.
- In the console log, on every attempt:

```text
find mtd partition [RedBoot] by name fail
fail to map all device partition
fail to malloc mtd driver buffer, error = 38
...
No upgrade file exists
Exit on error [3] init not health....
```

- In the kernel log:

```text
Searching for RedBoot partition table in RtkSFC at offset 0x7ff000
No RedBoot partition table detected
using single partition
```

- And `/proc/mtd` contained a single partition:

```text
dev:    size   erasesize  name
mtd0: 00800000 00001000 "RtkSFC"
```

- Every kernel module failed to load with:

```text
phy_rtk_usb2: version magic '4.4.59+ SMP mod_unload aarch64' should be '4.4.302+ SMP mod_unload aarch64'
```

  Cause: the flash held a 4.4.302+ kernel together with an initial filesystem from the 6.2.4-25556 family (modules built for 4.4.59+). This mismatch never went away because the installation never completed.

- The displayed serial number was empty or 0 and the MAC address changed at every boot (random values), because the `vendor` partition was not readable.

## Hardware symptoms (handled separately)

### Power and LEDs (before the intervention)

Before any repair, the behaviour at power-on varied from one attempt to the next:

| Case | Description |
|---|---|
| A | The **power button blinks blue** and **no other LED** lights up |
| B | The power button LED is **steady**, the **Status LED blinks green**, and the NAS **beeps** |
| C | Only the **power button blinks** |
| D | The **LAN** and **disk** LEDs never light up, even with disks inserted |
| E | With an **unallocated** disk inserted: back to case A (the button blinks blue, nothing else) |
| F | With **a single disk** previously formatted under Windows (ext-type filesystem): the NAS becomes **visible on the network**, the Status LED blinks green and the power button stays steady. According to the author, this was the only method that made the NAS visible at first |

### Boot blockages (serial console logs)

The serial console logs (24 PuTTY session files collected during this troubleshooting) show several families of failures. The excerpts below come from those logs.

**1. Reboot loop at the very start of boot (FSBL verification).** The boot never gets past the ROM: the NAS repeats the same lines in a loop until, sometimes, one attempt goes through.

```text
C1:80000000
C2
?
C3h
hwsetting size: 00000B94
C4
f
5-5verify fsbl fail
0000003BC7
C1:80000000
C2
?uu3-1
```

**2. Very early kernel crash (about 8 s after the kernel starts).** A memory access error, then a loop of audio coprocessor errors, then a complete halt:

```text
[    7.982879] Internal error: Oops: 96000006 [#1] SMP
[    8.354466] Internal error: Oops: 96000005 [#2] SMP
FATAL: Audio ROS Unexpected interrupt error!!
FATAL: Audio ROS Unexpected interrupt error!!
[    8.796186] Internal error: Oops - undefined instruction: 0 [#3] SMP
[    9.870675] Kernel panic - not syncing: Fatal exception in interrupt
```

(Part of the text in this log was garbled: a "non-existent" instruction, unreadable characters. That is consistent with memory corruption.)

**3. Memory corruption later, during installation or use.** Examples:

```text
[   55.379818] kernel BUG at mm/slab.c:2816!
[   55.384722] Internal error: Oops - BUG: 0 [#1] SMP
[   55.394723] CPU: 1 PID: 2134 Comm: findhostd Not tainted 4.4.302+ #90080
[   55.412021] PC is at cache_alloc_refill+0x22c/0x560

[  119.840990] skbuff: skb_over_panic: text:ffffffc0006360f4 len:1514 put:1514 head:ffffffc073071000 data:ffffffc073071088 tail:0x800672 end:0x680 dev:<NULL>
[  120.798638] Kernel panic - not syncing: Fatal exception in interrupt
```

In the last case, `tail` should be `0x672`: the difference with `0x800672` is exactly **bit 23** (`0x00800000`). The same bit was wrong in other crashes: the return address `d65f03c0` read as `d6df03c0`, and a program counter `…6aecf0` read as `…eaecf0`. Always the same bit, always flipping from 0 to 1. A faulty memory data line or a marginal solder joint fits this profile, not a software bug.

These crashes are clearly different from the final cause ([root cause](06-root-cause.md)): that one produces a **clean, repeatable** installer error, with no kernel crash.

### Effect of pressing on chip U3

**Pressing on chip U3 by hand guaranteed a good boot.** Without that pressure, the logs showed the blockages described above. It is the best clue pointing to a faulty solder contact under that chip (cracked BGA-type solder joints).

[INSERT PHOTO: log excerpt with `skb_over_panic` (hide any personal data)]
[INSERT PHOTO: log excerpt with a hang while reading the kernel (offset `0x002f0000`)]
[INSERT PHOTO: state of the NAS LEDs during a failed boot (blinking power button, other LEDs off)]
