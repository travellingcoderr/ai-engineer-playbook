import mongoose from 'mongoose';
import { ClaimStatus } from '../common/types';
import { ClaimSnapshot } from './claim.schema';

export interface ClaimState {
  id: string;
  status: ClaimStatus;
  procedures: Array<{
    code: string;
    description: string;
    toothNumber?: number;
  }>;
  missingDocuments: string[];
  denialReason?: string;
  notes: string[];
}

/**
 * ClaimSnapshotTool mimics the GOLD-AI-API loan-snapshot-tool.
 * It provides "Structured State" to the AI, explaining why a claim is 'stuck'.
 * Local Snapshots are now PERSISTED in MongoDB.
 */
export class ClaimSnapshotTool {
  private mockClaims: Map<string, ClaimState> = new Map();

  constructor() {
    this.seedData();
    this.ensureConnected();
  }

  private async ensureConnected() {
    if (mongoose.connection.readyState === 0) {
      console.log('📡 Connecting to MongoDB for Snapshots...');
      await mongoose.connect(process.env.MONGODB_URL || 'mongodb://mongodb:27017/insuredoc');
    }
  }

  private seedData() {
    this.mockClaims.set('CLAIM-123', {
      id: 'CLAIM-123',
      status: ClaimStatus.STUCK,
      procedures: [{ code: 'D2740', description: 'Porcelain Crown', toothNumber: 30 }],
      missingDocuments: ['Pre-operative X-ray (Tooth 30)'],
      denialReason: 'Pending Clinical Review: Missing required X-ray.',
      notes: [
        'Procedure code D2740 requires an X-ray per policy guidelines.',
        'Sent auto-notification to patient on 2024-03-20.'
      ]
    });
  }

  async getClaimSnapshot(claimId: string): Promise<string> {
    await this.ensureConnected();
    const claimData = this.mockClaims.get(claimId);
    
    if (!claimData) return `Claim ${claimId} not found.`;

    // UPSERT (Persistence)
    console.log(`💾 Persisting Analysis Snapshot for ${claimId} to MongoDB...`);
    await ClaimSnapshot.findOneAndUpdate(
      { claimId: claimData.id },
      { 
        status: claimData.status,
        procedures: claimData.procedures,
        missingDocuments: claimData.missingDocuments,
        denialReason: claimData.denialReason,
        notes: claimData.notes
      },
      { upsert: true, new: true }
    );

    return `
CLAIM SNAPSHOT (${claimData.id})
Status: ${claimData.status}
Procedures: ${claimData.procedures.map(p => `${p.description} (${p.code}) on Tooth ${p.toothNumber}`).join(', ')}
Missing Docs: ${claimData.missingDocuments.join(', ') || 'None'}
Denial Reason: ${claimData.denialReason || 'N/A'}
Recent Notes: ${claimData.notes.slice(-1)[0]}
    `.trim();
  }
}
