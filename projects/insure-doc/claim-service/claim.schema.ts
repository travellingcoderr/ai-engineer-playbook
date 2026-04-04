import mongoose, { Schema, Document } from 'mongoose';
import { ClaimStatus } from '../common/types';

export interface IClaimSnapshot extends Document {
  claimId: string;
  status: ClaimStatus;
  procedures: Array<{
    code: string;
    description: string;
    toothNumber?: number;
  }>;
  missingDocuments: string[];
  denialReason?: string;
  notes: string[];
  updatedAt: Date;
}

const ClaimSnapshotSchema: Schema = new Schema({
  claimId: { type: String, required: true, unique: true },
  status: { type: String, required: true, enum: Object.values(ClaimStatus) },
  procedures: [{
    code: { type: String, required: true },
    description: { type: String, required: true },
    toothNumber: { type: Number }
  }],
  missingDocuments: [{ type: String }],
  denialReason: { type: String },
  notes: [{ type: String }],
  updatedAt: { type: Date, default: Date.now }
});

// Update the updatedAt timestamp on every save
ClaimSnapshotSchema.pre<IClaimSnapshot>('save', function(next) {
  this.updatedAt = new Date();
  next();
});

export const ClaimSnapshot = mongoose.model<IClaimSnapshot>('Claim', ClaimSnapshotSchema);
