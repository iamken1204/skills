#!/usr/bin/env python3
"""Dump the JS bundle and embedded files out of a Bun single-file executable.

Bun appends a "standalone module graph" to the binary (Mach-O: the __BUN
segment; ELF/PE: the tail of the file). Its layout, from the end:

    [module contents ...][module names ...][module table][Offsets][trailer]

    trailer  = b"\\n---- Bun! ----\\n"
    Offsets  = byte_count u64 | modules{off u32, len u32} | entry_point u32
             | exec_argv{off u32, len u32} | flags u32            (32 bytes)
    entry    = name{off,len} contents{off,len} sourcemap{off,len} bytecode{off,len}
             | 16 reserved bytes | encoding u8 loader u8 module_format u8 side u8

All offsets are relative to the graph base = trailer_start - 32 - byte_count.
JS sources are usually stored as UTF-16LE, which is why `strings` on the binary
finds almost nothing. If the table layout does not match (newer Bun), the script
falls back to locating the "// @bun" header and decoding from there.

Usage: unpack.py <binary> [-o OUTDIR]
"""
import argparse
import os
import struct
import sys

TRAILER = b"\n---- Bun! ----\n"
OFFSETS_FMT = "<QIIIIII"  # 32 bytes
OFFSETS_SIZE = struct.calcsize(OFFSETS_FMT)
NAME_PREFIX = b"/$bunfs/"
ENTRY_STRIDES = (52, 44, 36, 60, 68)


def read_ptr(data, at):
    return struct.unpack_from("<II", data, at)


def parse_table(data, base, mod_off, mod_len):
    """Return [(name, contents_off, contents_len, encoding)] or None if layout is unknown."""
    for stride in ENTRY_STRIDES:
        if mod_len % stride:
            continue
        entries = []
        ok = True
        for i in range(mod_len // stride):
            at = base + mod_off + i * stride
            n_off, n_len = read_ptr(data, at)
            c_off, c_len = read_ptr(data, at + 8)
            name = data[base + n_off : base + n_off + n_len]
            if not name.startswith(NAME_PREFIX) or c_off + c_len > len(data) - base:
                ok = False
                break
            encoding = data[at + stride - 4]
            entries.append((name.decode("utf-8", "replace"), c_off, c_len, encoding))
        if ok and entries:
            return entries
    return None


def looks_utf16le(b):
    head = b[:64]
    return len(head) >= 8 and all(head[i] == 0 for i in range(1, len(head), 2))


def decode_module(raw, encoding):
    if encoding == 2 or looks_utf16le(raw):
        return raw.decode("utf-16-le", "replace"), "utf-16-le"
    if raw[:7] == b"// @bun" or raw[:1] in (b"/", b"(", b"v", b"i", b"\""):
        try:
            return raw.decode("utf-8"), "utf-8"
        except UnicodeDecodeError:
            pass
    return None, "binary"


def fallback_main_module(data, base, trailer_at):
    """No usable table: find the JS header at base and take everything up to the first name string."""
    utf16_header = "// @bun".encode("utf-16-le")
    if data[base : base + len(utf16_header)] == utf16_header:
        enc = "utf-16-le"
    elif data[base : base + 7] == b"// @bun":
        enc = "utf-8"
    else:
        return None
    first_name = data.find(NAME_PREFIX, base, trailer_at)
    end = first_name if first_name > 0 else trailer_at
    # the .node/binary files sit between the JS and the names; cut at the first NUL run
    nul_run = data.find(b"\x00" * 16, base, end)
    if nul_run > 0:
        end = nul_run
    return data[base:end].decode(enc, "replace"), enc


def safe_name(name):
    return name.replace("/$bunfs/root/", "").replace("/", "__") or "module"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("binary")
    ap.add_argument("-o", "--out", default="bun-unpacked")
    args = ap.parse_args()

    data = open(args.binary, "rb").read()
    trailer_at = data.rfind(TRAILER)
    if trailer_at < 0:
        sys.exit("no Bun trailer found: not a Bun single-file executable")

    byte_count, mod_off, mod_len, entry_id, argv_off, argv_len, flags = struct.unpack_from(
        OFFSETS_FMT, data, trailer_at - OFFSETS_SIZE
    )
    base = trailer_at - OFFSETS_SIZE - byte_count
    os.makedirs(args.out, exist_ok=True)

    entries = parse_table(data, base, mod_off, mod_len) if 0 < base < trailer_at else None
    written = []
    if entries:
        for name, c_off, c_len, encoding in entries:
            raw = data[base + c_off : base + c_off + c_len]
            text, enc = decode_module(raw, encoding)
            out = os.path.join(args.out, safe_name(name) + ("" if enc == "binary" else ".js"))
            if text is None:
                open(out, "wb").write(raw)
            else:
                open(out, "w", encoding="utf-8").write(text)
            written.append((name, out, len(raw), enc))
    else:
        got = fallback_main_module(data, base, trailer_at)
        if not got:
            sys.exit("module table layout unknown and no '// @bun' header at graph base; inspect the trailer by hand")
        text, enc = got
        out = os.path.join(args.out, "main.js")
        open(out, "w", encoding="utf-8").write(text)
        written.append(("(fallback) main module", out, len(text), enc))

    print(f"graph base={base:#x} trailer={trailer_at:#x} byte_count={byte_count} entry_point={entry_id} flags={flags:#x}")
    for name, out, size, enc in written:
        print(f"  {name}  ->  {out}  ({size:,} bytes, {enc})")


if __name__ == "__main__":
    main()
