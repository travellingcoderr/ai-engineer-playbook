import express from 'express';
import dotenv from 'dotenv';
import { validateEntraToken } from '../common/auth.middleware';
import { app as orchestrator } from './agent';
import { HumanMessage } from '@langchain/core/messages';
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
      title: 'InsureDoc Orchestrator API',
      version: '1.0.0',
      description: 'AI Multi-Agent Orchestrator for Insurance Claim analysis.',
    },
    servers: [{ url: 'http://localhost:3003' }],
    components: {
      securitySchemes: {
        bearerAuth: { type: 'http', scheme: 'bearer', bearerFormat: 'JWT' }
      }
    },
    security: [{ bearerAuth: [] }]
  },
  apis: ['./orchestrator-service/**/*.ts'], // Files containing annotations
};

const swaggerDocs = swaggerJsdoc(swaggerOptions);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocs));

/**
 * @openapi
 * /api/v1/chat:
 *   post:
 *     summary: Ask a question to the AI Insurance Agent
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               message:
 *                 type: string
 *                 description: The user query (e.g., 'Why is CLAIM-123 stuck?')
 *     responses:
 *       200:
 *         description: AI response retrieved successfully
 */
app.post('/api/v1/chat', validateEntraToken, async (req, res) => {
  try {
    const { message } = req.body;
    
    if (!message) return res.status(400).json({ error: 'Message is required' });

    const result = await orchestrator.invoke({
      messages: [{ role: 'user', content: message }],
    });

    // Find the last message that actually has text content (skipping tool call messages)
    const messages = result.messages;
    let finalContent = '';
    
    for (let i = messages.length - 1; i >= 0; i--) {
      if (messages[i].content && typeof messages[i].content === 'string' && messages[i].content.trim() !== '') {
        finalContent = messages[i].content;
        break;
      }
    }

    res.json({ response: finalContent });
  } catch (error) {
    console.error('Orchestrator Error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

const PORT = process.env.ORCHESTRATOR_PORT || 3003;
app.listen(PORT, () => console.log(`Orchestrator Service running on port ${PORT}`));
