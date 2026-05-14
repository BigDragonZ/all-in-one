/**
 * Transcription service configuration.
 * Fault-tolerant chain: gcp-vertex -> gemini
 */

/** Transcription backend type */
export type TranscriberBackend = "gcp-vertex" | "gemini";

/** Configuration loaded from environment */
export interface TranscribeConfig {
  /** Explicit backend choice; null = auto-failover */
  transcriber: TranscriberBackend | null;

  // GCP Vertex AI
  gcpProjectId: string;
  gcpLocation: string;
  gcpModel: string;
  gcsBucket: string;
  gcsPrefix: string;
  apiVersion: string;
  gcpApiKey: string;

  // Gemini Standard API (fallback)
  geminiStdModel: string;
  googleApiKey: string;
}

function getEnv(key: string, fallback = ""): string {
  return Deno.env.get(key) || fallback;
}

export function loadConfig(): TranscribeConfig {
  const explicit = getEnv("TRANSCRIBER") as TranscriberBackend | "";

  return {
    transcriber: explicit === "gcp-vertex" || explicit === "gemini"
      ? explicit
      : null,

    gcpProjectId: getEnv("GCP_PROJECT_ID", "gen-lang-client-0385617544"),
    gcpLocation: getEnv("GCP_LOCATION", "us-central1"),
    gcpModel: getEnv("GCP_MODEL", "gemini-2.5-flash-lite"),
    gcsBucket: getEnv("GCS_BUCKET", "hermes_brain"),
    gcsPrefix: getEnv("GCS_PREFIX", "audio_jobs/"),
    apiVersion: getEnv("API_VERSION", "v1"),
    gcpApiKey: getEnv("gcp-vertex-key", ""),

    geminiStdModel: getEnv("GEMINI_STD_MODEL", "gemini-2.5-flash-lite"),
    googleApiKey: getEnv("GEMINI_API_KEY", ""),
  };
}

/** Validate that at least one backend has credentials */
export function validateConfig(cfg: TranscribeConfig): void {
  const hasVertex = cfg.gcpApiKey.length > 0;
  const hasGemini = cfg.googleApiKey.length > 0;

  if (!hasVertex && !hasGemini) {
    throw new Error(
      "No transcription credentials found. " +
        "Set gcp-vertex-key or GEMINI_API_KEY environment variable.",
    );
  }
}
