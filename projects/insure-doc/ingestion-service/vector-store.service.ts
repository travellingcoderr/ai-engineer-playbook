import { SearchClient, AzureKeyCredential } from '@azure/search-documents';
import { RawChunk } from '../common/types';

export interface IVectorStore {
  uploadDocuments(chunks: RawChunk[], embeddings: number[][], documentId: string): Promise<void>;
  search(query: string, vector: number[], top?: number): Promise<any>;
}

/**
 * AzureVectorStore: Implementation for Azure AI Search.
 */
export class AzureVectorStore implements IVectorStore {
  private client: SearchClient<any>;

  constructor(endpoint: string, apiKey: string, indexName: string) {
    this.client = new SearchClient(endpoint, indexName, new AzureKeyCredential(apiKey));
  }

  async uploadDocuments(chunks: RawChunk[], embeddings: number[][], documentId: string) {
    const documents = chunks.map((chunk, index) => ({
      id: `${documentId}-${index}`,
      content: chunk.text,
      contentVector: embeddings[index],
      metadata: JSON.stringify(chunk.metadata),
    }));
    await this.client.uploadDocuments(documents);
  }

  async search(query: string, vector: number[], top = 5) {
    return await this.client.search(query, {
      vectorQueries: [{ kind: 'vector', vector, fields: ['contentVector'], kNearestNeighborsCount: top }],
      top,
    });
  }
}

/**
 * ChromaVectorStore: Implementation for local ChromaDB.
 */
export class ChromaVectorStore implements IVectorStore {
  // Using a simplified implementation for local dev
  async uploadDocuments(chunks: RawChunk[], embeddings: number[][], documentId: string) {
    console.log(`[ChromaDB] Simulating upload of ${chunks.length} chunks for ${documentId}`);
  }

  async search(query: string, vector: number[], top = 5) {
    console.log(`[ChromaDB] Simulating hybrid search for: ${query}`);
    return { results: [] };
  }
}
