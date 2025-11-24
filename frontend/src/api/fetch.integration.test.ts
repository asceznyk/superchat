import { describe, it, expect } from "vitest";
import { streamMockResponse } from "@/api/fetch";

describe("integration: streamMockResponse", () => {
  it("connects to real backend", async () => {
    const { reader, decoder } = await streamMockResponse("hi", "");
    let result = "";
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      result += decoder.decode(value, { stream: true });
    }
    expect(result.length).toBeGreaterThan(0);
    expect(result.includes("This is some")).toBe(true);
  });
});

