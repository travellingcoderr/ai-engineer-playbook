/**
 * Shared types for the InsureDoc AI Assistant.
 */
export enum ClaimStatus {
  SUBMITTED = 'submitted',
  REVIEWING = 'reviewing',
  DENIED = 'denied',
  APPROVED = 'approved',
  STUCK = 'stuck',
  PENDING_INFO = 'pending_info',
}
export enum ChunkType {
  TEXT = 'text',
  TABLE = 'table',
  IMAGE = 'image',
}

export interface RawChunk {
  text: string;
  type: ChunkType;
  metadata: Record<string, any>;
}

export interface DentalPolicy {
  procedureCode: string;
  category: string;
  coinsurance: number;
  requirements: string[]; // e.g., ['X-ray required', 'Pre-auth needed']
}
