import DocumentIntelligence, { isUnexpected } from "@azure-rest/ai-document-intelligence";
import { AzureKeyCredential } from "@azure/core-auth";
import dotenv from 'dotenv';

dotenv.config();

/**
 * DocIntelService leverages Azure AI Document Intelligence (Prebuilt Layout)
 * to extract specialized Markdown layout from PDFs.
 * This is the 'Senior' way of ensuring table-of-contents and multi-column tables 
 * are preserved for RAG.
 */
export class DocIntelService {
  private client: any;

  constructor() {
    const endpoint = process.env.AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT;
    const key = process.env.AZURE_DOCUMENT_INTELLIGENCE_KEY;

    if (!endpoint || !key) {
      console.warn('⚠️  Azure Document Intelligence credentials missing. Smart Ingest will fail.');
      return;
    }

    this.client = DocumentIntelligence(endpoint, new AzureKeyCredential(key));
  }

  async extractMarkdown(fileBuffer: Buffer): Promise<string> {
    if (!this.client) throw new Error("Document Intelligence client NOT initialized.");

    console.log("📑 Azure AI: Analyzing document layout...");
    
    // 1. Start Analysis
    const initialResponse = await this.client.path("/documentModels/{modelId}:analyze", "prebuilt-layout").post({
      contentType: "application/octet-stream",
      body: fileBuffer,
      queryParameters: {
        outputContentFormat: "markdown" // THE KEY FOR RAG
      }
    });

    if (isUnexpected(initialResponse)) throw initialResponse.body.error;

    // 2. Poll for Results
    const operationLocation = initialResponse.headers["operation-location"];
    if (!operationLocation) throw new Error("Azure did not return an operation-location header.");

    console.log(`⏳ Azure AI: Task initiated. Polling status...`);

    let result: any;
    let attempts = 0;
    while (attempts < 60) { // Timeout after 60 seconds
      // We use the full URL from Azure to avoid path-template errors
      const response = await this.client.path(operationLocation).get();
      
      if (isUnexpected(response)) {
        console.error("❌ Azure AI Polling Error Detail:", response.body?.error);
        throw response.body.error;
      }

      const status = response.body.status;
      console.log(`🔄 Azure AI Status: ${status} (Attempt ${attempts + 1})`);

      if (status === "succeeded") {
        result = response.body.analyzeResult;
        break;
      } else if (status === "failed") {
        throw new Error("Azure Document Intelligence Task Failed.");
      }

      attempts++;
      await new Promise(resolve => setTimeout(resolve, 1000));
    }

    if (!result) throw new Error("Azure Document Intelligence timed out or failed to return results.");

    console.log("✅ Azure AI: Layout Extraction Complete.");
    return result.content || "";
  }
}
