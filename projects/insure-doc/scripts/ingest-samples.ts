import * as fs from 'fs';
import * as path from 'path';

const INGESTION_URL = 'http://localhost:3001/api/v1/ingestion';

const policies = [
  { title: 'Crown Coverage (D2740)', content: 'Porcelain crowns (D2740) require a pre-operative X-ray and clinical notes for medical necessity. Covered at 50% after deductible.' },
  { title: 'Root Canal Therapy (D3310)', content: 'Anterior root canals (D3310) are covered at 80%. Multi-rooted teeth require specialist referral if complications exist.' },
  { title: 'Preventive Exams (D0120)', content: 'Periodic exams (D0120) are covered twice per calendar year at 100%. No deductible applies for preventive care.' },
  { title: 'Dental Cleanings (D1110)', content: 'Prophylaxis (D1110) is covered 100% twice per year. 6 months must elapse between appointments.' },
  { title: 'Fillings (D2391)', content: 'Resin-based composite fillings (D2391) are covered on anterior and posterior teeth. Amalgam (Silver) is optional.' },
  { title: 'Deep Cleaning (D4341)', content: 'Scaling and root planing (D4341) requires periodontal charting and at least 4mm pocket depths for coverage.' },
  { title: 'Tooth Extraction (D7140)', content: 'Simple extractions (D7140) of erupted teeth are covered at 80%. Surgical extractions require X-rays.' },
  { title: 'Night Guards (D9944)', content: 'Occlusal guards (D9944) for bruxism are covered once every 3 years. Requires evidence of tooth wear.' },
  { title: 'X-Rays (D0210)', content: 'Full mouth series (D0210) is covered once every 5 years. Bitewing X-rays are covered once per year.' },
  { title: 'Space Maintainers (D1510)', content: 'Fixed space maintainers (D1510) are covered for children under 14 who lose baby teeth prematurely.' },
];

async function ingest() {
  console.log('🚀 Starting ingestion of sample policies...');

  for (const policy of policies) {
    try {
      const response = await fetch(INGESTION_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer mock-token' // Auth bypass is on
        },
        body: JSON.stringify({
          title: policy.title,
          content: policy.content
        })
      });

      if (response.ok) {
        const result = await response.json();
        console.log(`✅ Ingested: ${policy.title} (${result.chunkCount} chunks)`);
      } else {
        const error = await response.text();
        console.error(`❌ Failed to ingest ${policy.title}: ${error}`);
      }
    } catch (err) {
      console.error(`❌ Network error for ${policy.title}:`, (err as Error).message);
    }
  }

  console.log('🏁 Ingestion complete.');
}

ingest();
