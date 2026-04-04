import { TokenTextSplitter } from '@langchain/textsplitters';
import { encodingForModel } from 'js-tiktoken';
import { ChunkType, RawChunk } from '../common/types';

export interface ChunkingConfig {
  maxTokens: number;
  overlapTokens: number;
}

/**
 * ChunkingService mirrors the sophisticated logic of GOLD-AI-API.
 * It uses section-based boundaries and adaptive token sizing.
 */
export class ChunkingService {
  private tokenizer = encodingForModel('gpt-4o');
  private config: ChunkingConfig;

  constructor(config: ChunkingConfig = { maxTokens: 512, overlapTokens: 50 }) {
    this.config = config;
  }

  /**
   * Main entry point for document chunking.
   */
  async chunkDocument(content: string, title: string, headings: string[] = []): Promise<RawChunk[]> {
    const safeHeadings = Array.isArray(headings) ? headings : [];
    const chunks: RawChunk[] = [];

    // Adaptive logic: Insurance procedure tables require denser chunks.
    if (content.toLowerCase().includes('procedure code')) {
      this.config.maxTokens = 256;
      this.config.overlapTokens = 30;
    }

    // 1. Structural Chunks (Based on headings)
    let currentPos = 0;
    for (const heading of safeHeadings) {
      const headingPos = content.indexOf(heading, currentPos);
      if (headingPos !== -1) {
        const section = content.substring(currentPos, headingPos).trim();
        if (section) {
          chunks.push(...await this.splitIntoTokenChunks(section, [title, heading]));
        }
        currentPos = headingPos;
      }
    }

    // 2. Final Window
    const remaining = content.substring(currentPos).trim();
    if (remaining) {
      chunks.push(...await this.splitIntoTokenChunks(remaining, [title]));
    }

    return chunks;
  }

  private async splitIntoTokenChunks(text: string, path: string[]): Promise<RawChunk[]> {
    const splitter = new TokenTextSplitter({
      encodingName: 'cl100k_base',
      chunkSize: this.config.maxTokens,
      chunkOverlap: this.config.overlapTokens,
    });

    const results = await splitter.splitText(text);
    return results.map((t: string) => ({
      text: t.trim(),
      type: ChunkType.TEXT,
      metadata: { headingPath: path },
    }));
  }

  countTokens(text: string): number {
    return this.tokenizer.encode(text).length;
  }
}
