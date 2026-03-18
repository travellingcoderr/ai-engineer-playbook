# mortgage-bot Database Schema

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Knowledge Documents Table
CREATE TABLE IF NOT EXISTS knowledge_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    description TEXT,
    source_type TEXT NOT NULL,
    blob_uri TEXT,
    mime_type TEXT,
    status TEXT NOT NULL DEFAULT 'draft',
    version INTEGER DEFAULT 1,
    tags TEXT[],
    audiences TEXT[],
    language TEXT DEFAULT 'en',
    author TEXT,
    expiry_date TIMESTAMP WITH TIME ZONE,
    priority INTEGER DEFAULT 0,
    hash TEXT UNIQUE NOT NULL,
    file_size INTEGER,
    word_count INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    published_at TIMESTAMP WITH TIME ZONE,
    metadata JSONB DEFAULT '{}'
);

-- Knowledge Chunks Table
CREATE TABLE IF NOT EXISTS knowledge_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES knowledge_documents(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    type TEXT NOT NULL DEFAULT 'text',
    tokens INTEGER NOT NULL,
    embedding vector(1536),
    heading_path TEXT[],
    section_anchor TEXT,
    start_offset INTEGER,
    end_offset INTEGER,
    hash TEXT UNIQUE NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Loans Table
CREATE TABLE IF NOT EXISTS loans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    loan_id TEXT NOT NULL UNIQUE,
    borrower_name TEXT NOT NULL,
    property_address TEXT,
    loan_type TEXT,
    loan_amount DOUBLE PRECISION,
    status TEXT NOT NULL DEFAULT 'new',
    milestone TEXT NOT NULL DEFAULT 'application',
    assigned_officer TEXT,
    external_loan_id TEXT,
    source_system TEXT NOT NULL DEFAULT 'internal',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Support Tickets Table
CREATE TABLE IF NOT EXISTS support_tickets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    external_id TEXT UNIQUE,
    user_id TEXT NOT NULL,
    user_email TEXT NOT NULL,
    user_name TEXT NOT NULL,
    subject TEXT NOT NULL,
    description TEXT NOT NULL,
    category TEXT NOT NULL,
    severity TEXT NOT NULL DEFAULT 'medium',
    status TEXT NOT NULL DEFAULT 'open',
    tags TEXT[],
    loan_id TEXT,
    assigned_to TEXT,
    resolved_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    context JSONB DEFAULT '{}'
);

-- Support Comments Table
CREATE TABLE IF NOT EXISTS support_comments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticket_id UUID REFERENCES support_tickets(id) ON DELETE CASCADE,
    author_id TEXT NOT NULL,
    author_name TEXT NOT NULL,
    author_type TEXT NOT NULL,
    content TEXT NOT NULL,
    is_public BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for search
CREATE INDEX IF NOT EXISTS idx_knowledge_chunks_embedding ON knowledge_chunks USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX IF NOT EXISTS idx_loans_loan_id ON loans(loan_id);
CREATE INDEX IF NOT EXISTS idx_loans_status ON loans(status);
CREATE INDEX IF NOT EXISTS idx_support_tickets_status ON support_tickets(status);
CREATE INDEX IF NOT EXISTS idx_support_tickets_user_id ON support_tickets(user_id);
