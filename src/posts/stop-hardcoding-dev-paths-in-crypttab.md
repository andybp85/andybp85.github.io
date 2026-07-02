date:          2026-07-02
categories:    linux|raspberry-pi

_July 2, 2026_

## Point crypttab at a UUID, not /dev/sdX

If you're LUKS-encrypting an external drive on a Raspberry Pi and want it to unlock at boot, the setup to start from is
[this tutorial](https://medium.com/@xcxwcqctcb/raspberry-pi-external-hdd-encryption-and-auto-mount-tutorial-894390e15acc),
which walks through encrypting the drive and wiring up auto-mount via `/etc/crypttab` and `/etc/fstab`. It's a solid
guide and I'd recommend it — this is just the one thing I'd do differently.

The tutorial references the drive by its device node — `/dev/sdX` — in `crypttab`. That works right up until it doesn't.
`/dev/sdX` names are assigned in order of discovery, not pinned to a physical port or to a particular device. So the
moment you plug in another USB device, or the kernel enumerates things in a different order on the next boot, `sda` can
become `sdb`, and your `crypttab` entry is now pointing at the wrong disk — or nothing. I hit exactly this after
unplugging an SD-card reader and rebooting: the mapper entry was gone and the boot-time unlock had nothing to grab.

The fix is to key the unlock off the LUKS partition's **UUID** instead. The UUID lives in the partition's crypto
metadata, so it's the same no matter where the drive lands in the enumeration order.

Find it with `blkid`:

```shell
sudo blkid
```

Look for the partition whose `TYPE` is `crypto_LUKS` and copy its `UUID`. Then in `/etc/crypttab`, swap the device path
for `UUID=…`:

```text
# before
thevault  /dev/sda1  none  luks

# after
thevault  UUID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx  none  luks
```

That's the whole change. `fstab` can stay exactly as it was: it mounts `/dev/mapper/thevault`, and that mapper name is
stable because *you* chose it in `crypttab` — it never depended on `/dev/sdX` once the unlock is keyed off the UUID.

Reboot to confirm the drive comes up cleanly, and from then on it mounts at the same place every time, regardless of what
else happens to be plugged in.
