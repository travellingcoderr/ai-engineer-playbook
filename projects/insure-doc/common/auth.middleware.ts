import { Request, Response, NextFunction } from 'express';
import * as jwt from 'jsonwebtoken';
import jwksRsa from 'jwks-rsa';

const client = jwksRsa({
  jwksUri: `https://login.microsoftonline.com/${process.env.AZURE_TENANT_ID}/discovery/v2.0/keys`,
});

function getKey(header: any, callback: any) {
  client.getSigningKey(header.kid, (err, key) => {
    const signingKey = key?.getPublicKey();
    callback(null, signingKey);
  });
}

/**
 * validateEntraToken: Middleware to verify Azure Entra ID (MSAL) Bearer tokens.
 */
export const validateEntraToken = (req: Request, res: Response, next: NextFunction) => {
  const authHeader = req.headers.authorization;

  // LOCAL DEVELOPMENT BYPASS
  if (process.env.AZURE_AUTH_BYPASS === 'true') {
    console.warn('⚠️  Auth Bypass: Proceeding with mock user for development.');
    (req as any).user = { name: 'Dev User', role: 'admin' };
    return next();
  }

  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Missing or invalid Authorization header' });
  }

  const token = authHeader.split(' ')[1];

  jwt.verify(token, getKey, {
    audience: process.env.AZURE_CLIENT_ID,
    issuer: `https://login.microsoftonline.com/${process.env.AZURE_TENANT_ID}/v2.0`,
  }, (err, decoded) => {
    if (err) {
      console.error('JWT Validation Error:', err.message);
      return res.status(401).json({ error: 'Token validation failed' });
    }
    (req as any).user = decoded;
    next();
  });
};
