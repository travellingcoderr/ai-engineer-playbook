import { app } from './orchestrator/agent';
import { HumanMessage } from '@langchain/core/messages';
import * as dotenv from 'dotenv';

dotenv.config();

/**
 * InsureDoc Final Verification Demo
 * Demonstrates the "Secret Sauce" logic: 
 * Combining Policy Knowledge + Live Claim State.
 */
async function runDemo() {
  console.log('--- InsureDoc AI Assistant Demo ---');
  
  const query = "Why is my crown claim CLAIM-123 stuck? Also, what are the policy requirements for crowns?";
  console.log(`User: ${query}`);

  const initialState = {
    messages: [new HumanMessage(query)],
  };

  const result = await app.invoke(initialState);
  const finalMessage = result.messages[result.messages.length - 1];

  console.log('\nAI Response:');
  console.log(finalMessage.content);
}

runDemo().catch(console.error);
