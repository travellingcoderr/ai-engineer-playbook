import express from 'express';
import dotenv from 'dotenv';
import { validateEntraToken } from '../common/auth.middleware';
import { ClaimSnapshotTool } from './stuck-claim-tool';
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
      title: 'InsureDoc Claim API',
      version: '1.0.0',
      description: 'Snapshot and stuck-reason analysis service for AI Insurance.',
    },
    servers: [{ url: 'http://localhost:3002' }],
    components: {
      securitySchemes: {
        bearerAuth: { type: 'http', scheme: 'bearer', bearerFormat: 'JWT' }
      }
    },
    security: [{ bearerAuth: [] }]
  },
  apis: ['./claim-service/**/*.ts'], // Files containing annotations
};

const swaggerDocs = swaggerJsdoc(swaggerOptions);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocs));

console.log(`📡 Claim Service initialization (Provider: ${process.env.DB_PROVIDER || 'mock'})`);
const claimTool = new ClaimSnapshotTool();

/**
 * @openapi
 * /api/v1/claims/{id}:
 *   get:
 *     summary: Get a structured snapshot of a claim
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *         description: The unique Claim ID (e.g., CLAIM-123)
 *     responses:
 *       200:
 *         description: Claim snapshot retrieved successfully
 */
app.get('/api/v1/claims/:id', validateEntraToken, async (req, res) => {
  try {
    const snapshot = await claimTool.getClaimSnapshot(req.params.id);
    res.json({ snapshot });
  } catch (error) {
    console.error('Claim Service Error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

const PORT = process.env.CLAIM_PORT || 3002;
app.listen(PORT, () => console.log(`Claim Service running on port ${PORT}`));
