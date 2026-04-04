import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import { validateEntraToken } from '../common/auth.middleware';
import { app as orchestrator } from './agent';
import swaggerUi from 'swagger-ui-express';
import swaggerJsdoc from 'swagger-jsdoc';

dotenv.config();

const app = express();
app.use(cors());
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
  // Existing non-streaming logic for backward compatibility
  try {
    const { message } = req.body;
    if (!message) return res.status(400).json({ error: 'Message is required' });

    const result = await orchestrator.invoke({
      messages: [{ role: 'user', content: message }],
    });

    const messages = result.messages;
    let finalContent = '';
    for (let i = messages.length - 1; i >= 0; i--) {
      const msg = messages[i];
      if (msg.content && typeof msg.content === 'string' && msg.content.trim() !== '') {
        finalContent = msg.content;
        break;
      }
    }

    res.json({ 
      response: finalContent,
      messages: messages.map((m: any) => ({
        role: m._getType(),
        content: m.content,
        tool_calls: m.tool_calls
      }))
    });
  } catch (error) {
    console.error('Orchestrator Error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

/**
 * @openapi
 * /api/v1/chat/stream:
 *   get:
 *     summary: Stream AI response with real-time events
 *     parameters:
 *       - in: query
 *         name: message
 *         required: true
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: SSE stream of AI events
 */
app.get('/api/v1/chat/stream', async (req, res) => {
  try {
    const { message } = req.query;
    if (!message) return res.status(400).send('Message required');

    res.writeHead(200, {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
      'Access-Control-Allow-Origin': '*'
    });

    const eventStream = await orchestrator.streamEvents(
      { messages: [{ role: 'user', content: message as string }] },
      { version: 'v2' }
    );

    for await (const event of eventStream) {
      const eventType = event.event;
      
      if (eventType === 'on_chat_model_stream') {
        const content = event.data.chunk.content;
        if (content) {
          res.write(`data: ${JSON.stringify({ type: 'content', delta: content })}\n\n`);
        }
      } else if (eventType === 'on_tool_start') {
        res.write(`data: ${JSON.stringify({ type: 'tool_start', tool: event.name })}\n\n`);
      } else if (eventType === 'on_tool_end') {
        res.write(`data: ${JSON.stringify({ type: 'tool_end', tool: event.name, output: event.data.output })}\n\n`);
      }
    }

    res.write('data: [DONE]\n\n');
    res.end();
  } catch (error) {
    console.error('Streaming Error:', error);
    res.end();
  }
});

const PORT = process.env.ORCHESTRATOR_PORT || 3003;
app.listen(PORT, () => console.log(`Orchestrator Service running on port ${PORT}`));
