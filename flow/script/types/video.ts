/**
 * Domain types for video/subtitle processing.
 */

export interface VideoMeta {
  id: string;
  title: string;
  url: string;
  index: number;
  duration?: number;
}

export interface SubtitleEntry {
  index: number;
  start: string;
  end: string;
  text: string;
}

export interface CourseConfig {
  name: string;
  playlistUrl: string;
  source: "youtube" | "bilibili";
  lang: string;
}
