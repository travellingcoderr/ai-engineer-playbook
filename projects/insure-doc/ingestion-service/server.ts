import express from 'express';
import dotenv from 'dotenv';
import { validateEntraToken } from '../common/auth.middleware';
import { ChunkingService } from './chunking.service';
import { VectorStoreService, AzureVectorStore, ChromaVectorStore } from './vector-store.service';
import swaggerUi from 'swagger-ui-express';
import swaggerJsdoc from 'swagger-jsdoc';

dotenv.config();

const app = express();
app.use(express.json());

// SWAGGER CONFIGURATION
const swaggerOptions = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'InsureDoc Ingestion API',
      version: '1.0.0',
      description: 'Document processing and vectorization service for AI Insurance.',
    },
    servers: [{ url: 'http://localhost:3001' }],
    components: {
      securitySchemes: {
        bearerAuth: { type: 'http', scheme: 'bearer', bearerFormat: 'JWT' }
      }
    },
    security: [{ bearerAuth: [] }]
  },
  apis: ['./ingestion-service/**/*.ts'], // Files containing annotations
};

const swaggerDocs = swaggerJsdoc(swaggerOptions);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocs));

const chunkingService = new ChunkingService();

// INITIALIZE VECTOR STORE PROVIDER
let vectorStore;
if (process.env.VECTOR_STORE_PROVIDER === 'chroma') {
  console.log('📦 Using Local ChromaDB Vector Store');
  vectorStore = new ChromaVectorStore();
} else {
  console.log('☁️ Using Azure AI Search Vector Store');
  vectorStore = new AzureVectorStore(
    process.env.AZURE_SEARCH_ENDPOINT!,
    process.env.AZURE_SEARCH_KEY!,
    process.env.AZURE_SEARCH_INDEX!
  );
}

/**
 * @openapi
 * /api/v1/ingestion:
 *   post:
 *     summary: Ingest a document for AI processing
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               content:
 *                 type: string
 *               title:
 *                 type: string
 *     responses:
 *       200:
 *         description: Document processed successfully
 */
app.post('/api/v1/ingestion', validateEntraToken, async (req, res) => {
  try {
    const { content, title, headings } = req.body;
    
    if (!content) return res.status(400).json({ error: 'Content is required' });

    const chunks = await chunkingService.chunkDocument(content, title, headings);
    
    // MOCK EMBEDDINGS (Local Dev)
    const mockEmbeddings = chunks.map(() => new Array(1536).fill(0));
    
    await vectorStore.uploadDocuments(chunks, mockEmbeddings, title || 'unknown');
    
    res.json({ message: 'Document processed successfully', chunkCount: chunks.length });
  } catch (error) {
    console.error('Ingestion Service Error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

const PORT = process.env.INGESTION_PORT || 3001;
app.listen(PORT, () => console.log(`Ingestion Service running on port ${PORT}`));
