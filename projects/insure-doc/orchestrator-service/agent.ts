import { StateGraph, MessagesAnnotation } from '@langchain/langgraph';
import { ChatOpenAI } from '@langchain/openai';
import { ToolNode } from '@langchain/langgraph/prebuilt';
import { DynamicStructuredTool } from '@langchain/core/tools';
import { z } from 'zod';
import dotenv from 'dotenv';

dotenv.config();
const checkClaimStatus = new DynamicStructuredTool({
  name: 'checkClaimStatus',
  description: 'Use this tool to get the real-time status and analysis of a dental claim, including why it might be stuck.',
  schema: z.object({
    claimId: z.string().describe('The ID of the dental claim (e.g., CLAIM-123)'),
  }),
  func: async ({ claimId }: { claimId: string }) => {
    try {
      const claimServiceUrl = process.env.CLAIM_SERVICE_URL || 'http://claim-service:3002';
      const response = await fetch(`${claimServiceUrl}/api/v1/claims/${claimId}`);

      if (!response.ok) return `Error fetching claim: ${await response.text()}`;
      
      const data = await response.json();
      return JSON.stringify(data, null, 2);
    } catch (err) {
      return `Failed to connect to claim service: ${(err as Error).message}`;
    }
  },
});

const searchInsurancePolicy = new DynamicStructuredTool({
  name: 'searchInsurancePolicy',
  description: 'Use this tool to search through insurance benefit booklets.',
  schema: z.object({
    query: z.string().describe('The dental procedure or benefit to lookup.'),
  }),
  func: async ({ query }: { query: string }) => {
    try {
      const ingestionUrl = process.env.INGESTION_URL || 'http://ingestion-service:3001';
      const response = await fetch(`${ingestionUrl}/api/v1/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer mock-token'
        },
        body: JSON.stringify({ query })
      });

      if (!response.ok) return `Error searching policy: ${await response.text()}`;
      
      const { results } = await response.json();
      if (!results?.length) return `No policy found for "${query}".`;
      
      return results.map((r: any) => r.text).join('\n---\n');
    } catch (err) {
      return `Failed to connect to policy service: ${(err as Error).message}`;
    }
  },
});

const tools = [checkClaimStatus, searchInsurancePolicy];

// 2. Robust Model Initialization helper
const getModel = () => {
  const apiKey = process.env.AZURE_OPENAI_API_KEY;
  const instanceName = process.env.AZURE_OPENAI_INSTANCE_NAME;

  if (!apiKey || apiKey === 'your-api-key' || !instanceName || instanceName === 'your-instance-name') {
    throw new Error('MISSING_AZURE_CONFIG: Please update your projects/insure-doc/.env file with a real AZURE_OPENAI_API_KEY and AZURE_OPENAI_INSTANCE_NAME.');
  }

  return new ChatOpenAI({ 
    azureOpenAIApiKey: apiKey,
    azureOpenAIApiInstanceName: instanceName,
    azureOpenAIApiDeploymentName: process.env.AZURE_OPENAI_DEPLOYMENT || 'gpt-4o',
    azureOpenAIApiVersion: process.env.AZURE_OPENAI_API_VERSION || '2024-02-01',
    temperature: 0
  }).bind({
    tools: tools
  });
};

// 3. Modern LangGraph 0.2.x / 0.3.x flow
const workflow = new StateGraph(MessagesAnnotation)
  .addNode('agent', async (state: typeof MessagesAnnotation.State) => {
    const model = getModel();
    console.log('🤖 AI Agent Turn: Processing', state.messages.length, 'messages...');
    const result = await model.invoke(state.messages);
    
    // DIAGNOSTIC LOGGING
    console.log('🔄 Raw Model Result:', JSON.stringify({
      content: result.content,
      tool_calls: (result as any).tool_calls,
      finish_reason: (result as any).response_metadata?.finish_reason,
    }, null, 2));
    
    if ((result as any).tool_calls?.length) {
      console.log('🛠️  AI Identifies Tool Call:', (result as any).tool_calls.map((tc: any) => tc.name).join(', '));
    } else {
      console.log('💬 AI Natural Language Response:', result.content.toString().slice(0, 50), '...');
    }
    
    return { messages: [result] };
  })
  .addNode('tools', new ToolNode(tools))
  .addEdge('__start__', 'agent')
  .addConditionalEdges('agent', (state) => {
    const lastMsg = state.messages[state.messages.length - 1];
    return (lastMsg as any).tool_calls?.length ? 'tools' : '__end__';
  })
  .addEdge('tools', 'agent');

export const app = workflow.compile();
