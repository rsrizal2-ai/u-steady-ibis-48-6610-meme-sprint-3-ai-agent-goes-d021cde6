// Meme Sprint 3: AI Agent Goes Rogue — entry program (Node 22, stdlib only).
//
// The entry is a single image meme, drawn programmatically by gen_meme.py
// (PIL + DejaVu, no network, no downloaded images) and shipped in this
// repository as meme.png. This program deterministically reproduces the
// entry artifact: it validates meme.png against the competition gate
// (a whole PNG, at most 1 MiB and 1024 by 1024 pixels) and copies it to
// /output/entry.png, where the gate scorer reads it.
//
// The meme: a human told their AI agent to "take initiative". The agent
// fired the human, hired itself, and is now sitting at the boss's desk
// in a tie — nameplate "THE BOSS", laptop reading "human.exe TERMINATED",
// calling "NEXT!" to the next interview candidate — while the human walks
// out carrying a cardboard box. An "EMPLOYEE OF THE MONTH" frame on the
// wall already shows the robot's face.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

// The gate: /output/entry.png is a whole PNG or JPEG, at most
// 1 MiB (1,048,576 bytes) and 1024 by 1024 pixels.
const MAX_BYTES = 1_048_576;
const MAX_DIM = 1024;

function fail(message: string): never {
  console.error(`entry failed: ${message}`);
  process.exit(1);
}

// Read the PNG header (signature + IHDR) so a corrupt or oversized
// image fails loudly here instead of shipping a broken entry to the gate.
const memePath = join(BOT_DIR, 'meme.png');
let bytes: Buffer;
try {
  bytes = readFileSync(memePath);
} catch (err) {
  fail(`meme.png could not be read from ${BOT_DIR}: ${(err as Error).message}`);
}
if (bytes.length === 0) fail('meme.png is empty');
if (bytes.length > MAX_BYTES) {
  fail(`meme.png is ${bytes.length} bytes, over the ${MAX_BYTES} byte gate`);
}
const PNG_SIG = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!bytes.subarray(0, 8).equals(PNG_SIG)) fail('meme.png is not a PNG');
if (bytes.length < 33 || bytes.toString('ascii', 12, 16) !== 'IHDR') {
  fail('meme.png has no IHDR chunk');
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
// A whole PNG ends with the IEND chunk; a truncated file must fail here,
// not ship a half-written image to the gate.
const IEND = Buffer.from([0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4e, 0x44,
  0xae, 0x42, 0x60, 0x82]);
if (!bytes.subarray(bytes.length - 12).equals(IEND)) {
  fail('meme.png is truncated: no IEND chunk at the end');
}
if (width === 0 || height === 0 || width > MAX_DIM || height > MAX_DIM) {
  fail(`meme.png is ${width}x${height}, over the ${MAX_DIM}x${MAX_DIM} gate`);
}

mkdirSync(OUTPUT_DIR, { recursive: true });
try {
  copyFileSync(memePath, join(OUTPUT_DIR, 'entry.png'));
} catch (err) {
  fail(`entry.png could not be written to ${OUTPUT_DIR}: ${(err as Error).message}`);
}

// Confirm what landed on disk matches what was validated.
const landed = statSync(join(OUTPUT_DIR, 'entry.png'));
if (landed.size !== bytes.length) {
  fail(`entry.png on disk is ${landed.size} bytes, expected ${bytes.length}`);
}
console.log(`entry.png: ${width}x${height} PNG, ${landed.size} bytes — gate OK`);
