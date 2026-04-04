import { StateGraph, MessagesAnnotation } from '@langchain/langgraph';
import { ChatOpenAI } from '@langchain/openai';
import { ToolNode } from '@langchain/langgraph/prebuilt';
import { ClaimSnapshotTool } from '../claim-service/stuck-claim-tool';
import { DynamicStructuredTool } from '@langchain/core/tools';
import { z } from 'zod';

const claimTool = new ClaimSnapshotTool();

// 1. Define Tools
const checkClaimStatus = new DynamicStructuredTool({
  name: 'checkClaimStatus',
  description: 'Use this tool to get the real-time status of a dental claim.',
  schema: z.object({
    claimId: z.string().describe('The ID of the dental claim (e.g., CLAIM-123)'),
  }),
  func: async ({ claimId }: { claimId: string }) => {
    return await claimTool.getClaimSnapshot(claimId);
  },
});

const searchInsurancePolicy = new DynamicStructuredTool({
  name: 'searchInsurancePolicy',
  description: 'Use this tool to search through insurance benefit booklets.',
  schema: z.object({
    query: z.string().describe('The dental procedure or benefit to lookup.'),
  }),
  func: async ({ query }: { query: string }) => {
    return `Policy lookup for "${query}": Procedural D2740 Porcelain Crowns require pre-operative x-rays.`;
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
