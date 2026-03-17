import http from 'k6/http';
import { check, sleep } from 'k6';

/**
 * Phase 4: Performance Stress Test Script
 * 
 * This script simulates multiple virtual users (VUs) hitting the 
 * Resilient Gateway concurrently to validate load balancing and 
 * multi-region failover stability.
 */

export const options = {
    // Number of virtual users to simulate
    vus: 10,
    // Duration of the stress test
    duration: '30s',
    // Thresholds for failure (Latency vs Success Rate)
    thresholds: {
        http_req_duration: ['p(95)<2000'], // 95% of requests must complete below 2s
        http_req_failed: ['rate<0.05'],    // Error rate must be below 5%
    },
};

export default function () {
    const url = 'http://localhost:8006/v1/complete';
    const payload = JSON.stringify({
        prompt: 'Generate a short summary of k6 load testing.',
        model: 'gpt-4o'
    });

    const params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    // Execute POST request to the Gateway
    const res = http.post(url, payload, params);

    // Verify the response status is 200 (Success)
    check(res, {
        'status is 200': (r) => r.status === 200,
        'has completion content': (r) => r.json().content !== undefined,
    });

    // Pacing: Wait 1 second between requests
    sleep(1);
}
