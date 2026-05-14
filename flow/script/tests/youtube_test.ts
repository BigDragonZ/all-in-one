/**
 * Unit tests for lib/youtube.ts
 */

import { assertEquals, assertStringIncludes } from "https://deno.land/std@0.224.0/assert/mod.ts";
import { parseSrt, toMarkdown } from "../lib/youtube.ts";

Deno.test("parseSrt handles basic SRT", () => {
  const srt = `1
00:00:01,000 --> 00:00:03,000
Hello world

2
00:00:04,000 --> 00:00:05,000
Second line
`;
  const entries = parseSrt(srt);
  assertEquals(entries.length, 2);
  assertEquals(entries[0].index, 1);
  assertEquals(entries[0].start, "00:00:01,000");
  assertEquals(entries[0].text, "Hello world");
});

Deno.test("parseSrt strips HTML tags", () => {
  const srt = `1
00:00:01,000 --> 00:00:02,000
<b>Bold</b> text
`;
  const entries = parseSrt(srt);
  assertEquals(entries[0].text, "Bold text");
});

Deno.test("parseSrt strips music markers", () => {
  const srt = `1
00:00:01,000 --> 00:00:02,000
[Music] playing ♪
`;
  const entries = parseSrt(srt);
  assertEquals(entries[0].text, "playing");
});

Deno.test("parseSrt skips empty entries", () => {
  const srt = `1
00:00:01,000 --> 00:00:02,000

2
00:00:03,000 --> 00:00:04,000
Real text
`;
  const entries = parseSrt(srt);
  assertEquals(entries.length, 1);
  assertEquals(entries[0].text, "Real text");
});

Deno.test("toMarkdown includes metadata", () => {
  const entries = [{ index: 1, start: "00:00:01,000", end: "00:00:02,000", text: "Hello" }];
  const md = toMarkdown(entries, {
    title: "Test Video",
    url: "https://example.com",
    course: "Test_Course",
    index: 5,
  });
  assertStringIncludes(md, "# Test Video");
  assertStringIncludes(md, "**序号**: 5");
  assertStringIncludes(md, "**课程**: Test_Course");
  assertStringIncludes(md, "https://example.com");
  assertStringIncludes(md, "**条目数**: 1");
});

Deno.test("toMarkdown includes subtitle entries", () => {
  const entries = [
    { index: 1, start: "00:00:01,000", end: "00:00:02,000", text: "First" },
    { index: 2, start: "00:00:03,000", end: "00:00:04,000", text: "Second" },
  ];
  const md = toMarkdown(entries, {
    title: "Test",
    url: "https://example.com",
    course: "Course",
    index: 1,
  });
  assertStringIncludes(md, "**[00:00:01,000 - 00:00:02,000]** First");
  assertStringIncludes(md, "**[00:00:03,000 - 00:00:04,000]** Second");
});
