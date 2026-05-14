/**
 * Unit tests for config/paths.ts
 */

import { assertEquals, assertStringIncludes } from "https://deno.land/std@0.224.0/assert/mod.ts";
import { PATHS, BINARIES, courseDir, buildFilename, PROJECT_ROOT } from "../config/paths.ts";

Deno.test("PROJECT_ROOT ends with all-in-one", () => {
  assertStringIncludes(PROJECT_ROOT, "all-in-one");
});

Deno.test("PATHS.projectRoot is defined", () => {
  assertEquals(typeof PATHS.projectRoot, "string");
  assertEquals(PATHS.projectRoot, PROJECT_ROOT);
});

Deno.test("PATHS.flowDir ends with /flow", () => {
  assertStringIncludes(PATHS.flowDir, "/flow");
});

Deno.test("BINARIES.ytDlp ends with yt-dlp", () => {
  assertStringIncludes(BINARIES.ytDlp, "yt-dlp");
});

Deno.test("courseDir builds correct path", () => {
  const dir = courseDir("Test_Course");
  assertStringIncludes(dir, "flow/Test_Course");
});

Deno.test("buildFilename formats correctly", () => {
  const name = buildFilename(3, "Hello: World?", "md");
  assertEquals(name, "03-Hello_ World_.md");
});

Deno.test("buildFilename pads single digit index", () => {
  const name = buildFilename(1, "Title", "mp3");
  assertEquals(name, "01-Title.mp3");
});

Deno.test("buildFilename handles multi-digit index", () => {
  const name = buildFilename(12, "Title", "md");
  assertEquals(name, "12-Title.md");
});
