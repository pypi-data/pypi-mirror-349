import { dev } from "$app/environment";

export const BASE_URL = dev
    ? "http://localhost:6680"
    : (globalThis?.location?.origin ?? "");
export const WS_URL = BASE_URL.replace(/^http/, "ws");

export const SEPARATOR = "•";
