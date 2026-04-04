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

import { QdrantClient } from '@qdrant/js-client-rest';

/**
 * QdrantVectorStore: Implementation for local Qdrant.
 */
export class QdrantVectorStore implements IVectorStore {
  private client: QdrantClient;
  private collectionName: string;

  constructor(url: string, collectionName: string) {
    this.client = new QdrantClient({ url });
    this.collectionName = collectionName;
  }

  private async ensureCollection() {
    const collections = await this.client.getCollections();
    const exists = collections.collections.some(c => c.name === this.collectionName);
    
    if (!exists) {
      console.log(`🚀 Creating Qdrant Collection: ${this.collectionName}`);
      await this.client.createCollection(this.collectionName, {
        vectors: {
          size: 1536, // Azure OpenAI standard
          distance: 'Cosine'
        }
      });
    }
  }

  async uploadDocuments(chunks: RawChunk[], embeddings: number[][], documentId: string) {
    await this.ensureCollection();
    
    const points = chunks.map((chunk, index) => ({
      id: crypto.randomUUID(),
      vector: embeddings[index],
      payload: {
        text: chunk.text,
        documentId: documentId,
        metadata: chunk.metadata,
      }
    }));

    await this.client.upsert(this.collectionName, {
      wait: true,
      points
    });
    console.log(`✅ Uploaded ${chunks.length} points to Qdrant collection ${this.collectionName}`);
  }

  async search(query: string, vector: number[], top = 5) {
    await this.ensureCollection();
    
    const results = await this.client.search(this.collectionName, {
      vector,
      limit: top,
      with_payload: true
    });

    return results.map(r => ({
      text: r.payload?.text,
      metadata: r.payload?.metadata,
      score: r.score
    }));
  }
}
