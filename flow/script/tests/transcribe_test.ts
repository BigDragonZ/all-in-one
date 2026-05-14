/**
 * Unit tests for lib/transcribe.ts
 */

import { assertEquals, assertStringIncludes } from "https://deno.land/std@0.224.0/assert/mod.ts";
import { loadConfig, validateConfig } from "../config/transcribe.ts";

Deno.test("loadConfig returns default values", () => {
  const cfg = loadConfig();
  assertEquals(typeof cfg.gcpProjectId, "string");
  assertEquals(cfg.gcpProjectId, "gen-lang-client-0385617544");
  assertEquals(cfg.gcpLocation, "us-central1");
  assertEquals(cfg.gcpModel, "gemini-2.5-flash-lite");
  assertEquals(cfg.gcsBucket, "hermes_brain");
  assertEquals(cfg.gcsPrefix, "audio_jobs/");
  assertEquals(cfg.apiVersion, "v1");
  assertEquals(cfg.geminiStdModel, "gemini-2.5-flash-lite");
});

Deno.test("validateConfig throws when no credentials", () => {
  const cfg = {
    transcriber: null,
    gcpProjectId: "",
    gcpLocation: "",
    gcpModel: "",
    gcsBucket: "",
    gcsPrefix: "",
    apiVersion: "",
    gcpApiKey: "",
    geminiStdModel: "",
    googleApiKey: "",
  };
  let threw = false;
  try {
    validateConfig(cfg);
  } catch (e: any) {
    threw = true;
    assertStringIncludes(e.message, "No transcription credentials");
  }
  assertEquals(threw, true);
});

Deno.test("validateConfig passes with gcp key", () => {
  const cfg = {
    transcriber: null,
    gcpProjectId: "test",
    gcpLocation: "us-central1",
    gcpModel: "gemini-2.5-flash-lite",
    gcsBucket: "bucket",
    gcsPrefix: "prefix/",
    apiVersion: "v1",
    gcpApiKey: "test-key",
    geminiStdModel: "gemini-2.5-flash-lite",
    googleApiKey: "",
  };
  // Should not throw
  validateConfig(cfg);
});

Deno.test("validateConfig passes with gemini key", () => {
  const cfg = {
    transcriber: null,
    gcpProjectId: "",
    gcpLocation: "",
    gcpModel: "",
    gcsBucket: "",
    gcsPrefix: "",
    apiVersion: "",
    gcpApiKey: "",
    geminiStdModel: "gemini-2.5-flash-lite",
    googleApiKey: "test-key",
  };
  // Should not throw
  validateConfig(cfg);
});
