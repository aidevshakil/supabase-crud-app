# Supabase Python CRUD App

This is a terminal-based Python CRUD application demonstrating how to use Supabase Storage, Database, and Edge Functions.

## Prerequisites

1. A [Supabase](https://supabase.com) project.
2. Python 3.8+ installed.
3. [Supabase CLI](https://supabase.com/docs/guides/cli) installed (optional, to deploy the Edge Function).

## Supabase Setup Instructions

Before running the app, you need to configure your Supabase project:

1. **Storage Bucket**:
   - Go to your Supabase Dashboard -> Storage.
   - Create a new bucket named `user-files`. Make it public if you want easily accessible download URLs, otherwise keep it private.

2. **Database Table**:
   - Go to the SQL Editor in your Supabase Dashboard.
   - Run the following SQL to create the `file_metadata` table:
   ```sql
   CREATE TABLE file_metadata (
       id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
       filename TEXT NOT NULL,
       file_size INTEGER,
       content_type TEXT,
       created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
   );
   ```

3. **Get Credentials**:
   - Go to Project Settings -> API.
   - Copy the `Project URL` and `anon` `public` key.
   - Rename `.env.example` to `.env` and fill in the values:
     ```env
     SUPABASE_URL=your-supabase-url
     SUPABASE_KEY=your-supabase-anon-key
     ```

## Deploying the Edge Function

We have an Edge Function located at `supabase/functions/process-file` that you can deploy to validate file uploads or log metadata.

To deploy it:
1. Login to the CLI: `supabase login`
2. Link your project: `supabase link --project-ref your-project-ref`
3. Deploy the function: `supabase functions deploy process-file --no-verify-jwt`

*(Note: `--no-verify-jwt` allows calling it without an auth token for easier testing in this simple example. In production, you would want to secure this.)*

## Installation & Running the App

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the CLI Application:
   ```bash
   python -m app.cli
   ```
   Follow the interactive terminal prompts to create, read, update, and delete files and database records!
