import OpenAI from 'openai';
import { RawChunk } from '../common/types';

export interface EmbeddingConfig {
  model: string;
  batchSize: number;
}

/**
 * EmbeddingService mirrors the batching and truncation logic of GOLD-AI-API.
 * It ensures vectors are generated at scale for the knowledge base.
 */
export class EmbeddingService {
  private openai: OpenAI;
  private config: EmbeddingConfig;

  constructor(apiKey: string, config: EmbeddingConfig = { model: 'text-embedding-3-small', batchSize: 20 }) {
    this.openai = new OpenAI({ apiKey });
    this.config = config;
  }

  /**
   * Embeds chunks in batches for efficiency.
   */
  async embedChunks(chunks: RawChunk[]): Promise<number[][]> {
    const embeddings: number[][] = [];

    for (let i = 0; i < chunks.length; i += this.config.batchSize) {
      const batch = chunks.slice(i, i + this.config.batchSize);
      const texts = batch.map(c => c.text);

      const response = await this.openai.embeddings.create({
        model: this.config.model,
        input: texts,
      });

      embeddings.push(...response.data.map(d => d.embedding));
    }

    return embeddings;
  }

  /**
   * Utility for single query embedding (for RAG search).
   */
  async embedQuery(query: string): Promise<number[]> {
    const response = await this.openai.embeddings.create({
      model: this.config.model,
      input: query,
    });
    return response.data[0].embedding;
  }
}
