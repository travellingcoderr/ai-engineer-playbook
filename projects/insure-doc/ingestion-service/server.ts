import express from 'express';
import dotenv from 'dotenv';
import multer from 'multer';
import pdf = require('pdf-parse');
import { validateEntraToken } from '../common/auth.middleware';
import { ChunkingService } from './chunking.service';
import { AzureVectorStore, QdrantVectorStore } from './vector-store.service';
import { AzureOpenAIEmbeddings } from '@langchain/openai';
import swaggerUi from 'swagger-ui-express';
import swaggerJsdoc from 'swagger-jsdoc';

dotenv.config();

const app = express();
const upload = multer({ storage: multer.memoryStorage() });
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

// INITIALIZE EMBEDDING MODEL
const embeddings = new AzureOpenAIEmbeddings({
  azureOpenAIApiKey: process.env.AZURE_OPENAI_API_KEY,
  azureOpenAIApiInstanceName: process.env.AZURE_OPENAI_INSTANCE_NAME,
  azureOpenAIApiDeploymentName: process.env.AZURE_OPENAI_EMBEDDING_DEPLOYMENT || 'text-embedding-3-small',
  azureOpenAIApiVersion: process.env.AZURE_OPENAI_API_VERSION,
});

// INITIALIZE VECTOR STORE PROVIDER
let vectorStore: any;
if (process.env.VECTOR_STORE_PROVIDER === 'qdrant') {
  console.log('🚀 Using Local Qdrant Vector Store');
  vectorStore = new QdrantVectorStore(
    process.env.QDRANT_URL || 'http://qdrant:6333',
    process.env.QDRANT_COLLECTION || 'insurance-policies'
  );
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
 *               headings:
 *                 type: array
 *                 items:
 *                   type: string
 *     responses:
 *       200:
 *         description: Document processed successfully
 */
app.post('/api/v1/ingestion', validateEntraToken, async (req, res) => {
  try {
    const { content, title, headings } = req.body;
    
    if (!content) return res.status(400).json({ error: 'Content is required' });

    console.log(`📄 Processing document: ${title || 'Untitled'}`);
    const chunks = await chunkingService.chunkDocument(content, title, headings);
    
    // GENERATE REAL EMBEDDINGS
    console.log(`🧠 Generating embeddings for ${chunks.length} chunks...`);
    const chunkTexts = chunks.map(c => c.text);
    const vectorEmbeddings = await embeddings.embedDocuments(chunkTexts);
    
    await vectorStore.uploadDocuments(chunks, vectorEmbeddings, title || 'unknown');
    
    res.json({ message: 'Document processed successfully', chunkCount: chunks.length });
  } catch (error) {
    console.error('Ingestion Service Error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

/**
 * @openapi
 * /api/v1/ingestion/pdf:
 *   post:
 *     summary: Ingest a PDF document for AI processing
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         multipart/form-data:
 *           schema:
 *             type: object
 *             properties:
 *               file:
 *                 type: string
 *                 format: binary
 *     responses:
 *       200:
 *         description: PDF processed successfully
 */
app.post('/api/v1/ingestion/pdf', validateEntraToken, upload.single('file'), async (req, res) => {
  try {
    if (!req.file) return res.status(400).json({ error: 'No file uploaded' });

    console.log(`📄 Extracting text from PDF: ${req.file.originalname}`);
    const data = await pdf(req.file.buffer);
    const content = data.text;
    const title = req.file.originalname.replace('.pdf', '');

    if (!content.trim()) return res.status(400).json({ error: 'PDF content is empty' });

    console.log(`📝 Chunking and embedding ${content.length} characters...`);
    const chunks = await chunkingService.chunkDocument(content, title, []);
    
    const chunkTexts = chunks.map(c => c.text);
    const vectorEmbeddings = await embeddings.embedDocuments(chunkTexts);
    
    await vectorStore.uploadDocuments(chunks, vectorEmbeddings, title);
    
    res.json({ 
      message: 'PDF processed successfully', 
      chunkCount: chunks.length,
      pageCount: data.numpages 
    });
  } catch (error) {
    console.error('PDF Ingestion Error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

/**
 * @openapi
 * /api/v1/search:
 *   post:
 *     summary: Search for policy information using vectorized query
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               query:
 *                 type: string
 *     responses:
 *       200:
 *         description: Search results retrieved successfully
 */
app.post('/api/v1/search', validateEntraToken, async (req, res) => {
  try {
    const { query } = req.body;
    if (!query) return res.status(400).json({ error: 'Query is required' });

    console.log(`🔍 Searching for: "${query}"`);
    const queryVector = await embeddings.embedQuery(query);
    const results = await vectorStore.search(query, queryVector);
    
    res.json({ results });
  } catch (error) {
    console.error('Search Service Error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

const PORT = process.env.INGESTION_PORT || 3001;
app.listen(PORT, () => console.log(`Ingestion Service running on port ${PORT}`));
