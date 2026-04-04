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
  constructor() {
    this.ensureConnected();
  }

  private async ensureConnected() {
    if (mongoose.connection.readyState === 0) {
      console.log('📡 Connecting to MongoDB for Snapshots...');
      await mongoose.connect(process.env.MONGODB_URL || 'mongodb://mongodb:27017/insuredoc');
    }
  }

  /**
   * upsertClaim: Saves a new claim record to MongoDB.
   */
  async upsertClaim(data: { id: string; patientName?: string; status: ClaimStatus; procedures: any[] }) {
    await this.ensureConnected();
    console.log(`💾 Persisting User-Entered Claim ${data.id} to MongoDB...`);
    
    return await ClaimSnapshot.findOneAndUpdate(
      { claimId: data.id },
      { 
        patientName: data.patientName,
        status: data.status,
        procedures: data.procedures,
        updatedAt: new Date()
      },
      { upsert: true, new: true }
    );
  }

  /**
   * getClaimSnapshot: Retrieves structured state for the AI.
   * Checks MongoDB first.
   */
  async getClaimSnapshot(claimId: string): Promise<string> {
    await this.ensureConnected();
    
    // 1. Try to find in DB
    const dbClaim = await ClaimSnapshot.findOne({ claimId });
    
    if (!dbClaim) {
      return `Claim ${claimId} not found in the database. Please ensure it has been created.`;
    }

    return `
CLAIM SNAPSHOT (${dbClaim.claimId})
Patient: ${dbClaim.patientName || 'N/A'}
Status: ${dbClaim.status}
Procedures: ${dbClaim.procedures.map(p => `${p.description} (${p.code})`).join(', ')}
Missing Docs: ${dbClaim.missingDocuments?.join(', ') || 'None identified yet'}
Denial Reason: ${dbClaim.denialReason || 'Pending analysis'}
Recent Notes: ${dbClaim.notes?.slice(-1)[0] || 'No notes available'}
    `.trim();
  }
}
