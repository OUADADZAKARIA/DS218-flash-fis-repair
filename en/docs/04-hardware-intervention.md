# Hardware intervention and RAM tests

## Hardware intervention

> **Before you read:** the **U3** reference is the one the author used on his own board (`HDR23L1` v1.1). Check the marking on yours (see [hardware and tools](01-hardware-and-tools.md)).

> Fields marked `[TO COMPLETE]` are details that were not provided. Do not publish this document without filling them in or deleting them.

**What was done:**

1. The enclosure was opened and the motherboard removed. [TO COMPLETE: opening steps, screws, order]
2. The **4 RAM chips were heated with hot air, several times, on both the front and the back of the board**, with particular attention to **U3**.
3. The board was left to **cool down** between operations.
4. A **plate** is used during the operation and **burns to the touch**. [TO CLARIFY: heating/preheating plate or metal heat-spreading plate]
5. A **metal cooling element** was added on the chips. It also **keeps pressure on U3**.
6. A fan was placed to cool the board during the tests. At first it was badly positioned.

**Hot-air reflow (to complete):**

| Parameter | Value |
|---|---|
| Tool used | [TO COMPLETE: hot-air station, heat gun…] |
| Set temperature | [TO COMPLETE] |
| Duration per chip and number of passes | [TO COMPLETE] |
| Airflow and nozzle | [TO COMPLETE] |
| Flux | [TO COMPLETE: yes/no, type] |
| Protection of neighbouring components | [TO COMPLETE] |
| Order of the chips | [TO COMPLETE] |
| Description of the cooling element | [TO COMPLETE: material, dimensions, mounting] |

[INSERT PHOTO: open enclosure, overview]
[INSERT PHOTO: board removed, front side (RAM chips)]
[INSERT PHOTO: board removed, back side (RAM chips)]
[INSERT PHOTO: heated area with the neighbouring components protected]
[INSERT PHOTO: plate used during the operation]
[INSERT PHOTO: metal cooling element in place, pressing on U3]
[INSERT PHOTO: final position of the fan]

**Observed result:** after these interventions, the **boot tests ran without errors**. Only then did the real "command line" phase begin ([timeline](05-timeline-and-diagnosis.md) and [procedure](08-rebuilding-the-fis-table.md)).

**Warnings specific to this intervention:**

- Hot-air reflow can **destroy** the board (chips, capacitors, neighbouring connectors) if temperature or duration are not controlled. The values in this chapter are not a recommendation.
- The improvement is a fact, but it is **not known which intervention** (repeated reflow, cooling and pressure element, fan) caused it. They were not tested separately.
- A metal part placed on a powered board can cause a short circuit or obstruct airflow. Check this before any prolonged power-on.
- Heated surfaces burn. Let everything cool down completely before touching.
- This intervention voids the NAS warranty.

## RAM tests (low and high zones)

Memory tests were run from the **U-Boot console** (`Realtek>` prompt), on a **low** and a **high** memory zone, then on the extended range. Original log: session of 21/10/2026.

**Entering the U-Boot console:** during boot, when the following message appears, press **Esc** (or Tab):

```text
Hit Esc or Tab key to enter console mode or rescue linux:  0
Press Esc Key
Enter console mode, disable watchdog ...
Realtek>
```

**Memory information (`bdinfo`):**

```text
DRAM bank   = 0x00000000
-> size     = 0x80000000          (2 GiB)
DDR        =  1600 MHz (0x1a)
DC0 DDR4, total size is 4Gb(x16)x2=8Gb
DC1 DDR4, total size is 4Gb(x16)x2=8Gb
```

**Commands and results:**

| Step | Command | Zone tested | Result |
|---|---|---|---|
| Disable the cache | `dcache off` | | `Data (writethrough) Cache is OFF` |
| Fill and read back | `mw.l 0x20000000 0x00000000 0x100000` then `md.l 0x20000000 0x100` | start of the low zone (4 MB written, 1 KB displayed) | All `00000000`, no difference |
| Low-zone test | `mtest 0x20000000 0x24000000` | 64 MB from `0x20000000` | The 4 patterns pass (`00000000`, `FFFFFFFF`, `00000001`, `FFFFFFFE`), no error shown |
| High-zone test | `mtest 0x60000000 0x64000000` | 64 MB from `0x60000000` | Same, no error shown |
| Re-enable the cache | `dcache on` | | `Cache: Enabled` |
| Extended test 1 | `mtest 0x20000000 0x40000000` | 512 MB | Same, no error shown |
| Extended test 2 | `mtest 0x40000000 0x7F000000` | about 1 GiB | Same, no error shown |
| Coupling test | `mtest2 cf 0x20000000 0x2000000 3` | 32 MB, 3 passes | `Tested 3 iteration(s) with 0 errors.` |
| Pattern test | `mtest2 saf 0x20000000 0x4000000 3` | 64 MB, 3 passes, ascending and descending `FFFFFFFF` and `00000000` patterns | `Tested 3 iteration(s) with 0 errors.` |

Notes on the commands:

- For `mtest2`, the second parameter is interpreted as a **size**, not as an end address (the output shows for example `end 0x23ffffff` for a size of `0x4000000`). A first attempt with 5 parameters only printed the help.
- `mtest` does **not** print an error counter: the absence of a message is the signal. Only `mtest2` prints `0 errors`.
- The `FFFFFFFE` and `00000001` patterns check one data line at a time, which suits the search for a stuck bit such as bit 23.

**Interpretation:** none of these tests showed a memory error. This confirms that, **at the time of the test**, the memory behaved correctly, including on the bit-23 data line. But **it is not proof of lasting stability**: the fault seen before the repair was intermittent (it depended on pressure on U3 and probably on heat), and a short U-Boot test can miss it. Only repeated cold boots and long installation sessions without a crash ([stability tests](11-stability-tests.md)) provide that proof.

[INSERT PHOTO: U-Boot terminal screenshot with `bdinfo` (hide default IP and MAC addresses if they appear)]
[INSERT PHOTO: U-Boot terminal screenshot with `mtest` results, low and high zones]
[INSERT PHOTO: U-Boot terminal screenshot with `mtest2 ... 0 errors`]
