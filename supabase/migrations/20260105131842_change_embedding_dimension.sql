-- Change embedding dimension from 1536 to 384 to match HuggingFace model

-- Step 1: Drop the existing HNSW index (required before altering column)
DROP INDEX IF EXISTS document_chunks_embedding_hnsw_idx;

-- Step 2: Delete existing chunks with 1536-dim embeddings (if any)
-- WARNING: This will delete all existing document chunks!
DELETE FROM document_chunks;

-- Step 3: Alter the embedding column to use vector(384)
ALTER TABLE document_chunks 
ALTER COLUMN embedding TYPE vector(384);

-- Step 4: Recreate the HNSW index with the new dimension
CREATE INDEX document_chunks_embedding_hnsw_idx 
ON document_chunks 
USING hnsw (embedding vector_ip_ops);
