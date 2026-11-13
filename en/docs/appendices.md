# Appendices

## A. RedBoot FIS entry format (`fis_image_desc` structure)

```c
struct fis_image_desc {
    unsigned char name[16];     // name, padded with zeros
    uint32_t flash_base;        // address in the flash
    uint32_t mem_base;          // address in memory (0 here)
    uint32_t size;              // reserved size
    uint32_t entry_point;       // entry point (0 here)
    uint32_t data_length;       // data size (= size here)
    unsigned char _pad[256 - 16 - 5 * 4 - 2 * 4];  // 212 bytes of 0xFF
    uint32_t desc_cksum;        // ignored by the Linux parser
    uint32_t file_cksum;        // ignored by the Linux parser
};
```

The Linux parser (`redboot.c`) looks for the entry named "FIS directory" whose size equals that of an erase sector (`0x1000`), then reads the entries. A free entry starts with `0xFF`. The base address is masked with the flash size minus 1.

## B. Observed boot stages

ROM, `hwsetting`, FSBL, U-Boot 2012.07, U-Boot 2015.07, then the Linux kernel. Before the repair, the kernel in the flash was a 4.4.302+; after the reinstallation, it is the 4.4.59+ #25556 of DSM 6.2.4.

## C. Quick checklist

- [ ] Serial console at 3.3 V, 115200 8N1
- [ ] Two identical flash dumps (8 388 608 bytes)
- [ ] Blank table at `0x7ff000` confirmed
- [ ] Partition names confirmed (`RedBoot`, `zImage`, `rd.gz`, `vendor`, `FIS directory`)
- [ ] 4096-byte block built and compared with the expected one
- [ ] Write, read back, identical comparison
- [ ] `/proc/mtd`: 5 partitions after the reboot
- [ ] DSM reinstalled ("Reinstall", official `.pat` file **of the version shown by Synology Assistant**, right model)
- [ ] Three successful cold boots
- [ ] NAS plugged into the router, fixed IP (or DHCP reservation) and time synchronised
- [ ] Extended stability test finished
- [ ] New flash backup taken from the working system

## D. Preparing disks under Windows (`diskpart`)

During the tests, disks were wiped on a Windows PC before being put back in the NAS (the NAS sometimes wrote incomplete boot files to the disk). **`clean` erases the whole disk**: check its number very carefully.

In a command prompt **run as administrator**:

```text
diskpart
list disk
select disk <N>
clean
```

Replace `<N>` with the NAS disk number (check the size in `list disk`). An equivalent script (`script_diskpart.txt`) simply contains:

```text
select disk <N>
clean
```

and can be run with `diskpart /s script_diskpart.txt`.

**Stop:** if you are not certain of the disk number, do not type `clean`. The wrong number erases another disk of the PC.
