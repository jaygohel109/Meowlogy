-- Supabase Database Schema for Cat Facts Application
-- Run this in your Supabase SQL Editor

-- Create cat_facts table
CREATE TABLE IF NOT EXISTS cat_facts (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    fact TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    likes_count INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE
);

-- Create fact_likes table for future like functionality
CREATE TABLE IF NOT EXISTS fact_likes (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    fact_id UUID REFERENCES cat_facts(id) ON DELETE CASCADE,
    user_id UUID, -- Will be used when you add authentication
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(fact_id, user_id)
);

-- Enable Row Level Security on both tables
ALTER TABLE cat_facts ENABLE ROW LEVEL SECURITY;
ALTER TABLE fact_likes ENABLE ROW LEVEL SECURITY;

-- Create policies to allow all operations for now (you can restrict this later)
CREATE POLICY "Allow all operations on cat_facts" ON cat_facts FOR ALL USING (true);
CREATE POLICY "Allow all operations on fact_likes" ON fact_likes FOR ALL USING (true);

-- Create function to update likes_count automatically
CREATE OR REPLACE FUNCTION update_likes_count()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE cat_facts SET likes_count = likes_count + 1 WHERE id = NEW.fact_id;
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE cat_facts SET likes_count = likes_count - 1 WHERE id = OLD.fact_id;
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Create trigger for automatic likes_count updates
DROP TRIGGER IF EXISTS update_likes_count_trigger ON fact_likes;
CREATE TRIGGER update_likes_count_trigger
    AFTER INSERT OR DELETE ON fact_likes
    FOR EACH ROW EXECUTE FUNCTION update_likes_count();

-- Create function to get random fact (for better performance)
CREATE OR REPLACE FUNCTION get_random_fact()
RETURNS TABLE (
    id UUID,
    fact TEXT,
    created_at TIMESTAMP WITH TIME ZONE,
    likes_count INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT cf.id, cf.fact, cf.created_at, cf.likes_count
    FROM cat_facts cf
    WHERE cf.is_active = TRUE
    ORDER BY RANDOM()
    LIMIT 1;
END;
$$ LANGUAGE plpgsql;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_cat_facts_active ON cat_facts(is_active);
CREATE INDEX IF NOT EXISTS idx_cat_facts_created_at ON cat_facts(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_fact_likes_fact_id ON fact_likes(fact_id);
CREATE INDEX IF NOT EXISTS idx_fact_likes_user_id ON fact_likes(user_id);

-- Insert some sample cat facts
INSERT INTO cat_facts (fact) VALUES
('Cats spend 70% of their lives sleeping.'),
('A group of cats is called a "clowder."'),
('Cats have over 20 muscles that control their ears.'),
('A cat''s purr vibrates at a frequency that promotes bone healing.'),
('Cats can rotate their ears 180 degrees.'),
('The average cat sleeps 16-18 hours per day.'),
('Cats have a third eyelid called a nictitating membrane.'),
('A cat''s whiskers help them determine if they can fit through a space.'),
('Cats can jump up to 6 times their body length.'),
('Cats have over 200 million odor-sensitive cells in their noses.')
ON CONFLICT (fact) DO NOTHING;

-- Create a view for active facts with like counts
CREATE OR REPLACE VIEW active_cat_facts AS
SELECT 
    cf.id,
    cf.fact,
    cf.created_at,
    cf.likes_count,
    cf.updated_at
FROM cat_facts cf
WHERE cf.is_active = TRUE
ORDER BY cf.created_at DESC; 