/**
 * Unit tests for lib/audio.ts
 */

import { assertEquals, assertStringIncludes } from "https://deno.land/std@0.224.0/assert/mod.ts";

// We test probeFile with the existing test audio file
const TEST_AUDIO = "flow/Valuation_Undergrad_2022/01-Valuation_ A Preview.mp3";

Deno.test("probeFile returns valid metadata", async () => {
  const { probeFile } = await import("../lib/audio.ts");
  const info = await probeFile(TEST_AUDIO);
  
  assertEquals(typeof info.duration, "number");
  assertEquals(info.duration > 0, true);
  assertEquals(typeof info.bitrate, "number");
  assertEquals(info.bitrate > 0, true);
  assertEquals(typeof info.codec, "string");
  assertStringIncludes(info.codec, "mp3");
});

Deno.test("probeFile detects sample rate", async () => {
  const { probeFile } = await import("../lib/audio.ts");
  const info = await probeFile(TEST_AUDIO);
  
  assertEquals(info.sampleRate, 22050);
});
